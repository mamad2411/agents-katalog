---
description: "Use when the user wants to check Tandem's activity log, review errors, or debug hook behavior. Also use when the user mentions 'tandem logs', 'what happened', or 'tandem errors'."
---

# Tandem Logs

Read and display entries from `~/.tandem/logs/tandem.log`.

## Subcommands

Parse `$ARGUMENTS` to determine the mode:

- **No arguments** (or empty): Show the last 20 log entries.
- **`errors`**: Filter to only `[ERROR]` and `[WARN ]` entries, show last 50.
- **A number (e.g., `50`)**: Show the last N entries.
- **`clear`**: Ask the user to confirm, then truncate the log file (`> ~/.tandem/logs/tandem.log`).

## Output format

Display the log entries in a code block. Each entry follows this format:
```
2026-02-12 10:30:45 [INFO ] [session-start] provisioned rules files
```

After the entries, show:
- Current log level: `TANDEM_LOG_LEVEL` env var (default: `info`)
- Tip: "Set `TANDEM_LOG_LEVEL=debug` for verbose output" (if not already debug)

## If log file doesn't exist

Report: "No log file found at `~/.tandem/logs/tandem.log`. Tandem logs are created on first hook execution."
