---
name: fibery-reports
description: Build Fibery reports - charts, tables, and metric tiles over workspace data, including time-in-state and change-frequency analysis from history. Use when the user wants to chart, graph, or visualize Fibery data, needs a dashboard or KPI tile, asks how long items sit in a state, or wants an existing report changed.
---

# Fibery reports

Reports run on a separate engine (vizydrop) with its own field names,
expression language, and filter model. Nothing you learned from `schema` or the
`query` language carries over.

**Call `get_fibery_skill` with `{skill: "reports"}` for the full expression
catalog, palette list, and operator tables.** This skill covers the workflow
and the traps.

## The one rule that matters most

**Report field names are not Fibery field names.** `display_report_schema`
returns the flat set of field titles usable inside `[...]` in expressions, and
they differ from the `Space/Field` identifiers everywhere else. Skipping this
call and guessing an expression is the main cause of broken reports.

Call `display_report_schema` on the target databases before configuring any
dimension.

## Workflow

1. `schema` to get exact `Space/Database` names.
2. Decide the source mode (see below). It cannot be changed later.
3. `display_report_schema` with those databases and that mode.
4. `create_report` with `title`, `sources`, `sourceMode`, and optional
   `spaceName` (it defaults to the user's private space, which is often not
   what they want).
5. Configure. **The new report already contains one empty scatterplot tab.**
   Configure that tab with `update_tab` and `update_dimension` rather than
   adding a second one, or the user ends up with a blank tab beside the real
   chart.
6. Add further tabs with `add_chart_tab`, `add_table_tab`, `add_metric_tab`.

To edit an existing report: `get_reports_list` for the id, then `get_report`
to read current `tabId`, `tabType`, and per-dimension `id` values. Dimension
ids are server-assigned and can change when a tab is recreated, so always
re-read them immediately before `update_dimension` or `remove_dimension`.

## Source mode

`current` reads live entity state and is the default.

`historical` reads every modification event and is what you need when the user
asks:

- how long entities spent in a state
- how often a field changed
- for a timeline of state transitions

Historical mode adds `Modification ID`, `Modification Date`,
`Modification Valid To`, `Modified By`, and `Changed Fields` to the schema, and
new historical reports come with a `LAST 90 DAYS` filter already applied.

Average days in state:

```
AVG(SUM(DATEDIFF([Modification Date], IF([Modification Valid To] > NOW(), NOW(), [Modification Valid To]), 'minute'))/1440 by [Id])
```

`sourceMode` is fixed at creation. If the user asks to switch an existing
report, say so and offer to create a new one.

## Tab types

**Chart** uses `x` and `y` arrays plus optional `color`, `size`, and `label`.
Types are `line`, `bar`, `stacked-bar`, `area`, `stacked-area`, and
`scatterplot` (the server default, and rarely what a user actually wants;
pick deliberately).

**Table** takes `columns`, and groups automatically when a categorical column
sits alongside an aggregate column. Only use `groupBy` for a grouping key that
is not itself a visible column.

**Metric** takes `metrics`, and every expression must be a scalar aggregate.
`COUNT([ID])` is valid; `[Name]` is not.

## Expressions

```
[Name]                        raw categorical value
COUNT([ID])                   count of records
COUNT_DISTINCT([ID])          distinct count
SUM([Story Points])           sum
AVG([Estimate])               average
AUTO([Creation Date])         auto-grouped date, picks the granularity
MONTH([Creation Date])        explicit date grouping
RUNNING_SUM(SUM([Hours]))     cumulative
BINS([Users Count], 10)       numeric buckets
IFNONE([Owner], 'No Owner')   null replacement
```

Rules that reject a config:

- **No duplicate expressions** within the same `x`, `y`, `columns`, `metrics`,
  or `groupBy` array.
- **`color` and `size` take exactly one dimension each.**
- **On a faceted axis, categorical and date dimensions go before numeric
  ones.** For Sprint and record count on the same axis, `[Sprint]` first, then
  `COUNT([ID])`.

## Two filter layers, applied in order

`fieldConditions` filter raw rows **before** aggregation:

```json
{"field": "Priority", "operator": "is in", "value": ["High", "Critical"]}
{"field": "Creation Date", "operator": "range", "value": "LAST 90 DAYS"}
```

`dimensionConditions` filter aggregated values **after** aggregation, and the
`expression` must exactly match one already used as a dimension in that tab:

```json
{"expression": "COUNT([ID])", "operator": "greater than", "value": 10}
{"expression": "[Priority]", "operator": "in top", "value": 5}
```

"Only features with more than 10 linked bugs" is a dimension condition.
"Only features created this quarter" is a field condition. Getting these
backwards silently produces the wrong numbers.

Date ranges use relative strings: `TODAY`, `THIS WEEK`, `PREVIOUS MONTH`,
`THIS QUARTER`, `LAST 90 DAYS`, `PREVIOUS 6 MONTHS`,
`BETWEEN 6 QUARTERS AGO AND 2 MONTHS AGO`.

Enum filter values must come from the `enumOptions` block of
`display_report_schema`, not invented.

## Multiple sources

Passing more than one database to `sources` injects a synthetic
`Entity Database` field whose value is each row's source database title. Put it
on an axis or in `color` to split a cross-database report by source.

## Palettes

Pick by data shape, not by taste: categorical (`fibery2.0`, `category10`,
`tableau10`) for nominal categories, sequential (`blues`, `greens`) for ordered
data, diverging (`red_blue`, `spectral`) when there is a meaningful midpoint.
`fibery2.0` is the on-brand default.

Leave `showChartLabel` off unless the user asks for data labels.

## Reporting back

Say what the report shows, which source mode it uses, and where it lives. If
the user asked a question ("how long do bugs sit in review?"), answer it in
prose from the data as well as building the chart. A chart they have to
interpret alone is half an answer.
