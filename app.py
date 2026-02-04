from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
import pandas as pd
from werkzeug.security import check_password_hash
from config.old_config import (
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
from config import new_config


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
    template_name = "index_paid.html" if plan_type=="paid" else "index_free.html"

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

    csv_path = f"data/{file_key}_at.csv" if selected_mode=="AT" else f"data/{file_key}_cz.csv" if selected_mode=="CZ" else f"data/{file_key}_st.csv" if selected_mode=="ST" else f"data/{file_key}_rb.csv"
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
def generate_labels_from_mode_options(mode_options):
    """
    mode_options の内容からラベルを自動生成する
    ・1つ → at_gap は「未設定」
    ・2つ以上 → at_gap も含めて生成
    """

    display_map = {
        "ボーナス": "ボナ",
        "AT": "AT",
        "ST": "ST",
        "CZ": "CZ",
    }

    # 表示順を固定
    order = ["ボーナス", "CZ", "AT", "ST"]

    normalized = [m for m in order if m in mode_options]
    if not normalized:
        return {
            "mode": "未設定",
            "at_gap": "未設定",
            "prev_diff": "未設定",
            "prev_game": "未設定",
            "prev_coin": "未設定",
            "prev_renchan": "未設定",
            "prev_type": "未設定",
            "custom_condition": "機種別条件",
        }
    display_modes = [display_map[m] for m in normalized]

    mode_label = "/".join(display_modes)

    # mode_options が1つの場合
    if len(normalized) == 1:
        base = display_modes[0]
        return {
            "mode": base,
            "at_gap": "未設定",
            "prev_diff": f"{base}終了時差枚数",
            "prev_game": f"{base}当選G数",
            "prev_coin": f"{base}獲得枚数",
            "prev_renchan": f"{base}連荘数",
            "prev_type": f"{base}種別",
            "custom_condition": "機種別条件",
        }

    # mode_options が2つ以上の場合
    first = display_modes[0]
    second = display_modes[1]

    return {
        "mode": mode_label,
        "at_gap": f"{first}終了時{second}間G数",
        "prev_diff": f"{first}({second})終了時差枚数",
        "prev_game": f"{second}当選G数",
        "prev_coin": f"{second}獲得枚数",
        "prev_renchan": f"{second}連荘数",
        "prev_type": f"{second}種別",
        "custom_condition": "機種別条件",
    }



@app.route("/all", methods=["GET", "POST"])
def all_tool():
    MACHINE_CONFIGS = new_config.machine_configs
    MACHINE_SETTINGS = new_config.machine_settings

    # --- プルダウン用機種選択 ---
    default_machine = list(MACHINE_CONFIGS.keys())[0]

    if request.method == "POST":
        selected_machine = request.form.get("machine", default_machine)
    else:
        selected_machine = default_machine

    display_name = MACHINE_CONFIGS[selected_machine]["display_name"]


    # --- 安全に全設定を取得 ---
    settings                 = MACHINE_SETTINGS.get(display_name, {})
    mode_options             = settings.get("mode_options", [])
    through                  = settings.get("through", (0, 5, 1))      # min, max, step
    at_gap                   = settings.get("at_gap", (0, 1000, 50))
    prev_game                = settings.get("prev_game", (0, 2000, 50))
    prev_coin                = settings.get("prev_coin", (0, 3000, 100))
    prev_diff                = settings.get("prev_diff", (-3000, 3000, 100))
    prev_renchan             = settings.get("prev_renchan", (0, 10, 1))
    prev_type_options        = settings.get("prev_type_options", ["不問"])
    custom_condition_options = settings.get("custom_condition_options", ["不問"])
    labels                   = generate_labels_from_mode_options(mode_options)

    # --- POST処理 ---
    if request.method == "POST":
        # min/max を取得
        input_game = int(request.form.get("input_game", 0))  # ← 追加
        selected_through_min     = int(request.form.get("through_min", through[0]))
        selected_through_max     = int(request.form.get("through_max", through[1]))
        selected_at_gap_min      = int(request.form.get("at_gap_min", at_gap[0]))
        selected_at_gap_max      = int(request.form.get("at_gap_max", at_gap[1]))
        selected_prev_game_min   = int(request.form.get("prev_game_min", prev_game[0]))
        selected_prev_game_max   = int(request.form.get("prev_game_max", prev_game[1]))
        selected_prev_coin_min   = int(request.form.get("prev_coin_min", prev_coin[0]))
        selected_prev_coin_max   = int(request.form.get("prev_coin_max", prev_coin[1]))
        selected_prev_diff_min   = int(request.form.get("prev_diff_min", prev_diff[0]))
        selected_prev_diff_max   = int(request.form.get("prev_diff_max", prev_diff[1]))
        selected_prev_renchan_min = int(request.form.get("prev_renchan_min", prev_renchan[0]))
        selected_prev_renchan_max = int(request.form.get("prev_renchan_max", prev_renchan[1]))
        selected_prev_type       = request.form.get("prev_type")
        selected_custom_condition = request.form.get("custom_condition")
        
        # データ抽出処理などをここに書く
        result = f"Received: through {selected_through_min}-{selected_through_max}, AT間 {selected_at_gap_min}-{selected_at_gap_max}"
    else:
        # 初期値
        input_game = 0   # ← 追加
        selected_through_min     = through[0]
        selected_through_max     = through[1]
        selected_at_gap_min      = at_gap[0]
        selected_at_gap_max      = at_gap[1]
        selected_prev_game_min   = prev_game[0]
        selected_prev_game_max   = prev_game[1]
        selected_prev_coin_min   = prev_coin[0]
        selected_prev_coin_max   = prev_coin[1]
        selected_prev_diff_min   = prev_diff[0]
        selected_prev_diff_max   = prev_diff[1]
        selected_prev_renchan_min = prev_renchan[0]
        selected_prev_renchan_max = prev_renchan[1]
        selected_prev_type       = None
        selected_custom_condition = None
        result = None

    return render_template(
        "index_all.html",
        machine_name=display_name,
        selected_machine=selected_machine,
        display_names=[(k, v["display_name"]) for k, v in MACHINE_CONFIGS.items()],
        mode_options_map={selected_machine: mode_options},
        selected_mode=None,
        selected_time=None,
        input_game=input_game,   # ← 変更
        mode_options=mode_options,
        through=through,
        at_gap=at_gap,
        prev_game=prev_game,
        prev_coin=prev_coin,
        prev_diff=prev_diff,
        prev_renchan=prev_renchan,
        prev_type_options=prev_type_options,
        custom_condition_options=custom_condition_options,
        selected_through_min=selected_through_min,
        selected_through_max=selected_through_max,
        selected_at_gap_min=selected_at_gap_min,
        selected_at_gap_max=selected_at_gap_max,
        selected_prev_game_min=selected_prev_game_min,
        selected_prev_game_max=selected_prev_game_max,
        selected_prev_coin_min=selected_prev_coin_min,
        selected_prev_coin_max=selected_prev_coin_max,
        selected_prev_diff_min=selected_prev_diff_min,
        selected_prev_diff_max=selected_prev_diff_max,
        selected_prev_renchan_min=selected_prev_renchan_min,
        selected_prev_renchan_max=selected_prev_renchan_max,
        selected_prev_type=selected_prev_type,
        selected_custom_condition=selected_custom_condition,
        labels=labels,
        link_url=MACHINE_CONFIGS[selected_machine].get("link_url"),
        link_preview=None,
        result=result,
        error_msg=None,
        locked_field_map={},
        og_url=request.url,
        og_image=MACHINE_CONFIGS[selected_machine].get("og_image"),
        tw_image=None,
        machines=MACHINE_CONFIGS,
        machine_settings=MACHINE_SETTINGS
    )



# ================================
# 🔹 東リベツール（/toreve/tools）
# ================================
@app.route("/toreve/tools")
def toreve_tools():
    base = os.path.join(app.root_path, "static", "tools", "toreve")
    index_path = os.path.join(base, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(base, "index.html")
    abort(404)

# ================================
# 🔹 沖ドキツール（/okidoki/tools）
# ================================
@app.route("/okidoki/tools")
def okidoki_tools():
    base = os.path.join(app.root_path, "static", "tools", "okidoki")
    index_path = os.path.join(base, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(base, "index.html")
    abort(404)

# ================================
# 🔹 ツール一覧ページ（/list）
# ================================
@app.route("/list")
def tool_list():
    return render_template("tool_list.html")

# ==============================================================================
# アプリ起動
# ==============================================================================
if __name__ == "__main__":
    # ローカル検証時のみ debug=True にしてOK。公開時は False 推奨。
    app.run(debug=False)

