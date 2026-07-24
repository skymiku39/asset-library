# 貢獻指南

感謝你願意一起維護這份素材庫索引與工具。

English summary: run `uv sync`, `uv run python -m unittest discover -s tests -v`, and `uv run python tools/audit_catalog.py` before opening a PR. See [README.en.md](README.en.md).

## 開發環境

```powershell
uv sync
uv run python -m unittest discover -s tests -v
uv run python tools/audit_catalog.py
```

## 新增／更新套件

1. 在 `tools/pack_registry.json` 新增或修改套件欄位（含 `asset_type`、`license_category`、`source_url`；需要時加 `style`）
2. 下載素材到對應 `assets/...` 路徑（本機；二進位預設不進版控）
3. 執行 `uv run python tools/reorganize_assets.py` 產生／更新 `SOURCE_LICENSE.md` 與 catalog
4. 執行 `uv run python tools/audit_catalog.py`，確認無 issues
5. 送出 PR；commit 訊息建議：`type: emoji [AI] 繁中主旨`（非 AI 貢獻可省略 `[AI]`）

## 授權注意

- 工具與文件：MIT（見 `LICENSE`）
- 第三方素材：見各套件 `SOURCE_LICENSE.md` 與 `NOTICE.md`
- 請勿提交 API token、本機絕對路徑設定（`config/google_drive.json`、`config/kenney_local.json`）

## 18+ 內容

`adult-18plus` 目錄與 catalog 含成人向素材索引。貢獻時請標示清楚，並遵守平台與當地法規。
