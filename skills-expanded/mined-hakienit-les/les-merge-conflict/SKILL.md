---
name: les-merge-conflict
description: Resolve an active merge or rebase conflict while preserving both sides' intended behavior.
invocation: model
maturity: stable
route: merge-conflict
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/git-safety.md","../../policies/rules/change-scope.md","../../policies/rules/testing.md"]
---

# Merge Conflict

## Invoke

Inherit `../les-bootstrap/SKILL.md` and Git safety policy.

## Inputs

Active conflict, both intended changes, and affected behavior.

## Procedure

1. Read both sides and common base. Done when: each intent is understood.
2. Resolve at the behavioral owner. Done when: neither intent is silently discarded.
3. Run impacted proof. Done when: merged behavior is evidenced.

## Output

Resolved state or blocked conflict record with terminal status.

## Guardrails

Do not use destructive history operations or resolve by arbitrary side selection.

## Verification

Record conflict paths, preserved intentions, and focused checks.

Bootstrap LES. Confirm the active Git operation, read both sides and their callers,
resolve by behavior rather than markers, and keep unrelated files untouched.
Output resolved files and focused verification. Stop on ambiguous product intent;
verify no conflict markers remain and affected behavior passes.
