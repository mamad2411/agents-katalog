---
name: skill-install-dry-run-planner
description: >-
  Plan cross-harness skills sync dry-run steps before any live install.
  Use when reconciling harness skill inventory. NOT for --apply or npx installs.
user-invocable: true
argument-hint: "[--harness <name>] [--format json]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Skill Install Dry-Run Planner

Produce a maintainer plan from skills-sync dry-run evidence.

**Scope:** Dry-run planning only. Never run live apply installs from this skill.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Empty | Full dry-run plan for all harnesses |
| `--harness <name>` | Plan for one harness adapter |
| `--format json` | Machine-readable plan |
| `help` | Show phases, gates, and related runbooks |

## Planned Phases

1. **Validate** — run the repo validation command
2. **Dry-run JSON** — run the skills-sync dry-run JSON command
3. **Review gaps** — inspect `missing`, `unresolved`, and `skipped` rows per harness
4. **Optional smoke** — `INSTALL_SMOKE=1` temp-home phase (maintainer machine only)
5. **Apply gate** — human approval required before any `--apply`

Also see `skills/cross-agent-install-smoke/` and `docs/runbooks/install-smoke.md`.

## Workflow

```bash
uv run python skills/skill-install-dry-run-planner/scripts/plan_dry_run.py
uv run python skills/skill-install-dry-run-planner/scripts/plan_dry_run.py --harness cursor --format json
```

## Validation Contract

```bash
uv run python skills/skill-install-dry-run-planner/scripts/check.py
```

## Critical Rules

1. Default to dry-run; treat sync JSON as evidence, not authority over repo policy.
2. Never auto-apply installs or run live `npx skills add` from this skill.
3. Run phase 1 dry-run checks before recommending reconciliation.
4. Gate temp-home smoke behind `INSTALL_SMOKE=1`.
5. Document unresolved catalog rows instead of silently skipping them.
