# backend/src/projectRunLock

Cross-process exclusion for repo-mutating runs — **defence layer #8** in the
root `CLAUDE.md`'s `.git`-deletion defences. The in-process guards (the
`mergeRuns.ts` singleton, `mergeLocks.ts`) only stop races *within one*
process; this stops two Lattice backends (classically: Lattice opened on its
own repo while another instance has the same repo as a project) from entering
the merge pipeline at once and racing on `git status` / snapshot /
fast-forward. `../projectRunLock.ts` is the public facade.

## What it guards

One lockfile per project: `~/.lattice/per-project/<hash>/run.lock` (`paths.ts`,
via `homeProjectDir` and the shared `projectHash` contract). Path aliases must
share the preserved storage hash so they contend for the same lock; never
recompute a hash from a path spelling — see
[project identity and legacy storage](../PROJECT_IDENTITY.md).

Body is `{pid, hostname, startedAt, label, ownerId}`. The UUID `ownerId` is
minted per acquisition and identifies its generation; legacy locks lack it.
Labels (`merge-run`, `manual-merge`, `workflow-<kind>:<runId>`,
`repo-maintenance`, …) drive diagnostics, recovery and restart deferral.

## Modules

- `paths.ts` — lockfile path.
- `types.ts` — `LockBody`, `ProjectRunLockHandle`, `ProjectRunLockInspection`.
- `lockfile.ts` — read/parse observations, complete-body hard-link publication, retirement claims + `sameLockBody`.
- `tombstones.ts` — `pruneRetiredTombstones`, the bounded prune below.
- `liveness.ts` — `currentLockBody`, PID-alive probe, PID-reuse disambiguation.
- `steal.ts` — `clearStaleLockOrThrow`: steal vs. throw.
- `acquire.ts` — `acquireProjectRunLock`: restart-drain gate, pruning, publication + one stale-recovery retry.
- `ownership.ts` — `Owner`, the single canonical-project local registry, `registerProjectRunLock` (registration + cached release that drains borrowers before retirement). No dependency on acquisition or mutation scheduling.
- `mutation.ts` — `withProjectMutation`: shared pending acquisitions, AsyncLocalStorage context, per-project scheduling, closing/exclusive wait policy. Keeps a compatibility re-export of `registerProjectRunLock`.
- `release.ts` — `releaseLockFile`: ownership check, then the shared retirement.
- `withLock.ts` — `withProjectRunLock(projectPath, label, fn)`: acquire, run, release in `finally` — the usual entry.
- `inspect.ts` — `inspectProjectRunLock` → `{holder, alive}` without acquiring or stealing (merge-run resume; the dev runner's restart deferral).
- `errors.ts` — `ProjectRunLockedError` (carries the contended `holder`), `describeProjectRunLockHolder`, label constants, `RepoMaintenanceBusyError` + `isLocalRepoMaintenanceHold`.
- `interruptedRun.ts` — `isResumableInterruptedRunLock` (`merge-run`, `workflow-merge:*`, `workflow-push:*`) + the `interrupted-run.json` marker that boot snapshot recovery writes before it steals such a lock, so `../recovery/mergeRunResume.ts` still resumes the run and the owed post-merge hook still defers. The resume clears it once it has acted.

## Lifecycle invariants

- **Acquire waits while a restart drain is active** (`../restartDrain/gate.ts`;
  the drain expires by TTL if no restart follows).
- **Publish only a complete body.** `writeNewLockBody` writes the body to a
  unique sibling with `wx`, then publishes with exclusive
  `fs.link(pending, run.lock)` — the hard link IS the mutual exclusion; sibling
  cleanup is best-effort. Never `wx`-write `run.lock` directly (a contender can
  read the still-empty body as corrupt and steal it), never read-then-write or
  an overwriting rename, and never fall back to partial-body publication where
  hard links are unsupported (acquisition fails). On `EEXIST`,
  `clearStaleLockOrThrow` retires or refuses; at most two publication attempts,
  then an error — never spin.
- **Retirement requires the exclusive claim.** Release checks `sameLockBody`
  (including `ownerId`); stale recovery applies the liveness rules first. Both
  use `retireLockFile`: claim `run.lock.retired/<sha256(exact raw body)>` with
  `wx`, re-read and match the exact raw body, then unlink `run.lock`. Only one
  observer can remove a generation, protecting a successor from a suspended
  stale observer — a body comparison alone is insufficient; hashing raw bytes
  also distinguishes legacy generations. `readLockObservation` treats only
  `ENOENT` as absence; other read errors propagate and refuse
  release/recovery.
- **Keep retirement tombstones** — deleting them while a process can retain an
  observation reintroduces the race. Sole exception: `pruneRetiredTombstonesOnce`
  (first acquisition per project per process) runs only while `run.lock` is
  absent and removes only tombstones older than 7 days (`at`, mtime fallback;
  unjudgeable age ⇒ kept). It relies on bodies never being re-issued (UUID
  `ownerId` + timestamp); do not broaden it.
- A crash after claiming retirement but before unlink deliberately leaves the
  lock blocked (fail-closed, not auto-recovered): stop all backends, then
  inspect/remove only `run.lock`, preserving `run.lock.retired`. Concurrent
  older backends that ignore tombstones are unsupported — upgrade together.

## Liveness / staleness model

Steal only on proof of death: an unparseable lockfile, or a same-host holder
whose PID is dead. **Refuse** (`ProjectRunLockedError`) on a live same-host
holder, any remote-host holder (its PID can't be probed — assume alive), and
same-process re-entry (would deadlock the merge worker; the in-process guards
should catch it first). Uncertainty fails safe: treat as alive / refuse.
**Never auto-steal a remote-host or same-process lock.**

PID reuse (aggressive on Windows) — `isLockHolderAlive` isn't just
`process.kill(pid, 0)`:
- Holder PID equals ours but its `startedAt` predates *this* process's start ⇒
  a prior backend's stale lock ⇒ dead, steal (`isCurrentProcessHolder` uses the
  same check for the re-entry refusal).
- PID live but the OS-reported start time is *after* the lock's `startedAt` ⇒
  recycled into an unrelated process ⇒ steal (`getProcessStartTimeMs`:
  PowerShell on win32, `ps -o lstart=` on POSIX; `null`/uncertain ⇒ alive).

Both use `THIS_PROCESS_STARTED_AT` (captured at load from `process.uptime()`)
and `PROCESS_START_FUZZ_MS` (1 s). Without them a crashed backend's
`merge-run` lock stays un-stealable and silently aborts every later run.

## Resolver and snapshot mutations

`withProjectMutation(project, fn)` borrows this process's acquired ownership
through a per-project queue, or acquires a short owner if no run owns the
project locally; another backend's ownership is never borrowable. Resolver
re-sync/finalization, snapshot capture and restoration all enter it; nested
calls inherit the active slot via AsyncLocalStorage; simultaneous standalone
callers share one acquisition. Only bounded repository operations belong in
it — **never a wait for an agent callback** — which is what lets a merge worker
keep `run.lock` while its callback finalizes.

- Release closes admissions, drains accepted mutations, then retires the lock.
  The owner stays registered until its lockfile is gone, on purpose — an
  earlier acquire would find our own pid's lock on disk and be refused.
- A mutation arriving while the owner is *closing* polls the local registry
  (25 ms steps, 2 s cap) until the owner has retired, then acquires afresh.
  Don't reintroduce an "ownership is closing" throw: a resolver's one-shot
  Stop-hook `/complete` 500'd, the parked merge-run waiter was never
  signalled, and the run sat on `run.lock` for its 30-minute cap.

## Exclusive holds

`acquireProjectRunLock(project, label, { lendable: false })` registers an owner
`withProjectMutation` will **not** borrow. Two holders:

- `repo-maintenance` — the post-merge-run gc (`../worktree/repoMaintenance.ts`);
  merging beside a repack leaves a full pack copy on Windows. `startMergeRun`
  throws a typed `RepoMaintenanceBusyError` while it runs (also when it loses
  the lock race to this process's gc — `isLocalRepoMaintenanceHold`); workflow
  control steps `waitForRepoMaintenance` first; callback-driven restarts
  (`/stash-resolved`, the resolver finalize, the mid-run restart) must go
  through `startMergeRunAfterMaintenance` (`../mergeRuns.ts`), which waits and
  retries — swallowing the refusal as "a run is already active" stranded the
  remaining Ready-to-Merge tasks.
- `workflow-test:<runId>` — the workflow Run tests step
  (`../workflowRuns/testStep/`), whose agent edits and commits on the main
  checkout for the whole hold; a manual-merge resolver's finalize
  (`routes/tasks/finalizeResolved.ts` → snapshot + FF) or a snapshot
  capture/restore must not run under it.

A mutation under an exclusive hold **defers**: `waitForExclusiveProjectHold`
polls the registry (500 ms) until the holder leaves, then proceeds as if no
owner had been there (leak backstop `EXCLUSIVE_HOLD_WAIT_MAX_MS`, 13 h; the step
caps itself at 12 h). The post-merge hook fired outside a merge run
(`routes/tasks/hooks/postMergeHookHelper.ts`, from the resolver `/complete`,
`/merged`, `/stash-resolved`) waits the same way, so no hook agent starts on
the tree under the test agent. A **new** acquisition while the hold is live
(manual `/merge`, Merge All) is refused as usual; `describeProjectRunLockHolder`
names the Run tests step / housekeeping gc for a same-process holder instead of
"another process". The dev runner (`backend/scripts/dev/runLocks.mjs`) exempts
every `workflow-*` label from its 15-minute forced restart, and
`../recovery/mergeRunResume.ts` never resumes a merge run for a stale
`workflow-test:` lock (the workflow resume re-takes it).

Tests (`../__tests__/`): `projectRunLock.test.ts`, `projectMutation.test.ts`
(ownership), `workflowRunTestsStep.lock.test.ts` (exclusive holds),
`repoMaintenanceMergeGate.test.ts`, `stashResolvedAfterMaintenance.test.ts`.
HOME-isolated single-file runs: [test guide](../__tests__/CLAUDE.md).
