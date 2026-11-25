---
name: skill-token-budget-linter
description: >-
  Lint skill descriptions, body length, and reference bulk against token budgets.
  Use when tightening standing-context cost. NOT for DCP tuning or RTK hooks.
user-invocable: true
argument-hint: "<skill-name|repo> [--strict]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Token Budget Linter

Measure standing-context pressure for skill assets before they ship.

**Scope:** Static token-budget linting only. Does not change OpenCode DCP, RTK, or harness hook policy.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Lint one skill directory |
| `repo` / `--all` | Lint every `skills/*/SKILL.md` |
| `--strict` | Fail on warning-tier budgets, not just hard limits |
| Empty | Show budget table and example commands |

## Budget Table

| Surface | Soft warn | Hard fail |
|---------|-----------|-----------|
| `description` | 200 chars | 1024 chars |
| body (below frontmatter) | 400 lines | 500 lines |
| single reference file | 300 lines | 500 lines |

## Workflow

```bash
uv run python skills/skill-token-budget-linter/scripts/lint_budget.py <name>
uv run python skills/skill-token-budget-linter/scripts/lint_budget.py --all
```

## Validation Contract

```bash
uv run python skills/skill-token-budget-linter/scripts/check.py
```
