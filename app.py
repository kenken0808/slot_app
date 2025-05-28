import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

MACHINE_SETTINGS = {
    "マイジャグラーV": {"through_max": 4, "game_max": 400},
    "ファンキージャグラー2": {"through_max": 2, "game_max": 600}
}

DATA_DIR = "data"  # CSVフォルダのパス

EXCLUDE_GAMES = 30
COIN_MOTI = 35  # コイン持ち
COIN_RATE = 3   # コインレート（例）

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    selected_machine = "マイジャグラーV"
    selected_time = "朝イチ"
    selected_through = 0
    input_game = 0

    if request.method == "POST":
        selected_machine = request.form.get("machine", selected_machine)
        selected_time = request.form.get("time", selected_time)  # 朝イチ or 朝イチ以外
        try:
            selected_through = int(request.form.get("through", 0))
        except ValueError:
            selected_through = 0
        try:
            input_game = int(request.form.get("game", 0))
        except ValueError:
            input_game = 0

        filename = f"{selected_machine}_{selected_time}_{selected_through}.csv"
        filepath = os.path.join(DATA_DIR, filename)

        if not os.path.exists(filepath):
            result = {"error": f"ファイルが見つかりません: {filename}"}
        else:
            try:
                df = pd.read_csv(filepath)

                count = 0
                total_reg_game = 0
                total_at_game = 0
                total_reg_coin = 0
                total_at_coin = 0

                for _, row in df.iterrows():
                    reg_game = row["REGゲーム数"]
                    if reg_game >= input_game + EXCLUDE_GAMES:
                        count += 1
                        total_reg_game += (reg_game - input_game)
                        total_at_game += row["ATゲーム数"]
                        total_reg_coin += row["REG枚数"]
                        total_at_coin += row["AT枚数"]

                if count > 0:
                    avg_reg_game = total_reg_game / count
                    avg_at_game = total_at_game / count
                    avg_reg_coin = total_reg_coin / count
                    avg_at_coin = total_at_coin / count

                    samai = avg_reg_coin + avg_at_coin - (avg_reg_game * 50 / COIN_MOTI)
                    in_coin = (avg_reg_game + avg_at_game) * COIN_RATE
                    out_coin = samai + in_coin
                    kikaiwari = out_coin / in_coin * 100  # %
                    kitaiti = samai * 20

                    result = {
                        "count": count,
                        "avg_reg_game": round(avg_reg_game, 1),
                        "avg_at_coin": round(avg_at_coin, 1),
                        "kikaiwari": round(kikaiwari, 2),
                        "kitaiti": round(kitaiti, 1),
                    }
                else:
                    result = {"error": "条件を満たすデータがありません。"}
            except Exception as e:
                result = {"error": f"処理中にエラーが発生しました: {e}"}

    return render_template(
        "index.html",
        machines=list(MACHINE_SETTINGS.keys()),
        settings=MACHINE_SETTINGS,
        selected_machine=selected_machine,
        selected_time=selected_time,
        selected_through=selected_through,
        input_game=input_game,
        result=result,
    )


if __name__ == "__main__":
    pass  # ローカルで動かす場合は app.run() に変更
    #app.run(debug=True)
