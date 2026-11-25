---
name: mobile-ui-playbook
description: Use when building or polishing mobile app UI visuals (Flutter, SwiftUI, Jetpack Compose) — before choosing spacing, typography, color, corner radius, elevation, or motion duration; when a screen "looks off", feels cluttered, cheap, or inconsistent; when reviewing touch targets, contrast ratio, Dynamic Type, text overflow, or dark mode; also when hard-coded colors/paddings spread across widgets, or every new screen re-invents its own styling.
---

> 🌐 [English version](https://github.com/tienenwu/fables/blob/main/en/mobile-ui/SKILL.md) · 繁體中文（正本 / canonical）

# Mobile UI 美觀判準手冊

「好看」不是品味玄學，是一致性、層級、密度、對比四件事的副產品。本手冊把它們寫成可裁決的數字與判準。

## 核心原則

1. **美觀是一致性的副產品**：token（間距/字級/色彩/圓角）先於畫面——畫面只消費 token，不自創數值；每個「就地微調」都在借高利貸。
2. **淺色＋預設字級＋大螢幕＋短資料的綠燈不算數**：深色模式、放大字級、小螢幕真機、長字串／真實資料是四條獨立驗證軸，各自能單獨讓 UI 崩壞。
3. **層級靠大小、字重、明度差、位置表達，不靠裝飾**：陰影、漸層、分隔線是最後 10% 的收尾，不是層級不清的補救藥。
4. **可點的東西必須夠大、夠像可點**：觸控目標 ≥44×44pt（iOS）/48×48dp（Android），互動元素與純文字要有可辨差異。
5. **動效是狀態變化的說明書**：元素的出現/消失/移動要有過渡（小元件 100–200ms、畫面轉場 250–350ms）；超過 500ms 使用者體感是「卡」，不是「華麗」。

## 開工分流

| 情境 | 路徑 | 先讀 |
|------|------|------|
| 新畫面開工 | 先確認 spacing/色彩/字級 token 齊備，再排版 | references/design-tokens.md |
| 選字級、字重、行高 | 走 type scale 判準，一畫面 ≤4 檔字級 | references/design-tokens.md §字級 |
| 挑顏色、做深色模式 | 只用 semantic color role，不挑裸 hex | references/design-tokens.md §色彩 |
| 畫面「看起來怪」說不出哪裡怪 | 跑五步診斷：對齊→間距→層級→色彩→密度 | references/layout-hierarchy.md §診斷 |
| 排版、對齊、資訊密度 | 單一 leading 邊線＋4/8 網格 | references/layout-hierarchy.md |
| 加動效、轉場 | 時長與 easing 區間判準 | references/layout-hierarchy.md §動效 |
| UI 完成要出貨 | 四軸＋極端資料逐條驗 | references/release-checklist.md |

## 紅線（絕對禁止）

- **禁止在 widget/view 內硬編碼色值、字級、間距數字**——深色模式與改版時全面崩壞；所有數值走 theme/token。
- **禁止觸控目標小於 44×44pt / 48×48dp**——點不中與誤觸是使用者體感「廉價」的最直接來源；視覺可以小，hit area 不行。
- **禁止內文對比低於 4.5:1（大字 3:1，WCAG AA）**——低對比在戶外陽光下直接不可讀；「設計稿就是這個灰」不是理由。
- **禁止把淺色主題逐色反轉當深色模式**——深色模式是重新指派 semantic role（surface 升明度表達 elevation、降飽和），不是 invert。
- **禁止照設計稿固定寬高硬排**——長使用者名、德文標籤、130% 字級任一個就爆版；一律彈性布局＋極端資料驗。
- **禁止一個畫面出現第 3 種強調色或第 4 檔圓角**——想加新值時回 token 層裁決，不准就地發明。
- **禁止只在淺色模式＋預設字級＋模擬器大螢幕驗過就宣告 UI 完成**——四軸各是獨立故障域，零證據力交集。

## 失敗訊號（該回頭，不是重試）

| 徵兆 | 多半是 | 退回 |
|------|--------|------|
| 每個新畫面都在重新決定 padding 數字 | 缺 spacing token 標尺 | token 層定 4/8 標尺，全畫面吸附 |
| 深色模式一堆元素看不清或刺眼 | 色彩硬編碼、沒走 semantic role | 色彩層重構，不是逐處補色 |
| 換語言或接真資料就爆版 | 固定寬高思維 | 彈性布局＋極端資料重驗 |
| 「再加一點陰影就好看了」第 3 次出現 | 層級結構問題，不是裝飾不足 | 大小/字重/間距的層級設計 |
| 間距微調來回改不定 | 沒有網格基準，憑感覺對齊 | 全部吸附 4/8 網格再談微調 |
| 這頁改完那頁又不一致 | 樣式散落、無單一真相 | theme/token 單一來源 |

## references 索引

- `references/design-tokens.md` — 間距標尺、type scale、semantic color、深色模式、圓角/elevation 檔數、token 的機器強制。動手排版前讀。
- `references/layout-hierarchy.md` — 對齊、視覺層級、密度、觸控目標、動效時長、「看起來怪」五步診斷。畫面不對勁時讀。
- `references/release-checklist.md` — UI 出貨前必查：四軸驗證、極端資料、對比與觸控目標稽核。出貨前逐條打勾。
- `references/test-scenarios.md` — 判準測驗集，驗證接手模型是否照走。不給執行中的模型讀。
