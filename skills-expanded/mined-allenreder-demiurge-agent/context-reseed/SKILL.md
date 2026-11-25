---
name: context_reseed
description: Use and review bounded continuity notes that seed future sessions.
category: context
---

# Context Reseed

This package maintains a small continuity note for future sessions. The note is
session-start background only; it is never a replacement for current user input
or higher-priority instructions.

## When to Use

Use this skill when the user asks to preserve continuity, prepare a handoff, or
review what a future session should know.

## Guidance

1. Treat the reseed note as stale reference. Verify important facts against the
   current repository, runtime state, or latest user message before acting.
2. Do not store secrets, credentials, private keys, or raw logs in continuity
   notes.
3. Prefer durable decisions, open questions, current objective, and validation
   status over full transcripts.
4. If the user says the note is wrong or obsolete, explain that the package-owned
   file is under the runtime core's configured `context/reseed.md` path and
   should be edited or regenerated in that core.

## Suggested Note Shape

- Current objective.
- Important constraints and boundaries.
- Decisions already made.
- Open questions or next checks.
- Last known verification status.
