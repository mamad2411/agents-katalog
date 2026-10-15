---
name: customer-onboarding-migration-runbook-review
description: Design and audit customer onboarding migration runbooks covering source assessment, data mapping, validation, sandbox rehearsals, cutover, rollback, downtime, customer communications, roles, permissions, integrations, training, support readiness, success criteria, and post-migration adoption. Use when customers must move from old tools or legacy data into a product safely.
---

# Customer Onboarding Migration Runbook Review

Use this skill to convert customer onboarding migration, data mapping, cutover, validation, rollback, training, and support-readiness questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify customer source system, data types, migration scope, success criteria, timeline, stakeholders, integrations, permissions, downtime tolerance, and support/training needs.
2. Read `references/customer-onboarding-migration-runbook-patterns.md`.
3. Classify migration as self-serve import, assisted import, enterprise data migration, phased cutover, integration migration, historical backfill, or high-risk regulated migration.
4. Define source assessment, mapping, dry run, validation, customer signoff, cutover, rollback, communication, training, support coverage, and adoption handoff.
5. Produce migration runbook, state machine, decision table, event schema, readiness checklist, and post-migration review.

## Guardrails

- Do not migrate customer data without mapping, sample validation, owner signoff, rollback/retry plan, and support visibility.
- Do not hide data loss, unsupported fields, permission differences, integration gaps, or downtime assumptions.
- Do not declare migration success from job completion alone; validate customer workflows and adoption outcomes.
- Do not let one-off migration scripts become unowned operational risk.

## Output format

```text
Migration context:
Audience / source of truth / risk boundary:

Onboarding migration runbook:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Validation, cutover, rollback, support, and adoption:
- <trigger> -> <policy, metric, edge case, support note>
```
