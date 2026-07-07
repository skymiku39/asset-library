"""Add paid character catalog entries and license-unclear UI/sound/character packs."""
from __future__ import annotations

import json
from pathlib import Path

REGISTRY = Path(__file__).with_name("pack_registry.json")

NEW_PACKS = [
    {
        "id": "chiewaters-neon-spire-dealer",
        "folder": "chiewaters-neon-spire-dealer",
        "name": "Neon-Spire: The Devil's Dealer — 2D VN Assets",
        "asset_type": "character",
        "style": "anime-2d",
        "license_category": "2-paid-commercial",
        "license": "購買後可商用",
        "author": "Chie Waters",
        "source_url": "https://chiewaters.itch.io/neon-spire-the-devils-dealer-2d-visual-novel-assets",
        "commercial": "需購買（$10.99+）",
        "attribution": "依購買條款",
        "note": "350 件賭場荷官／高 roller 立繪與場景，含作弊 UI",
        "status": "catalog-only",
    },
    {
        "id": "unity-2d-pixel-character-147",
        "folder": "unity-2d-pixel-character-147",
        "name": "2D Pixel Character Pack — 147 Characters",
        "asset_type": "character",
        "style": "pixel-art",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Unity Asset Store",
        "source_url": "https://assetstore.unity.com/packages/2d/characters/2d-pixel-character-pack-147-characters-20-weapons-369348",
        "commercial": "需購買（約 €4.59）",
        "attribution": "依 EULA",
        "note": "147 個像素角色 + 20 種武器",
        "status": "catalog-only",
    },
    {
        "id": "unity-topdown-hd-characters",
        "folder": "unity-topdown-hd-characters",
        "name": "TopDown HD Character Pack — Animated 2D",
        "asset_type": "character",
        "style": "pixel-art",
        "license_category": "2-paid-commercial",
        "license": "Unity Asset Store EULA",
        "author": "Unity Asset Store",
        "source_url": "https://assetstore.unity.com/packages/2d/characters/topdown-hd-character-pack-animated-2d-pixel-characters-282727",
        "commercial": "需購買（約 €9.19）",
        "attribution": "依 EULA",
        "note": "9 角色 8 方向動畫，含頭像與部分 UI 元件",
        "status": "catalog-only",
    },
    {
        "id": "bullseye-avatar-pack",
        "folder": "bullseye-avatar-pack",
        "name": "Avatar Pack by Bullseye",
        "asset_type": "character",
        "style": "vector-flat",
        "license_category": "3-license-unclear",
        "license": "未標示標準授權",
        "author": "Bull's-Eye Graphic Design (Bullseye)",
        "source_url": "https://opengameart.org/content/avatar-pack-by-bullseye",
        "commercial": "待確認",
        "attribution": "作者要求連結官網（口頭授權）",
        "note": "OGA「授權問題」收錄；網站無授權文件",
        "status": "pending-manual-download",
    },
    {
        "id": "lokif-gui-sounds",
        "folder": "lokif-gui-sounds",
        "name": "GUI Sound Effects by Lokif",
        "asset_type": "sound",
        "style": "ui-modern",
        "license_category": "3-license-unclear",
        "license": "未標示標準授權",
        "author": "Lokif",
        "source_url": "https://opengameart.org/content/gui-sound-effects",
        "commercial": "待確認",
        "attribution": "待確認",
        "note": "OGA 2009 上傳，頁面未選擇標準授權條款",
        "status": "pending-manual-download",
    },
    {
        "id": "oga-gui-pack-7binary",
        "folder": "oga-gui-pack-7binary",
        "name": "GUI Pack (Black/White Buttons)",
        "asset_type": "ui",
        "style": "flat-clean",
        "license_category": "3-license-unclear",
        "license": "未標示標準授權",
        "author": "7binaryStudios（OGA 上傳者）",
        "source_url": "https://opengameart.org/content/gui-pack",
        "commercial": "待確認",
        "attribution": "建議署名（非強制）",
        "note": "OGA 頁面 License 欄位空白，僅有建議署名說明",
        "status": "pending-manual-download",
    },
    {
        "id": "game-assets-66-ui-1",
        "folder": "game-assets-66-ui-1",
        "name": "Game User Interface #1",
        "asset_type": "ui",
        "style": "flat-clean",
        "license_category": "3-license-unclear",
        "license": "未標示標準授權",
        "author": "Game_assets_66",
        "source_url": "https://opengameart.org/content/game-user-interface-1",
        "commercial": "待確認",
        "attribution": "待確認",
        "note": "OGA 頁面未選擇標準授權；作者僅要求回報使用",
        "status": "pending-manual-download",
    },
]


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing_ids = {pack["id"] for pack in data["packs"]}
    added = 0
    for pack in NEW_PACKS:
        if pack["id"] not in existing_ids:
            data["packs"].append(pack)
            added += 1
    REGISTRY.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Added {added} catalog entries (skipped {len(NEW_PACKS) - added} duplicates)")


if __name__ == "__main__":
    main()
