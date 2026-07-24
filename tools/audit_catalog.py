"""Audit pack_registry.json against on-disk assets and style rules."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "assets"
REGISTRY = Path(__file__).with_name("pack_registry.json")
CATALOG_DIR = PROJECT_ROOT / "catalog"


def collect_styles(data: dict) -> dict[str, str]:
    styles: dict[str, str] = {}
    for key, value in data.items():
        if key.endswith("_styles") and isinstance(value, dict):
            styles.update(value)
    return styles


def pack_dest(pack: dict) -> Path:
    base = ASSETS_DIR / pack["license_category"] / pack["asset_type"]
    if pack.get("style"):
        base = base / pack["style"]
    return base / pack["folder"]


def disk_license_path(pack: dict) -> Path | None:
    if pack["status"] == "local-reference":
        base = ASSETS_DIR / "local-references" / pack["asset_type"]
        if pack.get("style"):
            base = base / pack["style"]
        path = base / pack["folder"] / "SOURCE_LICENSE.md"
        return path if path.exists() else None
    if pack["status"] == "catalog-only":
        path = pack_dest(pack) / "SOURCE_LICENSE.md"
        return path if path.exists() else None
    path = pack_dest(pack) / "SOURCE_LICENSE.md"
    return path if path.exists() else None


def has_asset_files(pack: dict) -> bool:
    folder = pack_dest(pack)
    if pack["status"] == "local-reference":
        folder = ASSETS_DIR / "local-references" / pack["asset_type"]
        if pack.get("style"):
            folder = folder / pack["style"]
        folder = folder / pack["folder"]
    if not folder.exists():
        return False
    for item in folder.rglob("*"):
        if item.is_file() and item.name not in {"SOURCE_LICENSE.md", "README.md"}:
            suffix = item.suffix.lower()
            if suffix not in {".url", ".md"}:
                return True
    return False


def style_map_for_type(data: dict, asset_type: str) -> dict[str, str]:
    key = asset_type.replace("-", "_") + "_styles"
    if key in data:
        return data[key]
    legacy = {
        "ui": "ui_styles",
        "sound": "sound_styles",
        "character": "character_styles",
        "mixed": "mixed_styles",
    }
    return data.get(legacy.get(asset_type, ""), {})


def audit(data: dict, *, require_asset_binaries: bool = True) -> list[str]:
    issues: list[str] = []
    packs: list[dict] = data["packs"]
    pack_ids = [p["id"] for p in packs]
    if len(pack_ids) != len(set(pack_ids)):
        dupes = [k for k, v in Counter(pack_ids).items() if v > 1]
        issues.append(f"duplicate pack ids: {dupes}")

    catalog_ids: set[str] = set()
    for cat_file in CATALOG_DIR.glob("*.json"):
        cat = json.loads(cat_file.read_text(encoding="utf-8"))
        for pack in cat.get("packs", []):
            catalog_ids.add(pack["id"])
    registry_ids = set(pack_ids)
    if registry_ids != catalog_ids:
        issues.append(
            f"registry/catalog id mismatch: "
            f"only_registry={sorted(registry_ids - catalog_ids)[:5]} "
            f"only_catalog={sorted(catalog_ids - registry_ids)[:5]}"
        )

    styled_types = set()
    for key in data:
        if key.endswith("_styles"):
            styled_types.add(key.replace("_styles", "").replace("_", "-"))
            if key == "playing_cards_styles":
                styled_types.add("playing-cards")

    for pack in packs:
        pid = pack["id"]
        at = pack["asset_type"]
        valid_styles = style_map_for_type(data, at)
        if valid_styles:
            style = pack.get("style")
            if not style:
                issues.append(f"{pid}: missing style for {at}")
            elif style not in valid_styles:
                issues.append(f"{pid}: unknown style '{style}' for {at}")

        lic_path = disk_license_path(pack)
        if pack["status"] in {"downloaded", "pending-manual-download", "catalog-only", "local-reference"}:
            if not lic_path:
                issues.append(f"{pid}: missing SOURCE_LICENSE.md ({pack['status']})")

        if require_asset_binaries:
            if pack["status"] == "downloaded" and not has_asset_files(pack):
                issues.append(f"{pid}: status downloaded but no asset files in {pack_dest(pack)}")

            if pack["status"] == "pending-manual-download" and has_asset_files(pack):
                issues.append(
                    f"{pid}: has asset files but status is pending-manual-download "
                    f"(consider updating to downloaded)"
                )

    return issues


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Audit pack registry vs on-disk assets")
    parser.add_argument(
        "--index-only",
        action="store_true",
        help="Skip binary asset checks (for CI / public clone without downloaded files)",
    )
    args = parser.parse_args(argv)

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    packs = data["packs"]
    issues = audit(data, require_asset_binaries=not args.index_only)

    print("=== AUDIT SUMMARY ===")
    print(f"packs: {len(packs)}")
    print(f"issues: {len(issues)}")
    print(f"mode: {'index-only' if args.index_only else 'full'}")
    by_status = Counter(p["status"] for p in packs)
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")

    if issues:
        print("\n=== ISSUES ===")
        for issue in issues:
            print(f"  - {issue}")
        return 1

    print("\nOK: catalog consistent with rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
