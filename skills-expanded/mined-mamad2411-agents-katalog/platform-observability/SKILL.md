---
name: platform-observability
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: platform observability design, unified observability stack, trace correlation platform, log aggregation architecture, metrics cardinality management, observability platform, telemetry pipeline, distributed tracing platform, observability cost, observability data model, observability self-service, alert routing platform
compose: observability-stack
---

# Skill — Platform Observability

## When this skill activates

This skill activates when the user is designing or implementing platform observability capabilities. This includes unified observability stacks, trace correlation, log aggregation architecture, metrics cardinality management, telemetry pipelines, distributed tracing platforms, observability cost optimization, observability data models, self-service observability, and alert routing platforms.

## Mandatory actions when this skill is active

### Before writing any code

1. Audit current observability tooling: metrics (Prometheus, Datadog), logs (Elasticsearch, Splunk), traces (Jaeger, Honeycomb). Identify gaps and redundancies.
2. Assess observability cost: cost per service, cost per metric, cost per log line, cost per trace. Identify high-cardinality metrics and expensive log patterns.
3. Define observability requirements per service tier: critical services need full traces, non-critical services need sampled traces.
4. Map existing alert sprawl: how many alerts fire per week, what percentage are actionable. Target: reduce noise by 70-90%.
5. Establish observability SLOs: query latency (p95 < 3 seconds), data freshness (under 30 seconds), retention (metrics 30 days, logs 7 days, traces 7 days).

### During implementation

- **Unified Observability Stack:** Use OpenTelemetry for instrumentation (vendor-neutral). Collect metrics, logs, and traces via single SDK. Export to backend(s) of choice (Prometheus, Loki, Tempo). Avoids vendor lock-in.
- **Trace Correlation:** Link traces, logs, and metrics via trace ID. Every log line should include trace ID and span ID. Enables root-cause analysis by jumping from metric spike → trace → logs.
- **Log Aggregation Architecture:** Centralized log storage (Elasticsearch, Loki, CloudWatch). Use structured logging (JSON) with consistent schema. Index on: service, environment, level, trace_id. Retain logs for 7-30 days (compliance may require longer).
- **Metrics Cardinality Management:** High-cardinality labels (user_id, request_id) explode metric storage cost. Use exemplars (link to trace) instead. Limit labels to: service, environment, region, status_code. Target: under 10,000 time series per service.
- **Telemetry Pipeline:** Decouple collection from storage. Use OpenTelemetry Collector as aggregation layer. Enables: sampling, filtering, enrichment, multi-backend export. Pipeline should handle 100k+ events/second.
- **Distributed Tracing:** Instrument all services with OpenTelemetry. Use head-based sampling (sample 1-10% of traces) or tail-based sampling (sample slow/error traces at 100%, fast traces at 1%). Traces should include: service name, operation, duration, status, attributes (http.method, db.statement).
- **Observability Cost Optimization:** Sample aggressively (1-10% for most services). Drop high-volume, low-value logs (health checks, debug logs in prod). Use tiered storage (hot: 7 days, warm: 30 days, cold: 90 days). Target: observability cost under 5% of infrastructure cost.
- **Observability Data Model:** Use semantic conventions (OpenTelemetry) for consistent attribute naming. Define standard labels: service.name, deployment.environment, service.version. Enables cross-service queries and dashboards.
- **Self-Service Observability:** Developers provision dashboards and alerts via IaC (Terraform, Jsonnet). Pre-built dashboard templates for common patterns (RED, USE, Golden Signals). Query language accessible to non-SREs (LogQL, PromQL with examples).
- **Alert Routing:** Route alerts to appropriate team via PagerDuty, Opsgenie, or Slack. Use severity levels: SEV1 (page), SEV2 (urgent Slack), SEV3 (non-urgent Slack). Alerts should include: runbook link, suggested queries, recent changes.

### After implementation

- Verify all services emit metrics, logs, and traces via OpenTelemetry.
- Confirm trace IDs are propagated and linked across logs, metrics, and traces.
- Validate metrics cardinality is under 10,000 time series per service.
- Ensure telemetry pipeline handles 100k+ events/second with sampling and filtering.
- Check that observability cost is under 5% of infrastructure cost.

## Self-check before task completion

- [ ] Unified observability stack uses OpenTelemetry for vendor-neutral instrumentation.
- [ ] Trace correlation links metrics, logs, and traces via trace ID and span ID.
- [ ] Log aggregation uses structured logging (JSON) with consistent schema.
- [ ] Metrics cardinality is managed: under 10,000 time series per service.
- [ ] Telemetry pipeline decouples collection from storage and handles 100k+ events/second.
- [ ] Distributed tracing uses sampling (head or tail-based) to control costs.
- [ ] Observability cost is under 5% of infrastructure cost via sampling and tiered storage.
- [ ] Observability data model uses OpenTelemetry semantic conventions.
- [ ] Self-service observability enables developers to provision dashboards and alerts via IaC.
- [ ] Alert routing uses severity levels and includes runbook links.
