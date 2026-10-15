---
name: data-deletion-erasure-review
description: Design and audit data deletion and erasure workflows covering user/account deletion, DSAR/RTBF, retention schedules, backups, logs, analytics, billing records, legal holds, fraud/security exceptions, subprocessors, exports, audit proof, customer communication, and recovery limits. Use when personal or customer data must be removed safely and provably.
---

# Data Deletion Erasure Review

Use this skill to convert data deletion, erasure, DSAR, retention, backup, legal hold, subprocessor, and audit-proof questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify data subject, account/workspace scope, data classes, systems, retention/legal basis, backups/logs, subprocessors, billing/security exceptions, and customer communication need.
2. Read `references/data-deletion-erasure-patterns.md`.
3. Classify request as user self-delete, admin account deletion, workspace deletion, DSAR erasure, retention purge, legal hold, fraud/security exception, or subprocessor deletion.
4. Define deletion map, eligibility check, approval, execution order, tombstone/anonymization, backup handling, evidence, customer notice, and exception path.
5. Produce erasure plan, state machine, decision table, event schema, deletion checklist, and proof/communication plan.

## Guardrails

- Do not promise physical deletion from backups, logs, invoices, or legal records where policy requires retention or delayed purge.
- Do not delete data without checking account ownership, legal hold, fraud/security needs, billing/tax retention, and shared workspace impact.
- Do not leave derived analytics, search indexes, AI datasets, exports, or subprocessors outside the deletion map.
- Do not make deletion irreversible without clear warnings, recovery window, and authorization.

## Output format

```text
Erasure context:
Audience / source of truth / risk boundary:

Deletion operating plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Eligibility, execution, exceptions, and proof:
- <trigger> -> <policy, metric, edge case, support note>
```
