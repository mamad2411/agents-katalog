---
name: observability-telemetry
description: Observability & telemetry — OpenTelemetry SDK/collector, Prometheus metrics, Grafana dashboards, structured logging, distributed tracing, RAG span attributes, event stream monitoring, Sentry integration, chaos drills, and automation.
origin: AI Dev Kit
---

# Observability & Telemetry

Comprehensive observability practices for production systems: OpenTelemetry instrumentation (Python + TypeScript), Prometheus metrics and alerting, Grafana dashboards, structured logging, distributed tracing, RAG/LLM-specific monitoring, event stream consumers, error tracking with Sentry, chaos engineering, and infrastructure-as-code for observability.

## When to Use

- Instrumenting microservices, APIs, or ML systems for production observability
- Setting up metrics, traces, and logs with OpenTelemetry exporters
- Building Grafana dashboards for application, API, and ML workload monitoring
- Implementing structured logging with correlation IDs and cost controls
- Tracing distributed requests across service boundaries with span baggage
- Monitoring RAG/LLM systems: embedding latency, retrieval hit-rate, hallucination rates
- Tracking Kafka/Redpanda consumer health, dead-letter queues, and replay strategies
- Integrating Sentry for error tracking, alert routing, and deduplication
- Running chaos drills and maintaining operational runbooks
- Provisioning observability infrastructure with Terraform and dashboards as code

## Core Concepts

### 1. OpenTelemetry SDK Setup

**Python SDK**:

```python
# otel_setup.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
import os

def setup_otel(service_name: str, service_version: str):
    """Initialize OpenTelemetry for Python services."""
    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
        "deployment.environment": os.environ.get("ENVIRONMENT", "production"),
    })

    # Tracing
    tracer_provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317"),
        insecure=True,  # Use TLS in production
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Metrics
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(
            endpoint=os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317"),
            insecure=True,
        ),
        export_interval_millis=10000,  # Export every 10s
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    return trace.get_tracer(service_name), metrics.get_meter(service_name)

tracer, meter = setup_otel("rag-api", "2.3.0")
```

**TypeScript SDK**:

```typescript
// otel-setup.ts
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";
import { OTLPMetricExporter } from "@opentelemetry/exporter-metrics-otlp-grpc";
import { PeriodicExportingMetricReader } from "@opentelemetry/sdk-metrics";
import { Resource } from "@opentelemetry/resources";
import { SemanticResourceAttributes } from "@opentelemetry/semantic-conventions";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: "rag-frontend-api",
    [SemanticResourceAttributes.SERVICE_VERSION]: "1.0.0",
    "deployment.environment": process.env.NODE_ENV || "production",
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://otel-collector:4317",
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || "http://otel-collector:4317",
    }),
    exportIntervalMillis: 10000,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

**OpenTelemetry Collector Config**:

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  prometheus:
    config:
      scrape_configs:
        - job_name: "otel-collector"
          scrape_interval: 10s
          static_configs:
            - targets: ["localhost:8888"]

processors:
  batch:
    timeout: 5s
    send_batch_max_size: 1000
  memory_limiter:
    limit_mib: 512
    spike_limit_mib: 128
    check_interval: 5s
  probabilistic_sampler:
    sampling_percentage: 25  # Sample 25% of spans in production

exporters:
  otlp/jaeger:
    endpoint: "jaeger:4317"
    tls:
      insecure: true
  prometheus:
    endpoint: "0.0.0.0:8889"
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch, probabilistic_sampler]
      exporters: [otlp/jaeger]
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [logging]
```

### 2. Prometheus Metrics & Alerting

**Custom Application Metrics**:

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
import time

# Request metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# RAG-specific metrics
EMBEDDING_LATENCY = Histogram(
    "rag_embedding_latency_ms",
    "Embedding generation latency in milliseconds",
    ["model"],
    buckets=[10, 50, 100, 200, 500, 1000, 2000],
)
RETRIEVAL_HIT_RATE = Gauge(
    "rag_retrieval_hit_rate",
    "Fraction of queries where top-N contains relevant document",
    ["top_k"],
)
CACHE_HIT_RATE = Gauge("rag_cache_hit_rate", "Semantic cache hit rate")
HALLUCINATION_RATE = Gauge("rag_hallucination_rate", "Fraction of responses flagged as hallucinated")
ACTIVE_CONVERSATIONS = Gauge("rag_active_conversations", "Number of active chat sessions")
TOKEN_USAGE = Counter("rag_token_usage_total", "Total tokens consumed", ["model", "type"])  # type: prompt/completion

# Middleware for automatic request tracking
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()
        REQUEST_DURATION.labels(
            method=request.method, endpoint=request.url.path
        ).observe(duration)

        return response
```

**Prometheus Alert Rules**:

```yaml
# prometheus-alerts.yml
groups:
  - name: rag-api-alerts
    rules:
      # SLO: 99% of requests succeed
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "RAG API error rate > 1% for 5 minutes"
          runbook_url: "https://wiki.internal/runbooks/high-error-rate"

      # Latency SLO: P95 < 3s
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)) > 3
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency > 3s for 10 minutes"

      # Embedding latency regression
      - alert: EmbeddingLatencyDegradation
        expr: |
          histogram_quantile(0.95, sum(rate(rag_embedding_latency_ms_bucket[5m])) by (le)) > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 embedding latency > 1s"

      # Cache hit rate dropped
      - alert: LowCacheHitRate
        expr: rag_cache_hit_rate < 0.15
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "Cache hit rate dropped below 15%"

      # SLO Burn Rate — Multi-Window Multi-Burn-Rate
      - alert: HighBurnRate1h
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[1h]))
          / sum(rate(http_requests_total[1h])) > 14.4 * 0.001  # 14.4x burn rate for 99.9% SLO
        for: 3m
        labels:
          severity: critical
          page: "true"
        annotations:
          summary: "Budget burn rate too high — 1h window"

      - alert: HighBurnRate6h
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[6h]))
          / sum(rate(http_requests_total[6h])) > 6 * 0.001
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Budget burn rate elevated — 6h window"
```

### 3. Grafana Dashboards

**Dashboard-as-Code** (Jsonnet):

```jsonnet
// dashboards/rag-api.jsonnet
local grafana = import 'github.com/grafana/grafonnet-lib/grafonnet/grafana.libsonnet';
local template = grafana.template;
local panel = grafana.graphPanel;

{
  dashboard: grafana.dashboard.new(
    'RAG API Dashboard',
    tags=['rag', 'production'],
    refresh='30s',
    time={from: 'now-6h', to: 'now'},
  )
  .addTemplate(template.new('datasource', 'Datasource', 'prometheus').hide())
  .addTemplate(template.new('service', 'Service', 'label_values(http_requests_total, service)').hide())
  .addRow(
    grafana.row.new('Overview')
    .addPanel(
      panel.new('Request Rate', datasource='$datasource')
      .addTarget(grafana.target.new('sum(rate(http_requests_total{service="$service"}[5m]))'))
      .setYAxisLabel('req/s'),
      {gridPos: {x: 0, y: 0, w: 8, h: 8}}
    )
    .addPanel(
      panel.new('Error Rate %', datasource='$datasource')
      .addTarget(grafana.target.new(
        'sum(rate(http_requests_total{service="$service", status_code=~"5.."}[5m])) / sum(rate(http_requests_total{service="$service"}[5m])) * 100'
      ))
      .setYAxisLabel('%'),
      {gridPos: {x: 8, y: 0, w: 8, h: 8}}
    )
    .addPanel(
      panel.new('P95 Latency', datasource='$datasource')
      .addTarget(grafana.target.new(
        'histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{service="$service"}[5m])) by (le))'
      ))
      .setYAxisLabel('seconds'),
      {gridPos: {x: 16, y: 0, w: 8, h: 8}}
    )
  )
  .addRow(
    grafana.row.new('RAG Metrics')
    .addPanel(
      panel.new('Embedding Latency P95', datasource='$datasource')
      .addTarget(grafana.target.new(
        'histogram_quantile(0.95, sum(rate(rag_embedding_latency_ms_bucket[5m])) by (le))'
      )),
      {gridPos: {x: 0, y: 8, w: 8, h: 8}}
    )
    .addPanel(
      panel.new('Retrieval Hit Rate', datasource='$datasource')
      .addTarget(grafana.target.new('rag_retrieval_hit_rate{top_k="5"}')),
      {gridPos: {x: 8, y: 8, w: 8, h: 8}}
    )
    .addPanel(
      panel.new('Cache Hit Rate', datasource='$datasource')
      .addTarget(grafana.target.new('rag_cache_hit_rate')),
      {gridPos: {x: 16, y: 8, w: 8, h: 8}}
    )
  )
}
```

**Drill-Down Pattern** — top-level dashboard → service dashboard → trace view:

```
┌─────────────────────────────────────────────────┐
│           Overview Dashboard                    │
│  [Req/s] [Error%] [P95 Latency] [SLO Budget]   │
└────────────────────┬────────────────────────────┘
                     │ Click service
┌────────────────────▼────────────────────────────┐
│         Service Dashboard (RAG API)             │
│  [Endpoints] [Embeddings] [Retrieval] [Cache]  │
└────────────────────┬────────────────────────────┘
                     │ Click spike
┌────────────────────▼────────────────────────────┐
│           Trace View (Jaeger/Tempo)             │
│  Span timeline: → retriever → embedder → LLM   │
└─────────────────────────────────────────────────┘
```

### 4. Structured Logging

**Python with Loguru**:

```python
from loguru import logger
import sys
import json

# Configure structured JSON logging for production
def serialize_record(record):
    """Format log record as JSON for ingestion."""
    return json.dumps({
        "timestamp": record["time"].isoformat(),
        "level": record["level"].name,
        "message": record["message"],
        "service": record["extra"].get("service", "unknown"),
        "trace_id": record["extra"].get("trace_id"),
        "span_id": record["extra"].get("span_id"),
        "user_id": record["extra"].get("user_id"),
        "request_id": record["extra"].get("request_id"),
        "file": record["file"].name,
        "line": record["line"],
    }) + "\n"

# Remove default handler
logger.remove()

# Add structured JSON handler for production
if os.environ.get("ENVIRONMENT") == "production":
    logger.add(sys.stdout, format=serialize_record, level="INFO", serialize=True)
else:
    logger.add(sys.stdout, level="DEBUG", colorize=True)

# Add rotation to control log volume/cost
logger.add(
    "logs/app-{time:YYYY-MM-DD}.log",
    rotation="100 MB",
    retention="7 days",
    compression="gzip",
    level="INFO",
)

# Usage with correlation ID
def process_request(request_id: str, trace_id: str, user_id: str):
    ctx_logger = logger.bind(
        request_id=request_id,
        trace_id=trace_id,
        user_id=user_id,
        service="rag-api",
    )
    ctx_logger.info("Processing RAG request", query_length=len(request_id))
```

**TypeScript with Winston**:

```typescript
import winston from "winston";

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json(),
  ),
  defaultMeta: {
    service: "rag-frontend-api",
    environment: process.env.NODE_ENV,
  },
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({
      filename: "logs/error.log",
      level: "error",
      maxsize: 100 * 1024 * 1024, // 100MB
      maxFiles: 7,
    }),
  ],
});

// Middleware: inject correlation ID
import { v4 as uuidv4 } from "uuid";
import { AsyncLocalStorage } from "async_hooks";

const als = new AsyncLocalStorage<Map<string, string>>();

export function correlationMiddleware(req, res, next) {
  const correlationId = req.headers["x-correlation-id"] || uuidv4();
  const store = new Map([
    ["correlationId", correlationId],
    ["traceId", req.headers["x-b3-traceid"] || ""],
  ]);
  res.setHeader("x-correlation-id", correlationId);
  als.run(store, next);
}

// Usage
function handleRequest(query: string) {
  const store = als.getStore();
  const correlationId = store?.get("correlationId");
  logger.info("Processing query", { correlationId, queryLength: query.length });
}
```

### 5. Distributed Tracing

**Span Naming Conventions**:

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode

tracer = trace.get_tracer("rag-api")

def process_rag_query(query: str, top_k: int = 5):
    """Process a full RAG pipeline with tracing."""
    with tracer.start_as_current_span(
        "rag.process_query",
        kind=SpanKind.SERVER,
        attributes={
            "rag.query_length": len(query),
            "rag.top_k": top_k,
        },
    ) as root_span:
        # Retrieve context
        contexts = retrieve_context(query, top_k)
        root_span.set_attribute("rag.context_count", len(contexts))

        # Generate response
        response = generate_response(query, contexts)
        root_span.set_attribute("rag.response_length", len(response))

        root_span.set_status(Status(StatusCode.OK))
        return response

def retrieve_context(query: str, top_k: int) -> list[str]:
    with tracer.start_as_current_span(
        "rag.retrieve",
        kind=SpanKind.INTERNAL,
        attributes={"rag.top_k": top_k},
    ) as span:
        embeddings = generate_embeddings([query])
        span.set_attribute("rag.embedding_model", "text-embedding-3-small")

        results = vector_store.search(embeddings[0], top_k=top_k)
        span.set_attribute("rag.results_count", len(results))

        return results
```

**RAG-Specific Span Attributes**:

```python
RAG_SPAN_ATTRIBUTES = {
    # Query metadata
    "rag.query": str,           # The user query (sanitized, no PII)
    "rag.query_length": int,    # Length of query in characters
    "rag.top_k": int,           # Number of retrieved contexts

    # Retrieval metadata
    "rag.embedding_model": str,  # Model used for embedding
    "rag.embedding_latency_ms": float,
    "rag.retriever_type": str,   # dense, sparse, hybrid
    "rag.context_count": int,    # Number of retrieved documents
    "rag.context_lengths": list, # Lengths of each context chunk

    # Generation metadata
    "rag.llm_model": str,        # LLM model used
    "rag.llm_latency_ms": float,
    "rag.prompt_tokens": int,
    "rag.completion_tokens": int,
    "rag.total_tokens": int,
    "rag.temperature": float,

    # Cache metadata
    "rag.cache_hit": bool,
    "rag.cache_similarity": float,  # Similarity score for cache match

    # Evaluation metadata
    "rag.faithfulness": float,
    "rag.hallucination_flag": bool,
}
```

**Baggage Propagation**:

```python
from opentelemetry import baggage, context

def propagate_user_context(user_id: str, tenant_id: str):
    """Attach user/tenant context to all downstream spans."""
    ctx = baggage.set_baggage("user.id", user_id)
    ctx = baggage.set_baggage("tenant.id", tenant_id, context=ctx)
    token = context.attach(ctx)
    try:
        # All spans in this context will carry baggage
        return process_rag_query("Hello")
    finally:
        context.detach(token)
```

**Sampling Strategy**:

```yaml
# Tail-based sampling — keep all errors, sample normal traffic
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

processors:
  # Head-based: sample 10% upfront
  probabilistic_sampler:
    sampling_percentage: 10
  # Tail-based: keep 100% of error traces
  tail_sampling:
    policies:
      - name: keep-errors
        type: status_code
        status_code:
          status_codes: [ERROR]
      - name: keep-slow
        type: latency
        latency:
          threshold_ms: 2000
      - name: sample-rest
        type: probabilistic
        probabilistic:
          sampling_percentage: 5
    decision_wait: 10s
```

### 6. Event Stream Monitoring

```python
# Kafka Consumer with observability
from confluent_kafka import Consumer
from opentelemetry import trace, metrics

tracer = trace.get_tracer("kafka-consumer")
meter = metrics.get_meter("kafka-consumer")

CONSUMER_LAG = Gauge("kafka_consumer_lag", "Consumer group lag by topic/partition", ["topic", "partition", "group"])
MESSAGE_PROCESSING_TIME = Histogram("kafka_message_processing_ms", "Time to process a message", ["topic"])
DLQ_COUNT = Counter("kafka_dlq_messages_total", "Messages sent to DLQ", ["topic", "error_type"])

class ObservableConsumer:
    def __init__(self, consumer: Consumer, topic: str, group_id: str):
        self.consumer = consumer
        self.topic = topic
        self.group_id = group_id

    def poll_and_process(self):
        with tracer.start_as_current_span(f"kafka.consume.{self.topic}") as span:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                return
            if msg.error():
                span.set_status(Status(StatusCode.ERROR, str(msg.error())))
                return

            span.set_attributes({
                "messaging.kafka.topic": self.topic,
                "messaging.kafka.partition": msg.partition(),
                "messaging.kafka.offset": msg.offset(),
                "messaging.message.key": msg.key().decode() if msg.key() else "",
            })

            start = time.time()
            try:
                self.process_message(msg)
                self.consumer.commit(msg)
            except Exception as e:
                DLQ_COUNT.labels(topic=self.topic, error_type=type(e).__name__).inc()
                self.send_to_dlq(msg, e)
                self.consumer.commit(msg)  # Commit to avoid infinite loop
            finally:
                duration = (time.time() - start) * 1000
                MESSAGE_PROCESSING_TIME.labels(topic=self.topic).observe(duration)

    def send_to_dlq(self, msg, error: Exception):
        """Send failed message to dead-letter topic for replay."""
        dlq_producer.produce(
            topic=f"{self.topic}.dlq",
            key=msg.key(),
            value=msg.value(),
            headers={
                "original_topic": self.topic.encode(),
                "original_partition": str(msg.partition()).encode(),
                "original_offset": str(msg.offset()).encode(),
                "error": str(error).encode(),
                "timestamp": str(int(time.time())).encode(),
            },
        )
```

**Replay Strategy**:

```bash
# Replay DLQ messages after fixing the bug
kafka-console-consumer --bootstrap-server kafka:9092 \
  --topic documents.raw.dlq \
  --from-beginning \
  --timeout-ms 10000 | \
kafka-console-producer --bootstrap-server kafka:9092 \
  --topic documents.raw
```

### 7. Sentry Integration

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    integrations=[
        FastApiIntegration(),
        LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
    ],
    traces_sample_rate=0.1,  # 10% of transactions
    profiles_sample_rate=0.5,
    environment=os.environ.get("ENVIRONMENT", "production"),
    release=f"rag-api@{get_version()}",
)

# Custom error tagging
def handle_rag_error(error: Exception, query: str):
    with sentry_sdk.push_scope() as scope:
        scope.set_tag("error_type", type(error).__name__)
        scope.set_tag("rag.operation", "process_query")
        scope.set_context("query", {"length": len(query)})
        scope.set_user({"id": get_current_user_id()})
        sentry_sdk.capture_exception(error)

# Alert routing with fingerprinting — deduplicate similar errors
def sentry_before_send(event, hint):
    """Customize event before sending to Sentry."""
    # Fingerprint by error type + endpoint to group similar errors
    if "request" in event:
        fingerprint = [
            event.get("exception", {}).get("values", [{}])[0].get("type", "unknown"),
            event["request"].get("url", "unknown"),
        ]
        event["fingerprint"] = fingerprint
    return event
```

### 8. RAG/LLM Observability

```python
# Comprehensive RAG monitoring
class RAGMonitor:
    """Track RAG-specific metrics and detect anomalies."""

    def __init__(self):
        self.embedding_latencies = deque(maxlen=1000)
        self.retrieval_results = deque(maxlen=1000)
        self.response_scores = deque(maxlen=1000)

    def record_retrieval(self, query: str, contexts: list[str], latency_ms: float):
        self.retrieval_results.append({
            "query_length": len(query),
            "context_count": len(contexts),
            "context_lengths": [len(c) for c in contexts],
            "latency_ms": latency_ms,
        })

    def record_generation(self, response: str, latency_ms: float, tokens: int):
        self.response_scores.append({
            "response_length": len(response),
            "latency_ms": latency_ms,
            "tokens": tokens,
        })

    def check_anomalies(self) -> list[str]:
        """Detect anomalies in recent RAG operations."""
        alerts = []

        # Check retrieval degradation
        if self.retrieval_results:
            recent_avg = np.mean([r["context_count"] for r in list(self.retrieval_results)[-100:]])
            if recent_avg < 2.0:
                alerts.append(f"Low retrieval results: avg {recent_avg:.1f} contexts")

        # Check embedding latency spike
        if self.embedding_latencies:
            recent_p95 = np.percentile(list(self.embedding_latencies)[-100:], 95)
            if recent_p95 > 500:
                alerts.append(f"Embedding latency spike: P95={recent_p95:.0f}ms")

        return alerts
```

### 9. Chaos Drills & Runbooks

```yaml
# chaos-experiments.yaml
experiments:
  - name: embedding-service-outage
    description: Simulate embedding service failure
    steady_state_hypothesis:
      - type: probe
        provider:
          type: http
          url: http://rag-api/health
          method: GET
        expected_status: 200
    method:
      - type: action
        name: block-embedding-traffic
        provider:
          type: network
          action: block
          target: embedding-service:8000
        pauses:
          before: 5
          after: 5
      - type: action
        name: restore-embedding-traffic
        provider:
          type: network
          action: unblock
          target: embedding-service:8000
    rollbacks:
      - type: action
        name: full-restore
        provider:
          type: network
          action: unblock
          target: embedding-service:8000
```

**Runbook Template**:

```markdown
# Runbook: High Embedding Latency

## Alert
- **Name**: EmbeddingLatencyDegradation
- **Condition**: P95 embedding latency > 1s for 5m
- **Severity**: Warning

## Diagnosis
1. Check embedding service dashboard: `Grafana → RAG API → Embedding Latency P95`
2. Check for model version changes: `git log -5 -- src/embeddings/`
3. Check for resource saturation: `kubectl top pods -l app=embedding-service`
4. Check embedding model logs: `kubectl logs -l app=embedding-service --tail=100`

## Remediation
1. **If resource saturation**: Scale up embedding pods
   ```bash
   kubectl scale deployment embedding-service --replicas=6
   ```
2. **If model version regression**: Roll back embedding model
   ```bash
   kubectl set image deployment/embedding-service embed=embedding-model:v1.2.0
   ```
3. **If upstream dependency slow**: Check vector store health
   ```bash
   curl -f http://vector-store:8000/health
   ```

## Escalation
- If unresolved after 15m → page ML platform team
- If unresolved after 30m → page on-call engineering manager
```

### 10. Terraform Observability Module

```hcl
# modules/observability/main.tf
resource "aws_cloudwatch_log_group" "app" {
  name              = "/ecs/${var.service_name}"
  retention_in_days = var.log_retention_days
  kms_key_id        = aws_kms_key.logs.arn

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "${var.service_name}-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5xx"
  namespace           = "AWS/Usage"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "Alarm when 5xx errors exceed threshold"

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
}

resource "aws_sns_topic" "alerts" {
  name = "${var.service_name}-alerts"
}

resource "aws_sns_topic_subscription" "pagerduty" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "https"
  endpoint  = var.pagerduty_webhook_url
}

resource "grafana_dashboard" "service" {
  folder      = var.grafana_folder
  config_json = file("${path.module}/dashboards/${var.service_name}.json")
}
```

## Anti-Patterns

- **Logging at DEBUG in production** — massive log volume, high ingestion costs, slow queries
- **No correlation IDs** — impossible to trace a request across services in logs and traces
- **Sampling everything** — 100% trace sampling overwhelms storage; 0% hides critical errors
- **Alert fatigue** — alerting on every warning with no deduplication or routing, causing pages to be ignored
- **No runbooks** — alerts fire but engineers don't know how to diagnose or remediate
- **Ignoring tail-based sampling** — losing all error traces because head-based sampling filtered them out
- **No log retention policy** — logs accumulate indefinitely, blowing up storage costs
- **Monitoring without SLOs** — tracking metrics without defined targets makes it hard to prioritize
- **Dashboard sprawl** — hundreds of dashboards with no ownership or lifecycle management
- **No chaos testing** — never testing failure modes means surprise outages in production

## Best Practices

1. **Structured JSON logging in production** — parseable by log aggregators, includes trace/correlation IDs
2. **Define SLOs before building dashboards** — error budget, latency targets, and burn-rate alerts
3. **Multi-window multi-burn-rate alerting** — page on fast burn, ticket on slow burn, avoid alert fatigue
4. **Tail-based sampling** — always keep error traces and slow traces, sample the rest
5. **Correlation IDs end-to-end** — propagate from ingress through all downstream services and into logs
6. **Control log costs** — rotate, compress, and set retention; sample verbose logs to a separate stream
7. **RAG-specific metrics** — track embedding latency, retrieval hit-rate, cache hit-rate, and hallucination rate separately
8. **Dashboards as code** — version Grafana dashboards in Git with Jsonnet or JSON files
9. **Runbook for every alert** — no alert should fire without a documented diagnosis and remediation path
10. **Run chaos drills regularly** — test failure modes (service outage, high latency, data corruption) monthly
11. **Sentry fingerprinting** — group similar errors to reduce noise and track unique issue counts
12. **Provision observability with Terraform** — CloudWatch groups, SNS topics, Grafana dashboards all as code

## Related Skills

- **mlops-rag** — LangSmith, Phoenix, and WhyLabs for RAG-specific model observability
- **data-pipelines-ai** — monitoring pipeline health, data drift, and freshness SLAs
- **aws-devops** — CloudWatch, X-Ray, and deployment monitoring for AWS services
- **openai-api** — tracking token usage, API latency, and rate limit compliance
