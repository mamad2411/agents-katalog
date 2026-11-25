---
name: helixora-observability
description: "Improve observability for Helixora AI across logs, metrics, traces, audit events, reliability signals, and operational diagnostics. Use for production readiness, debugging workflows, health monitoring, AI pipeline tracing, incident investigation, and SRE-oriented instrumentation."
user-invocable: true
---

# Helixora Observability

## When to Use

- Add or improve logging, metrics, and tracing
- Design health checks and operational dashboards
- Diagnose failures in AI, API, or data workflows
- Add audit trails for medical recommendation generation and review
- Improve incident response and production support readiness
- Instrument latency, quality, and reliability signals

## Observability Priorities

- request tracing across services
- structured logging with correlation IDs
- metrics for latency, throughput, failures, retries, and saturation
- audit events for recommendation generation, approval, and access
- alerts for degraded performance or unsafe failure patterns
- operational visibility into model calls and external integrations

## Procedure

1. Identify critical user journeys and background workflows.
2. Define what must be logged, measured, traced, and audited.
3. Add structured events with stable field names.
4. Separate diagnostic logs from compliance/audit logs.
5. Avoid logging raw sensitive patient data unless explicitly required and protected.
6. Instrument error paths and timeout boundaries.
7. Define service-level indicators and alert thresholds.
8. Recommend dashboards and runbook-oriented signals.

## Helixora-Specific Signals

- treatment recommendation generation success/failure
- explanation generation latency and quality issues
- clinician review turnaround time
- data-ingestion failures for genomic or clinical records
- model fallback events
- prompt/response safety interventions
- patient-record access audit trails

## Deliverables

- instrumentation plan
- metrics and log schema suggestions
- trace propagation recommendations
- alert ideas
- gaps in incident diagnosability

## Best Practices

- use structured logs, not ad hoc strings
- prefer correlation IDs end-to-end
- instrument before optimizing
- make audit events immutable and easy to query
- separate business events from noisy debug logs
