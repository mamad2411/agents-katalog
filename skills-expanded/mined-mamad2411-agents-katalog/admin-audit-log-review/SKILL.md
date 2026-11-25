---
name: admin-audit-log-review
description: Design and audit admin audit logs covering privileged actions, configuration changes, user/role management, billing/admin settings, data export/delete, API tokens, integrations, security events, retention, tamper evidence, customer access, filters, exports, SIEM, alerting, privacy, and enterprise evidence. Use when customers or operators need trustworthy administrative traceability.
---

# Admin Audit Log Review

Use this skill to convert admin audit log, privileged action, security evidence, retention, SIEM, and customer traceability questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify admins, privileged actions, enterprise requirements, data/security impact, retention needs, customer visibility, SIEM/export needs, and current logging gaps.
2. Read `references/admin-audit-log-patterns.md`.
3. Classify events as identity/admin, role/permission, billing, security, integration/API token, data export/delete, configuration, policy, support access, or system-generated change.
4. Define event contract, actor/target/context, retention, integrity controls, customer UI, export/API, alerting, privacy redaction, and support/audit workflow.
5. Produce audit-log design, state machine, decision table, event schema, coverage checklist, and rollout/backfill plan.

## Guardrails

- Do not log secrets, raw sensitive content, tokens, or unnecessary PII in audit logs.
- Do not let admins alter or delete audit evidence without separate tamper-evident controls.
- Do not claim audit-log coverage unless critical privileged actions are actually emitted and queryable.
- Do not make audit logs unusable for customers by omitting actor, target, timestamp, result, source, and correlation context.

## Output format

```text
Audit log context:
Audience / source of truth / risk boundary:

Admin audit-log plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Event coverage, retention, customer access, and alerts:
- <trigger> -> <policy, metric, edge case, support note>
```
