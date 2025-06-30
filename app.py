from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

machines = ["L マギアレコード 魔法少女まどか☆マギカ外伝", "L ゴッドイーター リザレクション"]

# 各機種ごとの設定値
machine_settings = {
    "L マギアレコード 魔法少女まどか☆マギカ外伝": {
        "exclude_games": 30,
        "coin_moti": 32.6,
        "file_key": "マギアレコード",
        "mode_options": ["CZ", "ボーナス"],
        "through_options": ["不問", "0", "1", "2", "3", "4", "5スルー以上"],
        "at_gap_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],  # ←追加
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "labels": {
            "mode": "CZ／ボナ",
            "at_gap": "ボナ間ゲーム数",
            "prev_game": "前回ボナ当選ゲーム数",
            "prev_coin": "前回ボナ獲得枚数",
            "prev_diff": "前回ボナ終了時差枚数",
            "prev_renchan": "前回ボナ連荘数",
            "prev_type": "前回ボナ種別"
        }
    },
    "L ゴッドイーター リザレクション": {
        "exclude_games": 30,
        "coin_moti": 31.0,
        "file_key": "ゴッドイーター",
        "mode_options": ["AT"],
        "through_options": ["不問"],
        "at_gap_options": ["不問"],  # ←追加
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "labels": {
            "mode": "AT",
            "at_gap": "AT間ゲーム数",
            "prev_game": "前回AT当選ゲーム数",
            "prev_coin": "前回AT獲得枚数",
            "prev_diff": "前回AT終了時差枚数",
            "prev_renchan": "前回AT連荘数",
            "prev_type": "前回AT種別"
        }
    }
}

# 範囲文字列をパースして判定
def parse_range(value, condition):
    if "～" in condition:
        low, high = condition.replace(",", "").replace("枚", "").replace("G", "").replace("連", "").replace("スルー", "").split("～")
        return int(low) <= value <= int(high)
    elif "以下" in condition:
        limit = int(condition.replace(",", "").replace("枚", "").replace("G", "").replace("連", "").replace("スルー", "").replace("以下", ""))
        return value <= limit
    elif "以上" in condition:
        limit = int(condition.replace(",", "").replace("枚", "").replace("G", "").replace("連", "").replace("スルー", "").replace("以上", ""))
        return value >= limit
    return False

# DataFrame フィルタリング処理
def filter_dataframe(df, form, settings):
    exclude_games = settings["exclude_games"] 
    cond = pd.Series([True]*len(df))
    # 朝イチ
    cond &= (df["朝イチ"] == (1 if form["time"] == "朝イチ" else 0))
    # スルー回数
    if form["through"] != "不問":
        cond &= (df["スルー回数"] == int(form["through"]))
    # AT間ゲーム数
    if form["at_gap"] != "不問":
        cond &= df["AT間ゲーム数"].apply(lambda v: parse_range(int(v), form["at_gap"]))
    # 前回当選ゲーム数
    if form["prev_game"] != "不問":
        cond &= df["前回当選ゲーム数"].apply(lambda v: parse_range(int(v), form["prev_game"]))
    # 前回獲得枚数
    if form["prev_coin"] != "不問":
        cond &= df["前回獲得枚数"].apply(lambda v: parse_range(int(v), form["prev_coin"]))
    # 前回差枚数
    if form["prev_diff"] != "不問":
        cond &= df["前回差枚数"].apply(lambda v: parse_range(int(v), form["prev_diff"]))
    # 前回連荘数
    if form["prev_renchan"] != "不問":
        cond &= df["前回連荘数"].apply(lambda v: parse_range(int(v), form["prev_renchan"]))
    # 前回種別
    if form["prev_type"] != "不問":
        cond &= (df["前回種別"] == form["prev_type"])
    # 打ち出しゲーム数 + 除外ゲーム数でフィルタ
    #cond &= (df["REGゲーム数"] >= (int(form["game"]) + exclude_games))
    cond &= (df["当該REGゲーム数"] >= (int(form["game"]) + exclude_games))
    return df[cond]

@app.route("/", methods=["GET", "POST"])
def index():
    # 初期値・POST受け取り
    if request.method == "POST":
        selected_machine = request.form.get("machine", "L マギアレコード 魔法少女まどか☆マギカ外伝")
        selected_mode = request.form.get("mode", "CZ")  # ←追加
        selected_time = request.form.get("time", "朝イチ")
        input_game = request.form.get("game", "0")
        selected_through = request.form.get("through", "不問")
        selected_at_gap = request.form.get("at_gap", "不問")  # ←追加
        selected_prev_game = request.form.get("prev_game", "不問")
        selected_prev_coin = request.form.get("prev_coin", "不問")
        selected_prev_diff = request.form.get("prev_diff", "不問")
        selected_prev_renchan = request.form.get("prev_renchan", "不問")
        selected_prev_type = request.form.get("prev_type", "不問")
    else:
        selected_machine = "L マギアレコード 魔法少女まどか☆マギカ外伝"
        selected_mode = "CZ"  # ←追加
        selected_time = "朝イチ"
        input_game = "0"
        selected_through = "不問"
        selected_at_gap = "不問"  # ←追加
        selected_prev_game = "不問"
        selected_prev_coin = "不問"
        selected_prev_diff = "不問"
        selected_prev_renchan = "不問"
        selected_prev_type = "不問"

    settings = machine_settings[selected_machine]
    file_key = settings["file_key"]  # ← 追加
    exclude_games = settings["exclude_games"]
    coin_moti = settings["coin_moti"]
    #csv_path = f"data/{selected_machine}.csv"
    if selected_mode == "AT":
        csv_path = f"data/{file_key}_at.csv"
    elif selected_mode == "CZ":
        csv_path = f"data/{file_key}_cz.csv"
    else:
        csv_path = f"data/{file_key}_rb.csv"

    # CSV読み込み
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        df = None
        error_msg = f"CSV読み込みエラー: {e}"
        return render_template(
            "index.html",
            machines=machines,
            selected_machine=selected_machine,
            selected_mode=selected_mode,  # ←追加
            selected_time=selected_time,
            input_game=input_game,
            mode_options=settings["mode_options"],  # ← これが必要！！
            through_options=settings["through_options"],
            at_gap_options=settings["at_gap_options"],  # ←追加
            prev_game_options=settings["prev_game_options"],
            prev_coin_options=settings["prev_coin_options"],
            prev_diff_options=settings["prev_diff_options"],
            prev_renchan_options=settings["prev_renchan_options"],
            prev_type_options=settings["prev_type_options"],
            selected_through=selected_through,
            selected_at_gap=selected_at_gap,             # ←追加
            selected_prev_game=selected_prev_game,
            selected_prev_coin=selected_prev_coin,
            selected_prev_diff=selected_prev_diff,
            selected_prev_renchan=selected_prev_renchan,
            selected_prev_type=selected_prev_type,
            labels=settings.get("labels", {}),  # ★ ここを追加
            error_msg=error_msg,
            result=None
        )

    # 条件フィルタリング
    form = {
        "time": selected_time,
        "through": selected_through,
        "at_gap": selected_at_gap,  # ←追加
        "prev_game": selected_prev_game,
        "prev_coin": selected_prev_coin,
        "prev_diff": selected_prev_diff,
        "prev_renchan": selected_prev_renchan,
        "prev_type": selected_prev_type,
        #"game": int(input_game) + exclude_games,
        "game": int(input_game),  # exclude_gamesはここでは加えない
    }

    filtered_df = filter_dataframe(df, form, settings)

    # --- 結果計算 ---
    if not filtered_df.empty and len(filtered_df) >= 10:
        count = len(filtered_df)
        avg_reg_games = filtered_df["REGゲーム数"].mean()
        avg_at_games = filtered_df["ATゲーム数"].mean()
        avg_reg_coins = filtered_df["REG枚数"].mean()
        avg_at_coins = filtered_df["AT枚数"].mean()

        input_games = int(form["game"])
        hatsu_atari = max(avg_reg_games - input_games, 0)  # 初当たりゲーム数

        # 平均差枚数の算出
        avg_diff = avg_at_coins + avg_reg_coins - (hatsu_atari * 50 / coin_moti)

        # 平均IN枚数とOUT枚数
        avg_in = (hatsu_atari + avg_at_games) * 3
        avg_out = avg_diff + avg_in

        # 機械割と期待値
        payout_rate = (avg_out / avg_in) * 100 if avg_in else 0
        expected_value = avg_diff * 20

        result = {
            "件数": f"{count:,}件",
            "平均REGゲーム数": f"1/{hatsu_atari:,.1f}",
            "平均AT枚数": f"{avg_at_coins:,.1f}枚",
            "機械割": f"{payout_rate:,.1f}%",
            "期待値": f"{expected_value:,.0f}円"
        }
    elif len(filtered_df) < 10:
        result = "サンプル不足"
    else:
        result = None

    # GETの場合は結果を表示しない
    if request.method == "GET":
        result = None

    return render_template(
        "index.html",
        machines=machines,
        selected_machine=selected_machine,
        selected_mode=selected_mode,
        selected_time=selected_time,
        input_game=input_game,
        mode_options=settings["mode_options"],  # ← これが必要！！
        through_options=settings["through_options"],
        at_gap_options=settings["at_gap_options"],  # ←追加
        prev_game_options=settings["prev_game_options"],
        prev_coin_options=settings["prev_coin_options"],
        prev_diff_options=settings["prev_diff_options"],
        prev_renchan_options=settings["prev_renchan_options"],
        prev_type_options=settings["prev_type_options"],
        selected_through=selected_through,
        selected_at_gap=selected_at_gap,             # ←追加
        selected_prev_game=selected_prev_game,
        selected_prev_coin=selected_prev_coin,
        selected_prev_diff=selected_prev_diff,
        selected_prev_renchan=selected_prev_renchan,
        selected_prev_type=selected_prev_type,
        labels=settings.get("labels", {}),  # ★ ここを追加
        result=result,
        error_msg=None
    )

if __name__ == "__main__":
    pass  # ローカルで動かす場合は app.run() に変更
    #app.run(debug=True)
