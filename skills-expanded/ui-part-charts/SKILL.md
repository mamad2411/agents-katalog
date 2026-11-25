---
name: ui-part-charts
description: "Charts and figures: choosing the chart by the question, titles, axes, units and direct labels, colour from tokens with one series highlighted, tooltips, loading, empty and error states, a text and table alternative, libraries, load cost and phones. Read before building a chart, a sparkline or any data figure."
---

# Charts and figures

The generated version: a donut of two values, a 3D bar, twelve series in a
rainbow under a legend nobody can match, an axis with no unit, a smooth
trend line drawn from numbers nobody measured, and the chart animating
again on every hover. A chart answers one question with real data; this is
how to choose it, label it, colour it, and make it readable by people who
cannot see it. One part of an interface: the principles (direction,
spacing, type, colour, icons, states, accessibility) are in the `ui`
skill, the measures in `ui-layout`.

## 1. Choose by the question

| Question | Chart | Notes |
|---|---|---|
| How did it change over time? | line; columns for a few periods | the period in the title |
| Which category is biggest? | horizontal bars sorted by value, with values | easier to read than a donut |
| What is the whole made of? | stacked or 100% bar; a donut only with 5 parts or fewer | never a donut for two values |
| How is it spread? | histogram, box plot, dot plot | say the bin size |
| Do two measures move together? | scatter | a trend line only when fitted |
| Where are we against a target? | the number, its change, a sparkline or bullet bar | with unit and period |

- A single figure is often the best chart: "412 orders this week, 38 more
  than last week", in words, from the data.
- No chart without a question: no decorative charts, no sample series to
  fill a dashboard.
- No 3D; no dual axes unless two units truly share one time line (then
  each axis labelled in its series' colour); no radar charts to compare.

## 2. Titles, axes, labels

- The title states the question the chart answers, with the measure, the
  unit and the period: "Failed jobs per hour, last 24 hours". A static
  report may state the finding instead ("Refunds fell after the size guide
  shipped") with the measure beneath; on a live dashboard the finding
  changes, so the measure is the title.
- Axes labelled, with units ("ms", "%", "Rp"). Bars start at zero, since
  their length is the value; a line may start above zero when the change
  is the point, with the axis clearly numbered.
- 3 to 6 ticks on a value axis, at round numbers; dates at natural steps
  (hours, days, months), formatted for the locale with
  `Intl.DateTimeFormat`, numbers with `Intl.NumberFormat`
  (`notation: "compact"` gives 12K).
- Direct labels rather than a legend: a line's name at its end, a bar's
  value at its tip. A legend only past three series, above the chart, in the order
  the lines end.
- Gridlines faint or none: horizontal only, at border strength.
- The source and the time of the data under it ("Orders database, updated
  10:15"), with the time zone when it matters.

## 3. Colour

- Drawn with the tokens: one accent for the series that matters, neutrals
  for the rest. One highlighted series says more than seven colours.
- When several series must be told apart: a categorical palette of 6 to 8
  token colours that differ in lightness as well as hue, safe for colour
  blindness (the Okabe-Ito set is a good start) and at 3:1 against the
  background in both themes. Past 8, group the rest as "Other".
- Sequential scales (one hue, light to dark) for amounts, as in a heatmap;
  diverging scales (two hues round a neutral middle) for above and below a
  baseline.
- Colour is never the only key: labels, markers or dashes carry it too.
  Never red and green alone for bad and good.

## 4. Interaction

- A tooltip on hover and on keyboard focus with the exact value, its unit
  and its date; it follows the pointer with no delay. On touch, a tap
  shows it and a tap elsewhere hides it.
- Points or bars reachable from the keyboard when the values matter (the
  library's accessibility option, or arrow keys along the series).
- Ranges (7 days, 30 days, 12 months) as a segmented control above the
  chart, kept in the URL; while new data loads, the old chart stays,
  dimmed.

## 5. States

- Loading: the frame at its final size with the title and axes, a quiet
  skeleton inside; never fake bars.
- Empty: said in the chart's place ("No failed jobs in the last 24
  hours"). A zero is data: a flat line at zero is right when the series
  exists.
- Error: in the chart's place, what failed and a retry.
- Gaps stay gaps: missing points are not drawn as zero or joined across.
- Never an invented series, trend or number. A template shows a visible
  "[Sample data]" label until real data is connected.

## 6. For people who cannot see it

- A text alternative: a `figure` whose `figcaption` gives the title and
  the finding, or `role="img"` with an `aria-label` on a small chart;
  decorative parts of the SVG `aria-hidden="true"`.
- The same numbers as a table, next to the chart or behind a "Show data"
  disclosure. A canvas chart (Chart.js, ECharts on canvas) is invisible to
  a screen reader without it.

## 7. Libraries and cost

- The component library's chart kit first (shadcn's charts are Recharts,
  themed with CSS variables), or an established library:
  - Recharts: React, SVG, declarative; dashboards up to a few thousand
    points.
  - ECharts: canvas or SVG, large datasets, heatmaps, maps; import from
    `echarts/core` so only the charts used ship.
  - Chart.js: canvas, any framework, simple charts, small.
  - visx: low-level React pieces on D3, for a chart you design yourself.
  - Observable Plot: SVG, concise, good defaults for reports and analysis.
  - Nivo: React, many chart types, SVG, canvas or HTML.
  - A sparkline is a `polyline` in an inline SVG; no library.
- The chart library loads when the chart is on screen (`import()`), not
  with the page: `React.lazy`, `next/dynamic`, or an IntersectionObserver.
- More points than pixels is waste: aggregate on the server, or downsample
  with LTTB (ECharts: `sampling: "lttb"`); SVG slows past a few thousand
  elements.

## 8. Phones, themes, motion

- Responsive: the chart takes its container's width, with a set height per
  width (240 to 320px on wide screens, 200 to 240px on a phone), not a
  ratio that shrinks it to a strip.
- On a phone it shows its headline number, with the chart below it or
  behind a tap; 3 or 4 ticks, short date labels ("Sep"), horizontal bars
  for long category names, any legend below.
- Themes: series colours from tokens, the same hues lighter on dark,
  labels in the muted text colour. A canvas chart reads the tokens with
  `getComputedStyle` and redraws when the theme changes (`ui-themes`).
- Motion: bars grow and lines draw once, on first view; a live update
  animates only the change; nothing replays on hover; under reduced motion
  the chart appears finished (`motion-interface` 14).

## 9. A sketch

Recharts: a sorted bar list with values, one bar highlighted.

```tsx
import { Bar, BarChart, Cell, LabelList, ResponsiveContainer, XAxis, YAxis } from "recharts";

type Row = { reason: string; count: number };

export function RefundsByReason({ rows, highlight, reducedMotion }: {
  rows: Row[]; highlight: string; reducedMotion: boolean;
}) {
  const sorted = [...rows].sort((a, b) => b.count - a.count);
  return (
    <figure>
      <figcaption>Refunds by reason, September</figcaption>
      <div style={{ height: 40 * sorted.length + 16 }}>
        <ResponsiveContainer>
          <BarChart data={sorted} layout="vertical" margin={{ right: 48 }}>
            <XAxis type="number" hide />
            <YAxis type="category" dataKey="reason" width={140} tickLine={false}
              axisLine={false} tick={{ fill: "var(--text-muted)" }} />
            <Bar dataKey="count" radius={2} isAnimationActive={!reducedMotion}>
              {sorted.map((r) => (
                <Cell key={r.reason}
                  fill={r.reason === highlight ? "var(--accent)" : "var(--chart-neutral)"} />
              ))}
              <LabelList dataKey="count" position="right" fill="var(--text)" />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <details>
        <summary>Show the data</summary>
        <table>{/* the same rows: reason, count */}</table>
      </details>
    </figure>
  );
}
```

## Check it

- `preview` in both themes: chart text below 4.5:1, and an SVG chart whose
  main colour is below 3:1, are reported; a canvas is not measured, so
  compute its colours yourself. At 360px nothing overflows and labels do
  not collide.
- `preview` with `motion: true`: the chart animates once, and not at all in
  the reduced-motion pass.
- Read the title alone: what is measured, in what unit, over what period?
  Cover the legend: can every series still be named?
- Tab to the chart: tooltips appear on focus; a screen reader reads the
  caption and reaches the table.
- Trace every number to its query. Empty the data source: the empty state
  shows, not a broken axis. `ui_check` flags invented figures around it.

## Avoid

Decorative charts; a donut for two values, or with twelve slices; 3D; dual
axes for convenience; bars that do not start at zero; a rainbow legend;
red and green as the only key; axes with no units; a trend line with no
data behind it; sample data left in; animation on every hover; the whole
chart library in the first load; a canvas chart with no table.
