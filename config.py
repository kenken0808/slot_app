
from __future__ import annotations
from typing import Dict, Any

# 機種ごとのURLキーと表示名、CSV読み込み用ファイルキーを定義
machine_configs = {
    "magireco": {
        "display_name": "L マギアレコード 魔法少女まどか☆マギカ外伝",
        "file_key": "magireco"
    },
    "godeater": {
        "display_name": "L ゴッドイーター リザレクション",
        "file_key": "godeater"
    }
}

# 機種ごとの条件設定・ラベル等を定義（display_name をキーに）
machine_settings = {
    "L マギアレコード 魔法少女まどか☆マギカ外伝": {
        "exclude_games": 30,
        "coin_moti": 32.6,
        "mode_options": ["CZ", "ボーナス"],
        "through_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
        "at_gap_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_game_options": ["不問", "1～500G", "501～1,000G", "1,001G以上"],
        "prev_coin_options": ["不問", "1～1,000枚", "1,001～2,000枚", "2,001枚以上"],
        "prev_diff_options": ["不問", "-2,001枚以下", "-2,000～-1枚", "1～500枚", "501～1,000枚", "1,001枚以上"],
        "prev_renchan_options": ["不問", "1～3連", "4～7連", "8連以上"],
        "prev_type_options": ["不問", "下位", "上位"],
        "custom_condition_options": ["不問", "0スルー", "1スルー", "2スルー", "3スルー", "4スルー", "5スルー以上"],
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
        "locked_fields": []
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
        "locked_fields": ["mode", "through", "at_gap", "custom_condition"]  # ← 🔒 ロックしたい項目
    }
}


FREE_CUSTOM_LABEL: str = "機種別条件"


def apply_free_custom_label_override(
    settings: Dict[str, Any], display_name: str, plan_type: str
) -> Dict[str, Any]:

    if plan_type != "free":
        return settings

    # 元データを破壊しないため浅いコピーを作成
    new_settings = {**settings}
    labels = {**settings.get("labels", {})}

    labels["custom_condition"] = FREE_CUSTOM_LABEL
    new_settings["labels"] = labels

    return new_settings


__all__ = [
    "machine_configs",
    "machine_settings",
    "FREE_CUSTOM_LABEL",
    "apply_free_custom_label_override",
]

