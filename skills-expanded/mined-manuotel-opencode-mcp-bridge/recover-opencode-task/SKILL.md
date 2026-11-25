---
name: recover-opencode-task
description: Diagnose and recover unknown, error, or stuck OpenCode worker tasks safely without duplicate side effects.
---

# Recover OpenCode Task

Use when `worker_status` returns `error` or `unknown`, output stalls, or the directory looks wrong.

## Diagnose first

- `unknown` usually means wrong `directory` or a gone session. Re-check once with `worker_status` using the exact `directory` returned by `worker_run`.
- `error` means the latest assistant message carries a provider error. Read `output` before retrying; the fix may be the prompt, not the infra.
- Stuck (`running` with no output growth): prefer one bounded `worker_wait` (default 30s, clamped 1-120) to wait for a change server-side instead of client sleep loops. Re-check with `worker_status` plus `include_output=false` to confirm state cheaply, then decide. `worker_verify` stays the evidence gate before accepting recovered work.

## Act safely

- Directory mismatch: fix the directory, do not launch a second worker for the same task.
- Retry: fix the cause, then `worker_run` again once. Never fire parallel retries of the same task; duplicates cause duplicate side effects.
- Abort/delete: use `worker_cleanup(action=abort)` for a live stuck session and
  `worker_cleanup(action=delete)` only when the task is abandoned. Only the given `taskID` is ever touched; unrelated sessions are never listed or killed. Cleanup deletes
  session data and cannot be undone. `abort_session` / `delete_session` are legacy
  equivalents for the full profile only.
- Approval states: `approval_required` needs `worker_decide`, `approved` needs `worker_resume` (same message, exact-once), rejected or expired needs a fresh `worker_run`.

## After recovery

- A recovered task restarts at `delegate-to-opencode` (re-scope) and must pass `verify-opencode-work` before it counts as done.
