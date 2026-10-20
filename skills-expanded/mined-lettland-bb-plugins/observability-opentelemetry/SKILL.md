---
name: observability-opentelemetry
description: Use when instrumenting with OpenTelemetry — SDK setup (Go/Python/Node), collector config, resource attributes, sampling, propagation, semantic conventions.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: observability
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related:
    [
      observability-essentials,
      observability-sentry,
      observability-loki-alloy,
      infra-prometheus-grafana,
      go-essentials,
      python-essentials,
    ]
---

# Observability OpenTelemetry

**Iron Law: every service sets `service.name`, `service.version`, `deployment.environment` as resource attributes. Every cross-process boundary propagates W3C `traceparent`. Every collector pipeline has `memory_limiter` BEFORE `batch`. Sampling is configured intentionally — `parentbased_traceidratio(1.0)` is a bill, not a strategy.**

**Versions:** OTel spec `1.40+` · Collector `0.115+` (semconv `1.29.0`) · Go SDK `1.32+` · Python SDK `1.29+` · Node SDK `1.29+` — _Spec is stable for traces, metrics, logs. Semconv changes occasionally (HTTP semconv stabilized in 1.20; older attribute names like `http.method` are deprecated in favor of `http.request.method`). Pin SDK + semconv versions together._

## Three pillars, one SDK

OTel unifies traces, metrics, and logs under one SDK + one wire protocol (OTLP). Pre-OTel: pick a vendor per pillar (Jaeger for traces, Prom for metrics, Loki for logs). OTel: instrument once, swap backend by changing exporter config. Canonical setup: SDK in-app, OTLP to collector, collector fans out to Tempo (traces), Mimir (metrics), Loki (logs).

For the high-level "what is a span" + RED/USE basics, see `Skill(observability-essentials)`. This skill goes deeper: SDK setup per language, collector pipeline, sampling tradeoffs, semconv discipline.

## SDK setup — Go

```go
import (
    "context"
    "os"

    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/propagation"
    "go.opentelemetry.io/otel/sdk/resource"
    sdktrace "go.opentelemetry.io/otel/sdk/trace"
    semconv "go.opentelemetry.io/otel/semconv/v1.29.0"
)

const serviceVersion = "1.4.2"   // wire from build flags or runtime env in your app

func setupTracing(ctx context.Context) (func(context.Context) error, error) {
    res, _ := resource.New(ctx,
        resource.WithAttributes(
            semconv.ServiceName("gateway"),
            semconv.ServiceVersion(serviceVersion),
            semconv.DeploymentEnvironmentName(os.Getenv("ENV")),   // semconv v1.27+ replaces deprecated DeploymentEnvironment
        ),
        resource.WithProcess(), resource.WithOS(), resource.WithContainer())
    exp, _ := otlptracegrpc.New(ctx,
        otlptracegrpc.WithEndpoint(os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT"))) // alloy:4317
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithResource(res),
        sdktrace.WithBatcher(exp, sdktrace.WithMaxQueueSize(2048)),
        sdktrace.WithSampler(sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.05))))
    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(
        propagation.TraceContext{}, propagation.Baggage{}))
    return tp.Shutdown, nil
}
```

For chi: wrap with `otelhttp.NewMiddleware("server")` or `otelchi.Middleware`. Auto-instrumentation libs: `otelhttp`, `otelgrpc`, `otelpgx`, `otelchi`.

## SDK setup — Python

```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install              # auto-installs detected instrumentations
OTEL_RESOURCE_ATTRIBUTES="service.name=myapp,service.version=1.4.2,deployment.environment=prod" \
OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4317 \   # http:// is sidecar/loopback only; cross-host MUST be https://alloy:4317 with mTLS
opentelemetry-instrument python -m myapp
```

Manual setup follows the same shape as Go: `Resource.create({"service.name": ...})`, `TracerProvider(resource=..., sampler=ParentBased(TraceIdRatioBased(0.05)))`, `BatchSpanProcessor(OTLPSpanExporter())`. Auto-distro covers Django, FastAPI, requests, psycopg, redis with zero code.

## SDK setup — Node

```typescript
// Easiest: @opentelemetry/auto-instrumentations-node
// node --require @opentelemetry/auto-instrumentations-node/register app.js
// OTEL_SERVICE_NAME=myapp OTEL_EXPORTER_OTLP_ENDPOINT=http://alloy:4317  (cross-host: https:// + mTLS)

import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-grpc";
import { Resource } from "@opentelemetry/resources";
import { ATTR_SERVICE_NAME } from "@opentelemetry/semantic-conventions";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";

new NodeSDK({
  resource: new Resource({
    [ATTR_SERVICE_NAME]: "myapp",
    "service.version": process.env.VERSION,
    "deployment.environment": process.env.ENV,
  }),
  traceExporter: new OTLPTraceExporter(),
  instrumentations: [getNodeAutoInstrumentations()],
}).start();
```

For Cloudflare Workers: `@microlabs/otel-cf-workers` (sdk-node won't run; no Node primitives). See `Skill(infra-cloudflare-workers)`.

## Resource attributes — non-negotiable

`service.name` (every dashboard filters on this) · `service.version` (regression-after-deploy queries) · `deployment.environment` · `service.instance.id` (per-replica spikes) · `container.id`/`host.name`/`k8s.*` (infra bridge — auto via resource detectors). Set via SDK or `OTEL_RESOURCE_ATTRIBUTES=k=v,k=v`; env wins (handy for CI-injected `service.version`).

## Semantic conventions — use them, don't invent

`http.request.method=GET`, `http.response.status_code=200`, `url.path=/orders/123`, `db.system=postgresql`, `db.statement="SELECT ..."`, `messaging.system=kafka`. Full list: `opentelemetry.io/docs/specs/semconv/`.

Hand-string `"method"` instead of `semconv.HTTPRequestMethod("GET")` and vendor dashboards break, cross-service queries break, future-you migrates. Use the semconv package per language.

## Propagation — W3C TraceContext

```
traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01
             │   └─trace-id (16B hex)────────────┘ └─span-id 8B─┘ flags
```

Outgoing clients **inject**, incoming servers **extract** — automatic in auto-instrumented HTTP libs. For raw TCP/queues/custom protocols, inject into the message envelope:

```go
carrier := propagation.MapCarrier{}
otel.GetTextMapPropagator().Inject(ctx, carrier)
msg.Headers = carrier                                       // producer side
parentCtx := otel.GetTextMapPropagator().Extract(ctx, propagation.MapCarrier(msg.Headers))
ctx, span := tracer.Start(parentCtx, "process_message")     // consumer side
```

For Sentry/legacy B3: composite with `b3.New()` alongside `TraceContext{}`.

## Sampling

| Strategy                               | Where     | Notes                                                      |
| -------------------------------------- | --------- | ---------------------------------------------------------- |
| `AlwaysOn`                             | dev only  | bill explodes in prod                                      |
| `ParentBased(TraceIDRatioBased(0.05))` | SDK       | head-based, consistent, misses rare errors                 |
| `tail_sampling` processor              | collector | post-decision; needs `loadbalancing` exporter on `traceID` |

Recommended: 1–10% head + 100% errors + 100% slow via collector tail-sampler:

```yaml
tail_sampling:
  decision_wait: 10s
  policies:
    - { name: errors, type: status_code, status_code: { status_codes: [ERROR] } }
    - { name: slow, type: latency, latency: { threshold_ms: 1000 } }
    - { name: baseline, type: probabilistic, probabilistic: { sampling_percentage: 5 } }
```

Pair with `loadbalancing` exporter keyed by `traceID` so all spans of one trace land on the same replica.

## Collector pipeline — the minimum

```yaml
receivers:
  otlp: { protocols: { grpc: { endpoint: 0.0.0.0:4317 }, http: { endpoint: 0.0.0.0:4318 } } }

processors:
  memory_limiter: { check_interval: 1s, limit_mib: 1024, spike_limit_mib: 256 } # MUST be first
  batch: { timeout: 10s, send_batch_size: 1024 }
  resource: { attributes: [{ key: cluster, value: ci-swarm-prod, action: insert }] }

exporters: # http:// only within the same private network; cross-host MUST be https:// + auth on all three
  otlp/tempo: { endpoint: tempo:4317 }
  prometheusremotewrite/mimir: { endpoint: http://mimir:9009/api/v1/push }
  loki: { endpoint: http://loki:3100/loki/api/v1/push }

service:
  pipelines:
    traces: { receivers: [otlp], processors: [memory_limiter, resource, batch], exporters: [otlp/tempo] }
    metrics:
      { receivers: [otlp], processors: [memory_limiter, resource, batch], exporters: [prometheusremotewrite/mimir] }
    logs: { receivers: [otlp], processors: [memory_limiter, resource, batch], exporters: [loki] }
```

`memory_limiter` MUST run before `batch` (otherwise spikes fill queues → OOM). `batch` before exporter saves round-trips.

## Collector vs direct push

Direct = fewer hops, vendor lock at SDK level. Via collector = swap exporters without redeploy + centralized sampling/scrubbing/retry. Run a collector even at small scale — retrofitting touches every service.

## Antipatterns

- `parentbased_traceidratio(1.0)` in prod (ingest-bill explosion); head-only 1% with no tail (never see the errors)
- Custom attribute names (`req_method`, `requestMethod`) — use semconv; `trace_id` logged without SDK correlation
- `OTEL_EXPORTER_OTLP_INSECURE=true` in prod (PII + hostnames + query strings cross-host) — use TLS
- One unnamed global tracer (at least `otel.Tracer("orders")` so spans tag origin); missing `defer tp.Shutdown(ctx)` (spans dropped on exit)
- Tail-sampling without `loadbalancing` exporter routing on `traceID` (half a trace lands per collector — no full picture)

## Red flags

| Thought                                  | Reality                                                                  |
| ---------------------------------------- | ------------------------------------------------------------------------ |
| "Add OTel later"                         | Cross-service tracing requires every service — "later" = quarter of work |
| "Auto-instrumentation covers everything" | It covers HTTP + DB + queues; business logic spans you write             |
| "1% sampling is fine"                    | Until the error you need isn't in the 1% — sample errors at 100%         |
| "Direct to vendor is simpler"            | Until you switch vendors and redeploy 30 services                        |

## Hand-off

RED/USE basics + pillar choice: `Skill(observability-essentials)`. Metrics pipeline (Prometheus/Mimir + recording rules): `Skill(infra-prometheus-grafana)`. Loki/Alloy logs: `Skill(observability-loki-alloy)`. Sentry as a trace backend: `Skill(observability-sentry)`.
