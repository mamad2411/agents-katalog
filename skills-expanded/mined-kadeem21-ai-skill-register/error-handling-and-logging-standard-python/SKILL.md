---
name: error-handling-and-logging-standard-python
description: Apply consistent exception taxonomy and logging policy in Python services, CLIs, or workers. Use when error handling is fragmented or inconsistent.
---

# Error Handling and Logging Standard Python

## Goal
Make errors predictable and logs actionable with log-once discipline.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Define domain error classes, API/UI mapping strategy, and correlation-id propagation where relevant.

## Verify Gate
Ensure each failure path has one logging point and stable outward-facing error shape.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
