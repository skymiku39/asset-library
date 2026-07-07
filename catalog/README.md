# 素材清單導覽

## 授權分類清單

| 分類 | 文件 |
|------|------|
| 完全免費授權商用 | [01-free-commercial.md](01-free-commercial.md) |
| 商用需購買授權 | [02-paid-commercial.md](02-paid-commercial.md) |
| 不確定相關規範 | [03-license-unclear.md](03-license-unclear.md) |

## 素材類型

目前以 **撲克牌**、**麻將** 為主：

| 類型 | 目錄 slug | 清單 |
|------|-----------|------|
| 撲克牌 | `playing-cards` | [playing-cards.md](playing-cards.md) |
| 麻將 | `mahjong` | [mahjong.md](mahjong.md) |
| UI | `ui` | 待收錄 |
| 綜合性 | `mixed` | 牌+籌碼+牌桌等多類素材 |
| 音效 | `sound` | **先分風格**，再放套件（見下）｜清單：[sound.md](sound.md)｜機器可讀：[sound.json](sound.json) |
| 角色 | `character` | **先分風格**，再放套件（見下）｜機器可讀：[character.json](character.json) |

## 風格母分類（先分風格）

**音效 `sound`** 與 **角色 `character`** 在套件之上多一層**風格母分類**，方便先依風格挑選。

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

## 路徑格式

```
一般：      assets/{授權分類}/{素材類型}/{套件名}/SOURCE_LICENSE.md
先分風格：  assets/{授權分類}/{素材類型}/{風格}/{套件名}/SOURCE_LICENSE.md
```

範例：
- `assets/1-free-commercial/playing-cards/cards2-cc0/SOURCE_LICENSE.md`
- `assets/1-free-commercial/sound/realistic-foley/kenney-casino-audio/SOURCE_LICENSE.md`
- `assets/1-free-commercial/character/pixel-art/chromoxi-good-and-evil/SOURCE_LICENSE.md`
