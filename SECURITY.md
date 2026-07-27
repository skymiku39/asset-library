# 安全性政策

## 適用範圍

本政策適用於 **asset-library 倉庫內的工具與索引**（Python 腳本、CI、設定檔、catalog／registry）。

**不適用**於第三方素材作者網站（itch.io、DLsite 等）或各套件 `SOURCE_LICENSE.md` 所列之原始來源；素材授權與內容爭議請直接向原作者或平台反映。

## 回報方式

若發現本倉庫工具可能導致：

- 任意檔案讀寫、路徑穿越
- 憑證或本機路徑意外外洩
- 依賴供應鏈或 CI 設定問題

請至 [GitHub Security Advisories](https://github.com/skymiku39/asset-library/security/advisories/new) 私下回報，或開 Issue 並標記「security」（勿在 Issue 內貼出可利用的敏感細節）。

## 回應時間

我們會在合理時間內確認收到，並於修復後於 release／commit 說明中致謝（若你希望署名）。

## 安全使用建議

- 勿將 `config/google_drive.json`、`config/kenney_local.json` 提交至公開倉庫
- 下載腳本會存取外部 URL；僅對信任來源執行
- 公開 clone 預設只有授權索引；完整稽核請在本機有素材後執行 `uv run python tools/audit_catalog.py`
