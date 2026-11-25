---
name: release-risk-exception-review
description: Design and audit release risk exceptions across launch gates, test failures, security findings, compliance gaps, performance regressions, rollout flags, customer impact, owner signoff, expiry, compensating controls, observability, rollback, incident readiness, and post-release review. Use when shipping despite an unresolved risk requires explicit governance.
---

# Release Risk Exception Review

Use this skill to convert release risk exception, launch gate waiver, known issue acceptance, test failure, compliance gap, performance regression, and rollback-readiness questions into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify release scope, blocked gate, unresolved risk, impacted customers, severity, owner, compensating control, expiry, rollout guardrail, observability, rollback path, and decision authority.
2. Read `references/release-risk-exception-patterns.md`.
3. Classify the situation as test waiver, known defect, security exception, compliance exception, performance regression, operational readiness gap, dependency risk, customer-specific exception, or emergency release.
4. Define risk statement, evidence, approval owner, guardrails, feature flags, monitoring, customer communication, rollback trigger, expiry, remediation task, and post-release review.
5. Produce release exception record, state machine, decision table, event schema, checklist, rollback plan, and post-release accountability log.

## Guardrails

- Do not convert release pressure into silent risk acceptance without owner, expiry, guardrails, and rollback criteria.
- Do not waive security, privacy, compliance, data-loss, payment, or availability gates with generic business approval.
- Do not ship known risk without customer-impact assessment and monitoring that can detect the failure mode.
- Do not leave exceptions open after release without remediation tracking and review.

## Output format

```text
Release exception context:
Audience / source of truth / risk boundary:

Release risk exception plan:
| Area | Decision | Evidence | Risk | Owner |
| --- | --- | --- | --- | --- |

Risk, authority, guardrails, monitoring, rollback, and expiry:
- <trigger> -> <policy, metric, edge case, support note>
```
