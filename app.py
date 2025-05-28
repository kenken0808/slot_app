from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

COIN_RATE = 4.1
COIN_HOLD = 35.0
EXCLUDE_GAME = 30

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        machine = request.form.get("machine")
        time = request.form.get("time")
        through = request.form.get("through")
        try:
            game = int(request.form.get("game"))
        except (TypeError, ValueError):
            result = {"error": "打ち出しゲーム数が不正です"}
            return render_template("index.html", result=result)

        filename = f"data/{machine}_{time}_{through}.csv"

        if not os.path.isfile(filename):
            result = {"error": f"ファイルが見つかりません: {filename}"}
            return render_template("index.html", result=result)

        try:
            df = pd.read_csv(filename)
        except Exception as e:
            result = {"error": f"CSV読み込みエラー: {e}"}
            return render_template("index.html", result=result)

        # 必須列チェック
        required_cols = ["番号", "REGゲーム数", "REG枚数", "ATゲーム数", "AT枚数"]
        if not all(col in df.columns for col in required_cols):
            result = {"error": "CSVファイルに必要な列がありません。"}
            return render_template("index.html", result=result)

        # 条件に合う行を抽出
        filtered = df[df["REGゲーム数"] >= game + EXCLUDE_GAME]
        count = len(filtered)

        if count == 0:
            result = {"error": "条件に合うデータがありません。"}
            return render_template("index.html", result=result)

        # 各種平均
        reg_game_avg = filtered["REGゲーム数"].mean() - EXCLUDE_GAME
        at_coin_avg = filtered["AT枚数"].mean()

        # 機械割計算
        total_in = (reg_game_avg / COIN_HOLD) * COIN_RATE
        kikaiwari = ((at_coin_avg + filtered["REG枚数"].mean()) / total_in) * 100
        kitaiti = ((kikaiwari / 100) - 1) * (game / COIN_HOLD) * COIN_RATE

        result = {
            "count": count,
            "avg_reg_game": round(reg_game_avg, 1),
            "avg_at_coin": round(at_coin_avg, 1),
            "kikaiwari": round(kikaiwari, 1),
            "kitaiti": round(kitaiti),
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    pass  # ローカルで動かす場合は app.run() に変更
    #app.run(debug=True)
