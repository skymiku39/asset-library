# 18+ 成人向素材總覽

> 最後更新：2026-07-14

> **注意**：本類別收錄含裸露、性暗示或露骨內容的遊戲素材，僅供 18 歲以上專案使用。使用前請再次確認各套件授權條款。

## 收錄統計

| 授權分類 | 狀態 | 套件數 |
|----------|------|--------|
| 完全免費授權商用 | downloaded | 38 |
| 授權待確認 | downloaded | 3 |
| 授權待確認 | 待手動下載 | 1 |
| 商用需購買 | catalog-only | 8 |
| **合計** | | **50** |

機器可讀：[adult-18plus.json](adult-18plus.json)

## 本次擴充重點（2026-07-14）

### DLsite（擴大作者掃描）
- 掃描 15 個素材作者頁，檢查 171 商品，找到 **50** 個帶 trial zip。
- 新下載並登錄 **17** 套體驗版：
  - 菊にぃ 擬音／セリフ／英語文字／擬音ブラシ（IMT ×4）
  - Pincree 等 R18 語音／KU100 効果音（AMT ×13）
- 工具：`uv run python tools/discover_dlsite_trials.py`（作者頁掃描；關鍵字搜尋仍會 403）
- 下載：`uv run python tools/dlsite_download.py <商品頁> <dest>`

### itch.io 新增
| 套件 | 授權 | 狀態 |
|------|------|------|
| Eros Fem VN Sprite Set 1 | CC0 | 已下載 |
| Meiro Knight Battler (Nudity) | 可商用（需署名） | 已下載 |
| Cool Devil Agatha Sprites | 待確認 | 已下載 |
| Fahrenheit Amanda P1 | 待確認 | 需手動下載 |

## 推薦免費來源路徑

| 需求 | 路徑 |
|------|------|
| VN 立繪 PSD | `adult-18plus/vn-sprite/eros-fem-vn-sprite-set-1/`、`eros-fem-vn-sprite-set-2/` |
| LeafletGames 手繪立繪 | `adult-18plus/vn-sprite/leafletgames-sprites-*` |
| DLsite 森の奥 体験版立繪 | `adult-18plus/vn-sprite/dlsite-morinooku-*-trial/` |
| R18 擬音文字 | `adult-18plus/ui/dlsite-菊屋素材集-*` |
| R18 語音／効果音體驗版 | `adult-18plus/sound/dlsite-*` |

## 搜尋方式

### DLsite
1. 關鍵字搜尋頁常回 **403** → 改掃作者 `maker_id`
2. 目標：商品頁內 `trial.dlsite.com/..._trial.zip`
3. 優先收錄 `IMT`（圖像）與 `AMT`（成人音訊）；暫不收刮權利不清的授權 IP 3D 模型（TOL）

### itch.io
- [Free NSFW Sprites](https://itch.io/game-assets/free/nsfw/tag-sprites)
- 優先 CC0／明確可商用；否則放 `3-license-unclear`
