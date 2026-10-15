---
name: skill-lifecycle-manager
description: >-
  Report skill lifecycle stage from frontmatter, eval coverage, and validators.
  Use when promoting, deprecating, or auditing repo skills. NOT for live installs.
user-invocable: true
argument-hint: "<skill-name|repo> [--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Lifecycle Manager

Classify repository skills by lifecycle stage and readiness gates.

**Scope:** Read-only lifecycle reporting. Does not edit skills, run installs, or mutate catalog indexes.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| `<name>` | Lifecycle report for one skill |
| `repo` / `--all` | Summary for every `skills/*/` directory |
| `--format json` | Machine-readable report |
| Empty | Show stage definitions and example commands |

## Lifecycle Stages

| Stage | Signals |
|-------|---------|
| `draft` | TODO description, missing evals, or failing `scripts/check.py` contract |
| `internal` | `metadata.internal: true` |
| `active` | Valid frontmatter, eval manifest, and portable validator present |
| `deprecated` | Body or metadata marks deprecation (maintainer-authored) |

## Workflow

```bash
uv run python skills/skill-lifecycle-manager/scripts/lifecycle_report.py <name>
uv run python skills/skill-lifecycle-manager/scripts/lifecycle_report.py --all --format json
```

Pair lifecycle output with `/skill-creator audit` before promotion.

## Validation Contract

```bash
uv run python skills/skill-lifecycle-manager/scripts/check.py
```

## Critical Rules

1. Never auto-promote a skill based on lifecycle heuristics alone.
2. Treat missing evals as a draft signal, not a hard block for internal skills.
3. Do not mutate `metadata.internal` or catalog authoring rows from this skill.
4. Run the repo validation command before declaring a skill active-ready.
5. Route executable fixes to skill-creator or the maintainer lead.
