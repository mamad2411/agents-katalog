---
name: telegram-plugin-maintenance
description: Maintain speech115/telegram-plugin: GitHub radar, safe PR flow, MCP/control-plane checks, plugin docs sync.
---

# Telegram Plugin Maintenance

Use this skill for `/Users/sereja/Projects/tools/telegram` when the task touches
GitHub state, commits/PRs, MCP tool behavior, control-plane commands, plugin
packaging, or release readiness.

## First Pass

1. Inspect local state with `git status --short --branch`.
2. For GitHub state, use `github-radar`:
   - `repobar pulls speech115/telegram-plugin --limit 20 --json`
   - `repobar issues speech115/telegram-plugin --limit 20 --json`
   - `repobar ci speech115/telegram-plugin --limit 20 --json`
3. Read `AGENTS.md`, then the narrower `mcp/AGENTS.md` or
   `control-plane/AGENTS.md` for files you will touch.

## Safe Change Flow

- Create a `codex/...` branch before repo changes.
- Commit with `safe-commit`, listing exact paths.
- Use `safe-pr` only when the user asked to publish a branch/PR.
- Keep merge, issue close, PR comments, tags, and releases as separate explicit
  user-approved actions.

## Checks

Run `scripts/safe-gate` before commit. For narrower edits, the focused checks
are:

```bash
mcp/.venv/bin/python -m pytest -q mcp/tests
control-plane/.venv/bin/python -m pytest -q control-plane/tests
mcp/bin/sync-agent-docs --plugin-dir plugin --check --no-restart --json
```

Run `scripts/ci-release-gate.sh` for release or packaging changes.

## Telegram-Specific Boundaries

- Default MCP expansion is read-only.
- Do not add or expose read-state mutators unless the user explicitly asks.
- Do not copy sessions, rewrite LaunchAgents, sync plugin caches, or start
  mirror/backfill jobs as incidental cleanup.
- After MCP tool metadata or surface changes, sync agent docs:

```bash
mcp/bin/sync-agent-docs --plugin-dir plugin --no-restart --json
```

Treat plugin drift checks as packaging evidence only; they do not prove live MCP
runtime health.
