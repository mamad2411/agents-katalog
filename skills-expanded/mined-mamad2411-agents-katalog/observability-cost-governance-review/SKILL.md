---
name: observability-cost-governance-review
description: Design and audit observability cost governance across logs, metrics, traces, events, profiling, session replay, analytics, retention, sampling, cardinality, dashboards, alerting, ownership, privacy redaction, budgets, and incident usefulness. Use when telemetry spend grows or observability needs to stay useful, safe, and cost-efficient.
---

# Observability Cost Governance Review

Use this skill to convert a observability cost governance, logs, metrics, traces, sampling, retention, cardinality, privacy, budgets, and incident usefulness question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify telemetry sources, owners, incident needs, cost drivers, retention requirements, sensitive fields, cardinality, and budget constraints.
2. Read `references/observability-cost-governance-patterns.md`.
3. Classify telemetry as critical signal, debugging detail, audit log, product analytics, security event, performance profile, or low-value noise.
4. Define sampling, retention, aggregation, redaction, ownership, budgets, dashboard/alert policy, cost allocation, and deletion/exception rules.
5. Produce observability governance plan, state machine, decision table, event schema, checklist, and cost-review cadence.

## Guardrails

- Do not cut telemetry that is required for incident response, security audit, billing reconciliation, or customer support without replacement.
- Do not reduce cost by dropping trace correlation, redaction, or critical SLO signals.
- Do not allow unbounded high-cardinality labels or raw payload logs.
- Do not keep expensive debug logs, session replay, or traces forever without owner and retention reason.

## Output format

```text
Observability context:
Signal / owner / cost driver / incident need:

Observability cost plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Signals, retention, and budgets:
- <item> -> <policy, metric, edge case, support note>

Exception and cost-review policy:
- <trigger> -> <action, communication, owner>
```
