---
name: repo-fingerprint
description: Discover repository structure, entrypoints, run/test/lint/build commands, CI setup, and sources of truth before making changes. Use at the start of unfamiliar repositories or before high-impact work.
---

# Repo Fingerprint

## Goal
Produce a reliable repository fingerprint and quick run guide without guessing.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
`repo_fingerprint.json` aligned with `../_shared/repo-fingerprint.schema.json` and a short "how to run" section.

## Verify Gate
Run detected install, run, and test commands in dry or safe mode when possible; flag unknowns explicitly.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
