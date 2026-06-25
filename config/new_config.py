from __future__ import annotations
from typing import Dict, Any
from werkzeug.security import generate_password_hash

# =========================================================
# 共通リンク
# =========================================================
COMMON_LINKS = [
    {
        "title": "沖ドキ！グラフ生成",
        "og_image": "icon/okidoki_ap1.jpg",
        "link_url": "/okidoki/tools"
    },
    {
        "title": "東京リベンジャーズおもちゃ",
        "og_image": "icon/toreve_ap1.jpg",
        "link_url": "/toreve/tools"
    },
]

# =========================================================
# 機種マスタ（UI・設定・リンクすべて統合）
# =========================================================
machine_configs = {
    "birdiewing": {
        "display_name": "L BIRDIE WING",
        "file_key": "birdiewing",
        "search_word": "ばーでぃーういんぐ",
        "links": [
            {
                "og_image": "icon/birdiewing_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/naddb7a7181b3"
            }
        ],
        "settings": {
            "exclude_games": 70,
            "coin_moti": 31.5,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1250, 50, 1250,0),
            "through": (0, 4, 1, 4),
            "at_gap": (0, 1250, 50, 1250),
            "prev_game": (0, 1250, 50, 1250),
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ST間天井】
                    恩恵はバーディーボーナス（ST濃厚）当選。
                    ※天井周期の次周期から前兆
                    朝イチ　　：7周期
                    朝イチ以外：10周期
                    """
            }
        }
    },
    "sengokuotome5": {
        "display_name": "L 戦国乙女5 業火を穿つ宿焔の双刃",
        "file_key": "sengokuotome5",
        "search_word": "せんごくおとめふぁいぶ",
        "links": [
            {
                "og_image": "icon/sengokuotome5_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/nc155c9bc2dd7"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1100, 50, 1100,0),
            "through": (0, 10, 1, 99),
            "at_gap": (0, 1100, 50, 1100),
            "prev_game": (0, 1100, 50, 1100),
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ　　：650G or 4周期
                    朝イチ以外：999G or 6周期
                    """
            }
        }
    },
    "taktopdestiny": {
        "display_name": "L タクトオーパス",
        "file_key": "taktopdestiny",
        "search_word": "たくとおーぱす",
        "links": [
            {
                "og_image": "icon/taktopdestiny_v4.jpg",
                "link_url": "https://note.com/kenslodata/n/n105f458ebc79"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 35.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050),
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    朝イチ　　：300G
                    朝イチ以外：500G
                    
                    【AT間天井】
                    恩恵はAT当選。
                    不問：999G
                    """
            }
        }
    },
    "bigdream": {
        "display_name": "L ビッグドリーム",
        "file_key": "bigdream",
        "search_word": "びっぐどりーむ",
        "links": [
            {
                "og_image": "icon/bigdream_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/na9b062ac77f5"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.7,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1550, 50, 1550,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1550, 50, 1550),
            "prev_game": (0, 1550, 50, 1550), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ：999G
                    下位後：1499G
                    上位後：999G
                    短縮　：333G or 555G or 999G
                    """
            }
        }
    },

    "residentevilre3": {
        "display_name": "L バイオハザードRE:3",
        "file_key": "residentevilre3",
        "search_word": "ばいおはざーどりべれーしょんすりー",
        "links": [
            {
                "og_image": "icon/residentevilre3_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/n0d5efbc741df"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.8,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 7, 1,7),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    不問　：500pt
                    上位後：50pt
                    
                    【AT間天井】
                    恩恵はAT当選 + パンデミックチャンス獲得。
                    朝イチ　　：650G
                    朝イチ以外：1000G
                    """,
                "through": """
                    【CZスルー天井】
                    恩恵は成功濃厚のCZ当選。
                    不問：6スルー後7回目
                    """
            }
        }
    },
# =========================================================
# アニマルドッチ
# =========================================================
    "unicorn2": {
        "display_name": "L ガンダムユニコーン2",
        "file_key": "unicorn2",
        "search_word": "がんだむゆにこーんつー",
        "links": [
            {
                "og_image": "icon/unicorn2_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/nfece014bf08a"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1450, 50, 1450,0),
            "through": (0, 7, 1,7),
            "at_gap": (0, 1450, 50, 1450),
            "prev_game": (0, 1450, 50, 1450), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    ※実ゲーム数。
                    朝イチ　　：400G
                    朝イチ以外：800G
                    
                    【AT間天井】
                    恩恵はボーナス（AT濃厚）当選。
                    ※液晶ゲーム数。
                    朝イチ　　：1000G
                    朝イチ以外：1400G
                    """,
                "through": """
                    【CZスルー天井】
                    恩恵はボーナス（AT濃厚）当選。
                    不問：6スルー後7回目
                    """
            }
        }
    },

    "milliongod": {
        "display_name": "L ミリオンゴッド",
        "file_key": "milliongod",
        "search_word": "みりおんごっど",
        "links": [
            {
                "og_image": "icon/milliongod_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.8,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1550, 50, 1550,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1550, 50, 1550),
            "prev_game": (0, 1550, 50, 1550), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選 + ループストック獲得。
                    朝イチ　　：1000G
                    朝イチ以外：1480G
                    短縮　　　：510G or 1000G
                    """
            }
        }
    },
# =========================================================
# 虚構推理
# =========================================================
# =========================================================
# アクダマドライブ
# =========================================================
    "shinuchiyoshimune": {
        "display_name": "L 真打吉宗",
        "file_key": "shinuchiyoshimune",
        "search_word": "しんうちよしむね",
        "links": [
            {
                "og_image": "icon/shinuchiyoshimune_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n25193f7ab63d"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1550, 50, 1550,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1550, 50, 1550),
            "prev_game": (0, 1550, 50, 1550), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    不問：1000G or 6周期
                    
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ：1000G
                    下位後：1500G
                    上位後：700G
                    """
            }
        }
    },
    "kabaneriunato": {
        "display_name": "L 甲鉄城のカバネリ海門決戦",
        "file_key": "kabaneriunato",
        "search_word": "こうてつじょうのかばねりうなとけっせん",
        "links": [
            {
                "og_image": "icon/kabaneriunato_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n5fd6c389a0d5"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.4,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1550, 50, 1550,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1550, 50, 1550),
            "prev_game": (0, 1550, 50, 1550), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ST間天井】
                    恩恵はエピソードボーナス（ST濃厚）当選。
                    朝イチ　　：596G or 4周期
                    駆け抜け後：596G or 4周期
                    下位後　　：996G or 6周期
                    上位後　　：596G or 4周期
                    """
            }
        }
    },
    "hanmabaki": {
        "display_name": "L 範馬刃牙",
        "file_key": "hanmabaki",
        "search_word": "はんまばき",
        "links": [
            {
                "og_image": "icon/hanmabaki_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/nd125e7fe7554"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.1,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 750, 50, 750,0),
            "through": (0, 6, 1,6),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　　：200G（※）
                    朝イチ以外：700G
                    ※朝イチほぼ200Gゾーンで当選。
                    　超えた場合は通常C濃厚。
                    """,
                "through": """
                    【ボーナススルー天井】
                    恩恵はAT当選。
                    不問：6スルー後7回目
                    """
            }
        }
    },
    "goblinslayer2": {
        "display_name": "L ゴブリンスレイヤーⅡ",
        "file_key": "goblinslayer2",
        "search_word": "ごぶりんすれいやーつー",
        "links": [
            {
                "og_image": "icon/goblinslayer2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n2cb70daf971e"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.6,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1550, 50, 1550,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1550, 50, 1550),
            "prev_game": (0, 1550, 50, 1550), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選 + 宿命バトルストック1〜5個。
                    朝イチ　　：1000G
                    朝イチ以外：1500G
                    短縮　　　：600G or 1000G
                    """
            }
        }
    },
    "ghostintheshell": {
        "display_name": "L 攻殻機動隊",
        "file_key": "ghostintheshell",
        "search_word": "こうかくきどうたい",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v3.jpg",
                "link_url": "https://note.com/kenslodata/n/nf71290e3a05e"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ「S.A.M」当選。
                    朝イチ　　　　：350G
                    朝イチ以外　　：550G
                    白の境界失敗後：400G（※）
                    ※400G到達時はCZ「タチコマの家出」に突入。
                    
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ　　：699G
                    朝イチ以外：999G
                    """
            }
        }
    },
    "fireforce2": {
        "display_name": "L 炎炎ノ消防隊2",
        "file_key": "fireforce2",
        "search_word": "えんえんのしょうぼうたいつー",
        "links": [
            {
                "og_image": "icon/fireforce2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n6e8cc7770e25"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 950, 50, 950,0),
            "through": (0, 5, 1,5),
            "at_gap": (0, 2100, 50, 2100),
            "prev_game": (0, 2100, 50, 2100), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　　：650G
                    朝イチ以外：850G
                    
                    【ST間天井】
                    恩恵はSPエピソードボーナス（ST濃厚）当選。
                    朝イチ　　：1500G
                    朝イチ以外：2000G
                    """,
                "through": """
                    【ボーナススルー天井】
                    恩恵はSPエピソードボーナス（ST濃厚）当選。
                    不問：5スルー後6回目
                    """
            }
        }
    },
    "tekken6": {
        "display_name": "L 鉄拳6",
        "file_key": "tekken6",
        "search_word": "てっけんしっくす",
        "links": [
            {
                "og_image": "icon/tekken6_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n483bc6255996"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 950, 50, 950,0),
            "through": (0, 3, 1,3),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　　：500pt
                    朝イチ以外：900pt
                    """,
                "through": """
                    【ボーナススルー天井】
                    恩恵は赤7（AT濃厚）当選。
                    朝イチ：2スルー後3回目
                    下位後：3スルー後4回目
                    上位後：2スルー後3回目
                    """
            }
        }
    },
    "hokutotensei2": {
        "display_name": "L 北斗の拳 転生の章2",
        "file_key": "hokutotensei2",
        "search_word": "ほくとのけんてんせいのしょうつー",
        "links": [
            {
                "og_image": "icon/hokutotensei2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/ncb695f0b4fb5"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.5,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1500, 50, 1500,0),
            "through": (0, 3, 1,3),
            "at_gap": (0, 1500, 50, 1500),
            "prev_game": (0, 1500, 50, 1500), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選 + ATレベル3以上。
                    朝イチ　　：1280あべし
                    朝イチ以外：1536あべし
                    """
            }
        }
    },
    "mushokutensei": {
        "display_name": "L 無職転生",
        "file_key": "mushokutensei",
        "search_word": "むしょくてんせい",
        "links": [
            {
                "og_image": "icon/mushokutensei_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/ne3d934a762e9"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1000, 50, 1000,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    ※天井はステージチェンジ回数。
                    朝イチ　　　　：13回
                    朝イチ以外　　：19回
                    駆け抜け後　　：13回
                    魔術ボーナス後：13回
                    
                    【AT間天井】
                    恩恵はエピソードボーナス（AT濃厚）当選。
                    ※天井はステージチェンジ回数。
                    朝イチ　　：17回
                    朝イチ以外：40回
                    """
            }
        }
    },
    "hihoden": {
        "display_name": "L 秘宝伝",
        "file_key": "hihoden",
        "search_word": "ひほうでん",
        "links": [
            {
                "og_image": "icon/hihoden_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n20a891c1e4b1"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 850, 50, 850,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　：499G
                    ビッグ後：799G
                    バケ後　：649G
                    """
            }
        }
    },
    "okidokiduoencore": {
        "display_name": "L 沖ドキ！DUO アンコール",
        "file_key": "okidokiduoencore",
        "search_word": "おきどきでゅおあんこーる",
        "links": [
            {
                "og_image": "icon/okidokiduoencore_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n726b1b9be413"
            }
        ],
        "settings": {
            "exclude_games": 1,
            "coin_moti": 25.3,
            "mode_options": ["ボーナス", "天国"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 800, 50, 800,0),
            "through": (0, 9, 1,9),
            "at_gap": (0, 3000, 50, 9999),
            "prev_game": (0, 3000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選 + のるカナチャンス獲得。
                    不問：800G（※）
                    ※300Gの仮天井が高確率で選択。
                    """,
                "through": """
                    【ボーナススルー天井】
                    恩恵は天国モード以上へ移行。
                    不問：9スルー後10回目
                    """
            }
        }
    },
    "prismnana": {
        "display_name": "L プリズムナナ",
        "file_key": "prismnana",
        "search_word": "ぷりずむなな",
        "links": [
            {
                "og_image": "icon/prismnana_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n10d7c2c98ace"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.2,
            "mode_options": ["ST"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 950, 50, 950,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 950, 50, 950),
            "prev_game": (0, 950, 50, 950), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ST間天井】
                    恩恵はST当選。
                    朝イチ　　：555G
                    朝イチ以外：899G or 7周期
                    駆け抜け後：555G
                    """
            }
        }
    },
    "logh": {
        "display_name": "L 銀河英雄伝説",
        "file_key": "logh",
        "search_word": "ぎんがえいゆうでんせつ",
        "links": [
            {
                "og_image": "icon/logh_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n33ab406dc7e6"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 35.0,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ST間天井】
                    恩恵はオープニングボーナス（ST濃厚）当選。
                    朝イチ　　：800G
                    朝イチ以外：1000G
                    
                    【GSC間天井】
                    恩恵はエピソードボーナス当選。
                    不問：2000G
                    短縮：1000G or 1200G or 1400G or 1600G or 1800G
                    """
            }
        }
    },
    "bakemonogatari": {
        "display_name": "L 化物語",
        "file_key": "bakemonogatari",
        "search_word": "ばけものがたり",
        "links": [
            {
                "og_image": "icon/bakemonogatari_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/nc7c8e2a4ea46"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.1,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選 + 倍倍チャンス獲得。
                    朝イチ　　：600G
                    朝イチ以外：1000G
                    """
            }
        }
    },
    "burningexpress": {
        "display_name": "L バーニングエクスプレス",
        "search_word": "ばーにんぐえくすぷれす",
        "file_key": "burningexpress",
        "links": [
            {
                "og_image": "icon/burningexpress_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n2648051423d9"
            }
        ],
        "settings": {
            "exclude_games": 1,
            "coin_moti": 31.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1000, 50, 1000,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1000, 50, 1000),
            "prev_game": (0, 1000, 50, 1000), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　　：666G
                    朝イチ以外：999G
                    短縮　　　：111G or 222G or 333G or 444G or 555G
                    """
            }
        }
    },
    "neoplanet": {
        "display_name": "L ネオプラネット",
        "file_key": "neoplanet",
        "search_word": "ねおぷらねっと",
        "links": [
            {
                "og_image": "icon/neoplanet_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/nfbb1961157e5"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.3,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 800, 50, 800,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　　：500G
                    朝イチ以外：777G
                    """
            }
        }
    },
    "zettaishogeki4": {
        "display_name": "L 絶対衝激Ⅳ",
        "file_key": "zettaishogeki4",
        "search_word": "ぜったいしょうげきふぉー",
        "links": [
            {
                "og_image": "icon/zettaishogeki4_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n1a880ae74aff"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.6,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1000, 50, 1000,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はプラトニックボーナスブラック当選。
                    朝イチ　　：5周期
                    朝イチ以外：9周期
                    """
            }
        }
    },
    "railgun2": {
        "display_name": "L とある科学の超電磁砲2",
        "file_key": "railgun2",
        "search_word": "とあるかがくのれーるがんつー",
        "links": [
            {
                "og_image": "icon/railgun2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n471a3dc95649"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.8,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    不問：499G

                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ　　：699G
                    朝イチ以外：999G
                    """
            }
        }
    },
    "valvrave2": {
        "display_name": "L 革命機ヴァルヴレイヴ2",
        "file_key": "valvrave2",
        "search_word": "かくめいきヴァルヴレイヴつー",
        "links": [
            {
                "og_image": "icon/valvrave2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/nf540daedf4b3"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.7,
            "mode_options": ["CZ", "ボーナス"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1500, 50, 1500,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1500, 50, 1500),
            "prev_game": (0, 1500, 50, 1500), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    朝イチ　　：999G or 3周期
                    朝イチ以外：999G or 6周期

                    【AT間天井】
                    恩恵は決戦ボーナス or 革命ボーナス or 革命RUSH当選。
                    朝イチ　　：1000G
                    朝イチ以外：1500G
                    """
            }
        }
    },
# =========================================================
# バベル3000
# =========================================================
    "zenigata5": {
        "display_name": "L 主役は銭形5",
        "file_key": "zenigata5",
        "search_word": "しゅやくはぜにがたふぁいぶ",
        "links": [
            {
                "og_image": "icon/zenigata5_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n14c453aae356"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.2,
            "mode_options": ["ST"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1300, 50, 1300,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1300, 50, 1300),
            "prev_game": (0, 1300, 50, 1300), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ST間天井】
                    恩恵はボーナス（ST濃厚）当選 + 50%で不二子デカタイム獲得。
                    朝イチ　　：850G
                    朝イチ以外：1250G
                    """
            }
        }
    },
    "onimusha3": {
        "display_name": "L 新鬼武者3",
        "file_key": "onimusha3",
        "search_word": "しんおにむしゃすりー",
        "links": [
            {
                "og_image": "icon/onimusha3_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n592917017aae"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ：1000G + 4周期
                    下位後：1000G + 6周期
                    上位後：1周期
                    """
            }
        }
    },
# =========================================================
# なめ猫
# =========================================================
    "sakitopbattle": {
        "display_name": "L 咲-Saki-頂上決戦",
        "file_key": "sakitopbattle",
        "search_word": "さきちょうじょうけっせん",
        "links": [
            {
                "og_image": "icon/sakitopbattle_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/nda1d15f56223"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.1,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 6, 1,6),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ当選。
                    不問：8周期
                    
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ　　：600G
                    朝イチ以外：1000G
                    駆け抜け後：800G
                    """,
                "through": """
                    【CZスルー天井】
                    恩恵は成功濃厚のCZ当選。
                    不問：6スルー後7回目
                    """
            }
        }
    },
    "reincarnatedasasword": {
        "display_name": "L 転生したら剣でした",
        "file_key": "reincarnatedasasword",
        "search_word": "てんせいしたらけんでした",
        "links": [
            {
                "og_image": "icon/reincarnatedasasword_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n9f437b3ce766"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.3,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はフランボーナス（通常時）、X転剣ボーナス（AT中）当選。
                    ※ボーナス間天井はAT当選でリセットされない。
                    朝イチ　　：980G
                    朝イチ以外：1280G
                    短縮　　　：200G or 500G or 980G
                    
                    【AT間天井】
                    恩恵は成功濃厚のCZ当選。
                    朝イチ　　：600G
                    朝イチ以外：970G
                    """
            }
        }
    },
    "azurlanetheanimetion": {
        "display_name": "L アズールレーン THE ANIMETION",
        "file_key": "azurlanetheanimetion",
        "search_word": "あずーるれーんじあにめーしょん",
        "links": [
            {
                "og_image": "icon/azurlanetheanimetion_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n38b6be48a9da"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 25.8,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 400, 50, 400,0),
            "through": (0, 9, 1,9),
            "at_gap": (0, 2050, 50, 2050),
            "prev_game": (0, 2050, 50, 2050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はアズールレーンボーナス-海戦-当選。
                    不問：350G
                    
                    【AT間天井】
                    恩恵はアズールレーンRUSH突入濃厚のアズールレーンボーナス-海戦-当選。
                    不問：2000G
                    """,
                "through": """
                    【ボーナススルー天井】
                    恩恵はアズールレーンRUSH当選。
                    朝イチ　　：9スルー後10回目
                    朝イチ以外：6スルー後7回目
                    """
            }
        }
    },
    "darlinginthefranxx": {
        "display_name": "L ダーリン・イン・ザ・フランキス",
        "file_key": "darlinginthefranxx",
        "search_word": "だーりんいんざふらんきす",
        "links": [
            {
                "og_image": "icon/darlinginthefranxx_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n6139b4291e69"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.8,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 750, 50, 750,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 50, 9999),
            "prev_game": (0, 2000, 50, 9999), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【ボーナス間天井】
                    恩恵はボーナス当選。
                    朝イチ　　：390G
                    朝イチ以外：666G
                    """,
                "through": """
                    【ボーナススルー天井】
                    恩恵は連チャンまでボーナスがダーリン・イン・ザ・ボーナス以上当選。
                    ※REGまたはST駆け抜けをスルーとする。
                    不問：4スルー後5回目以降
                    """
            }
        }
    },





# =========================================================
# ハイビリターン3000
# =========================================================
# =========================================================
# わたしの幸せな結婚5000
# =========================================================

# =========================================================
# 絶対衝撃
# =========================================================

# =========================================================
# ULTRAMAN4000
# =========================================================
# =========================================================
# ギルティクラウン7000
# =========================================================
# =========================================================
# デビルメイクライ10000
# =========================================================
    "izabantyo": {
        "display_name": "L いざ！番長",
        "file_key": "izabantyo",
        "search_word": "いざばんちょう",
        "links": [
            {
                "og_image": "icon/izabantyo_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n84de40377ba4"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 1050, 50, 1050,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1050, 50, 1050),
            "prev_game": (0, 1050, 50, 1050), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ　　：600G
                    朝イチ以外：999G
                    """
            }
        }
    },




# =========================================================
# マギアレコード2025年4月7日
# =========================================================
    "tokyoghoul": {
        "display_name": "L 東京喰種",
        "file_key": "tokyoghoul",
        "search_word": "とうきょうぐーるー",
        "links": [
            {
                "og_image": "icon/tokyoghoul_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n3c3178154117"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 600, 50, 600,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1200, 50, 1200),
            "prev_game": (0, 1200, 50, 1200), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【CZ間天井】
                    恩恵はCZ or AT当選。
                    朝イチ　　：200G
                    朝イチ以外：600G
                    
                    【AT間天井】
                    恩恵はAT当選。
                    不問：1200G
                    """
            }
        }
    },
# =========================================================
# ブラックジャック2025年2月3日
# =========================================================
# =========================================================
# かぐや様2024年9月2日
# =========================================================
# =========================================================
# ゴッドイーター2024年7月22日
# =========================================================
# =========================================================
# ブラック2024年7月1日
# =========================================================
# =========================================================
# 防御力に極振り2024年6月3日
# =========================================================
    "monkeyturn5": {
        "display_name": "L モンキーターンV",
        "file_key": "monkeyturn5",
        "search_word": "もんきーたーんふぁいぶ",
        "links": [
            {
                "og_image": "icon/monkeyturn5_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/na2bf9d6045a8"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "下位後", "上位後"],
            "game": (0, 850, 50, 850,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 850, 50, 850),
            "prev_game": (0, 850, 50, 850), 
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ：495G or 4周期
                    下位後：795G or 6周期
                    上位後：495G or 4周期
                    """
            }
        }
    },
    "hokuto": {
        "display_name": "L 北斗の拳",
        "file_key": "hokuto",
        "search_word": "ほくとのけん",
        # =========================
        # UIリンク情報
        # =========================
        "links": [
            {
                "og_image": "icon/hokuto_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n990e9f85b768"
            }
        ],
        # =========================
        # 計算・条件設定
        # =========================
        "settings": {
            "exclude_games": 40,
            "coin_moti": 35.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外"],
            "game": (0, 1350, 50,1350,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1350, 50,1350),
            "prev_game": (0, 1350, 50,1350),
            "prev_coin": (0, 3000, 100,9999),
            "prev_diff": (-4000, 2400, 100,-9999,2400),
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    【AT間天井】
                    恩恵はAT当選。
                    朝イチ　　：800G
                    朝イチ以外：1268G
                    短縮　　　：300G or 777G or 800G
                    """
            }
        }
    }
# =========================================================
# からくり2023年7月3日
# =========================================================
# =========================================================
# 北斗の拳2023年4月3日
# =========================================================
# =========================================================
# GOLD2022年12月19日
# =========================================================


# =========================================================
# 
# =========================================================
}

# =========================================================
# FREEプラン時のcustom_conditionラベル固定値
# =========================================================
FREE_CUSTOM_LABEL: str = "機種別条件"

def apply_free_custom_label_override(
    settings: Dict[str, Any],
    display_name: str,
    plan_type: str
) -> Dict[str, Any]:
    """
    freeプランの場合、custom_conditionラベルを強制的に固定値に差し替える
    """
    if plan_type != "free":
        return settings

    # 元データを破壊しないようにコピー
    new_settings = {**settings}
    labels = {**settings.get("labels", {})}

    labels["custom_condition"] = FREE_CUSTOM_LABEL
    new_settings["labels"] = labels
    return new_settings


# =========================================================
# ツールごとのパスワード（ハッシュ化）
# =========================================================
TOOL_PASSWORDS = {
    "hokuto": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "gobsla": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "zenigata4": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "sao": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "berserk": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "azurlane": {
        "paid": "scrypt:32768:8:1$PFBegCB04fHOgHF0$e710ae5a7fbea8429be66079386589a52d173fc972d45996937d61d45b8c7206db3393ddf501fafe3c08e1035251fd711f687ac81257300c82f6ab85659eeb5d"
    },
    "franxx": {
        "paid": "scrypt:32768:8:1$VFGmc7zGYS1ydnvs$909c0c927d02412e3466dba2403659b633f64873648190c311332f6803a4169abdaa980152808fce0b4295883197398e83f722a7097d463767afa9acc2259645"
    },
    "saki": {
        "paid": "scrypt:32768:8:1$T2kCZh0dXCl8alN2$479722165dcf0228f71bba801906880f231693bddb644ff25b7eaec0956376c150b818851202440702b7642d8666c235461bb6cc9df1453592eab1e35b892d11"
    },
    "onimusya": {
        "paid": "scrypt:32768:8:1$HXVhXY4Co3eDcFe3$3947c9a3df4088cf2c5db5d799d4f557835787c4e655f6088bec17410d6ffceda627de56707ff650d8a98edac57eee5274ad29ab9907546a3872d4d781ec7b29"
    },
    "zenigata5": {
        "paid": "scrypt:32768:8:1$pdyOc5wpwFfSCZKK$644e7ea858b3cb98db61a4e42b90e2cb10a60ab25d644aedd8abe4ed37411ad2411733ce63e4d92d0e0db42e2d257ac26a9d4192ddba55880bc5e54ef0309f0e"
    },
    "babel": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "kotobuki": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "vvv2": {
        "paid": "scrypt:32768:8:1$dDGDstZIrPx83SRo$de8733a9e815c3a220f7965cd3020264bcff6a42d8451a49b4fec1ae9da7b9ae183e3b80b52a4c9afd10185c3e5f868b9c3029cec2706844f3f507668256dfb4"
    },
    "railgun2": {
        "paid": "scrypt:32768:8:1$3XaTBbCRGDWeH1sj$cece3838ab9a441d7f0e7634d34c436b85e910572d2e42c10f77d1d70b4cb55455abb8bfc1a22a88863048d43194021c3f4d3bbb3f3557786389286016adaae0"
    },
    "syogeki4": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "neoplanet": {
        "paid": "scrypt:32768:8:1$U3dMj6TDdyhLgkfa$2fe6b3b269b73bd8be9dd54ef69b7d5090aa2c4d0e4afc1c5edbf819df27039319a07a318316f88a9369d1a8fd70abd6365a0abd4d7c35415aae1c85af124c08"
    },
    "express": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "bakemonogatari": {
        "paid": "scrypt:32768:8:1$99W19KGwTtqWP35c$61970ad6576c0d6a9c198a9309a43ed03be0d636d0fa70c5f907cc75a340796c25f0b95ba4eecfb286d0f84b9f24fec4e28f60184c48f0818bafd33227949a1d"
    },
    "prismnana": {
        "paid": "scrypt:32768:8:1$La8x4KQkovXJ0U8C$33591a2d3d7e91c5bb3d87fc858bb364275934a07d3a7488bf63ea04f16119484111399d0e9cd141a44d9b5fe01d7fdf853853e317d9936c1ed3db1c27bbadc2"
    },
    "logh": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "hihouden": {
        "paid": "scrypt:32768:8:1$I1w0SlHwAOFn9H7u$74a92e77576e592f74ede4a817697695763b4dd05e7a7d38bbfa77a92e6a094a5fbdcd37769fd203557f7d7b0571a72941eb91ba89507d653dd14fbc671a60d1"
    },
    "musyoku": {
        "paid": "scrypt:32768:8:1$Vdj4kCl4oYRJbsmr$51af6c5e1d1fd31222d3032a849126c2af78455ef6a19aa1b56a31af17a51b691cbcf76e88fe49b1d73706c450a4e1bd5ada0f3664596add5f324148aea338ac"
    }
}

# =====================================================================
# 20260623新ツール用パスワード
# =====================================================================
NEW_TOOL_PASSWORD = "123456"

__all__ = [
    "machine_configs",
    "machine_settings",
    "FREE_CUSTOM_LABEL",
    "apply_free_custom_label_override",
    "TOOL_PASSWORDS",
    "NEW_TOOL_PASSWORD"
]
