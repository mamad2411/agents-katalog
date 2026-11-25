---
name: packaging-and-distribution
description: Select and apply Python packaging/distribution mode for CLI or desktop delivery. Use when shipping runnable artifacts.
---

# Packaging and Distribution

## Goal
Produce repeatable artifact build and release checklist.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Mode selection using `../_shared/python-packaging-matrix.md` plus versioned release checklist.

## Verify Gate
Build artifact succeeds and smoke run validates startup path.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
