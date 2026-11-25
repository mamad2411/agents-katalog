---
name: verify-opencode-work
description: Independently verify a finished OpenCode worker task via diffs, tests, and evidence before accepting it.
---

# Verify OpenCode Work

Use when a worker reports `idle`. Never trust only the worker summary.

## Verify in worker profile

- Call `worker_verify` first: it re-checks state and evidence without side effects.
- Then inspect the exact diff yourself with the boss host's own filesystem and
  terminal tools (read the changed files, `git diff`). Check scope: only intended
  files touched, no secrets, no stray artifacts.
- Run proportionate checks with the host's own tools: at minimum the repo's fast
  tests/lint for the touched area; full suite before merge. See `AGENTS.md` for commands.
- Confirm acceptance criteria from `delegate-to-opencode` one by one. Missing criteria means the task is not done.
- Treat `error` state or an error flag in the latest output as failure even if the text sounds confident.
- `get_diff` (with the worker `taskID`, optional `messageID`, and `directory`) is a
  full-profile legacy option only. It never replaces reading the diff and running checks.

## Report

- Done: list files changed, checks run with results, and remaining follow-ups.
- Not done: say exactly which criterion failed, with file/line or command output as evidence, then re-scope or retry.
