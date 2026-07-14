from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request

LOG_PATH = "debug-4e8286.log"


def log(hypothesis_id: str, location: str, message: str, data: dict) -> None:
    # #region agent log
    payload = {
        "sessionId": "4e8286",
        "runId": "dlsite-discovery-2",
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    # #endregion


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def discover() -> None:
    keywords = [
        "立ち絵素材 体験版",
        "R18 立ち絵 体験版",
        "画像素材 体験版",
        "素材集 体験版 RPG",
        "ゲーム素材 体験版",
    ]
    product_ids: set[str] = set()
    id_re = re.compile(r"product_id/(RJ\d+)\.html")
    trial_re = re.compile(r"//trial\.dlsite\.com/[^\"']+_trial\.zip", re.IGNORECASE)

    for kw in keywords:
        encoded = urllib.parse.quote(kw)
        url = f"https://www.dlsite.com/maniax/fsr/=/keyword/{encoded}"
        try:
            html = fetch(url)
            ids = set(id_re.findall(html))
            product_ids.update(ids)
            log("H1", "discover_dlsite_trials.py:50", "keyword scanned", {"keyword": kw, "ids_found": len(ids)})
        except Exception as e:
            log("H1", "discover_dlsite_trials.py:52", "keyword scan failed", {"keyword": kw, "error": str(e)})

    maker_ids = [
        "RG29726",  # 森の奥の隠れ里
        "RG01039776",  # にゃんちぇると
        "RG61015",  # ふぁっちゅ
        "RG65563",  # Pincree
        "RG01003985",  # 素材WIZPACK
        "RG01062657",  # らむにくの素材屋さん
        "RG63073",  # れいが荘素材専門店
        "RG44045",  # キノコル
        "RG53789",  # バズ猫工務店
        "RG01045611",  # 乃図制作所
        "RG27887",  # 菊にぃ
        "RG01075080",  # WaifuKoubou
        "RG01066181",  # Mashiro Lab.
        "RG65654",  # スペースドーナツ
        "RG01051734",  # 月影
    ]
    for maker_id in maker_ids:
        murl = f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{maker_id}.html"
        try:
            html = fetch(murl)
            ids = set(id_re.findall(html))
            product_ids.update(ids)
            log(
                "H4",
                "discover_dlsite_trials.py:maker",
                "maker scanned",
                {"maker_id": maker_id, "ids_found": len(ids)},
            )
        except Exception as e:
            log(
                "H4",
                "discover_dlsite_trials.py:maker",
                "maker scan failed",
                {"maker_id": maker_id, "error": str(e)},
            )

    checked = 0
    trial_hits: list[dict] = []
    for pid in sorted(product_ids):
        purl = f"https://www.dlsite.com/maniax/work/=/product_id/{pid}.html"
        checked += 1
        try:
            html = fetch(purl)
            m = trial_re.search(html)
            if m:
                trial_hits.append({"product_id": pid, "product_url": purl, "trial_url": "https:" + m.group(0)})
                log("H2", "discover_dlsite_trials.py:66", "trial found", {"product_id": pid})
            else:
                log("H2", "discover_dlsite_trials.py:68", "no trial", {"product_id": pid})
        except Exception as e:
            log("H2", "discover_dlsite_trials.py:70", "product fetch failed", {"product_id": pid, "error": str(e)})

    print(json.dumps({"checked": checked, "trial_hits": trial_hits}, ensure_ascii=False, indent=2))
    log("H3", "discover_dlsite_trials.py:74", "discovery finished", {"checked": checked, "trial_hits": len(trial_hits)})


if __name__ == "__main__":
    discover()
