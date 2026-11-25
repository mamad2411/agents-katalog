---
name: cron-management
description: Manage Nolty's scheduled crons. Triggers on "show/list crons", "add a cron", "enable/disable cron X", "delete cron Y", "run cron Z now", "cron status", "next cron". Reads cron-runner/cron-jobs.json and cron-runner/state/cron-state.json. Always validates schedules with croniter before writing.
---

# Cron Management

Nolty's interface for managing the cron-runner. The runner at `cron-runner/bin/cron-runner.py` is the dispatcher — this skill is the CRUD layer for `cron-runner/cron-jobs.json`.

**Paths (adjust if your install location differs):**
- Config: `<NOLTY_HOME>/cron-runner/cron-jobs.json`
- State: `<NOLTY_HOME>/cron-runner/state/cron-state.json`
- Runner: `<NOLTY_HOME>/cron-runner/bin/cron-runner.py`

`<NOLTY_HOME>` is the path to your nolty/ checkout. Default: `~/Documents/CodingProjects/nolty`.

## Subcommands

Parse the user's intent into one of these actions. When ambiguous, ask. Never silently delete or fire a cron without confirmation.

### `list` — "show me my crons" / "list crons" / "next cron"

Run `python3 cron-runner/bin/cron-runner.py list` and format as a Telegram-friendly table. Include: enabled flag, id, next fire time (in user's TZ), last fired, model/effort. If the user asks "next cron", just return the soonest-firing enabled job.

### `add` — "add a cron that ..."

Conversational. Collect, in this order:

1. **id** (kebab-case, must be unique; suggest from name)
2. **name** (human label)
3. **schedule** (cron expression — validate with croniter; show next 3 fire times for confirmation)
4. **slash_command** (must start with `/`; verify the slash command file exists)
5. **model** (haiku | sonnet | opus — default sonnet)
6. **effort_level** (low | medium | high — default medium)
7. **category** (info | marketing | ops | sales)
8. **max_lag_minutes** — defaults by category: heartbeat=20, daily=60, weekly=1440, monthly=2880
9. **enabled** (default false — the user enables explicitly after a dry-run)

Validate schedule:
```python
from croniter import croniter
from datetime import datetime
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo("America/Chicago"))  # use user's TZ
c = croniter(schedule, now)
[c.get_next(datetime) for _ in range(3)]
```

Then append to `cron-jobs.json` `jobs` array and confirm.

### `enable <id>` / `disable <id>` — "disable the heartbeat cron"

Flip the `enabled` flag. Confirm with the user first if it's a high-visibility cron (heartbeat, morning-brief).

### `delete <id>` — "delete the X cron"

Remove the job. ALWAYS confirm first.

### `edit <id> <field> <value>` — "change daily-recap to 10pm"

Modify a single field. For schedule changes, validate with croniter and show new next-fire times before writing.

### `fire <id>` / `run <id>` — "run X now"

Force-fire one job immediately: `python3 cron-runner/bin/cron-runner.py fire <id>`. This bypasses the schedule check, types the slash command into Nolty's tmux pane. Note: that would trigger you (Nolty) to dispatch a sub-agent. Alternative: the user can just type the slash command directly in Telegram.

### `status` — "are crons healthy?"

Read `cron-state.json`. Report:
- N enabled jobs
- M fires in last 24h
- Any jobs with `last_status` other than `dispatched` or `dry_run`
- Most-recent fire and next upcoming

### `lookup <id>` — internal

Return a job's full record. Used by Nolty's routing rule if she needs full context on a cron.

## LaunchAgent control

- **Load** (start the 15-min dispatcher): `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/<your-label>.plist`
- **Unload**: `launchctl bootout gui/$(id -u)/<your-label>`
- **Check loaded**: `launchctl list | grep cron-runner`

Only suggest these to the user — don't run them silently. Loading/unloading the dispatcher is a system-level state change they should know about.

## Editing safety

- ALWAYS read `cron-jobs.json` fresh before writing — the user may have edited it.
- Write atomically: write to `.tmp` then rename.
- Validate JSON parses after every write.
- Keep `jobs` array sorted by `id` after add/edit for stable diffs.
- Never edit `cron-state.json` — that's the runner's territory.

## When the user's phrasing is ambiguous

- "is the morning brief cron working?" → run `status`, then specifically lookup `morning-brief` `last_fired_at` and next fire.
- "stop the heartbeat" → `disable heartbeat` (confirm).
- "add a 9pm cleanup" → start `add` flow; ask "what does it do?" to derive `slash_command`.
- "kill all crons" → confirm hard ("Disable ALL N crons? y/n"), then iterate `disable` per id.
