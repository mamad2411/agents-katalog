# backend/src/routes/tasks/hooks

The worktree callbacks: the task agent's Stop hook and the conflict resolver's
curls. `../hooks.ts` (`buildTaskHookRouter`) wires one handler module per
route; the shared resolver-finalize flow is `../finalizeResolved.ts`. Delivery
and replay of these callbacks: `../../../callbackOutbox/CLAUDE.md`. The
merge-run half of the resolver handshake: `../../../mergeRuns/CLAUDE.md`.

## Map

- `complete.ts` — `/complete`. Order: `?project=` pin (the hooks send none) →
  `rejectStaleReplay` → resolver-finished branch (ready_to_merge + `conflict`
  → `finalizeResolvedTask`, rendered by `respondToResolverFinalize`) → the
  in_progress → ready_to_merge flip (`decideInProgressComplete`) → deferred
  pty kill. Any other lane is an `{ok:true}` no-op.
  Opt-in second opinion (`../../../taskReview.ts`) replaces the task flip with
  a crash-safe `reviewing` record and `{ok:true,reviewing:true}`; same-head
  repeats are no-ops. Resolvers bypass it. The review owns the eventual flip
  or persisted fresh rerun; see `../../../taskReview/CLAUDE.md`.
- `merged.ts` — `/merged`: resolver success → `finalizeResolvedTask`.
- `mergeAborted.ts` — `/merge-aborted`: resolver give-up or the Resolving
  strip's Cancel. Delegates abort-mid-merge + clear-conflict-flags +
  kill-orphaned-resolver-pty to `mergeRuns/abandonedResolver.ts`
  `recoverAbandonedResolverTask`, then `signalConflictWaiter(task.id)`.
- `stashResolved.ts` — `/stash-resolved`: cleanup → qa, then restart the merge
  run for remaining work (`startMergeRunAfterMaintenance`).
- `postMergeHookHelper.ts` — `awaitPostMergeHookOutsideRun`, shared by
  complete / merged / stash-resolved.
- `../finalizeResolved.ts` — `finalizeResolvedTask`: re-sync with main,
  finalize, requeue on conflict; returns a discriminated result each route
  renders into its own HTTP shape.

## Invariants

- **Every callback is idempotent** and its path, method, status codes and
  response shape are the contract Stop hooks / resolver curls depend on —
  don't change them when refactoring.
- **`/complete` flips only on a real commit**: a real zero commit count →
  `{awaitingCommit:true}`, task stays in_progress; a *git error* counting
  commits flips anyway (the Stop hook fires exactly once; a genuinely empty
  branch is still caught by the merge's `emptyBranchOutcome`). The flip uses
  `updateTaskCrashSafe` (disk before cache), never the debounced update — a
  restart inside the debounce would strand a finished task at in_progress.
- **Stale replays are refused**: an outbox replay whose session moved on
  since `replayQueuedAt` gets **409** `stale-replay` (final, so the drain
  drops it) — acting on it would flip/finalize and kill the pty mid the
  user's new turn.
- **Respond before killing the pty**: `scheduleWorktreePtyKill` fires
  `PTY_KILL_DELAY_MS` (1 s) after the response — the calling curl runs inside
  that pty — then `notifySessionsFreed` so a deferred spawn takes the slot.
- **A resolver finalizes only while `task.conflict` is still set** (both
  `/complete`'s resolver branch and `/merged`). `/merge-aborted` clearing the
  flag is what makes Cancel authoritative: a late `/merged` from the
  abandoned resolver is a no-op, not a finalize + main fast-forward.
- **`/merge-aborted`**: honours the project pin (another board → 404, nothing
  aborted; missing/empty project = unpinned, so the resolver's give-up curl
  works). Runs recovery under the per-task `mergeLocks` lock (`git merge
  --abort` mutates the worktree index); a held lock is waited for up to
  `MERGE_ABORT_LOCK_WAIT_MS` (5 s, `acquireBriefly` — the run's conflict wait
  parks lock-free and the give-up curl is one-shot), then **409**. Signal the
  conflict waiter **after** recovery: without it a parked merge-run worker
  only notices via `mergeRuns/waiterLiveness.ts` (dead pty ~75 s, 30-min idle
  pause) while holding the project run-lock, 409-ing every later merge. The
  task stays plain ready_to_merge — no auto-restart, unlike `/complete` /
  `/merged`.
- **`/stash-resolved` acts only when the task is ready_to_merge AND
  `git merge-base --is-ancestor refs/heads/<branch> HEAD` (via `projectGit`)
  positively says merged**; anything else (not an ancestor, missing ref, git
  error, `.git` gone) is an `{ok:true}` no-op — a stray or late curl would
  otherwise `branch -D` unmerged commits and stamp a fake `mergedAt` that QA
  verdict logic trusts. Cleanup still passes `keepBranchIfUnmerged` as a
  backstop. A restart refused because the post-run `git gc` is in flight must
  wait and retry (`startMergeRunAfterMaintenance`), never be read as "a run
  owns the rest"; when no run picks up work the route fires the post-merge
  hook itself. Honours the `?project=` pin (404).
- **`awaitPostMergeHookOutsideRun` skips while a merge run is active** — the
  run owns its end-of-run hook fire, and double-firing deadlocks the run on
  its own gate. It first waits out an exclusive project hold (a workflow Run
  tests step on the main checkout); a hook-gate error is logged, never thrown.

## `finalizeResolvedTask` locking

- It takes the per-task `mergeLocks` lock around its git work, serializing
  against the merge-run worker (`mergeRuns/processTarget.ts`,
  `mergeRuns/flaggedConflict.ts` `tryFinalizeAfterResolverFinished`, same
  lock) and duplicate hook fires (two `/complete`s, or `/complete` racing
  `/merged`) — otherwise two `mergeWorktreeInRepo` runs race on
  `.git/index.lock` + `MERGE_HEAD` in one worktree. The loser gets
  `already-finalizing`, rendered `{ok:true, finalizing:true}`; the holder
  finishes the work.
- Once it holds the lock it re-reads the task (`deps.readTask`, default
  `getTask`) and returns the same no-op if `conflict` was cleared meanwhile —
  the route checked the flag before the lock, and a Cancel in that window
  must not be overridden by a fast-forward into main.
- The back-off is correct only because the holder is actively doing the git
  work, so **the merge-run worker must never hold the lock while parked** on
  a conflict waiter (`mergeRuns/resolverSpawn/park.ts`
  `parkOnConflictResolver` drops it): the resolver's `/complete` needs that
  lock to finalize + signal, and would otherwise back off forever. Detail:
  `../../../mergeRuns/CLAUDE.md`.
- `finalizeQueues` serializes only the fast-forward step, not this earlier
  in-worktree merge — don't rely on it in place of the lock.

## Tests

Named after the module (grep `complete`, `mergeAborted`, `stashResolved`,
`finalizeResolved` in `backend/src/__tests__/`). Each lock-taking handler has
an injectable deps seam (`recover` / `signalConflictWaiter` / `lockWaitMs`;
`cleanupWorktree` / `startMergeRun`; `readTask`) for its regression test.
