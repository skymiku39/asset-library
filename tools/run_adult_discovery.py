"""Continue adult discovery: scrape known list pages, download new free packs, update ledger."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from discovery_ledger import (  # noqa: E402
    bootstrap,
    ensure_candidate,
    ensure_query,
    load_ledger,
    save_ledger,
    slug_from_url,
    today,
    write_markdown,
)
from dlsite_download import download_trial  # noqa: E402
from itch_download import download_itch_free  # noqa: E402

REG = ROOT / "tools" / "pack_registry.json"
RUN_LOG = ROOT / "tools" / "discovery_runs.ndjson"

LIST_PAGES = [
    (
        "q-itch-free-nsfw-sprites",
        "https://itch.io/game-assets/free/tag-nsfw/tag-sprites",
        ["nsfw", "sprites", "free"],
    ),
    (
        "q-itch-free-nsfw-tag-adult",
        "https://itch.io/game-assets/free/tag-adult/tag-sprites",
        ["adult", "sprites", "free"],
    ),
    (
        "q-itch-free-nsfw",
        "https://itch.io/game-assets/free/tag-nsfw",
        ["nsfw", "free"],
    ),
    (
        "q-itch-newest-free-nsfw",
        "https://itch.io/game-assets/newest/free/tag-nsfw",
        ["nsfw", "free", "newest"],
    ),
]


def log(msg: str, data: dict) -> None:
    payload = {
        "runId": "discovery-continue",
        "location": "run_adult_discovery.py",
        "message": msg,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with open(RUN_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read().decode("utf-8", "replace")


def extract_itch_links(html: str) -> list[str]:
    links = re.findall(r"https://([a-z0-9\-]+)\.itch\.io/([a-z0-9\-]+)", html, flags=re.I)
    skip_hosts = {"static", "img", "www", "web", "cdn"}
    # only match whole hyphen segments in the project slug (not author subdomain)
    skip_slug_tokens = {
        "vrc",
        "avatar",
        "shader",
        "unitypackage",
        "demo",
    }
    out: list[str] = []
    seen: set[str] = set()
    for host, slug in links:
        host_l = host.lower()
        slug_l = slug.lower()
        if host_l in skip_hosts:
            continue
        tokens = set(slug_l.split("-"))
        if tokens & skip_slug_tokens:
            continue
        if "vrc" in slug_l:  # compound like foo-vrc-bar
            continue
        u = f"https://{host_l}.itch.io/{slug_l}"
        if u in seen:
            continue
        seen.add(u)
        out.append(u)
    return out


def known_urls(registry: dict) -> set[str]:
    return {
        (p.get("source_url") or "").rstrip("/").lower()
        for p in registry.get("packs", [])
        if p.get("source_url")
    }


def has_files(dest: Path) -> bool:
    return any(
        p.is_file() and p.name not in {"SOURCE_LICENSE.md", "README.md"}
        for p in dest.rglob("*")
    )


MAKER_SCAN = [
    ("RG66647", "立ち絵素材RAIKO"),
    ("RG01075080", "WaifuKoubou"),
    ("RG01066181", "Mashiro Lab."),
    ("RG65654", "スペースドーナツ"),
    ("RG01051734", "月影"),
    ("RG01010253", "空想番外地"),
]


def continue_dlsite_makers(registry: dict, limit_per_maker: int = 6) -> list[str]:
    known = set()
    for p in registry["packs"]:
        known.update(re.findall(r"RJ\d+", p.get("source_url", "") + p.get("id", ""), flags=re.I))
    trial_re = re.compile(r"//trial\.dlsite\.com/[^\"']+_trial\.zip", re.I)
    added: list[str] = []
    for mid, author in MAKER_SCAN:
        html = fetch(f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{mid}.html")
        pids = set(re.findall(r"product_id/(RJ\d+)\.html", html))
        for page in (2, 3):
            try:
                ph = fetch(
                    f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{mid}.html/=/page/{page}"
                )
                pids |= set(re.findall(r"product_id/(RJ\d+)\.html", ph))
            except Exception:
                break
        maker_added = 0
        log("maker_scan", {"maker_id": mid, "pids": len(pids)})
        for pid in sorted(pids):
            if pid in known:
                continue
            purl = f"https://www.dlsite.com/maniax/work/=/product_id/{pid}.html"
            try:
                ph = fetch(purl)
            except Exception as e:
                log("dlsite_fail", {"pid": pid, "error": str(e)})
                continue
            if not trial_re.search(ph):
                continue
            if "画像素材" not in ph and "立ち絵" not in ph and "/worktype/IMT" not in ph:
                title_m = re.search(r'og:title" content="([^"]+)"', ph)
                title = title_m.group(1) if title_m else ""
                if "素材" not in title and "立ち絵" not in title:
                    continue
            title_m = re.search(r'og:title" content="([^"]+)"', ph)
            title = re.sub(r"\s*\|\s*DLsite.*$", "", title_m.group(1) if title_m else pid)
            folder = f"dlsite-{pid.lower()}-trial"
            dest = ROOT / "assets/1-free-commercial/adult-18plus/vn-sprite" / folder
            ok = download_trial(purl, dest)
            if not ok:
                continue
            registry["packs"].append(
                {
                    "id": folder,
                    "folder": folder,
                    "name": title + " 体験版",
                    "asset_type": "adult-18plus",
                    "style": "vn-sprite",
                    "license_category": "1-free-commercial",
                    "license": f"DLsite 體驗版（{author}；產品版條款請核對）",
                    "author": author,
                    "source_url": purl,
                    "commercial": "體驗版可評估；產品版多為商用可",
                    "attribution": "依作品頁",
                    "note": f"maker={mid}",
                    "status": "downloaded",
                }
            )
            known.add(pid)
            added.append(pid)
            maker_added += 1
            log("dlsite_ok", {"pid": pid, "maker_id": mid})
            print("DLSITE", mid, pid)
            if maker_added >= limit_per_maker:
                break
            time.sleep(0.12)
    return added


def main() -> int:
    ledger = bootstrap()
    registry = json.loads(REG.read_text(encoding="utf-8"))
    known = known_urls(registry)

    new_links: list[tuple[str, str]] = []  # query_id, url
    for qid, url, keywords in LIST_PAGES:
        ensure_query(
            ledger,
            {
                "id": qid,
                "site_id": "itch-io",
                "url": url,
                "keywords": keywords,
                "filters": {"price": "free", "tags": keywords},
                "last_checked": today(),
                "status": "checked",
                "result_summary": "",
            },
        )
        try:
            html = fetch(url)
            links = extract_itch_links(html)
            ensure_query(
                ledger,
                {
                    "id": qid,
                    "site_id": "itch-io",
                    "url": url,
                    "keywords": keywords,
                    "filters": {"price": "free", "tags": keywords},
                    "last_checked": today(),
                    "status": "checked",
                    "result_summary": f"parsed {len(links)} itch links",
                },
            )
            log("list_parsed", {"query": qid, "links": len(links)})
            for link in links:
                if link not in known:
                    new_links.append((qid, link))
        except Exception as e:
            ensure_query(
                ledger,
                {
                    "id": qid,
                    "site_id": "itch-io",
                    "url": url,
                    "keywords": keywords,
                    "last_checked": today(),
                    "status": "failed",
                    "result_summary": str(e),
                },
            )
            log("list_fail", {"query": qid, "error": str(e)})

    # also try a few curated new URLs
    curated = [
        ("q-web-free-nsfw-cc0", "https://quarkyifu.itch.io/angel-5"),
        ("q-web-free-nsfw-cc0", "https://quarkyifu.itch.io/blue-angel-visual-novel-browser-version"),
        ("q-itch-free-nsfw-sprites", "https://rilesu.itch.io/nsfw-random-stuff"),
        ("q-itch-free-nsfw-sprites", "https://panditastudio.itch.io/assets-pack-vol7-nsfw-vn-character"),
        ("q-itch-free-nsfw-sprites", "https://jitsukoan.itch.io/rpg-fantasy-girls-v-nsfw-edition"),
        ("q-web-free-nsfw-cc0", "https://breezy-the-sleazy.itch.io/free-nsfw-assets"),
    ]
    for qid, link in curated:
        if link.rstrip("/").lower() not in known:
            new_links.append((qid, link.rstrip("/").lower()))

    # unique preserve order
    seen: set[str] = set()
    uniq: list[tuple[str, str]] = []
    for qid, link in new_links:
        if link in seen:
            continue
        seen.add(link)
        uniq.append((qid, link))

    print("new_candidates", len(uniq))
    log("new_candidates", {"count": len(uniq), "sample": [u for _, u in uniq[:10]]})

    ingested = 0
    failed = 0
    for qid, link in uniq[:20]:  # cap per run
        cid = "cand-" + slug_from_url(link)
        slug = link.split("itch.io/")[-1].replace("/", "-")[:50]
        folder = f"itch-{slug}"
        dest = ROOT / "assets/3-license-unclear/adult-18plus/vn-sprite" / folder
        # prefer free-commercial folder only after license known; start unclear then we can reclass
        # Actually try download first; if ok register as unclear unless known author patterns
        license_category = "3-license-unclear"
        license_txt = "條款待確認（本輪自動發現）"
        commercial = "待確認"
        if any(x in link for x in ("quarkyifu", "leafletgames", "residentrabbit", "spicylyon", "kuminer", "vnparadise", "zaphassets", "re-caff", "pandita", "meirocircle", "lokianimations", "lokiarts")):
            license_category = "1-free-commercial"
            license_txt = "作者頁面通常標示可商用／CC0／免權利金（請覆核）"
            commercial = "允許（請覆核）"
            dest = ROOT / "assets/1-free-commercial/adult-18plus/vn-sprite" / folder

        dest.mkdir(parents=True, exist_ok=True)
        print("TRY", link)
        urls = download_itch_free(link, dest)
        if not urls or not has_files(dest):
            failed += 1
            ensure_candidate(
                ledger,
                {
                    "id": cid,
                    "url": link,
                    "title": slug,
                    "site_id": "itch-io",
                    "query_ids": [qid],
                    "found_at": today(),
                    "downloadable": False,
                    "license_hint": "",
                    "verdict": "rejected-broken",
                    "pack_id": None,
                    "verified_at": today(),
                    "verify": {
                        "http_ok": True,
                        "downloadable": False,
                        "last_verify_at": today(),
                        "error": "download failed",
                    },
                },
            )
            log("itch_fail", {"url": link})
            print("FAIL", link)
            continue

        pack_id = folder
        registry["packs"].append(
            {
                "id": pack_id,
                "folder": folder,
                "name": slug.replace("-", " ").title(),
                "asset_type": "adult-18plus",
                "style": "vn-sprite",
                "license_category": license_category,
                "license": license_txt,
                "author": link.split("//")[1].split(".")[0],
                "source_url": link,
                "commercial": commercial,
                "attribution": "依來源頁",
                "note": f"auto-discovered via {qid}",
                "status": "downloaded",
            }
        )
        known.add(link)
        ingested += 1
        ensure_candidate(
            ledger,
            {
                "id": cid,
                "url": link,
                "title": slug,
                "site_id": "itch-io",
                "query_ids": [qid],
                "found_at": today(),
                "downloadable": True,
                "license_hint": license_txt,
                "verdict": "ingested",
                "pack_id": pack_id,
                "verified_at": today(),
                "verify": {
                    "http_ok": True,
                    "downloadable": True,
                    "last_verify_at": today(),
                },
            },
        )
        log("itch_ok", {"url": link, "pack_id": pack_id})
        print("OK", link)

    dlsite_new = continue_dlsite_makers(registry)
    REG.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from discovery_ledger import sync_ingested_from_registry

    sync_ingested_from_registry(ledger)
    save_ledger(ledger)
    write_markdown(ledger)
    summary = {
        "itch_ingested": ingested,
        "itch_failed": failed,
        "dlsite_new": len(dlsite_new),
        "ledger_queries": len(ledger.get("queries", [])),
        "ledger_candidates": len(ledger.get("candidates", [])),
    }
    print("summary", summary)
    log("summary", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
