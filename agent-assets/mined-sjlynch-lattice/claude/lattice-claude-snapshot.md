# backend/src/worktree/snapshot

Safety-critical copy-based working-tree snapshots under
`~/.lattice/snapshots/<hash>/`, behind the `../snapshot.ts` facade (`../stash.ts`
is the legacy name: `RUN_STASH_LABEL`, `assertSafeForStash`). Never replace with
`git stash --include-untracked` — it silently lost untracked files. Also owns the
format of `../discardArchive.ts`'s discarded-worktree archives (bottom).

- `capture.ts` — `snapshotWorkingTree` (under `withProjectMutation`),
  `createSnapshotDirectory`, `writeCapturedSnapshotManifest`,
  `buildSnapshotCleanupPlan`; scope filter, free-space refusal, partial-dir
  removal, `readHeadCommit` (→ `baseCommit`). Re-exports most helpers of the
  next two.
- `pathClassification.ts` — `parseStatusRecords` / `parseStatus` (`-z` parser,
  four buckets); `filterSafeDirtyPaths` / `classifySafeDirtyPaths`
  (repo-containment guard).
- `copyAndCleanup.ts` — `copyDirtyPathsToSnapshot`, `resetTrackedSnapshotPaths`,
  `unstageAddedSnapshotPaths`, `restoreDeletedSnapshotPaths`,
  `cleanupCapturedUntrackedPaths`; `chunkPathsForArgv` / `GIT_ARGV_CHAR_BUDGET`.
- `versions.ts` — `pathVersion`: streamed sha256 / `link:` target / `null` if
  absent.
- `manifest.ts` — `SNAPSHOTS_BASE`, `SNAPSHOT_MANIFEST_FILENAME`
  (`_lattice-snapshot.json`), `SnapshotHandle` / `SnapshotManifest` /
  `RetiredSnapshotPath`, `readSnapshotManifest` via `isSupportedSnapshotManifest`.
- `restore.ts` — public `restoreSnapshot` (mutation ownership, ordered
  whole-snapshot restore, guarded dir removal) and `describePartialRestore`.
- `restoreTypes.ts` — options/result types, `SNAPSHOT_CONFLICT_SUFFIX`, the single
  `StaleSnapshotConflict` / `SnapshotPathKept` constructors used to classify.
- `restorePath.ts` — `restoreSnapshotPath` / `reapplySnapshotDeletion`: guarded
  per-path copy/delete, destination version checks, exclusive/reusable conflict
  copies.
- `threeWay.ts` — `reconcileWithCommittedChange`, `deletedSinceCapture`,
  `MAX_THREE_WAY_MERGE_BYTES` (8 MB).
- `restoreRetirement.ts` — `retireSettledEntries`: narrow a partial restore's
  manifest to retryable entries; archive when none remain.
- `recovery.ts` — boot `recoverPendingSnapshots`: `listPendingSnapshotDirs`
  (lazy `<hash>/<snap>` walk) → `validateSnapshotForRecovery` (skip
  missing/unsupported/archived manifests, dir hash must match `repoRoot`, repo
  must exist; tampered hashes refused) → `recoverOneSnapshot`
  (`noteInterruptedRunBeforeSteal`, own run lock, manifest re-read,
  `guardStaleOverwrite` restore; errors defer).

Capture order (keep intact):

1. Parse `git status --porcelain=v1 -z --untracked-files=all`. `-z` is required:
   the newline form mangles renames (`R  old -> new`) and quotes special-char
   names, silently dropping them. FOUR buckets, each cleaned differently:
   `untracked` (copy + delete), `modified` (copy + `checkout HEAD --`), `added`
   (`A`/`R`/`C`, in the index not HEAD: copy + `reset HEAD --` + delete —
   `checkout HEAD` can't reset a path HEAD lacks, and git refuses a WHOLE
   batched checkout on one bad pathspec) and `deleted` (` D`/`D `/rename source:
   nothing to copy; `checkout HEAD --` resurrects it for a clean FF, the
   manifest lists it, restore re-deletes it only if still a clean tracked HEAD
   copy). `MD` stays `modified` (index-only content must not be reset). Every
   batched `checkout`/`reset` retries per path on a non-zero exit.
2. Drop paths failing the repo-containment guard (`../paths.ts`
   `isPathInsideRepo`, which also refuses in-repo `.git/*` and `.lattice/*`);
   never copy/reset/delete them. Restore re-validates every manifest path, so a
   corrupt/tampered manifest can't write into the gitdir.
3. Create the snapshot dir and copy, recording successes and failures separately.
4. Write the manifest only after copies, listing only successful copies.
5. Reset/delete **only** successfully copied paths. A failed copy stays dirty so
   later git operations fail safely instead of losing data.

Scale limits (keep — a large uncommitted tree once filled the disk):

- **Scope.** `onlyPaths` captures only dirty paths colliding with it (equal, or
  one an ancestor dir of the other). `fastForwardMain` passes `git diff
  --name-only --no-renames HEAD <branch>` (`merge --ff-only` rewrites nothing
  else and refuses without writing if an unlisted dirty path would be
  clobbered); the merge-run stash passes the union of each Ready-to-Merge
  branch's `HEAD...branch`. No overlap ⇒ no snapshot; a failed diff ⇒ full
  snapshot.
- **Free space.** Bytes to copy are summed before creating the dir; the capture
  is refused (tree untouched) if they would cross `globalSettings.minFreeDiskGb`.
- **Command-line length.** Path-list git calls are chunked at 8,000 chars:
  Windows' 32,767-char limit surfaces as `spawn ENAMETOOLONG`, an exception the
  per-path retry never sees.
- **Partial copies.** A capture that throws before its manifest is written
  removes its dir (nothing was reset yet; recovery ignores manifest-less dirs).

Recovery invariants:

- Snapshot dirs use `mkdtemp`: same-label captures in one millisecond never
  share payloads or manifests.
- A repository path named `_lattice-snapshot.json` (case-insensitive) is left
  dirty, not captured/reset; older manifests listing it are refused on restore.
- Untracked cleanup is nonrecursive and rechecks parent symlinks. A file that
  became a directory after capture holds uncaptured work and must survive.
- The manifest reader validates recovery fields and arrays; a version number
  alone does not make a record safe.
- Stale conflict copies use exclusive creation with numbered suffixes; existing
  recovery work is never overwritten. Identical copies are reused across boots.

Ownership and edit preservation:

- Manifests carry the owning project lock generation. Boot recovery acquires its
  own project lock and re-reads the manifest before restoring; it never borrows
  a live merge's local ownership. Live-owned snapshots defer. Legacy snapshot
  identity: `../../PROJECT_IDENTITY.md`.
- Cleanup requires the snapshot dir and compares captured/current `pathVersion`
  before resetting/deleting; missing version evidence refuses cleanup. Literal
  Git pathspecs stop wildcard names resetting other files. Hashing streams, to
  keep large artifacts off the JS heap.
- Default (in-session) restoration preserves newer dirty edits and overlays
  only tracked destinations verified clean against HEAD;
  assume-unchanged/skip-worktree paths count as uncertain. Boot restoration
  (`guardStaleOverwrite`) is stricter: every differing destination keeps its
  content and the captured copy goes to a `.lattice-conflict` sibling.
- Restoration returns a structured restored/partial result (restored paths,
  conflicts, failures, retention). A partial restore retains the snapshot;
  partial teardown becomes a run error; a post-FF partial is surfaced to the
  finalize caller without retrying the already-successful HEAD move. Recursive
  cleanup refuses reparse points, filesystem roots, and any snapshot/project
  containment overlap.
- External editors don't take Lattice's lock: version checks catch changes
  before cleanup, but the final comparison + replacement is not an OS-level
  compare-and-swap; that window remains.

Restoring over a change that landed after capture:

- A capture records its HEAD (`baseCommit`). An in-session restore of a tracked
  destination clean against the NEW HEAD compares `baseCommit:<path>` with
  `HEAD:<path>`: same object → the copy overlays it; different (the FF rewrote
  it) → `git merge-file -p` of base / captured / current. Never blindly overlay
  the pre-merge copy — it silently reverts the task's change while reporting
  `restored`. A clean merge writes the combined file; overlapping hunks,
  binary/non-UTF-8 or > 8 MB keep HEAD's version and save the capture as
  `<file>.lattice-conflict` → `'partial'`, surfaced by FF finalize and merge-run
  teardown. Conflict markers never reach the main checkout. A modified file the
  merge DELETED is a conflict copy too, not resurrected. Boot recovery never
  merges. `projectGit` whitelists `merge-file` only as `-p`, fed temp copies of
  the checked bytes.
- A partial restore moves restored, conflict-copied, deliberately-kept (a
  captured deletion of a since-edited file) and unsafe entries to `retired`;
  only retry-fixable failures stay listed. Nothing left → `archived: true`: the
  payload stays for the user and recovery skips it. Without this every boot
  re-applies the whole manifest, resurrecting deleted files and re-creating
  reviewed conflict copies.
- Boot recovery's run lock steals an interrupted Merge All's dead `merge-run`
  lock (or a workflow Merge/Push step's), so it first records
  `interrupted-run.json` (`../../projectRunLock/interruptedRun.ts`):
  `resumeInterruptedMergeRuns` still resumes and the owed post-merge hook check
  still defers; the resume clears it once it has acted.

Discarded-worktree archives (`../discardArchive.ts`, also used by
`../merge/mergeResidue.ts`):

- Taken before reconcile, the boot orphan sweep or `cleanupWorktreeForTask`
  force-removes a worktree (`git worktree remove --force` drops uncommitted
  edits). Same status parse, containment filter, `mkdtemp` dir
  (`<ts>-discarded-worktree-<slug>-XXXX/`) and copy routine (links copied, never
  followed), with the WORKTREE as source; Lattice-managed files are skipped.
- Never mutates the worktree. Returns `absent`/`clean`/`archived`/`failed`; on
  `failed` (git can't vouch for the checkout, a containment drop, any copy
  failure, manifest write) the caller **MUST keep the worktree**.
- Manifest `_lattice-discarded-worktree.json`, payload under `files/` — never a
  `_lattice-snapshot.json`: `recovery.ts` acts only on that name, so archives
  (and older backends) never auto-restore a worktree's edits into the project.
- Retention: newest `DISCARDED_WORKTREE_ARCHIVE_KEEP` (20) per project, but never
  one younger than `DISCARDED_WORKTREE_ARCHIVE_MIN_AGE_MS` (7 days — a boot sweep
  over hundreds of orphans would otherwise delete archives seconds after their
  only-copy checkout). Only dirs with a valid discarded-worktree manifest are
  candidates (pending merge snapshots never are); removal is guarded (direct
  child of the project's snapshot dir, `assertNotReparsePoint`, links stripped
  first).
