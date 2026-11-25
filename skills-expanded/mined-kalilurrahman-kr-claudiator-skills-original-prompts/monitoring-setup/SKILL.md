---
name: monitoring-setup
description: Setup monitoring with Prometheus, Grafana, alerting. Outputs metrics collection, dashboards, alert rules, and SLO tracking.
argument-hint: [infrastructure type, SLA requirements, team size]
allowed-tools: Read, Write, Bash
---

# Monitoring & Observability Setup

Design production monitoring with metrics, logs, traces. Not basic dashboards — Prometheus/Grafana stack with SLOs, alerting, and on-call runbooks.

## Process

1. **Define SLIs/SLOs.** Service Level Indicators (latency, availability) and Objectives (99.9% uptime).
2. **Instrument code.** Prometheus metrics, structured logs, OpenTelemetry traces.
3. **Deploy collectors.** Prometheus server, exporters, log aggregators.
4. **Create dashboards.** Grafana with RED metrics (Rate, Errors, Duration).
5. **Configure alerts.** Critical: page on-call, Warning: ticket, Info: log.
6. **Write runbooks.** Debugging steps for each alert.
7. **Track SLOs.** Error budget, burn rate, incident review.

## Output Format

### Monitoring Stack: [Application Name]

**Metrics:** Prometheus + Grafana  
**Logs:** Loki + promtail  
**Traces:** Jaeger (OpenTelemetry)  
**Alerting:** Alertmanager → PagerDuty  
**SLO:** 99.9% availability (43min downtime/month)

---

## Architecture

```
┌─────────────┐
│ Application │──metrics──┐
└─────────────┘           │
                          ▼
┌─────────────┐    ┌─────────────┐
│   Node      │───▶│ Prometheus  │
│  Exporter   │    │   Server    │
└─────────────┘    └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Grafana   │
                   │  Dashboards │
                   └─────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │Alertmanager │──▶ PagerDuty
                   └─────────────┘
```

---

## Prometheus Metrics

### Counter (Always Increasing)
```python
from prometheus_client import Counter

http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Increment
http_requests_total.labels(method='GET', endpoint='/api/users', status='200').inc()
```

### Gauge (Goes Up/Down)
```python
from prometheus_client import Gauge

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

# Set value
active_connections.set(42)

# Increment/decrement
active_connections.inc()
active_connections.dec(5)
```

### Histogram (Distribution)
```python
from prometheus_client import Histogram

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

# Measure duration
with http_request_duration.labels(method='GET', endpoint='/api/users').time():
    # Handle request
    process_request()
```

### Summary (Similar to Histogram)
```python
from prometheus_client import Summary

http_request_size = Summary(
    'http_request_size_bytes',
    'HTTP request size'
)

http_request_size.observe(1024)  # 1KB request
```

---

## Instrumented Application (Express.js)

```javascript
const express = require('express');
const client = require('prom-client');

const app = express();

// Create metrics
const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status']
});

const httpRequestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 5]
});

// Middleware to track metrics
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    
    httpRequestsTotal.labels(req.method, req.route?.path || 'unknown', res.statusCode).inc();
    httpRequestDuration.labels(req.method, req.route?.path || 'unknown').observe(duration);
  });
  
  next();
});

// Expose /metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', client.register.contentType);
  res.end(await client.register.metrics());
});

app.listen(3000);
```

---

## Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Application metrics
  - job_name: 'api'
    static_configs:
      - targets: ['api:3000']
    metrics_path: '/metrics'
  
  # Node exporter (system metrics)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
  
  # PostgreSQL exporter
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
  
  # Kubernetes service discovery
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

# Alerting rules
rule_files:
  - 'alerts.yml'

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

---

## Alert Rules

```yaml
# alerts.yml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m]) / 
          rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on {{ $labels.instance }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
      
      # High response time
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            rate(http_request_duration_seconds_bucket[5m])
          ) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency on {{ $labels.route }}"
          description: "p95 latency is {{ $value }}s"
      
      # Service down
      - alert: ServiceDown
        expr: up{job="api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: "Service has been down for 1 minute"
      
      # High CPU usage
      - alert: HighCPU
        expr: |
          100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU on {{ $labels.instance }}"
          description: "CPU usage is {{ $value }}%"
      
      # Low disk space
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Only {{ $value | humanizePercentage }} disk space remaining"
```

---

## Alertmanager Configuration

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'team-notifications'
  
  routes:
    # Critical alerts to PagerDuty
    - match:
        severity: critical
      receiver: 'pagerduty'
      continue: true
    
    # Warnings to Slack
    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'team-notifications'
    email_configs:
      - to: 'team@example.com'
  
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<pagerduty-key>'
        description: '{{ .CommonAnnotations.summary }}'
  
  - name: 'slack'
    slack_configs:
      - api_url: '<slack-webhook>'
        channel: '#alerts'
        title: '{{ .CommonAnnotations.summary }}'
        text: '{{ .CommonAnnotations.description }}'

inhibit_rules:
  # Don't alert on individual instances if whole cluster is down
  - source_match:
      alertname: 'ClusterDown'
    target_match:
      alertname: 'ServiceDown'
    equal: ['cluster']
```

---

## Grafana Dashboard

### RED Metrics (Rate, Errors, Duration)

```json
{
  "dashboard": {
    "title": "API Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{
          "expr": "rate(http_requests_total[5m])"
        }]
      },
      {
        "title": "Error Rate",
        "targets": [{
          "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])"
        }]
      },
      {
        "title": "Response Time (p95)",
        "targets": [{
          "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
        }]
      }
    ]
  }
}
```

### Common Queries

```promql
# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# Error percentage
100 * sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))

# p95 latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# CPU usage
100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes * 100

# Disk I/O
rate(node_disk_io_time_seconds_total[5m])

# Network traffic
rate(node_network_receive_bytes_total[5m])
```

---

## SLO Tracking

### Define SLO
```
Availability SLO: 99.9%
- Error budget: 0.1% = 43.2 minutes/month
- Burn rate alert: Consuming budget too fast

Latency SLO: p95 < 200ms
- Success rate: % of requests < 200ms
```

### SLO Alert
```yaml
- alert: ErrorBudgetBurnRate
  expr: |
    (
      1 - (
        sum(rate(http_requests_total{status!~"5.."}[1h])) /
        sum(rate(http_requests_total[1h]))
      )
    ) > (14.4 * 0.001)  # Burning budget 14.4x faster than allowed
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "SLO burn rate too high"
    description: "At current error rate, will exhaust monthly budget in 2 days"
```

---

## Logging (Structured)

### Application Logs (JSON)
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'api' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});

// Log with context
logger.info('User logged in', {
  userId: '12345',
  ip: '192.168.1.1',
  duration: 234
});

// Output:
{
  "level": "info",
  "message": "User logged in",
  "service": "api",
  "userId": "12345",
  "ip": "192.168.1.1",
  "duration": 234,
  "timestamp": "2024-03-21T10:30:00.000Z"
}
```

### Loki Configuration
```yaml
# promtail.yml - Log collector
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*.log
  
  - job_name: app
    static_configs:
      - targets:
          - localhost
        labels:
          job: app
          __path__: /app/logs/*.log
```

### Query Logs in Grafana
```logql
{job="app"} |= "error"                    # Filter by keyword
{job="app"} | json | userId="12345"       # Filter JSON field
rate({job="app"}[5m])                     # Log rate
```

---

## Distributed Tracing (Jaeger)

```javascript
const opentelemetry = require('@opentelemetry/api');
const { JaegerExporter } = require('@opentelemetry/exporter-jaeger');
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');

// Initialize tracer
const provider = new NodeTracerProvider();
const exporter = new JaegerExporter({
  endpoint: 'http://jaeger:14268/api/traces',
});

provider.addSpanProcessor(new opentelemetry.BatchSpanProcessor(exporter));
provider.register();

const tracer = opentelemetry.trace.getTracer('api');

// Trace request
app.get('/users/:id', async (req, res) => {
  const span = tracer.startSpan('GET /users/:id');
  
  try {
    const user = await getUserFromDB(req.params.id);
    const orders = await getOrdersForUser(user.id);
    
    span.setAttributes({
      'user.id': user.id,
      'orders.count': orders.length
    });
    
    res.json({ user, orders });
  } catch (error) {
    span.recordException(error);
    res.status(500).json({ error: error.message });
  } finally {
    span.end();
  }
});
```

---

## On-Call Runbooks

### Alert: HighErrorRate

```markdown
## Runbook: High Error Rate

**Alert:** Error rate > 5% for 5 minutes

### Diagnosis Steps
1. Check Grafana dashboard for error distribution by endpoint
2. Check logs for error details: `{job="api"} |= "error" | json`
3. Check recent deploys: `kubectl rollout history deployment/api`

### Common Causes
- Recent deploy introduced bug → Rollback
- Database connection pool exhausted → Scale DB or app
- External API down → Enable circuit breaker

### Commands
```bash
# Check current error rate
curl -s prometheus:9090/api/v1/query?query=rate(http_requests_total{status=~"5.."}[5m])

# View recent logs
kubectl logs deployment/api --tail=100 | grep ERROR

# Rollback deploy
kubectl rollout undo deployment/api
```

### Escalation
If error rate > 10% for 10 minutes, page SRE lead.
```

---

## Docker Compose Stack

```yaml
# docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alerts.yml:/etc/prometheus/alerts.yml
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
  
  alertmanager:
    image: prom/alertmanager:latest
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"
  
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
  
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
  
  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/log:/var/log
      - ./promtail.yml:/etc/promtail/promtail.yml

volumes:
  grafana-storage:
```

## Rules

- Instrument all services with metrics — RED metrics (Rate, Errors, Duration) minimum.
- Use labels wisely — endpoint, method, status, but not user ID (high cardinality).
- Alert on symptoms, not causes — alert on "high error rate" not "database slow query".
- Define SLOs before alerting — know acceptable error budget before setting thresholds.
- Runbook for every alert — on-call engineer needs debugging steps, not guesswork.
- Page only for critical — wake someone at 3am only if customer impact.
- Structured logging (JSON) — enables filtering, aggregation, correlation with traces.
- Dashboard for humans, alerts for robots — dashboards show trends, alerts require action.
- Test alerts in staging — validate alert fires at correct threshold before production.
- Review metrics quarterly — remove unused metrics, add missing observability.
