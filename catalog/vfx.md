# 特效素材總覽

> 最後更新：2026-07-08

## 目錄結構（先分風格）

特效在「素材類型」之下多一層 **風格母分類**，先依風格分類再放套件：

```
assets/{授權分類}/vfx/{風格}/{套件名}/SOURCE_LICENSE.md
```

範例：`assets/1-free-commercial/vfx/particle-texture/kenney-particle-pack/`

機器可讀：[vfx.json](vfx.json)

## 風格母分類

| 風格 slug | 說明 | 適用場景 |
|-----------|------|----------|
| `pixel-vfx` | 像素特效（爆炸、魔法、打擊動畫） | 像素風、復古街機、2D 動作 |
| `particle-texture` | 粒子貼圖（火花、煙霧、光暈） | 引擎粒子系統、UI 閃光、環境氛圍 |
| `ui-juice` | UI 回饋特效（加分、閃光、收集） | 得分、金幣、強化道具、成就提示 |
| `impact-hit` | 命中／打擊特效 | 攻擊命中、碰撞回饋、技能打擊 |

## 已收錄套件（皆為完全免費授權商用）

### 粒子貼圖 `particle-texture`

| 套件 | 授權 | 內容 |
|------|------|------|
| [Kenney Particle Pack](../assets/1-free-commercial/vfx/particle-texture/kenney-particle-pack/) | CC0 | 80+ 粒子貼圖；含火焰、煙霧、魔法、愛心、火花、電流範例 |
| [Kenney Smoke Particles](../assets/1-free-commercial/vfx/particle-texture/kenney-smoke-particles/) | CC0 | 煙霧粒子貼圖 spritesheet |
| [Kenney Splat Pack](../assets/1-free-commercial/vfx/particle-texture/kenney-splat-pack/) | CC0 | 30+ 潑濺／塗抹貼圖，含向量原始檔 |
| [Brackeys VFX Bundle](../assets/1-free-commercial/vfx/particle-texture/brackeys-vfx-bundle/) | CC0 | 粒子貼圖、flipbook 與預繪 spritesheet 合集 |
| [Kronbits 1000 Particles](../assets/1-free-commercial/vfx/particle-texture/kronbits-particle-pack-1000/) | CC0 | 1000 張 512×512 粒子貼圖 |

### 像素特效 `pixel-vfx`

| 套件 | 授權 | 內容 |
|------|------|------|
| [CodeManu Free Pixel Effects Pack](../assets/1-free-commercial/vfx/pixel-vfx/codemanu-pixel-effects/) | CC0 / PD | 20 個像素特效動畫，100×100px |
| [CodeManu Free VFX Asset Pack](../assets/1-free-commercial/vfx/pixel-vfx/codemanu-vfx-free-pack/) | CC0 / PD | 22 個像素特效，含 30/60fps 與 SpriteMancer 專案檔 |
| [Foozle Pixel Magic Effects](../assets/1-free-commercial/vfx/pixel-vfx/foozle-pixel-magic-effects/) | CC0 | 10 組 32×32 魔法特效（火／水／土／風／傳送門／爆炸） |
| [Foozle Lucifer Effects](../assets/1-free-commercial/vfx/pixel-vfx/foozle-lucifer-effects/) | CC0 | 拾取物、裝備、攻擊用像素特效，含 Aseprite 原始檔 |
| [Vitalyez Fireball VFX](../assets/1-free-commercial/vfx/pixel-vfx/vitalyez-fireball-vfx/) | CC0 | 12 幀火球特效，32×32px |
| [M484 Explosion Set 1](../assets/1-free-commercial/vfx/pixel-vfx/m484-explosion-set-1/) | PD | 經典 2D 爆炸動畫，3 種配色主題 |
| [M484 Explosion Set 2](../assets/1-free-commercial/vfx/pixel-vfx/m484-explosion-set-2/) | PD | 3 種爆炸 × 4 配色 × 30/16px 兩種尺寸 |
| [M484 Explosion Set 3](../assets/1-free-commercial/vfx/pixel-vfx/m484-explosion-set-3/) | OGA-BY 4.0 | 多種風格爆炸，含 16/32px 與多配色 |
| [tiopalada Spring VFX Pack](../assets/1-free-commercial/vfx/pixel-vfx/tiopalada-spring-vfx/) | CC0 | 7 組春季主題 RPG 魔法特效 |
| [TornadoGames Magic Sparks](../assets/1-free-commercial/vfx/pixel-vfx/tornadogames-magic-sparks/) | CC0 | 魔法火花／火球／爆炸（清單收錄，itch 多檔需手動全下） |

### UI 回饋特效 `ui-juice`

| 套件 | 授權 | 內容 |
|------|------|------|
| [Bevouliin Shining Items](../assets/1-free-commercial/vfx/ui-juice/bevouliin-shining-items/) | CC0 | 閃光金幣、生命、強化道具旋轉動畫 |
| [EverCrazy 8x8 Coin/Gem](../assets/1-free-commercial/vfx/ui-juice/evercrazy-coin-gem-8x8/) | CC0 | 90+ 個 8×8 金幣／寶石動畫 sprite |

### 命中／打擊特效 `impact-hit`

| 套件 | 授權 | 內容 |
|------|------|------|
| [Pixel Art Impact VFX](../assets/1-free-commercial/vfx/impact-hit/kekkorider-impact-vfx/) | 免費商用 | 7 種變體 × 5 色，共 35 組命中特效，128×128px |
| [GustavoPlima Hit Confirm](../assets/1-free-commercial/vfx/impact-hit/gustavoplima-hit-confirm/) | OGA-BY 4.0 | 6 組小型命中確認爆炸特效 |

## 推薦選用

| 需求 | 推薦 |
|------|------|
| 通用粒子貼圖（火花、煙霧、魔法） | `particle-texture/kenney-particle-pack/` |
| 煙霧／潑濺粒子 | `particle-texture/kenney-smoke-particles/`、`kenney-splat-pack/` |
| 大量粒子貼圖備選 | `particle-texture/kronbits-particle-pack-1000/` |
| 引擎粒子快速上手合集 | `particle-texture/brackeys-vfx-bundle/` |
| 像素風爆炸動畫 | `pixel-vfx/m484-explosion-set-1/`～`set-3/` |
| 像素風魔法／元素特效 | `pixel-vfx/foozle-pixel-magic-effects/`、`tiopalada-spring-vfx/` |
| 火球投射物 | `pixel-vfx/vitalyez-fireball-vfx/` |
| 金幣／得分閃光動畫 | `ui-juice/bevouliin-shining-items/`、`evercrazy-coin-gem-8x8/` |
| 打擊／命中回饋 | `impact-hit/kekkorider-impact-vfx/`、`gustavoplima-hit-confirm/` |

## 本輪再擴充

- `particle-texture`：新增 `para-animated-particle-effects-1`、`para-animated-particle-effects-2`、`kenney-smoke-particle-assets`、`rubberduck-teleporter-effect`
- `pixel-vfx`：新增 `ansimuz-warped-shooting-fx`、`systemg6-rpg-vfx-pack`
- `ui-juice`：新增 `vwolfdog-sparkle-animations`
- `impact-hit`：新增 `metashinryu-slash-effect-collection`
