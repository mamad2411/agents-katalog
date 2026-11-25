---
name: build-capture
description: A hands-off daily log of everything you build in Claude Code. Once a day it reads that day's sessions and the files that changed, and appends a short entry per real build (what it is, what shipped) to a local markdown file. No /wrap, no manual step. Perfect for standups, changelogs, or a running record of what you've made.
---

# build-capture

The stuff you build in Claude Code never gets written down unless you stop and do it. You won't. This does it for you.

Once a day a cron reads that day's Claude Code sessions plus the files that changed in a folder you watch, figures out what you actually built or shipped, and appends a short entry for each to a markdown file. Hands-off. Routine chatter and pure Q&A are skipped.

## What you get, per build
- **Name** — short title of the thing you built
- **What it is** — one plain sentence
- **Latest** — what happened today (built, shipped, fixed, refactored)
- Type (skill / script / app / fix) + date

## Setup (2 minutes)
1. Requires the `claude` CLI on your PATH and Python 3.
2. Set `WATCH_DIR` to the folder you build in (default: the current repo / `~/.claude/skills`), and `LOG_FILE` for the log (default `~/build-log.md`).
3. Install the daily cron:
   ```
   cp com.example.build-capture-daily.plist ~/Library/LaunchAgents/
   # edit the path inside to point at this folder, then:
   launchctl load ~/Library/LaunchAgents/com.example.build-capture-daily.plist
   ```
   (On Linux, use the `crontab` line in `daily-sweep.sh`'s header.)

## Run it by hand
```
./daily-sweep.sh          # log today's builds now
./daily-sweep.sh dry      # print what it would log, write nothing
```

## How it works
`build_digest.py` (pure local, no LLM) collects the last day's session text, the files that changed under `WATCH_DIR`, and recent git commits, into one digest. A headless `claude` pass reads it per `SWEEP_PROMPT.md` and appends the builds to your log, deduping by name so re-runs don't pile up. Additive only, it never edits past entries.
