from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
import pandas as pd
from werkzeug.security import check_password_hash
from config.legacy import (
    machine_configs,
    machine_settings,
    TOOL_PASSWORDS,
    apply_free_custom_label_override,
)
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import traceback, werkzeug
from functools import lru_cache
from typing import Dict, Tuple, Optional
from datetime import timedelta
import time as _time

# =====================================================================
# Flask アプリ初期化
# =====================================================================
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=30)

# =====================================================================
# 認証・レートリミット
# =====================================================================
MAX_TRIES = 5
LOCK_SECONDS = 5 * 60

def _access_key(machine_key: str, plan_type: str) -> str:
    return f"{machine_key}:{plan_type}"

def is_authorized(machine_key: str, plan_type: str) -> bool:
    return session.get("tool_access", {}).get(_access_key(machine_key, plan_type), False)

def _tries_key(key: str) -> str:
    return f"tries:{key}"

def _lock_key(key: str) -> str:
    return f"lock:{key}"

def is_locked(key: str) -> Optional[float]:
    unlock_at = session.get(_lock_key(key))
    if unlock_at and time.time() < unlock_at:
        return unlock_at
    session.pop(_lock_key(key), None)
    return None

def record_fail(key: str) -> None:
    tries = session.get(_tries_key(key), 0) + 1
    session[_tries_key(key)] = tries
    if tries >= MAX_TRIES:
        session[_lock_key(key)] = time.time() + LOCK_SECONDS
        session[_tries_key(key)] = 0

def record_success(key: str) -> None:
    session.pop(_tries_key(key), None)
    session.pop(_lock_key(key), None)

# =====================================================================
# ログインページ
# =====================================================================
@app.route("/<machine_key>/<plan_type>/login", methods=["GET", "POST"])
def tool_login(machine_key, plan_type):
    if plan_type == "free":
        return redirect(url_for("machine_page", machine_key=machine_key, plan_type=plan_type))

    if machine_key not in machine_configs:
        return "無効なURLです", 404

    tool_pw_hash = (TOOL_PASSWORDS.get(machine_key) or {}).get(plan_type)
    if tool_pw_hash is None:
        flash("このツールは現在ロック中です。")
        return redirect(url_for("machine_page", machine_key=machine_key, plan_type="free"))

    cfg = machine_configs.get(machine_key, {}) or {}
    og_filename = cfg.get("og_image", "ogp.jpg")
    try:
        og_image = url_for("static", filename=og_filename, _external=True)
    except Exception:
        og_image = None
    tw_image = og_image

    key = _access_key(machine_key, plan_type)
    unlock_at = is_locked(key)
    if unlock_at:
        remain = int(unlock_at - time.time())
        flash(f"一時的にロック中です。あと {remain} 秒後に再試行できます。")
        return render_template("login.html",
                               machine_key=machine_key,
                               plan_type=plan_type,
                               og_url=request.url,
                               og_image=og_image,
                               tw_image=tw_image)

    if request.method == "GET":
        return render_template("login.html",
                               machine_key=machine_key,
                               plan_type=plan_type,
                               og_url=request.url,
                               og_image=og_image,
                               tw_image=tw_image)

    input_pw = (request.form.get("password") or "").strip()
    if not re.fullmatch(r"\d{4}", input_pw):
        flash("4桁の数字を入力してください。")
        record_fail(key)
        return render_template("login.html",
                               machine_key=machine_key,
                               plan_type=plan_type,
                               og_url=request.url,
                               og_image=og_image,
                               tw_image=tw_image)

    if check_password_hash(tool_pw_hash, input_pw):
        access = session.get("tool_access", {})
        access[key] = True
        session["tool_access"] = access
        record_success(key)
        return redirect(url_for("machine_page", machine_key=machine_key, plan_type=plan_type))
    else:
        record_fail(key)
        flash("パスワードが違います。")
        return render_template("login.html",
                               machine_key=machine_key,
                               plan_type=plan_type,
                               og_url=request.url,
                               og_image=og_image,
                               tw_image=tw_image)

# =====================================================================
# OGP / Twitter Card 取得（LRU+TTL）
# =====================================================================
def fetch_link_preview(url: str, timeout: int = 6):
    if not url:
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        def pick(*names):
            for n in names:
                el = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n})
                if el and el.get("content"):
                    return el["content"].strip()
            return None

        title = pick("og:title", "twitter:title") or (soup.title.string.strip() if soup.title else None)
        desc  = pick("og:description", "twitter:description", "description")
        image = pick("og:image", "twitter:image")
        site  = pick("og:site_name", "twitter:site")
        if image and image.startswith("//"):
            image = "https:" + image
        return {"url": url, "title": title or url, "description": desc or "", "image": image, "site_name": site or ""}
    except Exception:
        return {"url": url, "title": url, "description": "", "image": None, "site_name": ""}

_PREVIEW_TTL = 60*60

@lru_cache(maxsize=64)
def _cached_fetch_link_preview(url: str) -> Tuple[float, Optional[dict]]:
    data = fetch_link_preview(url)
    return (_time.time(), data)

def get_link_preview_cached(url: str) -> Optional[dict]:
    ts, data = _cached_fetch_link_preview(url)
    if _time.time() - ts > _PREVIEW_TTL:
        _cached_fetch_link_preview.cache_clear()
        ts, data = _cached_fetch_link_preview(url)
    return data

# =====================================================================
# CSV キャッシュ
# =====================================================================
DATA_CACHE: Dict[str, Tuple[float, pd.DataFrame]] = {}

def load_csv_cached(path: str, dtypes: Optional[dict] = None, usecols: Optional[list] = None) -> pd.DataFrame:
    mtime = os.path.getmtime(path)
    cache = DATA_CACHE.get(path)
    if cache and cache[0] == mtime:
        return cache[1]
    df = pd.read_csv(path, dtype=dtypes, usecols=usecols)
    DATA_CACHE[path] = (mtime, df)
    return df

# =====================================================================
# 条件処理ユーティリティ
# =====================================================================
def _normalize_range_str(s: str) -> str:
    return s.replace(",", "").replace("枚", "").replace("G","").replace("連","").replace("スルー","").strip()

def _to_numeric_condition(cond_str: str):
    s = _normalize_range_str(cond_str)
    if "～" in s:
        low, high = s.split("～")
        return ("between", int(low), int(high))
    if s.endswith("以下"):
        return ("le", int(s[:-2]), None)
    if s.endswith("以上"):
        return ("ge", int(s[:-2]), None)
    return ("eq", int(s), None)

def _apply_numeric_mask(series: pd.Series, cond_str: str) -> pd.Series:
    op, a, b = _to_numeric_condition(cond_str)
    if op == "between":
        return series.between(a,b)
    if op == "le":
        return series.le(a)
    if op == "ge":
        return series.ge(a)
    return series.eq(a)

def filter_dataframe(df, form, settings):
    exclude_games = settings["exclude_games"]
    mask = pd.Series(True, index=df.index)
    mask &= df["朝イチ"].eq(1 if form["time"]=="朝イチ" else 0)
    if form["through"] != "不問":
        mask &= _apply_numeric_mask(df["スルー回数"], form["through"])
    if form["at_gap"] != "不問":
        mask &= _apply_numeric_mask(df["AT間ゲーム数"], form["at_gap"])
    if form["prev_game"] != "不問":
        mask &= _apply_numeric_mask(df["前回当選ゲーム数"], form["prev_game"])
    if form["prev_coin"] != "不問":
        mask &= _apply_numeric_mask(df["前回獲得枚数"], form["prev_coin"])
    if form["prev_diff"] != "不問":
        mask &= _apply_numeric_mask(df["前回差枚数"], form["prev_diff"])
    if form["prev_renchan"] != "不問":
        mask &= _apply_numeric_mask(df["前回連荘数"], form["prev_renchan"])
    if form.get("prev_type") != "不問" and "前回種別" in df.columns:
        mask &= df["前回種別"].eq(form["prev_type"])
    if form.get("custom_condition") not in (None,"不問") and "機種別条件" in df.columns:
        mask &= _apply_numeric_mask(df["機種別条件"], form["custom_condition"])
    mask &= df["当該REGゲーム数"].ge(int(form["game"]) + exclude_games)
    return df.loc[mask]

# =====================================================================
# レガシーツールページ
# =====================================================================
@app.route("/<machine_key>/<plan_type>", methods=["GET","POST"])
def machine_page(machine_key, plan_type):
    if plan_type=="paid" and not is_authorized(machine_key, plan_type):
        return redirect(url_for("tool_login", machine_key=machine_key, plan_type=plan_type))
    if machine_key not in machine_configs:
        return "無効なURLです",404
    if plan_type not in ["paid","free"]:
        return "プラン種別が無効です",404

    config = machine_configs[machine_key]
    display_name = config["display_name"]
    file_key = config["file_key"]
    og_image = url_for("static", filename=config.get("og_image","ogp.jpg"), _external=True)
    link_url = config.get("link_url")
    settings = machine_settings[display_name]
    settings = apply_free_custom_label_override(settings, display_name, plan_type)
    link_preview = get_link_preview_cached(link_url) if link_url else None
    ASSET_REV = os.environ.get("ASSET_REV","20251007")
    tw_image = f"{og_image}?v={ASSET_REV}"
    template_name = "index_legacy_paid.html" if plan_type=="paid" else "index_legacy_free.html"

    # フォーム値
    if request.method=="POST":
        selected_mode = request.form.get("mode", settings["mode_options"][0])
        selected_time = request.form.get("time", "朝イチ")
        input_game = request.form.get("game","0")
        selected_through = request.form.get("through","不問")
        selected_at_gap = request.form.get("at_gap","不問")
        selected_prev_game = request.form.get("prev_game","不問")
        selected_prev_coin = request.form.get("prev_coin","不問")
        selected_prev_diff = request.form.get("prev_diff","不問")
        selected_prev_renchan = request.form.get("prev_renchan","不問")
        selected_prev_type = request.form.get("prev_type","不問")
        selected_custom_condition = request.form.get("custom_condition","不問")
    else:
        selected_mode = settings["mode_options"][0]
        selected_time = "朝イチ"
        input_game = "0"
        selected_through = selected_at_gap = selected_prev_game = selected_prev_coin = selected_prev_diff = selected_prev_renchan = selected_prev_type = selected_custom_condition = "不問"

    csv_path = f"data/{file_key}_at.csv" if selected_mode=="AT" else f"data/{file_key}_cz.csv" if selected_mode=="CZ" else f"data/{file_key}_rb.csv"
    try:
        dtypes = {
            "朝イチ": "int8",
            "スルー回数": "int16",
            "AT間ゲーム数": "int32",
            "前回当選ゲーム数": "int32",
            "前回獲得枚数": "int32",
            "前回差枚数": "int32",
            "前回連荘数": "int16",
            "当該REGゲーム数": "int32",
            "REGゲーム数": "float32",
            "ATゲーム数": "float32",
            "REG枚数": "float32",
            "AT枚数": "float32",
        }
        df = load_csv_cached(csv_path, dtypes=dtypes)
    except Exception as e:
        return render_template(template_name, error_msg=f"CSV読み込みエラー: {e}", result=None, labels=settings.get("labels",{}))

    form = {
        "time": selected_time,
        "through": selected_through,
        "at_gap": selected_at_gap,
        "prev_game": selected_prev_game,
        "prev_coin": selected_prev_coin,
        "prev_diff": selected_prev_diff,
        "prev_renchan": selected_prev_renchan,
        "prev_type": selected_prev_type,
        "game": int(input_game),
        "custom_condition": selected_custom_condition
    }

    filtered_df = filter_dataframe(df, form, settings)

    if not filtered_df.empty and len(filtered_df) >= 100:
        count = len(filtered_df)
        avg_reg_games = filtered_df["REGゲーム数"].mean()
        avg_at_games = filtered_df["ATゲーム数"].mean()
        avg_reg_coins = filtered_df["REG枚数"].mean()
        avg_at_coins = filtered_df["AT枚数"].mean()
        hatsu_atari = max(avg_reg_games - int(input_game),0)
        avg_diff = avg_at_coins + avg_reg_coins - (hatsu_atari*50/settings["coin_moti"])
        avg_in = (hatsu_atari + avg_at_games)*3
        avg_out = avg_diff + avg_in
        payout_rate = (avg_out/avg_in)*100 if avg_in else 0
        expected_value = avg_diff*20
        result = {
            "件数": f"{count:,}件",
            "平均REGゲーム数": f"1/{hatsu_atari:,.1f}",
            "平均AT枚数": f"{avg_at_coins:,.1f}枚",
            "機械割": f"{payout_rate:,.1f}%",
            "期待値": f"{expected_value:,.0f}円"
        }
    elif len(filtered_df)<100:
        result = "サンプル不足"
    else:
        result = None

    if request.method=="GET":
        result = None

    locked_field_map = {
        cfg["display_name"]: machine_settings[cfg["display_name"]].get("locked_fields", [])
        for cfg in machine_configs.values()
    }

    return render_template(template_name,
                           url_path=f"{machine_key}/{plan_type}",
                           machine_name=display_name,
                           mode_options_map={machine_key: settings["mode_options"]},
                           selected_mode=selected_mode,
                           selected_time=selected_time,
                           input_game=input_game,
                           mode_options=settings["mode_options"],
                           through_options=settings["through_options"],
                           at_gap_options=settings["at_gap_options"],
                           prev_game_options=settings["prev_game_options"],
                           prev_coin_options=settings["prev_coin_options"],
                           prev_diff_options=settings["prev_diff_options"],
                           prev_renchan_options=settings["prev_renchan_options"],
                           prev_type_options=settings["prev_type_options"],
                           selected_through=selected_through,
                           selected_at_gap=selected_at_gap,
                           selected_prev_game=selected_prev_game,
                           selected_prev_coin=selected_prev_coin,
                           selected_prev_diff=selected_prev_diff,
                           selected_prev_renchan=selected_prev_renchan,
                           selected_prev_type=selected_prev_type,
                           labels=settings.get("labels", {}),
                           link_url=link_url,
                           link_preview=link_preview,
                           result=result,
                           error_msg=None,
                           selected_custom_condition=selected_custom_condition,
                           custom_condition_options=settings.get("custom_condition_options", ["不問"]),
                           locked_field_map=locked_field_map,
                           og_url=request.url,
                           og_image=og_image,
                           tw_image=tw_image
    )

# =====================================================================
# 新ツールページ
# =====================================================================
from config import new as new_config

@app.route("/tool/<machine_key>", methods=["GET","POST"])
def new_tool(machine_key):
    if machine_key not in new_config.machines:
        return "無効なURLです",404
    cfg = new_config.machines[machine_key]

    if request.method=="POST":
        selected_mode = request.form.get("mode", cfg["mode_options"][0])
        input_game = request.form.get("game","0")
    else:
        selected_mode = cfg["mode_options"][0]
        input_game = "0"

    csv_path = f"data/{cfg['file_key']}.csv"
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return render_template("index_new.html",
                               machine_name=cfg["display_name"],
                               selected_mode=selected_mode,
                               input_game=input_game,
                               mode_options=cfg["mode_options"],
                               result=None,
                               error_msg=f"CSV読み込みエラー: {e}")

    filtered_df = df[df["ゲーム数"]>=int(input_game)]

    result = None
    if not filtered_df.empty:
        result = {
            "件数": len(filtered_df),
            "平均値": filtered_df["差枚"].mean()
        }

    return render_template("index_new.html",
                           machine_name=cfg["display_name"],
                           selected_mode=selected_mode,
                           input_game=input_game,
                           mode_options=cfg["mode_options"],
                           result=result,
                           error_msg=None)

# =====================================================================
# 新ツール静的
# =====================================================================
@app.route("/toreve/tools")
def toreve_tools():
    tools_dir = os.path.join(app.root_path, "static/tools")
    if not os.path.exists(tools_dir):
        abort(404)
    return send_from_directory(tools_dir, "index.html")

# =====================================================================
# 静的ファイル配信
# =====================================================================
@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, "static"), filename)

# =====================================================================
# エラーハンドラー
# =====================================================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

# ==============================================================================
# アプリ起動
# ==============================================================================
if __name__ == "__main__":
    # ローカル検証時のみ debug=True にしてOK。公開時は False 推奨。
    app.run(debug=False)

