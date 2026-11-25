---
name: chase-log-debug
description: Workflow for debugging local development environments using the chase CLI. Use this skill whenever the user wants to investigate logs, debug a running service, find out why something broke, check for recent errors, or validate service health — even if they don't mention "chase" explicitly. Trigger on phrases like "check the logs", "something is broken", "why is X failing", "show me errors", "what's happening with the service", "the app is down", "triage this", or "get me a debug snapshot". Especially useful in projects that use chase for log management.
---

# Chase Log Debug

Use `chase` as the single entrypoint for log triage.
Prefer JSON responses for machine steps, then switch to text only when reading long tails.

## Quick Flow

1. Verify the project is initialized:
   - Run `chase describe --output json`.
   - If initialization is missing, run `chase install .`.
2. Collect high-signal failures first:
   - Run `chase errors --output json`.
3. Inspect specific logs only when needed:
   - Run `chase logs $TARGET 120 --output json`
4. Produce a shareable snapshot for handoff:
   - Run `chase debug-bundle --output json`.
   - Read `.debug/latest.md`.

## Command Contract

Use these commands by default:

- `chase describe --output json`: Return command surface and expected project files.
- `chase errors --output json`: Return regex matches across `.logs/*.log`.
- `chase logs <target> <lines> --output json`: Return tail content for one target.
- `chase summary --output json`: Return per-log metadata and short tails.
- `chase debug-bundle --output json`: Write `.debug/latest.md` and return output path.
- `chase dev-up <target> --dry-run --output json`: Validate launch command without starting services.

## Agent Rules

- Prefer `--output json` for any step where another tool or decision follows.
- Use `--dry-run` before actions that may start long-running processes.
- Keep `lines` small first (`80-200`), then increase only if unresolved.
- Do not read pane output directly when `chase` data exists.
- If a command fails due to missing config, initialize with `chase install .` and continue.

## Escalation Pattern

If `chase errors` is empty but issue persists:

1. Run `chase summary --output json`.
2. Inspect suspicious target with `chase logs <target> 300 --output json`.
3. Rebuild snapshot with `chase debug-bundle --output json`.
4. Report findings using `.debug/latest.md` + exact failing lines.
