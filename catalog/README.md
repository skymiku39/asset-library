# 素材清單導覽

## 授權分類清單

| 分類 | 文件 |
|------|------|
| 完全免費授權商用 | [01-free-commercial.md](01-free-commercial.md) |
| 商用需購買授權 | [02-paid-commercial.md](02-paid-commercial.md) |
| 不確定相關規範 | [03-license-unclear.md](03-license-unclear.md) |

## 素材類型

目前以 **撲克牌**、**麻將** 為主；`playing-cards`、`mahjong`、`ui`、`sound`、`character` 皆**先分風格**再放套件：

| 類型 | 目錄 slug | 清單 |
|------|-----------|------|
| 撲克牌 | `playing-cards` | [playing-cards.md](playing-cards.md)｜機器可讀：[playing-cards.json](playing-cards.json) |
| 麻將 | `mahjong` | [mahjong.md](mahjong.md)｜機器可讀：[mahjong.json](mahjong.json) |
| UI | `ui` | [ui.md](ui.md)｜機器可讀：[ui.json](ui.json) |
| 綜合性 | `mixed` | [mixed.md](mixed.md)｜機器可讀：[mixed.json](mixed.json) |
| 音效 | `sound` | [sound.md](sound.md)｜機器可讀：[sound.json](sound.json) |
| 角色 | `character` | [character.md](character.md)｜機器可讀：[character.json](character.json) |
| 特效 | `vfx` | [vfx.md](vfx.md)｜機器可讀：[vfx.json](vfx.json) |
| 18+ 成人向 | `adult-18plus` | [adult-18plus.md](adult-18plus.md)｜機器可讀：[adult-18plus.json](adult-18plus.json) |

## 風格母分類（先分風格）

**撲克牌 `playing-cards`**、**麻將 `mahjong`**、**UI `ui`**、**音效 `sound`** 與 **角色 `character`** 在套件之上多一層**風格母分類**，方便先依風格挑選。

撲克牌 `playing-cards`：

| 風格 slug | 說明 |
|-----------|------|
| `pixel` | 像素風 |
| `vector` | 向量／SVG |
| `flat` | 扁平／標準牌面 |
| `stylized` | 藝術／裝飾風 |
| `3d` | 3D |

麻將 `mahjong`：

| 風格 slug | 說明 |
|-----------|------|
| `pixel` | 像素風 |
| `vector` | 向量／傳統牌面 |
| `riichi` | 立直麻將 |
| `3d` | 3D |

綜合性 `mixed`：

| 子類 slug | 說明 |
|-----------|------|
| `poker-kit` | 撲克遊戲包（牌+籌碼+牌桌） |
| `mahjong-kit` | 麻將遊戲包（牌+UI+範本） |
| `boardgame` | 棋盤／通用遊戲包 |

UI `ui`：

| 風格 slug | 說明 |
|-----------|------|
| `flat-clean` | 扁平／簡潔 |
| `pixel-ui` | 像素 UI |
| `casual-cartoon` | 休閒卡通 |
| `fantasy-rpg` | 奇幻 RPG |
| `sci-fi` | 科幻 |

音效 `sound`：

| 風格 slug | 說明 |
|-----------|------|
| `realistic-foley` | 寫實擬音（牌／籌碼／骰子） |
| `ui-modern` | 現代 UI 介面音 |
| `retro-8bit` | 復古 8-bit／街機 |
| `casino-bgm` | 賭場／爵士氛圍 BGM |

角色 `character`：

| 風格 slug | 說明 |
|-----------|------|
| `pixel-art` | 像素風 |
| `toon-cartoon` | 卡通／Q版 |
| `vector-flat` | 向量／扁平 |
| `anime-2d` | 動漫／立繪 |
| `low-poly-3d` | 3D 低多邊形 |

特效 `vfx`：

| 風格 slug | 說明 |
|-----------|------|
| `pixel-vfx` | 像素特效（爆炸、魔法、打擊動畫） |
| `particle-texture` | 粒子貼圖（火花、煙霧、光暈） |
| `ui-juice` | UI 回饋特效（加分、閃光、收集） |
| `impact-hit` | 命中／打擊特效 |

**18+ 成人向 `adult-18plus`**：

| 風格 slug | 說明 |
|-----------|------|
| `vn-sprite` | 視覺小說立繪（靜態 PNG／PSD） |
| `anime-2d` | 動漫 2D 立繪（含 AI 生成） |
| `animation` | 角色動畫（序列影格／影片） |
| `pixel-art` | 像素風 NSFW |
| `background` | 成人向背景場景 |

## 路徑格式

```
一般：      assets/{授權分類}/{素材類型}/{套件名}/SOURCE_LICENSE.md
先分風格：  assets/{授權分類}/{素材類型}/{風格}/{套件名}/SOURCE_LICENSE.md
```

範例：
範例：
- `assets/1-free-commercial/playing-cards/flat/cards2-cc0/SOURCE_LICENSE.md`
- `assets/1-free-commercial/mixed/poker-kit/sbs-2d-poker-pack/SOURCE_LICENSE.md`
- `assets/1-free-commercial/mahjong/riichi/fluffystuff-riichi-mahjong-tiles/SOURCE_LICENSE.md`
- `assets/1-free-commercial/ui/flat-clean/kenney-ui-pack/SOURCE_LICENSE.md`
- `assets/1-free-commercial/sound/realistic-foley/kenney-casino-audio/SOURCE_LICENSE.md`
- `assets/1-free-commercial/character/pixel-art/chromoxi-good-and-evil/SOURCE_LICENSE.md`
