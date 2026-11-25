---
name: canon-charts
description: Use when designing, auditing, or refactoring charts, graphs, data visualizations, dashboards, sparklines, or any visual representation of data. Covers chart-type selection, color, axes, labels, tooltips, accessibility, animation, and anti-patterns like 3D pies and dual-axis charts. Trigger when the user mentions chart, graph, visualization, dashboard, bar chart, line chart, pie chart, or sparkline.
---

# CANON · Charts

A chart is a claim. If the reader can't extract the claim in five seconds, the chart failed regardless of how pretty it is.

## Pick the right chart type

| Goal | Chart type |
|---|---|
| Compare categories | Bar chart (horizontal if labels are long) |
| Show trend over time | Line chart |
| Show part-of-whole, ≤ 5 slices | Pie or donut (used sparingly) |
| Show part-of-whole, > 5 slices | Stacked bar or treemap |
| Show distribution | Histogram, box plot |
| Show correlation | Scatter plot |
| Show change across two points | Dumbbell chart, slope chart |
| Single key metric with trend | Big number + sparkline |
| Show composition over time | Stacked area |

## Axis rules

- **Y-axis should start at zero** for bar charts. Always. Truncating bar axes inflates differences and misleads.
- Line charts may use a non-zero baseline *if* the data range is narrow and a zero-start would flatten the signal — in that case, explicitly note the baseline.
- X-axis time: left → right, always. Never right → left.
- Label axes clearly. "Revenue ($)" beats "$".
- Tick marks: 4–7 per axis. More = visual noise. Fewer = hard to read.
- Grid lines: light, thin, optional. Full grids often hurt. Horizontal-only grid for vertical bar charts.

## Color in charts

Follow `canon-color` for palette. Chart-specific rules:

- **Categorical (qualitative)**: distinct hues, roughly equal perceptual weight. 5–8 max. Beyond 8, reorganize the data.
- **Sequential (ordinal)**: single-hue light-to-dark. Works for ordered data (low → high).
- **Diverging**: two hues from neutral midpoint. Use for data with a meaningful zero or center (profit/loss, above/below average).

**Avoid rainbow palettes** — they imply order where there is none and fail for colorblind users.

**Avoid red/green as the only signal.** 8% of men are red-green colorblind. Pair with shape or position.

Test palettes against deuteranopia, protanopia, tritanopia simulators.

## Labels over legends

If you can label data directly, do it. Legends force the eye back and forth.

```
Bad:
  [chart with color swatches]
  Legend: ■ Q1  ■ Q2  ■ Q3

Better:
  [chart with "Q1 $2.1M" labeled next to the bar]
```

When legend is required, place it top-left or aligned with the chart title, not bottom-right.

## Tooltips

- Trigger: hover (desktop), tap (mobile). Keyboard focus must also trigger.
- Content: the exact value, the label, optional context ("+12% vs Q3").
- Position: above the point, offset 8–12px. Never covers the cursor.
- Follow the cursor for line/scatter; snap to nearest data point.
- Fade: 120–180ms on enter, 100ms on exit.

## Accessibility

- Every chart needs a **text alternative**: `aria-label` on the chart container, or `<figcaption>` summarizing the finding.
- Provide a **data table alternative** — either visible (toggle) or screen-reader-only. WCAG 1.1.1.
- Focusable data points with keyboard nav in complex charts. Arrow keys move between points, Enter/Space reads the value.
- Color is never the only signal. Add pattern fills, shapes, or labels.
- Don't animate past `prefers-reduced-motion`.

## Animation

| Purpose | Allowed? | How |
|---|---|---|
| First-paint entrance | Yes | 400–600ms ease-out, each bar/line staggered 30–60ms |
| Data update | Yes | 300–400ms ease-in-out, interpolate values |
| Decorative motion (pulsing, rotating) | No | Serves no purpose, distracts |
| Tooltip | Yes | 120–180ms fade |

Honor `prefers-reduced-motion: reduce` with an instant-draw fallback.

## Labels and numbers

- Use `font-variant-numeric: tabular-nums` so digit widths align.
- Thousands separators (1,234 not 1234) unless the space is desperate.
- Round intelligently: 2.4M not 2,400,000 for labels; precise for tooltips.
- Currency symbol attached, no space: `$1.2M` not `$ 1.2 M`.
- Percentages without decimal where precision isn't critical: `12%` not `12.00%`.

## Sizing and aspect ratio

- Line charts: 16:9 or 3:1 (wide for trends).
- Bar charts: 4:3 or 1:1, enough vertical room for labels.
- Minimum readable size: 320×240px. Smaller → sparkline territory.
- Sparkline: 80–160px wide, 24–40px tall, no axes, single sparkline per row.

## Dashboards

- Most important metric: top-left (F-pattern entry).
- Hierarchy: big numbers > charts > tables.
- Consistent card heights in a row.
- Timeframe controls visible and global.
- Max 8 tiles per dashboard screen — more needs drill-down, not density.

## Common chart bugs

| Bug | Fix |
|---|---|
| Bars truncated at top | Add 10% headroom above max data point |
| Overlapping X-axis labels | Rotate 30–45°, or use horizontal bars |
| Same color for positive and negative | Use a diverging palette |
| Time axis not in order | Sort by date always |
| Tooltip flickering | Add 100ms hover delay, use `pointer-events: none` inside the chart plot |
| Legend wraps awkwardly | Break to new line at fixed width, or convert to direct labels |

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| 3D pie charts | Distort perception of slice sizes |
| Dual-axis line charts | Misleading; two different scales suggest correlation that doesn't exist |
| Pie chart with 8+ slices | Unreadable; use stacked bar |
| Rainbow palette for categorical data | Implies order, colorblind fail |
| Red and green as only signal | 8% colorblind population fails to distinguish |
| Truncated Y-axis on bar chart | Exaggerates differences, misleads |
| Chart with no title | Users guess the point |
| Chart with no units | "$2.4" — millions? thousands? |
| Pulsing / rotating decoration | Distraction, triggers motion sensitivity |
| Tooltip covering the data point | Can't re-check the source |
| Animation on every data update | Chart thrashes in live dashboards |

## Decision tree

```
What's the user trying to learn?

Compare values across a few categories → Bar chart
Spot trend over time → Line chart
Composition of one whole → Donut (≤ 5 slices) or stacked bar (> 5)
Correlation between two variables → Scatter
Distribution → Histogram or box plot
How did N series change between two snapshots → Slope or dumbbell
One key number → Big number + optional sparkline
```

## Audit checklist

- [ ] Chart type matches the question the user is asking
- [ ] Bar chart Y-axis starts at zero
- [ ] Time axis is left-to-right
- [ ] Axis labels include units
- [ ] Chart has a title or caption stating the claim
- [ ] Color palette is colorblind-safe
- [ ] Color is not the only signal
- [ ] Direct labels preferred over legends where possible
- [ ] Tooltips keyboard-accessible
- [ ] Text alternative exists (`aria-label`, table toggle, or figcaption)
- [ ] `font-variant-numeric: tabular-nums` on data numbers
- [ ] Animations honor `prefers-reduced-motion`
- [ ] No 3D effects
- [ ] No dual-axis charts (unless genuinely justified and labeled)
- [ ] Pie charts have ≤ 5 slices

## Sources

- Edward Tufte · The Visual Display of Quantitative Information
- Stephen Few · Information Dashboard Design
- Cole Nussbaumer Knaflic · Storytelling with Data
- WCAG 2.2 · 1.1.1 Non-text Content, 1.4.1 Use of Color, 2.1.1 Keyboard
- Viz Palette · colorblind-safe palettes
- Material Design 3 · Data visualization
