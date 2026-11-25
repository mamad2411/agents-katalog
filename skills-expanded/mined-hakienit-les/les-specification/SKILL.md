---
name: les-specification
description: Turn an approved product or engineering decision into an unambiguous implementation contract.
invocation: model
maturity: stable
route: specification
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/technical-decisions.md","../../policies/rules/documentation.md","../../policies/rules/definition-of-done.md"]
---

# Specification

## Invoke

Inherit `../les-bootstrap/SKILL.md` and load declared policy dependencies.

## Inputs

Approved decision, constraints, and acceptance intent.

## Procedure

1. State behavior, exclusions, and interfaces. Done when: scope is unambiguous.
2. Define failure, migration, and verification behavior. Done when: each boundary has an owner.
3. Resolve conflicting interpretations. Done when: implementation can proceed without guessing.

## Output

Implementation contract with acceptance conditions and terminal status.

## Guardrails

Do not invent product scope or restate universal policy.

## Verification

Check every requirement is observable and flag human choices as `PENDING_USER_ACTION`.

Bootstrap LES. Define observable behavior, boundaries, failure states, exclusions,
and acceptance evidence without prescribing incidental implementation. Output one
project-owned specification. Stop on contradictory requirements; verify it has no
placeholder, ambiguous authority, or acceptance condition without a check.
