# 找素材專案

從各種來源搜尋、下載並整理遊戲／專案所需素材的中央素材庫。

## 目錄結構（雙軸分類）

素材依 **授權狀態** 與 **素材類型** 兩個維度組織：

```
assets/
├── 1-free-commercial/          # 完全免費授權商用
│   ├── playing-cards/          # 撲克牌
│   ├── mahjong/                # 麻將
│   ├── ui/                     # UI
│   ├── mixed/                  # 綜合性（牌+籌碼+介面等）
│   ├── sound/                  # 音效
│   └── character/              # 角色
├── 2-paid-commercial/          # 商用需購買授權
├── 3-license-unclear/          # 不確定相關規範
└── local-references/           # 本機其他專案參照
```

每個套件資料夾內必有 **`SOURCE_LICENSE.md`**，記錄來源網址、授權條款與商用／署名要求。

## 授權分類

| 目錄 | 說明 |
|------|------|
| `1-free-commercial` | CC0、MIT、明確允許免費商用 |
| `2-paid-commercial` | 需付費購買後方可商用（僅清單或已購買檔案） |
| `3-license-unclear` | 授權不明確，使用前需確認 |

## 素材類型

| 目錄 | 說明 |
|------|------|
| `playing-cards` | 撲克牌牌面、牌背 |
| `mahjong` | 麻將牌、麻將 UI |
| `ui` | 介面元件、按鈕、面板 |
| `mixed` | 綜合性遊戲包（如牌+籌碼+牌桌） |
| `sound` | 音效、BGM |
| `character` | 角色立繪、sprite |

## 清單與工具

| 項目 | 路徑 |
|------|------|
| 撲克牌總覽 | [catalog/playing-cards.md](catalog/playing-cards.md) |
| 套件登錄表（機器可讀） | [tools/pack_registry.json](tools/pack_registry.json) |
| 目錄重整工具 | `uv run python tools/reorganize_assets.py` |

## 新增素材流程

1. 在 `tools/pack_registry.json` 登記套件（含 `asset_type`、`license_category`）
2. 將檔案放入對應目錄
3. 執行 `uv run python tools/reorganize_assets.py` 產生 `SOURCE_LICENSE.md` 並更新 catalog
