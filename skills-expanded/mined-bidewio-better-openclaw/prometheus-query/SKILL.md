---
name: prometheus-query
description: "Query metrics and set up alerts using Prometheus at {{PROMETHEUS_HOST}}:{{PROMETHEUS_PORT}}."
metadata:
  openclaw:
    emoji: "🔥"
---

# Prometheus Query

Prometheus is available at `http://{{PROMETHEUS_HOST}}:{{PROMETHEUS_PORT}}` within the Docker network.

## Instant Query

```bash
curl -G "http://{{PROMETHEUS_HOST}}:{{PROMETHEUS_PORT}}/api/v1/query" \
  --data-urlencode 'query=up'
```

## Range Query

```bash
curl -G "http://{{PROMETHEUS_HOST}}:{{PROMETHEUS_PORT}}/api/v1/query_range" \
  --data-urlencode 'query=rate(http_requests_total[5m])' \
  --data-urlencode 'start=2024-01-01T00:00:00Z' \
  --data-urlencode 'end=2024-01-01T01:00:00Z' \
  --data-urlencode 'step=60'
```

## List Targets

```bash
curl "http://{{PROMETHEUS_HOST}}:{{PROMETHEUS_PORT}}/api/v1/targets"
```

## Tips for AI Agents

- Use PromQL for powerful metric queries: `rate()`, `sum()`, `histogram_quantile()`.
- Check target health at `/targets` to verify scrape configurations.
- Combine with Grafana for visual dashboards.
