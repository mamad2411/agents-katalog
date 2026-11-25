---
name: les-work-triage
description: Triage a set of engineering requests by outcome, urgency, risk, dependency, and next safe action without implementing them.
invocation: model
maturity: stable
route: triage
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/risk-model.md","../../policies/rules/change-scope.md","../../policies/rules/definition-of-done.md"]
---

# Work Triage

## Invoke

Bootstrap LES when multiple requests compete for attention or their risk and
ownership are unclear.

## Inputs

Request list, user impact, deadlines, dependencies, known evidence, ownership,
and available capacity constraints.

## Procedure

1. Normalize each request into outcome, evidence, and unresolved choice. Done when: symptom, desired result, and non-goals are separate.
2. Classify urgency, blast radius, reversibility, and dependency order. Done when: priority reasons are visible rather than implied.
3. Select the smallest safe next action for each item. Done when: no item is represented as implementation-ready without acceptance.
4. Return the queue and escalation points. Done when: blocked, pending-user, and ready items are distinguishable.

## Output

Prioritized triage record with rationale, risk, dependency, owner, next action,
acceptance gap, and terminal status per request.

## Guardrails

Triage does not authorize scope expansion, destructive work, or external mutation.
Urgency never bypasses risk or approval policy.

## Verification

Check that each priority has an evidence-based reason and that unresolved decisions
are surfaced as `PENDING_USER_ACTION` or `BLOCKED`.
