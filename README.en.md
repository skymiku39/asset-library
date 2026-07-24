# Asset Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/skymiku39/asset-library/actions/workflows/ci.yml/badge.svg)](https://github.com/skymiku39/asset-library/actions/workflows/ci.yml)

[繁體中文](README.md)

Central **index and tooling** for discovering, downloading, and organizing game assets.

> **Important**
> - The MIT license covers **tools and indexes only**. It does **not** re-license third-party asset binaries. See [NOTICE.md](NOTICE.md) and each pack’s `SOURCE_LICENSE.md`.
> - Asset binaries are **not** stored in Git by default. Download them with the tools or from the source URLs.
> - Includes an **18+ / adult** catalog (`adult-18plus`). Do not browse that category if you are under 18.

## Quick start

```bash
git clone https://github.com/skymiku39/asset-library.git
cd asset-library
uv sync
uv run python -m unittest discover -s tests -v
uv run python tools/audit_catalog.py
# Public clone / CI (no asset binaries):
# uv run python tools/audit_catalog.py --index-only
```

Optional: copy `config/google_drive.example.json` → `config/google_drive.json` to sync `assets/` via Google Drive (see the Chinese README for full steps).

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md).

## Layout (two axes)

Assets are organized by **license status** × **asset type**:

```
assets/
├── 1-free-commercial/      # Free for commercial use
├── 2-paid-commercial/      # Paid commercial license
├── 3-license-unclear/      # Needs manual license review
├── 4-free-noncommercial/   # Free but non-commercial / trials
└── local-references/       # Local mirrors (paths not committed)
```

Types include `playing-cards`, `mahjong`, `ui`, `mixed`, `sound`, `character`, `vfx`, and `adult-18plus`. Many types also use a **style** subfolder (e.g. `pixel`, `vn-sprite`).

## Key files

| Item | Path |
|------|------|
| Pack registry | [`tools/pack_registry.json`](tools/pack_registry.json) |
| Catalogs | [`catalog/`](catalog/) |
| 18+ discovery ledger | [`catalog/discovery-ledger.md`](catalog/discovery-ledger.md) |
| Reorganize + write `SOURCE_LICENSE.md` | `uv run python tools/reorganize_assets.py` |
| Consistency audit | `uv run python tools/audit_catalog.py` |
| Continue 18+ discovery | `uv run python tools/run_adult_discovery.py` |
| Verify discovery ledger | `uv run python tools/verify_discovery_ledger.py` |
| itch.io free download | `uv run python tools/itch_download.py <url> <dest_dir>` |
| DLsite trial download | `uv run python tools/dlsite_download.py <product_url> <dest_dir>` |

## Adding a pack

1. Register the pack in `tools/pack_registry.json`
2. Download files into the matching `assets/...` folder locally
3. Run `uv run python tools/reorganize_assets.py`
4. Run `uv run python tools/audit_catalog.py`

## License

- Repository code & docs: [MIT](LICENSE)
- Third-party assets: per-pack terms only — see [NOTICE.md](NOTICE.md)
