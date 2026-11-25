---
name: makino-data-slides
invocation: user
description: "Data Slides — Turn Excel/data analysis into investor-grade HTML slide cards with narrative. ECharts + static cards, Playwright screenshot."
version: "5.2.2"
last_updated: "2026-09-25"
---

# Data Slides — Data tells the story

You turn data analysis results into investor-grade HTML slide cards.
Each slide is a 1080×720 card combining a **data visualization** with a **narrative takeaway** — designed to be screenshot and embedded in articles or shared standalone.

NOT a chart tool. NOT a presentation tool. This is: **Excel data → analysis conclusions → visual cards with opinions.**

## What This Is (and Isn't)

| Need | Use this? | Use instead |
|------|-----------|-------------|
| Single chart (line/bar/pie) | No | Any charting library |
| Article → navigable slide deck | No | [`/content-to-html`](https://github.com/makinotes/makino-content-to-html) |
| Cover image for article | No | An image generator |
| **Data analysis → multi-slide cards with narrative, embedded in articles** | **Yes** | — |

The key difference from a plain chart: every card here has a **takeaway** (an opinion/conclusion), not just a visualization. It's "chart + judgment" as a unit.

## Input

Primary input: **Excel/CSV with structured data** (scores, rankings, time series, category breakdowns).

Also accepts:
- JSON data files
- Markdown with inline data points (tables, bullet lists with numbers)
- Verbal description of data + conclusions (least ideal, most manual)

The skill reads the data, proposes analysis angles, and generates cards. User provides or confirms the narrative direction.

**Feedback notice**: Every time the skill starts, print this line before any output:

```
💬 使用问题或建议 → 飞书群/公众号「马奇诺」后台留言（详见 README）
```

## Commands

| Command | What it does |
|---------|-------------|
| `/makino-data-slides` | Interactive: ask for data + narrative, generate slides |
| `/makino-data-slides <path>` | Generate slides from a data file (Excel/CSV/JSON/markdown) |

## Slide Anatomy (5-layer structure)

Every slide follows this exact structure, top to bottom:

```
┌─────────────────────────────────────────────┐
│ hdr: padding 18px 36px 0                page│  ← ~50px
│ takeaway: margin 6px 36px 0                 │  ← ~32px
│                                              │
│ body: padding 8px 36px 0, explicit height    │  ← ~570-590px
│   charts (ECharts) / cards / tables / grids  │
│   justify-content: space-between             │
│                                              │
│ ft: padding 6px 36px 10px                    │  ← ~28px
└─────────────────────────────────────────────┘
```

Total: 1080×720px fixed.

### Spacing 铁律（从已验证的 charts_v4.html 提取）

```css
.slide .hdr       { padding: 18px 36px 0 }       /* 紧凑头部 */
.slide .takeaway  { margin: 6px 36px 0 }          /* 紧贴标题 */
.slide .body      { padding: 8px 36px 0 }         /* 最小顶部留白 */
.slide .ft        { padding: 6px 36px 10px }       /* 底部克制 */
```

### Body 填充策略（关键）

**禁止 `flex:1` + 固定 gap 组合** — 会导致内容堆在顶部、底部留白过多。

正确做法：
1. body 设显式高度（根据 hdr/takeaway/ft 实际高度计算）
2. 用 `justify-content: space-between` 或 `space-evenly` 让内容均匀撑满
3. chart 容器用 `flex:1` 吃掉剩余空间，其他元素 `flex-shrink:0`

```css
/* 典型 body 高度计算 */
.body { height: 596px; display: flex; flex-direction: column; justify-content: space-between; }
/* chart 吃剩余 */
#chart { flex: 1; width: 100%; }
/* 固定元素不缩 */
.stat-row { flex-shrink: 0; }
```

## Visual System

### Background & Shadow
```css
body { background: #1a1a2e; }                     /* 深色背景衬托白卡 */
.slide { box-shadow: 0 8px 32px rgba(0,0,0,.25); border-radius: 6px; }
```

### Colors
```js
const C = {
  blue:   '#1e40af',  // primary, deep layer
  blueL:  '#93c5fd',  // blue light (secondary bars)
  blueP:  '#dbeafe',  // blue pale (background)
  red:    '#dc2626',  // alert, negative
  green:  '#059669',  // positive, action layer
  purple: '#7c3aed',  // accent (open source etc)
  amber:  '#d97706',  // warning, interpretation layer
  gray:   '#9ca3af',  // neutral, news layer
  dark:   '#1e293b',  // text primary (body)
  mid:    '#475569',  // text secondary
  light:  '#64748b',  // text tertiary
  grid:   '#f1f5f9',  // chart grid lines
  axis:   '#e2e8f0',  // chart axis lines
};
```

### Typography

| 元素 | 字号 | 字重 | 颜色 | 备注 |
|------|------|------|------|------|
| Font family | — | — | — | `-apple-system, 'PingFang SC', 'Helvetica Neue', sans-serif` |
| Title (h2) | 21px | 800 | `#0f172a` | margin-bottom 2px |
| Subtitle (.sub) | 12px | 400 | `#64748b` | max-width 720px |
| Page number | 11px | 600 | `#94a3b8` | letter-spacing 1px, 格式 `01 / 08` |
| Takeaway | 13px | 600 | `#991b1b` | gradient bg, border-left 3px solid #dc2626, border-radius `0 6px 6px 0` |
| Body text | 11-12px | 400 | `#334155` | line-height 1.6 |
| Footer | 11px | 400 | `#64748b` | letter-spacing .3px, centered |
| Hero number (.n) | 32-40px | 800 | #fff | 40px for emphasis |
| Hero label (.l) | 10px | 400 | #fff | opacity .8 |
| Hero detail (.d) | 9px | 400 | #fff | opacity .5 |
| Stat value (.v) | 24px | 800 | per-color | `.v.blue` / `.v.red` etc |
| Stat key (.k) | 10px | 400 | `#64748b` | margin-top 2px |
| Insight number (.n) | 20px | 800 | per-color | |
| Insight label (.l) | 9px | 400 | `#64748b` | |
| Finding title | 14px | 700 | per-color | with page ref `→ P3` in 10px #94a3b8 |
| Finding text | 12px | 400 | `#334155` | line-height 1.6 |
| Section heading (in body) | 13px | 700 | `#334155` | text-align center, margin-bottom 6px |

### Takeaway 精确样式
```css
.slide .takeaway {
  margin: 6px 36px 0;
  font-size: 13px;
  font-weight: 600;
  color: #991b1b;
  padding: 8px 14px;
  background: linear-gradient(90deg, #fef2f2, #fff);  /* 渐变，不是纯色 */
  border-left: 3px solid #dc2626;
  border-radius: 0 6px 6px 0;
  flex-shrink: 0;
}
```

### Watermark
```css
.slide::before {
  content: '{BRAND}  {BRAND}  ...';  /* Replace {BRAND} with your brand name -- 40 repeats, double-space separated */
  position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  z-index: 999; pointer-events: none;
  font-size: 16px; font-weight: 600;
  color: rgba(0,0,0,0.03);
  letter-spacing: 20px; line-height: 80px;
  transform: rotate(-25deg); transform-origin: center center;
  word-break: break-all; overflow: hidden; padding: 0 40px;
}
```

### Card Components

| Component | CSS | Key specs |
|-----------|-----|-----------|
| Hero card (.hc) | `background:linear-gradient(135deg,#1e3a5f,#1e40af)` | border-radius 10px, padding 16px 12px (or 24px 14px for emphasis) |
| Hero card variant | `background:linear-gradient(135deg,#059669,#047857)` | green variant for positive metrics |
| Stat box (.stat-box) | `background:#f8fafc; border:1px solid #e2e8f0` | border-radius 8px, padding 10px 14px, text-align center |
| Insight card (.ic) | `background:#f8fafc; border:1px solid #e2e8f0` | border-radius 8px, padding 10px 8px |
| Layer bar (.lbar) | `display:flex; overflow:hidden` | height 24px (or 32px), border-radius 5px, font 10px 700 white |
| Layer legend (.lleg) | `display:flex; gap:14px` | font-size 9px, color `#64748b`, colored square `8px` |
| Mini table (.mini-tbl) | `border-collapse:collapse` | th: `background:#1e3a5f` (深蓝), td: padding 4px 8px |
| Finding card (2×2 grid) | `grid-template-columns:1fr 1fr; gap:12px` | border-radius 8px, padding 14px 16px, border-left 3px |
| Finding badge (.fb) | `20px×20px; border-radius:4px` | background per-color, 10px 700 white |
| Progress bar | Pure HTML div | 10px height, border-radius 5px, bg `#e2e8f0` |
| Info callout | colored bg + border | border-radius 10px, padding 26px 20px |
| Summary card row | `display:flex; gap:6px` | border 1px, border-radius 6px, padding 5px 8px |

### Chart Types (ECharts)

Common axis config:
```js
const bA = {
  axisLine:  { lineStyle: { color: C.axis } },
  splitLine: { lineStyle: { color: C.grid } },
  axisLabel: { fontSize: 11, color: C.light }
};
```

| Chart | When to use | Key settings |
|-------|-------------|-------------|
| Scatter/Bubble | Distribution, 2D | symbolSize by volume, opacity .75, border white 1.5px, `labelLayout:{hideOverlap:true}` |
| Grouped Bar | Time comparison | barCategoryGap 25%, barGap 5%, borderRadius `[3,3,0,0]` |
| Stacked Bar | Composition | stack prop, label position 'right' shows total, borderRadius `[0,4,4,0]` on last segment |
| Horizontal Bar | Ranking | barWidth 18-20px, borderRadius `[0,5,5,0]`, label right bold |
| Progress Bar | Percentage | **Pure HTML**, no ECharts. 10px height, border-radius 5px |
| Proportion Bar | Part-of-whole | **Pure HTML** flex-based, colored segments |
| Zone Scatter | Quadrant/区域 | markArea with transparent fill + markLine dashed thresholds + graphic text zone labels |

ECharts grid defaults:
```js
grid: { left: 50, right: 30, top: 36, bottom: 20 }  // top 留 legend 空间
animation: false  // ALWAYS disable for screenshot
legend: { top: 4 }  // 统一放顶部，禁止 bottom（会和 bar label 重叠）
```

标注线/标注文字：
```js
// 正确：用 markLine（在 SVG 内渲染，不被 watermark z-index 遮挡）
markLine: {
  silent: true, symbol: 'none',
  lineStyle: { type: 'dashed', width: 1 },
  data: [
    { xAxis: '02-12', lineStyle: { color: '#dc2626' },
      label: { formatter: '2/12 事件', fontSize: 10, color: '#dc2626', fontWeight: 600, position: 'insideStartTop' }}
  ]
}
// 错误：graphic 硬编码像素 — 位置不准 + 被 watermark 遮挡
```

Scatter zone labels (graphic watermark style):
```js
graphic: [
  { type:'text', left:'45%', top:'12%',
    style: { text:'深度层', fontSize:28, fontWeight:900, fill:'rgba(30,64,175,0.10)' }},
  { type:'text', left:'43%', top:'20%',
    style: { text:'4个号 · 81篇', fontSize:14, fontWeight:700, fill:'rgba(30,64,175,0.08)' }}
]
```

## Execution

### Phase 0: Version check

```bash
curl -s https://raw.githubusercontent.com/makinotes/makino-data-slides/master/SKILL.md | head -6
```

Extract `version:` from remote, compare with the local frontmatter `version`.
If remote > local, show before proceeding:

```
[UPDATE] makino-data-slides v{remote} available (you have v{local}).
Update now? Run: cd ~/.claude/skills/makino-data-slides && git pull
```

If versions match or curl fails: skip silently.

### Phase 1: Understand the data

1. Read the data source (JSON/CSV/markdown/user description)
2. **Output Analysis Intent Table** (user must confirm before proceeding):

```
| Sheet/Data | Analysis Type | Chart Type | Layout | Magnitude Check |
|------------|--------------|------------|--------|-----------------|
| Sheet 1: 搜索vs大盘 | Cross-group comparison | Grouped Bar (dual Y-axis: 5x diff) | layout-split | max 2497万 vs 508万 = 4.9x → dual Y |
| Sheet 2: 逐日明细 | Time series + event | Line (dual Y-axis) + markLine | layout-chart-full | same issue, dual Y |
| Sheet 3: 留存分析 | Group comparison (dense) | HTML Table (too many cells for chart) | layout-split | N/A |
```

3. **Output Data Preprocessing Plan** (user must confirm):

```
| Column | Raw Unit | Display Unit | Transform | Decimal |
|--------|----------|-------------|-----------|---------|
| 大盘DAU | 个 (24970000) | 万 (2497) | ÷10000 | 0 |
| 春节跌幅 | decimal (-0.48) | % (-48%) | ×100 | 1 |
| 留存率 | decimal (0.332) | % (33.2%) | ×100 | 1 |
```

4. **Choose style preset**: Ask user which preset (default: investor). Read `STYLE_PRESETS.md`.
5. Propose slide outline with narrative order: overview → comparison → trend → breakdown → conclusion
6. Get user approval on ALL of the above

### Phase 2: Generate HTML

1. **Read `base.css`** — embed EXACTLY as-is in `<style>` block. Do NOT modify or add inline styles that override it.
2. **Read `STYLE_PRESETS.md`** — embed chosen preset's CSS overrides AFTER base.css
3. **Read `CHART_GUIDE.md`** — use the matching chart template for each slide's analysis goal. Check magnitude rules.
4. **Body height calculation (MANDATORY per slide)**:
   ```
   total = 720px
   hdr = 50px (18px padding-top + ~32px content)
   takeaway = 38px (6px margin + 8px padding × 2 + 13px text)
   ft = 28px (6px + 10px padding + 11px text)
   body_available = 720 - 50 - 38 - 28 = 604px
   body_padding_top = 8px
   body_usable = 604 - 8 = 596px

   → Set .body height to 596px explicitly
   → Allocate: chart_height + stat_row_height + margins = 596px
   → Use layout class from base.css, NOT inline flex/grid
   ```
5. **ECharts 加载策略（双保险）**：
   - 首选：内联 ECharts。检查本地缓存 `/tmp/echarts.min.js`，存在则读取内容嵌入 `<script>` 标签
   - 如果本地缓存不存在，先下载：`curl -sL "https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js" > /tmp/echarts.min.js`
   - 内联后 HTML 文件 ~1MB，但 file:// 直接打开也能渲染图表
   - 同时保留 CDN fallback：`<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>`
   - 加载失败提示：如果 `typeof echarts === 'undefined'`，在图表容器内显示错误信息和 HTTP server 启动命令
3. Each slide is a `<div class="slide">` with the 5-layer structure
4. Charts render via `DOMContentLoaded` with 50ms delay
5. **每个 slide 的 body 必须显式计算高度**，用 space-between 撑满

### Phase 3: Review and iterate

1. **必须用 HTTP server 打开**（即使内联了 ECharts，部分浏览器仍可能限制 file://）：
   ```bash
   cd "$(dirname "$HTML_PATH")" && python3 -m http.server 8766 &
   open "http://localhost:8766/$(basename "$HTML_PATH")"
   ```
2. Screenshot each slide for user review
3. Iterate on feedback: spacing, data accuracy, readability

### Phase 4: Screenshot

1. Use Playwright to screenshot each slide at native 1080×720
2. Save to user-specified directory
3. Naming convention: `slide_{N}_{slug}.png`

```javascript
// Playwright screenshot pattern
const slide = page.locator('.slide').nth(i);
await slide.scrollIntoViewIfNeeded();
await page.waitForTimeout(500);
await slide.screenshot({ path: outputPath, type: 'png' });
```

## CSS & Style

**CSS template and chart guide are in separate files** — Read them and embed into generated HTML.

| File | Purpose | When to Read |
|------|---------|-------------|
| `base.css` | Layout structure, components (shared across all presets) | Always — embed in every HTML |
| `STYLE_PRESETS.md` | 3 color themes (investor/corporate/dark) | Phase 1 — user picks preset |
| `CHART_GUIDE.md` | Chart selection by analysis goal + ECharts templates | Phase 2 — pick chart type per slide |

## Data Accuracy Rules

- Every number on a slide must trace back to the source data
- Cross-check totals: if parts shown, verify they sum correctly
- If a number appears on multiple slides, it must be identical everywhere
- Footer can provide context but must not introduce new data claims
- When data is approximate, say so (e.g. "~40%" not "40%")

## File Structure

Output: single self-contained HTML file.
- All CSS inline in `<style>` block
- All JS inline in `<script>` block
- Only external dependency: ECharts CDN
- No images, no external CSS, no build step

## Error Warnings

- Do NOT use `animation: true` in ECharts — screenshots capture mid-animation
- Do NOT use `flex:1` + fixed `gap` on body — 会导致底部留白过多。用显式高度 + `space-between`
- Do NOT mix `gap` with `justify-content: space-evenly` — pick one spacing strategy
- Do NOT forget `overflow:hidden` on `.slide` — content must not escape the card
- Test data label overlap on dense charts — use `labelLayout:{hideOverlap:true}`
- Do NOT use `padding-top:16px+` on body — 最大 8px，紧凑是核心
- Do NOT use pure `#fef2f2` for takeaway bg — 必须是 `linear-gradient(90deg,#fef2f2,#fff)`
- Do NOT use `#1e293b` for title — title 用 `#0f172a`，比 body text 更深
- Page number 格式 `01 / 08` — 零填充，斜杠两侧有空格
- Do NOT put `legend` at `bottom` when chart has `label` on bars — legend 和 bar label 重叠。**legend 统一放 top**，grid.top 相应下移（如 top:36）
- Do NOT use `graphic` 画标注线/文字 — watermark `::before` z-index:999 会遮挡 graphic 层。**标注线必须用 `markLine`**（xAxis/yAxis 值定位，在 SVG 内渲染不受 z-index 影响），标注文字用 markLine 的 `label` 属性
- Do NOT rely on CDN `<script src>` alone — file:// 协议下浏览器会静默拦截外部脚本。**必须内联 ECharts + CDN fallback + 错误提示三层保险**
- Do NOT use `open file:///` 打开含 ECharts 的 HTML — **必须用 `python3 -m http.server` + `http://localhost`**
