---
name: sync-agents
description: This skill activates when the user mentions "sync agents", "agent registry", "validate agents", "agent mismatch", "update registry", "fix agent", "check agents", "agent out of sync", or when adding/removing agent .md files from the agents/ directory. Also runs automatically during daily-check.
version: 2.0.0
---

# Agent Sync Skill

Keeps `agents/*.md` frontmatter in sync with `config/agent-registry.json`.

## Triggers

Auto-trigger on these phrases:
- "sync agents", "sync the agents", "sync agent registry"
- "validate agents", "check agents", "agent check"
- "agent registry", "update registry", "registry out of sync"
- "agent mismatch", "agent id mismatch", "id not in registry"
- "fix agent", "fix agents", "fix the registry"
- "agent out of sync", "agents not in sync"
- "add agent to registry", "remove agent from registry"
- "what agents do I have", "show agent stats", "agent statistics"

Also auto-runs during `daily-check.sh`.

## What It Validates

- Every `.md` in `agents/**/*.md` has required frontmatter fields (`id`, `name`, `category`, `primary_model`, `status`, `allowed-tools`)
- Every `id` in agent `.md` files exists in `agent-registry.json`
- Every agent in `agent-registry.json` has a corresponding `.md` file
- No duplicate IDs
- Valid model names (sonnet, opus, haiku, or known free/local models)
- Status values are `active` or `pool`

## Usage

```bash
/sync-agents              # validate only (--check, default)
/sync-agents --diff       # preview what --fix would change (dry-run)
/sync-agents --fix        # auto-fix mismatches
/sync-agents --stats      # show statistics breakdown
/sync-agents --check --json  # machine-readable output for CI
/sync-agents --path DIR   # use alternate agents directory
/sync-agents --quiet      # errors only, suppress info
```

## Auto-Fix Behavior

`--fix` will:
1. Add missing agents to registry (from .md frontmatter)
2. Remove orphaned registry entries (no .md file)
3. Update registry fields from .md frontmatter (one-way: .md → registry)

Always run `--diff` before `--fix` to preview changes.

## Integration

Runs automatically in:
- `daily-check.sh` (`--check` mode)
- `install.sh` Phase 10 (`--check` with warning on failure)
- Pre-commit hook (if enabled)
- forge cycles (via `--check --json` for structured output)
