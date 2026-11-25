---
name: observability-setup
description: Adds metrics, traces and structured logs to a service, then builds the alerts and dashboards you need to find a problem within minutes.
---

# Observability setup

Instrument to answer incident questions, not to collect everything.

## Steps

1. Read the service entry points, dependencies (databases, HTTP clients, queues) and any existing logging or metrics code.
2. Metrics: record the RED set for each endpoint or consumer: request rate, error rate and a duration histogram. Add saturation signals such as queue depth, pool usage and memory. Allowed labels: route template, method, status class. Never label by user ID, URL with IDs, or error message.
3. Traces: add OpenTelemetry auto-instrumentation, then manual spans around business operations. Propagate the W3C `traceparent` header on outgoing calls. Sample sensibly: keep errors and slow traces.
4. Logs: emit one JSON object per line with `timestamp`, `level`, `service`, `trace_id`, `span_id` and a stable `event` name. Log decisions and failures, not every function call. Redact tokens, passwords and personal data.
5. Alerts: alert on symptoms users feel (error ratio, latency percentile, no traffic), with a runbook link and an owner. Do not alert on CPU alone.
6. Dashboards: one overview with rate, errors and latency on top, dependencies below. Use the same time range on every panel.
7. Verify locally: run the service, send a request, and confirm the span, metric and log line appear with the same trace ID.

## Rules

- Never send telemetry to an endpoint the user did not name.
- Never add high-cardinality labels.

## Report

What is instrumented, metric names, alert rules with thresholds, and how to see a request end to end.
