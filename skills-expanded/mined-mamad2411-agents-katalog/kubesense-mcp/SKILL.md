---
name: kubesense-mcp
description: How to use KubeSense MCP tools to query logs, traces, and metrics from Kubernetes clusters. Covers tool selection, the discovery-first workflow, and links to datasource-specific skills.
---

# KubeSense MCP

KubeSense MCP provides observability tools for querying logs, traces, and metrics from Kubernetes clusters.

## Tools

| Tool                      | Purpose                                       |
| ------------------------- | --------------------------------------------- |
| `get-trace-or-log-fields` | Discover available fields for logs or traces  |
| `get-available-metrics`   | Discover available metric names               |
| `get-metric-labels`       | Get label names for a specific metric         |
| `search-logs`             | Browse raw log records (max 10 rows)          |
| `search-traces`           | Browse raw trace/span records (max 10 rows)   |
| `analyze-logs`            | Run aggregated analysis on logs               |
| `analyze-traces`          | Run aggregated analysis on traces             |
| `analyze-metrics`         | Execute PromQL queries on metrics             |
| `analyze-telemetry`       | Multi-datasource queries with formula support |

## Discovery-First Rule

**Always discover before querying.** Never guess field names or metric names.

```
logs/traces:  get-trace-or-log-fields  →  search-logs / search-traces / analyze-logs / analyze-traces
metrics:      get-available-metrics    →  get-metric-labels  →  analyze-metrics
```

## Choosing the Right Tool

- **Show me recent logs** → `search-logs`
- **How many errors in the last hour?** → `analyze-logs` with `row_count` + error filter
- **P99 latency for a service** → `analyze-traces` with `p99` aggregation on `duration`
- **CPU / memory usage** → `get-available-metrics` → `analyze-metrics`
- **Error rate as a percentage** → `analyze-telemetry` with a formula query

## Query Types

All `analyze-*` tools accept a `queryType`:

- `"range"` — time-series values over the given window (for trends)
- `"instant"` — single point-in-time snapshot (for totals/counts)

## Time Ranges

All tools require `from_time` and `to_time` as ISO 8601 strings, e.g.:

```
"from_time": "2026-04-23T10:00:00Z"
"to_time":   "2026-04-23T10:30:00Z"
```

Start narrow (15–30 min) and widen if needed.

## Filters

The `filters` parameter in `search-logs`, `search-traces`, `analyze-logs`, and `analyze-traces` accepts a SQL-like WHERE clause.

### Operators

| Operator          | Example                            | Notes                                              |
| ----------------- | ---------------------------------- | -------------------------------------------------- |
| `=`               | `level = 'ERROR'`                  | Exact match                                        |
| `!=`              | `status != 'ok'`                   | Not equal                                          |
| `>` `<` `>=` `<=` | `duration_ms > 500`                | Comparisons; use unquoted numbers for float fields. Filter trace latency via `duration_ms` (ms), not the ns `duration` field |
| `IN`              | `level IN ('ERROR', 'WARN')`       | Matches any value in list                          |
| `NOT IN`          | `namespace NOT IN ('kube-system')` | Excludes values in list                            |
| `LIKE`            | `workload LIKE '%api%'`            | `%` is wildcard                                    |
| `NOT LIKE`        | `pod_name NOT LIKE '%debug%'`      | Negative pattern match                             |

### Combining Conditions

```
level = 'ERROR' AND namespace = 'production'
```

```
status = 'error' AND (workload = 'api-server' OR workload = 'auth-service')
```

### Value Types

- **Strings** — always single-quoted: `workload = 'my-service'`
- **Numbers** — unquoted: `duration_ms > 500` (filter trace latency in ms via `duration_ms`)

### Examples

```
level IN ('ERROR', 'FATAL') AND workload LIKE '%payment%'
```

```
status = 'error' AND protocol_type = 'HTTP' AND return_code = '500'
```

```
duration_ms > 500 AND workload = 'checkout-service'
```

## Datasource Skills

For detailed field references, examples, and query patterns, read the datasource-specific skill:

- **[kubesense-logs](./kubesense-logs/SKILL.md)** — Discover fields, search raw logs, aggregate with counts/percentiles, filter syntax
- **[kubesense-apm](./kubesense-apm/SKILL.md)** — Discover fields, search raw spans, analyze latency and errors, filter syntax
- **[kubesense-metrics](./kubesense-metrics/SKILL.md)** — Discover metrics, get labels, write PromQL queries

## Multi-Query Reference

- [multi-query.md](multi-query.md) — Multi-datasource queries and formula expressions with `analyze-telemetry`
