---
name: les-migration
description: Change a schema, API, protocol, configuration, or dependency while preserving compatibility and rollback.
invocation: model
maturity: stable
route: migration
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/feature-delivery.md","../../policies/rules/architecture.md","../../policies/rules/dependencies.md","../../policies/rules/error-handling.md","../../policies/verification.md"]
---

# Migration

## Invoke

Inherit `../les-bootstrap/SKILL.md` and migration-relevant policies.

## Inputs

Current and target contracts, compatibility constraints, and rollback path.

## Procedure

1. Define transition and compatibility window. Done when: old and new behavior are explicit.
2. Prove reversible movement through each boundary. Done when: rollback is executable.
3. Verify consumers and data transitions. Done when: required compatibility passes.

## Output

Migration plan or change, compatibility proof, and terminal status.

## Guardrails

Do not remove compatibility or execute R3 transitions without immediate approval.

## Verification

Report forward, rollback, and unavailable boundary evidence separately.

Bootstrap LES. Define old and new contracts, compatibility window, ordered cutover,
preservation proof, and rollback before mutation. Output a reversible transition
with explicit cleanup criteria. Stop at external or destructive steps without R3
approval; verify both forward use and rollback against representative data.
