---
name: chart
description: >-
  Build a chart comparing census numbers across districts/regions. Supports comparisons,
  growth trends, rural vs urban splits. Use when the user asks to "show", "plot",
  "chart", or "visualize" data.
---

# Chart recipe

1. GET THE DATA from tools, never from memory:
   - one metric across districts → `query_tables` on the relevant statement CSV;
   - a few values from prose → `search_census` and record each chunk_id.
2. CALL `render_chart` with a `ChartSpec` (DO NOT hand-write plotting code):
   - Pass the chart details directly in the `ChartSpec` schema (e.g. `{"template": "bar", "title": "...", "x": ["Dist A", "Dist B"], "series": [{"name": "Pop", "y": [10, 20]}], "slug": "my-chart"}`).
   - The backend renders the vetted template and always produces `<slug>.png`, `<slug>.json`, and `<slug>.csv`.
   - If `render_chart` errors, READ the stderr, fix the cause, and retry. Max 3 attempts.
3. Reply with `kind="artifact"`: `artifacts=["my-chart.png"]` (use the generated PNG's name), `answer_md` = one-paragraph
   takeaway, and a claim citing every page/chunk the numbers came from.

## Gotchas
- Sex ratio = females per 1000 males. NEVER convert it to a percentage.
- Growth rates in the docs are already percentages — do not recompute from absolutes
  unless district boundaries changed (Yadgir, Ramanagara, Chikkaballapura were created
  after 2001; their 2001 figures don't exist).
