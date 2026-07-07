from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


audit_mod = load_module("audit_catalog", "audit_catalog.py")
oga_mod = load_module("oga_download", "oga_download.py")


class AuditCatalogTest(unittest.TestCase):
    def test_audit_passes_on_current_registry(self) -> None:
        import json

        data = json.loads(audit_mod.REGISTRY.read_text(encoding="utf-8"))
        issues = audit_mod.audit(data)
        self.assertEqual(issues, [], "\n".join(issues))

    def test_audit_detects_missing_style(self) -> None:
        data = {
            "packs": [
                {
                    "id": "bad-ui",
                    "folder": "bad-ui",
                    "asset_type": "ui",
                    "license_category": "1-free-commercial",
                    "status": "catalog-only",
                }
            ],
            "ui_styles": {"flat-clean": "扁平"},
        }
        issues = audit_mod.audit(data)
        self.assertTrue(any("missing style" in issue for issue in issues))


class OgaDownloadTest(unittest.TestCase):
    def test_is_asset_file_filters_css(self) -> None:
        self.assertFalse(oga_mod.is_asset_file("css_xE-rWrJf.css"))
        self.assertTrue(oga_mod.is_asset_file("GUI_Sound_Effects_by_Lokif.7z"))
        self.assertTrue(oga_mod.is_asset_file("gui_pack_Black.zip"))


if __name__ == "__main__":
    unittest.main()
