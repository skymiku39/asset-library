"""Discovery ledger for adult-18plus source searches and verification.

Machine-readable source of truth: tools/discovery_ledger.json
Human-readable report: catalog/discovery-ledger.md
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
LEDGER_PATH = TOOLS / "discovery_ledger.json"
MARKDOWN_PATH = ROOT / "catalog" / "discovery-ledger.md"
REGISTRY_PATH = TOOLS / "pack_registry.json"

SCHEMA_VERSION = 1


def today() -> str:
    return date.today().isoformat()


def empty_ledger() -> dict[str, Any]:
    return {
        "version": SCHEMA_VERSION,
        "updated": today(),
        "scope": "adult-18plus",
        "purpose": "記錄已查詢網站、關鍵字／篩選條件、候選與已確認條目，供後續自動化驗證",
        "sites": [],
        "queries": [],
        "candidates": [],
    }


def load_ledger() -> dict[str, Any]:
    if not LEDGER_PATH.exists():
        return empty_ledger()
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def save_ledger(data: dict[str, Any]) -> None:
    data["updated"] = today()
    data["version"] = SCHEMA_VERSION
    LEDGER_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def upsert_by_id(items: list[dict], item: dict) -> None:
    for i, existing in enumerate(items):
        if existing.get("id") == item["id"]:
            items[i] = {**existing, **item}
            return
    items.append(item)


def ensure_site(data: dict, site: dict) -> None:
    upsert_by_id(data["sites"], site)


def ensure_query(data: dict, query: dict) -> None:
    upsert_by_id(data["queries"], query)


def ensure_candidate(data: dict, candidate: dict) -> None:
    upsert_by_id(data["candidates"], candidate)


def slug_from_url(url: str) -> str:
    cleaned = re.sub(r"^https?://", "", url.rstrip("/").lower())
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned).strip("-")
    return cleaned[:80]


VERDICT_LABELS = {
    "ingested": "已收錄到素材庫",
    "verified-downloadable": "已確認可下載（尚未／不需收錄）",
    "rejected-paywall": "需付費／登入牆",
    "rejected-broken": "連結失效或無法下載",
    "rejected-duplicate": "與既有套件重複",
    "rejected-non-asset": "非素材（遊戲／工具等）",
    "rejected-license": "授權不合／不可商用",
    "pending": "待確認",
}


def render_markdown(data: dict[str, Any]) -> str:
    sites = {s["id"]: s for s in data.get("sites", [])}
    lines: list[str] = [
        "# 18+ 素材搜尋履歷（Discovery Ledger）",
        "",
        f"> 更新：{data.get('updated', today())}｜機器可讀：`tools/discovery_ledger.json`",
        "",
        data.get("purpose", ""),
        "",
        "## 已查詢網站",
        "",
        "| 網站 ID | 名稱 | 網址 | 備註 |",
        "|---------|------|------|------|",
    ]
    for site in data.get("sites", []):
        lines.append(
            f"| `{site['id']}` | {site.get('name', '')} | {site.get('base_url', '')} | {site.get('notes', '')} |"
        )

    lines.extend(
        [
            "",
            "## 查詢紀錄（關鍵字／篩選）",
            "",
            "| 查詢 ID | 網站 | 關鍵字／標籤 | 查詢網址 | 最近檢查 | 狀態 | 結果摘要 |",
            "|---------|------|--------------|----------|----------|------|----------|",
        ]
    )
    for q in data.get("queries", []):
        site = sites.get(q.get("site_id", ""), {})
        kw = ", ".join(q.get("keywords", []) or q.get("tags", []) or [])
        lines.append(
            "| `{id}` | {site} | {kw} | {url} | {checked} | {status} | {summary} |".format(
                id=q["id"],
                site=site.get("name", q.get("site_id", "")),
                kw=kw or "—",
                url=q.get("url", ""),
                checked=q.get("last_checked", ""),
                status=q.get("status", ""),
                summary=q.get("result_summary", q.get("notes", "")),
            )
        )

    lines.extend(
        [
            "",
            "## 已確認／候選條目",
            "",
            "| 條目 ID | 標題 | 來源 URL | 判決 | 對應 pack_id | 驗證 |",
            "|---------|------|----------|------|--------------|------|",
        ]
    )
    for c in data.get("candidates", []):
        verdict = c.get("verdict", "pending")
        label = VERDICT_LABELS.get(verdict, verdict)
        verify = c.get("verify") or {}
        vtxt = "—"
        if verify:
            if verify.get("error"):
                vtxt = f"fail: {verify['error']}"
            else:
                bits = []
                if verify.get("http_ok") is True:
                    bits.append("http_ok")
                if verify.get("downloadable") is True:
                    bits.append("downloadable")
                if verify.get("last_verify_at"):
                    bits.append(str(verify["last_verify_at"]))
                vtxt = ", ".join(bits) or "checked"
        lines.append(
            "| `{id}` | {title} | {url} | {label} | `{pack}` | {vtxt} |".format(
                id=c.get("id", ""),
                title=(c.get("title") or "")[:40],
                url=c.get("url", ""),
                label=label,
                pack=c.get("pack_id") or "—",
                vtxt=vtxt,
            )
        )

    lines.extend(
        [
            "",
            "## 自動化驗證",
            "",
            "```bash",
            "uv run python tools/verify_discovery_ledger.py",
            "uv run python tools/discovery_ledger.py --render",
            "```",
            "",
            "驗證規則摘要：",
            "",
            "- `ingested`／`verified-downloadable`：來源 URL 應可 HTTP 存取；若標記可下載，應能偵測到下載入口或 trial zip。",
            "- `rejected-*`：保留履歷，但預設不強制要求仍可下載。",
            "- `pending`：等待人工或下一輪掃描。",
            "",
        ]
    )
    return "\n".join(lines)


def write_markdown(data: dict[str, Any] | None = None) -> Path:
    payload = data or load_ledger()
    MARKDOWN_PATH.write_text(render_markdown(payload), encoding="utf-8")
    return MARKDOWN_PATH


def _fetch(url: str, timeout: int = 30) -> tuple[int | None, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (asset-library/1.0)"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace") if hasattr(e, "read") else ""
        return e.code, body
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def detect_downloadable(url: str, html: str) -> bool:
    lower = html.lower()
    if "itch.io" in url:
        return bool(
            re.search(r'data-upload_id="\d+"', html)
            or "direct_download" in lower
            or "generate_download_url" in lower
            or "name your own price" in lower
            or "download now" in lower
        )
    if "dlsite.com" in url:
        return bool(re.search(r"trial\.dlsite\.com/[^\"']+_trial\.zip", html, re.I))
    return "download" in lower


def verify_candidate(candidate: dict, *, force: bool = False) -> dict:
    """Verify one candidate in-place and return verify payload."""
    verdict = candidate.get("verdict", "pending")
    if not force and verdict.startswith("rejected-") and verdict != "rejected-broken":
        # Still record a skip-style verify stamp for automation.
        payload = {
            "skipped": True,
            "reason": "rejected-entry",
            "last_verify_at": today(),
        }
        candidate["verify"] = payload
        return payload

    url = candidate.get("url", "")
    status, html_or_err = _fetch(url)
    payload: dict[str, Any] = {
        "http_status": status,
        "http_ok": status is not None and 200 <= status < 400,
        "last_verify_at": today(),
        "error": None,
        "downloadable": False,
    }
    if status is None:
        payload["error"] = html_or_err
        payload["http_ok"] = False
    elif payload["http_ok"]:
        payload["downloadable"] = detect_downloadable(url, html_or_err)
    else:
        payload["error"] = f"HTTP {status}"

    candidate["verify"] = payload
    if verdict in {"ingested", "verified-downloadable", "pending"} and not payload["http_ok"]:
        candidate["verdict"] = "rejected-broken"
    return payload


def sync_ingested_from_registry(data: dict) -> int:
    """Ensure downloaded adult packs appear as ingested candidates."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    added = 0
    for pack in registry.get("packs", []):
        if pack.get("asset_type") != "adult-18plus":
            continue
        url = (pack.get("source_url") or "").rstrip("/")
        if not url:
            continue
        cid = "cand-" + slug_from_url(url)
        existing = next((c for c in data["candidates"] if c["id"] == cid), None)
        if existing and existing.get("verdict") == "ingested":
            existing["pack_id"] = pack["id"]
            continue
        ensure_candidate(
            data,
            {
                "id": cid,
                "url": url,
                "title": pack.get("name", pack["id"]),
                "site_id": (
                    "itch-io"
                    if "itch.io" in url
                    else "dlsite-maniax"
                    if "dlsite.com" in url
                    else "other"
                ),
                "query_ids": [],
                "found_at": today(),
                "downloadable": pack.get("status") == "downloaded",
                "license_hint": pack.get("license", ""),
                "verdict": (
                    "ingested"
                    if pack.get("status") == "downloaded"
                    else "rejected-paywall"
                    if pack.get("status") == "catalog-only"
                    and "付費" in (pack.get("license") or "")
                    else "rejected-broken"
                    if "失效" in (pack.get("note") or "")
                    else "pending"
                ),
                "pack_id": pack["id"],
                "verified_at": today() if pack.get("status") == "downloaded" else None,
            },
        )
        added += 1
    return added


def seed_known_queries(data: dict) -> None:
    ensure_site(
        data,
        {
            "id": "itch-io",
            "name": "itch.io",
            "base_url": "https://itch.io",
            "notes": "免費／PWYW 素材主來源；注意別名子網域下載 API",
        },
    )
    ensure_site(
        data,
        {
            "id": "dlsite-maniax",
            "name": "DLsite Maniax",
            "base_url": "https://www.dlsite.com/maniax",
            "notes": "R18 素材；關鍵字搜尋常 403，改以 maker profile／作品頁 trial zip",
        },
    )
    ensure_site(
        data,
        {
            "id": "web-search",
            "name": "Web Search (general)",
            "base_url": "https://www.google.com",
            "notes": "輔助發現作者／作品頁後再回 itch／DLsite 驗證",
        },
    )

    queries = [
        {
            "id": "q-itch-free-nsfw-sprites",
            "site_id": "itch-io",
            "url": "https://itch.io/game-assets/free/tag-nsfw/tag-sprites",
            "keywords": ["nsfw", "sprites", "free"],
            "filters": {"price": "free", "tags": ["nsfw", "sprites"]},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "免費 NSFW sprites 列表（約 80+）",
        },
        {
            "id": "q-itch-free-nsfw",
            "site_id": "itch-io",
            "url": "https://itch.io/game-assets/free/tag-nsfw",
            "keywords": ["nsfw", "free"],
            "filters": {"price": "free", "tags": ["nsfw"]},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "免費 NSFW assets 總表",
        },
        {
            "id": "q-itch-cc0-vn",
            "site_id": "itch-io",
            "url": "https://itch.io/game-assets/free/assets-cc0/genre-visual-novel",
            "keywords": ["cc0", "visual novel", "free"],
            "filters": {"price": "free", "license": "cc0", "genre": "visual-novel"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "CC0 VN 素材列表",
        },
        {
            "id": "q-itch-newest-free-nsfw",
            "site_id": "itch-io",
            "url": "https://itch.io/game-assets/newest/free/tag-nsfw",
            "keywords": ["nsfw", "free", "newest"],
            "filters": {"price": "free", "tags": ["nsfw"], "sort": "newest"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "最新免費 NSFW（年齡牆可能擋爬蟲）",
        },
        {
            "id": "q-dlsite-kw-tachie-trial",
            "site_id": "dlsite-maniax",
            "url": "https://www.dlsite.com/maniax/fsr/=/keyword/%E7%AB%8B%E3%81%A1%E7%B5%B5%E7%B4%A0%E6%9D%90%20%E4%BD%93%E9%A8%93%E7%89%88",
            "keywords": ["立ち絵素材", "体験版"],
            "filters": {"keyword_search": True},
            "last_checked": today(),
            "status": "blocked",
            "result_summary": "關鍵字搜尋常回 HTTP 403",
        },
        {
            "id": "q-dlsite-maker-morinooku",
            "site_id": "dlsite-maniax",
            "url": "https://www.dlsite.com/maniax/circle/profile/=/maker_id/RG29726.html",
            "keywords": ["maker_id:RG29726", "森の奥の隠れ里"],
            "filters": {"maker_id": "RG29726"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "作者頁掃描；多套立繪 trial 已收",
        },
        {
            "id": "q-dlsite-maker-raiko",
            "site_id": "dlsite-maniax",
            "url": "https://www.dlsite.com/maniax/circle/profile/=/maker_id/RG66647.html",
            "keywords": ["maker_id:RG66647", "立ち絵素材RAIKO"],
            "filters": {"maker_id": "RG66647"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "RAIKO 立繪 trial 分批收錄中",
        },
        {
            "id": "q-dlsite-maker-kuusou",
            "site_id": "dlsite-maniax",
            "url": "https://www.dlsite.com/maniax/circle/profile/=/maker_id/RG01010253.html",
            "keywords": ["maker_id:RG01010253", "空想番外地"],
            "filters": {"maker_id": "RG01010253"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "空想番外地 R18 立繪 trial",
        },
        {
            "id": "q-dlsite-maker-snow",
            "site_id": "dlsite-maniax",
            "url": "https://www.dlsite.com/maniax/circle/profile/=/maker_id/RG01012324.html",
            "keywords": ["maker_id:RG01012324", "Snow Material"],
            "filters": {"maker_id": "RG01012324"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "Snow Material；部分作品無 trial",
        },
        {
            "id": "q-web-free-nsfw-cc0",
            "site_id": "web-search",
            "url": "websearch:itch.io free NSFW CC0 visual novel sprite",
            "keywords": ["itch.io", "free", "NSFW", "CC0", "visual novel", "sprite"],
            "filters": {"engine": "web-search"},
            "last_checked": today(),
            "status": "checked",
            "result_summary": "用於發現 SpicyLyon／Eros／Leaflet／Kuminer 等",
        },
    ]
    # 其餘 DLsite maker（與 discover_dlsite_trials.py 同步，供自動化覆核）
    extra_makers = [
        ("nyancheruto", "RG01039776", "にゃんちぇると"),
        ("fattyu", "RG61015", "ふぁっちゅ"),
        ("pincree", "RG65563", "Pincree"),
        ("wizpack", "RG01003985", "素材WIZPACK"),
        ("ramuniku", "RG01062657", "らむにくの素材屋さん"),
        ("reigasou", "RG63073", "れいが荘素材専門店"),
        ("kinokoru", "RG44045", "キノコル"),
        ("bazuneko", "RG53789", "バズ猫工務店"),
        ("nozu", "RG01045611", "乃図制作所"),
        ("kikunii", "RG27887", "菊にぃ"),
        ("waifukoubou", "RG01075080", "WaifuKoubou"),
        ("mashiro-lab", "RG01066181", "Mashiro Lab."),
        ("spacedoughnut", "RG65654", "スペースドーナツ"),
        ("tsukikage", "RG01051734", "月影"),
    ]
    for slug, mid, name in extra_makers:
        queries.append(
            {
                "id": f"q-dlsite-maker-{slug}",
                "site_id": "dlsite-maniax",
                "url": f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{mid}.html",
                "keywords": [f"maker_id:{mid}", name],
                "filters": {"maker_id": mid},
                "last_checked": today(),
                "status": "checked",
                "result_summary": f"maker profile 掃描清單：{name}",
            }
        )
    for q in queries:
        ensure_query(data, q)


def bootstrap() -> dict:
    data = load_ledger()
    seed_known_queries(data)
    sync_ingested_from_registry(data)
    save_ledger(data)
    write_markdown(data)
    return data


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Manage discovery ledger")
    parser.add_argument("--bootstrap", action="store_true", help="Seed sites/queries and sync registry")
    parser.add_argument("--render", action="store_true", help="Render markdown only")
    parser.add_argument("--sync-registry", action="store_true", help="Sync ingested packs from registry")
    args = parser.parse_args(argv)

    if args.bootstrap or (not LEDGER_PATH.exists() and not args.render):
        bootstrap()
        print(f"bootstrapped {LEDGER_PATH}")
        print(f"wrote {MARKDOWN_PATH}")
        return 0

    data = load_ledger()
    if args.sync_registry:
        n = sync_ingested_from_registry(data)
        save_ledger(data)
        print(f"synced {n} candidates from registry")
    if args.render or args.sync_registry:
        write_markdown(data)
        print(f"wrote {MARKDOWN_PATH}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
