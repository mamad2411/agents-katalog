---
name: tracing-strategy-otel
description: Design an OpenTelemetry tracing strategy — sampling, attribute discipline, span hygiene, context propagation, baggage, cost-aware exporter config.
---

# tracing-strategy-otel

> Trace what matters at a sampling rate you can afford. Output is a service's tracing plan.

## When to use

- A new service needs tracing and you want the right setup, not a copy-paste.
- An existing OTel deployment is expensive and the team can't tell why.

## Procedure

1. **SDK** — language-official OTel SDK. Auto-instrumentation for HTTP / DB / gRPC; manual spans for business-meaningful operations.
2. **Sampling** — pick a strategy:
   - **Head-based, parent-aware** — `ParentBased(TraceIdRatioBased(0.1))` keeps 10% of root spans, follows the parent decision for children. Cheap, deterministic, predictable cost.
   - **Tail-based** — sample at the collector based on error / latency outcome. Catches all errors; needs collector capacity.
   - **Adaptive** — let the collector tune sampling rate per route. Use when traffic is bursty.
   Start head-based at 10%; layer tail-based at the collector when you can afford a collector.
3. **Span hygiene**:
   - One span per logical step (DB call, external call, business operation). Not per function.
   - Span name = stable identifier (`HTTP GET /v1/orders/{id}`, not `getOrder(42)`).
   - Status: set to `ERROR` only when the span itself failed. Don't propagate child errors upward unless they cause the parent to fail.
4. **Attribute discipline**:
   - Use OTel semantic conventions (`http.request.method`, `db.system`, `service.name`, etc.).
   - **Don't** put high-cardinality values as resource attributes (user_id is OK as a span attribute; never as a resource attribute).
   - **Don't** add ad-hoc attributes the cardinality of which you can't predict.
5. **Context propagation** — W3C `traceparent` / `tracestate` headers on every outbound call. If you control both sides and have legacy clients, keep `b3` headers as a fallback during migration.
6. **Baggage** — sparingly. Each item rides every request downstream. `user_tier` is fine; `entire user object JSON` is not.
7. **Exporter config**:
   - OTLP/gRPC to a collector. Don't push directly from app to vendor backend; the collector is the choke point you tune.
   - Collector samples / batches / re-routes. App stays simple.
8. **Cost target** — explicit. Sample rate × request rate × span size × attribute count. Make the rough math fit your budget before turning it on.

## Output

```text
Tracing strategy: refund-service

SDK: OpenTelemetry Go SDK 1.x, auto-instrumented (HTTP server,
HTTP client, database/sql).

Sampling:
  App: ParentBased(TraceIdRatioBased(0.1))   → keep 10% of roots.
  Collector: tail-based on error or latency > 1s → keep 100% of those.

Span hygiene:
  Manual spans for: refund_create, downstream.stripe, db.refund_insert.
  Span names use route templates, never raw paths with IDs.

Attribute conventions:
  Always: service.name, service.version, deployment.environment.
  Per span: http.request.method, http.response.status_code,
            db.system, db.statement (sanitized).
  User-related: user.tier (low cardinality). NEVER user.id as resource.

Propagation: W3C tracecontext only.

Baggage: user.tier only.

Exporter: OTLP/gRPC to in-cluster collector.
  Collector → Tempo (traces) + sample to vendor X (errors only).

Cost target: $400/mo at 10% sampling + tail-based error capture.
  Sample rate is the cheapest dial to turn if cost grows.
```

## Anti-patterns to avoid

- 100% sampling "to see everything" — bills explode, signal doesn't improve.
- Spans per function (huge trees, noise).
- user_id as resource attribute (cardinality explosion in the backend).
- Direct vendor exporter from each app pod (no collector buffer to tune).
