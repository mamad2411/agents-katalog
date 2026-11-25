---
name: les-task-decomposition
description: Split an approved specification into independently verifiable delivery units when one change is too broad to execute safely.
invocation: model
maturity: stable
route: decomposition
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/architecture.md","../../policies/rules/change-scope.md","../../policies/rules/definition-of-done.md"]
---

# Task Decomposition

## Invoke

Inherit `../les-bootstrap/SKILL.md` and load declared policy dependencies.

## Inputs

Approved broad scope, dependencies, and acceptance conditions.

## Procedure

1. Find independently verifiable seams. Done when: each unit has one outcome.
2. Order units by dependency and risk. Done when: integration points are explicit.
3. Define proof and ownership per unit. Done when: parallel work cannot conflict silently.

## Output

Ordered task list with boundaries, evidence, and handoff points.

## Guardrails

Do not split work merely to create ceremony or change the approved outcome.

## Verification

Confirm every unit contributes to acceptance and has a deterministic completion check.

Bootstrap LES. Cut work at owned boundaries so every unit has an outcome, inputs,
dependencies, and decisive verification. Output the smallest ordered units that
still deliver coherent value. Stop if decomposition would create placeholder
architecture; verify full specification coverage with no duplicated ownership.
