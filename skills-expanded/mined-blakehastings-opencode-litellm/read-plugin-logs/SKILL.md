---
name: read-plugin-logs
description: >-
  Read and filter [litellm-plugin] debug lines from the most recent OpenCode log
  file. Use when diagnosing why the LiteLLM provider is not appearing in the UI,
  troubleshooting model fetch failures, auth key issues, config hook startup
  errors, or any opencode-litellm plugin problem. Injects live log output for
  immediate analysis.
argument-hint: "[--lines N] [--all-logs]"
context: fork
allowed-tools: Bash
---
# Read Plugin Logs

## Live Log Output

!`uv run read-logs $ARGUMENTS`

## Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--lines N` / `-n N` | 100 | Show last N matching lines (0 = all) |
| `--all-logs` | off | Search all retained log files, not just the most recent |

## Manual Invocation

From the repo root:

```sh
uv run read-logs                      # last 100 litellm-plugin lines
uv run read-logs --lines 500          # more history
uv run read-logs --all-logs           # across all retained logs
```

uv auto-creates a `.venv/` and installs dependencies on first run.

## Log File Location

The plugin logs via `client.app.log()` which writes into OpenCode's standard session log:

- **Windows:** `%USERPROFILE%\.local\share\opencode\log\<timestamp>.log`
- **macOS/Linux:** `~/.local/share/opencode/log/<timestamp>.log`

The script filters these files for lines containing `litellm-plugin` (the service name).
