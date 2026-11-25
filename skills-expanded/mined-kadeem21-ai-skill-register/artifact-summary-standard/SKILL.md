---
name: artifact-summary-standard
description: Enforce a consistent delivery summary containing changed files, run steps, tests, and rollback instructions. Use at the end of every skill-driven task.
---

# Artifact Summary Standard

## Goal
Standardize handoff and debugging context.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Summary section matching `../_shared/artifact-summary-template.md`.

## Verify Gate
Reject completion if any section is missing.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
