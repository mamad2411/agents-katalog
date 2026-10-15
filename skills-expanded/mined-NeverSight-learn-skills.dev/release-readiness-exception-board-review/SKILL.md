---
name: release-readiness-exception-board-review
description: Design and audit release readiness exception boards covering unmet launch gates, risk acceptance, customer scope, mitigation owners, feature flags, rollback triggers, monitoring, support readiness, communication, approval authority, expiry, and post-release review. Use when a release is not fully ready and teams need a controlled exception instead of hidden risk.
---

# Release Readiness Exception Board Review

Use this skill to convert release readiness exception, launch gate waiver, release risk acceptance, feature flag mitigation, rollback trigger, support readiness, customer-scope exception, and approval board questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify release scope, unmet gates, evidence gaps, customer impact, risk tier, mitigation options, decision authority, rollout containment, support/docs readiness, monitoring, rollback proof, and exception expiry.
2. Read `references/release-readiness-exception-board-patterns.md`.
3. Classify the situation as minor gate waiver, customer-limited release, compliance-sensitive exception, migration exception, store deadline exception, hotfix exception, feature-flagged rollout, or release freeze override.
4. Define exception intake, evidence requirements, decision table, approval authority, mitigation owners, rollout limits, rollback triggers, monitoring signals, support comms, expiry, and post-release review.
5. Produce exception board packet, state machine, decision table, event schema, exception register, readiness checklist, approval record, and post-release follow-up plan.

## Guardrails

- Do not let exceptions become a way to bypass normal release gates without evidence, owner, expiry, and review.
- Do not approve customer-impacting exceptions without support readiness, monitoring, rollback trigger, and communication plan.
- Do not confuse a feature flag with mitigation unless kill-switch ownership and customer impact are proven.
- Do not leave repeated exceptions as process debt; route them into gate, staffing, or architecture fixes.

## Output format

```text
Release exception context:
Audience / source of truth / risk boundary:

Exception board plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Unmet gates, risk acceptance, mitigations, approvals, monitoring, rollback, support, and expiry:
- <trigger> -> <policy, metric, edge case, support note>
```
