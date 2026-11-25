---
name: infra-observability
description: "Design logs, metrics, traces, dashboards, alerts, SLOs, and cardinality controls."
---

# Infra Observability

Review whether failures are visible, actionable, correlated, and low-cardinality enough for production use.

## Process

1. Map the request path or operational path end to end.
2. Check rollout, rollback, observability, security, secrets, resource limits, and failure behavior.
3. For review, report concrete production risks first, then maintainability issues.
4. For debugging, collect evidence from config, allocation/container state, logs, metrics, and recent changes before proposing fixes.

## Evidence

Prefer job specs, Dockerfiles, proxy config, deployment manifests, logs, metrics, health checks, and runbook steps over assumptions.

## Focused References

- [01-runtime-observability.md](./references/01-runtime-observability.md) - Runtime Observability
- [02-metrics-logs-alerting-review.md](./references/02-metrics-logs-alerting-review.md) - Metrics Logs Alerting And Review
