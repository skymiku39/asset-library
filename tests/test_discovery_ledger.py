from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ledger_mod = load_module("discovery_ledger", "discovery_ledger.py")
discovery_run_mod = load_module("run_adult_discovery", "run_adult_discovery.py")


class DiscoveryLedgerTest(unittest.TestCase):
    def test_empty_ledger_shape(self) -> None:
        data = ledger_mod.empty_ledger()
        self.assertEqual(data["version"], 1)
        self.assertEqual(data["scope"], "adult-18plus")
        self.assertIn("sites", data)
        self.assertIn("queries", data)
        self.assertIn("candidates", data)

    def test_upsert_by_id(self) -> None:
        items: list[dict] = []
        ledger_mod.upsert_by_id(items, {"id": "a", "v": 1})
        ledger_mod.upsert_by_id(items, {"id": "a", "v": 2})
        ledger_mod.upsert_by_id(items, {"id": "b", "v": 1})
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["v"], 2)

    def test_detect_downloadable_itch_and_dlsite(self) -> None:
        itch_html = 'data-upload_id="123" generate_download_url'
        self.assertTrue(ledger_mod.detect_downloadable("https://x.itch.io/y", itch_html))
        dlsite_html = '//trial.dlsite.com/doujin/RJ1/RJ1_trial.zip'
        self.assertTrue(
            ledger_mod.detect_downloadable(
                "https://www.dlsite.com/maniax/work/=/product_id/RJ1.html",
                dlsite_html,
            )
        )
        self.assertFalse(ledger_mod.detect_downloadable("https://example.com", "<html></html>"))

    def test_render_markdown_includes_sections(self) -> None:
        data = ledger_mod.empty_ledger()
        data["sites"] = [{"id": "itch-io", "name": "itch.io", "base_url": "https://itch.io", "notes": ""}]
        data["queries"] = [
            {
                "id": "q1",
                "site_id": "itch-io",
                "url": "https://itch.io/game-assets/free/tag-nsfw",
                "keywords": ["nsfw", "free"],
                "last_checked": "2026-07-24",
                "status": "checked",
                "result_summary": "ok",
            }
        ]
        data["candidates"] = [
            {
                "id": "cand-1",
                "title": "Demo",
                "url": "https://example.itch.io/demo",
                "verdict": "ingested",
                "pack_id": "demo",
                "verify": {"http_ok": True, "downloadable": True, "last_verify_at": "2026-07-24"},
            }
        ]
        md = ledger_mod.render_markdown(data)
        self.assertIn("已查詢網站", md)
        self.assertIn("查詢紀錄", md)
        self.assertIn("已確認／候選條目", md)
        self.assertIn("q1", md)
        self.assertIn("cand-1", md)

    def test_bootstrap_writes_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            old_ledger = ledger_mod.LEDGER_PATH
            old_md = ledger_mod.MARKDOWN_PATH
            try:
                ledger_mod.LEDGER_PATH = tmp_path / "discovery_ledger.json"
                ledger_mod.MARKDOWN_PATH = tmp_path / "discovery-ledger.md"
                # Avoid depending on full registry sync path differences in temp;
                # call seed + render only.
                data = ledger_mod.empty_ledger()
                ledger_mod.seed_known_queries(data)
                ledger_mod.save_ledger(data)
                ledger_mod.write_markdown(data)
                self.assertTrue(ledger_mod.LEDGER_PATH.exists())
                self.assertTrue(ledger_mod.MARKDOWN_PATH.exists())
                loaded = json.loads(ledger_mod.LEDGER_PATH.read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(loaded["sites"]), 2)
                self.assertGreaterEqual(len(loaded["queries"]), 5)
            finally:
                ledger_mod.LEDGER_PATH = old_ledger
                ledger_mod.MARKDOWN_PATH = old_md

    def test_seed_includes_discover_makers(self) -> None:
        data = ledger_mod.empty_ledger()
        ledger_mod.seed_known_queries(data)
        maker_q = [q for q in data["queries"] if q["id"].startswith("q-dlsite-maker-")]
        self.assertGreaterEqual(len(maker_q), 10)
        ids = {q["filters"]["maker_id"] for q in maker_q if "filters" in q}
        self.assertIn("RG66647", ids)
        self.assertIn("RG01075080", ids)


class AdultDiscoveryFilterTest(unittest.TestCase):
    def test_extract_itch_links_skips_cdn_and_vrc(self) -> None:
        html = """
        https://static.itch.io/main
        https://bunnightfury.itch.io/faye-artemis-vrc
        https://leafletgames.itch.io/free-sprites-4-nudity
        https://kento-games.itch.io/foo-demo
        """
        got = discovery_run_mod.extract_itch_links(html)
        self.assertEqual(got, ["https://leafletgames.itch.io/free-sprites-4-nudity"])


if __name__ == "__main__":
    unittest.main()
