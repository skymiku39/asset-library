"""Download free itch.io asset packs without API key."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from http.cookiejar import CookieJar
from pathlib import Path

LOG_PATH = "debug-4e8286.log"


def _debug_log(hypothesis_id: str, location: str, message: str, data: dict) -> None:
    # #region agent log
    payload = {
        "sessionId": "4e8286",
        "runId": "itch-canonical-fix",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except OSError:
        pass
    # #endregion


def _opener() -> urllib.request.OpenerDirector:
    jar = CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def fetch(
    opener: urllib.request.OpenerDirector,
    url: str,
    data: bytes | None = None,
    method: str = "GET",
    *,
    referer: str | None = None,
) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (asset-library/1.0)",
        "Accept": "application/json, text/html, */*",
    }
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["X-Requested-With"] = "XMLHttpRequest"
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with opener.open(req, timeout=120) as resp:
        return resp.read()


def _parse_page(html: str) -> tuple[str, list[str]]:
    csrf_match = re.search(r'name="csrf_token"\s+value="([^"]+)"', html)
    upload_ids = re.findall(r'data-upload_id="(\d+)"', html)
    return (csrf_match.group(1) if csrf_match else "", list(dict.fromkeys(upload_ids)))


def _canonical_page_url(html: str, page_url: str) -> str:
    """Resolve itch alias domains to the page URL used by download APIs."""
    for key in ("generate_download_url", "download_url"):
        match = re.search(rf'"{key}"\s*:\s*"([^"]+)"', html)
        if not match:
            continue
        url = match.group(1).replace("\\/", "/").rstrip("/")
        if url.endswith("/download_url"):
            return url[: -len("/download_url")]
    return page_url.rstrip("/")


def _cdn_url_from_file_post(
    opener: urllib.request.OpenerDirector,
    page_url: str,
    upload_id: str,
    csrf: str,
    referer: str,
) -> str | None:
    body = urllib.parse.urlencode({"csrf_token": csrf}).encode()
    try:
        raw = fetch(opener, f"{page_url}/file/{upload_id}", body, "POST", referer=referer)
        payload = json.loads(raw.decode("utf-8"))
        url = payload.get("url", "").replace("\\/", "/")
        return url or None
    except (urllib.error.URLError, json.JSONDecodeError, AttributeError):
        return None


def _save_content(content: bytes, dest_dir: Path, upload_id: str) -> bool:
    dest_dir.mkdir(parents=True, exist_ok=True)
    if content.startswith(b"PK"):
        zip_path = dest_dir / "pack.zip"
        zip_path.write_bytes(content)
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(dest_dir)
        zip_path.unlink(missing_ok=True)
        return True

    if content.startswith(b"Rar!"):
        (dest_dir / "pack.rar").write_bytes(content)
        return True

    ext = ".png" if content.startswith(b"\x89PNG") else ".bin"
    (dest_dir / f"download-{upload_id}{ext}").write_bytes(content)
    return True


def download_itch_free(page_url: str, dest_dir: Path) -> list[str]:
    """Download the first available free file from an itch.io page."""
    page_url = page_url.rstrip("/")
    opener = _opener()
    dest_dir.mkdir(parents=True, exist_ok=True)

    try:
        page_html = fetch(opener, page_url).decode("utf-8", errors="replace")
    except urllib.error.URLError:
        return []

    api_url = _canonical_page_url(page_html, page_url)
    _debug_log(
        "H8",
        "itch_download.py:download_itch_free",
        "resolved api url",
        {"requested": page_url, "api_url": api_url, "alias": api_url != page_url.rstrip("/")},
    )

    csrf, upload_ids = _parse_page(page_html)
    if not csrf:
        return []

    # Demo / direct download shortcut (skips purchase wall on some paid pages).
    for upload_id in upload_ids:
        cdn_url = _cdn_url_from_file_post(opener, api_url, upload_id, csrf, page_url)
        if not cdn_url:
            continue
        try:
            content = fetch(opener, cdn_url, referer=page_url)
            if _save_content(content, dest_dir, upload_id):
                return [cdn_url]
        except urllib.error.URLError:
            continue

    body = urllib.parse.urlencode(
        {"csrf_token": csrf, "upload_id": upload_ids[0]} if upload_ids else {"csrf_token": csrf}
    ).encode()

    try:
        raw = fetch(opener, f"{api_url}/download_url", body, "POST", referer=page_url)
        payload = json.loads(raw.decode("utf-8"))
        if payload.get("errors"):
            return []
        dl_page_url = payload.get("url", "").replace("\\/", "/")
    except (urllib.error.URLError, json.JSONDecodeError, AttributeError):
        return []

    if not dl_page_url:
        return []

    try:
        dl_html = fetch(opener, dl_page_url, referer=page_url).decode("utf-8", errors="replace")
    except urllib.error.URLError:
        return []

    dl_csrf, dl_upload_ids = _parse_page(dl_html)
    upload_id = (dl_upload_ids or upload_ids or [None])[0]
    if not upload_id:
        return []

    csrf = dl_csrf or csrf
    cdn_url = _cdn_url_from_file_post(opener, api_url, upload_id, csrf, dl_page_url)
    if not cdn_url:
        return []

    try:
        content = fetch(opener, cdn_url, referer=dl_page_url)
        if _save_content(content, dest_dir, upload_id):
            return [cdn_url]
    except urllib.error.URLError:
        return []

    return []


def main() -> int:
    import sys

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
