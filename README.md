# 找素材專案

從各種來源搜尋、下載並整理遊戲／專案所需素材的中央素材庫。

## 目錄結構（雙軸分類）

素材依 **授權狀態** 與 **素材類型** 兩個維度組織：

```
assets/
├── 1-free-commercial/          # 完全免費授權商用
│   ├── playing-cards/          # 撲克牌（先分風格）
│   ├── mahjong/                # 麻將（先分風格）
│   ├── ui/                     # UI（先分風格）
│   ├── mixed/                  # 綜合性（先分子類）
│   ├── sound/                  # 音效（先分風格）
│   └── character/              # 角色（先分風格）
├── 2-paid-commercial/          # 商用需購買授權
├── 3-license-unclear/          # 不確定相關規範
└── local-references/           # 本機其他專案參照
```

每個套件資料夾內必有 **`SOURCE_LICENSE.md`**，記錄來源網址、授權條款與商用／署名要求。

### 先分風格（風格母分類）

`playing-cards`、`mahjong`、`ui`、`sound`、`character`、`mixed` 類型在套件之上**多一層風格或子類母分類**，方便先依類型挑選：

```
mixed/
├── poker-kit/        # 撲克遊戲包（牌+籌碼+牌桌）
├── mahjong-kit/      # 麻將遊戲包（牌+UI+範本）
└── boardgame/        # 棋盤／通用遊戲包
    └── {套件名}/SOURCE_LICENSE.md

playing-cards/
├── pixel/            # 像素風
├── vector/           # 向量／SVG
├── flat/             # 扁平／標準牌面
├── stylized/         # 藝術／裝飾風
└── 3d/               # 3D
    └── {套件名}/SOURCE_LICENSE.md

mahjong/
├── pixel/            # 像素風
├── vector/           # 向量／傳統牌面
├── riichi/           # 立直麻將
└── 3d/               # 3D
    └── {套件名}/SOURCE_LICENSE.md

ui/
├── flat-clean/       # 扁平／簡潔
├── pixel-ui/         # 像素 UI
├── casual-cartoon/   # 休閒卡通
├── fantasy-rpg/      # 奇幻 RPG
└── sci-fi/           # 科幻
    └── {套件名}/SOURCE_LICENSE.md

sound/
├── realistic-foley/   # 寫實擬音（牌／籌碼／骰子）
├── ui-modern/         # 現代 UI 介面音
├── retro-8bit/        # 復古 8-bit／街機
└── casino-bgm/        # 賭場／爵士氛圍 BGM
    └── {套件名}/SOURCE_LICENSE.md

character/
├── pixel-art/       # 像素風
├── toon-cartoon/    # 卡通／Q版
├── vector-flat/     # 向量／扁平
├── anime-2d/        # 動漫／立繪
└── low-poly-3d/     # 3D 低多邊形
    └── {套件名}/SOURCE_LICENSE.md
```

風格清單集中定義於 `tools/pack_registry.json` 的 `*_styles` 對照表；套件加上 `style` 欄位即可自動歸位。

## 授權分類

| 目錄 | 說明 |
|------|------|
| `1-free-commercial` | CC0、MIT、明確允許免費商用 |
| `2-paid-commercial` | 需付費購買後方可商用（僅清單或已購買檔案） |
| `3-license-unclear` | 授權不明確，使用前需確認 |
| `local-references` | 本機其他專案已有副本，僅作參照連結 |

## 素材類型

| 目錄 | 說明 |
|------|------|
| `playing-cards` | 撲克牌牌面、牌背 |
| `mahjong` | 麻將牌、麻將 UI |
| `ui` | 介面元件、按鈕、面板 |
| `mixed` | 綜合性遊戲包（牌+籌碼+牌桌等，先分子類） |
| `sound` | 音效、BGM |
| `character` | 角色立繪、sprite |

## 清單與工具

| 項目 | 路徑 |
|------|------|
| 撲克牌總覽 | [catalog/playing-cards.md](catalog/playing-cards.md) |
| 麻將總覽 | [catalog/mahjong.md](catalog/mahjong.md) |
| 綜合性總覽（先分子類） | [catalog/mixed.md](catalog/mixed.md) |
| UI 總覽（先分風格） | [catalog/ui.md](catalog/ui.md) |
| 音效總覽（先分風格） | [catalog/sound.md](catalog/sound.md) |
| 免費商用清單（含角色風格分類） | [catalog/01-free-commercial.md](catalog/01-free-commercial.md) |
| 套件登錄表（機器可讀） | [tools/pack_registry.json](tools/pack_registry.json) |
| 目錄重整工具 | `uv run python tools/reorganize_assets.py` |

## 新增素材流程

1. 在 `tools/pack_registry.json` 登記套件（含 `asset_type`、`license_category`；UI／音效／角色另加 `style`）
2. 將檔案放入對應目錄
3. 執行 `uv run python tools/reorganize_assets.py` 產生 `SOURCE_LICENSE.md` 並更新 catalog
