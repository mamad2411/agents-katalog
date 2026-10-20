# backend/src/mergeRuns

Helper modules for the backend "merge all" engine. `../mergeRuns.ts` owns the
public singleton API and worker loop (`startMergeRun`, `finishRun`,
`restartMergeRun`). Not here: the in-worktree merge + fast-forward
(`../worktree/merge/CLAUDE.md`), the cross-process `run.lock`
(`../projectRunLock/CLAUDE.md`), boot resume (`../recovery/CLAUDE.md` step 5),
the hook itself (`../postMergeHooks/CLAUDE.md`).

## Map

- `types.ts` — persisted run records, events, status/error types, waiter entry.
- `snapshot.ts` — clone helpers; keep cloning here so subscriber and
  persistence snapshots stay identical.
- `normalization.ts` — `merge-runs.json` deserialization; a `running` run
  loaded from disk becomes errored (its worker died with the old process).
- `state.ts` — `RunState` / `MergeRunStateManager`: run maps, persistence,
  notify/subscribe, active-run lookup/cancel, zombie reaping.
- `lifecycle.ts` — `initializeRunState` (canonicalize, load, in-process 409
  gate, lock acquire honouring `lockMode: 'inherit'`; throws before any run
  record exists), `loadRunTargets`, `filterAndSortTargets`, `createRunRecord`.
- `preflight.ts` — per-run setup: task JSON backup, git bundle, Lattice-owned
  exclude/untrack repair, copy snapshot, circuit-breaker baseline HEAD.
- `processTarget.ts` — per-task state machine: re-read task, honour the merge
  lock, retry flagged conflicts, re-sync/finalize, spawn resolvers, progress,
  integrity check.
- `withMergeLock.ts` — shared per-task lock lifecycle (`tryAcquire`, record
  "lock held" + report `lock-unavailable`, release in `finally` unless an
  `awaiting-resolver` outcome handed it off). Callers choose the
  lock-unavailable follow-up.
- `flaggedConflict.ts` — a retried `conflict:true` task (below).
- `conflictWaiters.ts` / `waiterLiveness.ts` — resolver waiter registry and its
  bounded wrapper (below).
- `resolverSpawn.ts` / `resolverSpawn/` — resolver spawn, park, adoption. See
  [resolverSpawn/CLAUDE.md](resolverSpawn/CLAUDE.md).
- `resolverWaitFailure.ts` — `preserveResolverAfterWaitFailure`: a
  non-signalled wait records a `run.errored` entry and sets `cancelRequested`,
  preserving worktree, conflict flags, terminal and edits.
- `abandonedResolver.ts` — `recoverAbandonedResolverTask` for the explicit
  give-up (`routes/tasks/hooks/mergeAborted.ts`): abort the in-worktree merge,
  clear conflict flags (a late `/merged` becomes a no-op), kill the resolver
  pty by cwd; task stays plain `ready_to_merge`.
- `cancellation.ts` — WeakMap (keyed by the live run object) of the
  `AbortSignal` handed to resolver spawns, pre-aborted if `cancelRequested`;
  `cancelMergeRunSpawns` aborts it from `cancelRun`.
- `repoIntegrity.ts` — the run circuit breaker (below).
- `teardown.ts` — snapshot restore, `autoRestartIfNeeded`, `runPostMergeHook`.
- `finalize.ts` — `finalizeMergeRun`: worker body, lock release, then restart.

## Invariants

- **Runs must stay safely re-runnable.** Boot restarts an interrupted run
  (`recovery/mergeRunResume.ts`), so every per-task step is idempotent on a
  half-done task (merged-but-not-FF'd, half-finalized, conflict-flagged).
- Targets: `ready_to_merge` including conflict-flagged, `createdAt` ascending.
- **The in-memory run object is authoritative**; `loadProject` may only ADD
  ids it lacks. Persisted runs are snapshots, and re-seeding an existing id
  swaps the live object the worker mutates for a frozen clone — every later
  start then 409s and cancel does nothing (`startMergeRun` callers all run
  `loadProject` before the 409 gate).
- **A `running` record with no worker is reaped, never obeyed.**
  `markRunLive`/`markRunSettled` track what this process executes;
  `reapOrphanedRuns` (from `initializeRunState` and `getActiveRunForProject`)
  errors any other `running` record; `cancelRun` settles one outright. A
  zombie costs one reaped run, not every future merge.
- Persistence keeps the newest `MAX_PERSISTED_RUNS_PER_PROJECT` (50) settled
  runs plus every running one; pruning never drops a running run or one a
  live worker / parked waiter references. By-id waiters
  (`waitForMergeRunFinished`, `workflowRuns/controlSteps/merge.ts`) must treat
  a `null` lookup as finished.
- **Restart only after lock release and `finishRun`** (`finalize.ts`):
  otherwise the fresh run hits the 409 gate / held lock, `restartMergeRun`'s
  `.catch(() => {})` swallows it, and mid-run-ready tasks strand (no stale
  lock ⇒ no boot resume). Teardown only *decides* (returns a boolean, so it
  keeps no dependency on `../mergeRuns.ts`); no restart after a worker crash,
  a cancel, or an inherited lock (the workflow Merge step loops itself).
- Teardown restores the copy snapshot in-session, **on cancel too** (deferring
  to the next boot clobbered the user's re-done edits), and runs in a
  `finally` around the task loop. `loadRunTargets` releases an acquired lock
  if startup task loading throws before the worker exists.
- The post-merge hook (`runPostMergeHook`) is awaited **before** `finishRun`,
  so `completed` — and a workflow Merge step waiting on it — waits the hook
  out. It fires only when something merged or a hook is owed; a
  cancelled/halted run fires none and clears the owed marker.
- **Circuit breaker** (`checkRepoIntegrity` / `finishTaskAndCheckIntegrity`):
  between tasks `.git` must exist and HEAD may only move forward; the baseline
  advances after each pass, so a rewind to run-start HEAD trips too. A
  violation records a `(run)` error, sets `cancelRequested` and halts, leaving
  remaining tasks at `ready_to_merge`. It also halts on a git lock
  (`….lock: File exists`) surviving the FF retries + `clearStaleGitLocks`
  (`lock-halt`), and on disk full (`disk-halt`, `worktree/diskFull.ts`
  `isDiskFullMessage`, incl. the merge's `MERGE_MIN_FREE_BYTES` refusal) —
  both would fail every later task. The workflow Merge step's "made no
  progress" error quotes the halt reason.

## Conflict waiters

- `conflictWaiters.ts` is keyed by **taskId** (not runId), so task A's
  resolver can't unblock task B. Releases: `signal(taskId)` (real completion:
  `/complete` and `/merged` after finalize/re-sync advanced or requeued that
  task; `/merge-aborted` after clearing the conflict — that task is NOT
  auto-restarted), `unblockRun(runId)` (cancel), `abandon(taskId, runId)`
  (liveness backstop, not a completion; runId-guarded so a re-queued task's
  fresh waiter survives). A missing waiter means the backend restarted: start
  a fresh run. `taskIdsForRun` (`listLiveMergeRunResolverWaits()`) tells the
  restart drain a run is parked on a live resolver, not wedged.
- Park sites await `waiterLiveness.ts` `awaitResolverWaiter`, never the raw
  untimed `registerConflictWaiter`. It registers **synchronously** (keeps the
  register-then-release-lock ordering), then races a pty-liveness probe
  (exact session ID + normalized worktree cwd): `'signalled'`,
  `'resolver-dead'` (~75 s of no pty), `'resolver-idle'` (30 min without
  output), `'timeout'` (30-min cap while liveness is "can't tell"). Any
  non-signalled result `abandon`s the entry and goes to
  `preserveResolverAfterWaitFailure` — the run stops so `finalizeMergeRun`'s
  `finally` frees the project lock; a dead resolver can never wedge it.
- Register the task waiter before probing/repairing a recovered session and
  pass it into the wrapper, so a callback during those awaits is kept.
- `flaggedConflict.ts` `handleFlaggedConflictTask`: still mid-merge →
  `tryRespawnMidMergeResolver` reattaches or spawns a resolver
  (`resolverSpawn/`) and parks lock-free; after the spawn it **re-reads the
  task** and, if `/merge-aborted` cleared `conflict` (or it left
  `ready_to_merge`) while queued, kills the new resolver and records an error.
  Worktree clean → `tryFinalizeAfterResolverFinished` finalizes directly when
  main is already an ancestor, else falls through to the normal merge. Every
  path ends in `finishTaskAndCheckIntegrity`.

Tests: named after the module — grep it in `backend/src/__tests__/`.
