---
name: grafana-patterns
description: "When to activate: Grafana, dashboard, panel, variable, annotation, alert, data source, provisioning, Loki, tempo"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: devops
  language: devops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Grafana Patterns

## Dashboard Provisioning (as code)

```yaml
# grafana/provisioning/dashboards/myapp.yaml
apiVersion: 1
providers:
  - name: myapp
    type: file
    updateIntervalSeconds: 30
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

## Dashboard JSON Structure (key fields)

```json
{
  "title": "MyApp Overview",
  "uid": "myapp-overview",
  "refresh": "30s",
  "time": { "from": "now-1h", "to": "now" },
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "query": "label_values(kube_pod_info, namespace)",
        "refresh": 2
      },
      {
        "name": "service",
        "type": "query",
        "query": "label_values(http_requests_total{namespace=\"$namespace\"}, service)"
      }
    ]
  },
  "panels": []
}
```

## Standard Row Layout (Four Golden Signals)

```
Row 1: Traffic
  - Stat: Total RPS
  - Time series: RPS by endpoint

Row 2: Errors
  - Stat: Error rate %
  - Time series: Error rate over time
  - Table: Top erroring endpoints

Row 3: Latency
  - Stat: p99 latency
  - Time series: p50 / p95 / p99

Row 4: Saturation
  - Gauge: CPU utilization
  - Gauge: Memory utilization
  - Time series: Pod count / HPA status
```

## Common Panel Queries

```
# RPS Stat panel
sum(rate(http_requests_total{namespace="$namespace", service="$service"}[5m]))

# Error rate Time series
100 * sum(rate(http_requests_total{namespace="$namespace",status=~"5.."}[5m]))
    / sum(rate(http_requests_total{namespace="$namespace"}[5m]))

# p99 latency
histogram_quantile(0.99,
  sum(rate(http_request_duration_seconds_bucket{namespace="$namespace"}[5m])) by (le)
)

# Memory usage %
100 * container_memory_working_set_bytes{namespace="$namespace"}
    / container_spec_memory_limit_bytes{namespace="$namespace"}
```

## Grafana Alerting Rule

```yaml
apiVersion: 1
groups:
  - orgId: 1
    name: MyApp SLO
    folder: MyApp
    interval: 1m
    rules:
      - uid: myapp-error-rate
        title: High Error Rate
        condition: C
        data:
          - refId: A
            queryType: ''
            relativeTimeRange: { from: 600, to: 0 }
            datasourceUid: prometheus
            model:
              expr: |
                sum(rate(http_requests_total{status=~"5.."}[5m]))
                / sum(rate(http_requests_total[5m]))
          - refId: C
            datasourceUid: __expr__
            model:
              type: threshold
              conditions:
                - evaluator: { params: [0.01], type: gt }
                  query: { params: [A] }
        noDataState: OK
        execErrState: Alerting
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 1%"
```

## Loki Log Panel Query

```
{namespace="prod", pod=~"myapp-.*"} 
  | json 
  | level = "error" 
  | line_format "{{.message}} trace={{.trace_id}}"
```

## Key Rules
- Use dashboard UIDs for stable linking between dashboards
- Template variables make dashboards reusable across namespaces/services
- Provision dashboards as code — never rely on manual UI-only dashboards
- Use `$__rate_interval` instead of a hardcoded `[5m]` — adapts to scrape interval
- Link panels to runbooks via panel links for faster incident response
