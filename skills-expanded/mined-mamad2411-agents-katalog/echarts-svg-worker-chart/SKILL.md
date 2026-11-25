---
tags: [design, echarts, svg, worker, chart]
name: echarts-svg-worker-chart
description: High-performance chart component using ECharts with custom SVG overlays (markLine/markArea/markPoint), worker thread data processing, and brush selection interaction
category: design
trigger: When building performance-critical charts with custom overlays, worker-based data processing, or brush/drag selection interactions
version: 1.0.0
source_project: lucida-ui
---

# ECharts SVG Worker Chart

## Architecture

```
ChartSvg (forwardRef + useImperativeHandle)
  ├── ECharts instance (canvas/svg renderer)
  ├── Custom SVG overlays (markLine, markArea, markPoint)
  ├── Worker thread (data transformation, aggregation)
  └── Event system (hover, drag, brush selection)
```

## Steps

1. **Create chart component** with `forwardRef` + `useImperativeHandle`:
   - Expose external API: `setOption()`, `resize()`, `getDataIndex()`, `dispatchAction()`
   - Internal state: ECharts instance ref, overlay positions, selected indices

2. **Offload data processing to Web Worker**:
   - Heavy operations (aggregation, downsampling, unit conversion) run in worker
   - Worker posts processed data back; component calls `setOption()` on ECharts instance
   - Prevents UI thread blocking for large datasets

3. **Add custom SVG overlays**:
   - `markLine`: threshold lines, baselines (rendered as ECharts markLine series)
   - `markArea`: highlighted ranges (time windows, anomaly zones)
   - `markPoint`: annotations at specific data points
   - Configure via `CustomChartOptions` prop: `{ markLine, markArea, smooth, isStacked, lineStyle }`

4. **Implement brush selection**:
   - Enable ECharts brush toolbox action
   - `chartEventNew.ts` handles brush start/end events
   - Track selected data indices for drill-down or time range sync
   - Drag interaction: mouse events for custom drag behavior (pan, zoom region)

5. **Chart variants** (compose from base):
   - `ChartNew`: standard line/bar/area with Sirius styling
   - `ScatterChart`: scatter plot with custom point renderers
   - `HexagonChart`: hexbin layout via `hexagonUtil.ts`
   - `SankeyChart` / `TreemapChart`: flow/hierarchy visualizations

## Key details
- `useParentSize` hook for responsive dimension tracking
- Color scheme injection from design tokens
- Legend can be separate grid component or inline within chart
