# backend/src/worktree

Git-worktree subsystem: task worktree setup/teardown, the merge-in-worktree +
fast-forward pipeline, project-repo git policy, disk/LFS/gc guards, snapshots.
Public surface: the `../worktree.ts` facade. Not here: run exclusion
(`../projectRunLock/CLAUDE.md`), merge-all runs + circuit breaker
(`../mergeRuns/CLAUDE.md`), boot orphan sweeps (`../recovery/CLAUDE.md`).
**Read Invariants before touching merge / cleanup** — each rule is a past incident.

## Map

Files not listed here lead their Invariants bullet.

- `merge*.ts` + `merge/`, `conflictResolve.ts`, `finalize*.ts`, `resyncFinalize.ts`, `staleGitLocks.ts` — merge pipeline → `merge/CLAUDE.md`.
- `snapshot.ts` + `snapshot/`, `discardArchive.ts` (format) → `snapshot/CLAUDE.md`; `stash.ts` is the legacy name delegating to it.
- `projectGit.ts` + `projectGit/` → `projectGit/CLAUDE.md`; `projectGuards.ts` + `projectGuards/` (excludes, untrack) and `instructions.ts` + `instructions/` (agent briefs) → their docs.
- `setup.ts` — `setupTaskWorktree` facade over `setupProject.ts` (repo root + hygiene), `setupCandidates.ts` (canonical / `-rN` path + branch), `setupAdd.ts` (reconcile → `git worktree add`), `setupFiles.ts` (`LATTICE_TASK.md`, hooks, excludes).
- `envDetect.ts` + `envDetect/` — package-manager envs a fresh worktree lacks (`node_modules`, `.venv`, …) → brief env notes (`UserSettings.worktreeEnvNotes`; empty ⇒ none).
- `commands.ts` — pure claude/pi/codex command-string builders, no I/O.
- `state.ts` — read-only queries (bottom).

## Invariants

### `.git`-deletion defences

Only a recursive delete reaching `.git` (direct `fs.rm`, or a lost
`git stash --include-untracked`) has ever deleted it. Layers, outermost first:

1. Worktrees live in `~/.lattice/worktrees/<hash>/`, outside the project.
2. `projectGit` whitelist — destructive project-repo git throws first.
3. Cleanup never falls back to `fs.rm`: `git worktree remove` (exact dir, no symlink following); never a global `git worktree prune`.
4. `pruneReparsePointsUnder` before any recursive removal — breaks junction loops from an in-worktree `npm install` of a `file:..` self-dep (never re-add one to `backend`/`frontend`).
5. Copy-based snapshots, never `git stash`; no discard archive, no force-removal.
6. Circuit breaker (`../mergeRuns/repoIntegrity.ts`): `.git` gone or HEAD moved non-forward halts the run.
7. `gitBackup.ts` — `git bundle --all` before each merge run; recover with `git fetch <bundle>`.
8. `assertNotReparsePoint` on remaining `fs.rm` sites, snapshot-manifest path validation, the cross-process run lock.

### exec / projectGit

- **All project-repo git goes through `projectGit`**; raw `exec('git')` only in modules `../__tests__/rawGitAllowlist.test.ts` lists (worktree-side git, read-only `state.ts`).
- `exec.ts`: `setEncoding('utf8')` (a multi-byte char split across reads must not become U+FFFD); a timeout resolves within `EXEC_KILL_GRACE_MS` even if a grandchild holds the pipes; a missing `cwd` REJECTS (ENOENT), never a non-zero code; `env` merges over `process.env` for that child only.

### Disk space, LFS, gc

- **`checkoutGate.ts`**: ≤ 2 concurrent `git worktree add`s machine-wide, FIFO (parallel big checkouts + LFS smudge pinned disk and CPU). The disk reservation is taken *inside* the slot so waiters hold none. Every add (setup + merge re-create) is bounded by `WORKTREE_ADD_TIMEOUT_MS` (30 min; a hung hook / smudge / credential prompt held a slot forever); a timed-out setup add is cleaned via `reconcileStaleState` and throws (no other suffixes).
- **`diskSpace.ts` guard** (right before every `worktree add`): admit only if `free − in-flight reservations − estimate ≥ minFreeDiskGb` (default 10), else `SpawnDiskSpaceError` — a spawn-queue **deferral, never a failure** (`../spawnQueue/CLAUDE.md`). The estimate (`git ls-files` size, raised to the largest measured fresh worktree) is keyed by repo **and LFS mode** — one mode's observation never raises the other's. Unmeasurable ⇒ admit.
- **`diskFull.ts` merge floor**: merge and FF refuse under `MERGE_MIN_FREE_BYTES` (1 GB) — a floor, not the reserve, since merging is what frees space.
- **LFS pointer mode** (`lfsMode.ts`; `UserSettings.taskWorktreeLfsContent`, absent = `'pointers'`): `GIT_LFS_SKIP_SMUDGE=1` goes to every git that checks files out INTO a task worktree — `worktree add` + re-create, worktree-side `merge` / `merge --abort` (setting read at merge time), and the task/resolver pty (`../terminalServerClient/spawnBody.ts`, via the `managedMcpEnv` wire field so an older executor applies it). **Main's FF uses the normal env.** `lfsMode.ts` must not import `projectGit` (`state.ts` imports it). `lfsPaths.ts`'s `git lfs pull --include` brief note: pointer mode + LFS files only.
- **No git auto-gc** (`gitAutoGc.ts`): every git child gets `gc.auto=0` + `maintenance.auto=false` via `GIT_CONFIG_COUNT/KEY_n/VALUE_n`, appended to any existing count; agent ptys too (`spawnBody.ts`). Per-merge repacks on Windows left undeletable pack copies — 80 GB in minutes.
- **`repoMaintenance.ts`** (a quiet minute after a merge run, single-flight, skipped while the project merges): unlinks `tmp_*` > 6 h and `.idx`-less `pack-*.pack` — never a `.keep` pack, never under a fresh `gc.pid`, single files only — then foreground `gc --auto` only if another pack copy fits above the reserve, **under a non-lendable `repo-maintenance` run lock**. Callback-driven merge-run restarts must use `startMergeRunAfterMaintenance` (`../projectRunLock/CLAUDE.md` → "Exclusive holds").
- **Bundles** (`gitBackup.ts`): ≤ 5 **and** ≤ 8 GB per project (newest kept); prune *before* writing; skip when it won't fit above `minFreeDiskGb`; reuse one under 10 min old. Timeout 60 s + 60 s/GiB, cap 20 min. A failed bundle removes its `.bundle.lock`; each backup sweeps non-`.bundle` leftovers older than `LEFTOVER_STALE_MS`, and leftovers count against the byte budget.

### Teardown: reconcile, cleanup, archive

- **Archive before any force-removal** (`discardArchive.ts`); on `failed` the caller **must keep the worktree**.
- **`staleInitLock.ts`** `worktree unlock`s **only when** the reason is exactly `initializing`, the checkout is under a managed dir, and its admin `locked` file is > 10 min old. Cleanup, reconcile and the boot sweep call it before their lock check (they honour locks: a mid-checkout kill would strand a multi-GB checkout).
- **`reconcile.ts`** frees only an exact managed fresh-run candidate: verifies NUL-delimited registrations, branch ownership, locks, nested checkouts and physical path before mutating; rechecks after PTY shutdown; **refuses a branch with unmerged commits** (`HEAD..<branch>` > 0 — a task moved back to Open keeps its branch; a fresh Run would `branch -D` the only copy) or a failed archive — setup takes `-rN`; the boot sweep applies the same guard. Preserves other/main/moved/locked registrations; stops on git removal failure. Its `fsRmWithRetries` is only for verified unregistered home-scoped strays without a `.git` marker (`guardReparse: true`), never after a failed registered removal.
- **`cleanup.ts`** order: validate registration, branch/detached state, locks, physical path → kill PTYs by cwd → recheck → archive (`skipArchive` only if the boot sweep did) → `pruneReparsePointsUnder` → exact `git worktree remove --force` → verify no checkout uses the branch → delete only `lattice/*`. `keepBranchIfUnmerged` (task delete) keeps a branch with unmerged commits **or an undeterminable count** (`onBranchKept`). `true` = done/idempotent, `false` = preserved/deferred. Failed remove, still registered → keep branch + registration for the boot sweep; registration gone → log leftovers for `../recovery/worktreeResidueSweep.ts`, run the branch step. Unregistered dirs, locked/moved/nested checkouts, permission-unknown paths: preserved.
- `rmRetry.ts` is the one retrying recursive delete (reconcile + `../homeScratch/cleanup.ts`); only EBUSY/EPERM/ENOTEMPTY retry; the callers' `delays` differ on purpose — **don't unify**. `guardReparse` runs the reparse guards in-loop (reconcile); home-scratch runs them itself.
- `cleanupSafety.ts`: `isUnderManagedWorktreesDir` (home or legacy in-project dir), `assertSafeWorktreePath` (throws on empty / repo-root / out-of-bounds before any git), `assertNotReparsePoint` (refuses a symlink or a realpath elsewhere — junctions, mounts, 8.3 aliases).
- `reparsePoints.ts` removes only the *link*, never its target (skips ordinary `node_modules` package subtrees); otherwise `git worktree remove` fails on Windows past MAX_PATH.
- `pathProbe.ts` `pathExistsStrict` is the one teardown existence probe: `lstat`, `false` **only** on `ENOENT` (permission error = unknown, never absent) — no `stat` / swallow-all substitute.
- `paths.ts` `isPathStrictlyInside` case-folds on win32 (mixed `homedir()` / git spellings made `assertSafeWorktreePath` refuse).

### Lattice-owned files

- `managedFiles.ts` is the only source of owned / exclude / shelve lists. A "which owned files are tracked?" site issues ONE `git ls-files -z` for the set (`trackedOwnedPaths`), never a spawn per path.
- `stopHook.ts`: Claude hook JSON stays byte-identical for task worktrees and workflow steps (`../claudeStopHook.ts`). `.codex/hooks.json` is **if-absent** (never clobber the repo's own) unless `isLatticeGeneratedCodexHooks` says it's Lattice's — then rewritten (a committed copy would point new worktrees at another task's `/complete`). Excluded + shelved, but deliberately NOT owned / auto-resolved to "ours".
- Merge-time shelving: `merge/CLAUDE.md`. Excludes in the COMMON gitdir, hygiene order, `.gitignore` never edited: `projectGuards/CLAUDE.md`.

## `state.ts` (read-only queries)

Plain `exec` (project repo *or* worktree). `checkBranchExists` / `countBetween` **throw** on git failure (`execSignalKill.test.ts`) — only a clean exit is evidence (a transient failure read as "gone" once let the boot sweep delete a branch with unmerged work). `isMidMerge` reads a missing dir as `false` (ENOENT would crash the merge-run worker); `abortWorktreeMerge` only after it. `parseWorktreesPorcelain` takes `-z` (and legacy newline) output and keeps `lockReason`; `listConflictedFiles` uses `-z`; `assertGitDirIntact` opens every project-repo mutation.

Tests: grep the module name in `../__tests__/`.
