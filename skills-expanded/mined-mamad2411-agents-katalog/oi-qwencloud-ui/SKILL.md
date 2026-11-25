---
name: oi-qwencloud-ui
description: >-
  Qwen Cloud brand UI: simple flat surfaces, weak borders, light shadow only, purple-on-hover CTAs,
  Inter + Roboto Mono. Icons and photos MUST come from CDN Icons.json / Images.json manifests.
  TRIGGER for Qwen Cloud style, oi-qwencloud-ui, qwencloud-ui, or Qwen Cloud landing/product UI.
  NOT for generic UI, other brands, or video/media tools.
---
# Oi Qwen Cloud UI — Qwen Cloud Design System

**Author:** Alibaba Cloud Design

**Skill path:** `<skill-dir>/` (e.g. `~/.cursor/skills/oi-qwencloud-ui`).

Reference specs: `references/` (`tokens.md`, `components.md`, `layouts.md`, `icons.md`, `assets.md`). Brand kit on CDN — see `assets.md`.

---

## 核心约束（Agent 必守）

### ★ 头号铁律 — 大标题永远不要压在视觉元素上

**Title + subtitle are their own clean paragraph on white (`--pt-color-neutral-50`). The image/video/flower/gradient is a SEPARATE panel below or beside. Two paragraphs, never one box.**

- ❌ Wrong: `<div class="hero-panel" style="background-image: flower.jpg"><h1>AI 驱动的…</h1></div>` — heading sitting over the flower
- ✅ Right: `<header><h1>Ship the next</h1><p>subtitle</p><CTAs/></header>` on `neutral-50`, **then** a separate `<div class="hero-panel">image/video</div>` below with 48–64 px whitespace between
- No `text-shadow`, no dark overlay "for legibility" — if a heading needs help reading, it's in the wrong place; move it up to the canvas paragraph
- Upper bound for text on imagery: **title-lg 28 px** (small metric chips, captions). Anything ≥36 px belongs in the title paragraph on canvas
- Only exception: era closing-CTA hero (`layouts.md` §2.5) — has an art-directed quiet video backdrop and centered 72 px h2. Don't generalize this to other heroes

Full rule + DO/DON'T diagrams: `references/layouts.md` §2.

### 视觉气质：简洁 · 平白 · 弱描边 · 淡阴影

- **简洁** — 克制组件数量；营销页以 Inter 排版为主，图标小而稀。
- **平白** — `neutral-50` / `150` / `100` 面色阶分层；卡片与 hero 框架默认无装饰投影。
- **弱描边** — 仅 outline 按钮、表单、pricing featured  rim 等必要处使用 `line-200` 1px；不靠粗框线分区。
- **淡阴影** — 新页面默认 flat（`shadow: none`）；若需可读性分层，仅用 token 阴影且极轻，禁止厚重 drop-shadow / 发光底。

### 配图与图标：只从 manifest 抽取

**禁止** stock 图、占位图、自造 URL、Lucide/emoji、与 kit 混用的随机 SVG。

| 类型 | 做法 |
|------|------|
| **配图** | fetch `Images.json` → 使用数组中的 **绝对 URL**（`flower_*` 每页一张 hero；`card_1–4` 客户故事） |
| **图标** | fetch `Icons.json` → 按场景选 `id`，静态页用条目 **`href`**；React 优先 `@ali/qwen-cloud-icons` 同名组件 |

实现前若未读 manifest，先 fetch 再写 markup。详见 `references/assets.md`.

### 面板即卡片：外不描边 · 内不嵌灰底  ★

当一个区块本身就是「**面板即卡片**」（recommended models 列表、cost summary、feature 列表、step 介绍、FAQ 列表、bundle 内的子项汇总）时：

1. **外层面板不要描边。** 用 `--pt-gradient-card-bg` 或一阶中性步（`neutral-100`）做底，靠 bg-step 与画布分离；不要叠 `1px line-100` 外框线。`shadow: none`。
2. **面板内部的小区域不要再叠灰底子卡。** 推荐项 / 成本行 / 规格行 **不要**用 `bg-neutral-100`/`neutral-150` 圆角小盒子盛装；它们直接坐在面板上，用 **typography + hairline** 分层：
   - 标题：`font-semibold` body-lg / title-md，强对比 neutral-950
   - 描述：body-sm neutral-650/750
   - 价格 / 状态：mono `--pt-font-mono`，func 色（`func-success` 价格，neutral-650 价目）
   - 标签：单个 pill chip（`primary-50` / `neutral-150` 填充），**不**整块灰底盛一段信息
   - 行间分隔：`border-bottom: 1px solid var(--pt-color-line-100)`（标准），或 `0.5px var(--pt-color-line-200)`（密集数据）
3. **干净空白 > 视觉容器。** 标题与正文、行与行之间留 `12 / 16 / 24 / 32 px`；不要靠灰底圆角圈出"这是一个区域"。

对比：

```
❌ 错误 — 大卡片外有 1px 描边，内部又嵌灰底圆角小卡
┌─ bg-neutral-50  border 1px line-100  rounded-md ───────────┐
│  RECOMMENDED MODELS                                        │
│  ┌─ bg-neutral-150 rounded-sm ──────────────────────────┐ │   ← grey card-in-card
│  │  Qwen3.7-Max …                                       │ │
│  └──────────────────────────────────────────────────────┘ │
│  ┌─ bg-neutral-150 rounded-sm ──────────────────────────┐ │
│  │  Qwen3-Coder …                                       │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘

✅ 正确 — 外层无描边 wash 面板，内部行靠 hairline + typography
┌─ bg gradient-card-bg  rounded-md  no border  no shadow ───┐
│  RECOMMENDED MODELS  (mono uppercase neutral-450, mb-16)  │
│                                                            │
│  Qwen3.7-Max   [CORE]              ¥12 / 1M tokens         │  ← row directly on
│  Flagship LLM with deep grasp …                            │     panel; no fill
│  → Outline, episode scripts, dialogue lines                │
│  ─────────────────────────────────  border-b line-100      │
│  Qwen3-Coder   [ASSIST]            Low cost                │
│  Code-tuned model …                                        │
│  → Structured script JSON, relationship graphs             │
└────────────────────────────────────────────────────────────┘
```

适用清单：recommended models、bundle 内 cost summary、plan benefit、step intro、prod-shell prod-group、FAQ list、feature breakdown 等"卡内含多条目"场景。

详细规则与可视示例：`references/layouts.md` §11.6。bordered 紧凑 tile 网格（Supported AI Tools、logo tile）仍允许 `1px line-100` 单层描边 — 那不是面板即卡片。

---

## Usage

> **Agent:** If the user asks how to use this skill (`usage`, `怎么用`, `help`, `@oi-qwencloud-ui` without a concrete task), **reply with this section** (replace `<skill-dir>` with this skill's install path, e.g. `~/.agents/skills/oi-qwencloud-ui`), then ask what they want to accomplish.

**Triggers:** `oi-qwencloud-ui`, `qwencloud-ui`, qwen cloud ui, qwen cloud / qwencloud / Qwen Cloud / QwenCloud style & design, Qwen Cloud 风格 / 设计系统.

**Quick start**
1. Read this `SKILL.md` (philosophy, workflow, anti-patterns).
2. Load specs: `<skill-dir>/references/tokens.md`, `components.md`, `layouts.md`, `icons.md`, `assets.md`.
3. Inject the `@font-face` block below for Inter; load Roboto Mono per tokens. Ask light/dark, implement with `--pt-*` tokens.

**Example prompts**
- 「用 oi-qwencloud-ui 做 Qwen Cloud 产品页」
- 「按 Qwen Cloud tokens 做 model feature 双卡」
- 「Qwen Cloud 浅色 pricing + floral hero」

**Do not use for:** generic UI without explicit Qwen Cloud request; other brand kits; ffmpeg / video (`widget/*`).

## When to use

- User wants **Qwen Cloud** brand UI (cloud product marketing, model cards, pricing tiers, customer stories)
- Pages needing floral hero grids, near-black light-mode CTAs, and sparse outlined icons
- Token-level specs for forms, tags, gradients-as-text-only, and flat elevation

**Do not use** unless the user names Qwen Cloud or this skill.

---

## 1. Design philosophy

- **Simple, flat, quiet.** 简洁平白：弱描边、淡阴影（见核心约束）；色阶与留白优先于装饰。
- **Quiet and flat.** Background steps (`neutral-50` / `150` / `100`) replace heavy shadows; hairlines only when structure is unclear.
- **Purple on interaction.** Light primary CTA: near-black at rest, `primary-550` on hover — not purple fill at rest.
- **One accent per view.** Pick among: black CTA, one gradient word, or purple hover — do not compete.
- **Typography-led.** Inter for all marketing type; Roboto Mono for labels, pricing, uppercase captions.
- **Gradients are text-only.** Eight `--pt-gradient-*` tokens clip to single words; featured tier may use 1px gradient border rim only.
- **Photography as hero.** One `flower_*` per page behind headline; customer cards use `card_1–4` full-bleed art.

**Fonts (inject before coding):**

Embed the following `@font-face` block in the page's `<style>` (or top of the global CSS). Do **not** swap in Google Fonts, system fallbacks, or alternate URLs.

```css
@font-face {
    font-family: 'Inter';
    src: url('https://acd-assets.alicdn.com/acd_work/web-fonts/inter/Inter-Variable.ttf') format('truetype');
    font-style: normal;
    font-weight: 100 900;
    font-display: swap;
}
```

Then set `--pt-font-base: 'Inter', sans-serif`. Roboto Mono: see `references/tokens.md` § Typography.

**Reset (inject right after the `@font-face` block):**

Browser defaults italicize `<em>`, `<i>`, `<cite>`, `<dfn>`, `<var>`, `<address>` — that creates accidental italics inside body copy, captions, blockquotes, and AI-generated prose. Inject this minimal reset so emphasis becomes a deliberate utility class instead of a default. Reference: `/Users/duhaihang/Ali/Gitwork/organic/src/css/reset.scss` (canonical Meyer-style reset used by the source codebase — copy it wholesale when the page is more than a single landing block).

```css
*, *::before, *::after { box-sizing: border-box; }
html, body, h1, h2, h3, h4, h5, h6, p, ul, ol, li, figure, blockquote, dl, dd {
    margin: 0;
    padding: 0;
}
ul, ol { list-style: none; }
a { color: inherit; text-decoration: none; }
button { background: none; border: 0; padding: 0; font: inherit; color: inherit; cursor: pointer; }
img, svg, video { display: block; max-width: 100%; }
input, textarea, select { font: inherit; color: inherit; }

/* No accidental italics — render upright by default; italicize only via an explicit utility. */
em, i, cite, dfn, var, address { font-style: normal; }
```

If you need real emphasis, mark it with a deliberate class (e.g. `<em class="is-italic">`) and style it explicitly — never rely on the user-agent default.

---

## 2. Craft rules

### 2.1 Token namespace

Use `--pt-*` from `references/tokens.md` verbatim. **Spacing is literal px on a 2-px rhythm** — there is no `--pt-spacing-N` ladder. Pick from: `4 · 6 · 8 · 10 · 12 · 14 · 16 · 18 · 20 · 24 · 28 · 32 · 36 · 40 · 44 · 48 · 56 · 64 · 72 · 96 · 122 · 138`. See `references/layouts.md` §10.

### 2.2 Signature patterns

| Pattern | Rule |
|---------|------|
| Primary button | Pill; light: `neutral-950` fill → hover `primary-550`; icon `arrow-up-outlined` |
| Secondary | `primary-50` soft fill, no border |
| Outline | Only variant with `line-200` border |
| Model cards | 2-col grid; primary uses `gradient-card-bg`; secondary `neutral-50`; no shadow |
| Pricing | 3-up; featured tier gradient-1 **border rim** only |
| Hero | `neutral-100` flat; title up to 72/76; one `.grad` word |
| Customer card | Full-bleed image + white typographic panel, `radius-md` / `radius-xs` |
| Theme toggle | `sun-outlined` · `moon-outlined` |

### 2.3 Layout

Page-level composition lives in `references/layouts.md`. Highlights:

- **Marketing flat contract (§1.6):** all §4 floors — `shadow: none`, bg-step separation (`neutral-50` ↔ `100` ↔ `gradient-card-bg`), no nested grey sub-cards, hero/tail L1+L3 only.
- **Canonical page stacks (§4.0):** Home · Token Plan · Hackathon recipes — pick one; Token Plan accordion = §2.8 Mode B in hero, **not** §4.13.
- **Three container layers** (§1): `.layout-max-wide` (outer, ~140 px viewport gutter, for framed visuals) → `.layout-max-inner-wrap > .layout-max-inner` (inner, ~280 px gutter, **default** for headings/grids/copy) → reader (768 px cap, for prose). Never bypass.
- **Heading on white, never on imagery** (§2): giant H1/H2 sits on `--pt-color-neutral-50` (canvas) or `--pt-color-neutral-100` (tinted floor). Photos/videos sit in their *own* framed panel below or beside. Only exception: era closing CTA (§2.5).
- **Homepage hero** (§2.7–§2.8, variant B): centered h1 + subtitle on canvas → **Level 1 `btn--primary` + Level 3 `btn--outline`** → **48–64 px** gap → `.hero-visual` (`radius-lg`). Visual **Mode A:** hero image **450–480 px** + optional 4-up metrics (Hackathon). **Mode B:** accordion + preview **420 px** (`gradient-card-bg`, Token Plan). 字不压视觉 — title never inside the visual block.
- **9 hero variants A–I** (§3); **3 floor-head patterns A/B/C** + asymmetric D (§5); grid table at §7 — pull a row, don't invent.
- **§08 component gallery** (§19): 53 production cards + `ui-*` primitives — open CDN `Guideline.html` §08 or `components.md` §08 before building console/dashboard surfaces.
- **Card row floor** (§4.4): 3-up or 4-up pricing/prize/token tiers — flat cards (`shadow: none`), `line-100` hairline or **one** featured gradient rim, R9 interior (price → CTA → icon feature list §8.16); no grey feature sub-cards.
- **Media duo floor** (§4.5): 2-up **borderless** visual cards (Agent builder) — large `radius-md` media frame on top, left-aligned title + 2-line desc, **text-link CTA** + `arrow-up-right-outlined` (not pill buttons); no border/shadow on visual or card shell.
- **Simple card floor** (§4.6): 3-up **`line-100` no-shadow** cards — **A** step flow (`step-tag` + title + desc + centered floor `btn--primary`) or **B** skill/model row (name, chips, **price-text**, divider, 2-col metrics per R11).
- **Secondary showcase** (§4.7): **次级楼层** — shared **text-cards** (only `border-bottom line-100`). **A:** tabs §8.20 + R13 + optional `btn--outline`. **B (no tabs):** two-line left head + R13b + §8.22 carousel pager — e.g. AI and Cloud / ECS solutions row.
- **Logo floor** (§4.8): **A — matrix** — 4×N `.logo-matrix-tile` (`line-100`, icon + name, R14). **B — borderless strip** — `.logo-strip` row of brand logos on canvas only (no border/bg/shadow, R19). E.g. Supported AI Tools vs Our Partners.
- **Tail visual CTA** (§4.9): last marketing band before footer — **790 px** tall or **370 px** compact in `.layout-max-wide` (`radius-lg`); centered h2 (one gradient phrase) + subtitle + **Level 1 primary + Level 3 outline** (R15). E.g. Co-Build Future / Join the community.
- **Site footer** (§4.10): **35%** aside (flat social icons §8.24) + **65%** three-column link groups (R16); legal bar with `line-100` top rule — copyright left, Manage Cookies right. Flush under tail visual.
- **Carousel toggle** (§4.11): **100vw** horizontal card track — `line-100` bordered **or** `neutral-100` filled cards (`radius-lg`, no shadow). **A:** centered head + bottom ‹ › (§8.26, R17 testimonials). **B:** left head + pager in title row (R18 criteria). Click to slide; no autoplay/dots.
- **FAQ** (§4.12): two-column — left title + whitespace, right `+` accordion (R20). **Shell A:** `neutral-50` in `layout-inner`. **Shell B:** `neutral-100` `radius-lg` panel in `layout-max-wide`. §8.27: **first item open**, **single-open only** (always exactly one expanded).
- **Accordion + visual sync** (§4.13): centered head → **left** `+` fold list (R21) + **right** `radius-lg` preview (`min-height 400+`, cross-fade). §8.28 links `data-arena-panel` ↔ visual panel. E.g. **Choose Your Arena**. Not §2.8 hero Mode B (that's under `.hero-visual` 420 px).
- **Card system** (§11): two equally first-class flavors — bordered (hairline `--pt-color-line-100` on canvas) and **borderless** (bg-step separation when sitting on a stepped panel). Decision tree §11.4. Nine internal recipes §11.2 (incl. R9 card-row). Ten clean-flat signals §11.3.
- **Radius vocabulary (5):** `full · xs · sm · md · lg` → 999 / 12 / 18 / 24 / 36 (§15).
- **Section rhythm:** top-of-floor `96 / 122 / 138`; heading→body `48 / 60 / 64` (§1.5).
- **Sticky offset:** `calc(var(--pt-nav-backdrop-offset) + 12px)` for rails; nav is 84 px desktop / 62 px mobile.
- **Data-page interaction** (§17): models toolbar shares `height: 40 + radius-full` across all controls; search uses gradient mask-composite focus rim; popovers are borderless + `--pt-shadow-light`.
- **Breakpoint:** 1024 px; mobile gutters 20 px (utilities handle it); grids collapse to `1fr`.

### 2.4 Icons & assets (CDN)

All brand assets live on CDN — **not** in `<skill-dir>`. See `references/assets.md`.

| Asset | Source |
|-------|--------|
| Guideline | `…/qwencloud/Guideline.html` |
| Icons (48) | `…/qwencloud/Icons.json` → `Icons/*.svg` |
| Images | `…/qwencloud/Images.json` → absolute JPG URLs |
| Logo | Inline in Guideline |

**Mandatory:** every JPG from `Images.json` — no substitutes. Icons: prefer `Icons.json` / `@ali/qwen-cloud-icons`; when a needed glyph is **not** in the 48-icon manifest, fall back to **Tabler outlined** (`stroke: 1.5`, `currentColor`). One kit per screen — manifest **or** Tabler, never mixed. See `references/icons.md`.

**Dark mode icons in static HTML:** `filter: invert(1)` on `.qc-icon-img` where guideline specifies.

---

## 3. Anti-patterns

- **Panel-as-card outer stroke** — when a card hosts multi-row content (recommended list, cost summary, plan breakdown, FAQ), it must be borderless (`gradient-card-bg` or `neutral-100` step); no 1px outer hairline around the whole panel
- **Grey-bg sub-card inside a card** — no `neutral-100` / `neutral-150` filled rounded boxes wrapping individual rows inside an outer card; rows sit directly on the panel, divided by `border-b line-100`
- **Accidental italics** — reset block must include `em, i, cite, dfn, var, address { font-style: normal }`; italic only via an explicit utility class on a wrapper span
- No purple glyph fill on icons (`currentColor` only)
- No stock/placeholder images; no icons outside `Icons.json` or Tabler-outlined fallback
- No heavy shadow on cards; new work stays flat — 淡阴影 token only when Guideline requires legibility
- No gradient button or card backgrounds
- No multiple gradient words per screen
- No badges + chips on the same card
- No bounce easing; opacity/color only
- Do not mix icon kits on the same screen (manifest **or** Tabler, never both, never with Lucide/Heroicons/Feather)
- No orphan spacing — values must land on the 2-px rhythm (`layouts.md` §9)
- No invented column counts/gaps — pull from `layouts.md` §4 grid table
- No new radius values outside the 5-token vocabulary (`layouts.md` §8)

---

## 4. Workflow

1. **Declare fonts** — Inter, Roboto Mono
2. **Ask mode** — light or dark
3. **Load tokens** — `references/tokens.md`
4. **Pick layout** — `references/layouts.md`: page shell (§1) → hero variant (§2) → section header pattern (§3) → grid from the §4 table → filter/reader if needed (§5–6)
5. **Compose components** — `references/components.md` (§01–07 marketing blocks; **§08** production cards + `ui-*` primitives; §09–10 tags & customer cards)
6. **Manifests** — fetch `Icons.json` + `Images.json`; bind all photos to manifest URLs (required); icons from manifest or Tabler fallback
7. **Guideline** — open `Guideline.html` for visual QA; **§08** for console card gallery (`Scripts/ui.js` on CDN per `assets.md`)
8. **Review** — checklist below + `layouts.md` §18

---

## 5. Reference files

| File | Path | Scope |
|------|------|-------|
| Tokens | `<skill-dir>/references/tokens.md` | Color, type, radius, motion, width tokens (`--pt-*`) |
| Components | `<skill-dir>/references/components.md` | §01–10: heroes, buttons, model/pricing cards, **§08 gallery (53 cards + ui primitives)**, tags, customer cards |
| Layouts | `<skill-dir>/references/layouts.md` | Container layers, heading-on-white rule, heroes A–I, floor taxonomy, headers A/B/C, grids, sub-blocks, typography, card archetypes, data-page interaction, **§19 preview gallery** |
| Icons | `<skill-dir>/references/icons.md` | Manifest + Tabler fallback rules |
| CDN assets | `<skill-dir>/references/assets.md` | Image / icon manifest URLs |

---

## 6. Review checklist

- [ ] `@font-face` for Inter injected verbatim (acd-assets URL)
- [ ] Reset block injected right after `@font-face` — includes `em, i, cite, dfn, var, address { font-style: normal }`, list/link/button resets, `box-sizing: border-box`
- [ ] Light CTA: black rest, purple hover — not purple at rest
- [ ] ≤1 gradient text word per screen (plus allowed tier border rim)
- [ ] Cards and hero frames flat — no decorative shadow
- [ ] **Panel-as-card** blocks (recommended/cost/plan/feature/faq lists) are **borderless** outer + **typography + hairline** rows — no outer 1px stroke, no grey-bg inset sub-cards (`layouts.md` §11.6)
- [ ] Model primary vs secondary card backgrounds distinct
- [ ] `arrow-up-outlined` on primary CTA
- [ ] `flower_*` / `card_*` URLs from `Images.json` only; one floral hero per page
- [ ] Icons from `Icons.json` / `@ali/qwen-cloud-icons` first; Tabler outlined only as fallback
- [ ] 简洁平白：弱描边、无重阴影、无渐变按钮/卡片底
- [ ] Spacing values land on the 2-px rhythm; grids/radii pull from `layouts.md` vocabulary
- [ ] Heading sits on canvas/tinted floor — **never** on imagery (only exception: era closing CTA per `layouts.md` §2.3)
- [ ] Card chosen via the §11.4 decision tree (bordered vs borderless; A–H archetypes); padding + radius from §11.5
- [ ] Data-page (if applicable) passes the `layouts.md` §17.14 interaction-layer checklist
- [ ] Page passes the layout checklist in `layouts.md` §18
