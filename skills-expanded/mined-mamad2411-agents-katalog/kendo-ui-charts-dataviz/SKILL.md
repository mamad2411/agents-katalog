---
name: kendo-ui-charts-dataviz
description: Use when implementing or reviewing Kendo UI charts and data visualizations for large datasets, drill-down, cross-filtering, and accessible interaction behavior.
---

# Kendo UI Charts and Data Visualization

## Specialization

Implement and review Kendo UI charting patterns that remain accurate, performant, and interpretable under real-world data volume, interactive filtering, and multi-series configuration.

## Trigger Conditions

- A feature includes Kendo Chart, Sparkline, StockChart, or Gauge components.
- Visualization needs drill-down, linked filtering, or coordinated interactions.
- Large datasets impact render speed or readability.
- Axis, tooltip, legend, or series semantics are inconsistent across dashboards.
- Accessibility and keyboard/screen-reader expectations apply to visualization surfaces.

## Scope Boundaries

In scope:

- Chart type selection and option contract design.
- Series, category, and axis mapping validation.
- Drill-down and cross-filter interaction patterns.
- Data reduction and rendering strategy for large volumes.
- Visualization clarity checks: legends, labels, tooltip density.

Out of scope:

- Generic DataSource transport contracts (see `kendo-ui-data-binding`).
- Generic theming governance (see `kendo-ui-theming`).
- Final release disposition (see `kendo-ui-quality-gate`).

## Inputs

- Visualization goals and decision tasks.
- Data shape (time series, categorical, stacked, mixed).
- Expected volume, update cadence, and latency tolerance.
- Dashboard context and interaction requirements.

## Required Outputs

- Chart configuration contract aligned to analysis intent.
- Interaction model for drill-down/cross-filter behavior.
- Performance strategy for rendering and update cadence.
- Accessibility notes for fallback text and interaction semantics.
- Test scenarios for correctness under filtering and data refresh.

## Core Patterns

### Multi-Series Time Chart

```javascript
$("#revenueChart").kendoChart({
    dataSource: revenueData,
    series: [
        { type: "line", field: "actual", name: "Actual" },
        { type: "line", field: "forecast", name: "Forecast" }
    ],
    categoryAxis: { field: "month" },
    tooltip: { visible: true, format: "{0:c}" },
    legend: { position: "bottom" }
});
```

### Drill-Down Handler

```javascript
seriesClick: function(e) {
    // Route filter state to a detail view or linked Grid.
    applyDetailFilter({ series: e.series.name, category: e.category });
}
```

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Deliver one chart correctly | Data mapping and labels are correct |
| L2 Delivery | Add interactive drill-down or linked filtering | Interaction contract is deterministic |
| L3 Hardening | Operate with large datasets and refreshes | Performance and readability validated |
| L4 Expert | Standardize dataviz pattern library | Reusable chart specifications documented |
