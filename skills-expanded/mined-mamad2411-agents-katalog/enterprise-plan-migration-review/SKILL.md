---
name: enterprise-plan-migration-review
description: Design and audit enterprise plan migrations across legacy plans, grandfathering, entitlements, feature gates, seats, usage caps, discounts, contracts, invoices, revenue recognition, migration cohorts, customer communication, support readiness, rollback, and renewal impact. Use when moving customers between plans or packaging without breaking trust, access, or revenue.
---

# Enterprise Plan Migration Review

Use this skill to convert enterprise plan migration, packaging transition, entitlement change, grandfathering, and customer communication questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify current plan, target plan, customer cohort, contract terms, entitlement deltas, billing system, feature gates, discounts, migration deadline, support owner, and rollback constraints.
2. Read `references/enterprise-plan-migration-patterns.md`.
3. Classify the situation as self-serve plan move, assisted migration, forced sunset, grandfathered exception, enterprise amendment, billing-system migration, entitlement cleanup, or renewal-time transition.
4. Define eligibility, customer notice, entitlement mapping, invoice impact, discount handling, success metrics, exception approval, support macros, rollback, and post-migration audit.
5. Produce plan migration brief, state machine, decision table, entitlement mapping checklist, event schema, customer-communication plan, and exception register.

## Guardrails

- Do not migrate plans without entitlement parity review, billing proof, customer-visible communication, and support readiness.
- Do not hide lost features, price increases, discount changes, usage-cap changes, or contract amendments inside a background migration.
- Do not rely on spreadsheet truth for migrated entitlements or grandfathered exceptions.
- Do not call the migration done until access, invoice, revenue, support, and renewal records agree.

## Output format

```text
Plan migration context:
Audience / source of truth / risk boundary:

Enterprise plan migration plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Cohorts, entitlements, billing, exceptions, and rollback:
- <trigger> -> <policy, metric, edge case, support note>
```
