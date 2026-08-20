画像配置先: granbluefantasy/images/critical/

【武器】
wamuspear.png       ワム槍
oluobe.png          オルオベ・冬ノ霜柱
mareaxe.png         マレ斧
leviathan_spear.png リヴァ槍

【加護・補正】
main.png            メイン召喚石
friend.png          フレンド召喚石
boost.png           ブースト武器
gabriel.png         ガブリエル
uruki.png           ウルキ
kusabi.png          蒼空の楔

画像は横長表示を前提にしています（object-fit: cover）。
今回アップロードされた friend.png はサンプルとして格納済みです。


【Render / Flask】
URL:
https://kenkentools.com/granbluefantasy/critical

app.py に以下の3ルートが必要です:

@app.route("/granbluefantasy/critical")
def granbluefantasy_critical():
    base = os.path.join(app.root_path, "granbluefantasy", "critical")
    return send_from_directory(base, "critical.html")

@app.route("/granbluefantasy/critical/<path:filename>")
def granbluefantasy_critical_files(filename):
    base = os.path.join(app.root_path, "granbluefantasy", "critical")
    return send_from_directory(base, filename)

@app.route("/granbluefantasy/images/critical/<path:filename>")
def granbluefantasy_critical_images(filename):
    base = os.path.join(app.root_path, "granbluefantasy", "images", "critical")
    return send_from_directory(base, filename)

CSS/JS/画像はすべて /granbluefantasy/... の絶対パスに修正済みです。
