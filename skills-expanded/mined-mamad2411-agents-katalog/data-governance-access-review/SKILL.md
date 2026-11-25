---
name: data-governance-access-review
description: Design and audit data governance, data classification, access controls, least privilege, approval workflows, owner review, retention, deletion, audit logs, data catalog, sensitive fields, analytics access, support/admin access, AI dataset access, and break-glass paths. Use when teams need product data access without privacy, security, or compliance drift.
---

# Data Governance Access Review

Use this skill to convert a data governance, classification, access controls, least privilege, approvals, retention, audit logs, and break-glass policy question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify data domains, sensitive fields, actors, access purpose, retention requirements, owner teams, tooling, and audit expectations.
2. Read `references/data-governance-access-patterns.md`.
3. Classify data by sensitivity, residency, source, purpose, retention, customer visibility, and allowed access roles.
4. Define access request workflow, approval policy, least privilege, expiration, review cadence, audit log, break-glass, and offboarding.
5. Produce governance plan, state machine, decision table, event schema, access checklist, and exception review policy.

## Guardrails

- Do not grant permanent broad production data access for convenience.
- Do not let analytics, support, AI, or sales tooling copy sensitive data without purpose, minimization, retention, and owner approval.
- Do not run break-glass without incident/ticket reason, expiry, audit, and post-review.
- Do not treat data governance as complete if offboarding and stale access reviews are missing.

## Output format

```text
Data governance context:
Data class / actor / purpose / retention:

Data access governance plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Roles, approvals, and audits:
- <item> -> <policy, metric, edge case, support note>

Exception and break-glass policy:
- <trigger> -> <action, communication, owner>
```
