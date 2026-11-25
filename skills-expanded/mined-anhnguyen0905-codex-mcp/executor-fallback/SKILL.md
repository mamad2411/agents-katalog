---
name: executor-fallback
description: Keep a codex-flow run alive when Codex cannot execute — outage triggers, the single explicit AskUserQuestion switch at a task boundary, STATE.md and Decision-log recording, Phase 4 and Phase 5 with Claude as executor plus an independent subagent review, returning to Codex, and the fast-path small-change lane under fallback.
---

# Executor fallback — Claude executes when Codex is unavailable

Codex is the default executor. When it cannot run, the flow does not die: the user chooses once,
explicitly, between fixing Codex and letting Claude execute. The planning, approval, review, and
reporting contract stays identical; only WHO writes the code changes.

**Triggers** (any one):
- Phase 0: `mcp__codex__codex_health` tool call fails, the server is missing, `loggedIn: false`, or
  the deep call's `execProbe` is `quota`, `model`, or `error`.
- Mid-run: a `codex_execute` / `codex_continue` / `codex_review` returns `failed` or `aborted` with
  no `sessionId`, or its `errors`/`stderr` indicate authentication, quota exhaustion, or an
  unreachable service. No health re-check is required: an `execProbe` of `quota` or `model`, or a
  run error carrying those signatures, is sufficient on its own to open the fallback decision.
- Mid-run: the same task exhausts bounded auto-resume twice in a row (`attempts`/`resumeReasons`).

**Decision** — use AskUserQuestion exactly once per outage with two options: **Fix Codex and
re-check** (recommended when the user can log in or restore service now) or **Continue with Claude
as executor**. Never switch executors silently, and never switch mid-task: finish or reset the
current task first (per the preflight in-progress reconciliation), then switch at the task boundary.

**Recording** — STATE.md carries `executor: codex` by default. On fallback set
`executor: claude (fallback: <not-logged-in | server-missing | codex-unavailable> <ISO 8601>)`;
on return set `executor: codex (restored <ISO 8601>)`. Record each switch once in PLAN.md's
Decision log using the non-task event-block schema from `codex-flow:plan-architecture`.

**Phase 4 under fallback** — for each task in dependency order, sequential mode only:
- Generate and read the task's `.codex-flow/CONTEXT-T<n>.md` slice exactly as for Codex, and apply
  the loaded `exec-coding-standards`, `exec-self-testing`, language, deliverable, and distilled
  domain-skill blocks to your own work — they bind Claude the same way they bind Codex.
- Perform the same durable pre-launch writes, but write `- Session: claude-fallback (base: <short sha>)`.
- Implement ONLY this task, within its `Files:` scope. Run the task's acceptance command yourself
  and record `- Verification: <command> → exit <code>` in the task's report entry; this replaces
  the server-side `verification` field.
- Parallel worktree mode is not available under fallback; when `task-waves` reports width > 1,
  still run sequentially and note it in the Decision log.

**Phase 5 under fallback** — Claude must not grade its own homework alone:
- Replace `mcp__codex__codex_review` with an independent review by a fresh subagent (a code-review
  agent, or a general-purpose agent with the review skills), given the same focus block from
  `codex-flow:review-dual` (task id, acceptance criteria, `Files:` list, review order).
- Run your own conformance → quality → security pass as usual, then apply the review-dual
  comparison protocol to the two reviews.
- Fix verified CRITICAL/HIGH findings directly (there is no Codex session to route them to), re-run
  the task's acceptance checks after every round; the full suite runs once in the whole-feature review. Keep the 3-round cap; after 3 rounds,
  stop and re-plan the task with the user.
- Report PIC for a fallback task is `claude (fallback: <reason>)` per `codex-flow:session-report`;
  `cost.md` reports measured Codex cost for the run's Codex tasks only and says so.

**Returning to Codex** — at any task boundary, when the user says Codex is available again, re-run
`mcp__codex__codex_health` with `{ deep: true }`; on `loggedIn: true` with `execProbe: ok` restore `executor: codex (restored <ISO 8601>)` and
run the remaining tasks through Codex normally. Tasks completed under fallback keep their
`claude-fallback` Session line and are never re-executed.

**Fast-path small-change lane under fallback** — allowed: Claude implements the ≤ 2 files itself
under the same embedded blocks, runs the lane's known-red comparison, and gets the independent
subagent review in place of the skipped `codex_review`. Log `session=claude-fallback` in
`fastpath.log`.
