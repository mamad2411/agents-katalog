---
name: les-bootstrap
description: Bootstrap LES for any engineering task by loading authority, project context, risk, workflow, and verification requirements.
invocation: bootstrap
maturity: stable
route: bootstrap
profile: core
loads: ["../../policies/principles.md","../../policies/precedence.md","../../policies/risk-model.md","../../policies/memory-model.md","../../policies/verification.md","../../policies/workflow-contracts.md","../../policies/rules/context-loading.md"]
---

# LES Bootstrap

## Invoke

Use first for every LES task; load only task-activated rules after this kernel.
When the session-start hook already injected this bootstrap, treat it as loaded and do not re-read `loads`.

## Inputs

Request, runtime constraints, project entrypoint, and current work state.

## Procedure

1. Resolve precedence and the task route. Done when: one route, near-miss interpretation, and fallback are selected.
2. Reconstruct relevant project context, active work state, and repository identity. Done when: scope, ownership, and stale evidence are named.
3. Classify risk, authority, active profile, verification tier, and team rung. Done when: approval and evidence gates are explicit and any dispatched department has a brief.
4. Report the next safe action and context trace. Done when: terminal evidence, residual uncertainty, and status are defined.

## Output

Task state: outcome, scope, route, fallback, risk, active profile, evidence class,
approval requirement, context trace, residual uncertainty, and terminal status.

For task-scoped responses, use the closeability footer defined in
`../../policies/workflow-contracts.md`.

## Guardrails

Do not grant authority, duplicate policy, or load inactive profiles. Load the rules the task activates and one workflow from `../../policies/workflows/`; use `task-lifecycle.md` when none matches. Load `../../policies/team.md` only when the task is R1 and multi-step, R2 or higher, or spans routes. Stop before dependent work when precedence is unresolved or required authority is absent.

## Verification

Return `COMPLETE`, `BLOCKED`, `PENDING_USER_ACTION`, `FAILED`, or `SKIPPED` with evidence.
