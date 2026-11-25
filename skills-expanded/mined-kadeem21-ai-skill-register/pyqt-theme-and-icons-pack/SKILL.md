---
name: pyqt-theme-and-icons-pack
description: Standardize visual assets and theme loading with qrc/qss conventions. Use when UI styling is fragmented or hardcoded.
---

# PyQt Theme and Icons Pack

## Goal
Deliver consistent cross-platform look with asset pipeline.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
resources.qrc, qss variable policy, and DPI/font fallback guidance.

## Verify Gate
Theme loads from resources and remains readable across common DPI settings.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
