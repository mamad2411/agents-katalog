---
name: pyqt-export-pipeline-pdf-xlsx
description: Standardize PDF/XLSX export architecture in PyQt apps with preview-capable flow. Use for reporting, packing lists, and document outputs.
---

# PyQt Export Pipeline PDF XLSX

## Goal
Make export logic testable and reusable.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Generator -> renderer -> writer flow from `../_shared/pyqt-export-pipeline-template.md` plus preview/save behavior.

## Verify Gate
Golden tests validate semantic output fields/pages and UI preview path works.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
