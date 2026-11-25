---
name: pyqt-dialogs-and-validation
description: Standardize field validation and error presentation in PyQt forms and dialogs. Use when validation is inconsistent or duplicated.
---

# PyQt Dialogs and Validation

## Goal
Separate UI-level and domain-level validation cleanly.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Validation flow and message display policy (inline/status/dialog).

## Verify Gate
Validation runs live and on submit with clear user feedback path.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
