---
name: python-project-fingerprint
description: Detect Python project layout and execution conventions by inspecting pyproject.toml, requirements, setup.cfg, test and lint configs. Use before editing unknown Python repositories.
---

# Python Project Fingerprint

## Goal
Eliminate guesswork for Python run/test/lint/build workflows.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Create `RUNBOOK.md` from `../_shared/python-runbook-template.md` and `repo_fingerprint.json` including toolchain and source-of-truth paths.

## Verify Gate
Run discovered run/test/lint commands or record explicit blockers with confidence level.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
