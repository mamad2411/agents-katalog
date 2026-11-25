---
name: building-html-presentations
description: Use when the user wants to build a presentation, deck, slides, pitch, readout, or interactive report from data work — exploratory analysis, dashboards, business plans, proposals. Covers as-code HTML formats (reveal.js deck, flexible scrollable deck, interactive site, consulting-style PDF, Marp) plus a chart cookbook, how to choose between them, and ready-to-edit starters. Default engine is reveal.js. For native editable PowerPoint use the generating-pptx skill.
---

# Skill: building-html-presentations

Build presentations **as code** so they are versionable, diffable, and reproducible. This skill
covers when to use each format and gives starters you copy and fill with real content. Pair it
with `applying-visual-identity` to make the output on-brand.

## Pick the format first

| Output | Use when | Engine | Export |
|---|---|---|---|
| **Slide deck** | Live readout / meeting; linear narrative, fixed canvas | **reveal.js** (default) | HTML, PDF (`?print-pdf`) |
| **Flexible / scrollable deck** | Slides that hold more than one screen and need in-slide scroll + buttons to switch visuals | custom vanilla JS (`flex-deck.html`) | HTML |
| **Interactive site** | Self-serve exploration; one long scrolling page with anchors | single static HTML page (`interactive-site.html`) | HTML |
| **Designed report PDF** | Polished consulting-style document (action titles, exhibits) | HTML print template (`report-pdf.html`) | PDF (print) |
| **Quick handout PDF/PPTX** | Plain Markdown deliverable, no custom design | **Marp** (Markdown → PDF/PPTX) | PDF, PPTX |
| **Editable PowerPoint** | The deliverable must be a native, editable `.pptx` | → use the `generating-pptx` skill (python-pptx) | PPTX |

Default to **reveal.js**: most mature, pure HTML/CSS (easy theming from `DESIGN.md`), and it
exports to PDF — so one source covers deck + site + print. Reach for **Marp** only when the
deliverable is fundamentally a document (Markdown-only, clean PDF/PPTX, no interactivity).
**Slidev** is a fine choice for fully technical audiences already on Node/Vue — mention it,
don't default to it.

## Working order
1. **Find the brand.** Look for a `DESIGN.md` in the project root. If present, load
   `applying-visual-identity` and map its tokens to CSS variables. If absent, offer to scaffold
   one (don't invent a brand silently) and use the neutral defaults in the starter meanwhile.
2. **Pick the format** from the table above and say which and why. A native `.pptx` that must be
   editable in PowerPoint → `generating-pptx`.
3. **Story before charts.** Know the audience (exec → fewer slides, takeaway titles, no code;
   technical → allow detail/appendix). Agree the storyline (5–9 beats) before writing HTML: lead
   with the conclusion (BLUF), then evidence, then "so what / next". Use `data-story-outline.md`.
4. **Build from a starter** (`templates/`), drop in real numbers and charts, keep it
   **self-contained** (works offline; pin CDN versions or vendor the files).
5. **Export** if needed (see the export note below).

## Exporting (incl. PowerPoint)
- **reveal.js → PDF:** open the deck with `?print-pdf` appended, then print → Save as PDF. This is
  the clean, high-fidelity export.
- **reveal.js → PPTX:** there is **no native, editable** path. If a `.pptx` file is required, use
  **Marp** (`marp deck.md --pptx`) — but note each slide becomes an **image** (not editable text).
  A PDF→PPTX converter is equally image-based. For truly editable native PPTX, generate it
  separately (e.g. `python-pptx`); tell the user it's a different workflow, not an HTML export.
- **Marp → PDF / PPTX:** `marp deck.md --pdf` or `--pptx`.
- **Interactive site:** ship the HTML file itself (or host it); it isn't meant for PDF/PPTX.

## Starters (in `templates/`)
- `reveal-deck.html` — a sophisticated, single-file **data-dashboard deck system** (dark theme,
  brand tokens in `:root` mapped from `DESIGN.md`). Ships reusable layout primitives:
  - **Cover** with KPI grid + stat chips + CTA bar; **section dividers**.
  - **2×2 dashboard panels** mixing charts and narrative with colored keyword highlights.
  - **Ranking bars** (CSS, value + ±pp delta, semantic colors); **heatmap matrix** with a
    score-band color scale and metric **toggle pills**; **quote cards** with category tags.
  - **Custom chrome**: zero-padded `01 / 07` counter, top progress bar, section tag, and a
    dots + prev/next nav wired to the reveal.js API.
  - **Charts**: pure-CSS bars for rankings + **ECharts** (pinned) for line/combo charts.
  Copy it, swap the tokens, replace the demo content. Reach for the panel/bar/heatmap classes
  rather than hand-rolling layout each time.
- `flex-deck.html` — a **flexible, scrollable deck** (no framework, no fixed aspect ratio): each
  slide is a full-width sub-page that can be **taller than the screen and scrolls vertically**,
  while ← → moves between slides. Includes **dynamic toggle buttons** that swap the visual in place
  (chart series, and chart ↔ table). Use when a deck slide carries dashboard-density content.
- `interactive-site.html` — a single-file **scrolling report site** (not slides): sticky nav with
  active-link highlight, reading-progress bar, hero + KPI band, scroll-reveal sections, a sticky
  data table, and ECharts (line + donut). Same tokens as the deck. Use for self-serve exploration.
- `report-pdf.html` — a **consulting-style report** (McKinsey/Deloitte feel) built for PDF export:
  print-first A4, light theme, running header/footer chrome, a **contents page**, **full-sentence
  action titles**, an exec summary (key findings + takeaways), an **"at a glance" small-multiples**
  page, 10 numbered **Exhibits** with varied charts (combo, grouped bar, scatter w/ quadrant lines,
  waterfall bridge, donut, gauge, CSS bars), **insight callouts** + **margin notes**, a data-bar
  table, and a recommendations table (owner/timeline/measure). Export via Chrome Print → Save as
  PDF (A4, margins none, background graphics on).
- `charts-reference.html` — a **chart cookbook**: a live gallery of ~18 chart patterns (ECharts +
  CSS-only) — line, area, multi-line, combo, bar, grouped, stacked, horizontal, scatter, bubble,
  pie/doughnut, gauge, radar, heatmap, treemap, funnel, boxplot, waterfall, sparkline. Each card
  names the type and when to use it. **Consult this to pick a chart and copy its config** into any
  template, instead of defaulting to line + bar every time.
- `marp-deck.md` — Markdown deck for a quick, plain PDF/PPTX deliverable (no custom design).
- `data-story-outline.md` — fill-in narrative skeleton for analyses, EDA, and business plans.

All HTML starters use a generic **sales review** as demo content — replace it with your own.

## Charts & data
- **Match the chart to the question** — see `templates/charts-reference.html` for the full palette
  and a "pick by question" guide (trend → line/area; compare → bar; composition → stacked;
  correlation → scatter; part-of-whole → pie; KPI vs goal → gauge; matrix → heatmap; etc.).
  Don't reach for the same line+bar by reflex.
- Use **ECharts** (pinned CDN, SVG renderer) for rich charts; pure-CSS bars/heatmap when it must
  print or stay JS-free. Prefer SVG for PDF targets.
- Every data slide states **source, grain, date range, filters**. Never invent numbers — mark
  unknowns `TODO`.

## Data storytelling rules
- **Title = insight.** "Revenue fell 12% in EMEA", not "Revenue by region".
- **One idea per slide.** Move supporting detail to an appendix section.
- **Label the source & grain** on any data slide (table, date range, filters). Trust is the point.
- **Never fabricate data.** Use only numbers the user provides or that exist in the repo; mark
  placeholders explicitly as `TODO`.

## Rules
- Keep it self-contained and offline-capable; pin versions, don't rely on live network at present time.
- Accessibility: real text (not images of text), sufficient contrast, logical heading order.
