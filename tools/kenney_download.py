"""Kenney.nl direct zip download (no donation gate bypass beyond public links)."""
from __future__ import annotations

import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (asset-library/1.0)"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def find_zip_links(asset_slug: str) -> list[str]:
    page = f"https://kenney.nl/assets/{asset_slug}"
    try:
        html = fetch(page).decode("utf-8", errors="replace")
    except urllib.error.URLError:
        return []
    links = re.findall(
        rf'https://kenney\.nl/media/pages/assets/{re.escape(asset_slug)}/[^"\']+\.zip',
        html,
        flags=re.I,
    )
    return list(dict.fromkeys(links))


def download_asset(asset_slug: str, dest_dir: Path) -> bool:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for url in find_zip_links(asset_slug):
        try:
            content = fetch(url)
        except urllib.error.URLError:
            continue
        if not content.startswith(b"PK"):
            continue
        zip_path = dest_dir / "pack.zip"
        zip_path.write_bytes(content)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_dir)
        zip_path.unlink(missing_ok=True)
        return True
    return False


def main() -> int:
    import sys

    if len(sys.argv) < 3:
        print("Usage: kenney_download.py <asset_slug> <dest_dir>")
        return 1
    ok = download_asset(sys.argv[1], Path(sys.argv[2]))
    print("OK" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
