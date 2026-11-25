---
name: task-loop
description: Execute and review tasks through the Phase 4 and Phase 5 loop.
---

# Task Loop (embed into Codex prompts)

**Helpers**: required — task-waves.mjs, context-slice.mjs, flow-state.mjs, scope-check.mjs, requirements-coverage.mjs (helper rule: if a named helper is missing or exits non-zero, stop and tell the user to reinstall the plugin).

## Phase 4 — Execution (Codex)

**Sequential vs parallel**: always run
`node "${CLAUDE_PLUGIN_ROOT}/scripts/task-waves.mjs" .codex-flow/TASKS.md` to compute execution
waves from the `Depends on:` + `Files:` metadata. When it reports width > 1, **parallel mode is the
default**: load `codex-flow:parallel-execution` and follow that skill end to end — worktree +
subagent workflow, clean tracked-baseline gate, serial worktree/control-file setup, reviewed task
commit, wave merge + integration review, and when to stay sequential. Proceed without asking for
waves of ≤3 concurrent tasks; ask the user before a wider wave (N× simultaneous quota). Record each
wave with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set wave <n>` before dispatching it.

For each task in dependency order (sequential mode):

1. Before each `mcp__codex__codex_execute`, run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs" --task T<n>`. If it reports
   `mandatory slice content exceeds tokenBudget`, split the
   oversized task in the backlog before continuing; never raise the slice budget. Immediately
   before the call, record `git rev-parse --short HEAD` as the task's base sha. When `checkpointCommits` is `no`, use the `scope-check.mjs snapshot` tree id instead. In the same durable
   update, set the task's `- Status:` line to `in-progress`, append
   `  - <ISO 8601 ts> pending -> in-progress` beneath it, and write
   `- Session: launching (base: <short sha>)`. Make the Status write and its transition line with
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" task T<n> in-progress`, and run `flow-state set currentTask T<n>` and
   `flow-state set taskStage launching`; once the call is dispatched, run `flow-state set taskStage executing`.
   Complete all of these writes before calling `mcp__codex__codex_execute` with:
   - `prompt`: start with the single header line `Run position: phase execution — task T<n> <title> — next gate: <gate>`, then the opener "Read .codex-flow/CONTEXT-T<n>.md for context (a budgeted slice of PLAN.md; its header records the generation anchor, and blocks marked [verify] must be re-checked against the current code before relying on them)." Then append "Implement task T<n> exactly as specified below, and only this task. Run its acceptance checks before finishing." + the standards, testing, and language blocks from the loaded skills (or the `exec-deliverable` blocks for a non-code task) + a distilled ≤ 30-line rules block per skill in the task's `Skills:` field (see `codex-flow:skill-selection` Step 6 — never paste a whole SKILL.md); do not append the full task text because the slice already embeds it as mandatory content.
   - `cwd`: absolute path of the project root
   - `sandbox`: `workspace-write` by default; `read-only` for investigation-only tasks; `danger-full-access` ONLY when the task genuinely needs network or a global install, and tell the user first.
   - `model` and `reasoningEffort`: pass `model` only when Phase 0's `codex_health.authMode` is `apikey`; otherwise omit `model` and steer with `reasoningEffort` (the server rejects a `model` override under ChatGPT auth). Match effort to complexity — `high` (plus a stronger model where `model` is allowed) for architectural, cross-cutting, or subtle-logic tasks; `low` for small, mechanical, well-specified tasks; omit `reasoningEffort` for standard implementation work (use the CLI default). Note both choices in the Decision log.
   - `timeoutMs`: default 60 min; scale UP for large tasks rather than letting them die. The server auto-resumes within bounded limits, so never retry manually before inspecting `attempts` and `resumeReasons` (see step 2).
   - `terminal`: `true` — opens a live-progress terminal window when supported; progress also streams into the session via MCP notifications
   - `verifyCommand`: the task's exact acceptance check from its `Acceptance:` field (test file/pattern or build command, e.g. `npx vitest run tests/foo.test.ts`). The server runs it in `cwd` after the run settles and returns `verification` (`exitCode`, `passed`, `outputTail`) — deterministic evidence that the check ran, independent of Codex's account. Pass the same `verifyCommand` on every `codex_continue` fix round. Omit only when the acceptance is a manual probe with no command.
2. **Check the returned `status` field** before anything else:
   - `success` → proceed normally.
   - `partial` (not a tool error) → the run ended without a completion marker, or with unparseable
     event lines after any bounded auto-resume, so Codex's account of the run is suspect. Inspect
     `attempts`/`resumeReasons`, `diff`/`attribution`, and the live log; explicitly verify the
     acceptance checks before treating it as done, and ask the user before any manual retry.
   - `failed` / `aborted` (tool error) → inspect `attempts`/`resumeReasons` first; if bounded
     auto-resume was exhausted or the failure was ineligible for it, report it and ask the user
     before any manual retry (quota is not free; never retry silently).
3. **Save the returned `sessionId`** — when `codex_execute` returns, replace the task's launching
   Session line with `- Session: <sessionId> (cwd: <path>, base: <short sha>)`, preserving the base
   recorded before the call. Phase 5 reviews and fix rounds go back into that session. The DEFAULT
   is a fresh `codex_execute` per task; use `codex_continue` for review/fix rounds within the same
   task. Cross-task session reuse is allowed only when the next task directly depends on the
   previous task AND stays in the same domain, and is capped at that one adjacent task — after
   that, start fresh. A fresh session gets the new task's distilled skill blocks instead of inheriting stale context from the previous domain.
4. Keep the task `in-progress` while it is under review and its durable handoff is being written.
   Do not mark it done here; Phase 5 step 7 makes that the last durable task write. When a
   task is abandoned, set `- Status:` to `failed` via `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" task T<n> failed` (the helper appends the
   bare transition line `  - <ISO 8601 ts> in-progress -> failed`; record the session id and reason
   in the Decision log, never as a suffix on that line), then set `taskStage idle` and
   `currentTask -`, and update TaskUpdate. Transition lines are append-only — never rewrite or delete earlier ones.
5. Run Phase 5 review for the task BEFORE starting the next one.
6. When the task passes review, act as the only per-task writer in sequential mode: Phase 5 step 7
   performs the durable completion handoff in the order given there, and only after all of its
   writes succeed may it flip the task to `done`; `done` means the complete durable handoff exists.

## Phase 5 — Review (Claude, per task + final)

At the Phase 4 → Phase 5 boundary, `phase` stays `execution`. Sequential mode: set `taskStage` to
`reviewing` with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set taskStage reviewing`.
Parallel mode: `taskStage` stays `executing` for the whole wave (subagents review inside their
worktrees) and moves to `handoff` only in the coordinator's Step 3.8. `phase: review` is set once,
in step 8, after the last task.

0. Before reviewing, reuse the existing `.codex-flow/CONTEXT-T<n>.md` only when its generated header's anchor equals the current `git rev-parse HEAD` and the tree is clean; otherwise run `node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs" --task T<n>` to regenerate this task's slice, then re-read it and this task's entry in `.codex-flow/TASKS.md`. Treat the files read on disk — not session memory, which may have been compacted — as the source of truth for acceptance criteria, architecture, `Files:` scope, and the known-red baseline. Read full `.codex-flow/PLAN.md` only when a finding disputes plan intent or the slice's omitted-pointer line points at a section the review needs.
1. **Start the Codex-side review in the background FIRST** — it is read-only and independent of your own pass, so never run it after your review: launch a background subagent (Agent tool, general-purpose) whose only job is to call `mcp__codex__codex_review` for THIS task with the focus block from `codex-flow:review-dual` (task id/title, acceptance criteria, `Files:` list) plus `scope: { files: <the task's `Files:` list>, contract: <the PLAN Contracts the task lists> }`, and return the tool result's `reviewFindings` object plus `status` verbatim, nothing else. Do steps 2–4 yourself while it runs; collect its result in step 4. If the Agent tool is unavailable, call `mcp__codex__codex_review` directly at step 4 instead (sequential fallback).
   **Scope trip-wire (mechanical, not judgment)** — in sequential mode, before the Claude review
   pass, run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/scope-check.mjs" --task T<n> --base <base sha> --tasks .codex-flow/TASKS.md`
   with the base sha recorded on this task's `- Session:` line. Exit 0 → proceed. ANY extra path it
   prints — lockfiles, `node_modules`, and `.codex-flow/` are already excluded — is a blocking finding routed through
   step 5, or, when the extra path proves the PLAN declared the wrong `Files:`, the step 6 plan-drift
   transaction; do not review the out-of-scope diff as if it were in scope and do not re-argue the
   task's `Files:` after the fact. Exit 1 with a placeholder or empty `Files:` set is the same
   blocker. Parallel mode gets this from the worktree boundary and `codex-flow:parallel-execution`'s
   undeclared-file stop instead.
   Inspect what Codex did: use the returned `diff` field (git status + patch) and read changed files where the patch is not enough; for diffs over 400 lines follow the `codex-flow:context-discipline` no-raw-read rules.
2. Review in order: conformance → quality → security, per the loaded skills.
3. Read the tool result's `accepted` verdict first (`true` only when the run succeeded AND its
   `verification` passed — or no `verifyCommand` was given; `accepted: false` means treat the task
   as not done until you know why), then its `verification` field: `passed: true` is evidence the task's
   acceptance command ran green in the workspace; `passed: false` (or `skipped`) means the task is
   not done regardless of what `agentMessage` says — quote `outputTail` in the finding. Do NOT
   re-run the full test suite per task — `verifyCommand` is the single authoritative acceptance run;
   the full suite runs once per merged parallel wave (integration review) and once in the
   whole-feature review (step 8), where failures are compared against the **known-red baseline** in
   PLAN.md so only new ones count against the task. Codex's claim is input, not evidence: check the
   result's `commands` list for what actually ran.
4. **Collect the Codex-side review** started in step 1 (wait for the subagent; in the sequential
   fallback call `mcp__codex__codex_review` now with the same focus block and `scope`, which
   restrict the review to this task).
   Read Codex's findings from the result's `reviewFindings` field: when
   `parsed: true`, its `findings[]` and `improvements[]` are the Codex review — do not re-derive severities from the prose; when
   `parsed: false`, tell the user, fall back to the prose `agentMessage`, and treat any severity you
   assign yourself as unverified until checked. `reviewFindings.dropped > 0` blocks acceptance of
   this task: the reviewer MUST read `reviewFindings.droppedReasons` (one ordered reason per dropped
   entry) and report them before treating the review as complete. Re-obtain them in another reviewer
   round or get an explicit user waiver — never reconstruct a dropped entry from the prose, and
   never mark the task done on a review with `dropped > 0`. A finding stamped `inScope: false`
   (counted in `reviewFindings.outOfScopeCount`) is routed to the improvements ledger by default and
   does not block; it blocks only when you verify it affects THIS task's acceptance.
   Compare Claude's and Codex's findings
   per the review-dual comparison protocol (which also carries the buckets, the evidence rule, and
   the AskUserQuestion exceptions), and append non-blocking suggestions from BOTH reviews to
   `.codex-flow/IMPROVEMENTS.md` per that skill; they never block the task. A failed, timed-out, or
   `partial` `codex_review` falls back to Claude-only review per that skill.
5. **If issues found**: route verified CRITICAL/HIGH findings from EITHER review to the task's
   recorded Session line via `mcp__codex__codex_continue` (passing the same `verifyCommand`, see
   Phase 4 step 1, so acceptance re-runs mechanically), never to the fresh reviewer session from
   `mcp__codex__codex_review`, using the review-feedback format (numbered, severity-tagged,
   file:line, expected vs observed). If `codex_continue` fails because the
   recorded session is gone (expired or compacted), fall back to a fresh `codex_execute` fix task
   that embeds the finding text plus the task's `.codex-flow/CONTEXT-T<n>.md` slice; never hand-edit
   Codex's code (the only exception is the after-3-rounds hand-fix in `codex-flow:review-feedback`). The fallback `codex_execute` also passes the same `verifyCommand`. Then re-review. Repeat up to 3 rounds per task.
6. **Plan drift**: when a finding traces to the PLAN being wrong (wrong architecture, missed
   requirement) rather than Codex mis-implementing it, do NOT burn review rounds. Run this
   plan-change transaction before execution resumes: FIRST run `flow-state plan-drift` → amend PLAN.md
   with user approval → write an impact analysis listing which done and pending tasks the change
   touches → update the affected
   TASKS.md `Steps` / `Files` / `Requirements` / `Acceptance` fields → re-run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/requirements-coverage.mjs" --requirements .codex-flow/REQUIREMENTS.md --tasks .codex-flow/TASKS.md --plan .codex-flow/PLAN.md`
   plus the `plan-backlog` backlog sanity checks → regenerate affected slices → recompute waves →
   get backlog re-approval → only then run `flow-state approve backlog` then `flow-state advance`. Improvement
   tasks appended at the improvement decision gate go through the same mini-transaction — impact analysis,
   coverage lint, backlog sanity checks, re-approval, then `flow-state approve backlog` and `flow-state advance` — before they are scheduled.
7. **If clean**: complete the durable handoff while the task remains `in-progress`. In sequential
   mode first set `taskStage handoff` with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set taskStage handoff`
   (parallel mode does this once per wave in Step 3.8).
   **Sequential mode**: append the Decision-log schema block, append this
   task's section to the report dir's `tasks.md`, append its dual-review record to `reviews.md`, then run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs" --check-plan` and fix the block before
   the next task if it exits non-zero, and
   make the checkpoint commit when enabled. When a task is dropped or abandoned, record it with
   `Result: dropped` at the moment of that decision. After every required write succeeds, update
   TaskUpdate, then make the LAST durable task write: set `- Status:` to `done` via
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" task T<n> done`, which appends the bare transition line
   `  - <ISO 8601 ts> in-progress -> done` (the session id lives on the task's `- Session:` line and
   in the Decision log, never as a suffix), then set `taskStage idle` and
   `currentTask -`. With the full durable handoff and final status transition on disk, take the
   `codex-flow:context-discipline` sequential-task compaction point, then move to the next task.
   **Parallel mode**: follow `codex-flow:parallel-execution`'s wave workflow — always commit each
   passed worktree task, and after the wave merge and passing integration review the coordinator
   appends the schema blocks, then runs
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs" --check-plan` and fixes blocks before the
   next wave, and takes the wave compaction point.
