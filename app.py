from flask import Flask, render_template, request
import pandas as pd
from config import machine_configs, machine_settings

app = Flask(__name__)

def parse_range(value, condition):
    condition = condition.replace(",", "").replace("枚", "").replace("G", "").replace("連", "").replace("スルー", "")
    if "～" in condition:
        low, high = condition.split("～")
        return int(low) <= value <= int(high)
    elif "以下" in condition:
        limit = int(condition.replace("以下", ""))
        return value <= limit
    elif "以上" in condition:
        limit = int(condition.replace("以上", ""))
        return value >= limit
    else:
        # 単一値（例: "3スルー"）に対応
        try:
            return value == int(condition)
        except ValueError:
            return False

def filter_dataframe(df, form, settings):
    exclude_games = settings["exclude_games"]
    cond = pd.Series([True]*len(df))
    cond &= (df["朝イチ"] == (1 if form["time"] == "朝イチ" else 0))
    if form["through"] != "不問":
        cond &= df["スルー回数"].apply(lambda v: parse_range(int(v), form["through"]))
    if form["at_gap"] != "不問":
        cond &= df["AT間ゲーム数"].apply(lambda v: parse_range(int(v), form["at_gap"]))
    if form["prev_game"] != "不問":
        cond &= df["前回当選ゲーム数"].apply(lambda v: parse_range(int(v), form["prev_game"]))
    if form["prev_coin"] != "不問":
        cond &= df["前回獲得枚数"].apply(lambda v: parse_range(int(v), form["prev_coin"]))
    if form["prev_diff"] != "不問":
        cond &= df["前回差枚数"].apply(lambda v: parse_range(int(v), form["prev_diff"]))
    if form["prev_renchan"] != "不問":
        cond &= df["前回連荘数"].apply(lambda v: parse_range(int(v), form["prev_renchan"]))
    if form["prev_type"] != "不問":
        cond &= (df["前回種別"] == form["prev_type"])
    if form.get("custom_condition") != "不問":
        cond &= df["機種別条件"].apply(lambda v: parse_range(int(v), form["custom_condition"]))

    cond &= (df["当該REGゲーム数"] >= (int(form["game"]) + exclude_games))
    return df[cond]

@app.route("/<machine_key>/<plan_type>", methods=["GET", "POST"])
def machine_page(machine_key, plan_type):
    if machine_key not in machine_configs:
        return "無効なURLです", 404
    if plan_type not in ["paid", "free"]:
        return "プラン種別が無効です", 404

    config = machine_configs[machine_key]
    display_name = config["display_name"]
    file_key = config["file_key"]
    settings = machine_settings[display_name]

    template_name = "index_paid.html" if plan_type == "paid" else "index_free.html"

    if request.method == "POST":
        selected_mode = request.form.get("mode", settings["mode_options"][0])
        selected_time = request.form.get("time", "朝イチ")
        input_game = request.form.get("game", "0")
        selected_through = request.form.get("through", "不問")  # ここでスルー回数を受け取る
        print(f"selected_through (POST): {selected_through}")  # 受け取った値を確認
        selected_at_gap = request.form.get("at_gap", "不問")
        selected_prev_game = request.form.get("prev_game", "不問")
        selected_prev_coin = request.form.get("prev_coin", "不問")
        selected_prev_diff = request.form.get("prev_diff", "不問")
        selected_prev_renchan = request.form.get("prev_renchan", "不問")
        selected_prev_type = request.form.get("prev_type", "不問")
        selected_custom_condition = request.form.get("custom_condition", "不問")

        # デバッグ用に確認
        print(f"selected_through: {selected_through}")

    else:
        selected_mode = settings["mode_options"][0]
        selected_time = "朝イチ"
        input_game = "0"
        selected_through = "不問"  # 初期値として不問
        selected_at_gap = "不問"
        selected_prev_game = "不問"
        selected_prev_coin = "不問"
        selected_prev_diff = "不問"
        selected_prev_renchan = "不問"
        selected_prev_type = "不問"
        selected_custom_condition = "不問"

    if selected_mode == "AT":
        csv_path = f"data/{file_key}_at.csv"
    elif selected_mode == "CZ":
        csv_path = f"data/{file_key}_cz.csv"
    else:
        csv_path = f"data/{file_key}_rb.csv"

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        return render_template(
            template_name,
            error_msg=f"CSV読み込みエラー: {e}",
            result=None,
            labels=settings.get("labels", {})
        )

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
        "custom_condition": selected_custom_condition  # ← 追加
    }

    filtered_df = filter_dataframe(df, form, settings)

    if not filtered_df.empty and len(filtered_df) >= 10:
        count = len(filtered_df)
        avg_reg_games = filtered_df["REGゲーム数"].mean()
        avg_at_games = filtered_df["ATゲーム数"].mean()
        avg_reg_coins = filtered_df["REG枚数"].mean()
        avg_at_coins = filtered_df["AT枚数"].mean()
        hatsu_atari = max(avg_reg_games - int(input_game), 0)
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
            "期待値": f"{expected_value:,.0f}円"
        }
    elif len(filtered_df) < 10:
        result = "サンプル不足"
    else:
        result = None

    if request.method == "GET":
        result = None

    locked_field_map = {
        key: machine_settings[machine_configs[key]["display_name"]].get("locked_fields", [])
        for key in machine_configs
    }

    return render_template(
        template_name,
        url_path=f"{machine_key}/{plan_type}",
        machine_name=display_name,
        mode_options_map={machine_key: settings["mode_options"]},  # ✅ machine_key を使用
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
        selected_through=selected_through,  # 正しい値を渡す
        selected_at_gap=selected_at_gap,
        selected_prev_game=selected_prev_game,
        selected_prev_coin=selected_prev_coin,
        selected_prev_diff=selected_prev_diff,
        selected_prev_renchan=selected_prev_renchan,
        selected_prev_type=selected_prev_type,
        labels=settings.get("labels", {}),
        result=result,
        error_msg=None,
        selected_custom_condition=selected_custom_condition,
        custom_condition_options=settings.get("custom_condition_options", ["不問"]),
        locked_field_map=locked_field_map
    )



if __name__ == "__main__":
    #pass  # ローカルで動かす場合は app.run() に変更
    app.run(debug=True)


