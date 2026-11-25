---
name: write-data-viz
description: Produces data visualizations and dashboards as code — matplotlib/seaborn/plotly static and interactive charts, plus D3.js/HTML dashboards — picking chart types that fit the data.
when_to_use: When the user asks to visualize data or build a chart/dashboard — plot a trend, comparison, distribution, or relationship, generate an interactive Plotly/D3 chart, or assemble a multi-panel dashboard from a dataset.
---

## When to Use

Use when the request is to turn data into a visual artifact in code: plot a trend/comparison/distribution/relationship, build an interactive Plotly/D3 chart, or assemble a multi-panel dashboard from a dataset (CSV/JSON/DataFrame/SQL result).

Not this skill: native Excel/Sheets charts embedded in a workbook (that is the spreadsheet skill — this one emits code and web artifacts, png/svg/html).

## Steps

1. **Inspect the data first — do not guess.** Load it and check shape before plotting: row count, dtypes, null counts, cardinality of categorical columns, min/max of numerics. In pandas: `df.info()`, `df.describe()`, `df.isna().sum()`, `df[col].nunique()`. Decide here whether aggregation is needed (e.g. >5k points → sample/bin; >12 categories → top-N + "Other").

2. **Map analytical goal → chart type** (the goal is in the request verb, not the user's wording):
   - trend over time → line (or area for cumulative)
   - compare categories → bar (horizontal bar if labels are long or >7 categories)
   - distribution of one variable → histogram or box/violin; KDE if smooth shape matters
   - relationship between two numerics → scatter; add trendline/`hexbin` if dense
   - part-of-whole → stacked bar or treemap — **avoid pie for >3 slices**
   - correlation matrix → heatmap
   - ranking → sorted horizontal bar
   When unsure between two, default to the one with less ink (bar over pie, line over stacked area).

3. **Pick the engine by output requirement, not by habit:**
   - static report image (png/svg) → `matplotlib` + `seaborn`
   - interactive (hover/zoom/toggle) needed → `plotly` (`plotly.express` for speed, `graph_objects` for control)
   - embeddable/standalone web dashboard, custom interaction, or no-Python-runtime delivery → `D3.js` in a single self-contained HTML file
   Confirm the library is installed (`python -c "import plotly"`) before writing the full script; if missing, install or fall back to matplotlib and say so.

4. **Annotate every chart** — non-negotiable, in this order: title (states the takeaway, not "Chart of X"), axis labels **with units**, legend only when >1 series, source/date note if relevant. Format axis ticks for humans (thousands separators, `%`, dates as `%b %Y`). Sort bars by value unless the x-axis is inherently ordered (time, ordinal).

5. **Style:** use a colorblind-safe palette (matplotlib `tab10`/`viridis`, seaborn `colorblind`, plotly default Safe). Strip chartjunk: no 3D, no gridlines on bars, no background fill, no redundant legend. One accent color for the series that matters; grey out the rest. Set `dpi=150`+ for static export.

6. **Multi-panel dashboard** when ≥3 related metrics: matplotlib `plt.subplots()` / `GridSpec`, plotly `make_subplots`, or D3 a CSS-grid of `<svg>` panels. Share axes where comparable, give each panel its own clear title, keep one consistent palette across panels.

7. **Save the artifact and tell the user how to view it.** Static → `fig.savefig("chart.png", dpi=150, bbox_inches="tight")` (use `bbox_inches="tight"` or labels clip). Interactive plotly → `fig.write_html("dashboard.html")`. D3 → one HTML file with the data inlined or fetched. State the absolute path and the open command (e.g. open the `.html` in a browser).

## Common Errors

- **Overplotting** — thousands of scatter points become a blob. Fix with `alpha=0.3`, `hexbin`/2D-density, or sampling. Do not ship a solid ink cloud.
- **Misleading dual axes** — two y-axes invite false correlation and can be scaled to tell any story. Prefer two stacked panels sharing the x-axis; only use twin axes when units are genuinely paired and label both clearly.
- **Categorical read as numeric** — IDs/year-codes/zip codes loaded as int get a continuous color scale or spaced as numbers. Cast to `str`/`category` first.
- **Truncated/non-zero bar baseline** — bar charts MUST start the value axis at 0 or they exaggerate differences. Line charts may zoom; bars may not.
- **bbox clipping** — long tick/axis labels get cut off in saved PNGs. Always `bbox_inches="tight"` and rotate or horizontal-bar long labels.
- **Too many colors / rainbow** — >7 hues are unreadable. Group, use top-N + Other, or a sequential scale.
- **Time not parsed** — date strings on the x-axis sort lexically (2026-01 after 2026-1). Parse to datetime before plotting.
- **Plotly HTML huge/blank offline** — default embeds the full lib (~3MB) and a blank page if CDN is blocked; pass `include_plotlyjs="cdn"` for size or `=True` for offline-safe.

## Verify

1. Script runs to completion with no exception, and the output file exists on disk (check the path).
2. Open/inspect the rendered artifact — title, both axis labels+units, and legend are present and not clipped.
3. Chart type matches the analytical goal from Step 2 (a trend is a line, not a bar; bars start at 0).
4. No overplotting/rainbow/dual-axis trap from Common Errors slipped through.
5. For interactive output, confirm hover/zoom actually works (open the HTML); for a dashboard, every panel rendered and shares a consistent palette.
