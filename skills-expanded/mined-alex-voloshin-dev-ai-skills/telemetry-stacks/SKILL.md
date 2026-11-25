---
name: telemetry-stacks
description: Use this skill when querying a production telemetry stack, when authoring or reviewing an analysis workflow that needs vendor query examples, or when identifying which stack is deployed from `CLAUDE.md`, helm charts, `prometheus-operator` CRDs, or an OTel collector config — a knowledge skill providing a production telemetry stack reference covering Prometheus + Grafana, Datadog, Honeycomb, New Relic, Sentry, and OpenTelemetry + Tempo / Jaeger, with per-stack ingestion model, query patterns, UI surface, and when each stack is the right choice. Loaded by `/analyze-prod`, `/analyze-local`, `/env-analyze`, `/infra-change`, and `/bugfix` workflows when production-context diagnosis needs vendor-specific query syntax.
disable-model-invocation: true
---

# Telemetry Stacks

Reference for the production telemetry stacks supported by `/analyze-prod` and related analysis workflows. Identify the stack by checking `CLAUDE.md`, helm charts, `prometheus-operator` CRDs, or OTel collector configuration, then query directly using the patterns below. Pair with `@observability-methods` to map the surfaced signals (Latency / Traffic / Errors / Saturation, or Rate / Errors / Duration, or Utilization / Saturation / Errors) onto vendor queries.

## Stack Reference Table

| Stack | Where to look | Common queries |
|---|---|---|
| **Prometheus + Grafana** | Dashboards, Alertmanager, `prometheus-operator` CRDs | `rate(http_requests_total[5m])`, `histogram_quantile(0.99, ...bucket[5m])`, `up == 0` |
| **Datadog** | APM, Service Catalog, Logs | `service:x error_rate`, `@http.status_code:5*`, anomaly monitors |
| **Honeycomb** | Tracing + BubbleUp | `WHERE service.name=x \| HEATMAP duration_ms`, BubbleUp on slow traces |
| **New Relic** | APM + Distributed Tracing | `SELECT percentile(duration,50,95,99) FROM Transaction WHERE appName='x'` |
| **Sentry** | Issues filtered to release | error patterns + breadcrumbs (frontend / mobile) |
| **OTel + Tempo / Jaeger** | Tempo / Jaeger UI | trace search by `service.name`, `trace.id` |

## Prometheus + Grafana

**Ingestion**: pull-based scrape from `/metrics` endpoints; service discovery via Kubernetes API; long-term storage often via Thanos / Mimir / Cortex. PromQL is the query language.

**Surface**: Grafana dashboards (panels), Alertmanager (alerts), Prometheus UI (ad-hoc PromQL).

**Common queries**:
- Request rate: `rate(http_requests_total[5m])`
- p99 latency: `histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))`
- Error rate: `sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))`
- Target down: `up == 0`
- Saturation (CPU throttling): `rate(container_cpu_cfs_throttled_seconds_total[5m])`

**Right choice when**: Kubernetes-native shop, open-source preference, cost-sensitive, custom application metrics dominate.

## Datadog

**Ingestion**: push-based via Datadog Agent (per node) and APM tracer libraries (in-process). Auto-instruments common frameworks; log collection via agent tail.

**Surface**: APM service map and traces, Service Catalog, Logs Explorer, Dashboards, Monitors (alerts), Watchdog (anomaly detection).

**Common queries**:
- Service error rate: `service:x error_rate`
- HTTP 5xx logs: `@http.status_code:5*`
- Custom metric: `avg:trace.http.request.duration{service:x} by {resource_name}`
- Anomaly monitors and forecast monitors for capacity planning

**Right choice when**: managed SaaS preferred, multi-language polyglot stack, want APM + logs + metrics + RUM in one product, budget allows.

## Honeycomb

**Ingestion**: push-based via OpenTelemetry or Honeycomb Beelines; event-based model — each event is a wide-column record with high-cardinality attributes.

**Surface**: Query Builder, BubbleUp (attribute correlation), Triggers (alerts), Service Map.

**Common queries**:
- Heatmap of latency: `WHERE service.name=x | HEATMAP duration_ms`
- BubbleUp on slow traces: select a slow region on the heatmap, BubbleUp surfaces which attributes (customer, endpoint, region) correlate with slowness.
- Group by high-cardinality attribute: `GROUP BY user.id, ORDER BY P99(duration_ms) DESC`

**Right choice when**: high-cardinality debugging (per-customer, per-tenant, per-endpoint), tracing-first culture, hard-to-reproduce intermittent issues.

## New Relic

**Ingestion**: push-based via New Relic agents (per language) and OTel; NRQL (New Relic Query Language) for queries.

**Surface**: APM, Distributed Tracing, Logs, Browser, Infrastructure, Alerts.

**Common queries**:
- Percentile latency: `SELECT percentile(duration, 50, 95, 99) FROM Transaction WHERE appName='x'`
- Error rate: `SELECT percentage(count(*), WHERE error IS true) FROM Transaction WHERE appName='x'`
- Throughput by endpoint: `SELECT rate(count(*), 1 minute) FROM Transaction WHERE appName='x' FACET name`

**Right choice when**: enterprise with mixed legacy + modern stacks, want bundled APM + Infra + Logs + Browser, NRQL familiarity exists.

## Sentry

**Ingestion**: push-based via Sentry SDKs (per language / framework); event-based — each event is an error / exception with stack trace, breadcrumbs, and context.

**Surface**: Issues view (grouped errors), Releases, Performance (transaction tracing), Alerts.

**Common queries / filters**:
- Filter by release: `release:1.2.3 environment:production`
- Filter by user impact: sort issues by `users` affected, descending
- Error patterns + breadcrumbs (frontend / mobile) — breadcrumbs reconstruct user actions before the error
- Suspect commits — Sentry links error frames to git commits via release tracking

**Right choice when**: frontend / mobile error tracking is the priority, want error-grouping + release correlation, paired with another stack for infra metrics.

## OpenTelemetry + Tempo / Jaeger

**Ingestion**: push-based via OTel SDKs and OTel Collector; vendor-neutral semantic conventions. Tempo (Grafana Labs) and Jaeger (CNCF) are open-source trace storage backends.

**Surface**: Tempo UI or Jaeger UI; Grafana panels (TraceQL in Tempo); often paired with Prometheus for metrics and Loki for logs (the "LGTM stack" — Loki, Grafana, Tempo, Mimir).

**Common queries**:
- Trace search: `{ service.name = "checkout" && duration > 1s }` (TraceQL)
- Find trace by ID: paste `trace.id` into the UI
- Service dependency map: derived from spans
- Span attribute filters: `http.status_code`, `db.statement`, `error=true`

**Right choice when**: vendor-neutral instrumentation is a priority, open-source stack preferred, already running Grafana + Prometheus and want tracing in the same UI.

## Choosing a Stack

| Constraint | Likely stack |
|---|---|
| Kubernetes-native, OSS, custom metrics dominate | Prometheus + Grafana (+ Tempo for tracing) |
| Managed SaaS, polyglot, all-in-one | Datadog or New Relic |
| High-cardinality debugging | Honeycomb |
| Frontend / mobile error tracking | Sentry (alongside another stack) |
| Vendor-neutral, OSS tracing-first | OTel + Tempo / Jaeger |

## When this applies

| Workflow | Apply this knowledge |
|---|---|
| `/analyze-prod` (snapshot phase) | Identify the stack from `CLAUDE.md` / helm / CRDs, then run vendor-specific queries to surface the signals chosen via `@observability-methods` |
| `/analyze-local` (Docker logs) | If a local stack ships Prometheus / Grafana / OTel containers, use the same query patterns against the local endpoints |
| `/env-analyze` (multi-scope) | Cross-reference K8s pod state with telemetry-stack metrics (Datadog Service Map, Prometheus `up`, Honeycomb heatmap) |
| `/infra-change` (post-apply verify) | Query the stack post-apply to confirm no SLO regression — Prometheus `histogram_quantile`, Datadog monitors, NRQL percentile queries |
| `/bugfix` (production-context bugs) | Pull traces (Honeycomb / Tempo / Jaeger / New Relic) and Sentry issues filtered to the offending release to localize the bug |

## Integration

- **Used by**: `/analyze-prod`, `/analyze-local`, `/env-analyze`, `/infra-change`, `/bugfix`
- **Companion knowledge**: `@observability-methods` (which signals to query for — Golden Signals / RED / USE / Tracing), `@cloud-platforms` (managed-service native metrics via cloud CLI), `@deployment-procedures` (post-deploy verification queries)
- **External references**:
  - Prometheus docs — PromQL reference and `prometheus-operator` CRDs
  - Datadog docs — APM, log search syntax, Watchdog
  - Honeycomb docs — Query Builder, BubbleUp, Triggers
  - New Relic docs — NRQL reference
  - Sentry docs — Issue grouping, Releases, Performance
  - OpenTelemetry specification; Tempo (Grafana Labs) and Jaeger (CNCF) documentation
