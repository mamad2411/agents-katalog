---
name: run-background
description: Submit and schedule long-running background scripts. Scripts execute as your Linux user with full access to your workdir and sharedDir, plus the Tool API for LLM-requiring tools (FetchUrl, Research, SearchWeb, PostMessage).
scope: platform
---

# Run Background

## Purpose

Run scripts that are too slow for an agent turn (>2 min) — data refreshes, web scraping,
report generation, model training. If the job is memory- or compute-heavy enough that it
might not fit on this mission's current machine, see the `request-resources` skill
*before* submitting it. Your script:

- Runs as **your** Linux user — same file permissions as your agent turn
- Can call LLM tools (FetchUrl, Research, SearchWeb, PostMessage) via the Tool API using
  the automatically-injected `MAGI_TOOL_TOKEN` and `MAGI_TOOL_URL` environment variables
- Stdout + stderr go to `sharedDir/logs/bg-<jobId>.log`
- On completion, you receive a mailbox notification (optional but recommended)

## Submit a one-shot job

```bash
bash $SKILL_DIR/../run-background/scripts/submit-job.sh \
  --script "$WORKDIR/scripts/refresh.py" \
  --args "$SHARED_DIR" \
  --agent "$AGENT_ID" \
  --notify-subject "Refresh complete"
```

### Arguments

| Flag | Description |
|------|-------------|
| `--script <path>` | Absolute path to the script (shebang selects interpreter) |
| `--args <...>` | Space-separated positional args to pass to the script |
| `--agent <id>` | Your agent id (determines linuxUser and ACL) |
| `--notify-subject <text>` | Subject for the completion PostMessage (omit to suppress) |
| `--notify-agent <id>` | Recipient of the completion notification (default: same as --agent) |

The script is submitted immediately (job file written to `sharedDir/jobs/pending/`).
The daemon picks it up within 1 minute.

## Schedule a recurring job

```bash
bash $SKILL_DIR/../run-background/scripts/schedule-job.sh \
  --label "daily-refresh" \
  --cron "30 5 * * *" \
  --script "$WORKDIR/scripts/refresh.py" \
  --args "$SHARED_DIR" \
  --agent "$AGENT_ID" \
  --notify-subject "Daily refresh complete"
```

Writes `sharedDir/schedules/<label>.json`. The daemon fires the script on schedule
and re-arms it automatically. Re-running with the same label updates the schedule.

## Check job status

```bash
bash $SKILL_DIR/../run-background/scripts/job-status.sh <jobId>
# → prints status JSON + last 20 lines of log
```

Job ids are printed by `submit-job.sh` and included in completion notifications.

## Calling tools from your script (Python)

Copy `magi_tool.py` into your script directory:

```bash
cp $SKILL_DIR/../run-background/scripts/magi_tool.py $WORKDIR/scripts/
```

Then import it in your Python script:

```python
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import magi_tool

# FetchUrl
result = magi_tool.fetch_url("https://example.com")
text = result["result"]["content"][0]["text"]

# Research
result = magi_tool.research("What is NVDA's current P/E ratio?")
finding = result["result"]["content"][0]["text"]

# PostMessage
magi_tool.post_message("lead-analyst", "Data refresh complete", "All series updated.")
```

Calling tools from shell scripts (bash):

```bash
magi-tool fetch-url --url "https://example.com"
magi-tool research --question "What is NVDA's current P/E ratio?"
magi-tool research \
  --question "Update NVDA brief from today's digest" \
  --context-file "$FACTORY/news/nvda/digest.json" \
  --context-file "$FACTORY/news/nvda/brief.md" \
  --output "$FACTORY/news/nvda/brief.md" \
  --max-age-hours 0
```

`MAGI_TOOL_TOKEN` and `MAGI_TOOL_URL` are injected automatically by the daemon.

## Concurrency limit

Maximum **3 background jobs** run simultaneously. Additional jobs wait in
`sharedDir/jobs/pending/` until a slot frees.

## Cancelling a scheduled job

```bash
rm $SHARED_DIR/schedules/<label>.json
```

The current pending entry will still fire once. To cancel pending jobs already queued in
`jobs/pending/`, delete the corresponding `.json` file there.
