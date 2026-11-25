---
name: bytedtrace-knowledge
description: Guide for BytedTrace (Trace 2.0) metrics, Go SDK usage, and framework integration. Use when the user needs to query QPS, latency, or throughput, find specific metric names, look up available tags for Server/Client/Event spans, initialize or use the BytedTrace Go SDK, add custom spans/events/metrics, or check which frameworks and storage components support BytedTrace.
user-invocable: false
---

# BytedTrace Metrics

## Metric Format

All Metrics 2.0 follow the 4-segment format:
`<tenant>.<component>.<family>.<suffix>`

- **Tenant**: Fixed as `bytedtrace`
- **Component**: Fixed as `sdk`
- **Family**: `span`, `event`, `custom`, or `internal`
- **Suffix**: The specific measurement (e.g., `rate`, `latency.us.pct99`)

## Common Query Patterns

### Server Side (Inbound)
Monitor calls received by a PSM.

- **QPS**: `bytedtrace.sdk.span.server.rate{_psm="your.psm"}`
- **Latency (P99)**: `bytedtrace.sdk.span.server.latency.us.pct99{_psm="your.psm"}`
- **Error Rate**: Filter by `_is_error="1"` or `_status_code`.

### Client Side (Outbound)
Monitor calls made by a PSM to downstream services.

- **QPS**: `bytedtrace.sdk.span.client.rate{_psm="your.psm", _to_service="downstream.psm"}`
- **Latency (P99)**: `bytedtrace.sdk.span.client.latency.us.pct99{_psm="your.psm", _to_service="downstream.psm"}`

### Events/Logs
- **Log Frequency**: `bytedtrace.sdk.event.log.rate{_psm="your.psm", _log_level="4"}` (Level 4=Warn, 5=Error)

## Detailed Reference

- **[metrics-schema.md](references/metrics-schema.md)**: Complete list of Tags, Metric Suffixes, and Pre-aggregation keys.
- **[sdk-usage.md](sdk-usage.md)**: Go SDK initialization, Tracer/Span/Event/Metrics API, pre-registration, span inheritance (in-process and cross-process), and sampling.
- **[framework-integration.md](framework-integration.md)**: Supported service frameworks (kitex, hertz, ginex, etc.), storage/cache/MQ components (MySQL, Redis, Kafka, etc.), FaaS, and CronJob integration.
