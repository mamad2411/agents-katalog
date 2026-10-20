# backend/src/worktree/merge

The single-task merge pipeline: merge main INTO the task's worktree, fast-forward
main to the result, finalize the task. This doc also owns the root-level
`../merge*.ts`, `../conflictResolve.ts`, `../finalize*.ts`,
`../resyncFinalize.ts` and `../staleGitLocks.ts`. Merge-all orchestration (runs,
resolver spawns, the circuit breaker) is `../../mergeRuns/CLAUDE.md`; snapshots
are `../snapshot/CLAUDE.md`; disk/LFS rules are `../CLAUDE.md` → "Disk space,
LFS, gc".

> **Name-collision hazard:** this `merge/` DIRECTORY ≠ the `../merge.ts` FILE.
> The FILE owns only the public orchestrator `mergeWorktreeInRepo` and
> re-exports `fastForwardMain`, `FF_LOCK_RETRY_DELAYS_MS` and the outcome types
> from here (callers keep that import path). Mind which one you're editing.

## Call chain (`mergeWorktreeInRepo` drives it)

1. `preflight.ts` — `preflightWorktreeMerge`: `.git` intact, is-a-repo, main on
   a branch, not already mid-merge, worktree exists (re-created if
   hand-deleted); auto-aborts an orphan worktree `MERGE_HEAD` from a crashed
   prior attempt; returns main's HEAD sha. Then `../merge.ts` refuses under
   the disk floor.
2. `branchState.ts` — `checkBranchState`: `already-merged` / `empty` / `ahead` /
   `error` (a git failure is `error`, never misread as an empty branch that
   silently drops the merge).
3. `mergeResidue.ts` — `clearMergeBlockingChanges`: an uncommitted change to a
   path main changed since the merge base (residue of a merge that died
   part-way, or an agent's never-committed edit) would make git refuse every
   later merge. Lattice merges the branch's COMMITS, so residue is archived
   (`../discardArchive.ts`) and only the blocking paths restored to HEAD —
   never merged. Archive failure → no change, `error`. Lattice-managed files
   are left to step 4.
4. `runWorktreeMerge.ts` — `git merge --no-ff -m <msg> <mainHeadSha>`, with
   owned files shelved/reset around it (an accidentally committed
   `LATTICE_TASK.md` can't abort it). A failure that leaves no merge in
   progress (not a conflict) → `restoreFailedMergeWrites` undoes exactly the
   paths that attempt wrote (dirty-now minus dirty-before).
5. `conflict.ts` — `handleMergeConflict`: auto-resolves Lattice-owned files; if
   they were the *only* conflicts it commits and returns `clean`, else
   `conflict` with the remaining files (caller spawns a resolver Claude).
   Re-installs the Stop hook either way.

- `fastForward.ts` — `fastForwardMain`: private `prepareFastForward`
  (`.git` exists, main on a branch, disk floor, `clearStaleGitLocks`,
  `assertSafeForStash` + snapshot scoped to `diff HEAD <branch>`) →
  `projectGit merge --ff-only` (an FF that hits a git lock retries after
  `FF_LOCK_RETRY_DELAYS_MS`, 2/5/10 s) → snapshot restore.
- `types.ts` — shared `MergeOutcome` / `MergeConflictKind`.

Root-level siblings:

- `../mergeConflict.ts` — `prepareMergeConflictOutcome` / `markTaskMergeConflict`:
  the shared resolver hand-off prep (write `MERGE_INSTRUCTIONS.md` → optionally
  set `conflict` + `conflictStartedAt` → build the resolver command) for
  `../finalize.ts`, `../resyncFinalize.ts` and
  `../../mergeRuns/resolverSpawn/spawn.ts` (`markConflict: false`, so an
  already-flagged task keeps its `conflictStartedAt`). Only the preparation is
  shared; each caller keeps its own outcome shape.
- `../conflictResolve.ts` — `resolveOwnedFileConflicts` (merge / stash-pop) +
  `resetOwnedFileLocalChanges`; its own module to break the `merge.ts` ↔
  `stash.ts` cycle.
- `../mergeOwnedFiles.ts` — shelve/restore around the merge,
  `untrackOwnedFilesPostMerge` after it.
- `../finalize.ts` — `finalizeMergedTask`: the FF / re-sync / state-transition
  decision tree only. `../finalizeQueues.ts` — `runSerializedFinalize` +
  `scheduleWorktreeCleanup`, the two per-project queues. `../resyncFinalize.ts`
  — `resyncWithMainAndFinalize`, shared "merge main into the worktree, then
  finalize".

## Invariants

- **`git merge` runs only inside the worktree** — main's vite-watched files
  never see conflict markers; main only ever moves by
  `projectGit … merge --ff-only`.
- **Refuse on a detached project HEAD** (`assertMainOnBranch`, read-only
  `symbolic-ref -q HEAD`) in both merge and FF: an FF there lands the tip on
  nothing `main` can see, and cleanup then deletes the `lattice/*` branch.
- **Re-create, don't fail, a hand-deleted worktree dir** from its surviving
  branch (`worktree remove --force` the stale registration → `worktree add
  <path> <branch>` → re-install Stop hook + excludes). The re-create is bounded
  by `WORKTREE_ADD_TIMEOUT_MS`; on timeout it removes its partial checkout and
  keeps the branch.
- **Disk floor**: merge and FF refuse under `MERGE_MIN_FREE_BYTES` (1 GB,
  `../diskFull.ts`) — a merge that runs out of disk dies part-way, and an FF
  truncates the files it rewrites. The FF checks too: a resolver's `/complete`
  reaches it without the merge preflight.
- **Stale git locks** (`../staleGitLocks.ts`, also run by merge-run preflight
  and `projectInit`): `clearStaleGitLocks` unlinks `index.lock`, `HEAD.lock`,
  `ORIG_HEAD.lock`, `packed-refs.lock` and the current branch's ref lock **only
  when** > 10 min old AND no running `git`/`git-*` started before it (an
  unreadable start time or failed listing counts as a possible holder).
  Single-file unlink, never recursive. One that survives halts a merge run once
  (`../../mergeRuns/repoIntegrity.ts`) instead of failing every remaining FF.
- **LFS**: worktree-side `git merge` / `merge --abort` get `GIT_LFS_SKIP_SMUDGE`
  per the setting read at merge time (`worktreeCheckoutEnv`); main's FF runs
  with the normal env.
- **The whole flow is re-runnable**: a merge run or boot recovery re-attempts
  half-done tasks (an FF already done is a no-op; `already-merged` is clean).

### Lattice-owned files around the merge

- The shelve list is the central `LATTICE_SHELVE_PATHS` (`../managedFiles.ts`),
  never a local array (a stale local list let a committed `.codex/hooks.json`
  abort merges with "untracked working tree files would be overwritten" —
  before any conflict exists, so no resolver can recover it).
- Shelve **untracked files only**: renaming a *tracked* file aside reads as a
  deletion and git refuses the merge for the opposite reason. Tracked owned
  files go through `resetOwnedFileLocalChanges` + the conflict auto-resolve.
- Restore favours Lattice for owned paths (per-worktree content) but keeps a
  tracked `.codex/hooks.json` the merge brought in (may be the repo's own).
- Shelve first recovers any `<f>.lattice-bak` a killed backend left (moved back
  when the original is absent, dropped when a re-created file supersedes it);
  `*.lattice-bak` is in `LATTICE_EXCLUDE_PATTERNS` so a resolver's `git add -A`
  never commits one.
- "Resolve to ours" is always correct for Lattice-owned files: a conflicted
  `.claude/settings.local.json` breaks the resolver Claude's bootstrap before it
  reads its instructions. `.codex/hooks.json` is deliberately NOT auto-resolved.
- Each "which owned files are tracked?" site issues ONE `git ls-files -z` for
  the whole set (`trackedOwnedPaths`), never a spawn per path.

### Finalize ordering (`../finalize.ts` / `../resyncFinalize.ts`)

Capture / finalize / restore share the project mutation owner
(`withProjectMutation`, `../../projectRunLock/CLAUDE.md`); boot recovery takes
its own lock.

1. Narrow `task.branch` + `task.worktreePath` before entering queued closures;
   missing info returns the existing error shape without touching git.
2. Inside `runSerializedFinalize` (two finalizes for one project must not
   interleave — the FF moves main's HEAD; the slot is released in a `finally`
   so an early return/throw never jams it), `assertGitDirIntact` before any
   project-repo git.
3. FF main with `projectGit … merge --ff-only` only. On error: at most one
   in-queue `mergeWorktreeInRepo` re-sync against current main, then retry the
   FF once. A re-sync conflict is not a bare error: leave the worktree
   mid-merge, write `MERGE_INSTRUCTIONS.md` + set `task.conflict`
   (`../mergeConflict.ts`) and return the merge-conflict outcome so a resolver
   can be spawned.
4. Stash/snapshot conflict outcomes keep their public shape (`stashConflict`,
   `resolveCommand`, `cwd`) and do not move the task to QA.
5. On success, `updateTaskCrashSafe({status: 'qa', ...})` **before** cleanup —
   disk first, cache second. Crash after the write ⇒ QA on disk; crash between
   FF and write ⇒ startup recovery re-runs finalization. If the write returns
   null (disk error / task gone), return an error and do **not** schedule
   cleanup — the task is still `ready_to_merge` and needs its worktree + branch
   for the retry (whose FF is then a no-op).
6. `scheduleWorktreeCleanup` runs **after** finalize returns, on a *separate*
   sequential per-project queue: two `git worktree remove`s must not race on
   `.git/index.lock`, and a hung cleanup must not stall the run worker once the
   task is QA on disk. Errors are swallowed; completed vs deferred cleanup is
   logged accurately (the boot sweep retries registered orphans). No raw
   `fs.rm` fallback — teardown rules: `../CLAUDE.md` → "Teardown".

`resyncWithMainAndFinalize` preserves caller hook ordering, short-circuits
(`mainIsAncestorOfWorktree`) only when the caller opts into the ancestor
check, writes first-pass conflict instructions before returning
`merge-conflict`, and maps finalize retry conflicts / stash conflicts / errors
back to the existing endpoint / merge-run outcome shapes.
