---
name: release-freeze-change-control-review
description: Design and audit release freeze change control for holiday freezes, enterprise blackout windows, app-store deadlines, incident recovery, compliance windows, infrastructure freezes, and critical hotfixes covering change intake, severity, approval authority, customer scope, rollback, monitoring, communication, exception expiry, and post-freeze review. Use when teams must control changes during frozen release windows.
---

# Release Freeze Change Control Review

Use this skill to convert release freeze, change control, blackout window, holiday freeze, critical hotfix, compliance freeze, app-store deadline, customer blackout, infrastructure freeze, and freeze exception questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify freeze window, protected systems, change request, severity, customer impact, risk tier, approval authority, evidence, rollback plan, monitoring signals, communication plan, and expiry/review owner.
2. Read `references/release-freeze-change-control-patterns.md`.
3. Classify the situation as planned freeze, emergency hotfix, security patch, store deadline exception, customer-specific blackout, infrastructure freeze, incident-recovery change, or compliance freeze override.
4. Define freeze policy, intake fields, severity ladder, approval matrix, permitted changes, evidence requirements, rollout/rollback guardrails, comms, monitoring, exception register, and post-freeze review.
5. Produce release freeze change-control review, state machine, decision table, event schema, freeze checklist, exception register, and post-freeze learning plan.

## Guardrails

- Do not treat a freeze as a slogan; define protected systems, allowed changes, approvers, and evidence.
- Do not let emergency hotfix urgency bypass rollback, monitoring, support readiness, and customer communication.
- Do not approve freeze exceptions without expiry and post-change review.
- Do not use freeze policy to block security, compliance, or incident fixes that have controlled evidence and authority.

## Output format

```text
Release freeze context:
Audience / source of truth / risk boundary:

Freeze change-control plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Freeze scope, change severity, approvals, rollout/rollback, monitoring, communication, and exception retirement:
- <trigger> -> <policy, metric, edge case, support note>
```
