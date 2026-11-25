---
name: monitor-telemetry-setup
description: 'Design, configure or diagnose telemetry delivery, structured logging (Fluent Bit), storage and dashboards from observable runtime evidence. Use for missing logs, metrics or dashboards. RU: логи, мониторинг, дашборд, сбор логов.'
disable-model-invocation: true
---

# Telemetry, logging and dashboards

Identify the question, scope, source, telemetry type, available interfaces, audience and permitted observations. Trace the actual boundary from instrumentation through transport, collection, storage, query and display. A configured exporter, accepted transport response, indexed record, query result and rendered dashboard are distinct facts. Isolate the first unverified or failing boundary before changing a live system; use the superpowers `systematic-debugging` skill for the underlying failure investigation.

Define units, timestamp, identity, aggregation, freshness and missing/unknown semantics for the actual data contract. Preserve privacy through a bounded field policy, appropriate retention and redaction at the final output; do not expose credentials or raw payloads in examples or diagnostics. Never treat missing data, a failed query or a display gap as a measured zero.

Validate using existing data or appropriately scoped, authorized synthetic events and read back the stored result where delivery proof is required. Separate test-only fixtures from real workload and live acceptance. Source changes, collector activation, dashboard publication, alert routing and notifications need their own authorization and the supported runtime interface.

## Structured logging and Fluent Bit

Inspect the project's existing logging contract, selected collectors, deployment configuration and authorized destinations first; use its documented integration interface and assume no package, vendor, host or log backend. Preserve existing fields, severity semantics, retention and access controls unless the task authorizes changing them. Emit structured records where the project supports them with stable fields; keep credentials, session material and unnecessary personal data out, and check URLs, exceptions, HTTP traces and request bodies for inadvertent secrets. Treat high-cardinality fields according to the actual storage and indexing design. Take the sink-unavailable behavior (best-effort or fail-closed) from the project's reliability and audit requirements; do not impose one. Verify the pipeline end to end with an authorized synthetic marker (application emission, collector routing, searchable destination) and report which boundary was observed: local output alone does not prove delivery. Container driver or collector changes can require service recreation, so identify the maintenance and recovery procedure first.

References: [telemetry evidence](references/telemetry-evidence.md) for delivery and aggregation pitfalls, [dashboard operations](references/dashboard-operations.md) for dashboard design and readback, [audit trail boundaries](references/audit-trail-boundaries.md) for an explicitly requested persisted audit trail. The Fluent Bit [integration](references/logging-integration.md), historical [logging rules](references/logging-rules.md) and [Python example](references/logging-python.md) are project-specific examples, not universal policy: verify their assumptions against the selected versions and add no dependency or deployment step without authorization and evidence it fits.
