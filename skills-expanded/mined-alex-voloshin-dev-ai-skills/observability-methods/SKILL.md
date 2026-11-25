---
name: observability-methods
description: Use this skill when picking a diagnostic vocabulary for a latency, error-rate, saturation, or crashloop investigation, when authoring or reviewing an analysis workflow that needs the method reference, or when correlating SLI metrics and active alerts against a method's signal set — a knowledge skill of industry-canonical observability methodologies (Four Golden Signals, RED, USE, Distributed Tracing) with method-to-problem mapping that explains which signals each method surfaces and when each method applies. Loaded by `/analyze-prod`, `/analyze-local`, `/env-analyze`, `/infra-change`, and `/bugfix` workflows when production-context diagnosis needs a named methodology.
disable-model-invocation: true
---

# Observability Methods

Reference for the four industry-canonical observability methodologies used by production-analysis and incident-response workflows in this plugin. Pick one named method per problem class to give analysis a vocabulary handle and a defined signal coverage. Cross-reference SLI metrics, error-budget burn, and active alerts against the chosen method's signals.

## Four Golden Signals (Google SRE)

Source: [SRE Book Ch. 6 — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/).

User-facing service monitoring. Tracks the four signals a user-visible service must expose:

- **Latency** — p50 / p95 / p99. Success and failed requests must be tracked **separately** (failed-fast errors otherwise hide tail latency).
- **Traffic** — demand on the service, typically requests per second (RPS) or transactions per second.
- **Errors** — rate of failed requests, broken down by error type (5xx, 4xx, timeouts, business-logic errors).
- **Saturation** — how "full" the service is — resource headroom before degradation (CPU, memory, queue depth, connection pool, thread pool).

Apply when: the service is user-facing, has a defined SLO, or owns an SLI.

## RED Method (Tom Wilkie — microservices)

Source: [RED Method](https://thenewstack.io/monitoring-microservices-red-method/).

Request-driven microservices. Three signals per service:

- **Rate** — requests per second the service is handling.
- **Errors** — number/percentage of failed requests.
- **Duration** — distribution of request latency, especially the p99 tail.

Apply when: diagnosing a request-response microservice, especially with many small services where per-service uniformity matters more than resource depth. Strong fit for slow-API and 5xx-spike investigations.

## USE Method (Brendan Gregg — resources)

Source: [USE Method](https://brendangregg.com/usemethod.html).

Resource-driven. For every resource (CPU, memory, disk, network, queue), check three signals:

- **Utilization** — percentage of time the resource was busy.
- **Saturation** — degree of extra work queued / waiting (run queue, swap, retries).
- **Errors** — error events for that resource (OOMKilled, disk I/O errors, NIC drops).

Apply when: resource exhaustion is suspected — OOMKilled pods, CPU throttling, disk pressure, node-level pressure, container crashloops driven by limits.

## Distributed Tracing

For latency or cross-service failures, a single trace through 5–7 services is the canonical root-cause path:

- **Storage**: Tempo / Jaeger / Zipkin.
- **Instrumentation**: OpenTelemetry SDK (vendor-neutral) or vendor agent (Datadog APM, New Relic, Honeycomb Beelines).
- **Search**: by `service.name`, `trace.id`, or slow-trace heatmap. Honeycomb BubbleUp narrows attributes that correlate with slow traces.
- **Span attributes that matter**: HTTP route, DB query (statement + duration), external API call (host + latency), retry count, error/exception flag.

Apply when: a request crosses ≥2 services, latency is high but no single service is obviously saturated, error blame is unclear, or aggregate metrics show the symptom but not the cause.

## Method-to-Problem Mapping

| Problem | Method | Why |
|---|---|---|
| Slow API | RED | Duration p99 tail is the surfaced signal |
| 5xx spike | Golden Signals | Errors + Saturation cover cause and capacity together |
| OOMKilled / crashloop | USE | Memory/CPU saturation + resource errors |
| Customer-reported latency | RED + Distributed Tracing | RED localizes the slow service, tracing finds the slow span |
| Node / disk pressure | USE | Resource-axis Utilization + Saturation |
| Cross-service failure (no single hotspot) | Distributed Tracing | Single trace reveals the failing hop |
| New service with SLO | Golden Signals | Establish baseline for all four user-facing signals |

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `/analyze-prod` (snapshot phase) | Pick a named method per problem class before running queries; cross-reference SLI/SLO and alerts against the method's signals |
| `/analyze-local` (Docker logs) | Apply USE on container resource limits when local services crashloop or are OOMKilled |
| `/env-analyze` (multi-scope) | Use Golden Signals or RED to frame service-level findings; USE for node/resource layer |
| `/infra-change` (post-apply verify) | Use Golden Signals to confirm SLO is not regressed by the change |
| `/bugfix` (production-context bugs) | Use RED + tracing to localize the failing service / span before code-level investigation |

## Integration

- **Used by**: `/analyze-prod`, `/analyze-local`, `/env-analyze`, `/infra-change`, `/bugfix`
- **Companion knowledge**: `@telemetry-stacks` (vendor-specific queries that surface these signals), `@cloud-platforms` (managed-service metric sources), `@deployment-procedures` (post-deploy health verification)
- **External references**:
  - Google SRE Book Ch. 6 — Monitoring Distributed Systems (Four Golden Signals)
  - Tom Wilkie — RED Method
  - Brendan Gregg — USE Method
  - OpenTelemetry specification (tracing semantic conventions)
