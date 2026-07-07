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
        self.assertTrue(str(path).endswith("1-free-commercial/playing-cards/cards2-cc0".replace("/", "\\")) or str(path).endswith("1-free-commercial\\playing-cards\\cards2-cc0"))


if __name__ == "__main__":
    unittest.main()
