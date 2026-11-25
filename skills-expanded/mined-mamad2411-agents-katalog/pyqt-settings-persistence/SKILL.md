---
name: pyqt-settings-persistence
description: Implement consistent persistence of user settings and UI state with version-aware migration. Use when app preferences are required.
---

# PyQt Settings Persistence

## Goal
Preserve user context safely across sessions.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
QSettings policy for window/table/path state plus settings version migration notes.

## Verify Gate
Settings round-trip correctly across restart with backward-compatible defaults.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
