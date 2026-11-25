---
name: les-review
description: Review a change, plan, or release candidate against its acceptance source and LES policy.
invocation: model
maturity: stable
route: review
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../policies/verification.md","../../policies/rules/security.md","../../policies/rules/testing.md","../../policies/rules/definition-of-done.md"]
---

# Review

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the review workflow.

## Inputs

Comparison point, acceptance source, and reviewed scope.

## Procedure

1. Resolve comparison identity, objective, dirty manifest, and freshness. Done when: the reviewed source cannot be confused with another change.
2. Inspect changed behavior, callers, state transitions, trust boundaries, and reachable UI journeys. Done when: evidence covers the affected flow and the standards and acceptance/spec questions are kept separate.
3. Assess correctness, tests, security, compatibility, performance, accessibility, and documentation. Done when: findings are shaped by impact and confidence.
4. Separate findings, no-findings, skipped coverage, and residual risk. Done when: result is actionable and no unrun check is implied to pass.

## Output

Severity-ordered findings or no-finding result with terminal status.

## Guardrails

Do not mutate without a separate request or claim unrun checks passed.

## Verification

Each finding includes severity, confidence, location, evidence type, impact, owner,
and next safe action. The report includes coverage and review identity.

Bootstrap LES, then load `../../policies/workflows/review.md`, verification,
security, testing, and definition-of-done rules. Input a fixed comparison point
and acceptance source. Output severity-ordered findings with locations and
evidence. Review remains read-only unless change authority is explicit.
