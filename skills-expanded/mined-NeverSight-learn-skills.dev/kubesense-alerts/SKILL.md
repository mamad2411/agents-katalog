---
name: kubesense-alerts
description: Generate KubeSense alert rule JSON (the import/export format) from user requirements over metrics, logs, and traces — threshold, change, and no-data conditions — for import-and-review in the Alerts UI, and translate Datadog monitors into equivalent KubeSense alerts.
---

# KubeSense Alert Rule Generator

Generate a valid KubeSense **alert rule** as JSON that the user imports through
the Alerts UI (**Alert Events / Alert Rules tab → "Import JSON"**). The JSON opens
in the create editor — the user reviews every field (and the live condition chart)
and clicks **Create**. Nothing is written until they confirm.

This is the **same JSON the "Export" button produces**, so an exported rule can be
edited and re-imported, and a generated rule round-trips cleanly.

## When to Use

User asks to:

- "Create an alert when..." / "Alert me if..."
- "Give me the alert JSON / config for..."
- "Migrate / convert this Datadog monitor to KubeSense" → also read
  [datadog-migration.md](./datadog-migration.md)

## Two hard rules

1. **Discover real names first.** Never invent metric names, log/trace fields, or
   group-by labels. A wrong name doesn't just fail to fire — the engine errors on
   every evaluation ("unknown field") and **holds the rule's current state**. A new
   rule silently never fires; worse, a rule that is *already firing* **freezes —
   it never resolves, and editing its threshold has no effect** (the query errors
   before the threshold is ever checked). This is the #1 real-world failure, so the
   group-by/filter field names below must be EXACT. Use the KubeSense MCP tools:

   | You need… | Call |
   |---|---|
   | A metric name | `get-available-metrics` → `get-metric-labels` |
   | Log/trace fields, group-by keys, filter values | `get-trace-or-log-fields` |
   | Channel ids for `notification_channel_ids` | `GET /api/alerts/notification-channels` |

   **If the MCP tools aren't connected**, you may still generate logs/traces rules
   using the verified field catalogs in this skill (see the Logs and Traces query
   sections — these are canonical field names, not guesses). You may NOT invent
   metric names this way — PromQL metric names are cluster-specific, so for metrics
   rules without MCP, ask the user for the metric name or to Export a reference rule.
   Either way, tell the user to confirm names + values on the import editor's
   condition chart before clicking Create.

2. **For an unfamiliar rule shape, export a reference first.** Ask the user to
   Export a similar existing rule from the UI, or fetch one
   (`GET /api/alerts/rules`), and modify it — the exact `query_config` shape is
   then guaranteed. Generate from scratch only for shapes you're confident in.

## Output Format (import = export format)

```json
{
  "name": "High pod CPU {{pod}}",
  "description": "Pod CPU above 80% for 5 minutes",
  "severity": "warning",
  "enabled": true,
  "query_type": "metrics",
  "query_config": [ /* see Query objects */ ],
  "metric_query_label": "A",
  "threshold_operator": "greater_than_or_equal",
  "threshold_value": 0.8,
  "condition_type": "",
  "evaluation_interval": "1m",
  "time_window": "5m",
  "frequency_type": "at_least_once",
  "labels": {},
  "notification_channel_ids": [],
  "route_by_labels": false,
  "no_data_state": "normal",
  "include_samples": false,
  "sample_limit": 5,
  "unit": "percent_unit"
}
```

Note the **flat** fields (`threshold_operator`/`threshold_value`, not a nested
`threshold`), the **plain durations** (`evaluation_interval: "1m"`, `time_window:
"5m"` — not `*_prometheus_format`), and `notification_channel_ids` (not
`notificationChannels`). This is the import/export shape, NOT the raw POST body.

## Field Reference

| Field | Values / notes |
|---|---|
| `name` | Required. `{{field}}` placeholders resolve per firing series — the `field` MUST be a group-by key (PromQL `by (...)` label, or a logs/traces `groupBy` field), e.g. group `by (pod)` → `High CPU {{pod}}`. A placeholder with no matching group-by renders empty. |
| `severity` | `critical` \| `error` \| `warning` \| `info` |
| `query_type` | the first query's mode: `metrics` \| `logs` \| `traces` |
| `threshold_operator` | `greater_than` \| `greater_than_or_equal` \| `less_than` \| `less_than_or_equal` \| `equals` \| `not_equals` |
| `threshold_value` | number to compare against |
| `frequency_type` | `at_least_once` (any breach) \| `more_than_once` (≥ `breaches_count`) \| `always` (every eval in window breached) |
| `breaches_count` | int ≥ 2 — only for `more_than_once` |
| `breach_counting_window` | optional duration to count breaches over; defaults to `time_window` |
| `evaluation_interval` | how often the rule runs: `30s`,`1m`,`5m`,`1h`,`1d` |
| `time_window` | how far back the query looks: same duration format |
| `condition_type` | `""` threshold (default) \| `change` \| `change_percent` \| `new_value` |
| `compared_to` | for change/new_value: a duration **string** like `"1h"` (the historical lookback) |
| `metric_query_label` | label of the thresholded query. Single query → its label (`A`). Formula → the formula label. |
| `notification_channel_ids` | array of channel **ids** (from the channels endpoint) |
| `route_by_labels` | `false` route by listed channels; `true` route via each channel's label matchers |
| `no_data_state` | `normal` resolve (default) \| `firing` fire when no data (metric vanished) \| `previous` hold state |
| `include_samples` / `sample_limit` | LOGS rules only — attach up to N matching rows to notifications |
| `unit` | display only (never affects evaluation) — but **set it to match the value** so the chart/notifications read correctly: `ns` for trace duration/latency · `bytes` for byte metrics (memory/disk/network) · `percent` for ratios & error-rates (a formula `×100`) · `percent_unit` for 0–1 fractions (e.g. CPU usage) · `ms` for millisecond latencies · `short` or `""` for plain counts. |
| `enabled` | `true` |

## Query objects (`query_config[]`)

Each query has a `label` (A, B, C…), `selectedMode`, and `visible: true`.

### Metrics — PromQL (preferred)

```json
{ "label": "A", "selectedMode": "metrics", "visible": true, "queryMode": "code",
  "promql": "max by (pod)(rate(container_cpu_usage_seconds_total{namespace=\"prod\"}[5m]))" }
```

- Put grouping in PromQL `by (...)`; each series = one firing instance.
- `metric_query_label`: `"A"`.

### Logs (row-count / aggregation)

```json
{ "label": "A", "selectedMode": "logs", "visible": true,
  "value_operation": "row_count",
  "groupBy": [ { "field": "workload", "type": "string", "is_attribute": false } ],
  "raw_filters": { "level": ["ERROR"] },
  "filters": { "level": ["ERROR"] } }
```

- `value_operation`: `row_count` \| `unique_count` \| `avg` \| `sum` \| `max` \| `min` \| `p99` \| `p95` \| `p90` \| `p75` \| `p50`.
- **Log field names** — use these EXACT strings for `groupBy[].field` and filter
  keys. They are the intersection of what the webapp persists (`LOG_COLUMNS`) and
  what the engine accepts (`LogsAllowedColumns`); anything else freezes the rule
  with "unknown field" and it silently never fires:
  `workload`, `namespace`, `cluster`, `pod_name`, `container_name`, `host`,
  `level`, `format`, `source`, `region`, `app_version`, `customer_identifier`.
- Logs use the **storage names** `pod_name`/`container_name` (NOT `pod`/`container`)
  and `host` for the node (NOT `node`/`node_name`). `level` is the severity field
  (traces use `status`).
- ⚠️ **Not accepted by the alert engine — do NOT use** (selectable in the explorer
  but absent from `LogsAllowedColumns`, so they freeze a rule): `env_type` and the
  log body. Stick to the list above.
- Provide BOTH `raw_filters` and `filters` with the same `{ field: [values] }` map.

### Traces (count / latency)

```json
{ "label": "A", "selectedMode": "traces", "visible": true,
  "value_operation": "p95",
  "fields": [ { "field": "duration", "type": "float", "is_attribute": false } ],
  "groupBy": [ { "field": "workload", "type": "string", "is_attribute": false } ],
  "raw_filters": { "status": ["error"] }, "filters": { "status": ["error"] } }
```

- ⚠️ **Trace FILTER keys and GROUP-BY fields use DIFFERENT names** — the webapp has
  two trace catalogs. Get this wrong and the editor silently drops the field.
  - **`raw_filters` / `filters` keys → use the STORAGE name** (the trace filter
    dropdown is keyed by storage columns; the engine accepts them):

    | intent | filter key |
    |---|---|
    | service | `app_service` |
    | resource / endpoint | `clustered_resource` |
    | HTTP method | `subtype` |
    | HTTP status code | `return_code` |
    | role (client/server) | `kind` |
    | protocol | `protocol_type` |
    | node | `node_name` |
    | pod / instance | `pod_name` |
    | container | `container_name` |
    | status (ok/error), workload, namespace, cluster, source, region, app_version, server, client, *_namespace, operation_name, partner_cluster | same name |

  - **`groupBy[].field` → use the CATALOG name** (the engine strictly validates
    group-by against `TraceAllowedColumns`): `workload`, `app_service`, `namespace`,
    `cluster`, `node`, `pod`, `container`, `server`, `client`, `server_namespace`,
    `client_namespace`, `source`, `region`, `app_version`, `operation_name`,
    `partner_cluster`, `customer_identifier`, `status`, `protocol`, `role`, `method`,
    `resource`.
  - **value field**: `duration`.
  - Do NOT use `status_code`, `resource`, `method` as *filter* keys (editor drops
    them — use `return_code`, `clustered_resource`, `subtype`). Do NOT use
    `clustered_resource`/`subtype` as *group-by* fields (engine freezes — use
    `resource`/`method`).
- **For APM "by service"**, either `app_service` (the instrumented service name)
  or `workload` (the k8s workload) works. Note: on aggregated windows (≥60s, which
  latency/count rules always use) `app_service` resolves to the `app_name` rollup
  column — so service grouping is by `app_name` there. Both are reliable; pick
  `app_service` for service-name semantics, `workload` for k8s-object semantics.
- Traces use `status` for outcome (logs use `level`), `pod`/`container` (not
  `pod_name`); there is no trace body field.
- ⚠️ **Trace `duration` is stored in NANOSECONDS** (`uint64`); p50/p95/p99 are
  computed on the raw value, so latency thresholds MUST be in ns. Convert from the
  user's stated time:

  | User says | `threshold_value` (ns) |
  |---|---|
  | 100ms | `100000000` |
  | 250ms | `250000000` |
  | 500ms | `500000000` |
  | 1s | `1000000000` |
  | 2s | `2000000000` |

  General rule: `ns = ms × 1_000_000` = `seconds × 1_000_000_000`. Set `unit: "ns"`.
  Always tell the user to confirm the value reads correctly on the import editor's
  condition chart.
- Latency: `value_operation` = `p99`/`p95`/`p50`/`avg` over `fields: [{duration}]`.

**Complete trace-latency example** (p95 > 500ms by service — note `workload` grouping,
ns threshold, `unit: "ns"`):

```json
{
  "name": "High p95 latency {{workload}}",
  "description": "Service p95 latency above 500ms over 5m",
  "severity": "warning",
  "enabled": true,
  "query_type": "traces",
  "query_config": [
    { "label": "A", "selectedMode": "traces", "visible": true,
      "value_operation": "p95",
      "fields": [ { "field": "duration", "type": "float", "is_attribute": false } ],
      "groupBy": [ { "field": "workload", "type": "string", "is_attribute": false } ] }
  ],
  "metric_query_label": "A",
  "threshold_operator": "greater_than",
  "threshold_value": 500000000,
  "condition_type": "",
  "evaluation_interval": "1m",
  "time_window": "5m",
  "frequency_type": "at_least_once",
  "no_data_state": "normal",
  "notification_channel_ids": [],
  "route_by_labels": false,
  "unit": "ns"
}
```

### Formula (ratio / error-rate)

```json
"query_config": [
  { "label": "A", "selectedMode": "logs", "value_operation": "row_count", "visible": false },
  { "label": "B", "selectedMode": "logs", "value_operation": "row_count", "raw_filters": {"level":["ERROR"]}, "filters": {"level":["ERROR"]}, "visible": false },
  { "label": "C", "selectedMode": "formula", "expression": "(B/A)*100", "visible": true }
]
```

- `metric_query_label`: `"C"`. `unit`: `"percent"`.
- **Show only the evaluated query on the chart.** Set `visible: true` on the
  `metric_query_label` query (here `C`, the error rate) and `visible: false` on the
  helper queries (`A`, `B`). They're still **executed** (the formula needs them) and
  the engine ignores `visible` for evaluation — it only hides their raw-count series
  from the graph, so the chart shows the error-rate line alone, not the two counts.

## Condition types

| condition_type | Meaning | Extra |
|---|---|---|
| `""` | value vs threshold now | — |
| `change` | absolute change vs `compared_to` ago | `compared_to: "1h"` |
| `change_percent` | % change vs `compared_to` ago | `compared_to` |
| `new_value` | a group-by value unseen in the `compared_to` window appears | `compared_to`, logs/traces only |

## How the user applies it

1. Copy the JSON.
2. KubeSense → **Alerts → Alert Events or Alert Rules tab → "Import JSON"**.
3. Paste (or upload the `.json`) → **Review in editor**.
4. The rule opens prefilled; the user checks fields + the condition chart, then **Create**.

(Exported rules import the same way — so "tweak this rule" = Export → edit JSON → Import.)

## Multiple alerts → ONE array (bulk import)

When you generate **more than one rule** — e.g. migrating several Datadog monitors,
or a `warning`+`critical` split, or one rule per service — output a **single JSON
array**, not separate per-rule snippets:

```json
[
  { "name": "…", "query_type": "traces",  "query_config": [ … ], "threshold_operator": "greater_than", "threshold_value": 500000000, … },
  { "name": "…", "query_type": "metrics", "query_config": [ … ], "threshold_operator": "greater_than_or_equal", "threshold_value": 0.8, … }
]
```

- Each element is the **exact same object shape** as a single rule (above) — just listed in an array.
- The user **bulk-imports** the array: it's validated server-side, returns a **dry-run
  review** (per-rule valid / field problems), then creates the valid ones — invalid
  rules are reported, not silently dropped.
- Field validation is the same as a single rule, so the same EXACT field names apply
  to every element (a wrong group-by field is rejected up front, per rule).
- Emit **one** array even for two rules. Only emit a bare object when there is exactly
  one rule.

## Datadog migration

To convert a Datadog monitor, read **[datadog-migration.md](./datadog-migration.md)**.

## Rules

1. **Discover first** — validate every metric/field/group-by name via MCP before emitting.
2. Output the **import/export shape** (flat fields, plain durations, `notification_channel_ids`). **One rule → a single JSON object; multiple rules → ONE JSON array** `[ {…}, {…} ]` (see "Multiple alerts → ONE array"). One code block either way — never separate per-rule snippets.
3. Each query needs a unique `label`; formula `expression` references labels (`(B/A)*100`).
4. `metric_query_label` = the thresholded query (single → its label; formula → formula label).
5. Logs use `level`/`pod_name`/`container_name`; traces use `status`/`pod`/`container`. Give logs/traces filters as BOTH `raw_filters` and `filters`.
6. Durations are plain strings (`30s`,`1m`,`5m`,`1h`,`1d`) — NOT `*_prometheus_format`.
7. `more_than_once` needs `breaches_count` (≥2) and usually `breach_counting_window`.
8. `include_samples` is logs-only; `no_data_state: "firing"` only when metric disappearance is the incident.
9. `notification_channel_ids` are real ids from the channels endpoint; leave `[]` if unspecified.
10. Prefer **starting from an exported reference rule** for unfamiliar shapes — it guarantees the `query_config` is valid.
11. Tell the user to import via the UI and review before creating — never claim the alert was created.
12. **Multiple alerts (incl. Datadog bulk migration) → emit ONE JSON array of rule objects**, not N separate snippets, so they bulk-import in one pass.
13. **Set `unit` to match the value** — `ns` for trace duration/latency, `bytes` for byte metrics, `percent` for ratio/error-rate formulas, `percent_unit` for 0–1 fractions, `ms`/`short` otherwise.
14. For a status/code **class** (4xx, 5xx) or any range, use an **advanced-query** filter (`return_code LIKE "4__"`), not an enumerated `raw_filters` list.
15. **Chart shows only the evaluated query.** `visible: true` on the `metric_query_label` query; `visible: false` on every other query (e.g. the formula's helper counts). Helpers still run; this only hides their series from the graph.
