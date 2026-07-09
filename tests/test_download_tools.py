from __future__ import annotations

import importlib.util
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, TOOLS / filename)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


itch_mod = load_module("itch_download", "itch_download.py")
kenney_mod = load_module("kenney_download", "kenney_download.py")
dlsite_mod = load_module("dlsite_download", "dlsite_download.py")


class ItchDownloadTest(unittest.TestCase):
    def test_parse_page_extracts_csrf_and_upload_ids(self) -> None:
        html = (
            '<input name="csrf_token" value="abc123" />'
            '<a data-upload_id="99"></a>'
            '<a data-upload_id="100"></a>'
        )
        csrf, upload_ids = itch_mod._parse_page(html)
        self.assertEqual(csrf, "abc123")
        self.assertEqual(upload_ids, ["99", "100"])

    def test_save_content_extracts_zip(self) -> None:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("hello.txt", "world")
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            self.assertTrue(itch_mod._save_content(buf.getvalue(), dest, "1"))
            self.assertTrue((dest / "hello.txt").exists())

    def test_save_content_writes_png(self) -> None:
        png = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            self.assertTrue(itch_mod._save_content(png, dest, "42"))
            self.assertTrue((dest / "download-42.png").exists())


class KenneyDownloadTest(unittest.TestCase):
    def test_find_zip_links_parses_media_urls(self) -> None:
        html = (
            '<a href="https://kenney.nl/media/pages/assets/pixel-ui-pack/'
            'abc/kenney_pixel-ui-pack.zip">Download</a>'
        )
        original = kenney_mod.fetch
        kenney_mod.fetch = lambda _url: html.encode()  # type: ignore[assignment]
        try:
            links = kenney_mod.find_zip_links("pixel-ui-pack")
        finally:
            kenney_mod.fetch = original  # type: ignore[assignment]

        self.assertEqual(len(links), 1)
        self.assertIn("kenney_pixel-ui-pack.zip", links[0])


class DlsiteDownloadTest(unittest.TestCase):
    def test_parse_trial_zip_url_from_html(self) -> None:
        html = (
            '<a href="//trial.dlsite.com/doujin/RJ01280000/'
            'RJ01279308_trial.zip">trial</a>'
        )
        url = dlsite_mod.parse_trial_zip_url("https://example.com", html)
        self.assertEqual(
            url,
            "https://trial.dlsite.com/doujin/RJ01280000/RJ01279308_trial.zip",
        )

    def test_parse_trial_zip_url_missing(self) -> None:
        self.assertIsNone(dlsite_mod.parse_trial_zip_url("https://example.com", "<html></html>"))


if __name__ == "__main__":
    unittest.main()
