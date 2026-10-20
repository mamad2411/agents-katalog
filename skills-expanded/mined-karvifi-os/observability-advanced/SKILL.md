---
name: observability-advanced
description: Production observability — distributed tracing, metrics, logs, OpenTelemetry, Prometheus
triggers: [observability, tracing, metrics, logs, OpenTelemetry, Prometheus, Grafana, monitoring]
---

# SKILL: Observability Advanced

## Three Pillars: Metrics, Logs, Traces

### Pattern 1: Distributed Tracing (OpenTelemetry)
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Export to collector
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317")
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument code
@tracer.start_as_current_span("process_order")
def process_order(order_id):
    span = trace.get_current_span()
    span.set_attribute("order.id", order_id)
    
    # Child span
    with tracer.start_as_current_span("validate_order"):
        validate(order_id)
    
    with tracer.start_as_current_span("charge_payment"):
        charge(order_id)
    
    with tracer.start_as_current_span("ship_order"):
        ship(order_id)
```

### Pattern 2: Metrics (Prometheus)
```python
from prometheus_client import Counter, Histogram, Gauge, Summary

# Counter (monotonic increase)
requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram (distribution)
request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Gauge (up/down value)
active_users = Gauge(
    'active_users',
    'Number of active users'
)

# Usage
@request_duration.time()
def handle_request(method, endpoint):
    requests_total.labels(method=method, endpoint=endpoint, status=200).inc()
    active_users.set(get_active_user_count())
```

### Pattern 3: Structured Logging
```python
import structlog

logger = structlog.get_logger()

# Structured logs (JSON)
logger.info(
    "order_processed",
    order_id="123",
    user_id="456",
    amount=99.99,
    payment_method="card"
)

# Output:
# {"event": "order_processed", "order_id": "123", "user_id": "456", ...}
```

### Pattern 4: Log Correlation (Trace IDs)
```python
import logging
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        record.trace_id = f"{span.get_span_context().trace_id:032x}"
        record.span_id = f"{span.get_span_context().span_id:016x}"
        return True

logging.basicConfig()
logger = logging.getLogger()
logger.addFilter(TraceContextFilter())

# Logs now include trace_id
logger.info("Processing order")
# [trace_id=abc123] [span_id=def456] Processing order
```

### Pattern 5: RED Metrics (Request, Error, Duration)
```python
# Request rate
request_rate = Counter('requests_total', 'Total requests', ['service'])

# Error rate
error_rate = Counter('requests_errors_total', 'Failed requests', ['service'])

# Duration (latency)
request_duration = Histogram('request_duration_seconds', 'Request duration', ['service'])

# Track RED metrics
def track_request(service):
    request_rate.labels(service=service).inc()
    
    with request_duration.labels(service=service).time():
        try:
            process_request()
        except Exception:
            error_rate.labels(service=service).inc()
            raise
```

### Pattern 6: SLOs (Service Level Objectives)
```yaml
# Example: 99.9% availability
slo:
  availability: 99.9
  latency_p99: 200ms  # 99th percentile < 200ms
  error_budget: 0.1%  # Allowed 0.1% errors

# Alert when error budget depleted
alert:
  expr: (1 - (error_rate / request_rate)) < 0.999
  message: "SLO violated: availability below 99.9%"
```

## Quality Checks
- [ ] Distributed tracing enabled (OpenTelemetry)
- [ ] RED metrics collected (request, error, duration)
- [ ] Structured logging (JSON)
- [ ] Log correlation (trace IDs in logs)
- [ ] Dashboards created (Grafana)
- [ ] Alerts configured (Prometheus/Alertmanager)
- [ ] SLOs defined and monitored
- [ ] Sampling strategy configured (not tracing 100%)
