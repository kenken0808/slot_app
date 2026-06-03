from __future__ import annotations
from typing import Dict, Any
from werkzeug.security import generate_password_hash

# =========================================================
# 機種マスタ（UI・設定・リンクすべて統合）
# =========================================================
machine_configs = {
    "hokuto": {
        "display_name": "L 北斗の拳",
        "file_key": "hokuto",
        "search_words": ["北斗", "北斗の拳"],

        # =========================
        # UIリンク情報
        # =========================
        "links": [
            {
                "og_image": "icon/icon.jpg",
                "link_url": "https://note.com/kenslodata"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/hokuto"
            }
        ],

        # =========================
        # 計算・条件設定
        # =========================
        "settings": {
            "exclude_games": 40,
            "coin_moti": 35.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1000, 100, 9999,0),

            "through": (0, 5, 1,9999),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 1300, 100,9999),
            "prev_coin": (0, 3000, 300,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 10, 1,9999),

            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],

            "locked_fields": ["through", "at_gap", "prev_type", "custom_condition"],
            "help_texts": {}
        }
    },
    "taktopdestiny": {
        "display_name": "L タクトオーパス",
        "file_key": "taktopdestiny",
        "links": [
            {
                "og_image": "icon/taktopdestiny_v4.jpg",
                "link_url": "https://note.com/kenslodata/n/na9b062ac77f5"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/taktopdestiny"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 35.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 1000, 200,9999),
            "prev_game": (0, 1600, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["through", "at_gap", "prev_game", "prev_coin", "prev_diff", "prev_renchan", "prev_type", "custom_condition"]
        }
    },

    "bigdream": {
        "display_name": "L ビッグドリーム",
        "file_key": "bigdream",
        "links": [
            {
                "og_image": "icon/bigdream_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/na9b062ac77f5"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/bigdream"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.7,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 1000, 200,9999),
            "prev_game": (0, 1600, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },

    "residentevilre3": {
        "display_name": "L バイオハザードRE:3",
        "file_key": "residentevilre3",
        "links": [
            {
                "og_image": "icon/residentevilre3_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/n0d5efbc741df"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/residentevilre3"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.8,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 800, 200,9999),
            "prev_game": (0, 1100, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
# =========================================================
# アニマルドッチ
# =========================================================
    "unicorn2": {
        "display_name": "L ガンダムユニコーン2",
        "file_key": "unicorn2",
        "links": [
            {
                "og_image": "icon/unicorn2_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/nfece014bf08a"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/unicorn2"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 6, 1,99),
            "at_gap": (0, 1000, 200,9999),
            "prev_game": (0, 1500, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },

    "milliongod": {
        "display_name": "L ミリオンゴッド",
        "file_key": "milliongod",
        "links": [
            {
                "og_image": "icon/milliongod_v2.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/milliongod"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.8,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 6, 1,99),
            "at_gap": (0, 1000, 200,9999),
            "prev_game": (0, 1600, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
# =========================================================
# 虚構推理
# =========================================================
# =========================================================
# アクダマドライブ_スルー処理どうするか
# =========================================================
    "akudamadrive": {
        "display_name": "L アクダマドライブ",
        "file_key": "akudamadrive",
        "links": [
            {
                "og_image": "icon/akudamadrive_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/akudamadrive"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["ボーナス"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 6, 1,99),
            "at_gap": (0, 1000, 200,9999),
            "prev_game": (0, 1000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
    "shinuchiyoshimune": {
        "display_name": "L 真打吉宗",
        "file_key": "shinuchiyoshimune",
        "links": [
            {
                "og_image": "icon/shinuchiyoshimune_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/shinuchiyoshimune"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 7, 1,99),
            "at_gap": (0, 1400, 200,9999),
            "prev_game": (0, 1600, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
    "kabaneriunato": {
        "display_name": "L 甲鉄城のカバネリ海門決戦",
        "file_key": "kabaneriunato",
        "search_words": ["こうてつじょうのかばねりうなとけっせん"],
        "links": [
            {
                "og_image": "icon/kabaneriunato_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/kabaneriunato"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.4,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 4, 1,99),
            "at_gap": (50, 1000, 50,9999),
            "prev_game": (0, 1000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"],
            "help_texts": {
                "time": """
                    朝イチ　　：596G + 最大4周期
                    朝イチ以外：996G + 最大6周期
                    駆け抜け後：596G + 最大4周期
                    下位後　　：996G + 最大6周期
                    上位後　　：596G + 最大4周期
                    """
            }
        }
    },
    "hanmabaki": {
        "display_name": "L 範馬刃牙",
        "file_key": "hanmabaki",
        "links": [
            {
                "og_image": "icon/hanmabaki_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/hanmabaki"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.1,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 6, 1,99),
            "at_gap": (0, 1500, 200,9999),
            "prev_game": (0, 2000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "goblinslayer2": {
        "display_name": "L ゴブリンスレイヤーⅡ",
        "file_key": "goblinslayer2",
        "links": [
            {
                "og_image": "icon/goblinslayer2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/goblinslayer2"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 30.6,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 8, 1,99),
            "at_gap": (0, 800, 200,9999),
            "prev_game": (0, 1600, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
    "ghostintheshell": {
        "display_name": "L 攻殻機動隊",
        "file_key": "ghostintheshell",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/ghostintheshell"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 8, 1,99),
            "at_gap": (0, 800, 200,9999),
            "prev_game": (0, 1100, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "fireforce2": {
        "display_name": "L 炎炎ノ消防隊2",
        "file_key": "fireforce2",
        "links": [
            {
                "og_image": "icon/fireforce2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/fireforce2"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 1500, 200,9999),
            "prev_game": (0, 2200, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "tekken6": {
        "display_name": "L 鉄拳6",
        "file_key": "tekken6",
        "links": [
            {
                "og_image": "icon/fireforce2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/tekken6"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 3, 1,99),
            "at_gap": (0, 1500, 200,9999),
            "prev_game": (0, 2000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
    "hokutotensei2": {
        "display_name": "L 北斗の拳 転生の章2",
        "file_key": "hokutotensei2",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/hokutotensei2"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.5,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 8, 1,99),
            "at_gap": (0, 800, 200,9999),
            "prev_game": (0, 1500, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "mushokutensei": {
        "display_name": "L 無職転生",
        "file_key": "mushokutensei",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/mushokutensei"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 33.0,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 1500, 200,9999),
            "prev_game": (0, 2500, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "hihoden": {
        "display_name": "L 秘宝伝",
        "file_key": "hihoden",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/hihoden"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 3000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "okidokiduoencore": {
        "display_name": "L 沖ドキ！DUO アンコール",
        "file_key": "okidokiduoencore",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/okidokiduoencore"
            }
        ],
        "settings": {
            "exclude_games": 1,
            "coin_moti": 25.3,
            "mode_options": ["ボーナス", "天国"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1000, 50, 9999,32),
            "through": (0, 9, 1,99),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 3000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "prismnana": {
        "display_name": "L プリズムナナ",
        "file_key": "prismnana",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/prismnana"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.2,
            "mode_options": ["ST"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 9, 1,99),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 1000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
    "logh": {
        "display_name": "L 銀河英雄伝説",
        "file_key": "logh",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/logh"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 35.0,
            "mode_options": ["ボーナス", "ST"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 9, 1,99),
            "at_gap": (0, 800, 200,9999),
            "prev_game": (0, 1100, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "bakemonogatari": {
        "display_name": "L 化物語",
        "file_key": "bakemonogatari",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/bakemonogatari"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.1,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 9, 1,99),
            "at_gap": (0, 800, 200,9999),
            "prev_game": (0, 1100, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },
    "burningexpress": {
        "display_name": "L バーニングエクスプレス",
        "file_key": "burningexpress",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/burningexpress"
            }
        ],
        "settings": {
            "exclude_games": 1,
            "coin_moti": 31.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 9, 1,99),
            "at_gap": (0, 1000, 200,9999),
            "prev_game": (0, 1000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "neoplanet": {
        "display_name": "L ネオプラネット",
        "file_key": "neoplanet",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/neoplanet"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.3,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 2000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "zettaishogeki4": {
        "display_name": "L 絶対衝激Ⅳ",
        "file_key": "zettaishogeki4",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/zettaishogeki4"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.6,
            "mode_options": ["ボーナス", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 2000, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
    "railgun2": {
        "display_name": "L とある科学の超電磁砲2",
        "file_key": "railgun2",
        "links": [
            {
                "og_image": "icon/ghostintheshell_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/railgun2"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.8,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 10, 1,99),
            "at_gap": (0, 2000, 200,9999),
            "prev_game": (0, 1100, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["prev_type", "custom_condition"]
        }
    },
# =========================================================
# ヴァルヴレイヴ25000
# =========================================================

# =========================================================
# 鬼武者15000
# =========================================================
# =========================================================
# 主役は銭形10000
# =========================================================
# =========================================================
# バベル3000
# =========================================================

# =========================================================
# フランキス10000
# =========================================================
# =========================================================
# アズールレーン6000
# =========================================================
# =========================================================
# 転生したら剣5000
# =========================================================
# =========================================================
# 咲5000
# =========================================================
# =========================================================
# なめ猫
# =========================================================

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
        "links": [
            {
                "og_image": "icon/fireforce2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/izabantyo"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1500, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 1500, 200,9999),
            "prev_game": (0, 1100, 200,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
        }
    },




# =========================================================
# マギアレコード2025年4月7日
# =========================================================
    "tokyoghoul": {
        "display_name": "L 東京喰種",
        "file_key": "tokyoghoul",
        "links": [
            {
                "og_image": "icon/fireforce2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/tokyoghoul"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 31.0,
            "mode_options": ["CZ", "AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 1200, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 1200, 100,9999),
            "prev_game": (0, 1200, 100,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
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
        "links": [
            {
                "og_image": "icon/fireforce2_v1.jpg",
                "link_url": "https://note.com/kenslodata/n/n4c8095f6f816"
            },
            {
                "og_image": "icon/ogp_v4.jpg",
                "link_url": "/memo/monkeyturn5"
            }
        ],
        "settings": {
            "exclude_games": 40,
            "coin_moti": 32.0,
            "mode_options": ["AT"],
            "time_options": ["朝イチ", "朝イチ以外", "駆け抜け後", "下位後", "上位後"],
            "game": (0, 800, 50, 9999,0),
            "through": (0, 5, 1,99),
            "at_gap": (0, 1200, 100,9999),
            "prev_game": (0, 800, 100,9999), 
            "prev_coin": (0, 3000, 500,9999),
            "prev_diff": (-4000, 2000, 200,-9999,9999),
            "prev_renchan": (1, 15, 1,99),
            "prev_type_options": ["不問", "下位", "上位"],
            "custom_condition_options": ["不問"],
            "locked_fields": ["custom_condition"]
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

__all__ = [
    "machine_configs",
    "machine_settings",
    "FREE_CUSTOM_LABEL",
    "apply_free_custom_label_override",
    "TOOL_PASSWORDS"
]
