"""Download files from OpenGameArt.org content pages."""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

OGA_BASE = "https://opengameart.org"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (asset-library/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


ASSET_SUFFIXES = {
    ".zip",
    ".7z",
    ".rar",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".wav",
    ".ogg",
    ".mp3",
    ".ai",
    ".eps",
}


def is_asset_file(name: str) -> bool:
    lower = name.lower()
    if lower.startswith("css_") or lower.endswith(".css"):
        return False
    for suffix in ASSET_SUFFIXES:
        if lower.endswith(suffix):
            return True
    return False


def find_file_links(html: str) -> list[str]:
    links: list[str] = []
    for match in re.finditer(r'href="(/sites/default/files/[^"]+)"', html):
        url = OGA_BASE + match.group(1)
        if is_asset_file(url):
            links.append(url)
    for match in re.finditer(
        r'href="(https://opengameart\.org/sites/default/files/[^"]+)"', html
    ):
        url = match.group(1)
        if is_asset_file(url):
            links.append(url)
    return list(dict.fromkeys(links))


def download_page(page_url: str, dest_dir: Path) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    html = fetch(page_url).decode("utf-8", errors="replace")
    saved: list[Path] = []
    for file_url in find_file_links(html):
        name = file_url.split("/")[-1]
        if "?" in name:
            name = name.split("?", 1)[0]
        target = dest_dir / name
        if target.exists() and target.stat().st_size > 0:
            saved.append(target)
            continue
        try:
            data = fetch(file_url)
        except urllib.error.URLError:
            continue
        if len(data) < 100:
            continue
        target.write_bytes(data)
        saved.append(target)
        if target.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(target) as zf:
                    zf.extractall(dest_dir)
            except zipfile.BadZipFile:
                pass
    return saved


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: oga_download.py <oga_page_url> <dest_dir>")
        return 1
    saved = download_page(sys.argv[1], Path(sys.argv[2]))
    if saved:
        for path in saved:
            print(f"OK: {path}")
        return 0
    print("FAIL: no files downloaded")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
