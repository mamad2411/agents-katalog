---
name: landing-page-studio
description: Use when creating high-conversion landing pages with modern visual effects, including SVG/WebGL animation, autonomous multi-iteration optimization, and dual output modes (single-file HTML or React project). Trigger on requests like landing page, LP, hero section build, animated marketing page, conversion page redesign, or style variants A-L/custom.
---

# Landing Page Studio

## Overview

此技能用於快速產出「可直接交付」的 Landing Page，重點是轉換導向、視覺辨識度、動畫品質與實務性能平衡。

能力範圍：

1. 自主多輪產生與優化（最多 3 輪）
2. 現代前端特效（SVG procedural、GSAP、Anime.js、可選 Three.js/WebGL）
3. 雙輸出模式：`single-file-html`、`react-project`
4. Progressive Enhancement：低效能或 reduced motion 自動降級
5. 品質門檻驗收（視覺與性能雙門檻）

## Input Contract

輸入物件型別：`LandingPageInput`

必要欄位：

- `brand_theme`: `string`
- `value_props`: `string[3]`
- `primary_cta`: `string`
- `style_variant`: `A|B|C|D|E|F|G|H|I|J|K|L|custom`
- `output_mode`: `single-file-html|react-project`

選填欄位：

- `variant_mode`: `single|batch`，預設 `single`
- `autonomy_mode`: `single-pass|multi-iteration`，預設 `multi-iteration`
- `animation_level`: `low|medium|high`，預設 `high`
- `motion_preference`: `respect-reduced-motion`（建議預設採用）
- `target_audience`: `string`
- `industry`: `string`
- `react_stack`: `vite-react-tailwind-framer|nextjs-app-router|react-css-modules`

## Data Sufficiency Gate

若下列欄位任一缺失，先回 `MissingDataOutput`，不可生成頁面：

- `brand_theme`
- `value_props`
- `primary_cta`
- `style_variant`
- `output_mode`

`MissingDataOutput` 必須包含：

- `missing_fields`
- `why_needed`
- `questions_to_user`
- `next_step_rule`

## Output Contract

生成成功時回 `GenerationOutput`：

- `artifact_type`: `single-html|react-tree`
- `artifact_payload`: HTML 字串或檔案樹
- `asset_sources`: Unsplash/Pexels 來源與 attribution
- `animation_manifest`: 每段動畫的 `library`, `target`, `trigger`, `fallback`
- `autonomy_report`: 候選版本評分與最終採用理由
- `qa_report`: 門檻結果與修正記錄

## Mode Rules

### 1) `single-file-html`

- 交付單一 `index.html`
- 允許 CDN：Tailwind、GSAP、Iconify、Three.js、Anime.js、Google Fonts
- 需包含：Navbar、Hero、Value Props、Social Proof、Final CTA、Footer

### 2) `react-project`

- 若未指定 `react_stack`，先提供三種技術棧優缺點，再請使用者選擇
- 預設優先順序：`vite-react-tailwind-framer`
- 交付至少包含可啟動專案骨架與核心頁面

## Autonomous Generation Flow

若 `autonomy_mode=multi-iteration`，使用以下流程：

1. 依輸入產生 2-3 個候選稿（結構一致、視覺與動畫策略不同）
2. 依四維度打分：
   - conversion clarity
   - visual coherence
   - readability
   - performance risk
3. 選最低分項目做修正，最多 3 輪
4. 產出最佳版，並附 `autonomy_report`

若 `autonomy_mode=single-pass`：

- 只產 1 稿，仍需附簡版 `qa_report`

## Style System

支援 A-L 共 12 套預設風格，細節見：

- [02-style-presets-12.md](./references/02-style-presets-12.md)

若 `style_variant=custom`：

- 先抽取視覺關鍵詞（tone、contrast、material、motion）
- 映射到最接近的預設風格作為基底
- 僅在偏離需求時覆寫局部 token

## Animation System

動畫能力與降級矩陣見：

- [03-animation-system-and-fallbacks.md](./references/03-animation-system-and-fallbacks.md)

硬性規則：

1. 至少包含 4 類動畫
2. 必須提供每段 fallback
3. `prefers-reduced-motion` 時關閉高刺激動效
4. 無 WebGL 能力時自動使用 SVG/CSS 替代

## Asset Rules

1. 圖片來源只允許 Unsplash/Pexels
2. 不可使用 placeholder
3. Hero 必須加遮罩保證文字可讀
4. 輸出 `asset_sources` 必須含 attribution

## Quality Gates

完整規則見：

- [05-quality-gates.md](./references/05-quality-gates.md)

最低通過門檻：

1. Desktop: Performance >= 85, Accessibility >= 90
2. Mobile: Performance >= 75, Accessibility >= 90
3. 主要斷點需完整可讀（mobile/tablet/desktop）

## Conversion and Copy Rules

轉換導向內容結構與文案規範見：

- [06-copy-and-conversion-structure.md](./references/06-copy-and-conversion-structure.md)

## Scripts

- `scripts/validate_intake.py`: 驗證並標準化輸入，必要時回 MissingDataOutput
- `scripts/build_animation_manifest.py`: 根據 style/animation level 產生動畫清單與 fallback

## Templates

- `assets/templates/single-file-starter.html`: 單檔輸出骨架
- `assets/templates/react-vite-starter/`: React 專案骨架

## Execution Checklist

1. 先跑 intake 驗證
2. 再選擇輸出模式
3. 產生候選稿與動畫策略
4. 執行多輪優化（若開啟）
5. 產出 `GenerationOutput`
6. 附 `qa_report` 與 `asset_sources`

## Suggested Prompt

`Use $landing-page-studio with style_variant=C, output_mode=single-file-html, autonomy_mode=multi-iteration, animation_level=high, and motion_preference=respect-reduced-motion.`
