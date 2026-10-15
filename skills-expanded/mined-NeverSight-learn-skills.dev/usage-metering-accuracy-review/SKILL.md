---
name: usage-metering-accuracy-review
description: Design and audit usage-metering accuracy for usage-based pricing, credits, quotas, overages, AI/token billing, API calls, seats, storage, event ingestion, idempotency, late events, aggregation, reconciliation, invoices, customer visibility, disputes, corrections, and revenue leakage. Use when billable usage must be trusted by customers and finance.
---

# Usage Metering Accuracy Review

Use this skill to convert usage-metering, billing accuracy, quota, credit, overage, invoice, and reconciliation questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify billable units, source events, customer identifiers, plan rules, credit/commit logic, quota windows, aggregation grain, invoice timing, dispute process, and current accuracy risks.
2. Read `references/usage-metering-accuracy-patterns.md`.
3. Classify metering as raw event, derived usage, rating, quota check, invoice line, credit deduction, correction, dispute, or customer-visible estimate.
4. Define source-of-truth events, idempotency, dedupe, late-event policy, reconciliation, customer transparency, alerts, correction workflow, and audit trail.
5. Produce metering accuracy plan, state machine, decision table, event schema, control checklist, and dispute/recovery path.

## Guardrails

- Do not invoice usage that cannot be traced from customer-visible billable event to rated invoice line.
- Do not silently correct usage without audit trail, customer impact assessment, and finance/support notification.
- Do not mix quota enforcement, billing estimates, and final invoice truth without labeling freshness and accuracy.
- Do not launch usage-based pricing without dispute handling and metering backfill/replay controls.

## Output format

```text
Metering context:
Audience / source of truth / risk boundary:

Metering accuracy plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Reconciliation, correction, and dispute handling:
- <trigger> -> <policy, metric, edge case, support note>
```
