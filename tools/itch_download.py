"""Download free itch.io asset packs without API key."""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


def fetch(url: str, data: bytes | None = None, method: str = "GET") -> bytes:
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "User-Agent": "Mozilla/5.0 (asset-library/1.0)",
            "Accept": "application/json, text/html, */*",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def download_itch_free(page_url: str, dest_dir: Path) -> list[str]:
    """Try multiple itch.io free-download endpoints."""
    page_url = page_url.rstrip("/")
    slug = page_url.split("/")[-1]
    user = page_url.split("//")[1].split(".")[0]

    attempts: list[tuple[str, str, bytes | None]] = [
        (f"{page_url}/download-url", "POST", urllib.parse.urlencode({"price": "0"}).encode()),
        (f"https://{user}.itch.io/{slug}/download-url", "POST", urllib.parse.urlencode({"price": "0"}).encode()),
        (f"{page_url}/purchase", "POST", urllib.parse.urlencode({"price": "0"}).encode()),
    ]

    download_urls: list[str] = []

    for url, method, body in attempts:
        try:
            raw = fetch(url, body, method)
            text = raw.decode("utf-8", errors="replace")
            if text.strip().startswith("{"):
                payload = json.loads(text)
                if isinstance(payload, dict) and payload.get("url"):
                    download_urls.append(payload["url"])
            # HTML purchase page may contain filedn links
            download_urls.extend(re.findall(r"https://[^\"'\s>]+\.zip", text))
            download_urls.extend(re.findall(r"https://filedn\.com/[^\"'\s>]+", text))
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
            continue

    # Page HTML fallback
    try:
        html = fetch(page_url).decode("utf-8", errors="replace")
        download_urls.extend(re.findall(r"https://filedn\.com/[^\"'\s>]+", html))
        for m in re.finditer(r'data-upload_id="(\d+)"', html):
            upload_id = m.group(1)
            download_urls.append(f"{page_url}/file/{upload_id}")
    except urllib.error.URLError:
        pass

    saved: list[str] = []
    dest_dir.mkdir(parents=True, exist_ok=True)

    for dl_url in dict.fromkeys(download_urls):
        try:
            content = fetch(dl_url)
            if not content.startswith(b"PK"):
                continue
            zip_path = dest_dir / "pack.zip"
            zip_path.write_bytes(content)
            with zipfile.ZipFile(zip_path) as zf:
                zf.extractall(dest_dir)
            zip_path.unlink(missing_ok=True)
            saved.append(dl_url)
            break
        except (urllib.error.URLError, zipfile.BadZipFile, OSError):
            continue

    return saved


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: itch_download.py <itch_url> <dest_dir>")
        return 1
    urls = download_itch_free(sys.argv[1], Path(sys.argv[2]))
    if urls:
        print(f"OK: {urls[0]}")
        return 0
    print("FAIL: no download URL found")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
