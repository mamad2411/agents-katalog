---
name: frontend-charts
description: Use when picking a React chart lib — Recharts vs Visx vs Tremor vs ECharts. Decision matrix, common patterns, performance for large datasets, accessibility.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  languages: [react, typescript]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [react, typescript, frontend-tailwind, frontend-design-essentials, ux-essentials, ux-wcag-a11y]
---

# Frontend Charts

**Iron Law: pick by data shape and customization budget, not by GitHub stars. For 95% of dashboards, Recharts is the right default. Drop to Visx only when you need primitives Recharts can't express. Disable animation past ~500 points or your UI tanks.**

**Versions:** Recharts `3.x` · Visx `3.x` · Tremor `3.x` · Apache ECharts `5.x` · D3 `7.x` — _Recharts v3 (2025) added React 19 support, dropped IE polyfills, switched to ESM-first build. Visx is in slow steady-state; the d3 underneath does the heavy lifting. Tremor v3 dropped its own primitives and now wraps Recharts + Radix._

## Decision matrix

| Library                                  | Pick when                                                                                            | Avoid when                                                                                            |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| **Recharts**                             | composable React components; standard chart types (line/bar/area/pie/scatter); <2k points per series | hardcore custom interactions; >10k points; non-cartesian (sankey, force, sunburst — uses are limited) |
| **Visx**                                 | full control; novel viz; d3 scales + React rendering; large or non-standard data                     | you want it fast — Visx is verbose by design                                                          |
| **Tremor**                               | dashboard speed-run with Tailwind; KPI cards + simple charts ship in an hour                         | you need a chart Tremor doesn't ship; brand UI very far from Tailwind defaults                        |
| **Apache ECharts** (`echarts-for-react`) | massive feature set (heatmaps, graph, geo, parallel, treemap), large datasets, perf                  | you want React-idiomatic API — ECharts is option-object configured                                    |
| **D3 raw**                               | one-off bespoke viz (force graph, custom physics)                                                    | a typed chart library would do                                                                        |
| **Visx + d3-force / d3-hierarchy**       | network, tree, treemap with React control                                                            | a static layout would suffice                                                                         |
| **Tanstack Charts**                      | (in alpha; ignore for prod)                                                                          | always (for now)                                                                                      |

## Recharts — the default

```tsx
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

<div style={{ width: "100%", height: 300 }}>
  <ResponsiveContainer>
    <LineChart data={series} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="ts" tickFormatter={fmtDate} />
      <YAxis />
      <Tooltip content={<CustomTooltip />} />
      <Line dataKey="value" stroke="var(--color-action)" dot={false} isAnimationActive={false} />
    </LineChart>
  </ResponsiveContainer>
</div>;
```

| Recharts pattern                                   | Why                                                                            |
| -------------------------------------------------- | ------------------------------------------------------------------------------ |
| `<ResponsiveContainer>` parent has explicit height | Without explicit pixel height it renders 0 and shows nothing                   |
| `isAnimationActive={false}` past ~500 points       | Animation re-renders every frame across the path; chokes                       |
| `dot={false}` for lines past ~100 points           | Each dot is an SVG circle                                                      |
| Custom `<Tooltip content={fn}>` over default       | Defaults look generic; custom is one component                                 |
| Memoize `data` prop                                | Recharts reconciles on every parent render unless data is referentially stable |
| `dataKey` over `dataKey={(d) => ...}`              | Function accessors disable some path optimizations                             |

**Color from CSS variables**: pass `stroke="var(--color-action)"` so theme switches don't require a chart re-render. Pair with `Skill(frontend-design-essentials)` tokens.

## Recharts — large datasets

| Points | Strategy                                                                        |
| ------ | ------------------------------------------------------------------------------- |
| <500   | default; animation on if you want                                               |
| 500–2k | animation off; `dot={false}`; consider `syncMethod="value"` for linked charts   |
| 2k–10k | downsample on the data side (LTTB algorithm) before passing to the chart        |
| >10k   | switch to ECharts (canvas-rendered) or roll a canvas component with Visx scales |

SVG is the bottleneck — Recharts emits one path per series and one circle per point if dots are on.

## Visx — composability when you need it

```tsx
import { ParentSize } from "@visx/responsive";
import { scaleLinear, scaleTime } from "@visx/scale";
import { LinePath } from "@visx/shape";

<ParentSize>
  {({ width, height }) => {
    const xScale = scaleTime({ range: [0, width], domain: extent(data, (d) => d.ts) as [Date, Date] });
    const yScale = scaleLinear({ range: [height, 0], domain: [0, max(data, (d) => d.value)!] });
    return (
      <svg width={width} height={height}>
        <LinePath data={data} x={(d) => xScale(d.ts)} y={(d) => yScale(d.value)} stroke="currentColor" />
      </svg>
    );
  }}
</ParentSize>;
```

Visx is **d3 scales + React JSX shapes**. You compose; Visx doesn't decide layout for you. More code, full control. Good fit for unique viz (custom brush, linked sparklines, novel encodings).

## Tremor — dashboards in an hour

```tsx
import { Card, AreaChart, Metric, Text } from "@tremor/react";

<Card>
  <Text>Revenue</Text>
  <Metric>$ {revenue.toLocaleString()}</Metric>
  <AreaChart data={trend} index="date" categories={["mrr"]} colors={["blue"]} className="h-32 mt-4" />
</Card>;
```

Tremor v3 wraps Recharts. You get opinionated cards, KPIs, gauges, with Tailwind classes. **Trap**: when you outgrow the opinionation, you're stuck rewriting in raw Recharts. Use for internal dashboards where shipping speed > brand fit.

## ECharts — when feature breadth wins

```tsx
import ReactECharts from "echarts-for-react";

<ReactECharts
  option={{
    xAxis: { type: "time" },
    yAxis: { type: "value" },
    series: [{ type: "line", data: series, sampling: "lttb" }], // built-in downsampling
    animation: false,
  }}
  notMerge={true}
  lazyUpdate={true}
  style={{ height: 400 }}
/>;
```

Canvas-rendered (fast at 100k+ points), built-in sampling, datazoom, heatmaps, geo, sankey. Cost: configuration is an option-object, not React composition. Type-safety is partial. Pick for: massive datasets, niche chart types, polished interactions you don't want to build.

## Accessibility (skipped by every example online)

| Concern                   | Fix                                                                                                       |
| ------------------------- | --------------------------------------------------------------------------------------------------------- |
| Screen reader             | wrap chart in `<figure role="img" aria-label="Revenue over time, ..." aria-describedby="caption-id">`     |
| Color-blind safety        | use palettes from `colorbrewer` (qualitative `Set2`, sequential `Viridis`); never red/green alone         |
| Data table fallback       | render a `<table>` with the same data, `class="sr-only"` (or visible toggle) — the real accessibility win |
| Keyboard nav              | most React chart libs don't ship it; provide table fallback as primary a11y story                         |
| Tooltip on keyboard focus | pure SVG `<circle>` isn't focusable — Recharts has `tabIndex` on `<Line>` but coverage is incomplete      |
| High-contrast mode        | test with Windows High Contrast / forced-colors media query                                               |

See `Skill(ux-wcag-a11y)` for criteria. **The honest answer**: a chart is a graphical summary; an accessible app provides the data as a table too.

## Server-side / image-based rendering

| Use case                     | Approach                                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------ |
| Email digests                | `node-canvas` + ECharts headless, render PNG, attach                                             |
| PDF reports                  | render the React chart in Playwright/Puppeteer, screenshot, embed                                |
| OG images for share previews | satori (Vercel) → SVG → png; lightweight chart components                                        |
| Pre-rendered SSR for SEO     | Recharts works in SSR with explicit width/height (ResponsiveContainer needs a measurable parent) |

## Anti-patterns

- `<ResponsiveContainer>` parent with `height: auto` — renders 0px, you see nothing
- Animations on with thousands of points — UI freezes during pan/zoom
- Passing a freshly-built array on every render — Recharts re-reconciles the whole chart
- Inline lambda `dataKey={(d) => d.value * 100}` instead of pre-mapping data — perf hit + harder to memoize
- Importing all of ECharts when you need one chart — use `echarts/core` + register only what you use
- "Just use D3 directly" inside React — fights React's reconciliation; use Visx for that
- Storing chart hover/zoom state in a parent that re-renders the chart — local state in the tooltip layer
- Tooltip via DOM portal that doesn't follow scroll — use the library's tooltip component

## Red flags

| Thought                            | Reality                                                                        |
| ---------------------------------- | ------------------------------------------------------------------------------ |
| "It looks slow when I scroll"      | Animation is on. `isAnimationActive={false}`.                                  |
| "Visx feels heavy"                 | It is — that's the trade. Recharts is fine for cartesian basics.               |
| "I'll just use D3"                 | You're rendering DOM out from under React. Use Visx scales + React JSX shapes. |
| "Accessibility is hard for charts" | Ship a data table fallback. That's the answer.                                 |

## Hand-off

For tokens that drive chart colors: `Skill(frontend-design-essentials)`. For Tailwind utilities around chart containers: `Skill(frontend-tailwind)`. For a11y criteria and patterns: `Skill(ux-wcag-a11y)`. For React composition rules: `Skill(react)`.
