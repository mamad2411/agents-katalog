---
name: pyqt-app-skeleton-mvc
description: Create or enforce PyQt project structure with ui/controllers/services/domain separation. Use when desktop app code is overly mixed.
---

# PyQt App Skeleton MVC

## Goal
Keep widgets focused on rendering while moving logic to controllers/services.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
MVC folder contract using `../_shared/pyqt-mvc-boundary-template.md`.

## Verify Gate
No direct SQL, network, or filesystem logic in widgets.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
