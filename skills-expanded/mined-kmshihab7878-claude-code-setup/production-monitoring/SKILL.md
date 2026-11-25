---
name: production-monitoring
description: Production monitoring with Grafana, Prometheus, Loki, and OpenTelemetry for containerized Python services on AWS EKS
triggers:
  - monitoring
  - grafana
  - prometheus
  - loki
  - opentelemetry
  - otel
  - alerting
  - SLO
  - SLI
  - dashboard
  - metrics
  - observability
---

# Production Monitoring

Monitoring stack for containerized Python services: Prometheus (metrics), Loki (logs), Grafana (dashboards), OpenTelemetry (instrumentation).

## OpenTelemetry Python Instrumentation

```python
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_telemetry(app, service_name: str = "coremind"):
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("process_agent_task")
async def process_task(task_id: str):
    span = trace.get_current_span()
    span.set_attribute("task.id", task_id)
    # ... processing
```

## Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

REQUEST_COUNT = Counter("http_requests_total", "Total requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])
ACTIVE_AGENTS = Gauge("coremind_active_agents", "Currently active agents")
TASK_DURATION = Histogram("coremind_task_duration_seconds", "Task execution time", ["agent_type"])
```

## PromQL Queries

```promql
# Request rate (5m window)
rate(http_requests_total[5m])

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
100 * rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Agent utilization
coremind_active_agents / coremind_max_agents * 100
```

## Alert Rules

```yaml
groups:
  - name: coremind-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate (>5%)"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 latency >2s"

      - alert: AgentStuck
        expr: coremind_task_duration_seconds_count == 0 and coremind_active_agents > 0
        for: 10m
        labels:
          severity: warning
```

## SLO Definitions

| Service | SLI | SLO | Measurement |
|---------|-----|-----|-------------|
| API | Availability | 99.9% uptime | `1 - (5xx / total)` over 30d |
| API | Latency | P99 < 500ms | `histogram_quantile(0.99, ...)` |
| Agents | Success rate | >95% tasks complete | `succeeded / total` per hour |
| Agents | Duration | P95 < 30s | Task duration histogram |
