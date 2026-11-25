---
name: les-workspace-isolation
description: Prepare an isolated workspace for work that needs separation from dirty state, parallel changes, or a risky structural migration.
invocation: model
maturity: stable
route: workspace-isolation
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/risk-model.md","../../policies/rules/git-safety.md","../../policies/rules/change-scope.md"]
---

# Workspace Isolation

## Invoke

Bootstrap LES when isolation materially reduces collision, rollback, or dirty-tree
risk; do not create a worktree merely because the checkout is dirty.

## Inputs

Repository state, current branch, dirty paths, requested scope, base revision,
parallel writers, and rollback requirement.

## Procedure

1. Inspect status and ownership before isolation. Done when: unrelated changes and the intended base are recorded.
2. Choose current checkout, worktree, or another approved boundary. Done when: the choice is justified by collision or rollback risk.
3. Establish the boundary and verify identity. Done when: path, branch, base, and clean/dirty state are known.
4. Return the integration and cleanup plan. Done when: no unowned workspace remains and the next writer is explicit.

## Output

Workspace record with chosen boundary, identity, preserved paths, integration order,
rollback, cleanup, and terminal status.

## Guardrails

Preserve unrelated changes. Do not delete branches, reset, clean, or create remote
state without the relevant approval. Isolation does not grant mutation authority.

## Verification

Re-check repository identity and status before handoff. Report any unavailable or
conflicting state as `BLOCKED`.
