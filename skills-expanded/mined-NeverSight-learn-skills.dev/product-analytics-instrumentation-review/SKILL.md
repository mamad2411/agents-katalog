---
name: product-analytics-instrumentation-review
description: Design and audit product analytics instrumentation for events, properties, identity, sessions, funnels, cohorts, experiments, attribution, billing/support joins, privacy, consent, data quality, mobile/web/server tracking, dashboards, QA, release gates, and metric ownership. Use when teams need trustworthy behavior data before product decisions or launches.
---

# Product Analytics Instrumentation Review

Use this skill to convert product analytics instrumentation, event taxonomy, identity, funnel, privacy, QA, and metric-owner questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify decisions to support, user journey, platforms, event sources, identity model, consent/privacy constraints, downstream metrics, dashboards, experiments, and current data-quality failures.
2. Read `references/product-analytics-instrumentation-patterns.md`.
3. Classify tracking as client event, server event, billing/support join, experiment exposure, attribution touch, lifecycle event, error state, or derived metric input.
4. Define event contract, property schema, identity rules, consent gating, QA plan, dashboard owner, release gate, and drift monitoring.
5. Produce instrumentation plan, state machine, decision table, event schema, QA checklist, and rollout plan.

## Guardrails

- Do not instrument everything; track decision-relevant events with clear owners and retention/privacy constraints.
- Do not use client-only analytics for billing, compliance, entitlement, or critical operational truth.
- Do not ship events without property schema, identity behavior, consent handling, and QA fixtures.
- Do not let dashboards define metrics independently from the event/metrics source of truth.

## Output format

```text
Analytics context:
Audience / source of truth / risk boundary:

Instrumentation plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Event contracts, QA, privacy, and dashboard handoff:
- <trigger> -> <policy, metric, edge case, support note>
```
