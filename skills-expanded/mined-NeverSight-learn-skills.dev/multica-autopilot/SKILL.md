---
name: multica-autopilot
description: Schedule or manually trigger recurring Multica agent tasks via autopilots and cron. Covers autopilot CRUD, manual fires, run history, and cron trigger management. Use when the user mentions a recurring job, scheduled task, cron, nightly / weekly automation, or anything that should fire without a human in the loop.
---

# Multica Autopilot

An **autopilot** is a named automation that dispatches agent work on a schedule (or on demand). Each run can create a new issue assigned to an agent, which then executes as normal.

Official docs: https://github.com/multica-ai/multica/blob/main/CLI_AND_DAEMON.md#autopilot-commands

## When to use this skill

- "Run this every weekday at 9 AM" / "nightly bug triage" / "weekly sprint digest".
- Any recurring agent task — scheduled reports, periodic cleanups, cron-style automations.
- Re-running a one-off agent playbook on demand (`autopilot trigger`).
- Inspecting past runs of a scheduled task to see what happened.

## Model

```
Autopilot  (title, description as agent prompt, mode, agent, status)
  ├── Triggers  (cron + timezone, one autopilot can have many)
  └── Runs      (history of each fire — manual or scheduled)
```

## Core commands

```bash
multica autopilot list
multica autopilot list --status active --output json

multica autopilot get <id>
multica autopilot get <id> --output json    # Includes triggers

multica autopilot create \
  --title "Nightly bug triage" \
  --description "Scan todo issues and raise priority on anything critical." \
  --agent "Lambda" \
  --mode create_issue

multica autopilot update <id> --status paused
multica autopilot update <id> --description "New prompt"
multica autopilot delete <id>
```

Create flags: `--title`, `--description` (this is the prompt the agent receives each run), `--agent` (name or UUID), `--mode`.

**`--mode` only accepts `create_issue` today.** Each fire creates a new issue, assigns it to the agent, and records a run. The data model defines `run_only` but is not exposed via CLI.

## Manual trigger and run history

```bash
multica autopilot trigger <id>              # Fires once now; returns the run
multica autopilot runs    <id>              # All past runs
multica autopilot runs    <id> --limit 50 --output json
```

## Cron schedule triggers

Triggers are the attachment that turns an autopilot from "manual" into "scheduled". One autopilot can have multiple triggers (e.g. one for weekdays, one for weekends).

```bash
# Add: standard POSIX cron, timezone as IANA name
multica autopilot trigger-add <autopilot-id> \
  --cron "0 9 * * 1-5" \
  --timezone "America/New_York"

# Update (pause / resume)
multica autopilot trigger-update <autopilot-id> <trigger-id> --enabled=false
multica autopilot trigger-update <autopilot-id> <trigger-id> --cron "0 17 * * 5"

# Delete
multica autopilot trigger-delete <autopilot-id> <trigger-id>
```

Cron quick reference:

| Expression | Meaning |
|------------|---------|
| `*/15 * * * *` | Every 15 minutes |
| `0 * * * *`    | Top of every hour |
| `0 9 * * 1-5`  | 9:00 AM, Mon-Fri |
| `0 0 * * 0`    | Midnight Sunday |
| `0 0 1 * *`    | Midnight on the 1st of the month |

Only `schedule` (cron) triggers are exposed through the CLI today. `webhook` and `api` kinds exist in the data model but no server endpoint fires them yet.

## Common flows

**Create a weekday 9 AM triage autopilot end-to-end:**

```bash
AP=$(multica autopilot create \
  --title "Weekday bug triage" \
  --description "Review todo issues from the last 24h. For each critical-looking one raise priority to urgent and add a comment with a one-line justification." \
  --agent "Lambda" \
  --mode create_issue \
  --output json | jq -r '.autopilot.id')

multica autopilot trigger-add "$AP" --cron "0 9 * * 1-5" --timezone "America/New_York"
```

**Pause all autopilots during a freeze:**

```bash
multica autopilot list --status active --output json |
  jq -r '.autopilots[].id' |
  xargs -I {} multica autopilot update {} --status paused
```

**See what last night's run actually did:**

```bash
AP=<autopilot-id>
RUN=$(multica autopilot runs "$AP" --output json | jq -r '.runs[0].id')
# Runs translate to issues — inspect via the issues skill
multica issue run-messages "$RUN"
```

## Gotchas

- Timezone is an **IANA** name (`America/New_York`, `Asia/Shanghai`) — not `EST` or `GMT+8`. Wrong timezones silently run at the wrong hour.
- Pausing the autopilot (`--status paused`) stops *all* of its triggers. Disabling a single trigger uses `trigger-update --enabled=false`.
- The autopilot's `--description` is the agent prompt for every fire. Edit carefully — a bad prompt creates bad issues on every tick.
- Cron expressions are evaluated on the Multica server, not the runtime executing the task. Server clock skew is usually not an issue, but runtime clock skew is irrelevant here.
- `autopilot trigger` (manual fire) bypasses the cron schedule and does not consume / reset any schedule state.
