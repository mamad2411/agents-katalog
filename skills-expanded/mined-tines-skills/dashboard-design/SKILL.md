---
name: dashboard-design
description: Build polished, interactive analytics dashboards for any data source. Use this whenever the request involves a dashboard, data visualization, internal metrics, spend/usage/cost reporting, or any UI that shows data sliced across time, users, categories, or other dimensions — even if the word "dashboard" is never used. Covers cross-filtering, shareable URL state, filter models, legends, transitions, honest handling of incomplete data, and visualization craft. Not needed for a single static chart.
license: Apache-2.0
compatibility: Tines 3B
---

# Building analytics dashboards

Build it as a structured project — components, hooks, and helpers in separate files, not one giant file. Hand-rolled SVG is fine, often better than a chart library for bespoke interactions.

A dashboard answers questions; it isn't a page of charts. Its dimensions (time plus the data's categorical axes) are the product: make every one filterable, cross-linked, and honest about what it can't show.

For the visual identity — type, palette, spacing, and polish — use the **frontend-design** skill, and ask the user for brand guidelines or a reference if the direction isn't clear. This skill covers only what's specific to data and dashboards: pipeline, interaction, and visualization.

## Data pipeline

If the dashboard stores source data or derived views in named volumes, use `workflow-volume-design` for file ownership, bounded updates, retention, and capacity.

- Refresh on a schedule, and let users trigger a refresh on demand. Coalesce concurrent refreshes so they do not stampede the source. Put the schedule on one entry point that fans out to the fetchers, so cadence lives in one place.
- Fetch incrementally: pull only what's new since the last stored point, but keep a full-backfill path for a cold or empty store.
- Retry transient source failures with backoff, and never overwrite good data with an empty or failed result — a bad fetch leaves the last good data in place.
- Store raw source data under a stable schema so display changes don’t force a re-fetch. Keep the inputs to a transform, such as a lookup table, so derived views can be rebuilt when mappings change. Retain only the history the product needs.
- Aggregate on the fly only while the query remains bounded. When the raw volume is too large to load and roll up per request, query pre-summarized data at the source or precompute bounded rollups during refresh.
- Let users download the data (e.g. CSV): the processed rows behind the current view (respecting active filters, for finance/reporting) and/or the raw records (for their own analysis).

## Everything is a filter, selection is shared

- Clicking any mark (bar, legend entry, table row, node) scopes every other view to it, and dims (not removes) the rest of the clicked chart.
- Selection toggles: click again or `Esc` to clear. Never strand the user in a dead-end (a flow diagram filtered to one node shows nothing — exit the filter instead).
- Don't filter to a value that can't resolve — an "Others"/"+N more" bucket isn't real; expand it on hover.
- Drill-down: clicking one side of a relationship diagram can expand it and filter the other.

## Shareable URL state

Encode all view state in the URL (tab, date range, filters, grouping, granularity, scale, drill-down) so any view shares by copying the address. Keep param names matching the labels users see.

## Filters

- Multi-select by default, with an include/exclude mode ("only these" vs "all except these"). Show a count when collapsed.
- When one dimension groups another, put the parent first and scope the child's options to the parent's selection.
- Default to a recent window grouped by the dimension people care about most — not "all time", not the first column.
- Don't offer a granularity coarser than the window; disable options that can't apply.

## Legends

- Default the legend to the whole visible period, so its prominence matches the chart — not the last data point.
- Break data down per bucket only on select/hover, and pin it to a selection so it survives the mouse leaving.
- A legend that changes height must not reflow the chart; an inline hovered-label often beats a static block.

## Layout stability

The page must not jump. Reserve space so changing a filter, opening a custom-range control, or toggling a mode never shifts the title, toolbar, or charts by a pixel. Keep the header consistent across tabs. Avoid stray scrollbars.

## Transitions and the remount trap

- Animate values, not existence: a filtered-out series shrinks to zero, it doesn't vanish. Animate ticks, gridlines, and scale changes too.
- Only the data marks move on a filter change; the chart around them shouldn't repaint.
- Footgun: changing a React `key` (or whatever identity a transition depends on) remounts the element — the usual cause of marks flickering, vanishing, or staying empty until hover. Key on a stable series id, not a filtered index or a changing value, and fix it once, not per chart.

## Transparency about incomplete data

- A dynamic banner composed from whichever caveats apply — never warnings scattered around the page — and only on views where the caveat is relevant, not on totals it doesn't touch.
- Label each kind of missing data distinctly; don't merge them into one vague bucket.
- Prefer stale over missing, and "Loading…" over internal state — never leak "no data files yet".
- Don't show an incomplete period as complete: drop the current partial period from preset windows, show it only on custom ranges, and warn when a range includes it.

## Numbers and visualization craft

- Round to consistent significant figures; more decimals only where small magnitudes need them. Use tabular numerals so figures align. Offer an absolute-vs-share (%) toggle.
- Log/linear toggle for skewed data — linear alone hides the tail.
- Top-N + "Others" for high-cardinality series.
- Borrow techniques from data journalism (Tufte, Few, Economist, Bostock): labeled round-number gridlines, distribution views (beeswarm/strip with median, mean, percentiles). Delete decoration that carries no information — stray outlines, redundant legends, a number shown twice.
- Make charts self-explanatory: if you'd explain an encoding in chat, put that in the UI.
- Give series a dedicated categorical color scale (distinct from the UI's brand/chrome colors). Related categories get related colors — shades of a hue per family, a distinct hue per group — and treat a natural grouping as its own dimension. Ask the user whether the audience needs a color-blind-safe palette; if so, use a qualitative scheme designed for it (e.g. Paul Tol's / SRON schemes) and back color with a second cue (shape, pattern, direct labels).
- Charts follow the system light/dark theme like the rest of the UI, with axis, gridline, label, tooltip, and series colors and a series scale tuned for each mode. Chart colors are usually set in code, so choose them from `matchMedia('(prefers-color-scheme: dark)')` and re-render when it changes.
- Sort each chart by its meaningful axis; put axis labels outside the plot so marks never cover them.

## Affordances and accessibility

`cursor: pointer` on everything clickable, including custom SVG marks. Scope `user-select: none` to chart labels and chrome — never the whole app, or users can't copy real text. Keyboard activation on custom marks, and honor `prefers-reduced-motion`. Confirm with the user whether the dashboard needs to meet accessibility requirements (screen readers); if so, give charts ARIA roles and text alternatives (a caption or data-table fallback), since a screen reader can't read an SVG chart.
