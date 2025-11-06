from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, abort
import pandas as pd
from werkzeug.security import check_password_hash
from config import machine_configs, machine_settings, TOOL_PASSWORDS, apply_free_custom_label_override
from bs4 import BeautifulSoup
import requests
import re
import time
import os
import traceback, werkzeug

# 追加インポート（最適化）
from functools import lru_cache
from typing import Dict, Tuple, Optional
from datetime import timedelta
import time as _time


# ==============================================================================
# Flask アプリ初期化
# ==============================================================================
app = Flask(__name__)

# 本番は Render の環境変数（Env Vars）に SECRET_KEY を設定してここで読み込む
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

# 本番を想定した Cookie 設定（HTTPS 前提）
app.config.update(
    SESSION_COOKIE_SECURE=True,     # HTTPS のみで送信
    SESSION_COOKIE_HTTPONLY=True,   # JS から参照不可
    SESSION_COOKIE_SAMESITE="Lax",  # CSRF 軽減
)

# /static 配下を強キャッシュ（ASSET_REV クエリで破棄可能）
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=30)


# ==============================================================================
# 認証・レートリミット（セッションベースの簡易実装）
# ==============================================================================
MAX_TRIES = 5          # 失敗回数の上限
LOCK_SECONDS = 5 * 60  # ロック時間（秒）

def _access_key(machine_key: str, plan_type: str) -> str:
    """機種＋プランを一意に表すキー（例: 'magireco:paid'）を返す。"""
    return f"{machine_key}:{plan_type}"

def is_authorized(machine_key: str, plan_type: str) -> bool:
    """当該ツールの認証済みフラグをセッションから取得する。"""
    return session.get("tool_access", {}).get(_access_key(machine_key, plan_type), False)

def _tries_key(key: str) -> str:
    """失敗回数カウンタ用のセッションキー名。"""
    return f"tries:{key}"

def _lock_key(key: str) -> str:
    """ロック解除予定時刻（epoch）格納用のセッションキー名。"""
    return f"lock:{key}"

def is_locked(key: str) -> Optional[float]:
    """
    ロック中なら解除予定時刻（epoch）を返す。未ロックなら None。
    ロックが切れていればセッションからロック情報を削除する。
    """
    unlock_at = session.get(_lock_key(key))
    if unlock_at and time.time() < unlock_at:
        return unlock_at
    session.pop(_lock_key(key), None)
    return None

def record_fail(key: str) -> None:
    """失敗回数をカウントし、上限到達で一定時間ロックする。"""
    tries = session.get(_tries_key(key), 0) + 1
    session[_tries_key(key)] = tries
    if tries >= MAX_TRIES:
        session[_lock_key(key)] = time.time() + LOCK_SECONDS
        session[_tries_key(key)] = 0  # 上限到達時はカウンタをリセット

def record_success(key: str) -> None:
    """成功時に失敗カウンタ・ロック状態をクリアする。"""
    session.pop(_tries_key(key), None)
    session.pop(_lock_key(key), None)


# ==============================================================================
# ログインページ（有料ページの前に通過） — 元のシンプル版
# ==============================================================================
@app.route("/<machine_key>/<plan_type>/login", methods=["GET", "POST"])
def tool_login(machine_key, plan_type):
    import re, time, os

    # free は認証不要
    if plan_type == "free":
        return redirect(url_for("machine_page", machine_key=machine_key, plan_type=plan_type))

    # 機種キー妥当性（任意：不正URLは404）
    if machine_key not in machine_configs:
        return "無効なURLです", 404

    # ツール PIN（ハッシュ）を取得（未設定なら free へ誘導）
    tool_pw_hash = (TOOL_PASSWORDS.get(machine_key) or {}).get(plan_type)
    if tool_pw_hash is None:
        flash("このツールは現在ロック中です。")
        return redirect(url_for("machine_page", machine_key=machine_key, plan_type="free"))

    # og画像（テンプレの未定義を避けるために毎回用意）
    cfg = machine_configs.get(machine_key, {}) or {}
    og_filename = cfg.get("og_image", "ogp.jpg")
    try:
        og_image = url_for("static", filename=og_filename, _external=True)
    except Exception:
        og_image = None
    tw_image = og_image

    key = _access_key(machine_key, plan_type)

    # ロック中チェック
    unlock_at = is_locked(key)
    if unlock_at:
        remain = int(unlock_at - time.time())
        flash(f"一時的にロック中です。あと {remain} 秒後に再試行できます。")
        return render_template(
            "login.html",
            machine_key=machine_key,
            plan_type=plan_type,
            og_url=request.url,
            og_image=og_image,
            tw_image=tw_image,
        )

    # GET：画面表示
    if request.method == "GET":
        return render_template(
            "login.html",
            machine_key=machine_key,
            plan_type=plan_type,
            og_url=request.url,
            og_image=og_image,
            tw_image=tw_image,
        )

    # POST：シンプルな照合
    input_pw = (request.form.get("password") or "").strip()
    if not re.fullmatch(r"\d{4}", input_pw):
        flash("4桁の数字を入力してください。")
        record_fail(key)
        return render_template(
            "login.html",
            machine_key=machine_key,
            plan_type=plan_type,
            og_url=request.url,
            og_image=og_image,
            tw_image=tw_image,
        )

    if check_password_hash(tool_pw_hash, input_pw):
        access = session.get("tool_access", {})
        access[key] = True
        session["tool_access"] = access
        record_success(key)
        return redirect(url_for("machine_page", machine_key=machine_key, plan_type=plan_type))
    else:
        record_fail(key)
        flash("パスワードが違います。")
        return render_template(
            "login.html",
            machine_key=machine_key,
            plan_type=plan_type,
            og_url=request.url,
            og_image=og_image,
            tw_image=tw_image,
        )


# ==============================================================================
# 外部リンクの OGP / Twitter Card を取得してプレビュー用情報に整形（+ LRU+TTL）
# ==============================================================================
def fetch_link_preview(url: str, timeout: int = 6):
    if not url:
        return None
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/119.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        html = resp.text
        soup = BeautifulSoup(html, "html.parser")

        def pick(*names):
            # og:* / twitter:* / 汎用meta の順で探す
            for n in names:
                el = soup.find("meta", attrs={"property": n}) or soup.find("meta", attrs={"name": n})
                if el and el.get("content"):
                    return el["content"].strip()
            return None

        title = pick("og:title", "twitter:title") or (soup.title.string.strip() if soup.title else None)
        desc  = pick("og:description", "twitter:description", "description")
        image = pick("og:image", "twitter:image")
        site  = pick("og:site_name", "twitter:site")

        # 簡単な正規化
        if image and image.startswith("//"):
            image = "https:" + image

        return {
            "url": url,
            "title": title or url,
            "description": desc or "",
            "image": image,          # 画像が無い場合は None のまま
            "site_name": site or "",
        }
    except Exception:
        return {"url": url, "title": url, "description": "", "image": None, "site_name": ""}

# LRU + TTL（1時間）
_PREVIEW_TTL = 60 * 60  # 1時間

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


# ==============================================================================
# CSV 読み込み（mtime 監視つきメモリキャッシュ）
# ==============================================================================
DATA_CACHE: Dict[str, Tuple[float, pd.DataFrame]] = {}  # {path: (mtime, df)}

def load_csv_cached(path: str, dtypes: Optional[dict] = None, usecols: Optional[list] = None) -> pd.DataFrame:
    """ファイルの mtime が変わらない限りメモリ上の DataFrame を返す"""
    mtime = os.path.getmtime(path)  # FileNotFoundError は上位で拾う
    cache = DATA_CACHE.get(path)
    if cache and cache[0] == mtime:
        return cache[1]
    # 読み込み最適化
    df = pd.read_csv(path, dtype=dtypes, usecols=usecols)
    DATA_CACHE[path] = (mtime, df)
    return df


# ==============================================================================
# ユーティリティ：条件文字列のパース（ベクトル化用）
# ==============================================================================
def _normalize_range_str(s: str) -> str:
    # 余計な単位・カンマを落として正規化
    return (
        s.replace(",", "")
         .replace("枚", "")
         .replace("G", "")
         .replace("連", "")
         .replace("スルー", "")
         .strip()
    )

def _to_numeric_condition(cond_str: str):
    """
    '100～200' → ('between', 100, 200)
    '300以下'  → ('le', 300, None)
    '50以上'   → ('ge', 50, None)
    '3'        → ('eq', 3, None)
    """
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
        return series.between(a, b)
    if op == "le":
        return series.le(a)
    if op == "ge":
        return series.ge(a)
    return series.eq(a)


# ==============================================================================
# データ抽出フィルタリング（ベクトル化）
# ==============================================================================
def filter_dataframe(df, form, settings):
    """
    受け取ったフォーム条件に基づき DataFrame をフィルタリングする。
    除外ゲーム数は settings["exclude_games"] を利用。
    """
    exclude_games = settings["exclude_games"]

    # 条件の積み上げ（全行 True から開始）
    mask = pd.Series(True, index=df.index)

    # 朝イチ（1）／それ以外（0）
    mask &= df["朝イチ"].eq(1 if form["time"] == "朝イチ" else 0)

    # 各条件（"不問" でなければ適用）— ベクトル演算
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

    if form.get("custom_condition") not in (None, "不問") and "機種別条件" in df.columns:
        mask &= _apply_numeric_mask(df["機種別条件"], form["custom_condition"])

    # 当該 REG ゲーム数の下限（打ち出し + 除外）
    mask &= df["当該REGゲーム数"].ge(int(form["game"]) + exclude_games)

    return df.loc[mask]


# ==============================================================================
# ツール本体ページ（free / paid）
# ==============================================================================
@app.route("/<machine_key>/<plan_type>", methods=["GET", "POST"])
def machine_page(machine_key, plan_type):
    """
    /<machine_key>/<plan_type>
      - free: 認証不要
      - paid: 未認証なら /login へリダイレクト
      - POST/GET に応じて計算＆描画
    """
    # paid は未認証ならログインへ
    if plan_type == "paid" and not is_authorized(machine_key, plan_type):
        return redirect(url_for("tool_login", machine_key=machine_key, plan_type=plan_type))

    # ルート妥当性チェック
    if machine_key not in machine_configs:
        return "無効なURLです", 404
    if plan_type not in ["paid", "free"]:
        return "プラン種別が無効です", 404

    # 機種設定の取得
    config = machine_configs[machine_key]
    display_name = config["display_name"]
    file_key = config["file_key"]
    og_image = url_for("static", filename=config.get("og_image", "ogp.jpg"), _external=True)
    link_url = config.get("link_url")
    settings = machine_settings[display_name]
    settings = apply_free_custom_label_override(settings, display_name, plan_type)

    # OGPプレビュー（HTTPは LRU+TTL で節約）
    link_preview = get_link_preview_cached(link_url) if link_url else None

    # 追加（X用キャッシュバスター）
    ASSET_REV = os.environ.get("ASSET_REV", "20251007")  # 任意。更新したい時に変える
    tw_image = f"{og_image}?v={ASSET_REV}"

    # テンプレート切替
    template_name = "index_paid.html" if plan_type == "paid" else "index_free.html"

    # フォーム入力の取得
    if request.method == "POST":
        selected_mode = request.form.get("mode", settings["mode_options"][0])
        selected_time = request.form.get("time", "朝イチ")
        input_game = request.form.get("game", "0")

        selected_through = request.form.get("through", "不問")
        selected_at_gap = request.form.get("at_gap", "不問")
        selected_prev_game = request.form.get("prev_game", "不問")
        selected_prev_coin = request.form.get("prev_coin", "不問")
        selected_prev_diff = request.form.get("prev_diff", "不問")
        selected_prev_renchan = request.form.get("prev_renchan", "不問")
        selected_prev_type = request.form.get("prev_type", "不問")
        selected_custom_condition = request.form.get("custom_condition", "不問")
    else:
        # 初期表示（GET）のデフォルト値
        selected_mode = settings["mode_options"][0]
        selected_time = "朝イチ"
        input_game = "0"
        selected_through = "不問"
        selected_at_gap = "不問"
        selected_prev_game = "不問"
        selected_prev_coin = "不問"
        selected_prev_diff = "不問"
        selected_prev_renchan = "不問"
        selected_prev_type = "不問"
        selected_custom_condition = "不問"

    # CSV の読み分け（機種ごと）
    if selected_mode == "AT":
        csv_path = f"data/{file_key}_at.csv"
    elif selected_mode == "CZ":
        csv_path = f"data/{file_key}_cz.csv"
    else:
        csv_path = f"data/{file_key}_rb.csv"

    # CSV 読み込み（mtimeキャッシュ）
    try:
        # よく使う列を指定して省メモリ＆高速化（必要に応じて調整）
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
        # 列が存在しない場合もあるので usecols は指定しない（柔軟性重視）
        df = load_csv_cached(csv_path, dtypes=dtypes)
    except Exception as e:
        return render_template(
            template_name,
            error_msg=f"CSV読み込みエラー: {e}",
            result=None,
            labels=settings.get("labels", {})
        )

    # フィルタ用フォーム値
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
        "custom_condition": selected_custom_condition,
    }

    # 条件適用
    filtered_df = filter_dataframe(df, form, settings)

    # 結果計算（十分なサンプル件数がある場合のみ）
    if not filtered_df.empty and len(filtered_df) >= 100:
        count = len(filtered_df)
        avg_reg_games = filtered_df["REGゲーム数"].mean()
        avg_at_games = filtered_df["ATゲーム数"].mean()
        avg_reg_coins = filtered_df["REG枚数"].mean()
        avg_at_coins = filtered_df["AT枚数"].mean()

        # 初当たり想定（打ち出しゲームを控除）
        hatsu_atari = max(avg_reg_games - int(input_game), 0)

        # 差枚・IN/OUT・機械割・期待値
        avg_diff = avg_at_coins + avg_reg_coins - (hatsu_atari * 50 / settings["coin_moti"])
        avg_in = (hatsu_atari + avg_at_games) * 3
        avg_out = avg_diff + avg_in
        payout_rate = (avg_out / avg_in) * 100 if avg_in else 0
        expected_value = avg_diff * 20

        result = {
            "件数": f"{count:,}件",
            "平均REGゲーム数": f"1/{hatsu_atari:,.1f}",
            "平均AT枚数": f"{avg_at_coins:,.1f}枚",
            "機械割": f"{payout_rate:,.1f}%",
            "期待値": f"{expected_value:,.0f}円",
        }
    elif len(filtered_df) < 100:
        result = "サンプル不足"
    else:
        result = None

    # 初期表示（GET）は結果を表示しない
    if request.method == "GET":
        result = None

    # 機種別ロック対象（テンプレートで使用）
    locked_field_map = {
        cfg["display_name"]: machine_settings[cfg["display_name"]].get("locked_fields", [])
        for cfg in machine_configs.values()
    }

    # レンダリング
    return render_template(
        template_name,
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
        og_image=og_image,   # OGP
        tw_image=tw_image,   # X/Twitter
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
# ローカル起動
# ==============================================================================
if __name__ == "__main__":
    # ローカル検証時のみ debug=True にしてOK。公開時は False 推奨。
    app.run(debug=False)
