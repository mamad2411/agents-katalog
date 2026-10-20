# backend/src/taskCache

In-memory + on-disk store for Lattice's per-project task lists. Implementation
behind the `../tasks.ts` facade — import from there, never from these
internals. The generic cache / debounce / lock / corrupt-file machinery is the
`ProjectStateManager` base ([../projectState/CLAUDE.md](../projectState/CLAUDE.md));
this folder owns task semantics, paths, migration and backup/restore.

## Storage layout

```
~/.lattice/
├── projects.json                         # global index of project roots
├── tasks.json                            # legacy global tasks (pre-split)
└── per-project/
    └── <projectHash(project)>/
        ├── .canonical-path               # human-readable hint
        ├── tasks.json                    # the live task DB
        └── tasks.backup.json             # snapshot taken before each merge run
```

`projectHash(project)` comes from `../projectPath.ts`; a durable identity
binding may preserve a legacy hash (see [project identity](../PROJECT_IDENTITY.md)).
Legacy `<project>/.lattice/tasks.json` files auto-migrate here on first read;
the legacy copy is left in place so rolling back to an older build loses no
tasks.

## Module map

- `../tasks.ts` — the facade: constructs the singleton `ProjectsIndex`,
  `TaskMigrations` and `TaskCacheManager`, registers the memory gauges, and
  exports the public verbs (`listTasks`, `createTask`, `updateTask`,
  `updateTaskCrashSafe`, `deleteTask`, `backupTasksFile`,
  `restoreAllProjectsFromBackup`, …). Add a new public verb there, not on the
  manager directly.
- `manager.ts` — `TaskCacheManager extends ProjectStateManager<Task[]>`: CRUD,
  reorder, `updateTaskCrashSafe` (lock + notify; the disk-write core is in
  `crashSafeUpdate.ts`), `ensureProjectLoaded` / `loadAllKnown` (trigger
  migrations on first touch), `loadedTasks()` for recovery's read-only scans.
- `crashSafeUpdate.ts` — `applyCrashSafeTaskUpdate`, the disk-before-cache
  core. The caller binds `writeStateNow` / `cancelPendingPersist` /
  `getCached` / `setCached` to the live instance so subclass overrides still
  dispatch. MUST run under the manager's per-project write lock.
- `paths.ts` — `projectTasksFile`, `projectTasksBackupFile`,
  `LEGACY_GLOBAL_TASKS`; home root via `../projectPath.ts`.
- `projectsIndex.ts` — `ProjectsIndex`, the `Set<projectPath>` behind
  `~/.lattice/projects.json` that boot recovery uses to find every project.
- `pruneIndex.ts` — the conservative index-pruning predicate, run at boot by
  `projectsIndex.ts` and to reap an emptied scratch project in `deleteTask`.
- `migrations.ts` — `TaskMigrations` (once-per-process flag) +
  `migrateLegacy` (global `~/.lattice/tasks.json` → per-project split) and
  `migrateInProjectTasksToHome` (first-touch, idempotent; also called from
  `restoreTasksFromBackupIfMissing` so recovery sees legacy-only projects).
- `recovery.ts` — `backupTasksFile` (validates first; run by
  `mergeRuns/preflight.ts` at every merge run start),
  `restoreTasksFromBackupIfMissing` / `restoreAllProjectsFromBackup` (boot step
  1, `../recovery/CLAUDE.md`), `listReadyToMergeTasks` (boot branch repair),
  `listKnownProjects`.
- `taskUpdate.ts` — `stampTimestamps` (status-transition timestamps) and
  `applyTaskUpdate` (immutable one-item replace).
- `types.ts` — `Task`, `TaskStatus`, `TaskUpdates`, `TaskSubscriber`.
  `Task.review` holds per-head second-opinion state/attempt and durable kept
  branch identity. User lane changes withdraw active review identity.

## Ordering invariant

Derive state paths through the shared `../projectPath.ts` helpers; never
recompute SHA-1 from a display or canonical path. Loading a store normalizes
only task paths that match the physical project or its verified legacy storage
hash. Multiple legacy stores for one physical root are refused and preserved;
global load/backup sweeps continue past that project's identity conflict.

Load/canonicalize the projects index and run legacy global migration before
the first project cache read; then copy legacy
`<project>/.lattice/tasks.json` to the home location before `loadIfNeeded`.
Boot restore (`restoreAllProjectsFromBackup`) must run before any other task
read so the cache sees restored disk state.

## Crash-safety contract

- `updateTaskWith` accepts an async decision (e.g. rechecking the git head
  under the lock) and `{crashSafe:true}` for disk-first CAS transitions.
  `updateTaskCrashSafe` accepts a guard evaluated under that same lock.

- `updateTaskCrashSafe` writes disk **before** mutating cache — for one-way
  transitions (`ready_to_merge → qa`) where losing the update leaves the
  system inconsistent. On success it cancels the pending debounce so cache
  and disk agree.
- **Every read-modify-write takes the per-project write lock**
  (`runProjectWrite`; by-id mutators via `withLockedItemAcrossProjects`). After
  its disk-write `await`, `updateTaskCrashSafe` **re-reads the live cache** and
  re-applies only its own task's delta — never its pre-await full-list
  snapshot, which reverted sibling mutations that landed meanwhile (a run
  bump, a Stop-hook `/complete`) and dropped their scheduled persist.
  Read-only by-id helpers (`getTask`) stay **unlocked**.
- Base-class guarantees the task store relies on
  ([../projectState/CLAUDE.md](../projectState/CLAUDE.md)): debounced writes
  and flushes take the same lock (an already-fired timer can't overwrite a
  later crash-safe transition); writes are atomic temp→rename; a non-ENOENT
  read failure leaves the project unloaded (never cache an empty board over
  unread data); a parse failure moves the file to `<file>.corrupt-<ts>`, and
  if the bytes can't be preserved the key is write-protected. The task store
  opts into `flushOnExit` (a mutation still in its 100 ms debounce at
  `process.exit()` is written synchronously) — allowed only because its disk
  shape is its cached state.
- A `tasks.json` that parses but is **not an array** (`{}`, `null`) is
  corruption, not an empty board: `deserialize` throws so it takes the
  preserve-aside path. Backup, restore and migration share the same "valid =
  parses AND is an array" test.
- Subscriber fan-out is coalesced: N mutations of one project in one tick
  deliver ONE snapshot a `setImmediate` later (one `/ws/tasks` frame per bulk
  op). A test inspecting a subscriber after an awaited mutation must `await
  flushProjectNotifications()` first.
- Boot restores from `tasks.backup.json` only when the main file is
  **missing (ENOENT) or corrupt** — never on another read error (a transient
  Windows lock must not roll the DB back); a corrupt main file is moved to
  `.corrupt-<ts>` before the backup replaces it.
- First-touch migration treats a home dir holding EITHER `tasks.json` or
  `tasks.backup.json` as migrated, so a lost main file is restored from the
  recent backup, not the stale in-project legacy copy. The global legacy
  migration sets `~/.lattice/tasks.json` aside as `.unmigrated-<ts>` (never
  deletes it) when any row failed to migrate.
- `projects.json` writes are serialized and atomic (overlapping project opens
  or a failed write must not lose the index boot recovery depends on). A
  failed read stays unloaded and write-protects the existing index until a
  successful retry, so a corrupt index can't be replaced by an empty list
  plus the next registration. Loading canonicalizes, de-dups (case on
  Windows) and prunes, re-persisting.
- Index pruning only drops temp-dir scratch, shell-mangled, and phantom
  (gone-from-disk AND task-less) entries. A path that exists (or can't be
  stat'd for a reason other than ENOENT) or has task data is kept — including
  a corrupt/unreadable `tasks.json` or non-empty `tasks.backup.json`, which
  boot recovery restores.
- `stampTimestamps` clears `mergedAt` on a move back to a pre-merge lane so the
  next merge re-stamps it — the QA verdict guard depends on that.
- Storage lives under `~/.lattice/`, never inside the project tree, so a
  project-side catastrophe (`rm -rf .lattice`, `git clean -fdx`, a `.git`
  deletion) cannot reach it.

For a HOME-isolated single-file test invocation, see
[the test guide](../__tests__/CLAUDE.md). Tests: grep the module name in
`backend/src/__tests__/`.
