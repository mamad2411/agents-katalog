---
name: kb-dataviz
description: Portable data visualization and dashboard patterns for Next.js 16+ + React 19 + Tailwind — chart selection matrix, dashboard audience pyramid (strategic/tactical/operational), Knaflic decluttering rules, preattentive attributes, storytelling structure, KPI card patterns, color-blind safe palettes, WCAG AA for charts. Recharts + TanStack Table already installed in the kit. Invoke when building dashboards, KPI pages, or data-heavy screens.
last-verified: 2026-04-23
---

# Dataviz — Dashboards & Charts

> Stack: Next.js 16+ + React 19 + Tailwind. Kit-shipped libs: **Recharts** (charts), **TanStack Table** (tables), **Framer Motion** (entrance motion). Todas instaladas — los ejemplos de este skill son copy-paste-runnables.

---

## 1. Dashboard architecture — the audience pyramid

Design the layout for the audience's operational level:

| Level           | Audience   | Focus                                     | Components                                    |
| --------------- | ---------- | ----------------------------------------- | --------------------------------------------- |
| **Strategic**   | Executives | High-level KPIs, MoM/YoY variation, goals | Big-number cards, sparklines, progress bars   |
| **Tactical**    | Managers   | Trends, comparisons, segmentation         | Line charts, stacked bars, heatmaps           |
| **Operational** | Analysts   | Granular data, exact numbers, exports     | Interactive tables (TanStack), filtered views |

A single dashboard usually mixes 2 adjacent levels — don't try to serve all three on one page.

---

## 2. Chart selection matrix

Pick the component based on the **data relationship**, not the mockup:

| Goal                           | Use                                    | ❌ Never                   |
| ------------------------------ | -------------------------------------- | -------------------------- |
| Single metric                  | Big number + sparkline + delta %       | Gauges, speedometers       |
| Trend over time                | Line chart / area chart                | Bars (if many data points) |
| Comparison (categorical)       | Horizontal bar chart                   | Pie / donut                |
| Composition (parts of a whole) | Stacked 100% bar / treemap             | 3D pie                     |
| Relationship / distribution    | Scatter plot / bubble chart            | Line chart                 |
| Dense cross-sectional data     | Heatmap (table with conditional color) | Spider / radar charts      |

> **Pie charts:** the human eye cannot estimate angles accurately. Use horizontal bars when you have ≥3 categories.

---

## 3. Declutter — Cole Nussbaumer Knaflic rules

Default chart configs are noisy. Actively disable everything that isn't data:

| Default noise          | Rule                                                            |
| ---------------------- | --------------------------------------------------------------- |
| Chart borders          | Remove                                                          |
| Chart background       | `transparent` — matches the page surface                        |
| Full grid              | Keep horizontal lines only, very light gray, dashed             |
| Axis lines             | Remove the visible axis line; keep tick labels only             |
| Legends                | Prefer **direct labels** on the line/bar, not a detached legend |
| Decimal precision      | Round up — `10K`, not `10,000.00`, unless precision matters     |
| 3D, shadows, gradients | Remove — they add noise without adding data                     |

### Recharts example (declutter defaults)

```tsx
<LineChart data={data} margin={{ top: 8, right: 16, bottom: 0, left: 0 }}>
  <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" vertical={false} />
  <XAxis dataKey="month" tickLine={false} axisLine={false} />
  <YAxis tickLine={false} axisLine={false} tickFormatter={(v) => `${v / 1000}K`} />
  <Tooltip content={<CustomTooltip />} />
  <Line
    type="monotone"
    dataKey="revenue"
    stroke="var(--color-primary)"
    strokeWidth={2}
    dot={false}
  />
</LineChart>
```

---

## 4. Preattentive attributes — focus attention

Humans process these visual cues before conscious attention. Use them deliberately:

| Attribute           | How to use                                                                |
| ------------------- | ------------------------------------------------------------------------- |
| **Size**            | Largest element = most important KPI (`text-4xl font-bold`)               |
| **Color hue**       | Neutral palette (gray/slate) for context; ONE brand color on the insight  |
| **Color intensity** | Saturation proxies value (heatmaps)                                       |
| **Position**        | Top-left is the most valuable real estate — most critical KPI lives there |

### The "Where Are Your Eyes Drawn?" test

> Squint at the screen. What's the brightest, most prominent element?
>
> - If it's the data insight → the design is right.
> - If it's a border, a logo, or a colorful chrome element → the design is wrong.

---

## 5. Storytelling structure — narrative arc

A dashboard page should read like a story:

| Step           | Question                  | UI element                                                  |
| -------------- | ------------------------- | ----------------------------------------------------------- |
| **Context**    | "What are we looking at?" | Page title, subtitle, date range filter                     |
| **Conflict**   | "What changed?"           | Big-number KPIs with red/green delta vs target/prior period |
| **Resolution** | "Why did it change?"      | Breakdown charts + drill-down table at the bottom           |

Don't open with a table. Open with the top-line metric + the delta — then let the user drill down.

---

## 6. KPI card pattern

A premium KPI card shows **3 things**: the number, the context, and the trend.

```tsx
<div className="bg-card rounded-xl border p-6 shadow-sm">
  <h3 className="text-muted-foreground text-sm font-medium">Revenue (August)</h3>
  <div className="mt-2 flex items-baseline gap-2">
    <span className="text-foreground text-3xl font-semibold">€613.5k</span>
    <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-sm font-medium text-emerald-600 dark:bg-emerald-950">
      +15.2% YoY
    </span>
  </div>
  <p className="text-muted-foreground mt-1 text-sm">Target: €660.0k</p>
</div>
```

**Checklist:**

- [ ] Label (what the metric measures)
- [ ] The number, formatted (no trailing decimals for large values)
- [ ] Delta vs a comparison (previous period, target, prior year)
- [ ] Color semantics: green = improvement, red = regression. Paired with ↑/↓ icon (color-blind).
- [ ] Optional sparkline for trend shape

---

## 7. Tooltip UX

Default chart tooltips are ugly. Always customize:

- Include **date/category + metric + comparison** (vs target or prior period)
- Consistent number formatting (same format as the chart axis)
- Opaque background, high-contrast text (WCAG AA)
- Tooltip anchored to data point, not to cursor (avoids jitter)

---

## 8. Dashboard state management

| Scope              | Mechanism                                                           |
| ------------------ | ------------------------------------------------------------------- |
| Global filters     | URL query params (`?region=eu&year=2026`) — shareable, bookmarkable |
| Micro-interactions | `useState` (hover, toggle chart view)                               |
| Initial data       | Server Components + Server Actions — no client-side waterfalls      |

Rationale: dashboards are frequently shared ("check this link"). URL-backed filters make state portable. This repo uses `useSearchParams` directly (no `nuqs` dep) — for server-paginated data, `useServerTableState` already syncs `?sort=&dir=&page=&limit=` (see `kb-ui`).

---

## 9. Accessibility — non-negotiable

### Color-blind safety

- **Never use color alone** to convey meaning — pair with shape, pattern, icon, or label
- **Avoid red/green only** combinations. Use blue/orange or blue/red for diverging
- Test palettes with Chrome DevTools' vision emulation or Coblis

### Recommended safe palettes

| Use case             | Primary                          | Secondary        | Danger        |
| -------------------- | -------------------------------- | ---------------- | ------------- |
| Diverging (good/bad) | Blue `#4E79A7`                   | Orange `#F28E2B` | Red `#E15759` |
| Sequential (one hue) | Light → dark blue ramp           | —                | —             |
| Categorical (≤6)     | Tableau 10 or IBM Design palette | —                | —             |

### WCAG compliance

- **Contrast:** text on charts meets AA (4.5:1 body, 3:1 large)
- **Focus states:** interactive elements (tooltips, filter toggles, legend items) have visible focus rings
- **Screen readers:** every chart has `aria-label` or an accessible data-table alternative
- **Reduced motion:** respect `prefers-reduced-motion` — disable chart entrance animations

---

## 10. Dashboard art direction — the 4 types

The art direction varies with the audience. Pick one per dashboard:

| Type           | Characteristics                                                |
| -------------- | -------------------------------------------------------------- |
| **Executive**  | Fewer KPI blocks, more breathing room, summary-first, premium  |
| **Operator**   | Denser layout, stronger controls, stable navigation, task flow |
| **Analytical** | Charts + filtering prominence, comparative structures          |
| **Narrative**  | Insights, summaries, guided interpretation over raw controls   |

> For the full picking process (skin family + motion profile), load `doc-visual-direction` during the design phase.

### Composition anti-patterns

- Too many equal-weight cards (no hierarchy)
- Every module using the same card style (monotony)
- Weak top-of-page structure (user can't orient)
- Charts dropped in without narrative hierarchy
- Tables that look like raw admin leftovers
- Filters floating without strong grouping

---

## 11. Library recommendations

### First choice — shadcn-compatible stack

| Purpose             | Library               | Why                                                                 |
| ------------------- | --------------------- | ------------------------------------------------------------------- |
| Standard charts     | **Recharts**          | First-class shadcn/ui chart wrapper available; theme-aware          |
| Interactive tables  | **TanStack Table v8** | Headless — composes with our existing table hooks (`useTableState`) |
| Entrance animations | **Framer Motion**     | Already installed                                                   |

### Alternatives (evaluate per project)

| Library      | Use case                                             |
| ------------ | ---------------------------------------------------- |
| **Visx**     | Custom D3-based visualizations, fine-grained control |
| **Tremor**   | Fastest prototyping of Tailwind-native dashboards    |
| **Ag-Grid**  | Enterprise-grade grids (when TanStack isn't enough)  |
| **Chart.js** | Lightweight canvas-based charts                      |

> 🛑 **Dependency install rule:** Recharts y TanStack Table ya están instaladas. Cualquier lib adicional (Visx, Tremor, Ag-Grid, Chart.js) requiere propuesta + justificación antes de `pnpm add` (`CODING.md §7`).

---

## 12. Checklist — before closing a dashboard task

- [ ] Chart type matches the data relationship (see §2)
- [ ] Declutter pass applied (§3): no full grid, no axis lines, no chart borders
- [ ] Preattentive attributes used to highlight **one** insight per chart
- [ ] Every KPI card shows number + context + trend (§6)
- [ ] Tooltips customized — no default library chrome
- [ ] Filters use URL state, not local state
- [ ] Color-blind safe palette, color paired with shape/label
- [ ] WCAG AA contrast verified
- [ ] `prefers-reduced-motion` respected — no entrance animations when reduced
- [ ] Screen-reader alternative (aria-label or data table)

---

_Cross-reference: `kb-ui` for table hooks (`useTableState` / `useServerTableState`), URL state (`useSearchParams`), and form/filter patterns. `kb-design-system` for token discipline across dashboard surfaces. `doc-visual-direction` for picking the dashboard type and motion profile during the design phase._
