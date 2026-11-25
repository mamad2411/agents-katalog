---
name: problem-log
description: A hands-off daily log of how you actually solve problems. Once a day it reads your Claude Code sessions and writes a short entry per real problem-solving arc (the problem, how you worked it, the outcome) to a local markdown file. Great for standups, reviews, interviews, or just remembering what you figured out.
---

# problem-log

You solve real problems in Claude Code every day and forget them by next week. This logs them automatically.

Once a day a cron reads that day's Claude Code sessions, finds the genuine problem-solving arcs (a bug you chased down, a design decision with tradeoffs, a diagnosis that overturned your first guess), and appends a short entry for each to a markdown file. No manual step. Routine chatter and simple lookups are skipped.

## What you get, per arc
- **Problem** — the friction in one line
- **Approach & iteration** — how you worked it, including dead ends and pivots
- **Outcome** — what actually resolved it
- **Tools** — what you used
- Date + source session id

## Setup (2 minutes)
1. Requires the `claude` CLI on your PATH and Python 3.
2. Pick where the log lives (default `~/problem-log.md`).
3. Install the daily cron:
   ```
   cp com.example.problem-log-daily.plist ~/Library/LaunchAgents/
   # edit the path inside to point at this folder, then:
   launchctl load ~/Library/LaunchAgents/com.example.problem-log-daily.plist
   ```
   (On Linux, use the `crontab` line in `daily-sweep.sh`'s header instead.)

## Run it by hand
```
./daily-sweep.sh          # log yesterday's arcs now
./daily-sweep.sh dry      # print what it would log, write nothing
```

## How it works
`build_digest.py` (pure local, no LLM) reads your session transcripts from `~/.claude/projects`, keeps only the human/assistant text, and drops trivial sessions. Then a headless `claude` pass reads that digest per `SWEEP_PROMPT.md` and appends the arcs to your log file. Nothing leaves your machine except the model call you already use.
