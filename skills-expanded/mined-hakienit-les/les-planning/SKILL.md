---
name: les-planning
description: Plan multi-step engineering work after the outcome is clear and before execution begins.
invocation: model
maturity: stable
route: planning
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/risk-model.md","../../policies/rules/architecture.md","../../policies/rules/change-scope.md","../../policies/rules/definition-of-done.md"]
---

# Planning

## Invoke

Inherit `../les-bootstrap/SKILL.md` and load declared policy dependencies.

## Inputs

Clear outcome, scope, affected flow, and risk constraints.

## Procedure

1. Map acceptance conditions to owned delivery steps. Done when: every step has an owner, affected path, and evidence target.
2. Read the adopting project's context and durable decisions before planning. Trace callers, dependencies, boundaries, and project decisions. Done when: shared vocabulary, responsible seam, and integration order are explicit.
3. Identify risk, rollback, approvals, and unavailable evidence. Done when: risk is bounded and no authority is implied.
4. Sequence the smallest coherent work units and stop condition. Done when: the next action is executable without reopening scope.

## Output

Plan with objective, non-goals, file ownership, dependencies, acceptance evidence,
risks, approvals, rollback path, and terminal status.

## Guardrails

Do not authorize mutation or prescribe project-owned decisions without evidence.

## Verification

Mark unresolved choices `PENDING_USER_ACTION` and verify every condition has a
check, every risky step has a recovery path, and every new abstraction has a
consumer or proven boundary.

Bootstrap LES. Trace the affected flow, order coherent changes, attach proof to
each risky step, and name exclusions and rollback. Output an executable plan with
file ownership, dependencies, and completion criteria. Stop when the plan depends
on an unresolved decision; verify that every step serves an acceptance condition.
