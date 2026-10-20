---
name: observability-essentials
description: Use when adding logs, metrics, or traces — structured logging, Prometheus metrics with bounded cardinality, OpenTelemetry traces.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: observability
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [observability-sentry, debugging, root-cause, rest-essentials]
  keywords: [production, prod, monitoring]
---

# Observability Essentials

**Iron Law: structured logs (JSON), bounded-cardinality metrics, OTel traces. Three pillars; missing one and you're blind.**

## Three pillars — what each is for

| Pillar      | Answers                                       | When to reach for it                   |
| ----------- | --------------------------------------------- | -------------------------------------- |
| **Logs**    | "What happened on this specific request?"     | narrative, debugging individual events |
| **Metrics** | "How often / how slow / how many?"            | aggregates, dashboards, alerting       |
| **Traces**  | "Where in this distributed call did time go?" | latency analysis across services       |

Use all three — they answer different questions. Choosing one means giving up the other answers.

## Logs — structured (JSON), correlated

Free-form `printf` logs do not survive production. Emit JSON with stable keys.

```go
// Go: log/slog
slog.SetDefault(slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
})))
slog.InfoContext(ctx, "order.created",
    slog.String("order_id", id),
    slog.String("trace_id", trace.SpanContextFromContext(ctx).TraceID().String()),
)
```

```typescript
// Node: pino
import { pino } from "pino";
const log = pino({ level: "info" });
log.info({ order_id: id, trace_id }, "order.created");
```

```python
# Python: structlog or stdlib logging w/ JSON formatter
import structlog
log = structlog.get_logger()
log.info("order.created", order_id=id, trace_id=trace_id)
```

| Level              | Use for                                |
| ------------------ | -------------------------------------- |
| `DEBUG`            | local dev; off in prod or sampled      |
| `INFO`             | one line per request, lifecycle events |
| `WARN`             | recovered or unexpected but not failed |
| `ERROR`            | request failed; needs investigation    |
| `FATAL`/`CRITICAL` | process must die                       |

**What to redact** before the line hits stdout: passwords, tokens, API keys, full credit cards, SSNs, raw OAuth codes, session cookies. Build a serializer that strips known keys; don't trust each call site.

**Correlation ID:** every log line must carry `trace_id` (or `request_id` for non-traced systems). Without it, you can't reconstruct a multi-service flow.

## Metrics — Prometheus model

Three core types:

| Type          | What                     | Example                                      |
| ------------- | ------------------------ | -------------------------------------------- |
| **Counter**   | monotonically increasing | `http_requests_total{method, status, route}` |
| **Gauge**     | up/down value            | `db_connections_in_use`, `queue_depth`       |
| **Histogram** | distribution → buckets   | `http_request_duration_seconds{le}`          |

Summary exists but histograms are usually right — they aggregate across instances.

### Cardinality is the only thing that matters

Each unique label combination is a separate time series. `user_id` as a label = one series per user = OOM.

```
# DON'T
http_requests_total{user_id="abc123", request_id="req_..."}    # unbounded

# DO
http_requests_total{method="GET", status="200", route="/orders/:id"}  # bounded
```

**Routes must be templated** (`/orders/:id`, not `/orders/12345`). Most frameworks template via middleware — verify yours does.

Hard cap to keep in mind: aim for < 10k series per service. Past 100k, Prometheus storage hurts.

### What to instrument — RED & USE

| Pattern | For                              | Metrics                                     |
| ------- | -------------------------------- | ------------------------------------------- |
| **RED** | request-driven services          | **R**ate, **E**rrors, **D**uration          |
| **USE** | resources (CPU, disk, conn pool) | **U**tilization, **S**aturation, **E**rrors |

RED is the right default for HTTP/gRPC/queue services. USE complements it for the underlying infra.

```
# Three lines that cover RED for HTTP
http_requests_total{route, method, status}                # rate + errors (by status)
http_request_duration_seconds_bucket{route, method, le}   # duration histogram
http_requests_in_flight{route}                            # saturation gauge
```

Histogram buckets matter: tune them to your SLOs. Default `[0.005, 0.01, 0.025, ...]` works for sub-second APIs; tune for batch jobs (`[1, 5, 30, 60, 300]`).

## Traces — OpenTelemetry

A **trace** is the full request across services. A **span** is one unit of work (HTTP handler, DB query, RPC). Spans nest by parent-child; context propagates via headers.

```go
// Go OTel
tracer := otel.Tracer("orders")
ctx, span := tracer.Start(ctx, "CreateOrder",
    trace.WithAttributes(attribute.String("customer.id", id)))
defer span.End()
// span errors automatically captured via span.RecordError(err)
```

```python
# Python OTel
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("create_order") as span:
    span.set_attribute("customer.id", id)
```

### SDK status (as of 2026)

| Language | OTel SDK status                                                                 | Auto-instrumentation                     |
| -------- | ------------------------------------------------------------------------------- | ---------------------------------------- |
| Go       | stable                                                                          | yes (chi, gin, pgx, gRPC, http)          |
| Python   | stable                                                                          | yes (django, fastapi, requests, psycopg) |
| Node     | stable                                                                          | yes (express, fastify, http, pg, redis)  |
| Java     | stable                                                                          | yes (Java agent — zero-code)             |
| Rust     | stable (`opentelemetry` crate; bridge to `tracing` via `tracing-opentelemetry`) | per-crate                                |
| .NET     | stable                                                                          | yes                                      |
| Ruby     | stable                                                                          | yes                                      |
| PHP      | beta                                                                            | partial                                  |

Reach for auto-instrumentation first; add manual spans where the auto coverage misses (business logic).

### Context propagation — across **every** boundary

Default propagator: W3C `traceparent` header (and `tracestate`). Outgoing HTTP/gRPC clients **must** inject it; servers **must** extract.

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │  └─trace-id (16B hex)─────────────┘ └─span-id──────┘ flags
```

Missing propagation = orphan spans = "where did the time go?" with no answer. For message queues, propagate via headers (Kafka) or a `traceparent` field in the message envelope.

### Exporter & collector

```
app → OTLP/gRPC (4317) or OTLP/HTTP (4318) → OTel Collector → [Jaeger / Tempo / Honeycomb / Datadog / Sentry]
```

The Collector is a separate process (sidecar, daemonset, or shared). Lets you swap backends without changing app code, batch, retry, sample, scrub. Run one even at small scale — it's hard to add later.

**TLS / auth: OTLP is plaintext by default.** Spans carry PII, internal hostnames, and call topology. For any cross-host hop: enable TLS on the receiver (`tls.cert_file` / `tls.key_file` in the Collector), require mTLS (client cert — preferred) OR a bearer token, and never bind `0.0.0.0:4317` without auth. Don't ship insecure-mode flags to prod — the exact env var name varies by SDK (`OTEL_EXPORTER_OTLP_INSECURE` in Go; `OTEL_EXPORTER_OTLP_TRACES_INSECURE` in Python). Sidecar/loopback may legitimately run plaintext; cross-host must not.

**Sampling.** Head-based (decide at start, propagate) is simple and consistent — recommended default. Tail-based (decide after seeing all spans) catches errors and slow traces but requires the Collector to buffer state; **Collector restarts drop the buffered traces** mid-decision window, so for 100% error coverage pair the `tail_sampling` processor with a `loadbalancing` exporter routing on `trace_id` so all spans for a trace land on the same Collector replica (this is the canonical OTel-native pattern). Third-party services like Honeycomb Refinery or Grafana Agent offer state-aware alternatives. Aim 1–10% baseline + 100% errors + 100% high-latency.

## Anti-patterns

- Free-form text logs in production ("Order 123 created" with no JSON shape)
- `user_id`, `request_id`, raw URLs as **metric labels** → cardinality explosion
- Missing trace-context propagation between services → orphan spans
- Logs without `trace_id` → can't pivot between traces and logs
- One global log level, no per-module override
- Histogram buckets at the default for a 10ms-p99 API (all values in the first bucket)
- Sampling everything at 1% then wondering why errors don't show up — sample errors at 100%
- Logging PII/secrets without a redaction layer
- "We'll add tracing later" — adding instrumentation across 30 services is much harder later

## Red flags

| Thought                                              | Reality                                                                |
| ---------------------------------------------------- | ---------------------------------------------------------------------- |
| "We have logs, we're fine"                           | Logs answer "what". Metrics answer "how often". Traces answer "where". |
| "Cardinality won't explode"                          | One mis-templated route ID and you're at 1M series tomorrow.           |
| "Auto-instrumentation is magic"                      | It instruments HTTP/DB. Business logic spans you write.                |
| "We'll standardize on Datadog so we don't need OTel" | Then you marry one vendor. OTel keeps you portable.                    |

## Hand-off

For error tracking and stack-frame analysis: `Skill(observability-sentry)`. For working backward from a symptom to a fix: `Skill(debugging)` and `Skill(root-cause)`. For HTTP `request_id` shape: `Skill(rest-essentials)`.
