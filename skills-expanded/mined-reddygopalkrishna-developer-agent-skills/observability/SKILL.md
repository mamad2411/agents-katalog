---
name: observability
description: Instruments services so production behavior can be understood and debugged - structured logs with trace correlation, RED/USE metrics with histograms and safe label cardinality, OpenTelemetry tracing and context propagation, SLOs with burn-rate alerts, dashboards and runbooks. Use when adding logging, metrics or tracing, setting up OpenTelemetry, defining SLIs/SLOs or alerts, reviewing instrumentation in a PR, or when a production issue could not be diagnosed from existing telemetry.
license: MIT
---

# Observability

Instrument so that you can answer a new question about production without shipping new code. Logs, metrics and traces should share one set of identifiers and names, carry no secrets, and lead to alerts that point at user pain, not at internal noise.

## When to use

- Adding or reviewing logs, metrics, traces or alerts.
- Setting up OpenTelemetry in a service.
- Defining SLIs and SLOs, or reworking noisy alerts.
- After an incident where the telemetry could not explain what happened.

Not for: debugging one specific bug locally (use a debugging skill), or picking an observability vendor.

## Workflow

1. **Find what exists.** Search for the logging library, the metrics client, any OpenTelemetry setup, and the existing dashboards and alerts. Extend the existing conventions instead of adding a second system.
2. **Name the questions** the telemetry must answer: "Is checkout working for users?", "Which dependency is slow?", "Which tenant is affected?". Instrument for those.
3. **Logs:** switch to structured logging with the standard fields below; add trace correlation.
4. **Metrics:** RED metrics for every request handler and outbound dependency, USE metrics for pools and queues. Latency as histograms.
5. **Traces:** enable OpenTelemetry auto-instrumentation first, then add manual spans around important business operations and any I/O that auto-instrumentation misses. Confirm context propagates across HTTP, gRPC and message boundaries.
6. **SLOs and alerts:** define SLIs from user-facing metrics, set SLO targets with the team, and alert on error-budget burn rate. Every alert links a runbook.
7. **Verify** by triggering a real request and a real error locally or in staging: find the trace, jump from a log line to its trace, see the metric move, and check that no secret or PII appears anywhere.

Read [references/opentelemetry-setup.md](references/opentelemetry-setup.md) when setting up OpenTelemetry in a specific language or configuring the Collector.

## Logs

Emit one JSON object per line to stdout (containers) and let the platform ship it.

```json
{"timestamp":"2026-11-03T14:05:00.123Z","level":"error","message":"payment declined",
 "service.name":"checkout","deployment.environment.name":"prod","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736",
 "span_id":"00f067aa0ba902b7","http.route":"/v1/payments","order_id":"ord_123","error.type":"CardDeclined"}
```

Rules:

- **Consistent field names across services.** Reuse OpenTelemetry semantic-convention names (`service.name`, `http.request.method`, `http.response.status_code`, `error.type`) instead of inventing new ones.
- **Always include `trace_id` and `span_id`** when a span is active. Most OpenTelemetry logging integrations add them automatically.
- **Messages are constant; data goes in fields.** `"payment declined"` + `order_id` field, not `"payment for ord_123 declined"`. That keeps logs searchable and groupable.
- **Levels mean something:**

| Level | Use for |
|---|---|
| ERROR | A request or job failed and someone may need to act |
| WARN | Unexpected but handled (retry succeeded, fallback used, deprecated input) |
| INFO | Significant lifecycle and business events (startup, config loaded, order placed) |
| DEBUG | Detail for diagnosis; off in production by default, switchable at runtime if possible |

- Log an error **once**, where it is handled, with the exception and stack trace. Not at every layer it passes through.
- **Never log secrets or PII:** passwords, tokens, API keys, session IDs, full card numbers, auth headers, full request bodies of sensitive endpoints. Add a redaction filter or processor for known keys as a safety net, but do not rely on it alone.
- Do not log in hot loops. Sample or aggregate into a metric instead.
- Escape or structure user input. Raw newlines in log text can forge fake log lines.

## Metrics

| Method | Applies to | Signals |
|---|---|---|
| RED | Request-driven services and each outbound dependency | **R**ate, **E**rrors, **D**uration |
| USE | Resources: CPU, memory, connection pools, thread pools, queues, disks | **U**tilization, **S**aturation, **E**rrors |
| Four golden signals (Google SRE) | User-facing systems | Latency, traffic, errors, saturation |

Rules:

- **Latency is a histogram**, never an average or a pre-computed percentile gauge. Percentiles cannot be averaged across instances; histograms can be aggregated and then turned into percentiles. Choose bucket boundaries around your SLO threshold (for example include 0.3 s if the SLO is "under 300 ms").
- **Units in base units and in the name:** seconds and bytes. Prometheus style: `http_server_request_duration_seconds`, counters end in `_total`. OpenTelemetry style: `http.server.request.duration` with unit `s`. Follow whichever the stack uses.
- **Count errors by type** with a bounded label (`error.type="timeout"`), and separate client errors (4xx) from server errors (5xx).
- **Label cardinality:** every distinct label combination is a separate time series. **Never** use user IDs, emails, request IDs, trace IDs, raw URLs, or unbounded free text as labels. Use the route template (`/users/{id}`), not the path (`/users/8431`). Keep each label to a small, known set of values.
- Saturation metrics for every pool and queue: in-use vs max connections, queue depth, oldest item age.
- Business metrics (orders placed, payments failed) are often the fastest signal that something is wrong. Add a few.

## Traces (OpenTelemetry)

- Use the OpenTelemetry API in code and the SDK + an OTLP exporter in configuration, sending to an OpenTelemetry Collector rather than straight to a vendor. That keeps the code vendor-neutral.
- Set `service.name` (via `OTEL_SERVICE_NAME`), `service.version` and the deployment environment (`deployment.environment.name` in current semantic conventions, `deployment.environment` in older ones) as resource attributes on every service. An unnamed service shows up as `unknown_service`.
- **Start with auto-instrumentation** (HTTP servers and clients, gRPC, database drivers, messaging), then add manual spans for business operations: `checkout.place_order`, `pricing.calculate`.
- **Propagation:** W3C Trace Context (`traceparent`, `tracestate` headers) is the default propagator. Format: `traceparent: 00-<32-hex trace id>-<16-hex parent span id>-<2-hex flags>`. For queues, inject the context into message headers on publish and extract it on consume. Check this boundary explicitly; it is the one that breaks most often.
- Span names are low-cardinality: `GET /users/{id}`, not `GET /users/8431`. Put IDs in attributes.
- Errors: set the span status to error, record the exception, and set `error.type`.
- Never put secrets or PII into span attributes or baggage. Baggage propagates to every downstream service, including third parties you call.
- **Sampling:** head sampling (`parentbased_traceidratio`) keeps costs predictable. Tail sampling in the Collector can keep all error and slow traces. Child services must respect the parent's sampling decision (the `parentbased_*` samplers do).

## SLIs, SLOs and alerts

1. **Pick SLIs that users feel:** availability (`good requests / valid requests`, where good is non-5xx) and latency (`requests faster than threshold / valid requests`), measured as close to the user as possible (load balancer or gateway).
2. **Set the SLO with the team:** for example 99.9% of checkout requests succeed over 30 days. Error budget = 1 - SLO.
3. **Alert on burn rate, not on causes.** Page when the budget is being used up fast enough to matter. A common multi-window setup for a 30-day SLO (from the Google SRE Workbook):

| Severity | Burn rate | Long window | Short window | Budget used |
|---|---|---|---|---|
| Page | 14.4 | 1 h | 5 min | 2% |
| Page | 6 | 6 h | 30 min | 5% |
| Ticket | 1 | 3 days | 6 h | 10% |

   The alert fires only if both windows exceed the rate. The short window lets it reset quickly after recovery.
4. **Do not page on causes** such as CPU at 80%, a single pod restart, or one 500. Turn them into dashboard panels or tickets.
5. **Every alert has:** a clear title naming the user impact, a link to a dashboard, and a link to a runbook (what it means, how to check, how to mitigate, who to escalate to). An alert nobody knows how to act on should be deleted or fixed.

## Dashboards

- One overview per service: RED for inbound traffic, RED per dependency, saturation of pools and queues, SLO and remaining budget, and deploy markers.
- Top-down order: user impact first, then drill-down panels.
- Use the same time range and labels as the alerts, so the alert link lands on the right view.

## Anti-patterns

- **printf logging in production** — unstructured, unsearchable, uncorrelated.
- **Logging and rethrowing at every layer** — one failure becomes ten error lines.
- **Average latency** — hides the tail where users suffer; use histograms and percentiles.
- **User IDs or URLs as metric labels** — cardinality explosion, slow queries and large bills.
- **Alerting on every cause** — alert fatigue; real pages get ignored.
- **Traces that stop at the queue** — no context propagated through message headers.
- **Secrets in logs or span attributes** — logs are copied widely and kept a long time.
- **A vendor SDK in business code** — use the OpenTelemetry API and swap backends through configuration.

## Done when

- Logs are structured JSON with consistent field names, levels and `trace_id`/`span_id`, and contain no secrets or PII.
- Every endpoint and dependency has rate, error and duration metrics; latency is a histogram; labels are bounded.
- One request can be followed end to end in a trace, including across a message queue if there is one.
- SLIs and SLOs are written down; alerts use burn rate; every alert has a runbook link.
- A test request and a forced error were checked end to end: log, metric and trace all show them and link to each other.

## References

- [references/opentelemetry-setup.md](references/opentelemetry-setup.md) — read when adding OpenTelemetry to a Java, Python, Node.js, .NET or Go service, or configuring the Collector and sampling.
