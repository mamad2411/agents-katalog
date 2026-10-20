---
name: monitoring-patterns
description: "When to activate: monitoring, observability, SLO, SLI, SLA, alerting, dashboard, Prometheus, Grafana, Alertmanager, uptime, latency"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: devops
  language: devops
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# Monitoring Patterns

## SLO / SLI / SLA Definitions

```
SLI (indicator): The metric being measured
  → "99th-percentile request latency over 1 minute"

SLO (objective): The target for that metric
  → "p99 latency < 200ms for 99.9% of minutes in 30 days"

SLA (agreement): Business contract with consequences
  → "If availability < 99.5%, customers get credits"

Error budget = 1 - SLO target
  → 99.9% SLO = 0.1% error budget = ~43 minutes/month allowed downtime
```

## The Four Golden Signals

```
1. Latency   — how long requests take (p50, p95, p99)
2. Traffic   — requests per second (RPS)
3. Errors    — error rate (5xx / total)
4. Saturation — resource utilization (CPU, memory, disk, connections)
```

## Prometheus Alerting Rules

```yaml
groups:
  - name: myapp.slo
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "Error rate {{ $value | humanizePercentage }} exceeds 1%"
          runbook_url: "https://wiki.example.com/runbooks/high-error-rate"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le)
          ) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency {{ $value }}s exceeds 500ms"

      - alert: PodCrashLooping
        expr: |
          increase(kube_pod_container_status_restarts_total[15m]) > 3
        labels:
          severity: critical
```

## Alertmanager Routing

```yaml
route:
  group_by: [alertname, cluster]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: default
  routes:
    - matchers:
        - severity = critical
      receiver: pagerduty
    - matchers:
        - severity = warning
      receiver: slack

receivers:
  - name: pagerduty
    pagerduty_configs:
      - routing_key: ${PAGERDUTY_KEY}

  - name: slack
    slack_configs:
      - api_url: ${SLACK_WEBHOOK}
        channel: '#alerts'
        text: '{{ range .Alerts }}{{ .Annotations.summary }}{{ end }}'
```

## Instrumentation (Go example)

```go
var (
    requestTotal = promauto.NewCounterVec(prometheus.CounterOpts{
        Name: "http_requests_total",
        Help: "Total HTTP requests",
    }, []string{"method", "path", "status"})

    requestDuration = promauto.NewHistogramVec(prometheus.HistogramOpts{
        Name:    "http_request_duration_seconds",
        Help:    "HTTP request duration",
        Buckets: prometheus.DefBuckets,
    }, []string{"method", "path"})
)

func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        rw := &responseWriter{w, 200}
        next.ServeHTTP(rw, r)
        requestTotal.WithLabelValues(r.Method, r.URL.Path, strconv.Itoa(rw.status)).Inc()
        requestDuration.WithLabelValues(r.Method, r.URL.Path).Observe(time.Since(start).Seconds())
    })
}
```

## Key Rules
- Alert on symptoms (high latency, errors) not causes (high CPU) — causes have too many false positives
- Every alert must have a runbook URL
- Use multi-window burn-rate alerts for SLO alerting (fast burn + slow burn)
- Keep dashboards focused: one row per service, four golden signals per row
- Test alerts with `amtool` or manually fire them in staging
