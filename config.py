from __future__ import annotations
from typing import Dict, Any
from werkzeug.security import generate_password_hash

# =========================================================
# 機種ごとのURLキー・表示名・CSV読み込み用キー
# =========================================================
machine_configs = {
    "abc_magireco": {
        "display_name": "L マギアレコード 魔法少女まどか☆マギカ外伝",
        "file_key": "magireco",
        "og_image": "ogp.jpg",
        "link_url": "https://note.com/kenslodata/n/nf73890fb871e"
    },
    "abc_godeater": {
        "display_name": "L ゴッドイーター リザレクション",
        "file_key": "godeater",
        "og_image": "ogp.jpg",
        "link_url": "https://note.com/kenslodata/n/ncbba8cff88be"
    },
    "hokuto": {
        "display_name": "L 北斗の拳",
        "file_key": "hokuto",
        "og_image": "ogp.jpg",
        "link_url": "https://note.com/kenslodata"
    },
    "gobsla": {
        "display_name": "L ゴブリンスレイヤー",
        "file_key": "gobsla",
        "og_image": "gobsla.jpg",
        "link_url": "https://note.com/kenslodata/n/n32a75e8fe72c"
    },
    "zenigata4": {
        "display_name": "L 主役は銭形4",
        "file_key": "zenigata4",
        "og_image": "zenigata4.jpg",
        "link_url": "https://note.com/kenslodata/n/ndc323a0f3044"
    },
    "sao": {
        "display_name": "L ソードアート・オンライン",
        "file_key": "sao",
        "og_image": "sao.jpg",
        "link_url": "https://note.com/kenslodata/n/n34242a06a7f4"
    },
    "berserk": {
        "display_name": "L ベルセルク無双",
        "file_key": "berserk",
        "og_image": "berserk.jpg",
        "link_url": "https://note.com/kenslodata/n/nc10c9f9784f9"
    },
    "azurlane": {
        "display_name": "L アズールレーン THE ANIMETION",
        "file_key": "azurlane",
        "og_image": "ogp.jpg",
        "link_url": "https://note.com/kenslodata/n/n38b6be48a9da"
    },
    "franxx": {
        "display_name": "L ダーリン・イン・ザ・フランキス",
        "file_key": "franxx",
        "og_image": "ogp.jpg",
        "link_url": "https://note.com/kenslodata/n/n6139b4291e69"
    },
    "saki": {
        "display_name": "L 咲-Saki-頂上決戦",
        "file_key": "saki",
        "og_image": "ogp.jpg",
        "link_url": "https://note.com/kenslodata/n/nda1d15f56223"
    },
    "onimusya": {
        "display_name": "L 新鬼武者3",
        "file_key": "onimusya",
        "og_image": "onimusya.jpg",
        "link_url": "https://note.com/kenslodata/n/n592917017aae"
    },
    "zenigata5": {
        "display_name": "L 主役は銭形5",
        "file_key": "zenigata5",
        "og_image": "zenigata5.jpg",
        "link_url": "https://note.com/kenslodata/n/n14c453aae356"
    },
    "babel": {
        "display_name": "L バベル",
        "file_key": "babel",
        "og_image": "babel.jpg",
        "link_url": "https://note.com/kenslodata/n/n9edc151b54fc"
    },
    "kotobuki": {
        "display_name": "L 荒野のコトブキ飛行隊",
        "file_key": "kotobuki",
        "og_image": "kotobuki.jpg",
        "link_url": "https://note.com/kenslodata/n/n9475b350635e"
    },
    "vvv2": {
        "display_name": "L 革命機ヴァルヴレイヴ2",
        "file_key": "vvv2",
        "og_image": "vvv2.jpg",
        "link_url": "https://note.com/kenslodata/n/nf540daedf4b3"
    },
    "railgun2": {
        "display_name": "L とある科学の超電磁砲2",
        "file_key": "railgun2",
        "og_image": "railgun2.jpg",
        "link_url": "https://note.com/kenslodata/n/n471a3dc95649"
    },
    "syogeki4": {
        "display_name": "L 絶対衝激Ⅳ",
        "file_key": "syogeki4",
        "og_image": "syogeki4.jpg",
        "link_url": "https://note.com/kenslodata/n/n1a880ae74aff"
    },
    "neoplanet": {
        "display_name": "L ネオプラネット",
        "file_key": "neoplanet",
        "og_image": "neoplanet.jpg",
        "link_url": "https://note.com/kenslodata/n/nfbb1961157e5"
    }
}

# =========================================================
# 機種ごとの条件設定・ラベル（display_nameをキーに）
# =========================================================
machine_settings = {
    "L マギアレコード 魔法少女まどか☆マギカ外伝": {
        "exclude_games": 30,   # 除外ゲーム数
        "coin_moti": 32.6,     # コイン持ち
        "mode_options": ["CZ", "ボーナス"],

        # 各プルダウンの選択肢
        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],

        # ラベル設定
        "labels": {
            "mode": "CZ／ボナ",
            "at_gap": "ボナ間ゲーム数",
            "prev_game": "前回ボナ当選ゲーム数",
            "prev_coin": "前回ボナ獲得枚数",
            "prev_diff": "前回ボナ終了時差枚数",
            "prev_renchan": "前回ボナ連荘数",
            "prev_type": "前回ボナ種別",
            "custom_condition": "マギ特殊"
        },

        "locked_fields": []  # ロックしない項目
    },

    "L ゴッドイーター リザレクション": {
        "exclude_games": 30,
        "coin_moti": 31.0,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT間ゲーム数",
            "prev_game": "前回AT当選ゲーム数",
            "prev_coin": "前回AT獲得枚数",
            "prev_diff": "前回AT終了時差枚数",
            "prev_renchan": "前回AT連荘数",
            "prev_type": "前回AT種別",
            "custom_condition": "イーター特殊"
        },

        # ロックする項目
        "locked_fields": ["mode", "through", "at_gap", "custom_condition"]

    },

    "L 北斗の拳": {
        "exclude_games": 40,
        "coin_moti": 35.0,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～400G", "401～800G", "801～1,000G", "1,001～1,300G", "1,301G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT終了時AT間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "prev_type", "custom_condition"]

    },

    "L ゴブリンスレイヤー": {
        "exclude_games": 40,
        "coin_moti": 31.6,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001～1,500G", "1,501G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT終了時AT間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "custom_condition"]

    },

    "L 主役は銭形4": {
        "exclude_games": 40,
        "coin_moti": 32.0,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～300G", "301～600G", "601～900G", "901G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT終了時AT間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "custom_condition"]

    },

    "L ソードアート・オンライン": {
        "exclude_games": 40,
        "coin_moti": 35.0,
        "mode_options": ["CZ", "ボーナス"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～300G", "301～600G", "601G以上"],
        "prev_diff_options": ["不問"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "CZ／ボナ",
            "at_gap": "CZ終了時ボナ間G数",
            "prev_diff": "ボナ(AT)終了時差枚数",
            "prev_game": "ボナ(AT)当選G数",
            "prev_coin": "ボナ(AT)獲得枚数",
            "prev_renchan": "ボナ(AT)連荘数",
            "prev_type": "ボナ(AT)種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_diff", "prev_type", "custom_condition"]

    },

    "L ベルセルク無双": {
        "exclude_games": 40,
        "coin_moti": 35.5,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～250G", "251～500G", "501～750G", "751～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT終了時AT間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "prev_type", "custom_condition"]

    },

    "L アズールレーン THE ANIMETION": {
        "exclude_games": 40,
        "coin_moti": 25.8,
        "mode_options": ["ボーナス", "AT"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～250G", "251～500G", "501～750G", "751～1,000G", "1,001～1,250G", "1,251G以上"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ／AT",
            "at_gap": "ボナ(AT)終了時ボナ間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "ボナ(AT)終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_type", "custom_condition"]

    },

    "L ダーリン・イン・ザ・フランキス": {
        "exclude_games": 40,   # 除外ゲーム数
        "coin_moti": 30.8,     # コイン持ち
        "mode_options": ["ボーナス", "AT"],

        # 各プルダウンの選択肢
        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～250G", "251～500G", "501～750G", "751～1,000G", "1,001G以上"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        # ラベル設定
        "labels": {
            "mode": "ボナ／AT",
            "at_gap": "ボナ(AT)終了時ボナ間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "ボナ(AT)終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_type", "custom_condition"]  # ロックしない項目

    },

    "L 咲-Saki-頂上決戦": {
        "exclude_games": 40,
        "coin_moti": 32.1,
        "mode_options": ["CZ", "AT"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～200G", "201～400G", "401～600G", "601G以上"],
        "prev_game_options": ["不問", "1～300G", "301～600G", "601～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "CZ／AT",
            "at_gap": "CZ(AT)終了時ボナ間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "CZ(AT)終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_type", "custom_condition"]

    },

    "L 新鬼武者3": {
        "exclude_games": 80,
        "coin_moti": 33.0,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～250G", "251～500G", "501～750G", "751～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT終了時AT間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "custom_condition"]

    },

    "L 主役は銭形5": {
        "exclude_games": 40,
        "coin_moti": 32.2,
        "mode_options": ["ボーナス"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～400G", "401～800G", "801～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ",
            "at_gap": "ボナ終了時ボナ間G数",
            "prev_game": "ボナ当選G数",
            "prev_coin": "ボナ獲得枚数",
            "prev_diff": "ボナ終了時差枚数",
            "prev_renchan": "ボナ連荘数",
            "prev_type": "ボナ種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "prev_type", "custom_condition"]

    },

    "L バベル": {
        "exclude_games": 40,
        "coin_moti": 31.9,
        "mode_options": ["ボーナス"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問"],
        "prev_diff_options": ["不問"],
        "prev_game_options": ["不問", "1～1,000G", "1,001～2,000G", "2,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ",
            "at_gap": "AT終了時AT間G数",
            "prev_diff": "AT終了時差枚数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "at_gap", "prev_diff", "prev_type", "custom_condition"]

    },

    "L 荒野のコトブキ飛行隊": {
        "exclude_games": 40,
        "coin_moti": 35.0,
        "mode_options": ["CZ", "AT"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー", "6スルー"],
        "at_gap_options": ["不問", "1～400G", "401～800G", "801～1,200G", "1,201G以上"],
        "prev_diff_options": ["不問"],
        "prev_game_options": ["不問", "1～1,000G", "1,001～2,000G", "2,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ",
            "at_gap": "AT終了時AT間G数",
            "prev_diff": "AT終了時差枚数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_diff", "custom_condition"]

    },

    "L 革命機ヴァルヴレイヴ2": {
        "exclude_games": 50,
        "coin_moti": 32.7,
        "mode_options": ["CZ", "ボーナス"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～300G", "301～600G", "601～900G", "901G以上"],
        "prev_diff_options": ["不問"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001～1,300G", "1,301G以上"],
        "prev_coin_options": ["不問", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "CZ／ボナ",
            "at_gap": "CZ終了時ボナ間G数",
            "prev_diff": "ボナ(AT)終了時差枚数",
            "prev_game": "ボナ(AT)当選G数",
            "prev_coin": "ボナ(AT)獲得枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_diff", "prev_type", "custom_condition"]

    },

    "L とある科学の超電磁砲2": {
        "exclude_games": 40,
        "coin_moti": 31.8,
        "mode_options": ["AT"],

        "through_options": ["不問"],
        "at_gap_options": ["不問"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_game_options": ["不問", "1～200G", "201～400G", "401～600G", "601～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "at_gap": "AT終了時AT間G数",
            "prev_diff": "AT終了時差枚数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "custom_condition"]

    },

    "L 絶対衝激Ⅳ": {
        "exclude_games": 40,
        "coin_moti": 31.6,
        "mode_options": ["ボーナス"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問", "1～400G", "401～800G", "801G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5～9連", "10連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ",
            "at_gap": "AT終了時ボナ間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "at_gap", "prev_game", "prev_type", "custom_condition"]

    },

    "L ネオプラネット": {
        "exclude_games": 20,
        "coin_moti": 31.3,
        "mode_options": ["ボーナス"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問"],
        "prev_game_options": ["不問"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-3,001枚以下", "-3,000～-2,001枚", "-2,000～-1,001枚", "-1,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501枚以上"],
        "prev_renchan_options": ["不問"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ",
            "at_gap": "AT終了時ボナ間G数",
            "prev_game": "AT当選G数",
            "prev_coin": "AT獲得枚数",
            "prev_diff": "AT終了時差枚数",
            "prev_renchan": "AT連荘数",
            "prev_type": "AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "at_gap", "prev_game", "prev_renchan", "prev_type", "custom_condition"]
    }
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
    "magireco": {
        "paid": "scrypt:32768:8:1$3egFQQ5ggGwUS7gl$a1ca30c9e77e2393bc716a405205e947b823087fbdcda7162bc80e56b31b6b9e1ae18b1329576c2863c365849752c086924a890e75751887cd42260e96c9ba9d"
    },
    "godeater": {
        "paid": "scrypt:32768:8:1$D4Pjt3aUzUqWz1L3$59d03a3616fcf2e16587479d3b1409f22c35b352b01c990a4365252f5d19fe1972e982371e04c1c2a8097dc7f8227ff42806326569d76c7dda9a653a6c8f520d"
    },
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
    }
}

__all__ = [
    "machine_configs",
    "machine_settings",
    "FREE_CUSTOM_LABEL",
    "apply_free_custom_label_override",
    "TOOL_PASSWORDS"
]
