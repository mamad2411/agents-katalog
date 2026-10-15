---
name: kubesense-dashboards
description: Generate complete KubeSense dashboard JSON configurations (preset format) based on user requirements for panels, metrics, logs, traces, variables, and grid layouts.
---

# KubeSense Dashboard JSON Generator

Generate complete KubeSense dashboard JSON configurations (preset format) based on user requirements.

## When to Use

User asks to:

- "Create a dashboard for..."
- "Give me the dashboard JSON for..."
- "Build a dashboard with panels for..."
- "Generate a dashboard preset"

## Discover Fields First (KubeSense MCP)

If the KubeSense MCP server is available, use it to discover the real fields,
metrics, and labels before writing queries — never guess field names used for
grouping (`groupBy`), filtering (`filters`), or aggregation.

| To find...                                  | MCP tool                  |
| ------------------------------------------- | ------------------------- |
| Log/trace fields for `groupBy` & `filters`  | `get-trace-or-log-fields` |
| Available metric names (`selectedMetric`)   | `get-available-metrics`   |
| Labels of a metric (for `by` aggregations)  | `get-metric-labels`       |

Use the discovered field names verbatim (including whether a field is an
attribute — set `is_attribute` accordingly). If the MCP server is **not**
available, fall back to the user-provided field names and note that they should
be verified against the live datasource.

## Output Format

Always output the complete dashboard JSON in this structure:

```json
{
  "name": "<dashboard name>",
  "description": "<description>",
  "preset": "<stringified JSON of the preset object>"
}
```

> [!IMPORTANT]
> `preset` is a **JSON string**, NOT a nested object. The import validator
> defines `preset: z.string()` and only runs the preset schema check after
> `JSON.parse(preset)`. If you emit `preset` as a raw object, import fails with
> _"does not match the dashboard preset schema"_.
>
> The object that gets stringified has this shape:
>
> ```json
> {
>   "gridLayout": [],
>   "panels": [],
>   "variables": [],
>   "subGrids": [],
>   "subGridLayout": []
> }
> ```
>
> Only `gridLayout` and `panels` are required; the rest default to `[]`.

## Schema Reference

### Panel (`panelEditorFormValuesBaseSchema`)

```json
{
  "name": "string (required)",
  "description": "string (optional)",
  "panelType": "timeSeries | stat | table | list | bar | pie | topList | spl",
  "queries": [],
  "config": {}
}
```

### Panel Config (defaults)

```json
{
  "lineWidth": 1.5,
  "fillOpacity": 0,
  "stackSeries": false,
  "showTrend": false,
  "showLabel": false,
  "showPercentageChange": false,
  "percentageChangeColorMode": "standard",
  "legendVisibility": true,
  "legendPlacement": "bottom",
  "tooltipMode": "single",
  "yAxisLabelFormatter": "auto",
  "step": "auto",
  "thresholds": [],
  "enableThresholds": true,
  "valueOptions": { "show": "calculate", "calculation": "last" },
  "colorPalette": "default"
}
```

> [!NOTE]
> `mergeTables` accepts only the literal value `true` (`z.literal(true)`). Omit
> it entirely unless you are merging multiple table queries on a shared group-by
> key — in that case set `"mergeTables": true`. Never emit `"mergeTables": false`.

### Metrics Query

```json
{
  "selectedMode": "metrics",
  "label": "A",
  "selectedMetric": "metric_name",
  "functions": [],
  "filters": {},
  "queryMode": "builder",
  "visible": true,
  "variables": [],
  "labelOptions": { "type": "auto" },
  "pagination": { "page": 1, "page_size": 50 },
  "fieldConfig": {}
}
```

### Logs/Traces Query

```json
{
  "selectedMode": "logs",
  "label": "A",
  "filters": {},
  "queryMode": "builder",
  "filterMode": "MFD",
  "visible": true,
  "variables": [],
  "labelOptions": { "type": "auto" },
  "aggregation": { "function": "row_count" },
  "groupBy": [],
  "pagination": { "page": 1, "page_size": 50 },
  "sorting": {
    "sortBy": { "field": "", "type": "string", "is_attribute": false },
    "sortOrder": "ASC"
  },
  "query": "",
  "chart_type": "table",
  "columnFields": [],
  "xaxis": "auto",
  "yaxis": "auto",
  "source": "auto",
  "topListLabel": [],
  "topListValue": "auto",
  "fieldConfig": {}
}
```

> [!NOTE]
> `chart_type` is a query-level field with its own enum, separate from the
> panel-level `panelType`. Valid values: `table`, `bar`, `pie`, `topList`,
> `timeseries` (lowercase). It does **not** accept `stat` or `timeSeries` — use
> `panelType` for those distinctions and set `chart_type` to one of the values
> above (e.g. `timeseries` for a `timeSeries` panel, `table` for a `stat` panel).

### Formula Query

```json
{
  "selectedMode": "formula",
  "label": "C",
  "expression": "A+B",
  "visible": true,
  "labelOptions": { "type": "auto" },
  "fieldConfig": {}
}
```

### Metrics Query Functions (`panelMetricsQueryFormulaSchema`)

**Range:**

```json
{
  "type": "range",
  "name": "rate | increase | resets",
  "arguments": [{ "arg_name": "over", "arg_value": "5m" }]
}
```

**Aggregations:**

```json
{
  "type": "aggregations",
  "name": "sum | avg | max | min | count | No_Aggregations",
  "arguments": [{ "arg_name": "by", "arg_value": ["label1", "label2"] }]
}
```

**Top/Bottom:**

```json
{
  "type": "top_bottom",
  "name": "top | bottom",
  "arguments": [
    { "arg_name": "k", "arg_value": 5 },
    { "arg_name": "by", "arg_value": "max" }
  ]
}
```

**Rollup:**

```json
{
  "type": "rollup",
  "name": "avg_over_time | sum_over_time | max_over_time | min_over_time | count_over_time | last_over_time | absent_over_time | present_over_time | increases_over_time | range_over_time | quantile_over_time",
  "arguments": [{ "arg_name": "over", "arg_value": "5m" }]
}
```

**Comparison:**

```json
{
  "type": "comparison",
  "name": "greater | lesser | greater_than_or_equal | less_than_or_equal | equal | not_equal",
  "arguments": [{ "arg_name": "than", "arg_value": 100 }]
}
```

**Transform:**

```json
{
  "type": "transform",
  "name": "abs | clamp | clamp_max | clamp_min | round | histogram_quantile | sort | sort_desc",
  "arguments": [{ "arg_name": "quantile", "arg_value": 0.95 }]
}
```

### Grid Layout Item

```json
{ "i": "panel-0", "x": 0, "y": 0, "w": 6, "h": 4 }
```

- `i`: unique ID (use `panel-0`, `panel-1`, etc.)
- `x`: 0-11 (12-column grid)
- `y`: auto-increment based on previous items
- `w`: 1-12
- `h`: height in 100px units

### Variable (`dashboardVariableSchema`)

A variable has a top-level `name` + `description` and a `meta` object that is a
**discriminated union on `meta.variableType`**. There is no `id`, `label`, or
`multiSelect` field.

```json
{
  "name": "service",
  "description": "",
  "meta": { "variableType": "...", "...": "..." }
}
```

- `name`: required, non-empty, max 20 chars, must match `^[a-zA-Z_][a-zA-Z0-9_]*$`.
- `description`: required string (use `""` if none — it is NOT optional).
- `meta`: required; shape depends on `variableType`.

`selectType` (where present) is `"single"` or `"multiple"`.

**Textbox** (`variableType: "textbox"`):

```json
{ "variableType": "textbox", "defaultValue": "", "value": "" }
```

**Static / custom list** (`variableType: "custom"`):

```json
{
  "variableType": "custom",
  "options": ["a", "b"],
  "value": [],
  "selectType": "multiple"
}
```

`options` is required and must have at least 1 entry.

**Traces / Logs** (`variableType: "traces"` or `"logs"`):

```json
{
  "variableType": "traces",
  "fieldMeta": { "field": "service", "type": "string", "is_attribute": false },
  "value": [],
  "selectType": "single",
  "filters": {},
  "filterMode": "MFD"
}
```

`fieldMeta.field` is required. `filterMode` is `"MFD"` or `"ADVANCED_QUERY"`.

**Metrics** (`variableType: "metrics"`):

```json
{
  "variableType": "metrics",
  "metric": "metric_name",
  "fieldMeta": { "field": "service", "type": "string", "is_attribute": false },
  "value": [],
  "selectType": "single"
}
```

`metric` and `fieldMeta` are both required.

### Sub-Grid (Row)

```json
{
  "id": "subgrid-uuid",
  "title": "Row Name",
  "collapsed": false,
  "panels": [],
  "gridLayout": []
}
```

## Y-Axis Formatter Options

`auto`, `bytes`, `nanoseconds`, `microseconds`, `milliseconds`, `seconds`, `percent`, `percent_unit`, `ops`, `bps`, `short`, `celsius`, `fahrenheit`, `none`

Use `nanoseconds` for any panel aggregating over trace `duration` (it auto-scales ns → µs/ms/s).

## Rollup Time Ranges

`30s`, `1m`, `5m`, `30m`, `1h`, `1d`

## Aggregation Functions (logs/traces)

`row_count`, `unique_count`, `avg`, `sum`, `max`, `min`, `p99`, `p95`, `p90`, `p75`, `p50`

## Trace Duration Fields

Traces expose **two** duration fields — pick by operation:

- **`duration`** — span duration in **nanoseconds**. Use in panel `aggregation.fields`
  (latency `p99`/`p95`/`avg`/…) and in `groupBy`. This is the field returned by
  `get-trace-or-log-fields`. The aggregated value is in **nanoseconds**, so set the
  panel's `config.yAxisLabelFormatter: "nanoseconds"` — the formatter auto-scales
  ns → µs/ms/s for display. (Don't use a formula to pre-convert; just pick the
  `nanoseconds` unit.)
- **`duration_ms`** — span duration in **milliseconds**. Use when **filtering** by
  latency. `duration_ms` is **not returned by field discovery** — use it verbatim
  with `is_attribute: false`. Because MFD filters are equality-based, express a
  latency threshold with `filterMode: "ADVANCED_QUERY"` and a `query` like
  `duration_ms > 500`. Never filter on the raw ns `duration` field.

## Color Palette Keys

`default`, `classic`, `warm`, `cool`, `vivid`, `muted`

## Threshold Colors

`green`, `yellow`, `orange`, `red`, `blue`, `purple`

## Rules

1. Always output valid JSON — no markdown wrapping unless in a code block
2. Use `panel-0`, `panel-1` etc. for layout `i` values
3. Grid `x` values: place panels side by side (0, 6 for 2-column; 0, 4, 8 for 3-column)
4. Grid `y` values: increment based on previous panel height
5. Each metrics query needs a unique `label` (A, B, C...) for formula references
6. Formula expressions use query labels: `A+B`, `A/B*100`, `(A-B)/A*100`
7. Include `config` on every panel with defaults unless user specifies otherwise
8. For time series panels, typically use `rate()` + aggregation as first two functions
9. Empty `filters: {}` is valid — no need to populate unless user specifies filters
10. Generate UUIDs for sub-grid IDs (`subGrids[].id`). Variables have no `id`.
11. `preset` MUST be a stringified JSON string in the final output, not a nested object
12. `chart_type` (query-level) is one of `table | bar | pie | topList | timeseries` — never `stat`/`timeSeries`
13. Only set `mergeTables: true` when merging table queries; otherwise omit it
14. When the KubeSense MCP server is available, discover fields/metrics/labels with `get-trace-or-log-fields`, `get-available-metrics`, and `get-metric-labels` before writing queries — don't guess grouping/filtering field names
