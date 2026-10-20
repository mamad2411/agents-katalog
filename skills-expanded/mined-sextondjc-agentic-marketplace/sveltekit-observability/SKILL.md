---
name: sveltekit-observability
description: Use when adding OpenTelemetry tracing, instrumentation, or Server-Timing headers to a SvelteKit application via instrumentation.server.ts or the hooks-based instrumentation pattern.
---

# SvelteKit Observability

## Specialization

Expert guidance for observability in SvelteKit. Covers the `instrumentation.server.ts` lifecycle file for OpenTelemetry SDK initialisation, distributed tracing across server load functions and hooks, `Server-Timing` header instrumentation, integrating with observability platforms (Honeycomb, Jaeger, Grafana Tempo, Datadog), and correlating SvelteKit request traces with downstream service calls.

## Trigger Conditions

- Adding OpenTelemetry distributed tracing to a SvelteKit application.
- Diagnosing slow requests using `Server-Timing` headers.
- Instrumenting server load functions, hooks, or `+server.ts` endpoints with custom spans.
- Integrating a SvelteKit server with an observability backend (OTLP exporter, Honeycomb, etc.).
- Configuring `instrumentation.server.ts` for SDK startup and span propagation.
- Reviewing existing observability code for correct span lifecycle management.

## Scope Boundaries

In scope:

- `instrumentation.server.ts` (SvelteKit first-party instrumentation lifecycle file): placement, exports, and SDK initialisation timing.
- OpenTelemetry JS SDK setup: `@opentelemetry/sdk-node`, `NodeSDK`, `BatchSpanProcessor`, `OtlpHttpExporter`.
- Custom span creation inside `handle` hooks, server load functions, and `+server.ts` handlers.
- Context propagation: extracting trace context from incoming request headers; injecting into outgoing `fetch` calls.
- `Server-Timing` headers: adding `resolve()` with timing data from the `handle` hook.
- Resource attributes: service name, deployment environment, version tagging.
- Sampling configuration: head-based and tail-based sampling tradeoffs.
- Adapter compatibility: which adapters support `instrumentation.server.ts` (node, vercel, cloudflare workers limitations).
- Error recording on spans: `span.recordException()`, `span.setStatus(SpanStatusCode.ERROR)`.

Out of scope:

- Client-side browser performance tracing (Web Vitals, RUM) — `web-ux-performance` covers this.
- Log aggregation pipeline setup — infrastructure concern beyond SvelteKit's scope.
- Metrics collection (Prometheus, StatsD) — separate observability concern.
- APM agent auto-instrumentation outside of SvelteKit's `instrumentation.server.ts` pattern.

## Inputs

- Observability backend and exporter type (OTLP HTTP, OTLP gRPC, or platform-specific exporter).
- Service name and deployment environment identifiers.
- Target adapter (node, vercel, cloudflare, etc.) to determine `instrumentation.server.ts` support.
- Code paths to instrument (load functions, hooks, specific endpoints).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| `instrumentation.server.ts` | SDK initialisation file with correct OpenTelemetry provider and exporter setup |
| Span instrumentation | Custom spans in `handle` hook or load functions with correct start/end and attribute setting |
| Context propagation | Trace context extracted from incoming headers and injected into outgoing `event.fetch` calls |
| `Server-Timing` headers | Timing data surfaced in response headers for browser devtools visibility |
| Observability quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Initialise the OpenTelemetry SDK and confirm traces appear in the backend | `instrumentation.server.ts` initialises SDK; at least one root span visible per request |
| L2 Practical Delivery | Custom spans on all server load functions and a `Server-Timing` hook | Spans created and ended correctly; `Server-Timing` visible in browser network tab |
| L3 Specialist Hardening | Context propagation across downstream `fetch` calls and error recording | W3C trace context injected into outbound calls; errors recorded on spans |
| L4 Expert Standardisation | Production-grade tracing with sampling, resource attributes, and multi-service correlation | Sampling configured; service.name and environment set; traces correlated across services |

## Workflow

1. Install OpenTelemetry packages: `@opentelemetry/sdk-node`, `@opentelemetry/exporter-trace-otlp-http`, and any instrumentation packages needed (e.g. `@opentelemetry/instrumentation-http`).
2. Create `src/instrumentation.server.ts` (SvelteKit automatically imports this file before request handlers run on the server).
3. Inside `instrumentation.server.ts`, construct a `NodeSDK` with:
   - `resource`: `new Resource({ [SEMRESATTRS_SERVICE_NAME]: 'your-service', [SEMRESATTRS_DEPLOYMENT_ENVIRONMENT]: process.env.NODE_ENV })`.
   - `spanProcessor`: `new BatchSpanProcessor(new OtlpHttpExporter({ url: env.OTLP_ENDPOINT }))`.
   - `instrumentations`: auto-instrumentation packages as needed.
4. Call `sdk.start()` at module level in `instrumentation.server.ts`; do not call inside a function or conditional.
5. In `hooks.server.ts`, use the `handle` hook to create a root span per request, set HTTP attributes (`http.method`, `http.route`, `http.status_code`), and record any errors before ending the span.
6. For `Server-Timing` headers, call `resolve(event)` inside a wrapper that measures elapsed time and appends the `Server-Timing` header to the response.
7. For custom spans inside server load functions, call `trace.getActiveSpan()` or `tracer.startActiveSpan(name, fn)` to create child spans; always end spans in a `finally` block.
8. For context propagation to downstream services, use `propagation.inject(context.active(), headers)` when building `fetch` request headers inside server code.
9. For error recording, call `span.recordException(error)` and `span.setStatus({ code: SpanStatusCode.ERROR })` in catch blocks before rethrowing.
10. Run the observability quality checklist.

## Observability Quality Checklist

- [ ] `instrumentation.server.ts` exists at `src/instrumentation.server.ts` and initialises the SDK at module load time.
- [ ] SDK is started exactly once per process; no duplicate provider registrations.
- [ ] Service name and deployment environment are set as resource attributes.
- [ ] OTLP endpoint URL is sourced from `$env/dynamic/private`; it is not hardcoded.
- [ ] All custom spans are ended in a `finally` block; no span leaks.
- [ ] Error spans call both `recordException()` and `setStatus(ERROR)`.
- [ ] `Server-Timing` headers are set in the `handle` hook, not in individual load functions.
- [ ] Outgoing `fetch` calls propagate W3C trace context headers.
- [ ] Sampling is configured deliberately; default 100% sampling is only acceptable in development.
- [ ] Adapter compatibility is confirmed: `instrumentation.server.ts` requires a Node.js-compatible runtime (adapter-node, adapter-vercel with Node runtime).

## Security Notes

- OTLP endpoint URL and credentials must be kept in `$env/dynamic/private`; never hardcode them or store in `$env/static/public`.
- Spans may contain sensitive request data (URLs, params, user IDs); review attribute values before enabling tracing in production and ensure they comply with your data privacy policy.
- Do not log or trace authentication tokens, passwords, or session cookies as span attributes.
- Ensure the observability backend is access-controlled; trace data can reveal internal API structure and data access patterns.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| SDK initialisation | Workflow steps 1–4 |
| Root span per request | Workflow step 5 |
| `Server-Timing` headers | Workflow step 6 |
| Custom child spans | Workflow step 7 |
| Context propagation | Workflow step 8 |
| Error recording | Workflow step 9 |
| Security configuration | Security Notes + checklist |
| Quality validation | Observability Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
