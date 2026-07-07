"""One-shot helper: add playing-cards / mahjong style fields to pack_registry.json."""
from __future__ import annotations

import json
from pathlib import Path

REGISTRY = Path(__file__).with_name("pack_registry.json")

PLAYING_CARDS_STYLES: dict[str, str] = {
    "cards2-cc0": "flat",
    "byron-knoll-vector": "vector",
    "hayeah-vector-cards": "vector",
    "gilded-deck": "stylized",
    "ivoryred-pixel-poker": "pixel",
    "kenney-playing-cards-local": "flat",
    "mesmedir-bridge-size": "flat",
    "greywyvern-cardset": "flat",
    "greywyvern-cardset-svg": "vector",
    "greywyvern-pysol-medium": "flat",
    "greywyvern-pysol-small": "flat",
    "heratexx-4color-deck": "vector",
    "junus-ergin-4color": "vector",
    "letele-svg-cards": "vector",
    "revk-svg-cards": "vector",
    "mreliptik-stylized": "stylized",
    "kajiru-8bit": "pixel",
    "superdev-flat-cards": "flat",
    "kenney-playing-cards-ref": "flat",
    "unity-card-pack-vol2": "stylized",
    "pv-project-cards": "flat",
    "lempf-pixel-art-cards": "pixel",
    "devurandom-pc-style": "flat",
    "magnesus-cute-cards": "pixel",
    "george-blackwell-pixel": "pixel",
}

MAHJONG_STYLES: dict[str, str] = {
    "fluffystuff-riichi": "riichi",
    "samoheen-mahjong": "vector",
    "pyrano-ivory-tiles": "pixel",
    "natonato-simple-tiny": "pixel",
    "blueeyedrat-pixel": "pixel",
    "demching-mahjong-free": "vector",
    "lietxia-riichi-vector": "riichi",
    "tempai-riichi-svg": "riichi",
    "gamblemountain-riichi": "riichi",
    "moxica-tile-mahjong": "vector",
    "anisimova-vector-mahjong": "vector",
    "magory-free-pixel-set": "pixel",
    "codeinferno-mahjong": "pixel",
    "devurandom-pixel-mahjong": "pixel",
    "ffalt-mah-tile-sets": "vector",
    "unity-mahjong-hires": "vector",
    "unity-mahjong-3d": "3d",
    "demching-mahjong-paid": "vector",
    "pzuh-mahjong-pack": "vector",
    "royalgraphics-mahjong-basic": "vector",
    "royalgraphics-mahjong-premium": "vector",
    "royalgraphics-mahjong-dark-premium": "vector",
    "magory-mahjong-collection": "pixel",
    "almond-blossoms-mahjong-icons": "pixel",
    "unity-mahjong-mobile": "3d",
    "unity-mahjong-complete-set": "3d",
    "gameart2d-mahjong-pack": "vector",
}


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["license_categories"]["local-references"] = "本機參照"
    data["playing_cards_styles"] = {
        "pixel": "像素風",
        "vector": "向量／SVG",
        "flat": "扁平／標準牌面",
        "stylized": "藝術／裝飾風",
        "3d": "3D",
    }
    data["mahjong_styles"] = {
        "pixel": "像素風",
        "vector": "向量／傳統牌面",
        "riichi": "立直麻將",
        "3d": "3D",
    }

    for pack in data["packs"]:
        pid = pack["id"]
        if pack["asset_type"] == "playing-cards":
            pack["style"] = PLAYING_CARDS_STYLES[pid]
        elif pack["asset_type"] == "mahjong":
            pack["style"] = MAHJONG_STYLES[pid]

    REGISTRY.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Updated pack_registry.json with card/mahjong styles")


if __name__ == "__main__":
    main()
