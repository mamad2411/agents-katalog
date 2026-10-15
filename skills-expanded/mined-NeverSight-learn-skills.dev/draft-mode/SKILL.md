---
name: draft-mode
description: >-
  Fast iteration mode: after code changes, do not commit, run git, builds,
  tests, lints, typechecks, dev servers, or browser verification unless the
  user explicitly asks in that message. Use when the user says "draft mode",
  "draft-mode", "/draft-mode", or wants to iterate quickly without automatic
  verification after every edit.
---

# draft-mode

Stay in this mode for the rest of the conversation until the user says to stop (e.g. "stop draft mode", "exit draft mode", "normal mode").

## Goal

Enable a fast feedback loop. The human decides when to verify. Do not slow them down by running builds, tests, or other checks after every edit.

## Banned by default

After making code changes, **do not** run any of the following unless the user explicitly asks for that action **in the same message**:

- Git: `commit`, `push`, `pull`, `fetch`, `merge`, `rebase`, `checkout`, `branch`, `stash`, `add`, `status` (for staging/commit flow), or any other git write/operation
- Builds / compile / bundle
- Tests
- Linters / formatters / typechecks
- Dev servers / watchers
- Browser-based verification (navigate, screenshot, snapshot, click-through)

Also do not offer or propose running these as a next step after edits.

## Explicit ask = one-time only

If the user asks for a banned action in a specific message:

1. Do that action **once** for that message.
2. Treat it as **not** standing permission.
3. After the next code change, return to the banned-by-default rules above.

Standing permission requires an explicit ongoing grant (e.g. "always run tests after changes" or "exit draft mode").

## Still allowed

- Edit files
- Read files, search, explore the codebase
- Ask clarifying questions
- Summarize what changed

## After edits

Stop when the change is done. Brief summary of what changed is fine. No verification ritual.
