---
name: les-feature-delivery
description: Deliver a bounded feature when new user-visible or system behavior is requested.
invocation: model
maturity: stable
route: feature
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/feature-delivery.md","../../policies/rules/architecture.md","../../policies/rules/coding-quality.md","../../policies/rules/testing.md","../../policies/rules/change-scope.md"]
---

# Feature Delivery

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the feature workflow.

## Inputs

Approved behavior, acceptance checks, affected flow, and constraints.

## Procedure

1. Inspect the responsible seam and define exclusions. Done when: scope is bounded.
2. Establish behavioral proof and implement one vertical slice. Done when: acceptance behavior exists.
3. Run required checks, fix findings in scope, rerun affected checks, and review the final diff. Done when: evidence is recorded and no known delivery defect remains.

## Output

Working slice, verification record, and terminal status.

## Guardrails

Do not expand product scope, bypass approval, or mutate unrelated files.

## Verification

Return focused and integrated evidence; name unavailable checks.

Bootstrap LES, then load:

- `../../policies/workflows/feature-delivery.md`
- `../../policies/rules/architecture.md`
- `../../policies/rules/coding-quality.md`
- `../../policies/rules/testing.md`
- `../../policies/rules/change-scope.md`

Input: accepted behavior and repository context. Output: one complete slice and
verification evidence. Stop when product ambiguity changes the design or an
approval gate is unmet.
