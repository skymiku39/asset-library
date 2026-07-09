"""Download free DLsite trial/demo zip packs (no login required)."""
from __future__ import annotations

import re
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

_TRIAL_HREF = re.compile(
    r'href="(?P<url>//trial\.dlsite\.com/[^"]+_trial\.zip)"',
    re.IGNORECASE,
)


def parse_trial_zip_url(product_url: str, html: str | None = None) -> str | None:
    """Return https trial zip URL embedded in a DLsite product page."""
    if html is None:
        req = urllib.request.Request(
            product_url,
            headers={"User-Agent": "Mozilla/5.0 (asset-library/1.0)"},
        )
        try:
            html = urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")
        except urllib.error.URLError:
            return None
    match = _TRIAL_HREF.search(html)
    if not match:
        return None
    return "https:" + match.group("url")


def _has_assets(folder: Path) -> bool:
    if not folder.exists():
        return False
    for item in folder.rglob("*"):
        if not item.is_file():
            continue
        if item.name in {"SOURCE_LICENSE.md", "README.md", "trial.zip"}:
            continue
        if item.suffix.lower() in {".url", ".md"}:
            continue
        return True
    return False


def download_trial(product_url: str, dest_dir: Path) -> bool:
    """Download and extract a DLsite trial zip into dest_dir."""
    if _has_assets(dest_dir):
        return True

    trial_url = parse_trial_zip_url(product_url)
    if not trial_url:
        return False

    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "trial.zip"
    try:
        req = urllib.request.Request(
            trial_url,
            headers={"User-Agent": "Mozilla/5.0 (asset-library/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = resp.read()
    except urllib.error.URLError:
        return False

    if not data.startswith(b"PK"):
        return False

    zip_path.write_bytes(data)
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_dir)
    finally:
        zip_path.unlink(missing_ok=True)
    return _has_assets(dest_dir)


def main() -> int:
    import sys

    if len(sys.argv) < 3:
        print("Usage: dlsite_download.py <product_url> <dest_dir>")
        return 1
    ok = download_trial(sys.argv[1], Path(sys.argv[2]))
    print("OK" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
