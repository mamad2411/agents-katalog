---
name: save-session
description: Summarize current progress and persist it to a dated session file so work resumes cleanly in a future session. Use before /compact, before ending a session, or at major milestones. Pairs with /resume-session.
---

# /save-session — persist progress

Goal: a future session (or a fresh context) can pick up exactly where this left off.

## File location
- Inside a git repo: `.claude/sessions/<YYYY-MM-DD>.md` (append across the day).
- Otherwise: `~/.claude/harness-claude/sessions/<YYYY-MM-DD>.md`.

Create the directory if needed. Append to today's file; don't pollute it with old work
— start a new dated file per day.

## What to write (evidence-based, not aspirational)
```
# Session <date> — <project/feature>
## Goal / current objective
## What works (verified, with evidence: test names, commands, screenshots)
## What was tried and did NOT work (so we don't repeat it)
## Not yet attempted / remaining (the next concrete steps)
## Key decisions & files touched
## Open questions / blockers
```

## How
1. Summarize honestly: distinguish *verified* from *assumed*.
2. Append (don't overwrite) under a timestamped subheading.
3. Tell the user the file path so they can review/edit it.

This skill is also invoked automatically by the PreCompact and Stop hooks — keep the
format stable so those writes stay consistent.
