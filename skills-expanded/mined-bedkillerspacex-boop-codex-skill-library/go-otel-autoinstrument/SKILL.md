---
name: go-otel-autoinstrument
description: >
  OpenTelemetry Go auto-instrumentation and SDK setup: otelhttp/otelgrpc middleware,
  global TracerProvider, propagators (W3C), exporters (OTLP), sampling, and
  resource attributes. Use for owned services adding traces/metrics — not to
  exfiltrate telemetry from systems without authorization.
---

# Go OpenTelemetry Auto-Instrumentation

## Scope And Authorization

- **In scope:** Services you operate; exporters pointed at your collectors.
- **Out of scope:** Pointing telemetry scrapers at third-party systems without permission;
  shipping PII in span attributes.
- Prefer OTLP to your collector; scrub secrets from attributes.
- Pair with `observability-metrics-tracing` and `code-quality-standards`.

## When To Use

- Adding baseline HTTP/gRPC tracing with official otel contrib instrumentation.
- Standardizing trace context propagation across Go microservices.
- Configuring sampling and resource detection for K8s.
- Bridging auto-instrumentation with manual spans for business ops.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org-wide observability strategy | `observability-metrics-tracing` |
| Structured logging | `go-slog-structured-logging` |
| Context timeouts | `go-context-timeouts` |
| Go style | `go-style-conventions` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| TracerProvider | Creates tracers; shutdown flushes |
| MeterProvider | Metrics |
| Propagator | Inject/extract W3C `traceparent` |
| otelhttp / otelgrpc | Auto middleware/interceptors |
| OTLP exporter | gRPC/HTTP to collector |
| Resource | `service.name`, version, env |
| Sampling | Head sampling (ratio, parent-based) |
| Manual span | `tracer.Start` for domain ops |

“Auto-instrumentation” here means **library middleware** (and optionally eBPF/go auto
agent products) — wire libraries explicitly in Go.

## Workflow

### 1. Define telemetry requirements

1. Service name, environments, collector endpoint, PII policy.
2. Success: inbound HTTP spans appear; outbound child spans linked; dashboards work.

### 2. Install modules

```bash
go get go.opentelemetry.io/otel@latest
go get go.opentelemetry.io/otel/sdk@latest
go get go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp@latest
go get go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@latest
```

Pin versions via go.mod tidy; keep otel modules compatible.

### 3. Bootstrap provider (sketch)

```go
func InitTracer(ctx context.Context) (func(context.Context) error, error) {
    exp, err := otlptracehttp.New(ctx,
        otlptracehttp.WithEndpoint(os.Getenv("OTEL_EXPORTER_OTLP_ENDPOINT")),
        otlptracehttp.WithInsecure(), // only if appropriate; prefer TLS
    )
    if err != nil {
        return nil, err
    }
    tp := sdktrace.NewTracerProvider(
        sdktrace.WithBatcher(exp),
        sdktrace.WithResource(resource.NewWithAttributes(
            semconv.SchemaURL,
            semconv.ServiceName("checkout-api"),
            semconv.ServiceVersion("1.4.0"),
        )),
        sdktrace.WithSampler(sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.1))),
    )
    otel.SetTracerProvider(tp)
    otel.SetTextMapPropagator(propagation.TraceContext{})
    return tp.Shutdown, nil
}
```

Call `shutdown` on process exit.

### 4. HTTP auto-instrumentation

```go
mux := http.NewServeMux()
mux.Handle("/api/", handler)
var h http.Handler = otelhttp.NewHandler(mux, "checkout-api")
// outbound:
client := &http.Client{Transport: otelhttp.NewTransport(http.DefaultTransport)}
```

Gin: use contrib otelgin middleware if available for your stack.

### 5. gRPC

```go
// stats handlers / interceptors from otelgrpc
// grpc.NewServer(grpc.StatsHandler(otelgrpc.NewServerHandler()))
// grpc.Dial(..., grpc.WithStatsHandler(otelgrpc.NewClientHandler()))
```

### 6. Manual spans for business

```go
ctx, span := otel.Tracer("checkout").Start(ctx, "ReserveInventory")
defer span.End()
span.SetAttributes(attribute.String("order.id", orderID)) // no PII/secrets
```

### 7. Verify

| Check | Expect |
| --- | --- |
| Collector receives spans | service.name correct |
| Inbound → outbound | Parent/child linked |
| Errors | `span.RecordError` / status set |
| Shutdown | No truncated batch on exit (graceful) |
| PII | Attributes scrubbed |

### 8. Operate

- Alert on export failures.
- Tune sampling for high QPS.
- Correlate logs with trace_id (`go-slog-structured-logging`).
- Avoid high-cardinality attributes (raw URLs with IDs explosion).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Names | Stable `service.name` | Hostname as service name |
| Attributes | Low cardinality | User email on every span |
| Sampling | Parent-based + ratio | 100% forever in huge prod |
| Shutdown | Flush on SIGTERM | Kill -9 only |
| Secrets | Never as attributes | Auth header capture |

## Output Checklist

- [ ] Provider init + shutdown wired
- [ ] Propagators set (W3C)
- [ ] HTTP/gRPC instrumentation applied
- [ ] OTLP endpoint via config/env
- [ ] Resource attributes set
- [ ] Sampling policy documented
- [ ] PII scrub reviewed
- [ ] Traces verified in backend
- [ ] Log correlation optional done
- [ ] `code-quality-standards` applied

## Rules

- Owned services; authorized collectors only.
- No secrets/PII in telemetry.
- Always shutdown providers cleanly.
- Library instrumentation + sparse manual spans.
- Broader SLO strategy → observability skill.
