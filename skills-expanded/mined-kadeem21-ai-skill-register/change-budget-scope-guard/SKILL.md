---
name: change-budget-scope-guard
description: Constrain implementation by file/module/dependency budget and require explicit escalation before exceeding limits. Use for risk control in iterative coding.
---

# Change Budget and Scope Guard

## Goal
Keep changes predictable and reviewable.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Budget declaration and escalation note format from `../_shared/change-budget-policy.md`.

## Verify Gate
Compare planned and actual touched files/modules before each checkpoint close.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
