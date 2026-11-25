---
name: dataviz
description: Turns rows of data into one honest chart. Picks the chart type from the question being answered, builds it as inline SVG or CSS with no chart library, and keeps it readable: one accent, muted grid, mono tabular labels, a zero baseline, real units and a comparison on every figure. Use when the user asks for a chart, graph, plot, sparkline, dashboard, KPI or stat tile, wants data visualized, needs a report or slide figure, or when a screen has placeholder chart noise that has to become real.
license: CC-BY-4.0
---

# Dataviz

A chart is an answer to one question. If you cannot say the question in a sentence, you cannot pick the chart, and a chart that answers nothing is decoration with numbers on it.

## What good looks like

- **One question per chart.** The title is the question, or its answer. "Runs per month", not "Analytics".
- **The type follows the question.** Trend is a line, comparison is bars, share is one stacked bar, a single goal is a progress bar, a ranking is a list with thin bars.
- **One accent.** The thing that matters gets it. Everything else is neutral steps of one ramp. Never a rainbow inside one series.
- **Zero baseline for anything with area.** Bars and stacked bars start at zero, always. A line may start elsewhere if the truncation is visible and stated.
- **Muted chrome.** Grid, axis and labels are quiet. The data is the only loud thing, and only one series of it is loud.
- **Numbers you can read.** Units in the label, one format, `tabular-nums`, no trailing decimals that lie about precision.

## Run it

1. **Write the question.** One sentence: what decision does this chart help someone make. If it is "show the data", cut it or make it a table.
2. **Pick the type** from [references/charts.md](references/charts.md). It also names the chart that looks right and is wrong, which is usually a donut.
3. **Shape the rows.** One table, one row per category, one column per series, numbers already in the unit to be shown. CSV or JSON, nothing pre-aggregated twice.
4. **Build it.**
   - Fast path: `node <skill folder>/scripts/chart.mjs data.csv --type line --title "Runs per month" --unit runs --accent "#e0a458" --out chart.svg`
   - Types: `line`, `bar`, `stacked`, `sparkline`, `progress`. Options: `--width --height --theme dark|light --subtitle --xlabel --ylabel --decimals --max`.
   - It writes standalone SVG with `role="img"`, a `<title>`, a `<desc>`, mono tabular labels and a muted grid. Drop it in the page as-is, or inline it to style it with the page's tokens.
   - Hand-built when the chart has to live inside a component: the recipes in [references/charts.md](references/charts.md) are plain SVG and CSS, no dependency.
5. **Check it** against the checklist below, at the size it will really be seen. A chart legible at 720 wide is not legible at 280.

## Rules that are not taste

- **No chart library for a simple chart.** Four bars and a line are 30 lines of SVG. A library costs 40 to 120 KB, brings default styling that has to be undone, and usually ships a canvas that screen readers cannot read.
- **Do not encode one series in many colors.** One accent, one series that leads. More than three series in one chart means two charts, or a table.
- **Color is never the only signal.** Direct labels, position, or a shape difference. A chart that fails in greyscale fails for one in twelve men.
- **Text is real text.** SVG `<text>`, not paths, so it scales with the reader's settings. No labels baked into an image.
- **Respect the container.** `viewBox` plus `width:100%`, `height:auto`, a `max-width`, and a `min-width` where the labels stop fitting. Fewer ticks and fewer bars at 375 wide, not a shrunken chart.
- **No fake data.** If the numbers are placeholders, the chart says so next to the title and the report lists it. `[needs: real run count]` beats a plausible fiction.
- **Units and comparisons.** "47 runs" or "$48,210", never "47". A change always carries what it compares to: "+12% vs last month".
- **Charts have hierarchy.** One main chart per screen, clearly the largest. A second chart of the same size means neither one is the point.

## Checklist

- [ ] The chart answers one named question, and the title says it
- [ ] The type matches the question; no donut, no pie with six slices, no 3D, no dual axes
- [ ] Bars and stacked bars start at zero; any truncated line says so
- [ ] One accent on the series or point that matters; everything else neutral
- [ ] More than three series split into two charts or a table
- [ ] Grid and axis muted, no chart border, no drop shadow
- [ ] Labels in mono, tabular figures, one number format, units present
- [ ] Legend present when there is more than one series, and not needed when there is one
- [ ] Every figure has its comparison where a change is shown
- [ ] `role="img"`, `<title>` and `<desc>` say what the chart shows, in words
- [ ] Readable at 375 wide and at 200 percent zoom; nothing clipped, no label collisions
- [ ] Works in greyscale; color is not the only difference between series
- [ ] Placeholder data is marked in the page and listed in the report
- [ ] The numbers trace to a source you can name

Chart type table, the wrong-but-common choices, and the hand-built SVG and CSS recipes: [references/charts.md](references/charts.md).
