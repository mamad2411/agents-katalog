---
name: reset-plugin-config
description: >-
  Clears the provider.litellm entry in opencode.json, the litellm credential
  in OpenCode's auth store, and any cached opencode-litellm@* package under
  ~/.cache/opencode/packages/. Use when testing setup flows, switching proxies,
  reproducing first-run behavior, picking up local src/index.ts edits past a
  stale npm cache, or when plugin config has gotten into an unexpected state.
argument-hint: "[--dry-run]"
context: fork
allowed-tools: Bash
---
# Reset Plugin Config

## Live Output

!`uv run reset $ARGUMENTS`

## Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--dry-run` | off | Print what would be removed without modifying files |

## What This Wipes

| Path | Action |
|------|--------|
| `~/.config/opencode/opencode.json` | `provider.litellm` removed (other keys preserved) |
| `~/.local/share/opencode/auth.json` | top-level `litellm` credential removed (other providers preserved) |
| `~/.cache/opencode/packages/opencode-litellm@*/` | every cached plugin version deleted |

All operations are no-ops if the file or key is missing — safe to run anytime.

The cache wipe matters because OpenCode downloads npm-sourced plugins once and
keeps using the cached copy even after you publish a new tag or edit the local
source — if any opencode.json on your machine references the plugin by tag
(e.g. `"plugin": ["opencode-litellm"]`), the cached bundle shadows your edits
until it's removed.

## Manual Invocation

From the repo root:

```sh
uv run reset              # wipe
uv run reset --dry-run    # preview
```

uv auto-creates a `.venv/` and installs dependencies on first run.

## After Reset

Run `/connect litellm` to reconfigure from scratch: provide the LiteLLM proxy
URL and API key (if needed), then restart OpenCode.
