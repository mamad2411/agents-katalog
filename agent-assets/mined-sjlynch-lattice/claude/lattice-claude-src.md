# backend/src

Express server (`:5184`) plus a detached PTY executor (`terminal-server.ts`,
`:5185`). **To find which module owns X, read `MAP.md`** (this folder: every
module, one line each). A folder with its own `CLAUDE.md` owns its detail —
read it before changing that folder.

## Module layout

Pinned by `__tests__/moduleLayout.test.ts`: a domain's public surface is a root
`x.ts` facade beside its `x/` folder (`worktree.ts` over `worktree/`); never an
`x/index.ts`. Import the facade, not the folder's internals.

## Use the one helper — don't hand-roll a second

- JSON store/config writes: `fsAtomic.ts` `atomicWriteFile` (crash-safe temp→rename).
- In-process pub/sub: `emitter.ts` `createEmitter(label)`, never a hand-rolled listener `Set`.
- Per-project paths and route guards: `projectPath.ts`; key per-project state
  and watchers by `canonicalProjectPath` (a new path spelling duplicates them).
- Process-tree kills: `processTree.ts`. Bounded external CLI calls: `spawnWithTimeout.ts`.
- Overlapping read-modify-writes: `serializeWrites.ts` `runExclusive`.
- Harness names: `harnesses.ts` (over `shared/harnesses.ts`) — never open-code a harness union.
- `~/.lattice` secrets: `persistedSecretFile.ts` — never overwrite a secret you couldn't read.
- Long-lived collections / listener sets: `registerMemGauge` (`memDiag/CLAUDE.md`).

## Key invariants

- **One active merge run per project** — in-process (`mergeRuns.ts`, second
  start → 409) *and* cross-process (`projectRunLock.ts`).
- **Runs survive a backend restart, so every run step is re-runnable.**
  Workflow, push, QA and post-merge-hook runs are mirrored under
  `per-project/<hash>/` and re-adopted at boot (one-off runs before listen, so
  callbacks land); merge runs restart from a stale `run.lock`, so
  `startMergeRun` must tolerate a half-processed task set. Keep each mirror
  current on every run mutation and every resume idempotent
  (`recovery/CLAUDE.md`, `mergeRuns/CLAUDE.md`, `workflowRuns/CLAUDE.md`).
- **Per-task merge lock** (`mergeLocks.ts`) — a manual `/merge` can't race the run worker.
- **Crash-safe ordering** — `updateTaskCrashSafe` writes disk before cache;
  used for `ready_to_merge → qa`.
- **Merge in the worktree, not main** — main's tree only ever changes by
  fast-forward (`worktree/merge/CLAUDE.md`).
- **All project-repo git goes through `projectGit`** — a raw `exec('git', …)`
  is allowed only in the modules `__tests__/rawGitAllowlist.test.ts` lists
  (worktree-side git, which needs the real `git merge` `projectGit` forbids;
  read-only probes of paths that may not be a repo root; Git Setup's
  `git init`). A new raw call fails that test.
- **No `fs.rm({recursive})` on anything inside a project** — worktrees live
  outside the tree and teardown delegates to `git worktree remove`. One-off
  scratch cleanup is an intentional recursive delete, bounded to
  `per-project/<hash>/{push,qa,post-merge-hooks,reviews}/<id>/` with path +
  reparse-point guards (`homeScratch/CLAUDE.md`).
- **Executor imports** — every file `terminal-server.ts` reaches is in
  `terminalFingerprint.ts`'s `FINGERPRINT_FILES`; never import
  `latticeApiDocs.ts` from terminal-server code (use `latticeApiDocs/docPath.ts`)
  — every API tweak would mark the executor stale.

Scripts, type-check, tests and non-TS runtime assets (`copy-assets.mjs`):
`../CLAUDE.md`. Test conventions and cross-cutting guard tests:
`__tests__/CLAUDE.md`.
