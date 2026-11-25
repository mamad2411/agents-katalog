---
name: test-planning
description: Plans focused test coverage for features, bug fixes, refactors, migrations, dependency updates, and risky changes. Use when deciding what tests to add, change, run, or skip across any language or framework.
---

# Test Planning

Use this skill before implementing or validating a change where test scope matters.

## When to Use This Skill

Use this skill for new features, bug fixes, refactors, dependency upgrades, migration changes, API contract changes, security-sensitive changes, performance-sensitive behavior, release checks, or merge quality checks.

## Planning Process

1. Identify the behavior or risk being changed.
2. Identify affected layers: unit, integration, contract, UI, database, infrastructure, or operations.
3. Inspect existing tests before adding new patterns.
4. Use `resources/test-strategy-matrix.md` to choose test level.
5. Prefer the smallest test set that meaningfully reduces risk.
6. Identify required validation commands from repository docs, scripts, CI config, or detected tooling.
7. State what will not be tested and why.

## Workflow

Use `workflows/test-plan-workflow.md` when a change needs a test strategy before implementation.

## Scripts

This skill owns `scripts/detect-test-tools.py`. The script is read-only and helps identify common test-tooling signals. Run it with `--help` before manual use.
