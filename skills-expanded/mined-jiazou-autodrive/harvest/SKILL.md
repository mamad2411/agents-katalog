---
name: harvest
description: >-
  Mission Control's morning briefing. Summarizes the status of every live Claude session
  (what's running, what's waiting on you, what each is bound to) plus today's
  outstanding vault tasks. Read-only by default. Run on demand, or scheduled
  before wake-up (~7am). Use when asked to "harvest", "session status",
  "what are my agents doing", "morning briefing", or "what's running".
---

# harvest — Mission Control morning briefing

`harvest` answers one question: **"What is the state of everything right now, and what needs me?"**
It is the read-side of Mission Control. For each live Claude session it shows, headed by the
session's **goal** (its iTerm tab name, auto-resolved): the **goal**, a **progress** summary,
and **what to do next**. Sessions **waiting on you** sort first. Read-only.

## How to run

**Rich version (what the user wants — goal + progress + next per session):**

```bash
mc harvest --summarize
```

`--summarize` reads the recent tail of each session's transcript and summarizes Progress + Next
via headless `claude`. It makes one `claude` call per live session, so it takes a few seconds
each — fine on demand and for the 6:45am run. The Goal line (iTerm tab name) is always shown;
if a summary fails, that session degrades to Goal + status.

**Fast version (goal + status only, no LLM):**

```bash
mc harvest          # or: python3 ~/mission-control/bin/harvest.py
```

Then read the vault's due/overdue tasks (do NOT modify anything):

```bash
ls "${MC_VAULT:-$HOME/Documents/Vault}/01 Projects"/*/Tasks/*.md 2>/dev/null
```

Present the session digest first (it's the novel part), then a one-line vault summary
(`N overdue · M due today`), then — only if asked — propose the day's parallel plan.

## How the goal/progress/next are derived

- **Goal** = the iTerm tab name (`pid → tty → osascript`), which Claude Code auto-titles with the
  session's task. Falls back to the transcript's latest `ai-title` if iTerm automation is
  unavailable. No manual entry.
- **Progress / Next** = `bin/session_summary.py` summarizes the recent transcript tail. The
  6:45am job and `mc harvest --summarize` share this one path (no divergence).

## Binding sessions (enrichment)

When `harvest` shows an **unbound** session, bind it so future briefings carry the context:

```bash
mc bind <SHORT_ID> --project "<Project>" [--task <slug>] [--tab "<tab name>"]
```

- `<SHORT_ID>` is the 8-char id from the harvest output (full UUID also accepted).
- **Color and name are auto-resolved** from the session transcript (`/color`, `/rename`) —
  the binding only carries what can't be inferred: which task/project the session is on.
- Unbind with `mc bind --unbind <SHORT_ID>`. The ledger is append-only; latest event wins.

## Scheduled pre-wake run (the 6:45am job)

A launchd agent fires `bin/morning.sh` around 6:45am so you wake to today's surface already
written. It runs two real commands (see `bin/morning.sh`), appending output to
`~/mission-control/morning.log`:

```bash
mc standup --draft              # writes Today's Focus + Parallel Plan into the daily note
mc harvest --log --summarize    # per-session Goal/Progress/Next digest, appended to the daily note
```

`mc harvest --summarize` enriches each session with Progress + Next (one headless `claude`
call per live session); `--log` appends the rendered digest to today's daily note. These are
the only harvest flags — there is no `--prep` flag.

**Future (not built yet):** a richer "prep" mode would draft *tomorrow's* daily note plus a
proposed parallel plan with `needs_review: true`, so the pre-wake run produces a reviewable
draft rather than finalizing anything. This is unbuilt — you can't pass it today. When it is
built, everything it writes MUST be `needs_review: true` and land in `Daily/`, never mutating
existing task files.

## Design notes

- **Why join live files instead of a daemon:** Claude Code already writes per-session state
  to `~/.claude/sessions/`; Orchard only adds the binding it can't know (task/color/tab).
  No registration step, nothing to keep alive.
- **Liveness** = the session's pid still responds to `kill -0`. Dead sessions drop off
  automatically; no cleanup needed.
- Full design + roadmap: `~/mission-control/README.md`.
