---
name: grafana-queries
description: Write PromQL and LogQL queries in Grafana against Prometheus and Loki data sources. Use when building panel queries, exploring metrics and logs, or debugging query results.
---

# Grafana Queries: PromQL and LogQL

## PromQL essentials

Selectors and matchers:

```promql
http_requests_total{job="api", status=~"5.."}
```

Counters: never graph raw counters; use per-second rates over a window.
In Grafana panels prefer `$__rate_interval` as the window:

```promql
sum(rate(http_requests_total{job="api"}[$__rate_interval]))
sum by (route) (rate(http_requests_total[$__rate_interval]))   # per route
```

Errors as a ratio:

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/ sum(rate(http_requests_total[5m]))
```

Latency percentiles from histograms (classic buckets need `le` preserved):

```promql
histogram_quantile(0.95,
  sum by (le, route) (rate(http_request_duration_seconds_bucket[5m])))
```

Gauges: aggregate directly (`avg`, `max`, `min`); `increase()` for totals
over a range; `avg_over_time`, `max_over_time` for smoothing. `offset 1w` and
subtraction give week-over-week comparisons.

Pitfalls: aggregating away `le` before `histogram_quantile` (wrong results),
`rate` windows smaller than 2x scrape interval (gaps), mixing `sum` across
different metrics' label sets without `on()/ignoring()`.

## LogQL essentials

Every query starts with a stream selector, then a pipeline:

```logql
{app="api", env="prod"} |= "error" != "healthz"
{app="api"} | json | status >= 500 | line_format "{{.method}} {{.path}}"
{app="api"} | logfmt | duration > 500ms
```

- Line filters: `|=` contains, `!=` not contains, `|~` regex, `!~` not regex.
  Put the cheapest, most selective filters first.
- Parsers: `json`, `logfmt`, `pattern`, `regexp` extract labels for
  filtering and formatting.

Metric queries turn logs into time series (usable in panels and alerts):

```logql
sum by (status) (rate({app="api"} | json [5m]))
count_over_time({app="api"} |= "error" [10m])
quantile_over_time(0.95, {app="api"} | json | unwrap duration_ms [5m])
```

Keep stream label cardinality low (no user ids as labels); extract high
cardinality fields with parsers at query time instead.

## Data sources in Grafana

- Panels reference a data source by `uid`; use a `datasource` template
  variable for portability.
- Explore is the fastest place to iterate on a query before pasting it into
  a panel; it supports split view to correlate metrics with logs.
- Mixed data source panels can overlay Prometheus and Loki series.
- The bundled mcp-grafana server exposes query tools for Prometheus and Loki
  (plus metadata: label names, values, metric names), so queries can be run
  and refined against your live instance from Caeros.
