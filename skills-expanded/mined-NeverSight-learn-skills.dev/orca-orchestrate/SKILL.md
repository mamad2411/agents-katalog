---
name: orca-orchestrate
description: >-
  Orca orchestration coordinator runbook for orchestrator sessions only: bind the
  Run created by /orca-tasks, dispatch ready tasks one-worktree-one-branch, drive
  the task DAG, sweep and resolve pending decision gates, watchdog check --wait with
  a bounded escalation ladder, merge work that satisfied the setup marker's merge
  gate, and release workers without leaking terminals. Also has a quick path for 1-2
  task runs without a plan. Invoke with /orca-orchestrate.
disable-model-invocation: true
argument-hint: "Objective of the run?"
---

# Orca orchestration runbook

Drive a supervised multi-agent run on Orca from the orchestrator cockpit. The orchestrator is
the DAG driver: it dispatches only ready tasks, watches every worker settle with `worker_done`,
unblocks dependents only after their parent's green PR is merged, and gates on failures. It
never schedules workers itself — Orca does not infer placement or conflicts. The agents choose
placement; the orchestrator decides *what* runs *when*.

Re-orient first if you are in a fresh session (`/orca-resume`). Confirm the worktree guardrail
first: you must be in the **primary worktree** (see `/orca-setup`) — never coordinate from a
task branch.

## Two entry paths

- **Planned run** (recommended): `/orca-plan` → `/orca-tasks` produced a Run and its Tasks. You
  **bind** that Run and drive it.
- **Quick path**: a small 1-2 task job that skipped planning. `run-create` + `task-create`
  directly from the objective, then drive identically.

## Load the guides before any command

```text
orca skills get orchestration
orca skills get orca-cli
```

Read them before running anything. Prefer `--json` for agent-driven calls. Never guess
subcommands or flags from memory.

## Pre-flight

1. Verify the primary worktree: `orca worktree current --json` → `isMainWorktree` must be
   `true`, or the run is being coordinated from a task branch. Stop and move to the cockpit
   worktree if not.
2. Verify the setup marker exists (`docs/agents/setup.md`), else route to `/orca-setup`. Read
   its `## Merge gate` section now and keep it in mind for the whole run — it is what every
   `succeeded` report will be checked against. A marker with no merge gate predates this
   contract: re-run `/orca-setup` rather than inventing one mid-run. Read `## Worker runtime` at
   the same time — it decides which launch recipe in `runtimes.md` you will use for every
   dispatch, and a run whose default runtime is `freebuff` cannot be left unattended at all.
3. Bind the Run (planned path):
   ```bash
   orca orchestration run-use --id <run_id> --json
   ```
   or create it (quick path): `orca orchestration run-create --objective "<objective>" --json`.

## The DAG loop

Each turn of the loop is **sweep ready → sweep gates → dispatch → wait → settle**. The gate sweep
is not optional: a gate you opened blocks a task until you resolve it, so a loop that only ever
creates gates deadlocks the DAG by construction.

1. **Sweep** — first what is waiting on you, then what is ready to run:
   ```bash
   orca orchestration gate-list --run <run_id> --status pending --json
   orca orchestration task-list --run <run_id> --ready --json
   ```
   **Resolve every pending gate before dispatching more work.** Put the question to the user,
   then close it with their decision:
   ```bash
   orca orchestration gate-resolve --id <gate_id> --resolution "<the user's decision>" --json
   ```
   Never leave a gate pending across a wait window. An unresolved gate and a stuck worker look
   identical from the outside, and only one of them is your own doing.

   Every `ready` task has all its blockers merged on `main`. Dispatch each ready task to a
   worker in its own worktree — **one task = one branch = one worktree**, never the primary.

   **Pick the runtime, then create the worktree, launch the terminal, and bind the dispatch.** The
   runtime is the coding agent that executes the task — `opencode`, `claude-code`, or `freebuff` —
   and it is **independent of whichever agent you are orchestrating from**. Take the default from
   `docs/agents/setup.md` (`## Worker runtime`), overridden by the task's `runtime:` in the plan.
   **The exact launch command per runtime is in [`runtimes.md`](runtimes.md), next to this file.**
   Read it rather than reconstructing a command here — each runtime has a trap (opencode's broken
   `-a`, Claude Code's profile-vs-TUI distinction, freebuff's missing agent entirely).

   The shape is the same for all three:
   ```bash
   # independent (no blockers) → top-level worktree; dependent → child worktree
   orca worktree create --name <slug> --no-parent --setup run --json
   # or: orca worktree create --name <slug> --parent-worktree active --setup run --json
   orca terminal create --worktree id:<newWorktreeId> --title <slug> --command "<per runtimes.md>" --json
   orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 60000 --json
   orca orchestration worker-start --task <task_id> --terminal <handle> --worktree id:<newWorktreeId> --json
   ```
   `freebuff` is the exception at the last step: it is not a recognised agent, so `worker-start`
   and `dispatch --inject` refuse it and the coordinator drives it by hand — follow `/orca-freebuff`
   end to end for that runtime, including verifying the work and signing the `worker_done` yourself.

   Use a fresh terminal per worker (one worktree = one branch = one worker). Reuse a worker
   terminal only for an immediate follow-up Task on the same worktree, and only when the plan
   allows it. Tasks the plan marked `isolated: no` are the sole exception to the worktree rule —
   they run in the primary worktree and must be declared before dispatch.

   Note: the bare `worktree create` above (no `--agent`) may open a fallback shell alongside the
   later `terminal create`. Target only the agent handle; close a fallback shell only after
   `orca terminal list --worktree id:<id> --json` confirms it is an unused shell.

   **Never take the `worker-start --agent <tui>` shortcut to skip `terminal create`.** `--agent`
   launches a known TUI app; it does **not** select the permissive `worker` profile, so the run
   stalls on permission prompts nobody is watching.
2. **Wait** in rolling windows and process every message before acknowledging:
   ```bash
   orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
   ```
   A timeout or `{count:0}` is a checkpoint, not a worker failure. Keep waiting until every
   dispatch settles; workers routinely run 15-60 minutes.
3. **On each `worker_done`**, settle it before acknowledging the Delivery:
   - `succeeded` → **check how it was verified before you merge.** Read `## Merge gate` in
     `docs/agents/setup.md` and confirm the report matches it: under `ci: github-actions` the PR
     must show at least one check and all green (`gh pr checks <pr>` — `no checks reported` is a
     failed gate, not a pass); under `ci: local <command>` the `worker_done` body must quote that
     command's result; under `ci: unverified` there is nothing to check and the merge is the
     user's accepted risk. A `succeeded` that does not name its evidence is not a pass — ask the
     worker (`orca orchestration reply`) or gate it, do not merge on trust.
     Once the gate holds, **merge** the task branch, then clean up the task worktree, then
     re-sweep:
      ```bash
      # github tracker: merge the PR (auto or via the user's review gate)
      gh pr merge <pr_number> --squash --delete-branch
      # local-only (linear tracker, no remote): merge the branch into main in the cockpit
      #   git merge --squash <task-branch> && git push (if a remote exists)
      orca orchestration worker-release --dispatch <dispatch_id> --json
      orca worktree rm --worktree <task_worktree_id> --force --json
      # linear tracker: move the linked issue to Done explicitly — merge does not do it
      #   orca linear status set <issue_key> --to "Done" --workspace <workspace_id> --json
      ```
      Merging unblocks dependents: after cleanup, run `task-list --ready` again and dispatch
      what is newly ready. The worker merged nothing itself — the coordinator owns the merge.
      An `external_terminal` worker stays live after `worker-release`: close it with
      `orca terminal close --terminal <handle>` (see hard-won notes).
   - `failed` → **never redispatch silently.** Mark the task failed, block its dependents, and
     raise a decision gate to the user:
     ```bash
     orca orchestration task-update --id <task_id> --status failed --json
     # dependents are blocked by the failure — surface them via gate
     orca orchestration gate-create --task <dependent_id> --question "<task> failed; retry bounded (worker-start --retry-of), fix forward, or abandon?" --options '["retry","fix-forward","abandon"]' --json
     ```
     The recommended option is a single bounded retry: create a fresh worktree/terminal (same
     recipe as step 1) and bind `worker-start --task <id> --terminal <handle> --worktree <sel> --retry-of <failed_dispatch_id> --json`. Your call through the gate decides.
4. Acknowledge only after every message and release/merge/gate decision is handled:
   ```bash
   orca orchestration check --ack <delivery_id> --wait --types worker_done,escalation,question --timeout-ms 900000 --json
   ```
5. Repeat until `task-list` shows every task `completed` and no dispatch is unsettled.

## Watchdog: worker finished but no worker_done

A worker can finish its work and idle at the prompt without sending `worker_done`. When a wait
window times out, inspect each unsettled dispatch instead of waiting blindly:

1. `orca orchestration worker-read --dispatch <id> --json` and
   `orca terminal wait --terminal <handle> --for tui-idle --timeout-ms 60000 --json`.
2. If the worker is idle and its last message shows the work done (branch pushed, CI green, PR
   ready, final summary) but no `worker_done` arrived, re-inject the finalization from the
   worker's own terminal — the authority must come from there:
   ```bash
   orca terminal send --terminal <handle> --text 'orca orchestration send --type worker_done --subject "<status>" --body "<done, found, left>" --task-id <task_id> --dispatch-id <dispatch_id> --outcome succeeded --files-modified "path/a" --json' --enter --json
   ```
   then continue `check --wait`.
3. If it still does not settle, recover manually:
   `orca orchestration task-update --id <task_id> --status completed` then
   `orca orchestration worker-release --dispatch <dispatch_id> --json`.

Never stop, close, or kill a worker because of a timeout, TUI idle, heartbeat, or status — those
mean alive, not done. Never leave a settled worker live: reuse, retain only at the user's
request, or `worker-release`.

## Escalation ladder for a worker that will not settle

"Never kill on a timeout" is right, but it is not a plan — without a ceiling a stuck dispatch
waits forever and the run looks healthy. Give each task a **time budget** (the plan's `budget:`
field, default 60 min) and climb one rung at a time:

1. **Under budget** — keep waiting. Rolling `check --wait` windows; a timeout is a checkpoint.
2. **Budget exceeded** — run the watchdog above (`worker-read` + `terminal wait --for tui-idle`).
   If the work is visibly done, re-inject the finalization from the worker's own terminal.
3. **Still unsettled after the watchdog** — this is now a decision for the user, not a judgement
   call for you. Raise a gate with the evidence (last output, elapsed time, branch state):
   ```bash
   orca orchestration gate-create --task <task_id> --question "<task> has run <elapsed> past its <budget> budget and will not settle; last output shows <summary>. Wait longer, stop the worker, or abandon the dispatch?" --options '["wait","stop","abandon"]' --json
   ```
4. **Only on the user's decision** — `orca orchestration worker-stop --dispatch <id>` (fences the
   dispatch and stops its terminal) or `worker-abandon` (fences without claiming the process
   stopped, for a worker you cannot reach). Then `gate-resolve` with what was chosen. Neither
   command is ever yours to run unprompted.

## Leaked terminals

A settled task can still own a live terminal — terminal accounting is tracked separately from
task status, and the `external_terminal` workers this runbook launches are exactly the ones Orca
will not reclaim on its own. Sweep for them at the end of every run, and any time the host feels
loaded:

```bash
orca orchestration worker-list --run <run_id> --json
orca orchestration worker-list --terminal-state reclaimable --json
```

Anything `reclaimable` is a worker that finished and was never released: `worker-release` it, then
`orca terminal close --terminal <handle>` for the external ones. A run is not over while its
terminals are still alive.

## Merge policy

- **The gate is whatever `docs/agents/setup.md` recorded** under `## Merge gate` — `github-actions`,
  `local <command>`, or `unverified`. Nothing red merges, and nothing *unverified* merges quietly:
  say which mode applied every time you merge. "CI green" is not a gate until you know a CI exists.
- **github** tracker: squash-merge the PR (`gh pr merge --squash --delete-branch`) once the gate
  holds.
- **linear** tracker with no remote: merge the task branch into the cockpit `main` locally
  (`git merge --squash <task-branch>`), push if a remote exists.
- The coordinator merges, the worker never does. The merge is what unblocks dependents, so
  merge promptly after a `succeeded` report — a dependent blocked on an unmerged parent looks
  identical to a stuck run.

## Hard-won notes

- Launch commands per runtime live in [`runtimes.md`](runtimes.md) — that file is the single
  source for them, including why each runtime needs the shape it has. `worker-start --agent <tui>`
  launches the named TUI app and never selects the permissive `worker` profile, on any runtime.
- `worker-start --terminal <handle>` requires `--worktree` to match the terminal's worktree, or
  it fails with `terminal_worktree_mismatch`.
- opencode defaults to prompting (`ask`) for `external_directory` and `doom_loop`; the `worker`
  agent auto-allows them so unattended runs never stall on a permission prompt.
- `worker_done` must come from the worker's own terminal with the injected
  `--task-id` / `--dispatch-id`; it marks the task and dispatch complete automatically — do not
  follow it with a manual `task-update` (except in recovery).
- `worker-start` `--worktree new-child`/`new-top-level` creates a fresh worktree + branch and
  does not rerun setup. Do not reuse the primary worktree for tasks.
- A worker launched through `terminal create` (custom argv / `OPENCODE_CONFIG_CONTENT`) is an
  `external_terminal`: after `worker-release` returns `retained / external_terminal`, close the
  worker terminal yourself (`orca terminal close --terminal <handle>`) — Orca does not close
  terminals it did not create through `worker-start`.
- Tracker updates after merge are **not automatic**: `gh pr merge` closes the GitHub issue on its
  own, but Linear does **not** move the issue state when the PR merges. After a successful
  linear-tracker merge, update the linked issue explicitly
  (`orca linear status set <key> --to "Done" --workspace <id>` and
  `orca linear comment add <key> --body "Merged in <pr/branch>"`) so the tracker reflects the run.
