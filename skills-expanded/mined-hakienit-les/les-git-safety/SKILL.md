---
name: les-git-safety
description: Plan or perform version-control work when commits, history, branches, remotes, or cleanup affect recoverability.
invocation: model
maturity: stable
route: repository-operations
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/risk-model.md","../../policies/rules/git-safety.md","../../policies/rules/change-scope.md"]
---

# Git Safety

## Invoke

Inherit `../les-bootstrap/SKILL.md` and Git safety policy.

## Inputs

Repository state, requested operation, affected refs, and rollback option.

## Procedure

1. Inspect status and exact targets. Done when: impact is explicit.
2. Classify recoverability and risk. Done when: required approval is named.
3. Perform or plan the narrow operation. Done when: state and next action are recorded.

## Output

Repository-state record and terminal status.

## Guardrails

Never infer authority for destructive or remote mutation.

Use `BLOCKED` when the repository has no explicit target or change state from
which a safe operation can be mapped. Use `PENDING_USER_ACTION` when the
operation is understood but authority for the next mutation is missing.

## Verification

Report exact refs, diff/status evidence, and rollback path.

Bootstrap LES. Inspect status and exact targets, preserve unrelated work, classify
the operation, and choose the most recoverable native command. Output the local
result and recovery point. Stop before commit without user intent and before any
R3 operation without immediate approval; verify status after the operation.
