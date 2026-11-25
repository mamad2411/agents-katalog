---
name: pyqt-db-adapter-layer
description: Establish adapter and repository patterns for DB access in PyQt apps. Use when desktop app integrates with SQLite/MSSQL or similar stores.
---

# PyQt DB Adapter Layer

## Goal
Isolate data access from UI and keep domain mapping explicit.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Adapter/repository boundaries, transaction policy, retry strategy, and pagination guidance.

## Verify Gate
UI consumes repositories/services only; DB operations remain outside widgets.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
