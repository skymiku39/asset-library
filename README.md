# 找素材專案

從各種來源搜尋、下載並整理遊戲／專案所需素材的中央素材庫。

## 授權分類（素材庫核心結構）

所有素材依授權狀態分為三類：

| 目錄 | 分類 | 說明 |
|------|------|------|
| `assets/1-free-commercial/` | **完全免費授權商用** | CC0、MIT、明確允許免費商用的授權 |
| `assets/2-paid-commercial/` | **商用需購買授權** | 需付費購買後方可商用；本庫僅收錄清單與連結 |
| `assets/3-license-unclear/` | **不確定相關規範** | 授權條款不明確、需進一步確認或建議付費支持 |
| `assets/local-references/` | 本機參照 | 指向其他專案（如 Kenney）已下載的素材路徑 |

## 目錄結構

```
找素材專案/
├── catalog/                    # 素材清單（Markdown + JSON）
│   ├── playing-cards.md        # 撲克牌總覽
│   ├── 01-free-commercial.md
│   ├── 02-paid-commercial.md
│   └── 03-license-unclear.md
└── assets/
    ├── 1-free-commercial/
    ├── 2-paid-commercial/
    ├── 3-license-unclear/
    └── local-references/
```

## 已收錄分類

| 素材類型 | 清單 |
|----------|------|
| 撲克牌牌面 | [catalog/playing-cards.md](catalog/playing-cards.md) |
