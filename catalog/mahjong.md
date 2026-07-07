# 麻將素材總覽

> 最後更新：2026-07-07

## 目錄結構（先分風格）

麻將在「素材類型」之下多一層 **風格母分類**，先依風格分類再放套件：

```
assets/{授權分類}/mahjong/{風格}/{套件名}/SOURCE_LICENSE.md
```

範例：`assets/1-free-commercial/mahjong/riichi/fluffystuff-riichi-mahjong-tiles/`

## 風格母分類

| 風格 slug | 說明 | 適用場景 |
|-----------|------|----------|
| `pixel` | 像素風 | 小尺寸、復古、接龍類 |
| `vector` | 向量／傳統牌面 | 多地區 SVG、可縮放 |
| `riichi` | 立直麻將 | 日本立直規則專用牌面 |
| `3d` | 3D | 立體牌模（多為付費清單） |

| 分類 | 清單 | 收錄 |
|------|------|------|
| 完全免費授權商用 | [01-free-commercial.md#麻將mahjong](01-free-commercial.md) | **12 套**（8 已下載 + 4 待下載） |
| 商用需購買授權 | [02-paid-commercial.md#麻將mahjong](02-paid-commercial.md) | 清單 **12 套** |
| 不確定相關規範 | [03-license-unclear.md#麻將mahjong](03-license-unclear.md) | **3 套**（2 已下載 + 1 參考清單） |

機器可讀：[mahjong.json](mahjong.json)

## 搜尋覆蓋範圍

已盤點來源：**GitHub**、**itch.io**（含 `tag-mahjong` 全 18 筆）、**OpenGameArt**、**Unity Asset Store**、**GameArt2D**。  
Kenney 無麻將專用素材包。

## 推薦選用

| 需求 | 推薦 |
|------|------|
| 日本立直麻將（最常用） | `mahjong/riichi/fluffystuff-riichi-mahjong-tiles/` |
| 多地區麻將（港麻等） | `mahjong/vector/samoheen-mahjong-tiles/` |
| 雀魂風格 PNG/SVG | `mahjong/riichi/lietxia-riichi-vector/` |
| 像素風小尺寸 | `mahjong/pixel/natonato-simple-tiny/` |
| 64×64 像素精靈圖 | `mahjong/pixel/blueeyedrat-pixel-mahjong/` |
| 多地區 SVG（需自行組合底座） | `mahjong/vector/demching-mahjong-free/` |
| 高解析 PSD 原始檔 | `mahjong/pixel/codeinferno-mahjong-tileset/`（第三類，授權待確認） |

## 待手動下載（itch.io）

| 套件 | 路徑 |
|------|------|
| GambleMountain Riichi 32×32 | `1-free-commercial/mahjong/riichi/gamblemountain-riichi-asset/` |
| moxica 傳統 43 張 | `1-free-commercial/mahjong/vector/moxica-tile-mahjong/` |
| Anisimova 向量 42 張 | `1-free-commercial/mahjong/vector/anisimova-vector-mahjong/` |
| Magory 免費像素示範組 | `1-free-commercial/mahjong/pixel/magory-free-pixel-set/` |
