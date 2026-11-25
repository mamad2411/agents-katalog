---
name: dependency-and-env-policy
description: Standardize lockfile usage, environment variable conventions, and reproducible local commands. Use to avoid machine-specific behavior.
---

# Dependency and Environment Policy

## Goal
Make Python environments deterministic across developers and CI.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Document and apply policy from `../_shared/python-env-policy-template.md`, including lockfile and `.env.example` expectations.

## Verify Gate
Confirm lockfile exists and task aliases can run test/lint/run consistently.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
