---
name: mc
description: >-
  Mission Control command router — the Claude-native front door to the personal
  operating harness. Invoke as `/mc <subcommand>` (harvest, today, standup, weekly,
  tasks, done, bind). Runs the requested command and presents the result. Use when the
  user types "/mc ...", "mc harvest", "mc today", "mc standup", "mc weekly",
  "mc done", "mc bind", "run mission control", or asks for their session/task status.
---

# mc — Mission Control (run from inside Claude)

`/mc <subcommand> [args]` is how you drive Mission Control without leaving the Claude session.
Run the matching command below, then present the output to the user. The Python scripts under
`~/mission-control/bin/` are the engine; you are the front door.

`mc help` or bare `/mc` → list the subcommands below and stop.

## Subcommands

| `/mc …` | Run this | Notes |
|---|---|---|
| `harvest` | `python3 ~/mission-control/bin/harvest.py` | Per-session digest, each headed by its goal (iTerm tab name) + status. Fast, no LLM. |
| `harvest --summarize` | see **Rich harvest** below | Adds Progress + Next per session. |
| `today` | `python3 ~/mission-control/bin/today.py` | Today's tasks in one glance. |
| `standup` | `python3 ~/mission-control/bin/standup.py` | Plan the day; add `--draft` to write it into the daily note. |
| `weekly` | `python3 ~/mission-control/bin/weekly.py` | Weekly review agenda. |
| `tasks` | `python3 ~/mission-control/bin/vault_tasks.py` | Vault task buckets. |
| `done` | `python3 ~/mission-control/bin/done.py <slug>` | Mark a task done (sets `status: done`, clears `needs_review`, logs it). `--status <s>` for any status. |
| `bind` | `bash ~/mission-control/bin/mc-bind.sh <args>` | Bind a session ↔ task, e.g. `bind 7bdec158 --project "Surrogacy"`. |

Pass through any flags the user gave (`--draft`, `--log`, `--json`, etc.) verbatim.

## Rich harvest (`/mc harvest --summarize`)

This is the goal + Progress + Next per session view. You are already a Claude session, so do
NOT shell out to headless `claude` per session (that nests Claude in Claude and is wasteful).
Instead:

1. Run `python3 ~/mission-control/bin/harvest.py` to get the live sessions with their goals
   (the iTerm tab names) and status.
2. For each live session, read the recent tail of its transcript
   (`~/.claude/projects/*/<sessionId>.jsonl`) and summarize **Progress** (≤40 words) and
   **Next** (≤25 words). Transcripts are large (multi-MB) — spawn one bounded subagent per
   session ("read the last ~60 turns of this jsonl, return {progress, next}") so the main
   context stays clean; run them in parallel.
3. Present each session as: `● <goal>` then `progress:` / `next:` lines, waiting-on-you first.

The unattended 6:45am job uses `harvest.py --summarize` (headless `claude`) instead, because
there's no live Claude there to do step 2. Same output shape, different engine.

## Notes

- Every command reads live state and prints; only `--draft`/`--log` write (into the vault daily
  note, never an existing task). Present results faithfully; surface waiting-on-you sessions first.
- The terminal executable `mc` still exists for plain-shell use, but `/mc` is the in-session way.
- Engine + design: `~/mission-control/README.md`.
