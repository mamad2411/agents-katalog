---
name: observability
description: Structured logs, tracing, correlation IDs, metrics, event provenance, actionable errors, secrets redaction
---
# System Observability

## 1. Structured Logging
Emit all logs in a structured format (e.g., JSON). This allows log aggregation systems to parse, index, and query logs effectively. Never use unstructured string concatenation for log messages that contain variable data.

## 2. Distributed Tracing
Implement distributed tracing (e.g., OpenTelemetry) to track requests as they flow through multiple microservices. Propagate trace context (Trace ID, Span ID) across all process and network boundaries.

## 3. Correlation IDs
Assign a unique Correlation ID to every incoming external request. Inject this ID into all log messages, downstream API calls, and database queries associated with that request. This is essential for debugging complex workflows.

## 4. RED/USE Metrics
Instrument applications using standard metric frameworks. Use the RED method (Rate, Errors, Duration) for services and the USE method (Utilization, Saturation, Errors) for resources. Expose metrics via standard endpoints (e.g., Prometheus).

## 5. Event Provenance
For critical business events, log full provenance: who initiated it, what the exact input was, when it occurred, and what the outcome was. This provides an indisputable audit trail for security and business analysis.

## 6. Actionable Alerts
Alerts must be actionable. Do not page on symptoms that self-resolve or background noise. Page only when user-facing Service Level Objectives (SLOs) are threatened. Every alert must link to a runbook or standard operating procedure.

## 7. Secrets Redaction
Implement strict, automated secrets redaction in the logging and tracing pipelines. Never log passwords, API keys, PII (Personally Identifiable Information), or credit card numbers. Use allow-listing for log fields rather than block-listing.

## 8. Health Probes
Provide dedicated readiness and liveness probes. Readiness probes indicate if the app can handle traffic (e.g., DB connected). Liveness probes indicate if the app is hopelessly stuck and needs a restart. Do not couple them tightly.

## 9. Log Levels
Use log levels semantically. ERROR requires immediate human intervention. WARN indicates anomalous behavior that isn't immediately fatal. INFO tracks high-level lifecycle events. DEBUG provides granular detail for local development only.

## 10. Cardinality Management
Be mindful of metric cardinality. Do not use unbounded values (like user IDs or raw URLs) as metric labels/tags. High cardinality will overwhelm the metrics backend, causing it to crash or drop data. Group dynamic values into bounded buckets.

