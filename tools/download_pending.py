"""Batch-download packs marked pending-manual-download."""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS.parent
REGISTRY = TOOLS / "pack_registry.json"
ASSETS_DIR = PROJECT_ROOT / "assets"

SPEC = importlib.util.spec_from_file_location("reorganize_assets", TOOLS / "reorganize_assets.py")
assert SPEC and SPEC.loader
reorg = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reorg)

SPEC2 = importlib.util.spec_from_file_location("itch_download", TOOLS / "itch_download.py")
assert SPEC2 and SPEC2.loader
itch = importlib.util.module_from_spec(SPEC2)
SPEC2.loader.exec_module(itch)

SPEC3 = importlib.util.spec_from_file_location("oga_download", TOOLS / "oga_download.py")
assert SPEC3 and SPEC3.loader
oga = importlib.util.module_from_spec(SPEC3)
SPEC3.loader.exec_module(oga)

SPEC4 = importlib.util.spec_from_file_location("kenney_download", TOOLS / "kenney_download.py")
assert SPEC4 and SPEC4.loader
kenney_dl = importlib.util.module_from_spec(SPEC4)
SPEC4.loader.exec_module(kenney_dl)

# Optional local Kenney mirror to avoid re-downloading CC0 packs.
KENNEY_LOCAL: dict[str, str] = {
    "kenney-ui-pack": "d:/skymiku/kenney/assets/ui/ui-pack",
    "kenney-ui-pack-scifi": "d:/skymiku/kenney/assets/ui/ui-pack---sci-fi",
    "kenney-fantasy-ui-borders": "d:/skymiku/kenney/assets/ui/fantasy-ui-borders",
    "kenney-shape-characters": "d:/skymiku/kenney/assets/2d/shape-characters",
}

KENNEY_NL_SLUG: dict[str, str] = {
    "kenney-pixel-ui-pack": "pixel-ui-pack",
    "kenney-toon-characters": "toon-characters",
    "kenney-modular-characters": "modular-characters",
    "kenney-ui-rpg-expansion": "ui-pack-rpg-expansion",
    "kenney-ui-pack": "ui-pack",
    "kenney-ui-pack-scifi": "ui-pack-sci-fi",
    "kenney-fantasy-ui-borders": "fantasy-ui-borders",
    "kenney-shape-characters": "shape-characters",
    "kenney-particle-pack": "particle-pack",
    "kenney-smoke-particles": "smoke-particles",
    "kenney-splat-pack": "splat-pack",
}

# itch.io mirrors for Kenney assets not present locally.
KENNEY_ITCH: dict[str, str] = {
    "kenney-ui-pack": "https://kenney-assets.itch.io/ui-pack",
    "kenney-pixel-ui-pack": "https://kenney-assets.itch.io/pixel-ui-pack",
    "kenney-fantasy-ui-borders": "https://kenney-assets.itch.io/fantasy-ui-borders",
    "kenney-shape-characters": "https://kenney-assets.itch.io/shape-characters",
    "kenney-toon-characters": "https://kenney-assets.itch.io/toon-characters-1",
    "kenney-modular-characters": "https://kenney-assets.itch.io/modular-characters",
    "kenney-ui-rpg-expansion": "https://kenney-assets.itch.io/ui-pack-rpg-expansion",
    "kenney-ui-pack-scifi": "https://kenney-assets.itch.io/ui-pack-sci-fi",
    "kenney-splat-pack": "https://kenney-assets.itch.io/splat-pack",
}

GITHUB_ZIPS: dict[str, str] = {
    "lpc-universal-spritesheet": (
        "https://github.com/liberatedpixelcup/"
        "Universal-LPC-Spritesheet-Character-Generator/archive/refs/heads/master.zip"
    ),
}

QUATERNIUS_PAGES: dict[str, str] = {
    "quaternius-ultimate-animated-character": (
        "https://opengameart.org/content/animated-characters-pack"
    ),
    "quaternius-universal-base-characters": (
        "https://quaternius.itch.io/universal-base-characters"
    ),
}


def has_assets(folder: Path) -> bool:
    if not folder.exists():
        return False
    for item in folder.rglob("*"):
        if not item.is_file():
            continue
        if item.name in {"SOURCE_LICENSE.md", "README.md", "pack.zip"}:
            continue
        if item.suffix.lower() in {".url", ".md"}:
            continue
        return True
    return False


def copy_local_tree(src: Path, dest: Path) -> bool:
    if not src.exists():
        return False
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dest / item.name
        if item.is_dir():
            if target.exists():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)
    return has_assets(dest)


def download_http_zip(url: str, dest_dir: Path) -> bool:
    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (asset-library/1.0)"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = resp.read()
    except urllib.error.URLError:
        return False
    if not data.startswith(b"PK"):
        return False
    zip_path = dest_dir / "pack.zip"
    zip_path.write_bytes(data)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest_dir)
    zip_path.unlink(missing_ok=True)
    return has_assets(dest_dir)


def try_download(pack: dict) -> tuple[bool, str]:
    dest = reorg.target_dir(pack)
    pid = pack["id"]
    url = pack.get("source_url", "")

    if has_assets(dest):
        return True, "already present"

    if pid in KENNEY_LOCAL:
        local = Path(KENNEY_LOCAL[pid])
        if copy_local_tree(local, dest):
            return True, f"copied from {local}"

    slug = KENNEY_NL_SLUG.get(pid)
    if slug and kenney_dl.download_asset(slug, dest) and has_assets(dest):
        return True, f"kenney.nl {slug}"

    itch_url = KENNEY_ITCH.get(pid)
    if itch_url and itch.download_itch_free(itch_url, dest):
        if has_assets(dest):
            return True, f"itch {itch_url}"

    if "itch.io" in url:
        saved = itch.download_itch_free(url, dest)
        if saved and has_assets(dest):
            return True, f"itch {url}"

    if "opengameart.org" in url and oga.download_page(url, dest):
        if has_assets(dest):
            return True, f"oga {url}"

    if pid in GITHUB_ZIPS and download_http_zip(GITHUB_ZIPS[pid], dest):
        return True, "github zip"

    if pid in QUATERNIUS_PAGES:
        alt = QUATERNIUS_PAGES[pid]
        if "itch.io" in alt:
            saved = itch.download_itch_free(alt, dest)
            if saved and has_assets(dest):
                return True, f"itch {alt}"
        if "opengameart.org" in alt and oga.download_page(alt, dest):
            if has_assets(dest):
                return True, f"oga {alt}"

    return False, "no source succeeded"


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    packs = data["packs"]
    pending = [p for p in packs if p["status"] == "pending-manual-download"]

    ok: list[str] = []
    fail: list[str] = []

    for pack in pending:
        success, detail = try_download(pack)
        if success:
            pack["status"] = "downloaded"
            ok.append(f"{pack['id']}: {detail}")
        else:
            fail.append(f"{pack['id']}: {detail}")

    REGISTRY.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"pending tried: {len(pending)}")
    print(f"downloaded: {len(ok)}")
    for line in ok:
        print(f"  OK  {line}")
    print(f"failed: {len(fail)}")
    for line in fail:
        print(f"  FAIL {line}")

    if ok:
        reorg.main()

    return 0 if not fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
