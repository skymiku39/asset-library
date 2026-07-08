"""Reorganize asset folders by type and write SOURCE_LICENSE.md for each pack."""
from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = PROJECT_ROOT / "assets"
REGISTRY = Path(__file__).with_name("pack_registry.json")
TODAY = date.today().isoformat()


def render_source_license(
    pack: dict,
    asset_type_label: str,
    license_category_label: str,
    style_label: str | None = None,
) -> str:
    lines = [
        "# 來源與授權聲明",
        "",
        "> 本檔案由素材庫自動維護，供授權稽核使用。",
        "",
        "| 項目 | 內容 |",
        "|------|------|",
        f"| 套件名稱 | {pack['name']} |",
        f"| 素材類型 | {asset_type_label} |",
    ]
    if style_label:
        lines.append(f"| 風格 | {style_label} |")
    lines += [
        f"| 授權分類 | {license_category_label} |",
        f"| 授權條款 | {pack['license']} |",
        f"| 作者 | {pack['author']} |",
        f"| 來源網址 | {pack['source_url']} |",
        f"| 收錄日期 | {TODAY} |",
        f"| 商用 | {pack['commercial']} |",
        f"| 署名 | {pack['attribution']} |",
    ]
    if pack.get("local_path"):
        lines.append(f"| 本機參照路徑 | `{pack['local_path']}` |")
    if pack.get("note"):
        lines.append(f"| 備註 | {pack['note']} |")
    summary = ["", "## 授權摘要", "", f"- 素材類型：**{asset_type_label}**"]
    if style_label:
        summary.append(f"- 風格：**{style_label}**")
    summary += [
        f"- 授權分類：**{license_category_label}**",
        f"- 條款：**{pack['license']}**",
        "",
    ]
    lines.extend(
        [
            *summary,
            "## 原始授權連結",
            "",
            f"- {pack['source_url']}",
            "",
        ]
    )
    return "\n".join(lines)


def ensure_type_readme(type_dir: Path, asset_type: str, label: str) -> None:
    type_dir.mkdir(parents=True, exist_ok=True)
    readme = type_dir / "README.md"
    if readme.exists():
        return
    readme.write_text(
        f"# {label}\n\n素材類型：`{asset_type}`\n\n本目錄收錄**{label}**相關素材套件。\n",
        encoding="utf-8",
    )


def ensure_style_readme(
    style_dir: Path, asset_type: str, type_label: str, style: str, label: str
) -> None:
    style_dir.mkdir(parents=True, exist_ok=True)
    readme = style_dir / "README.md"
    if readme.exists():
        return
    readme.write_text(
        f"# {label}\n\n風格：`{style}`（隸屬素材類型 `{asset_type}`／{type_label}）\n\n"
        f"本目錄收錄**{label}**風格的{type_label}素材套件。\n",
        encoding="utf-8",
    )


def collect_styles(data: dict) -> dict[str, str]:
    """Merge every ``*_styles`` map in the registry into one slug→label lookup."""
    styles: dict[str, str] = {}
    for key, value in data.items():
        if key.endswith("_styles") and isinstance(value, dict):
            styles.update(value)
    return styles


def target_dir(pack: dict) -> Path:
    base = ASSETS_DIR / pack["license_category"] / pack["asset_type"]
    if pack.get("style"):
        base = base / pack["style"]
    return base / pack["folder"]


def migrate_downloaded_packs(packs: list[dict]) -> list[str]:
    moved: list[str] = []
    for pack in packs:
        if pack["status"] not in {"downloaded", "pending-manual-download"}:
            continue
        if pack["license_category"] == "local-references":
            continue

        old_candidates = [
            ASSETS_DIR / pack["license_category"] / pack["folder"],
            ASSETS_DIR / pack["license_category"] / pack["asset_type"] / pack["folder"],
        ]
        if pack.get("style"):
            old_candidates.insert(
                0,
                ASSETS_DIR
                / pack["license_category"]
                / pack["asset_type"]
                / pack["style"]
                / pack["folder"],
            )
        dest = target_dir(pack)
        dest.parent.mkdir(parents=True, exist_ok=True)

        for old in old_candidates:
            if old.exists() and old.resolve() != dest.resolve():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.move(str(old), str(dest))
                moved.append(f"{old} -> {dest}")
                break
        else:
            dest.mkdir(parents=True, exist_ok=True)

    return moved


def migrate_local_reference_packs(packs: list[dict]) -> list[str]:
    moved: list[str] = []
    for pack in packs:
        if pack["status"] != "local-reference":
            continue
        dest = ASSETS_DIR / "local-references" / pack["asset_type"]
        if pack.get("style"):
            dest = dest / pack["style"]
        dest = dest / pack["folder"]
        old = ASSETS_DIR / "local-references" / pack["asset_type"] / pack["folder"]
        if old.exists() and old.resolve() != dest.resolve():
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                shutil.rmtree(dest)
            shutil.move(str(old), str(dest))
            moved.append(f"{old} -> {dest}")
            stale_url = old.parent / f"{pack['folder']}.url"
            if stale_url.exists():
                stale_url.unlink()
    return moved


def write_source_licenses(
    packs: list[dict],
    asset_types: dict[str, str],
    license_categories: dict[str, str],
    styles: dict[str, str],
) -> int:
    count = 0
    for pack in packs:
        if pack["status"] == "catalog-only":
            dest = target_dir(pack)
            dest.mkdir(parents=True, exist_ok=True)
        elif pack["status"] == "local-reference":
            ref_dir = ASSETS_DIR / "local-references" / pack["asset_type"]
            if pack.get("style"):
                ref_dir = ref_dir / pack["style"]
            ref_dir.mkdir(parents=True, exist_ok=True)
            url_file = ref_dir / f"{pack['folder']}.url"
            local = pack.get("local_path", "")
            if local and not url_file.exists():
                url_file.write_text(
                    f"[InternetShortcut]\nURL=file:///{local.replace(chr(92), '/')}/\n",
                    encoding="utf-8",
                )
            dest = ref_dir / pack["folder"]
            dest.mkdir(parents=True, exist_ok=True)
            type_label = asset_types[pack["asset_type"]]
            style = pack.get("style")
            if style:
                ensure_style_readme(
                    ref_dir,
                    pack["asset_type"],
                    type_label,
                    style,
                    styles.get(style, style),
                )
        else:
            dest = target_dir(pack)
            if not dest.exists():
                dest.mkdir(parents=True, exist_ok=True)

        type_label = asset_types[pack["asset_type"]]
        cat_label = license_categories[pack["license_category"]]
        style = pack.get("style")
        if style:
            style_dir = dest.parent
            type_dir = style_dir.parent
            ensure_type_readme(type_dir, pack["asset_type"], type_label)
            ensure_style_readme(
                style_dir,
                pack["asset_type"],
                type_label,
                style,
                styles.get(style, style),
            )
        else:
            ensure_type_readme(dest.parent, pack["asset_type"], type_label)

        style_label = styles.get(style, style) if style else None
        license_file = dest / "SOURCE_LICENSE.md"
        license_file.write_text(
            render_source_license(pack, type_label, cat_label, style_label),
            encoding="utf-8",
        )
        count += 1
    return count


def cleanup_empty_dirs() -> None:
    for license_dir in ASSETS_DIR.iterdir():
        if not license_dir.is_dir() or license_dir.name == "local-references":
            continue
        for child in list(license_dir.iterdir()):
            if child.is_dir() and child.name in {
                "playing-cards",
                "mahjong",
                "ui",
                "mixed",
                "sound",
                "character",
                "vfx",
                "adult-18plus",
            }:
                continue
            if child.is_dir() and not any(child.iterdir()):
                child.rmdir()
            elif child.is_dir() and child.name not in {
                "playing-cards",
                "mahjong",
                "ui",
                "mixed",
                "sound",
                "character",
                "vfx",
                "adult-18plus",
            }:
                # legacy flat pack folder with content -> should have been moved
                if (child / "SOURCE_LICENSE.md").exists():
                    continue
                if not any(child.rglob("*")):
                    child.rmdir()


def update_catalog_json(
    packs: list[dict],
    asset_types: dict[str, str],
    styles: dict[str, str],
) -> None:
    license_categories = json.loads(REGISTRY.read_text(encoding="utf-8"))[
        "license_categories"
    ]
    by_type: dict[str, list[dict]] = {}
    for pack in packs:
        by_type.setdefault(pack["asset_type"], []).append(pack)

    catalog_dir = PROJECT_ROOT / "catalog"
    catalog_dir.mkdir(parents=True, exist_ok=True)
    updated_types: list[str] = []

    for asset_type, type_packs in sorted(by_type.items()):
        catalog = {
            "category": asset_type,
            "updated": TODAY,
            "asset_types": asset_types,
            "license_categories": license_categories,
            "packs": [],
        }
        used_styles = {
            pack["style"]: styles.get(pack["style"], pack["style"])
            for pack in type_packs
            if pack.get("style")
        }
        if used_styles:
            catalog["styles"] = used_styles
        for pack in type_packs:
            entry = {
                "id": pack["id"],
                "name": pack["name"],
                "asset_type": pack["asset_type"],
                "license_category": pack["license_category"],
                "license": pack["license"],
                "source_url": pack["source_url"],
                "status": pack["status"],
            }
            if pack.get("style"):
                entry["style"] = pack["style"]
            style_seg = f"{pack['style']}/" if pack.get("style") else ""
            if pack["status"] == "local-reference":
                entry["local_path"] = pack.get("local_path")
                entry["local_path_short"] = (
                    f"assets/local-references/{pack['asset_type']}/{style_seg}{pack['folder']}"
                )
            elif pack["status"] != "catalog-only":
                entry["local_path"] = (
                    f"assets/{pack['license_category']}/{pack['asset_type']}/{style_seg}{pack['folder']}"
                )
            catalog["packs"].append(entry)

        out = catalog_dir / f"{asset_type}.json"
        out.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
        updated_types.append(asset_type)

    print(f"Updated catalogs: {', '.join(updated_types)}")


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    packs: list[dict] = data["packs"]
    asset_types: dict[str, str] = data["asset_types"]
    license_categories: dict[str, str] = data["license_categories"]
    styles: dict[str, str] = collect_styles(data)

    # Ensure top-level type placeholders
    for lic in license_categories:
        lic_dir = ASSETS_DIR / lic
        lic_dir.mkdir(parents=True, exist_ok=True)
        for asset_type, label in asset_types.items():
            type_dir = lic_dir / asset_type
            type_dir.mkdir(parents=True, exist_ok=True)
            ensure_type_readme(type_dir, asset_type, label)

    ref_root = ASSETS_DIR / "local-references"
    ref_root.mkdir(parents=True, exist_ok=True)
    for asset_type, label in asset_types.items():
        ensure_type_readme(ref_root / asset_type, asset_type, label)

    moved = migrate_downloaded_packs(packs)
    moved.extend(migrate_local_reference_packs(packs))
    count = write_source_licenses(packs, asset_types, license_categories, styles)
    cleanup_empty_dirs()
    update_catalog_json(packs, asset_types, styles)

    print(f"Moved {len(moved)} pack folders")
    for line in moved:
        print(f"  {line}")
    print(f"Wrote {count} SOURCE_LICENSE.md files")


if __name__ == "__main__":
    main()
