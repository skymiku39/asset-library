"""Apply mixed subcategories and paid UI/sound catalog entries."""
from __future__ import annotations

import json
from pathlib import Path

REGISTRY = Path(__file__).with_name("pack_registry.json")

MIXED_STYLES: dict[str, str] = {
    "sbs-2d-poker-pack": "poker-kit",
    "kenney-boardgame-ref": "boardgame",
    "unity-playing-card-pack": "poker-kit",
    "aarnituli-3d-cards": "poker-kit",
    "craftpix-poker-kit": "poker-kit",
    "unity-mahjong-assets": "mahjong-kit",
    "unity-mahjong-solitaire-kit": "mahjong-kit",
}

NEW_PACKS = [
    {
        "id": "unity-playmat-casinoui",
        "folder": "unity-playmat-casinoui",
        "name": "Playmat CasinoUI Set",
        "asset_type": "ui",
        "style": "flat-clean",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Playmat",
        "source_url": "https://assetstore.unity.com/packages/2d/gui/playmat-casinoui-set-258570",
        "commercial": "需購買",
        "attribution": "依 EULA",
        "note": "賭場撲克介面：按鈕、籌碼、牌桌 UI",
        "status": "catalog-only",
    },
    {
        "id": "unity-lucky-seven-casino-ui",
        "folder": "unity-lucky-seven-casino-ui",
        "name": "Lucky Seven Casino Game UI",
        "asset_type": "ui",
        "style": "casual-cartoon",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Unity Asset Store",
        "source_url": "https://assetstore.unity.com/packages/2d/gui/lucky-seven-casino-game-ui-162267",
        "commercial": "需購買（$15）",
        "attribution": "依 EULA",
        "note": "完整賭場遊戲 UI 場景與元件",
        "status": "catalog-only",
    },
    {
        "id": "unity-casino-ui-icons",
        "folder": "unity-casino-ui-icons",
        "name": "Casino Game UI Icons Pack",
        "asset_type": "ui",
        "style": "flat-clean",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Unity Asset Store",
        "source_url": "https://assetstore.unity.com/packages/2d/casino-game-ui-icons-pack-for-slots-poker-blackjack-roulette-and-361052",
        "commercial": "需購買（$21.99）",
        "attribution": "依 EULA",
        "note": "老虎機／撲克／輪盤賭場圖示集",
        "status": "catalog-only",
    },
    {
        "id": "unity-essential-card-sfx",
        "folder": "unity-essential-card-sfx",
        "name": "Essential Card Game Sound Effects",
        "asset_type": "sound",
        "style": "realistic-foley",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Cyberwave Orchestra",
        "source_url": "https://assetstore.unity.com/packages/audio/sound-fx/essential-card-game-sound-effects-365118",
        "commercial": "需購買（$29）",
        "attribution": "依 EULA",
        "note": "113 個洗牌／發牌／翻牌／骰子擬音（WAV）",
        "status": "catalog-only",
    },
    {
        "id": "unity-aaa-card-game-sfx",
        "folder": "unity-aaa-card-game-sfx",
        "name": "AAA Card Game (DCCG Sound Effects)",
        "asset_type": "sound",
        "style": "realistic-foley",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Epic Stock Media",
        "source_url": "https://assetstore.unity.com/packages/audio/sound-fx/card-game-sounds-112743",
        "commercial": "需購買",
        "attribution": "依 EULA",
        "note": "503 個 DCCG 音效：UI、發牌、魔法、環境",
        "status": "catalog-only",
    },
    {
        "id": "unity-card-board-sfx-music",
        "folder": "unity-card-board-sfx-music",
        "name": "Card & Board Games SFX and Music Pack",
        "asset_type": "sound",
        "style": "casino-bgm",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Unity Asset Store",
        "source_url": "https://assetstore.unity.com/packages/audio/sound-fx/card-board-games-sound-effects-and-music-pack-230753",
        "commercial": "需購買（約 €46）",
        "attribution": "依 EULA",
        "note": "520+ SFX 與 3 首爵士 BGM，適用撲克／麻將／棋類",
        "status": "catalog-only",
    },
]


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["mixed_styles"] = {
        "poker-kit": "撲克遊戲包（牌+籌碼+牌桌）",
        "mahjong-kit": "麻將遊戲包（牌+UI+範本）",
        "boardgame": "棋盤／通用遊戲包",
    }

    existing_ids = {pack["id"] for pack in data["packs"]}
    for pack in data["packs"]:
        if pack["asset_type"] == "mixed":
            pack["style"] = MIXED_STYLES[pack["id"]]

    for pack in NEW_PACKS:
        if pack["id"] not in existing_ids:
            data["packs"].append(pack)

    REGISTRY.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Updated mixed styles and paid UI/sound catalog entries")


if __name__ == "__main__":
    main()
