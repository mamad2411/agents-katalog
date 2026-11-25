---
name: les-refactoring
description: Restructure code while preserving an explicitly stated behavioral contract.
invocation: model
maturity: stable
route: refactoring
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/refactoring.md","../../policies/rules/architecture.md","../../policies/rules/coding-quality.md","../../policies/rules/testing.md","../../policies/rules/change-scope.md"]
---

# Refactoring

## Invoke

Inherit `../les-bootstrap/SKILL.md` and the refactoring workflow.

## Inputs

Current behavioral contract, structural objective, and characterization proof.

## Procedure

1. State unchanged behavior. Done when: preservation contract is explicit.
2. Move one boundary at a time. Done when: each step remains proven.
3. Reclassify behavior changes. Done when: scope remains truthful.

## Output

Simpler structure, preservation evidence, and terminal status.

## Guardrails

Do not smuggle features into a preservation route.

## Verification

Run characterization and affected integration checks after coherent moves.

Bootstrap LES, then load `../../policies/workflows/refactoring.md` and the
architecture, coding-quality, testing, and change-scope rules. Input the current
contract and structural objective. Output preservation evidence and the smaller
structure. Stop and reclassify if behavior must change.
