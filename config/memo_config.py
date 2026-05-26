memo_configs = {

    "bigdream": {
        "title": "L ビッグドリーム",
        "updated": "2026/05/25",
        "sections": [
            {
                "title": "ゲーム数天井",
                "text":
                    "<div class='memo-line'><span>設定変更後</span><span>：</span><span>999G（333G , 555G）</span></div>"
                    "<div class='memo-line'><span>下位AT後</span><span>：</span><span>1,499G（333G , 555G , 999G）</span></div>"
                    "<div class='memo-line'><span>上位AT後</span><span>：</span><span>999G（333G , 555G）</span></div>"
                    "<div class='memo-line'><span>恩恵</span><span>：</span><span>AT当選</span></div>"
                    "※20%以上で天井短縮あり",
                "images": []
            },
            {
                "title": "ボール天井",
                "text":
                    "ボールが落下する度にボール天井pt獲得を抽選。<br>"
                    "プレミアムCZ「ドリームジャックポットチャンス」突入 or 次回ATの1個目が金箱。",
                "images": []
            },
            {
                "title": "やめどき",
                "text": "AT後ヤメ",
                "images": []
            },
            {
                "title": "アイキャッチ",
                "text":
                    "<div class='memo-line'><span>通常</span><span>：</span><span>デフォルト（上位AT終了時なら天井555G以下の期待大）</span></div>"
                    "<div class='memo-line'><span>赤</span><span>：</span><span>天井999G以下のチャンス（CZ後なら大チャンス）</span></div>"
                    "<div class='memo-line'><span>キリン柄</span><span>：</span><span>天井333G以下濃厚+ボール天井ptMAX濃厚</span></div>",
                "images": [
                    "3.jpg"
                ]
            },
            {
                "title": "AT終了画面",
                "text":
                  "下位後：設定+999G天井<br>"
                  "上位後：設定+555G天井",
                "images": [
                    "1.jpg"
                ]
            }
        ]
    },
    "residentevilre3": {
        "title": "L バイオハザードRE:3",
        "updated": "2026/05/26",
        "sections": [
            {
                "title": "ゲーム数天井",
                "text":
                    "設定変更後：650G+α<br>"
                    "設定変更後以外：1,000G+α<br>"
                    "恩恵：パンデミックチャンス+AT当選",
                "images": []
            },
            {
                "title": "CZスルー回数天井",
                "text":
                    "CZ6スルー後、7回目のCZが成功濃厚<br>"
                    "恩恵：AT当選",
                "images": []
            },
            {
                "title": "やめどき",
                "text":
                    "CZ、下位AT後：pt状況を確認して辞め<br>"
                    "<span class='orange'>上位AT後：50ptをフォローして辞め</span>",
                "images": []
            },
            {
                "title": "CZ失敗時のボイス示唆",
                "text":
                    "CZ「ネメシスバトル」失敗時にPUSHボタンを押すとボイスが発生。",
                "tables": [
                    {
                        "headers": ["ボイス", "示唆"],
                        "rows": [
                            ["ここまでね", "デフォルト"],
                            ["どこまでも追ってくる", "残り3回以内示唆"],
                            ["諦めるにはまだ早い", "<span class='green'>残り3回以内濃厚</span>"],
                            ["良いサンプルが取れた", "<span class='red'>次回CZ成功濃厚</span>"],
                            ["私(俺)達は負けない", "<span class='red'>復活濃厚</span>"]
                        ]
                    }
                ],
                "images": []
            },
            {
                "title": "NEポイント",
                "text":
                    "液晶右下のNEポイントが規定に到達するとCZ「ネメシスバトル」に当選。<br>"
                    "※期待度は△＜▲＜○＜◎",
                "tables": [
                    {
                        "headers": ["NEポイント", "CZ当選期待度"],
                        "rows": [
                            ["50pt", "△"],
                            ["100pt", "○"],
                            ["150pt", "△"],
                            ["200pt", "▲"],
                            ["250pt", "△"],
                            ["300pt", "◎"],
                            ["350pt", "△"],
                            ["400pt", "○"],
                            ["450pt", "△"],
                            ["500pt", "天井"]
                        ]
                    }
                ],
                "images": []
            }
        ]
    },
}