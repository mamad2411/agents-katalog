---
name: exec-visualization
description: Use flint-chart to create a chart, graph, visualization, plot, png, svg, dashboard, or diagram when data must be illustrated.
---

# flint-chart Visualization Standards (embed into Codex prompts)

## Standards block

```
flint-chart visualization (mandatory):
- Primary: If flint-chart MCP tools are available in the session, use them and request PNG/SVG
  output.
- Fallback: Otherwise, follow the flint-chart-author skill spec or run the local
  `npx flint-chart` CLI to compile and render.
- Last resort: Use Python matplotlib only when flint-chart cannot express the chart, and state the
  fallback reason in one line.
- Output: Default to PNG/SVG for documents and deliverables as a drop-in for matplotlib PNGs. Use
  backend specs such as Vega-Lite or ECharts JSON only for web or interactive targets that need them.
- Form: Match the data's job: magnitude -> bar; change over time -> line; part of whole -> stacked
  bar (pie sparingly); correlation -> scatter; single headline -> stat tile or hero number, not
  necessarily a chart.
- Axes: Use one y-scale only; never use a dual-axis chart. Put different-scale measures in two
  charts or index them to a common base.
- Series: For two or more series, always include a legend and never encode identity by color alone.
- Defaults: Let flint derive the palette, marks, and layout from the data; do not hand-tune colors.
- Integrity: Never fabricate data points.
```

## Verification block

```
Verification before finishing (mandatory):
- Confirm the chart file actually rendered: a non-empty PNG/SVG exists on disk, not just a spec.
- Confirm the chart form matches the data's job, axes and labels are correct, and no data was
  invented.
- If Python was used, confirm its one-line fallback reason is present.
```

## Setup — flint-chart-mcp

Install or run the server with `npx -y flint-chart-mcp`.

Register it with the Codex CLI in `~/.codex/config.toml`:

```toml
[mcp_servers.flint-chart]
command = "npx"
args = ["-y", "flint-chart-mcp"]
```

Register it with Claude using `claude mcp add flint-chart -- npx -y flint-chart-mcp`.

The fallback agent skill lives at `agent-skills/flint-chart-author/` in the
`microsoft/flint-chart` repository. The flint-chart Python port is preview-only and not released;
do not instruct users to install it with `pip`.

## Why flint-chart

Microsoft Research's flint-chart compiles simple specifications into polished Vega-Lite, ECharts,
Chart.js, Plotly, and Excel charts while keeping rendered deliverables consistent and avoiding ad
hoc plotting code.
