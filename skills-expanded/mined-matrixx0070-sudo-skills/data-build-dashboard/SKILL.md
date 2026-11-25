---
name: data-build-dashboard
version: 1.0.0
description: Build a self-contained interactive HTML dashboard with KPI cards, charts, and filters that runs from a single offline file.
author: matrixx0070
tags: [dashboard, html, visualization, interactive, reporting, kpi]
capabilities: []
---

# data-build-dashboard

## When to use

Use this when the user wants an explorable dashboard rather than a static chart or a one-off number — a KPI overview, a metrics tracker, or a report others click through. Deliver one HTML file that opens in any browser with no server, build step, or network dependency.

**Not for:** a single publication chart (use data-create-viz), the analysis or recommendation behind the numbers (use data-analyze), or verifying the numbers are correct (use data-validate).

## Method

1. **Define the decisions** the dashboard supports. List the 3-6 KPIs that answer them and the dimensions users slice by (date, region, segment).
2. **Shape the data.** Embed it inline as a JSON array in a `<script>` block. Decision point: if raw rows exceed a few thousand, pre-aggregate rollups and keep raw rows only where filtering needs them — note the row count.
3. **Lay out top-down:** KPI cards (with delta vs prior period) across the top, primary trend chart next, breakdown charts below, detail table last.
4. **Add interactivity:** a date-range control and dimension filters that recompute every KPI and chart. Wire all filters through one shared `applyFilters()` so state stays consistent.
5. **Style** with a clean CSS system: responsive grid, readable type scale, palette that works in light and dark. One charting library via CDN with an offline fallback, or hand-rolled SVG.
6. **Self-test** the numbers: totals must reconcile with the source before delivery.

## Example

One filter function feeds every widget, so nothing drifts out of sync:

```js
const DATA = [ /* ...inline rows... */ ];
function applyFilters() {
  const rows = DATA.filter(r => r.date >= start.value && r.region === region.value);
  renderKPIs(rows);      // all widgets read the same filtered set
  renderCharts(rows);
  renderTable(rows);
}
[start, end, region].forEach(el => el.addEventListener("change", applyFilters));
applyFilters();
```

## Pitfalls

- Embedding millions of raw rows, producing a multi-MB file that hangs the browser.
- Each chart filtering independently, so KPI cards and charts disagree.
- A CDN-only chart library with no fallback — the file breaks offline.
- Shipping without reconciling totals, so the dashboard looks polished but lies.

## Output format

```
Deliverable: one self-contained .html (data + CSS + JS inline, works double-clicked offline)
Top:    title, last-updated timestamp, KPI card row with period-over-period deltas
Middle: interactive filters + primary time-series chart
Bottom: breakdown charts + sortable detail table
Note:   data source, refresh method, assumptions
```

State how to refresh the data.
