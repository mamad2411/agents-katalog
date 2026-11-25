---
name: distributed-tracing
description: Implement distributed tracing across microservices using OpenTelemetry. Outputs trace instrumentation, context propagation, sampling configuration, Jaeger/Tempo integration, and trace-based debugging workflows.
argument-hint: [language/framework, tracing backend, existing observability stack, sampling rate]
allowed-tools: Read, Write, Bash
---

# Distributed Tracing

Distributed tracing follows a single request as it propagates through multiple services, capturing timing, errors, and context at each hop. Without tracing, debugging latency and failures in microservices is guesswork.

## Process

1. **Instrument the entry point** — create a root span at the API gateway or first service.
2. **Propagate context** — inject trace headers on all outbound calls.
3. **Extract context downstream** — each service reads headers and creates child spans.
4. **Add meaningful attributes** — user ID, order ID, database query, HTTP status.
5. **Configure sampling** — 100% in dev/staging, 1-10% in production for high-traffic services.
6. **Export to backend** — Jaeger, Grafana Tempo, or Datadog APM.
7. **Create dashboards** — service maps, p99 latency by trace, error rate by span.

## Output Format

### Python Instrumentation (FastAPI)

```python
# telemetry/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import ParentBased, TraceIdRatioBased
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
import os

def setup_tracing(app=None, service_name: str = None, sample_rate: float = 0.1):
    """Initialize OpenTelemetry tracing for a FastAPI application."""
    
    resource = Resource.create({
        SERVICE_NAME: service_name or os.getenv("SERVICE_NAME", "unknown"),
        SERVICE_VERSION: os.getenv("SERVICE_VERSION", "0.0.0"),
        "deployment.environment": os.getenv("ENVIRONMENT", "production"),
    })
    
    # Sampling: always sample errors, sample_rate% of successes
    sampler = ParentBased(
        root=TraceIdRatioBased(sample_rate),
    )
    
    provider = TracerProvider(resource=resource, sampler=sampler)
    
    # Export to OpenTelemetry Collector (which forwards to Jaeger/Tempo/Datadog)
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317"),
        insecure=True,
    )
    provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    
    trace.set_tracer_provider(provider)
    
    # Auto-instrument libraries
    if app:
        FastAPIInstrumentor.instrument_app(
            app,
            excluded_urls="health,metrics",  # Don't trace health checks
        )
    
    HTTPXClientInstrumentor().instrument()   # Outbound HTTP calls
    SQLAlchemyInstrumentor().instrument(    # Database queries
        enable_commenter=True,
        commenter_options={"opentelemetry_values": True}
    )
    RedisInstrumentor().instrument()         # Redis calls
    
    return trace.get_tracer(service_name or "app")


# Usage in FastAPI app
from fastapi import FastAPI
from opentelemetry import trace

app = FastAPI()
tracer = setup_tracing(app, service_name="order-service", sample_rate=0.05)

@app.post("/orders")
async def create_order(request: CreateOrderRequest, user: User = Depends(get_current_user)):
    # Current span created automatically by FastAPIInstrumentor
    span = trace.get_current_span()
    
    # Add business context to the span
    span.set_attributes({
        "user.id": user.id,
        "order.items_count": len(request.items),
        "order.total_cents": request.total_cents,
    })
    
    with tracer.start_as_current_span("validate_inventory") as validate_span:
        for item in request.items:
            validate_span.set_attribute("item.product_id", item.product_id)
            available = await inventory_client.check(item.product_id, item.quantity)
            if not available:
                validate_span.set_status(trace.StatusCode.ERROR, "Out of stock")
                raise HTTPException(409, "Item out of stock")
    
    with tracer.start_as_current_span("create_db_record") as db_span:
        order = await db.orders.create(request.dict(), user_id=user.id)
        db_span.set_attribute("order.id", order.id)
    
    with tracer.start_as_current_span("publish_order_event") as event_span:
        await event_bus.publish("order.created", {"order_id": order.id})
        event_span.set_attribute("event.topic", "order.created")
    
    return order
```

### Node.js Instrumentation (Express)

```typescript
// telemetry/tracing.ts — must be loaded BEFORE any other imports
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { TraceIdRatioBasedSampler } from '@opentelemetry/sdk-trace-base';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: process.env.SERVICE_NAME ?? 'unknown',
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.SERVICE_VERSION ?? '0.0.0',
    'deployment.environment': process.env.NODE_ENV ?? 'production',
  }),
  
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://otel-collector:4317',
  }),
  
  spanProcessor: new BatchSpanProcessor(new OTLPTraceExporter()),
  
  sampler: new TraceIdRatioBasedSampler(
    parseFloat(process.env.TRACE_SAMPLE_RATE ?? '0.05')
  ),
  
  instrumentations: [
    getNodeAutoInstrumentations({
      '@opentelemetry/instrumentation-http': {
        ignoreIncomingRequestHook: (req) => {
          return req.url?.includes('/health') || req.url?.includes('/metrics') || false;
        },
      },
      '@opentelemetry/instrumentation-pg': { enhancedDatabaseReporting: true },
    }),
  ],
});

sdk.start();
process.on('SIGTERM', () => sdk.shutdown());

// Custom spans in route handlers
import { trace, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');

app.post('/orders', async (req, res) => {
  const span = trace.getActiveSpan();
  span?.setAttributes({
    'user.id': req.user.id,
    'order.items_count': req.body.items.length,
  });
  
  await tracer.startActiveSpan('process_payment', async (paymentSpan) => {
    try {
      const result = await paymentService.charge(req.body);
      paymentSpan.setAttributes({
        'payment.provider': 'stripe',
        'payment.amount_cents': req.body.total_cents,
        'payment.intent_id': result.intentId,
      });
    } catch (err) {
      paymentSpan.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
      paymentSpan.recordException(err);
      throw err;
    } finally {
      paymentSpan.end();
    }
  });
});
```

### OpenTelemetry Collector Config

```yaml
# otel-collector.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024
  
  # Add environment attributes
  resource:
    attributes:
      - action: upsert
        key: cluster
        value: production-us-east
  
  # Filter out noisy health check spans
  filter:
    spans:
      exclude:
        match_type: regexp
        attributes:
          - key: http.target
            value: "(/health|/metrics|/ready)"
  
  # Sample errors at 100%, other spans at configured rate
  probabilistic_sampler:
    hash_seed: 22
    sampling_percentage: 10   # 10% of non-error spans
  
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: always-sample-errors
        type: status_code
        status_code: {status_codes: [ERROR]}
      - name: always-sample-slow
        type: latency
        latency: {threshold_ms: 1000}
      - name: probabilistic
        type: probabilistic
        probabilistic: {sampling_percentage: 10}

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true
  
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true
  
  prometheus:
    endpoint: 0.0.0.0:8889
    namespace: otel

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch, resource, filter, tail_sampling]
      exporters: [otlp/jaeger, otlp/tempo]
    
    metrics:
      receivers: [otlp]
      processors: [batch, resource]
      exporters: [prometheus]
```

### Jaeger Docker Compose

```yaml
# docker-compose.observability.yml
version: '3.8'
services:
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    volumes:
      - ./otel-collector.yaml:/etc/otelcol-contrib/config.yaml
    ports:
      - "4317:4317"    # OTLP gRPC
      - "4318:4318"    # OTLP HTTP
      - "8889:8889"    # Prometheus metrics
    depends_on:
      - jaeger
  
  jaeger:
    image: jaegertracing/all-in-one:latest
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    ports:
      - "16686:16686"  # Jaeger UI
      - "4317"         # OTLP gRPC (internal)
    volumes:
      - jaeger-data:/badger
  
  tempo:
    image: grafana/tempo:latest
    volumes:
      - ./tempo.yaml:/etc/tempo.yaml
    ports:
      - "3200:3200"    # Tempo HTTP
      - "4317"         # OTLP gRPC (internal)

volumes:
  jaeger-data:
```

### Trace Analysis Patterns

```python
# debugging/trace_analyzer.py — query traces to find problems

import requests

def find_slow_traces(service: str, threshold_ms: int = 1000, limit: int = 20):
    """Find slow traces for a service via Jaeger API."""
    r = requests.get(
        "http://jaeger:16686/api/traces",
        params={
            "service": service,
            "minDuration": f"{threshold_ms}ms",
            "limit": limit,
            "lookback": "1h",
        }
    )
    traces = r.json()["data"]
    
    for trace in traces:
        root_span = trace["spans"][0]
        duration_ms = root_span["duration"] / 1000
        
        # Find the slowest span
        slowest = max(trace["spans"], key=lambda s: s["duration"])
        
        print(f"Trace {trace['traceID'][:8]}: {duration_ms:.0f}ms")
        print(f"  Slowest span: {slowest['operationName']} ({slowest['duration']/1000:.0f}ms)")
        print(f"  Jaeger: http://jaeger:16686/trace/{trace['traceID']}")

def find_error_traces(service: str, limit: int = 20):
    """Find traces with errors."""
    r = requests.get(
        "http://jaeger:16686/api/traces",
        params={
            "service": service,
            "tags": '{"error":"true"}',
            "limit": limit,
            "lookback": "1h",
        }
    )
    return r.json()["data"]
```

## Rules

- **Instrument at the boundary, not inside functions** — HTTP handler, queue consumer, and cron job are the right entry points.
- **Propagate context always** — every outbound call must carry trace headers (W3C `traceparent`).
- **Sample proportionally to volume** — 100% for critical paths with low volume; 1% for high-traffic noisy services.
- **Always sample errors** — use tail sampling to capture 100% of error traces regardless of overall rate.
- **Add business attributes** — `user.id`, `order.id`, `tenant.id` make traces searchable and actionable.
- **Don't trace health checks** — they flood the backend with useless data.
- **Correlate logs with traces** — inject trace ID into log messages (`trace_id=abc123`).
- **Name spans descriptively** — `validate_inventory` beats `function_call`.
- **Record exceptions on spans** — `span.record_exception(e)` + `set_status(ERROR)` for automatic error tracking.
- **Start tracing before you need it** — retroactively adding tracing to debug a production issue is too late.
