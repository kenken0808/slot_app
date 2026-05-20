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
def fetch_link_preview(url: str, machine_name: str = "攻略メモ", timeout: int = 6):
    if not url:
        return None

    # ★ memo系は固定表示（スクレイピングしない）
    if "127.0.0.1" in url or "/memo/" in url:
        return {
            "url": url,
            "title": f"{machine_name}｜攻略メモ",
            "description": "",
            "image": None,
            "site_name": ""
        }

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

        title = (
            pick("og:title", "twitter:title")
            or (soup.title.string.strip() if soup.title and soup.title.string else None)
        )

        desc  = pick("og:description", "twitter:description", "description")
        image = pick("og:image", "twitter:image")
        site  = pick("og:site_name", "twitter:site")

        if image and image.startswith("//"):
            image = "https:" + image

        # ★フォールバック
        if not title:
            title = f"{machine_name}｜攻略メモ"

        return {
            "url": url,
            "title": title,
            "description": desc or "",
            "image": image,
            "site_name": site or ""
        }

    except Exception:
        return {
            "url": url,
            "title": f"{machine_name}｜攻略メモ",
            "description": "",
            "image": None,
            "site_name": ""
        }

_PREVIEW_TTL = 60*60

@lru_cache(maxsize=64)
def _cached_fetch_link_preview(url: str, machine_name: str):
    data = fetch_link_preview(url, machine_name)
    return (_time.time(), data)

def get_link_preview_cached(url: str, machine_name: str = "攻略メモ") -> Optional[dict]:
    ts, data = _cached_fetch_link_preview(url, machine_name)

    if _time.time() - ts > _PREVIEW_TTL:
        _cached_fetch_link_preview.cache_clear()
        ts, data = _cached_fetch_link_preview(url, machine_name)

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

@app.route("/api/default_values")
def api_default_values():

    machine = request.args.get("")

    # =========================
    # ❗ machineチェック
    # =========================
    cfg = new_config.machine_configs.get(machine)

    if not cfg:
        return jsonify({"error": "invalid machine"}), 400

    if "settings" not in cfg:
        return jsonify({"error": "settings missing"}), 400

    settings = cfg["settings"]

    defaults = get_default_values(settings.get("mode_options", []))

    return jsonify({
        "mode": defaults["mode"],
        "time": defaults["time"],
        "game": defaults["game"],

        "through": defaults["through"],
        "at_gap": defaults["at_gap"],
        "prev_game": defaults["prev_game"],
        "prev_coin": defaults["prev_coin"],
        "prev_diff": defaults["prev_diff"],
        "prev_renchan": defaults["prev_renchan"],
    })

def filter_dataframe_v2(df, form, settings):

    print("========== FILTER DEBUG START ==========")
    print("rows start:", len(df))
    print("form:", form)

    mask = pd.Series(True, index=df.index)

    # =========================
    # 朝イチ
    # =========================
    time_value = form.get("time")

    if time_value == "朝イチ":
        mask &= df["朝イチ"].eq(1)
    elif time_value == "朝イチ以外":
        mask &= df["朝イチ"].eq(0)

    print("after 朝イチ:", mask.sum())

    # =========================
    # range共通（安全化）
    # =========================
    def apply_range(column, key):

        val = form.get(key)

        if not val or len(val) != 3:
            return pd.Series(True, index=df.index)

        min_v, max_v, extra_v = val

        if min_v == 0 and max_v == 0 and extra_v is None:
            return pd.Series(True, index=df.index)

        mask = df[column].between(min_v, max_v)

        if extra_v is not None:
            mask |= (df[column] == extra_v)

        return mask

    mask &= apply_range("スルー回数", "through")
    mask &= apply_range("AT間ゲーム数", "at_gap")
    mask &= apply_range("前回当選ゲーム数", "prev_game")
    mask &= apply_range("前回獲得枚数", "prev_coin")
    mask &= apply_range("前回差枚数", "prev_diff")
    mask &= apply_range("前回連荘数", "prev_renchan")

    # =========================
    # 文字列条件（安全）
    # =========================
    if form.get("prev_type") and form.get("prev_type") != "不問":
        mask &= df["前回種別"].eq(form["prev_type"])

    if form.get("custom_condition") and form.get("custom_condition") != "不問":
        mask &= df["機種別条件"].eq(form["custom_condition"])

    # =========================
    # ゲーム数
    # =========================
    try:
        game = int(form.get("game", 0))
    except:
        game = 0

    exclude_games = settings.get("exclude_games", 0)

    mask &= df["当該REGゲーム数"].ge(game + exclude_games)

    print("after ゲーム数:", mask.sum())
    print("========== FILTER DEBUG END ==========")

    return df.loc[mask]

def generate_labels_from_mode_options(mode_options):

    display_map = {
        "ボーナス": "ボナ",
        "AT": "AT",
        "ST": "ST",
        "CZ": "CZ",
    }

    # 🔥order完全削除 → mode_optionsをそのまま使う
    normalized = [m for m in mode_options if m in display_map]

    if not normalized:
        return {
            "mode": "未設定",
            "at_gap": "未設定",
            "prev_diff": "未設定",
            "prev_game": "未設定",
            "prev_coin": "未設定",
            "prev_renchan": "未設定",
            "prev_type": "未設定",
            "custom_condition": "未設定",
        }

    display_modes = [display_map[m] for m in normalized]
    mode_label = "／".join(display_modes)

    if len(display_modes) == 1:
        base = display_modes[0]
        return {
            "mode": base,
            "at_gap": f"前回***終了時{base}間G数",
            "prev_diff": f"前回{base}終了時差枚数",
            "prev_game": f"前回{base}当選G数",
            "prev_coin": f"前回{base}獲得枚数",
            "prev_renchan": f"前回{base}連荘数",
            "prev_type": f"前回{base}種別",
            "custom_condition": "機種別条件",
        }

    first = display_modes[0]
    second = display_modes[1]

    return {
        "mode": mode_label,
        "at_gap": f"前回{first}終了時{second}間G数",
        "prev_diff": f"前回{second}終了時差枚数",
        "prev_game": f"前回{second}当選G数",
        "prev_coin": f"前回{second}獲得枚数",
        "prev_renchan": f"前回{second}連荘数",
        "prev_type": f"前回{second}種別",
        "custom_condition": "機種別条件",
    }


def mode_to_csv_suffix(mode: str) -> str:
    """
    UIモード → CSV suffix変換
    """
    mapping = {
        "ボーナス": "rb",
        "AT": "at",
        "CZ": "cz",
        "ST": "st",
    }
    return mapping.get(mode, "rb")




def get_default_values(mode_options):
    return {
        "machine": "",
        "mode": mode_options[0] if mode_options else "ボーナス",
        "time": "朝イチ",
        "game": 0,

        "through": (0, 0, 1, None),
        "at_gap": (0, 0, 100, None),
        "prev_game": (0, 0, 100, None),
        "prev_coin": (0, 0, 100, None),
        "prev_diff": (0, 0, 100, None),
        "prev_renchan": (0, 0, 1, None),

        "prev_type": "不問",
        "custom_condition": "不問",
    }


# =========================
# 攻略メモページ
# =========================
@app.route("/memo/<machine>")
def memo(machine):
    return render_template(f"memo/{machine}.html")


@app.route("/all", methods=["GET", "POST"])
def all_tool():
    MACHINE_CONFIGS = new_config.machine_configs

    # =========================
    # 機種選択
    # =========================
    default_machine = list(MACHINE_CONFIGS.keys())[0]

    selected_machine = (
        request.args.get("machine")
        or request.form.get("machine")
        or default_machine
    )

    # =========================
    # ★ここ修正（display_nameちゃんと入れる）
    # =========================
    display_name = ""
    settings = {}
    links = []

    if selected_machine in MACHINE_CONFIGS:
        cfg = MACHINE_CONFIGS[selected_machine]

        display_name = cfg.get("display_name", "")   # ←ここ重要
        settings = cfg.get("settings", {})
        links = cfg.get("links", [])
        print("DEBUG display_name =", display_name)

    # =========================
    # リンク処理
    # =========================
    link_previews = []

    for item in links:
        url = item.get("link_url")
        if not url:
            continue

        preview = get_link_preview_cached(url, display_name)

        if preview:
            preview["og_image_local"] = item.get("og_image")
            preview["display_title"] = preview.get("title") or f"{display_name}｜攻略メモ"
            link_previews.append(preview)

    # =========================
    # モード関連
    # =========================
    mode_options = settings.get("mode_options", [])

    defaults = get_default_values(mode_options)
    labels = generate_labels_from_mode_options(mode_options)




    # =========================
    # モード・基本入力
    # =========================
    mode_options = settings.get("mode_options", [])

    selected_mode = request.form.get("mode", defaults["mode"])
    selected_time = request.form.get("time", defaults["time"])

    try:
        input_game = int(request.form.get("game", defaults["game"]))
    except:
        input_game = defaults["game"]

    selected_prev_type = request.form.get("prev_type", "不問")
    selected_custom_condition = request.form.get("custom_condition", "不問")

    # =========================
    # min/max（安全変換）
    # =========================
    def get_int(name, default):
        v = request.form.get(name, None)

        if v is None or v == "":
            return default

        try:
            return int(v)
        except:
            return default

    selected_through_min = get_int("through_min", defaults["through"][0])
    selected_through_max = get_int("through_max", defaults["through"][1])
    selected_through_extra = get_int("through_extra", defaults["through"][3])

    selected_at_gap_min = get_int("at_gap_min", defaults["at_gap"][0])
    selected_at_gap_max = get_int("at_gap_max", defaults["at_gap"][1])
    selected_at_gap_extra = get_int("at_gap_extra", defaults["at_gap"][3])

    selected_prev_game_min = get_int("prev_game_min", defaults["prev_game"][0])
    selected_prev_game_max = get_int("prev_game_max", defaults["prev_game"][1])
    selected_prev_game_extra = get_int("prev_game_extra", defaults["prev_game"][3])

    selected_prev_coin_min = get_int("prev_coin_min", defaults["prev_coin"][0])
    selected_prev_coin_max = get_int("prev_coin_max", defaults["prev_coin"][1])
    selected_prev_coin_extra = get_int("prev_coin_extra", defaults["prev_coin"][3])

    selected_prev_diff_min = get_int("prev_diff_min", defaults["prev_diff"][0])
    selected_prev_diff_max = get_int("prev_diff_max", defaults["prev_diff"][1])
    selected_prev_diff_extra = get_int("prev_diff_extra", defaults["prev_diff"][3])

    selected_prev_renchan_min = get_int("prev_renchan_min", defaults["prev_renchan"][0])
    selected_prev_renchan_max = get_int("prev_renchan_max", defaults["prev_renchan"][1])
    selected_prev_renchan_extra = get_int("prev_renchan_extra", defaults["prev_renchan"][3])

    # =========================
    # UIレンジ（★必ず存在させる）
    # =========================
    through = settings.get("through", (0, 5, 1, None))
    at_gap = settings.get("at_gap", (0, 1000, 50, None))
    prev_game = settings.get("prev_game", (0, 2000, 50, None))
    prev_coin = settings.get("prev_coin", (0, 3000, 100, None))
    prev_diff = settings.get("prev_diff", (-3000, 3000, 100, None))
    prev_renchan = settings.get("prev_renchan", (0, 10, 1, None))

    # =========================
    # select用valueリスト生成
    # =========================
    def build_values(cfg):
        start, end, step = cfg[:3]

        values = list(range(start, end + 1, step))

        # extra値追加
        if len(cfg) >= 4 and cfg[3] is not None:
            if cfg[3] not in values:
                values.append(cfg[3])

        return sorted(values)

    through_values = build_values(through)
    at_gap_values = build_values(at_gap)
    prev_game_values = build_values(prev_game)
    prev_coin_values = build_values(prev_coin)
    prev_diff_values = build_values(prev_diff)
    prev_renchan_values = build_values(prev_renchan)

    # =========================
    # CSV（未選択でも落ちない）
    # =========================
    if not selected_machine or selected_machine not in MACHINE_CONFIGS:
        return render_template(
            "index_all.html",
            machine_name=display_name or "",
            selected_machine=None,
            display_names=[(k, v["display_name"]) for k, v in MACHINE_CONFIGS.items()],

            mode_options=[],
            selected_mode="",
            selected_time="朝イチ",
            input_game=0,

            through=through,
            at_gap=at_gap,
            prev_game=prev_game,
            prev_coin=prev_coin,
            prev_diff=prev_diff,
            prev_renchan=prev_renchan,

            selected_through_min=0,
            selected_through_max=0,
            selected_at_gap_min=0,
            selected_at_gap_max=0,
            selected_prev_game_min=0,
            selected_prev_game_max=0,
            selected_prev_coin_min=0,
            selected_prev_coin_max=0,
            selected_prev_diff_min=0,
            selected_prev_diff_max=0,
            selected_prev_renchan_min=0,
            selected_prev_renchan_max=0,

            selected_prev_type="不問",
            selected_custom_condition="不問",

            through_values=through_values,
            at_gap_values=at_gap_values,
            prev_game_values=prev_game_values,
            prev_coin_values=prev_coin_values,
            prev_diff_values=prev_diff_values,
            prev_renchan_values=prev_renchan_values,

            prev_type_options=[],
            custom_condition_options=[],

            labels=labels,
            result=None,
            error_msg="機種が未選択です",

            machines=MACHINE_CONFIGS,
            machine_configs=MACHINE_CONFIGS,
            link_previews=link_previews
        )

    # =========================
    # CSV読み込み
    # =========================
    file_key = MACHINE_CONFIGS[selected_machine]["file_key"]
    csv_suffix = mode_to_csv_suffix(selected_mode) or "rb"
    csv_path = f"data/{file_key}_{csv_suffix}.csv"

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
        return render_template(
            "index_all.html",
            machine_name=display_name,
            selected_machine=selected_machine,
            display_names=[(k, v["display_name"]) for k, v in MACHINE_CONFIGS.items()],
            mode_options=mode_options,

            through=through,
            at_gap=at_gap,
            prev_game=prev_game,
            prev_coin=prev_coin,
            prev_diff=prev_diff,
            prev_renchan=prev_renchan,

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

            through_values=through_values,
            at_gap_values=at_gap_values,
            prev_game_values=prev_game_values,
            prev_coin_values=prev_coin_values,
            prev_diff_values=prev_diff_values,
            prev_renchan_values=prev_renchan_values,

            prev_type_options=settings.get("prev_type_options", []),
            custom_condition_options=settings.get("custom_condition_options", []),

            labels=labels,
            result=None,
            error_msg=f"CSV読み込みエラー: {e}",

            machines=MACHINE_CONFIGS,
            machine_configs=MACHINE_CONFIGS,
            link_previews=link_previews
        )

    # =========================
    # form
    # =========================
    form = {
        "time": selected_time,
        "game": input_game,

        "through": (
            selected_through_min,
            selected_through_max,
            selected_through_extra
        ),

        "at_gap": (
            selected_at_gap_min,
            selected_at_gap_max,
            selected_at_gap_extra
        ),

        "prev_game": (
            selected_prev_game_min,
            selected_prev_game_max,
            selected_prev_game_extra
        ),

        "prev_coin": (
            selected_prev_coin_min,
            selected_prev_coin_max,
            selected_prev_coin_extra
        ),

        "prev_diff": (
            selected_prev_diff_min,
            selected_prev_diff_max,
            selected_prev_diff_extra
        ),

        "prev_renchan": (
            selected_prev_renchan_min,
            selected_prev_renchan_max,
            selected_prev_renchan_extra
        ),

        "prev_type": selected_prev_type,
        "custom_condition": selected_custom_condition
    }

    # =========================
    # フィルタ
    # =========================
    filtered_df = filter_dataframe_v2(df, form, settings)
    print("========== DEBUG START ==========")
    print("machine:", selected_machine)
    print("mode:", selected_mode)
    print("form:", form)
    print("csv rows:", len(df))
    print("filtered rows:", len(filtered_df))
    print("========== DEBUG END ==========")

    print("filtered rows:", len(filtered_df))

    # 0件のとき原因確認
    if len(filtered_df) == 0:
        print("---- SAMPLE DATA CHECK ----")
        print(df.head(3))
        print("columns:", df.columns.tolist())

        # 代表条件のヒット確認（重要）
        print("朝イチ分布:", df["朝イチ"].value_counts().to_dict())
        print("REG最大値:", df["当該REGゲーム数"].max())

    print("========== DEBUG END ==========")

    # =========================
    # 計算
    # =========================
    result = None

    if request.method == "POST" and not filtered_df.empty and len(filtered_df) >= 100:

        count = len(filtered_df)

        avg_reg_games = filtered_df["REGゲーム数"].mean()
        avg_at_games = filtered_df["ATゲーム数"].mean()
        avg_reg_coins = filtered_df["REG枚数"].mean()
        avg_at_coins = filtered_df["AT枚数"].mean()

        hatsu_atari = max(avg_reg_games - input_game, 0)

        avg_diff = avg_at_coins + avg_reg_coins - (
            hatsu_atari * 50 / settings.get("coin_moti", 1)
        )

        avg_in = (hatsu_atari + avg_at_games) * 3
        avg_out = avg_diff + avg_in

        payout_rate = (avg_out / avg_in) * 100 if avg_in else 0
        expected_value = avg_diff * 20

        result = {
            "件数　　　": f"{count:,}件",
            "初当たり　": f"1/{hatsu_atari:,.1f}",
            "獲得枚数　": f"{avg_at_coins:,.1f}枚",
            "機械割　　": f"{payout_rate:,.1f}%",
            "期待値　　": f"{expected_value:,.0f}円"
        }

    # =========================
    # render（★全変数必ず存在）
    # =========================
    return render_template(
        "index_all.html",

        machine_name=display_name,
        selected_machine=selected_machine,
        display_names=[(k, v["display_name"]) for k, v in MACHINE_CONFIGS.items()],

        mode_options=mode_options,
        selected_mode=selected_mode,
        selected_time=selected_time,
        input_game=input_game,

        through=through,
        at_gap=at_gap,
        prev_game=prev_game,
        prev_coin=prev_coin,
        prev_diff=prev_diff,
        prev_renchan=prev_renchan,

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

        through_values=through_values,
        at_gap_values=at_gap_values,
        prev_game_values=prev_game_values,
        prev_coin_values=prev_coin_values,
        prev_diff_values=prev_diff_values,
        prev_renchan_values=prev_renchan_values,

        prev_type_options=settings.get("prev_type_options", []),
        custom_condition_options=settings.get("custom_condition_options", []),

        labels=labels,
        result=result,
        error_msg=None,

        machines=MACHINE_CONFIGS,
        machine_configs=MACHINE_CONFIGS,
        link_previews=link_previews
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
    # app.run(debug=True, use_reloader=True)

