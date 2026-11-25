---
name: pyqt-logging-console-panel
description: Provide in-app log viewer and debug report export for PyQt desktop apps. Use when troubleshooting needs to happen inside the app.
---

# PyQt Logging Console Panel

## Goal
Improve supportability and issue reporting in production-like runs.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Logging panel spec including filtering, tail behavior, and copyable error report.

## Verify Gate
Panel displays runtime logs and captures stack trace plus app version info.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
