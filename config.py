from __future__ import annotations
from typing import Dict, Any
from werkzeug.security import generate_password_hash

# =========================================================
# 機種ごとのURLキー・表示名・CSV読み込み用キー
# =========================================================
machine_configs = {
    "magireco": {
        "display_name": "L マギアレコード 魔法少女まどか☆マギカ外伝",
        "file_key": "magireco",
        "link_url": "https://note.com/kenslodata/n/nf73890fb871e"
    },
    "godeater": {
        "display_name": "L ゴッドイーター リザレクション",
        "file_key": "godeater",
        "link_url": "https://note.com/kenslodata/n/ncbba8cff88be"
    },
    "franxx": {
        "display_name": "L ダーリン・イン・ザ・フランキス",
        "file_key": "franxx",
        "link_url": "https://note.com/kenslodata/n/n6139b4291e69"
    },
    "azurlane": {
        "display_name": "L アズールレーン THE ANIMETION",
        "file_key": "azurlane",
        "link_url": "https://note.com/kenslodata/n/n38b6be48a9da"
    },
    "saki": {
        "display_name": "L 咲-Saki-頂上決戦",
        "file_key": "saki",
        "link_url": "https://note.com/kenslodata/n/nda1d15f56223"
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

    "L ダーリン・イン・ザ・フランキス": {
        "exclude_games": 40,   # 除外ゲーム数
        "coin_moti": 30.8,     # コイン持ち
        "mode_options": ["ボーナス", "AT"],

        # 各プルダウンの選択肢
        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～250G", "251～500G", "501～750G", "751～1,000G", "1,001G以上"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        # ラベル設定
        "labels": {
            "mode": "ボナ／AT",
            "at_gap": "AT間ゲーム数",
            "prev_game": "前回AT当選ゲーム数",
            "prev_coin": "前回AT獲得枚数",
            "prev_diff": "前回AT終了時差枚数",
            "prev_renchan": "前回AT連荘数",
            "prev_type": "前回AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_type", "custom_condition"]  # ロックしない項目

    },

    "L アズールレーン THE ANIMETION": {
        "exclude_games": 40,
        "coin_moti": 25.8,
        "mode_options": ["ボーナス", "AT"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～300G", "301～600G", "601～900G", "901G以上"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "ボナ／AT",
            "at_gap": "AT間ゲーム数",
            "prev_game": "前回AT当選ゲーム数",
            "prev_coin": "前回AT獲得枚数",
            "prev_diff": "前回AT終了時差枚数",
            "prev_renchan": "前回AT連荘数",
            "prev_type": "前回AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_type", "custom_condition"]

    },

    "L 咲-Saki-頂上決戦": {
        "exclude_games": 40,
        "coin_moti": 32.1,
        "mode_options": ["CZ", "AT"],

        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～200G", "201～400G", "401～600G", "601G以上"],
        "prev_game_options": ["不問", "1～300G", "301～600G", "601～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001～1,500枚", "1,501～2,000枚", "2,001枚以上"],
        "prev_renchan_options": ["不問", "1連", "2～5連", "5連以上"],
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "CZ／AT",
            "at_gap": "AT間ゲーム数",
            "prev_game": "前回AT当選ゲーム数",
            "prev_coin": "前回AT獲得枚数",
            "prev_diff": "前回AT終了時差枚数",
            "prev_renchan": "前回AT連荘数",
            "prev_type": "前回AT種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["prev_type", "custom_condition"]

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
    "franxx": {
        "paid": "scrypt:32768:8:1$5fU98Y7AfIci9tIq$b921b1182bfdb1da0e432ab4650c47d91c8fd3cce6fcc31be0718466c2daf2397208e80da712e9e0c748918d983bc1db4216af5d2265c287ab43566df4770343"
    },
    "azurlane": {
        "paid": "scrypt:32768:8:1$PFBegCB04fHOgHF0$e710ae5a7fbea8429be66079386589a52d173fc972d45996937d61d45b8c7206db3393ddf501fafe3c08e1035251fd711f687ac81257300c82f6ab85659eeb5d"
    },
    "saki": {
        "paid": "scrypt:32768:8:1$T2kCZh0dXCl8alN2$479722165dcf0228f71bba801906880f231693bddb644ff25b7eaec0956376c150b818851202440702b7642d8666c235461bb6cc9df1453592eab1e35b892d11"
    }
}

__all__ = [
    "machine_configs",
    "machine_settings",
    "FREE_CUSTOM_LABEL",
    "apply_free_custom_label_override",
    "TOOL_PASSWORDS"
]
