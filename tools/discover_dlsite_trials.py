from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request


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
            print(f"keyword ok: {kw} -> {len(ids)}")
        except Exception as e:
            print(f"keyword fail: {kw}: {e}")

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
        "RG01010253",  # 空想番外地
        "RG01012324",  # Snow Material
        "RG66647",  # 立ち絵素材RAIKO
    ]
    for maker_id in maker_ids:
        murl = f"https://www.dlsite.com/maniax/circle/profile/=/maker_id/{maker_id}.html"
        try:
            html = fetch(murl)
            ids = set(id_re.findall(html))
            product_ids.update(ids)
            print(f"maker ok: {maker_id} -> {len(ids)}")
        except Exception as e:
            print(f"maker fail: {maker_id}: {e}")

    checked = 0
    trial_hits: list[dict] = []
    for pid in sorted(product_ids):
        purl = f"https://www.dlsite.com/maniax/work/=/product_id/{pid}.html"
        checked += 1
        try:
            html = fetch(purl)
            m = trial_re.search(html)
            if m:
                trial_hits.append(
                    {
                        "product_id": pid,
                        "product_url": purl,
                        "trial_url": "https:" + m.group(0),
                    }
                )
        except Exception as e:
            print(f"product fail: {pid}: {e}")

    print(json.dumps({"checked": checked, "trial_hits": trial_hits}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    discover()
