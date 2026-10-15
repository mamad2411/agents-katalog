---
name: enterprise-onboarding-implementation-review
description: Plan and audit enterprise onboarding and implementation programs covering kickoff, success criteria, stakeholder mapping, SSO/SCIM, integrations, data migration, sandboxing, training, go-live gates, risk escalation, support handoff, and adoption proof. Use when a sold customer must become live and successful without heroic project management.
---

# Enterprise Onboarding Implementation Review

Use this skill to convert enterprise onboarding, implementation, integration, migration, training, and go-live questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify buyer segment, contract promise, use case, launch deadline, stakeholders, technical dependencies, security constraints, data/integration scope, and success criteria.
2. Read `references/enterprise-onboarding-implementation-patterns.md`.
3. Classify implementation as self-serve assisted, guided onboarding, technical implementation, migration project, regulated rollout, or multi-team change program.
4. Define kickoff agenda, RACI, milestone plan, dependency register, go-live checklist, escalation path, training plan, and post-launch adoption handoff.
5. Produce implementation plan, state machine, decision table, event schema, readiness checklist, and customer/internal comms cadence.

## Guardrails

- Do not start implementation without clear success criteria, owner roles, timeline, and customer decision path.
- Do not treat SSO, data migration, integrations, security review, and training as generic onboarding tasks.
- Do not declare go-live from configuration alone; require user workflow validation and support readiness.
- Do not hide blocked dependencies until the renewal or executive review.

## Output format

```text
Implementation context:
Audience / source of truth / risk boundary:

Onboarding implementation plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Milestones, dependencies, and go-live readiness:
- <trigger> -> <policy, metric, edge case, support note>
```
