---
name: parallel-execution
description: Run a codex-flow backlog faster by executing independent tasks concurrently — compute dependency/file-disjoint waves from TASKS.md, give each parallel task its own git worktree (codex-mcp serializes per cwd but parallelizes across cwds), run a Claude subagent per worktree, then merge and integration-review each wave. Use by default when task-waves reports width greater than 1; proceed without asking for waves of up to 3 concurrent tasks and ask only before a wave exceeds 3 because of simultaneous quota cost.
---

# Parallel Execution (default when wave width > 1)

**Helpers**: required — task-waves.mjs, flow-state.mjs, context-slice.mjs, worktree-setup.mjs, requirements-coverage.mjs (helper rule: missing → STOP and tell the user to reinstall the codex-flow plugin; non-zero exit → surface the error and STOP).

codex-mcp serializes runs per `cwd` (to prevent file/git races) but runs different `cwd`s in
parallel. So real parallelism = **one git worktree per concurrent task**, each driven by its own
Claude subagent calling `codex_execute` into that worktree.

## Control-file ownership

The coordinator is the SOLE writer for every `.codex-flow/*` file, including TASKS.md, PLAN.md,
STATE.md, REQUIREMENTS.md, report directories, IMPROVEMENTS.md, and notes. Worktree subagents treat
those durable control-file copies as read-only inputs. They may regenerate derived context slices
inside their own worktree copies only; every durable update flows through the structured handoff
to the coordinator.

## Default-on policy

- Always run the wave tool below during Phase 4. When it reports width > 1, use parallel mode by
  default if the project is a git repo, its tracked baseline is clean, and the user has not opted
  out.
- Proceed without asking for waves of **≤3 concurrent tasks**. Show the user the wave plan, then
  start the wave.
- When a wave exceeds **3 concurrent tasks**, ask whether to run at that width or lower the cap
  before spawning; parallel execution burns N× simultaneous quota.
- Stay sequential when the tool reports "fully sequential", the user opted out, the project is
  not a git repo, the tracked baseline cannot be made clean, or the worktree canary fails.

## Step 1 — Compute waves

`node "${CLAUDE_PLUGIN_ROOT}/scripts/task-waves.mjs" .codex-flow/TASKS.md`

This helper and the `context-slice.mjs` call in Step 2 are both fail-closed.
If the helper is not found, STOP and tell the user to reinstall the codex-flow plugin (its scripts/ directory is required); if it is present but exits non-zero, surface the error to the user and STOP. Never edit control files by hand.

A **wave** is a set of tasks that can run at once: every task's dependencies are satisfied by
earlier waves, and no two tasks in the wave touch the same file (`Files:` field). Tasks with no
declared files run alone (unknown blast radius). The tool prints each wave and its width; a wave
of width 1 just runs like normal Phase 4.

Wave quality is only as good as the backlog metadata: accurate per-task `Files:` sets (from PLAN.md's
**Component → files** map) and fixed **Contracts** are what make concurrent tasks genuinely
independent. If tasks were sliced with vague file lists, fix the backlog before parallelizing —
don't parallelize on guesses.

Show the wave plan to the user before spawning anything. For waves of width ≤3, this is a status
update, not an approval gate.

## Step 2 — Per wave: spawn a subagent + worktree per task

Before wave 1, run `git worktree add --detach <tmp> HEAD`, then `git worktree remove --force <tmp>`. If the canary fails, set `executionMode` to `sequential (worktrees unavailable: <error>)` with `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set executionMode "sequential (worktrees unavailable: <error>)"` and run sequentially; never discover this mid-wave.

**Hard precondition:** parallel mode requires a clean tracked baseline, with every accepted project
change the tasks depend on committed at the branch point. If Phase 0 accepted a dirty baseline,
commit the required changes and stash unrelated residue before continuing, or stay sequential.
The untracked `.codex-flow` control files are copied separately below.

For each task in the wave (width > 1):

1. Create isolated worktrees **serially**, never with concurrent `git worktree add` calls. Cloud-
   synced filesystems such as OneDrive can fail concurrent creation with `mmap failed`. Use the
   `Agent` tool with `isolation: "worktree"`
   (or `EnterWorktree`). Each worktree is a distinct `cwd`. Branch point depends on the wave:
   - **Wave 1**: branch from the CURRENT integration branch HEAD, which includes the Phase-2
     `docs(agents)` commit.
   - **Wave N (N>1)**: branch from the CURRENT integration branch HEAD — i.e. only after wave
     N−1 has been merged and its wave integration review/tests passed (Step 3). Branching later
     waves off the baseline would run them on stale code missing earlier waves' merged output.
   The Phase 0 baseline ref is kept for audit, rollback, and the final-review diff only — never as
   a worktree branch point.
2. After creating each worktree, the coordinator MUST copy the untracked control files into it:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/scripts/context-slice.mjs" --task T<n>
   node "${CLAUDE_PLUGIN_ROOT}/scripts/worktree-setup.mjs" --worktree <worktree> --task T<n>
   ```

   Generate the task's `.codex-flow/CONTEXT-T<n>.md` immediately before copying it alongside
   PLAN.md and TASKS.md. When the task's `.codex-flow/SKILLS-T<n>.md` sidecar exists, copy it into
   the worktree alongside the context slice.
   If either command exits non-zero, surface the error and do NOT dispatch the subagent.
   If generation reports `mandatory slice content exceeds tokenBudget`, split the oversized task
   in the backlog and recompute the waves before continuing; never raise the slice budget.
   Treat these copies as coordinator-owned context: subagents read them but do not include them in
   task commits; the coordinator updates the integration copies in Step 3.
3. In each subagent, run the **Phase 4 execution mechanics** for its ONE task: embed the standards +
   the task's `Skills:` blocks, call `codex_execute` with that worktree as `cwd`, pick `model` by
   task complexity, and save the `sessionId`. Skip every control-file write prescribed by Phase 4:
   no TASKS.md, STATE.md, report, ledger, or Decision-log writes.
4. At dispatch time, before launching the batch, the coordinator marks every wave task
   `in-progress`, appends its pending-to-in-progress transition (both via
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" task T<n> in-progress`), and writes
   `- Session: launching (base: <short sha>, worktree: <path>, branch: <name>)` using that
   worktree's branch-point base sha, path, and branch. Parallel-mode STATE.md convention:
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set wave <n>` names the wave and `currentTask` stays `-`
   (several tasks run at once); the wave's stage sequence is `executing` (whole wave) → `handoff`
   (Step 3.8) → `idle`; per-task `reviewing` is not used in parallel mode.
5. After the serial worktree setup, control-file copies, and coordinator dispatch records finish,
   launch the subagents concurrently in a single batch.

Because each `cwd` differs, the per-workspace concurrency guard allows all of them at once.

## Step 3 — Per wave: review, then merge

1. Each subagent runs the **Phase 5 review mechanics** (conformance → quality → security) inside its
   worktree; a task that does not pass escalates as a blocker. Skip every control-file write that
   Phase 5 prescribes: no TASKS.md, STATE.md, report, ledger, or Decision-log writes. A subagent may
   regenerate derived slices inside its worktree copy only.
2. After review, each subagent returns a structured handoff containing: task id; sessionId; actual
   files changed; checks run with results; review findings and resolutions; a proposed Decision-log
   block; and proposed improvement entries. The handoff proposes control-file content but never
   edits the durable worktree copies; all durable updates flow through this handoff to the
   coordinator. IMMEDIATELY when each handoff arrives, before any merge or wave integration review,
   the coordinator replaces that task's `launching` Session line with its real sessionId while
   preserving the base, worktree path, and branch. Do not wait for the rest of the wave.
3. After review passes, each subagent MUST commit its task changes on the worktree branch as
   `wip(codex-flow): T<n> <title>`, regardless of the Phase-3 checkpoint-commit choice. This commit
   is required to transport the work back and can be squashed at delivery; exclude the copied
   `.codex-flow` control files. Only then does the subagent report the branch ready to merge.
   - Task commits MUST stage explicit paths (never `git add -A`) because coordinator-owned
     worktree artifacts — the `node_modules` symlink and copied `.codex-flow` control files — can
     escape gitignore rules. A symlink named `node_modules` is not matched by `node_modules/`.
4. Before merging each worktree, the coordinator diffs the worktree's actual changed files against
   the task's declared `Files:`. Any expansion — a changed file outside that declaration, excluding
   generated lockfiles explicitly listed as shared — stops the wave. As the FIRST step of this
   backlog-mutating transaction, run `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" plan-drift`. Only then update the task's `Files:` in TASKS.md, re-run
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/requirements-coverage.mjs" --requirements .codex-flow/REQUIREMENTS.md --tasks .codex-flow/TASKS.md`
   plus the `plan-backlog` backlog sanity checks, and get user re-approval. Only after re-approval,
   run `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" approve backlog` then `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" advance` to restore execution. Then RE-RUN
   the task's conformance → quality → security review over the EXPANDED `Files:` scope, using a
   fresh `codex_review` or a Claude pass, before the branch may merge. The security review is
   mandatory when the expansion touches auth, input, queries, files, or secrets.
5. Before merging, the coordinator verifies the task branch is ahead of its branch-point base
   (`git rev-list --count <base>..<branch>` must be greater than zero). A zero-commit branch is a
   failed task, not a branch to merge.
6. The coordinator merges each passed, verified worktree branch back into the integration branch
   **in task order**. Resolve conflicts here — they should be rare because the wave is
   file-disjoint, but dependency-driven edits to shared files across waves can still collide.
7. After merging the whole wave, run a **wave integration review**: full test suite on the merged
   result + a quick end-to-end probe. Branches never saw each other, so a green-in-isolation task
   can still break in combination — this pass is mandatory, not optional.
8. After each wave, first set `taskStage handoff` with
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set taskStage handoff`, then the coordinator serially applies the remaining structured handoffs:
   Decision-log appends, report entries, and IMP-id allocation in IMPROVEMENTS.md. Serial IMP-id
   allocation prevents duplicate ids. For each passed task, append one schema block (see
   `plan-architecture`) and write its report entries. Append one wave-integration event block using
   that skill's event schema. Only after every required handoff and event write succeeds, make each
   task's `Status: done` transition as the last durable task write via
   `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" task T<n> done`, then set `taskStage idle`. Follow `context-discipline` to
   declare the safe wave-boundary
   compaction point, then compute the next wave (dependencies of later tasks are now satisfied).
   The next wave's worktrees branch from the integration branch HEAD as it stands now — post-merge,
   post-review — so they build on this wave's output.

## Step 4 — Final integration

After the last wave: whole-feature review + full suite + end-to-end verification (same as
sequential Phase 5 step 8), then summarize. Offer to squash the per-task/per-wave commits.

## Rules & failure handling

- Never parallelize tasks that share a file — the wave tool already prevents this; do not override.
- If a subagent's task fails after 3 review rounds, quarantine it: keep the rest of the wave,
  report the failure, and ask the user before retrying (quota is not free).
- If a merge conflict is non-trivial, first record it durably with
  `node "${CLAUDE_PLUGIN_ROOT}/scripts/flow-state.mjs" set taskStage merge-conflict`, then stop and surface it — do not let a
  subagent force-resolve another task's code. A resume that finds `taskStage: merge-conflict`
  surfaces the conflict to the user and STOPs.
- Never spawn more than **10 subagents at once** — the wave tool already caps each wave at 10
  (`--max <n>` to lower it) and flows the rest into the next wave, so a very wide backlog is split
  into consecutive ≤10 waves. Lower the cap when quota or review load is tight.
- Keep parallel mode ON by default when Step 1 shows width > 1. Waves of width ≤3 need no opt-in;
  ask only before running a wave at width >3. Stay sequential for the exceptions in the
  Default-on policy.
