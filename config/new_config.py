from __future__ import annotations
from typing import Dict, Any
from werkzeug.security import generate_password_hash

# =========================================================
# 機種ごとのURLキー・表示名・CSV読み込み用キー
# =========================================================
machine_configs = {
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
    }
}

# =========================================================
# 機種ごとの条件設定・ラベル（display_nameをキーに）
# =========================================================
machine_settings = {
    "L 北斗の拳": {
        "exclude_games": 40,
        "coin_moti": 35.0,
        "mode_options": ["AT"],

        # 数値系項目: (最小, 最大, ステップ)
        "through": (0, 5, 1),
        "at_gap": (0, 2000, 50),
        "prev_game": (0, 1300, 50),
        "prev_coin": (0, 3000, 100),
        "prev_diff": (-3000, 1500, 100),
        "prev_renchan": (0, 10, 1),

        # 選択肢系
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "through": "スルー回数",
            "at_gap": "AT間G数",
            "prev_game": "前回当選G数",
            "prev_coin": "前回獲得枚数",
            "prev_diff": "前回差枚数",
            "prev_renchan": "前回連荘数",
            "prev_type": "前回種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "prev_type", "custom_condition"]

    },

    "L ゴブリンスレイヤー": {
        "exclude_games": 40,
        "coin_moti": 31.6,
        "mode_options": ["AT"],

        # 数値系項目: (最小, 最大, ステップ)
        "through": (0, 5, 1),
        "at_gap": (0, 2000, 50),
        "prev_game": (0, 1300, 50),
        "prev_coin": (0, 3000, 100),
        "prev_diff": (-3000, 1500, 100),
        "prev_renchan": (0, 10, 1),

        # 選択肢系
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "through": "スルー回数",
            "at_gap": "AT間G数",
            "prev_game": "前回当選G数",
            "prev_coin": "前回獲得枚数",
            "prev_diff": "前回差枚数",
            "prev_renchan": "前回連荘数",
            "prev_type": "前回種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "prev_type", "custom_condition"]

    },

    "L 主役は銭形4": {
        "exclude_games": 40,
        "coin_moti": 32.0,
        "mode_options": ["AT"],

        # 数値系項目: (最小, 最大, ステップ)
        "through": (0, 5, 1),
        "at_gap": (0, 2000, 50),
        "prev_game": (0, 1300, 50),
        "prev_coin": (0, 3000, 100),
        "prev_diff": (-3000, 1500, 100),
        "prev_renchan": (0, 10, 1),

        # 選択肢系
        "prev_type_options": ["不問"],
        "custom_condition_options": ["不問"],

        "labels": {
            "mode": "AT",
            "through": "スルー回数",
            "at_gap": "AT間G数",
            "prev_game": "前回当選G数",
            "prev_coin": "前回獲得枚数",
            "prev_diff": "前回差枚数",
            "prev_renchan": "前回連荘数",
            "prev_type": "前回種別",
            "custom_condition": "機種別条件"
        },

        "locked_fields": ["mode", "through", "at_gap", "prev_type", "custom_condition"]

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
