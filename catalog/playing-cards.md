# 撲克牌牌面素材總覽

> 最後更新：2026-07-07

## 目錄結構（先分風格）

撲克牌在「素材類型」之下多一層 **風格母分類**，先依風格分類再放套件：

```
assets/{授權分類}/playing-cards/{風格}/{套件名}/SOURCE_LICENSE.md
```

範例：`assets/1-free-commercial/playing-cards/vector/byron-knoll-vector/`

## 風格母分類

| 風格 slug | 說明 | 適用場景 |
|-----------|------|----------|
| `pixel` | 像素風 | 復古、8-bit、小尺寸遊戲 |
| `vector` | 向量／SVG | 可縮放、四色牌、程式生成 |
| `flat` | 扁平／標準牌面 | 通用撲克、橋牌尺寸 PNG |
| `stylized` | 藝術／裝飾風 | 主題牌組、華麗牌背 |
| `3d` | 3D | 立體牌面（多為付費清單） |

| 分類 | 清單 | 收錄 |
|------|------|------|
| 完全免費授權商用 | [01-free-commercial.md](01-free-commercial.md) | 18 套 |
| 商用需購買授權 | [02-paid-commercial.md](02-paid-commercial.md) | 清單 1 套（另 3 套歸 `mixed`） |
| 不確定相關規範 | [03-license-unclear.md](03-license-unclear.md) | 4 套（3 已下載 + 1 待下載） |
| 免費不可商用（含測試版） | [04-free-noncommercial.md](04-free-noncommercial.md) | 1 套 |

機器可讀：[playing-cards.json](playing-cards.json)｜套件登錄：[../tools/pack_registry.json](../tools/pack_registry.json)

## 授權檢查

每個套件資料夾內的 `SOURCE_LICENSE.md` 包含：

- 來源網址
- 授權條款與商用／署名要求
- 素材類型、風格與授權分類

## 綜合性素材

以下套件含多類內容，歸於 `mixed/`：

- `1-free-commercial/mixed/poker-kit/sbs-2d-poker-pack/` — 牌面 + 籌碼
- `local-references/mixed/boardgame/kenney-boardgame-pack/` — 牌 + 骰子 + 棋盤遊戲
