---
name: datadog-apm
description: Datadog APM standards — tracing, custom spans, logs correlation, metrics, and error tracking. Load when working with Datadog.
user-invocable: false
stack: error-monitoring/datadog-apm
paths:
  - "**/datadog*"
  - "**/dd-trace*"
  - "datadog.yaml"
---

Full standards in [datadog-apm.md](datadog-apm.md). Always-on summary:

**Tracer setup:**
- `const tracer = require('dd-trace'); tracer.init({ logInjection: true })` as the **very first lines** of your entry file — before any other imports
- Configure via environment variables (`DD_SERVICE`, `DD_ENV`, `DD_VERSION`) — not code
- `logInjection: true` auto-injects `trace_id` and `span_id` into log lines for correlation

**Custom spans:**
- Use `tracer.startSpan()` for operations not auto-instrumented (business logic, DB calls to non-supported clients)
- Always set `span.setTag(ERROR_TAG, error)` and `span.finish()` in the catch block — or spans leak
- Use `tracer.scope().active()` to get the current span without passing it explicitly

**Logs correlation:**
- Use structured logging (JSON) — Datadog correlates logs with traces via `dd.trace_id` and `dd.span_id`
- Never concatenate trace IDs into log strings — use the auto-injected fields from `logInjection: true`

**Metrics:**
- Use `StatsD` (DogStatsD) for custom metrics: counters, gauges, histograms
- Tag metrics with `env`, `service`, `version` — consistent with your tracer tags

**Never:**
- Import `dd-trace` after other modules — it patches modules at import time
- Catch errors without finishing the span — spans that never finish skew latency metrics
- Log PII in span tags or log lines sent to Datadog

**Related skills:** `logging/provider/datadog` (log forwarding), `core/error-handling`
