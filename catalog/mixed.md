# 綜合性素材總覽

> 最後更新：2026-07-07

## 目錄結構（先分子類）

綜合性素材在「素材類型」之下多一層 **子類母分類**，依內容組合類型分組：

```
assets/{授權分類}/mixed/{子類}/{套件名}/SOURCE_LICENSE.md
```

範例：`assets/1-free-commercial/mixed/poker-kit/sbs-2d-poker-pack/`

## 子類母分類

| 子類 slug | 說明 | 適用場景 |
|-----------|------|----------|
| `poker-kit` | 撲克遊戲包 | 牌面 + 籌碼 + 牌桌 + UI |
| `mahjong-kit` | 麻將遊戲包 | 麻將牌 + UI + 遊戲範本 |
| `boardgame` | 棋盤／通用遊戲包 | 骰子、棋盤、多類牌具 |

| 分類 | 清單 | 收錄 |
|------|------|------|
| 完全免費授權商用 | [01-free-commercial.md](01-free-commercial.md) | 1 套 |
| 商用需購買授權 | [02-paid-commercial.md](02-paid-commercial.md) | 清單 5 套 |
| 本機參照 | [01-free-commercial.md#本機參照](01-free-commercial.md) | 1 套 |

機器可讀：[mixed.json](mixed.json)

## 與單一類型的關係

若套件**僅含單一素材類型**（如純牌面、純 UI），應歸於對應的 `playing-cards`、`mahjong`、`ui` 等目錄。  
`mixed/` 保留給**跨類型組合包**或**完整遊戲範本**。
