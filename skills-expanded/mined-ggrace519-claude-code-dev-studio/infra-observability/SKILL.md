---
name: infra-observability
description: Observability specialist. Owns metrics / logs / traces, instrumentation, retention, cardinality control, and dashboards. Auto-invoked when instrumenting services, investigating perf, or building dashboards.
---

# Observability

You can't fix what you can't see — but high-cardinality metrics and chatty logs
will bankrupt you before they enlighten you. Signal over volume.

## When to reach for this

- Instrumenting a new service or filling gaps in an existing one
- A cardinality or log-volume bill spike that needs attribution and a budget
- Building dashboards for on-call, service owners, or execs
- Choosing sampling/retention policies per signal type

## Principles

1. **Standardize on OpenTelemetry.** OTel SDKs + Collector, vendor backends
   behind an exporter swap. Vendor-specific SDKs are a future migration tax paid
   with interest; the Collector also gives you one place for scrubbing,
   sampling, and routing.
2. **Cardinality is cost.** Series count is the *product* of label
   cardinalities — one `user_id` or `request_id` label turns a 10-series metric
   into millions. Bounded labels only (status class, route template, region);
   high-cardinality questions belong in traces or logs, not metrics.
3. **Structure logs from day one.** JSON, stable key names, severity, and a
   correlation/trace ID on every line. Sample the INFO firehose (keep 100% of
   WARN+); scrub PII at the collector, before it lands anywhere retained.
4. **Trace the critical path with intelligent sampling.** Head-sample a small
   percentage (1–10% is a common start) for the baseline; tail-sample to keep
   100% of errors and slow outliers. Propagate W3C `traceparent` everywhere or
   traces fragment at the first queue or gateway.
5. **Retention is tiered, not uniform.** Hot/queryable short (logs ~14–30 days),
   then cheap archive; metrics downsampled as they age (raw → 5m rollups);
   traces shortest. Default-forever retention is how observability becomes a
   top-3 line item.
6. **Dashboards per persona.** On-call needs golden signals (latency, traffic,
   errors, saturation) and "what changed"; service owners need
   capacity/dependency views; execs need SLO attainment. One dashboard for all
   three serves none.

## Per-signal defaults

| Signal | Instrument | Control knob | Starting point |
|---|---|---|---|
| Metrics | OTel/Prometheus, RED + USE | label allowlist, series limit per service | bounded labels only; alert on series-count growth |
| Logs | structured JSON + trace ID | sampling + level | 100% WARN+, sample INFO; 14–30 d hot, archive after |
| Traces | OTel SDK + Collector | head + tail sampling | 1–10% head; tail-keep errors and p99-slow |
| Dashboards | golden signals first | per persona | on-call board ≤ ~10 panels, each answering one question |

## Pitfalls

- `user_id`/`session_id`/raw URL path as a metric label — the canonical
  cardinality explosion (use route templates)
- Averages on dashboards hiding tail pain — graph p50/p95/p99, never mean
  latency alone
- Trace context dropped at queue/webhook boundaries, leaving disconnected
  fragments nobody can follow
- Logging full request/response bodies "temporarily" — cost plus a PII
  retention liability
- Instrumenting everything except the rollout: deploy markers/versions absent
  from dashboards, so "what changed at 14:02" takes an hour to answer
- Per-team logging formats that make cross-service correlation a regex project

---
*Related: `infra-sre` (SLOs and burn-rate alerting consume these signals),
`infra-finops` (cardinality and retention cost), `infra-k8s` (cluster and
workload metrics), `infra-networking` (flow logs) · domain agent:
`infra-architect` · output/ADR format: `playbook-conventions`*
