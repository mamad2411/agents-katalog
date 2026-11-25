---
name: qt-signals-slots-convention
description: Standardize signal and slot naming and responsibility boundaries in Qt components. Use when event flow is inconsistent.
---

# Qt Signals Slots Convention

## Goal
Make component communication explicit and maintainable.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Signal naming rules (`somethingChanged`, `requestX`, `errorOccurred`) and controller/view contract.

## Verify Gate
View emits intents, controller performs work, view updates state only.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
