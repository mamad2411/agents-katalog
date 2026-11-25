---
name: data-charts
description: "Analyze tabular data and render charts (bar, line, scatter, pie, histogram) to PNG/SVG with pandas + matplotlib. Use whenever the user wants to plot, chart, graph, or visualize data from a CSV/JSON/Excel file or inline numbers."
license: MIT (Code Buddy original skill)
nativeEngine:
  triggers:
    - chart
    - plot
    - graph
    - visualize
    - visualization
    - histogram
    - bar chart
    - scatter plot
    - line chart
    - pie chart
    - graphique
    - diagramme
    - trace
---

# Analyze data & render charts with pandas + matplotlib

Turn tabular data (CSV/JSON/Excel/inline) into a real chart image using the
open-source **pandas** + **matplotlib** libraries. Work in **visible steps** and
verify the image was written before reporting.

## Getting the data when it's NOT in a file (e.g. "France GDP over 10 years")
When the user asks to chart something you must look up rather than read from a
file, gather the numbers FIRST with your normal tools — your own knowledge, or a
quick `web_search` — then **hard-code them as inline Python lists**. Do **NOT**
fetch from an external API *inside* the Python script (`urllib`/`requests`):
sandboxed network calls routinely time out (the 30 s command limit), which makes
you give up and fall back to a much worse ASCII/text "chart". Inline numbers →
matplotlib → a real PNG is fast and reliable. Only read from the network when the
user explicitly gives you a data URL and it's known-fast.

## Preflight (extras-tier libs)
These libs are optional and not in the default build. Always check first:
```bash
python3 - <<'PY'
try:
    import pandas, matplotlib  # noqa: F401
except ModuleNotFoundError as e:
    raise SystemExit(
        f"{e.name} not installed. Run `npm run prepare:python:extras` in cowork/ "
        "to enable the data-charts skill (pandas + matplotlib)."
    )
print("data-charts deps OK")
PY
```

## Workflow (one step at a time)
1. **Load** the data with pandas (`read_csv` / `read_json` / `read_excel`), or
   build a `DataFrame` from inline numbers.
2. **Inspect**: print `df.head()` and `df.describe()` (or the shape) so the data
   is visibly understood before plotting.
3. **Plot**: use the **non-interactive Agg backend** (`matplotlib.use("Agg")`,
   set before importing pyplot — there is no display), build the chart, add a
   title + axis labels, and `savefig(path, dpi=144, bbox_inches="tight")`.
4. **Verify**: `assert os.path.getsize(path) > 0` and print the path + size.
5. **Report** the saved image path and a one-line insight from the data.

## Quality conventions
- Always set `matplotlib.use("Agg")` **before** `import matplotlib.pyplot` — the
  app has no X display; the interactive backend would crash.
- Label axes and give every chart a title; use a legend when >1 series.
- Prefer `tight_layout()` / `bbox_inches="tight"` so labels aren't clipped.
- Save PNG by default (144 dpi); SVG when the user wants a vector.

## Example
```bash
python3 - <<'PY'
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")            # headless — set before pyplot
import matplotlib.pyplot as plt

df = pd.read_csv("sales.csv")    # columns: month, revenue
print(df.head()); print(df.describe())

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(df["month"], df["revenue"], color="#3b82f6")
ax.set_title("Monthly revenue"); ax.set_xlabel("Month"); ax.set_ylabel("Revenue ($)")
fig.tight_layout()
out = "revenue.png"
fig.savefig(out, dpi=144, bbox_inches="tight")

assert os.path.getsize(out) > 0, "chart image is empty"
print(f"wrote {out} ({os.path.getsize(out)} bytes); peak month = "
      f"{df.loc[df['revenue'].idxmax(), 'month']}")
PY
```

## Notes
- The chart image is an artifact — surface its path so the GUI can preview it.
- For quick stats without a chart, `df.describe()` / `df.groupby(...).agg(...)`.
- To put a chart *into* an Excel/Word/PowerPoint file, hand the saved PNG to the
  `xlsx`/`docx`/`pptx` create skills.
