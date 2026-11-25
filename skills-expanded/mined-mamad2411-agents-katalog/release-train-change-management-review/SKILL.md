---
name: release-train-change-management-review
description: Design and audit release trains, change management, release calendars, risk classification, freeze windows, release notes, staged rollout, owner approvals, dependency readiness, rollback, support/comms, incident handoff, and post-release review. Use when shipping many product changes across apps, SaaS, games, APIs, desktop, or platform surfaces.
---

# Release Train Change Management Review

Use this skill to convert a release trains, change calendars, risk classification, rollout gates, rollback, comms, and support readiness question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify release scope, cadence, owners, dependency graph, affected surfaces, risk class, customer visibility, and rollback mechanism.
2. Read `references/release-train-change-management-patterns.md`.
3. Classify each change as routine, experiment, migration, billing/auth/security, API contract, infra, content/event, or emergency fix.
4. Define calendar, freeze rules, readiness gates, rollout stages, comms, support brief, monitoring, rollback, and post-release review.
5. Produce release train plan, state machine, decision table, event schema, checklist, and exception policy.

## Guardrails

- Do not put billing, auth, migration, or public API changes on an ordinary release train without special gates.
- Do not let release notes become the only support readiness artifact.
- Do not continue a rollout after guardrails fail because the calendar says ship.
- Do not rely on one human memory thread for cross-team release dependencies.

## Output format

```text
Release context:
Scope / cadence / risk class / rollback path:

Release train plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Changes and gates:
- <item> -> <policy, metric, edge case, support note>

Exception and rollback policy:
- <trigger> -> <action, communication, owner>
```
