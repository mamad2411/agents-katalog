---
name: delegate-to-opencode
description: Scope and launch an async OpenCode worker task with free-model defaults, acceptance criteria, and bounded server-side waiting.
---

# Delegate to OpenCode

Use when the boss hands work to a background worker instead of doing it inline.

## Scope the task

- One task, one worker. State: goal, repo path, branch/worktree, files in scope, files off limits.
- Write acceptance criteria: observable checks (tests, commands, diff shape). No vague "make it better".
- Pick the model: start with free default `opencode/muse-spark-1.3-contributor-free`
  (provider `opencode` + model `muse-spark-1.3-contributor-free`).
- If model availability is uncertain, call `worker_catalog` first (defaults already
  filter to free + connected) and record the selected provider/model in the report.
- Ordered fallback, one retry only: if the free model is missing/unavailable in
  `worker_catalog`, or `worker_run` cannot start because that model/provider is
  unavailable, retry the same scoped task once with paid fallback
  `opencode-go/muse-spark-1.3-contributor` (provider `opencode-go` + model
  `muse-spark-1.3-contributor`, `recommendations[1]`). Never use Copilot or any
  other paid model.
- This paid fallback is pre-authorized by the product owner for this project only when
  the free default is unavailable; it is not a general permission to spend. The bridge
  never auto-switches to paid; the coordinator performs one explicit fallback `worker_run`
  after confirming the free model is unavailable.
- Do not switch models after a worker has started, and never launch parallel duplicate
  retries. Catalog/start unavailability is distinct from task failure after start: once
  started, follow `recover-opencode-task` (inspect `worker_status`/`worker_wait` output
  first, never silently retry after a possible worker-side partial mutation).

## Launch

- Call `worker_run` with `message`, `directory`, and `title`. Save the returned `taskID`, `modelID`, and `directory`.
- Always pass that same `taskID` and `directory` to every later `worker_*` call. Status and messages are directory-scoped; a wrong directory reads as `unknown`. When `directory` is omitted, the saved task record supplies it.
- Do not pass `providerID` without `modelID` (or vice versa). The pair must be given together or omitted.
- Stay on `/worker-mcp`: the eight worker tools only (`worker_catalog`, `worker_run`, `worker_wait`, `worker_status`, `worker_verify`, `worker_cleanup`, `worker_decide`, `worker_resume`). It never exposes `exec_run`; use `/mcp` only for legacy compat. See `docs/tool-api.md`.

## Poll async

- Prefer bounded `worker_wait` (`timeout_s` default 30, clamped 1-120) for progress; it returns on state or message change or at the deadline with `timed_out=true` and `next_action="worker_wait"` to call again. No client sleep loops.
- Use `worker_status` for an immediate snapshot only (after a timed-out wait, after an error, or for one quick look). States: `running` (wait again), `idle` (inspect output), `error`/`unknown` (see `recover-opencode-task`).
- Follow the stable contract: `taskID`/`state` plus `retryable`/`next_action`/`error_code`/`evidence`. Do what `next_action` says. Field shapes live in `docs/tool-api.md`.
- Keep `include_output` true and the default cap unless output is huge. Never dump full history; `worker_status`/`worker_wait` return latest assistant text only. Use `include_output=false` for a cheap state-only check.
- When `idle`, move to `verify-opencode-work`. Never report success from the worker summary alone; `worker_verify` stays the evidence gate.

## Approval-gated work

- `worker_run` with `requires_approval=true` or a `risky_action` pauses as `approval_required` (an `apr_` `taskID` plus `approval_token`). No session is created and no prompt is sent until decide plus resume.
- `worker_decide` approves or rejects without starting work. `worker_resume` with the same `message`, `taskID`, token, and matching `directory` starts the deferred worker exactly once; duplicates or mismatches fail safely with no second session.
- Rejected or expired approvals need a fresh `worker_run`; approved needs `worker_resume`, never a second `worker_run`.
