---
name: skill-quality-dashboard
description: >-
  Aggregate generated maintainer reports into a skill-quality summary.
  Use when reviewing docs, link, and eval health. NOT for editing report sources.
user-invocable: true
argument-hint: "[--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Quality Dashboard

Summarize maintainer ops reports for skill and docs quality gates.

**Scope:** Read-only aggregation of committed `docs/public/generated-reports/*.json`. Does not regenerate reports.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Empty | Default dashboard summary |
| `--format json` | Machine-readable aggregate |
| `reports` | List registered report files and key counts |

## Workflow

```bash
uv run python skills/skill-quality-dashboard/scripts/aggregate_reports.py
uv run python skills/skill-quality-dashboard/scripts/aggregate_reports.py --format json
```

Regenerate upstream reports with the repo docs-generation pipeline — do not hand-edit JSON.

## Validation Contract

```bash
uv run python skills/skill-quality-dashboard/scripts/check.py
```

## Critical Rules

1. Treat generated report JSON as evidence, not authority to bypass validate gates.
2. Never hand-edit `docs/public/generated-reports/*.json`.
3. Pair dashboard output with skill-lifecycle-manager for per-skill readiness.
4. Route broken-link remediation to docs-steward.
5. Do not claim reports are fresh without checking generation timestamps when present.
