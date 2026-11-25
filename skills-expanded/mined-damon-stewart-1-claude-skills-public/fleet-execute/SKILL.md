---
name: fleet-execute
description: "Execute READY plans from the fleet triage queue. Shows which plans scored ready, asks for confirmation, then dispatches agents. Triggers on: /fleet-execute, 'run fleet', 'execute ready plans', 'dispatch fleet', 'run the fleet'."
user_invocable: true
---

# /fleet-execute: Plan Fleet Dispatcher

Dispatches autonomous agents to execute plans that scored READY in the last triage run.

## Setup

This skill assumes:
- A triage output directory, default `~/Claude-Stuff/fleet/` (adjust to your setup)
- A `fleet-execute.sh` script at `~/bin/fleet-execute.sh`
- A `fleet-triage.sh` script at `~/bin/fleet-triage.sh`

Both scripts must be executable. Adjust paths in this skill to match your local install.

## What to do

1. **Check triage data.** Read `~/Claude-Stuff/fleet/triage-latest.json` and `~/Claude-Stuff/fleet/last-triage.json`. If no file exists or triage is >12 hours old, tell the user and suggest running `~/bin/fleet-triage.sh` first.

2. **Show READY plans.** Display each plan that scored READY (score 10-12), with:
   - Plan name
   - Score (X/12)
   - Per-criterion breakdown (acceptance / no-human / paths / idempotency)
   - One-sentence summary
   - Any noted blockers

3. **Confirm with user.** Ask: "Ready to dispatch agents for these N plans? (yes/no, or name specific plans to skip)"

4. **On confirmation:** Run:
   ```bash
   ~/bin/fleet-execute.sh
   ```
   Do NOT pass `--autonomous`. Interactive mode only here.

5. **Tell the user:**
   - Run output lands at: `~/Claude-Stuff/fleet/runs/{date}-{time}/`
   - Escalations go to: `~/Claude-Stuff/fleet/needs-human.md`

6. **After completion:** Read the latest `~/Claude-Stuff/fleet/runs/*/summary.md` and report: how many completed, how many escalated.

## Stale triage handling

If `last-triage.json` is missing or triage was >12 hours ago:

> "No recent triage data (last run: {date} or never). Run `~/bin/fleet-triage.sh` manually. Triage takes 2-5 minutes."

## Hold file

To cancel today's execution without running this skill:
```bash
touch ~/Claude-Stuff/fleet/hold
# or for a specific date:
touch ~/Claude-Stuff/fleet/hold-$(date +%Y-%m-%d)
```

## Dry run

To see what would be dispatched without running agents:
```bash
~/bin/fleet-execute.sh --dry-run
```

## Notes

- Agents run with `--allowedTools "Read,Glob,Grep,Edit,Write"` (no Bash in allowedTools)
- Each agent has a 30-minute timeout
- Max 2 agents run concurrently
- Failed or blocked agents escalate to `needs-human.md` automatically
