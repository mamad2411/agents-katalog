---
name: tpl-devops-monitoring-observability
description: Template do pack (devops/06-monitoring-observability.md). Orienta o agente em infra, deploy, CI/CD e operacao alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: devops/06-monitoring-observability.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Monitoring & Observability Stack (Prometheus + Grafana + Loki + OpenTelemetry)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `devops/06-monitoring-observability.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Metrics:** Prometheus 2.50+ + Alertmanager
- **Visualization:** Grafana 10+ (dashboard-as-code with Grafonnet/JSON)
- **Logs:** Loki 3 + Promtail / Alloy
- **Tracing:** OpenTelemetry Collector + Tempo (or Jaeger)
- **App instrumentation:** Node.js + `@opentelemetry/sdk-node` + `prom-client`
- **Deployment:** Docker Compose (dev) / Helm kube-prometheus-stack (prod)

---

## ARCHITECTURE RULES
1. **Instrument at the boundary** — measure HTTP in/out, DB calls, queue produce/consume. Not every internal function.
2. **RED method for services** — Rate (req/s), Errors (error rate %), Duration (latency p50/p95/p99). Always.
3. **USE method for resources** — Utilization, Saturation, Errors for CPU/memory/disk/network.
4. **Metric naming is permanent** — rename = breaking change. Use `{service}_{noun}_{unit}_{type}` format.
5. **Logs are for events, metrics for aggregates** — never log `request_count++`; emit a counter metric.
6. **Structured JSON logs only** — no `console.log("User logged in")`. Use `logger.info({ userId, action })`.
7. **Alert on symptoms, not causes** — alert on high error rate (symptom), not "CPU > 80%" (cause).
8. **Dashboards are code** — store as JSON in `monitoring/dashboards/`; never click-to-build only.

---

## NODE.JS INSTRUMENTATION

```typescript
// src/telemetry.ts — import BEFORE everything else in src/index.ts
import { NodeSDK } from '@opentelemetry/sdk-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http'
import { PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics'
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http'
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express'
import { PgInstrumentation } from '@opentelemetry/instrumentation-pg'

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT || 'http://otel-collector:4318/v1/traces',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_METRICS_ENDPOINT || 'http://otel-collector:4318/v1/metrics',
    }),
    exportIntervalMillis: 15000,
  }),
  instrumentations: [
    new HttpInstrumentation({
      ignoreIncomingPaths: ['/healthz', '/metrics'],  // Don't trace health checks
    }),
    new ExpressInstrumentation(),
    new PgInstrumentation(),
  ],
  serviceName: process.env.OTEL_SERVICE_NAME || 'my-app',
})

sdk.start()
process.on('SIGTERM', () => sdk.shutdown())
```

---

## PROMETHEUS METRICS (Node.js)

```typescript
// src/metrics.ts
import { Registry, Counter, Histogram, Gauge } from 'prom-client'

export const registry = new Registry()
registry.setDefaultLabels({ service: 'my-app', env: process.env.NODE_ENV || 'dev' })

// ---- HTTP metrics (RED) ----
export const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [registry],
})

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [registry],
})

// ---- Business metrics ----
export const activeUsers = new Gauge({
  name: 'app_active_users',
  help: 'Currently active authenticated users',
  registers: [registry],
})

export const ordersProcessed = new Counter({
  name: 'app_orders_processed_total',
  help: 'Total orders processed',
  labelNames: ['status'],  // success | failed
  registers: [registry],
})

// ---- DB connection pool ----
export const dbPoolSize = new Gauge({
  name: 'pg_pool_size',
  help: 'PostgreSQL connection pool size',
  labelNames: ['state'],  // idle | active | waiting
  registers: [registry],
})
```

---

## MIDDLEWARE: METRICS + LOGGING

```typescript
// src/middleware/observability.ts
import { Request, Response, NextFunction } from 'express'
import { httpRequestsTotal, httpRequestDuration } from '../metrics'
import logger from '../logger'

export function metricsMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = Date.now()
  const route = req.route?.path || req.path

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000
    const labels = { method: req.method, route, status_code: String(res.statusCode) }

    httpRequestsTotal.inc(labels)
    httpRequestDuration.observe(labels, duration)

    logger.info({
      type: 'http_request',
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration_ms: Math.round(duration * 1000),
      request_id: req.headers['x-request-id'],
      user_id: (req as any).user?.id,
    })
  })

  next()
}
```

---

## STRUCTURED LOGGER

```typescript
// src/logger.ts — always use this, never console.log()
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  ...(process.env.NODE_ENV === 'development'
    ? { transport: { target: 'pino-pretty' } }
    : {}
  ),
  base: {
    service: process.env.OTEL_SERVICE_NAME || 'my-app',
    env: process.env.NODE_ENV,
    version: process.env.APP_VERSION,
  },
  redact: ['req.headers.authorization', 'body.password', 'body.token'],
  serializers: {
    err: pino.stdSerializers.err,
  },
})

export default logger

// Usage:
// logger.info({ userId: '123', action: 'login' }, 'User authenticated')
// logger.error({ err, orderId }, 'Order processing failed')
// NEVER: logger.info('User ' + userId + ' logged in')
```

---

## METRIC NAMING CONVENTIONS
```
Format: {service}_{noun}_{unit}_{type}

✅ http_requests_total           (counter)
✅ http_request_duration_seconds  (histogram)
✅ pg_pool_connections            (gauge)
✅ queue_messages_total           (counter, label: status=processed|failed)
✅ cache_hit_ratio                (gauge, 0.0-1.0)

❌ requestCount        (no service prefix, no unit, camelCase)
❌ error_rate          (rate is computed by PromQL, not stored)
❌ my_app_latency_ms   (use _seconds, Prometheus convention)
```

---

## ALERT RULES

```yaml
# monitoring/alerts/app.yml
groups:
  - name: app.rules
    rules:
      # Alert on symptoms, not causes
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status_code=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.05
        for: 2m
        labels:
          severity: critical
          team: backend
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"
          runbook: "https://runbooks.internal/high-error-rate"

      - alert: HighLatencyP99
        expr: |
          histogram_quantile(0.99,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 2.0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency > 2s on {{ $labels.service }}"

      - alert: ServiceDown
        expr: up{job="my-app"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "{{ $labels.instance }} is down"

      # Log-based alert via Loki ruler
      - alert: PanicInLogs
        expr: |
          count_over_time({app="my-app"} |= "panic" [5m]) > 0
        labels:
          severity: critical
```

---

## PROMETHEUS SCRAPE CONFIG

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - /etc/prometheus/rules/*.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: my-app
    static_configs:
      - targets: ['app:3000']
    metrics_path: /metrics
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance

  - job_name: node-exporter
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: postgres-exporter
    static_configs:
      - targets: ['postgres-exporter:9187']
```

---

## GRAFANA DASHBOARD AS CODE (JSON snippet)

```json
{
  "title": "App RED Dashboard",
  "uid": "app-red-v1",
  "tags": ["app", "red"],
  "panels": [
    {
      "title": "Request Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "sum(rate(http_requests_total[5m])) by (route)",
        "legendFormat": "{{ route }}"
      }]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [{
        "expr": "sum(rate(http_requests_total{status_code=~'5..'}[5m])) / sum(rate(http_requests_total[5m]))",
        "legendFormat": "Error %"
      }],
      "thresholds": {
        "steps": [
          {"color": "green", "value": null},
          {"color": "yellow", "value": 0.01},
          {"color": "red", "value": 0.05}
        ]
      }
    },
    {
      "title": "P95 Latency",
      "type": "timeseries",
      "targets": [{
        "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, route))",
        "legendFormat": "p95 {{ route }}"
      }]
    }
  ]
}
```

---

## OTEL COLLECTOR CONFIG

```yaml
# otel-collector/config.yml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    send_batch_size: 1024
    timeout: 5s
  memory_limiter:
    limit_mib: 512
    check_interval: 5s

exporters:
  prometheus:
    endpoint: 0.0.0.0:8889
  loki:
    endpoint: http://loki:3100/loki/api/v1/push
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, memory_limiter]
      exporters: [otlp/tempo]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [batch]
      exporters: [loki]
```
