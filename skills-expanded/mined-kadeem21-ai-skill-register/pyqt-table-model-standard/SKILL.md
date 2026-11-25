---
name: pyqt-table-model-standard
description: Use QAbstractTableModel and proxy models for scalable tables in PyQt applications. Use when datasets exceed simple widget-table usage.
---

# PyQt Table Model Standard

## Goal
Keep table rendering performant and maintainable.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Contract from `../_shared/pyqt-table-model-contract.md` and sort/filter approach.

## Verify Gate
Avoid QTableWidget for large datasets; demonstrate model/proxy integration.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
