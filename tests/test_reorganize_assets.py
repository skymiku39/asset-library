from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
SPEC = importlib.util.spec_from_file_location("reorganize_assets", TOOLS / "reorganize_assets.py")
assert SPEC and SPEC.loader
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ReorganizeAssetsTest(unittest.TestCase):
    def test_render_source_license_contains_required_fields(self) -> None:
        pack = {
            "name": "Test Pack",
            "license": "CC0 1.0 Universal",
            "author": "Tester",
            "source_url": "https://example.com/pack",
            "commercial": "允許",
            "attribution": "不需要",
            "note": "demo",
        }
        text = mod.render_source_license(pack, "撲克牌", "完全免費授權商用")
        self.assertIn("Test Pack", text)
        self.assertIn("https://example.com/pack", text)
        self.assertIn("CC0 1.0 Universal", text)
        self.assertIn("demo", text)

    def test_target_dir_uses_license_and_asset_type(self) -> None:
        pack = {
            "license_category": "1-free-commercial",
            "asset_type": "playing-cards",
            "folder": "cards2-cc0",
        }
        path = mod.target_dir(pack)
        expected = ("1-free-commercial", "playing-cards", "cards2-cc0")
        self.assertEqual(path.parts[-3:], expected)

    def test_target_dir_inserts_style_level_when_present(self) -> None:
        pack = {
            "license_category": "1-free-commercial",
            "asset_type": "character",
            "style": "pixel-art",
            "folder": "chromoxi-good-and-evil",
        }
        path = mod.target_dir(pack)
        self.assertEqual(
            path.parts[-4:],
            ("1-free-commercial", "character", "pixel-art", "chromoxi-good-and-evil"),
        )

    def test_target_dir_without_style_has_no_extra_level(self) -> None:
        pack = {
            "license_category": "1-free-commercial",
            "asset_type": "character",
            "folder": "some-pack",
        }
        path = mod.target_dir(pack)
        self.assertEqual(path.parts[-3:], ("1-free-commercial", "character", "some-pack"))

    def test_render_source_license_includes_style_when_provided(self) -> None:
        pack = {
            "name": "Styled Pack",
            "license": "CC0 1.0 Universal",
            "author": "Tester",
            "source_url": "https://example.com/pack",
            "commercial": "允許",
            "attribution": "不需要",
        }
        text = mod.render_source_license(pack, "角色", "完全免費授權商用", "像素風")
        self.assertIn("| 風格 | 像素風 |", text)
        self.assertIn("風格：**像素風**", text)

    def test_render_source_license_omits_style_when_absent(self) -> None:
        pack = {
            "name": "Plain Pack",
            "license": "CC0 1.0 Universal",
            "author": "Tester",
            "source_url": "https://example.com/pack",
            "commercial": "允許",
            "attribution": "不需要",
        }
        text = mod.render_source_license(pack, "撲克牌", "完全免費授權商用")
        self.assertNotIn("風格", text)

    def test_collect_styles_merges_every_style_map(self) -> None:
        data = {
            "character_styles": {"pixel-art": "像素風"},
            "sound_styles": {"ui-modern": "現代 UI 介面音"},
            "ui_styles": {"flat-clean": "扁平／簡潔"},
            "asset_types": {"ui": "UI"},
        }
        styles = mod.collect_styles(data)
        self.assertEqual(styles["pixel-art"], "像素風")
        self.assertEqual(styles["ui-modern"], "現代 UI 介面音")
        self.assertEqual(styles["flat-clean"], "扁平／簡潔")
        self.assertNotIn("ui", styles)

    def test_registry_ui_packs_use_declared_styles(self) -> None:
        import json

        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        ui_styles = data.get("ui_styles", {})
        ui_packs = [p for p in data["packs"] if p["asset_type"] == "ui"]
        self.assertTrue(ui_packs, "registry should contain UI packs")
        for pack in ui_packs:
            self.assertIn(pack.get("style"), ui_styles)

    def test_registry_playing_cards_packs_use_declared_styles(self) -> None:
        import json

        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        card_styles = data.get("playing_cards_styles", {})
        card_packs = [p for p in data["packs"] if p["asset_type"] == "playing-cards"]
        self.assertTrue(card_packs, "registry should contain playing-cards packs")
        for pack in card_packs:
            self.assertIn(pack.get("style"), card_styles)

    def test_registry_mahjong_packs_use_declared_styles(self) -> None:
        import json

        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        mahjong_styles = data.get("mahjong_styles", {})
        mahjong_packs = [p for p in data["packs"] if p["asset_type"] == "mahjong"]
        self.assertTrue(mahjong_packs, "registry should contain mahjong packs")
        for pack in mahjong_packs:
            self.assertIn(pack.get("style"), mahjong_styles)

    def test_registry_mixed_packs_use_declared_styles(self) -> None:
        import json

        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        mixed_styles = data.get("mixed_styles", {})
        mixed_packs = [p for p in data["packs"] if p["asset_type"] == "mixed"]
        self.assertTrue(mixed_packs, "registry should contain mixed packs")
        for pack in mixed_packs:
            self.assertIn(pack.get("style"), mixed_styles)

    def test_registry_paid_ui_and_sound_catalog_entries_exist(self) -> None:
        import json

        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        paid_ui = [
            p
            for p in data["packs"]
            if p["asset_type"] == "ui" and p["license_category"] == "2-paid-commercial"
        ]
        paid_sound = [
            p
            for p in data["packs"]
            if p["asset_type"] == "sound" and p["license_category"] == "2-paid-commercial"
        ]
        paid_character = [
            p
            for p in data["packs"]
            if p["asset_type"] == "character" and p["license_category"] == "2-paid-commercial"
        ]
        self.assertGreaterEqual(len(paid_ui), 3)
        self.assertGreaterEqual(len(paid_sound), 3)
        self.assertGreaterEqual(len(paid_character), 3)

    def test_registry_unclear_ui_sound_character_entries_exist(self) -> None:
        import json

        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        unclear_types = ("ui", "sound", "character")
        for asset_type in unclear_types:
            entries = [
                p
                for p in data["packs"]
                if p["asset_type"] == asset_type
                and p["license_category"] == "3-license-unclear"
            ]
            self.assertGreaterEqual(
                len(entries),
                1,
                f"expected at least one 3-license-unclear {asset_type} pack",
            )

    def test_target_dir_playing_cards_inserts_style_level(self) -> None:
        pack = {
            "license_category": "1-free-commercial",
            "asset_type": "playing-cards",
            "style": "vector",
            "folder": "byron-knoll-vector",
        }
        path = mod.target_dir(pack)
        self.assertEqual(
            path.parts[-4:],
            ("1-free-commercial", "playing-cards", "vector", "byron-knoll-vector"),
        )


REGISTRY = TOOLS / "pack_registry.json"


if __name__ == "__main__":
    unittest.main()
