# app/config/new.py

# ===================================================================
# 新ツール用機種設定
# ===================================================================
machines = {
    "北斗": {
        "display_name": "北斗",          # 画面表示用
        "file_key": "hokuto",            # CSVファイル識別用
        "mode_options": ["AT"],          # 選択モード
        "exclude_games": 30,             # 除外ゲーム数
        "coin_moti": 35,                 # コイン持ち
        "locked_fields": [],             # ロック対象フィールド
    },
    "ヴヴヴ": {
        "display_name": "ヴヴヴ",
        "file_key": "vvv",
        "mode_options": ["CZ", "ボーナス"],
        "exclude_games": 30,
        "coin_moti": 35,
        "locked_fields": [],
    },
    "カバネリ": {
        "display_name": "カバネリ",
        "file_key": "kabaneri",
        "mode_options": ["ボーナス", "ST"],
        "exclude_games": 30,
        "coin_moti": 35,
        "locked_fields": [],
    },
}

# ===================================================================
# 注意:
# og_image, link_url, TOOL_PASSWORDS などは新ツールでは未使用
# 必要な場合は app 側で設定・管理する
# ===================================================================
