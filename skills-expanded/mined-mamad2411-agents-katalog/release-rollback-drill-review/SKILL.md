---
name: release-rollback-drill-review
description: Design and audit release rollback drills for web, mobile, desktop, backend, database, configuration, feature flags, migrations, third-party dependencies, app stores, customer communication, monitoring, incident roles, and recovery proof. Use when teams need to prove rollback works before a risky release or recurring launch cadence.
---

# Release Rollback Drill Review

Use this skill to convert release rollback drill, rollback rehearsal, deployment recovery, migration rollback, feature flag kill switch, app-store rollback, and incident-readiness questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify release surface, rollback mechanism, irreversible steps, stateful data, dependencies, monitoring, trigger threshold, owners, communication path, and proof artifact.
2. Read `references/release-rollback-drill-patterns.md`.
3. Classify the situation as code rollback, config rollback, feature-flag kill switch, database migration rollback, mobile/store rollback, desktop updater rollback, dependency rollback, or customer communication drill.
4. Define drill scenario, preconditions, execution steps, success criteria, time target, monitoring, customer impact, owner roles, and lessons learned.
5. Produce rollback drill plan, state machine, decision table, event schema, readiness checklist, runbook diff, and evidence package.

## Guardrails

- Do not assume rollback works for databases, mobile apps, desktop clients, queues, caches, or third-party state without rehearsal.
- Do not run drills that mutate production or customer data unless the environment and approval path explicitly allow it.
- Do not call rollback successful without user-visible behavior and monitoring recovery proof.
- Do not leave rollback lessons in chat instead of updating runbooks, flags, alerts, and release gates.

## Output format

```text
Rollback drill context:
Audience / source of truth / risk boundary:

Rollback drill plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Scenario, trigger, roles, steps, proof, communication, and lessons:
- <trigger> -> <policy, metric, edge case, support note>
```
