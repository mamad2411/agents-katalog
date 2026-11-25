---
name: pyproject-bootstrap-standard
description: Generate or normalize pyproject.toml using PEP 621 with consistent tooling defaults. Use when standardizing Python project configuration.
---

# Pyproject Bootstrap Standard

## Goal
Provide one predictable baseline for formatting, linting, typing, and tests.

## Workflow
1. Read `../_shared/PROTOCOL.md` and align with task objective.
2. Read `../_shared/skill-usage-policy.md` and apply activation/escalation rules.
3. Collect repository evidence from source-of-truth files before proposing edits.
4. Produce required artifact for this skill.
5. Add explicit verify step and fail condition.
6. Stop and escalate if verify fails after two hypothesis changes.
7. Finish with summary from `../_shared/artifact-summary-template.md`.

## Required Output
Apply baseline from `../_shared/python-pyproject-pep621-template.toml` with uv + ruff + mypy + pytest defaults and optional pre-commit hooks.

## Verify Gate
Validate `pyproject.toml` structure and ensure configured tools can run in project context.

## Safety Rules
- Fail closed for risky work: architecture, refactor, release, config, or dependency changes.
- Do not exceed change budget without explicit escalation note.
- Do not repeat failing command without changing approach.
