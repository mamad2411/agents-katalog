---
name: chart-visualization
description: Generate a complete local HTML chart. Use for trends, comparisons, distributions, relationships, flows, or dashboards.
version: 1
tags: [chart, visualization, echarts, dashboard]
triggers: [make a chart, visualize data, plot trend, create dashboard]
requires:
  tools: [write_file]
optional:
  tools: [read_file]
---

# Chart Visualization

Deliver one complete HTML file under `output/` unless the user explicitly requests multiple views.

1. Select the chart type that best matches the question.
2. Read `references/echarts.md` when using ECharts.
3. Read `templates/chart.html` only when a starter document is useful.
4. Embed the data, provide explicit chart dimensions, responsive resizing, labels, tooltip, and visible SDK-load failure state.
5. Use `write_file` to create `output/<safe-descriptive-name>.html`.
6. Return the generated relative path. Do not claim that a frontend file list exists.

Do not add image export or download controls unless explicitly requested.
