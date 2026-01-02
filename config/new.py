# ===================================================================
# 新ツール用機種設定
# ===================================================================

machines = {
    "北斗": {
        "display_name": "北斗",        # 画面表示用
        "file_key": "hokuto",          # CSVファイル識別用
        "exclude_games": 30,           # 除外ゲーム数
        "coin_moti": 35,               # コイン持ち
        "mode_options": ["AT"],        # 選択モード

        # 数値幅設定（最小最大）
        "through_options": {"min": 0, "max": 10, "step": 1},
        "prev_renchan_options": {"min": 0, "max": 10, "step": 1},
        "at_gap_options": {"min": 0, "max": 1000, "step": 100},
        "prev_diff_options": {"min": 0, "max": 1000, "step": 100},
        "prev_game1_options": {"min": 0, "max": 1000, "step": 100},
        "prev_game2_options": {"min": 0, "max": 1000, "step": 100},
        "prev_coin_options": {"min": 0, "max": 1000, "step": 100},
        "prev_type_options": ["不問", "CZ", "ボーナス", "AT"],

        # ロック対象フィールド
        "locked_fields": [],
    },

    "ヴヴヴ": {
        "display_name": "ヴヴヴ",
        "file_key": "vvv",
        "exclude_games": 30,
        "coin_moti": 35,
        "mode_options": ["CZ", "ボーナス"],

        "through_options": {"min": 0, "max": 10, "step": 1},
        "prev_renchan_options": {"min": 0, "max": 10, "step": 1},
        "at_gap_options": {"min": 0, "max": 1000, "step": 100},
        "prev_diff_options": {"min": 0, "max": 1000, "step": 100},
        "prev_game1_options": {"min": 0, "max": 1000, "step": 100},
        "prev_game2_options": {"min": 0, "max": 1000, "step": 100},
        "prev_coin_options": {"min": 0, "max": 1000, "step": 100},
        "prev_type_options": ["不問", "CZ", "ボーナス", "AT"],

        "locked_fields": [],
    },

    "カバネリ": {
        "display_name": "カバネリ",
        "file_key": "kabaneri",
        "exclude_games": 30,
        "coin_moti": 35,
        "mode_options": ["ボーナス", "ST"],

        "through_options": {"min": 0, "max": 10, "step": 1},
        "prev_renchan_options": {"min": 0, "max": 10, "step": 1},
        "at_gap_options": {"min": 0, "max": 1000, "step": 100},
        "prev_diff_options": {"min": 0, "max": 1000, "step": 100},
        "prev_game1_options": {"min": 0, "max": 1000, "step": 100},
        "prev_game2_options": {"min": 0, "max": 1000, "step": 100},
        "prev_coin_options": {"min": 0, "max": 1000, "step": 100},
        "prev_type_options": ["不問", "ボーナス", "ST"],

        "locked_fields": [],
    },
}
