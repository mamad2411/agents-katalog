---
name: data-viz
description: Charts and data visualization — library choice, chart accessibility, SSR/hydration concerns, dashboard performance, large datasets and data tables. Use when building or fixing charts, graphs, dashboards, KPI displays, or ANY data table (sortable/filterable/paginated tables of records or metrics included — a table is data viz). 日本語の依頼例:「グラフ/チャートを追加して」「ダッシュボード作って」「データテーブル」「一覧テーブル(ソート/フィルタ付き)」「可視化して」「KPI表示」。
---

# Data Visualization

## Library policy

- One charting library per repo. If the repo already has one installed, use it — do not add a second. Otherwise the default is **Recharts** for standard charts (bar/line/area/pie/scatter); escalate to **visx** only when a design needs lower-level control Recharts can't express, and to D3's math modules (scale/shape, React owning the DOM) only for genuinely bespoke visualizations. For plots that stay dense after aggregation, use **uPlot** (canvas). Each escalation is a deliberate, ask-first dependency choice, not a default.
- Charting libraries are heavy: the CLAUDE.md dependency ask-first rule applies, and the chart bundle should be code-split with the dashboard route, not in the shared bundle.

## Rendering & SSR

- Charts measure the DOM → render client-side. Next.js: `next/dynamic` with `ssr: false`, called from inside a Client Component wrapper — it errors in Server Components (see `nextjs` for pushing the boundary down). Astro: `client:only` island — the sanctioned exception to the astro skill's last-resort rule, since a DOM-measuring chart cannot SSR; the fixed `aspect-ratio` container below neutralizes its layout-shift risk. SPA: `React.lazy`.
- Reserve space while loading: fixed `aspect-ratio` container + skeleton — a chart popping in is CLS.
- Responsive sizing via the library's responsive container or one `ResizeObserver` — never window resize listeners.

## Accessibility — a chart is information, not decoration

- Every chart has a text alternative: a one-sentence summary (what the data shows, not "a bar chart") plus access to the underlying data — a visually-hidden or toggleable `<table>`. The table covers the data as presented (the decimated/aggregated series, or link the raw dataset as a download) — never one row per raw point. Screen-reader users get the data, not a canvas mystery.
- Color is never the only encoding: pair palette with direct labels, patterns, or shape (see `a11y`). Use a colorblind-safe categorical palette defined as tokens, not library defaults.
- Hover-only tooltips hide data from keyboard/touch users — ensure the values are reachable elsewhere (labels, the table, or focusable points).

## Performance

- > ~1,000 points: aggregate or decimate server-side first — nobody reads 50k DOM nodes, and SVG dies long before that. Canvas rendering for genuinely dense plots.
- Live data: update via the library's data prop with stable references; don't re-mount the chart per tick.
- Large tables are virtualized (e.g. TanStack Virtual) past a few hundred rows; sorting/filtering of big datasets happens server-side.

## Formatting & states

- All numbers/dates through `Intl.NumberFormat` / `Intl.DateTimeFormat` (locale-aware, handles compact notation) — never hand-built strings (see `i18n` for locale/currency rules).
- Timezones are explicit: store/transport UTC, render in a deliberately chosen zone, label it when ambiguous.
- Every chart designs its empty, loading, and error states — and each is a Storybook story (see `storybook`); "blank white rectangle" is not an empty state.
