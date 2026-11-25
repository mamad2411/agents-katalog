---
name: revops-crm-governance-review
description: Design and audit Revenue Operations CRM governance covering account/contact/opportunity objects, lifecycle stages, source attribution, owner routing, required fields, forecast hygiene, pipeline stages, handoffs, duplicate management, integrations, permissions, automation, reporting, data quality, and change control. Use when revenue teams need one trustworthy operating system instead of spreadsheet truth.
---

# RevOps CRM Governance Review

Use this skill to convert RevOps CRM governance, lifecycle stage, routing, forecast, attribution, owner, and data-quality questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify CRM objects, revenue motion, lifecycle stages, owner teams, integrations, reporting dependencies, forecast process, current data-quality issues, and governance owner.
2. Read `references/revops-crm-governance-patterns.md`.
3. Classify work as lifecycle design, routing, required-field policy, pipeline stage hygiene, attribution, duplicate cleanup, integration change, permission review, or reporting governance.
4. Define object ownership, field definitions, stage exit criteria, automation rules, change approval, data-quality checks, and reporting contracts.
5. Produce CRM governance plan, state machine, decision table, event schema, data-quality checklist, and rollout/backfill plan.

## Guardrails

- Do not let reports, automations, routing, and compensation depend on undefined or manually inconsistent fields.
- Do not change CRM stages, attribution, or ownership without migration, training, and downstream-report impact review.
- Do not make reps do low-value admin work when automation or simpler stage design can preserve data quality.
- Do not treat CRM as finance truth, product usage truth, or support truth without reconciliation boundaries.

## Output format

```text
CRM governance context:
Audience / source of truth / risk boundary:

Revenue operations plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Lifecycle, fields, automation, and data-quality controls:
- <trigger> -> <policy, metric, edge case, support note>
```
