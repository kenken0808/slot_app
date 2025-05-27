from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# 定数
JUNZOU = 4.1
COIN_MOTI = 31.5
JOUGAI_GAMES = 30

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            user_game = int(request.form['game'])
            time_type = request.form['time']
            filename = 'data/ひな形朝イチ.csv' if time_type == '朝イチ' else 'data/ひな形朝イチ以外.csv'
            df = pd.read_csv(filename)

            count = 0
            total_reg_game = 0
            total_at_game = 0
            total_reg_coin = 0
            total_at_coin = 0

            for _, row in df.iterrows():
                reg_game = row['REGゲーム数']
                if reg_game >= user_game + JOUGAI_GAMES:
                    count += 1
                    total_reg_game += (reg_game - user_game)
                    total_at_game += row['ATゲーム数']
                    total_reg_coin += row['REG枚数']
                    total_at_coin += row['AT枚数']

            if count > 0:
                avg_reg_game = total_reg_game / count
                avg_at_game = total_at_game / count
                avg_reg_coin = total_reg_coin / count
                avg_at_coin = total_at_coin / count

                samai = avg_reg_coin + avg_at_coin - (avg_reg_game * 50 / COIN_MOTI)
                in_coin = (avg_reg_game + avg_at_game) * 3
                out_coin = samai + in_coin
                kikaiwari = out_coin / in_coin
                kitaiti = samai * 20

                result = {
                    'count': count,
                    'avg_reg_game': round(avg_reg_game, 1),
                    'avg_at_coin': round(avg_at_coin, 1),
                    'kikaiwari': round(kikaiwari * 100, 2),
                    'kitaiti': round(kitaiti, 1)
                }
            else:
                result = {'error': '条件を満たすデータがありません。'}

        except Exception as e:
            result = {'error': f'エラーが発生しました: {e}'}

    return render_template('index.html', result=result)

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=10000)
    pass
