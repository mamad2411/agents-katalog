---
name: skill-bundle-curator
description: >-
  Summarize bundle components from agent-bundle.json and repo skill/agent counts.
  Use when packaging or auditing distributable bundles. NOT for live plugin installs.
user-invocable: true
argument-hint: "[--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Bundle Curator

Report bundle composition and adapter install surfaces for the repository root bundle.

**Scope:** Read-only bundle inventory. Does not run install commands or marketplace updates.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Empty | Default bundle summary |
| `--format json` | Machine-readable bundle report |
| `adapters` | List adapter install/update commands only |

## Workflow

```bash
uv run python skills/skill-bundle-curator/scripts/bundle_report.py
uv run python skills/skill-bundle-curator/scripts/bundle_report.py --format json
uv run python skills/skill-bundle-curator/scripts/bundle_report.py adapters
```

Cross-check counts with skill-router index before publishing bundle notes.

## Validation Contract

```bash
uv run python skills/skill-bundle-curator/scripts/check.py
```

## Critical Rules

1. Treat adapter install strings as documentation — do not execute them from this skill.
2. Never duplicate `skills/` or `agents/` into platform plugin folders.
3. Pair bundle reports with cross-agent-install-smoke dry-run before install reconciliation.
4. Keep bundle root policy aligned with `AGENTS.md` §2.1.
5. Route packaging ZIP work to the repo packaging command, not ad-hoc archives.
