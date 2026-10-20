---
name: scheduled-turns
description: Use when a task needs recurring or always-on agent turns (periodic checks, polling workflows, run-this-every-morning jobs) without adding a daemon. OS scheduler plus one-shot headless Devin turns writing to ledgers.
---

# Scheduled Turns

Runs an agent turn on an OS schedule. Each fire is a FRESH one-shot
session (`devin -p`), never re-entry into a live session, never a
daemon, matching the runtime's single-process model (AGENTS.md Rule 18;
heartbeat/session-checkpoint emulations were pruned for this reason).

## When to Use

- Recurring chores: inbox triage, dep-update checks, report generation
- "Always-on" behavior for an otherwise session-bound agent

## When NOT to Use

- Sub-hour cadence or real-time reaction: use `cu-realtime` or
  `browser.py events` inside a live session
- Anything needing conversation continuity: each turn is amnesiac, so
  persist state in files the next turn reads

## Recipe

1. Write the turn prompt to the project as `.devin/scheduled/<name>.md`
   (what to check, where to write results, when to stop).
2. Register one OS scheduled task per turn:

   Windows (PowerShell, run once by the user):
   ```powershell
   $act = New-ScheduledTaskAction -Execute "devin" `
     -Argument "-p --prompt-file .devin/scheduled/<name>.md --respect-workspace-trust false" `
     -WorkingDirectory "C:\path\to\project"
   $trg = New-ScheduledTaskTrigger -Daily -At 09:00
   Register-ScheduledTask -TaskName "devin-<name>" `
     -Action $act -Trigger $trg
   ```

   POSIX cron equivalent:
   `0 9 * * * cd /path && devin -p --prompt-file .devin/scheduled/<name>.md --respect-workspace-trust false >> .devin/ledgers/scheduled-<name>.log 2>&1`

3. Each run appends outcome evidence to
   `.devin/ledgers/scheduled-<name>.md`: outcome, what ran, next check.
   The ledger is the inter-turn memory; prompts must name the files a
   turn should read first.

## Guards

- One instance per task: the scheduled script writes a lock file and
  exits when it exists (stale locks older than 24h are removed).
- Schedules are user-approved once; the agent never registers or edits
  a task itself. It writes the prompt file and the user runs the
  register command.
- No secrets in prompt files, task arguments, or ledger output.
- `--respect-workspace-trust false` is required: print mode cannot show
  the workspace trust prompt, so an untrusted dir fails without it.
- Turns are bounded: the prompt must state a hard stop condition and a
  max runtime expectation; a turn that cannot finish writes
  `ABANDON: <reason>` to its ledger instead of hanging.

## Disable

```powershell
Unregister-ScheduledTask -TaskName "devin-<name>" -Confirm:$false
# cron: remove the crontab line
```

Delete `.devin/scheduled/<name>.md` to retire the turn's instructions.
