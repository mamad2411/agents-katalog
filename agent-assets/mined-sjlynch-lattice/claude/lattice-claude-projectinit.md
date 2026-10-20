# backend/src/projectInit

Turns a folder that isn't a git repo into one Lattice can use: probe → preview
→ `git init` + starter `.gitignore` + first commit. Served by
`routes/projectInit.ts` (`POST /api/project-init/preview`, `POST /api/project-init`)
and surfaced additively on `GET /api/git-check`.

Without it, opening a non-repo folder dead-ends: `routes/tasks/projectValidation.ts`
400s every task create, because a task can only ever run in a worktree.

## Files

- `types.ts` — the wire contract the frontend re-exports via
  `../shared/wireTypes.ts` (`ProjectGitState`, `ProjectGitProbe`,
  `ProjectInitPreview`, `ProjectInitResult`; keep it node-free) plus
  `ProjectInitError`, the typed failure whose `code` the route maps to
  409 / 422 / 500 / 503.
- `probe.ts` — `probeProjectGit(project)`. `fs.stat(<project>/.git)` fast path
  (dir OR file), then the walk-up `rev-parse` (see invariant 1), then the bare
  check, then the path guards.
- `guards.ts` — `refuseInitReason(canonicalPath)`: home dir, filesystem/drive
  roots, anything under `~/.lattice`, Windows system trees, non-directories,
  and unwritable dirs. Returns the human-readable reason the dialog shows.
- `gitignoreTemplate.ts` — `buildStarterGitignore(repoRoot)`, composed from
  `health/constants.ts`'s `IGNORE_DIR_NAMES`, `worktree/managedFiles.ts`'s
  `LATTICE_GITIGNORE_ENTRIES`, and `worktree/envDetect.ts`'s detected
  ecosystems — plus secrets and OS/editor noise.
- `preview.ts` — `previewProjectInit(project, gitignore?)`: bounded, symlink-
  refusing walk counting what the first commit would capture. The pattern
  matcher is a deliberate subset of gitignore syntax; git is authoritative at
  commit time (see the file header).
- `init.ts` — `initProjectGit(project, {gitignore?})`, serialized per project
  through `runExclusive`. **`.gitignore` precedence:** an explicit `gitignore`
  wins over a file already on disk (it only ever comes from the dialog, where
  the user saw that exact text *and* the file count it produces — keeping the
  old file would make the count they approved describe a different commit);
  with no explicit text a `.gitignore` the project brought is left untouched.
  Either way `ensureLatticeGitignore` runs before `add -A`, so a user who edits
  the Lattice entries out can't commit `.lattice/` scratch. Also exports
  `isMissingIdentityFailure(stderr)` —
  the string match that stands in for the identity probe we're not allowed to
  run (invariant 2), pinned against git's real message text in
  `__tests__/projectInit.test.ts`.

## Unborn repos

A repo whose `git init` ran but whose first commit never landed — the usual
cause is a missing git identity aborting `initProjectGit` at the commit — is
reported by the probe as `state: 'repo'` + `unborn: true` + `initable: true`
(decided by `git rev-parse --verify -q HEAD` exiting 1; a 128 is a repo git
cannot open at all and is left alone). `initProjectGit` accepts that state and
skips `git init`, so the navbar's "finish setup" chip / the Git Setup dialog
can complete the job once the identity exists. Without this the project was a
dead end: `GET /api/git-check` said `repo`, init said 409, and no task could
ever run (`git worktree add` has no HEAD to branch from). The navbar chip also
stopped vanishing for these: `gitBranch.ts` names the branch with
`symbolic-ref --short HEAD`, which works on an unborn HEAD, where
`rev-parse --abbrev-ref HEAD` does not.

## Slow first commits

The folder being adopted is often a large existing project, so `add -A` and the
first `commit` run under `GIT_SLOW_TIMEOUT_MS` (20 min) rather than the 30 s
quick-call bound (`init`, `diff --cached`, `rev-parse`). A few GB / tens of
thousands of files overran 30 s on Windows (Defender scans every new loose
object), and a signed commit can sit on a passphrase prompt. On a timeout kill
(`runSlowGit`) the `index.lock` the killed git left — absent before the call,
present after it; we hold the per-project `runExclusive` lock — is unlinked, and
the user gets a "took longer than N minutes" message instead of exec's raw kill
marker. The unborn "finish setup" path also runs `clearStaleGitLocks(root)`
first and refuses with a readable message while a lock is still held or fresh.
Before this, the first timeout left `index.lock` behind and every retry failed
at once with "File exists" — the folder could never be initialized
(`__tests__/projectInit.test.ts` stubs a timed-out `add` via the
`InitProjectGitDeps` seam).

## Invariants

1. **Walk-up detection, always.** `'nested'` (a repo exists ABOVE this folder)
   must be decided by `git rev-parse --show-toplevel`, never by
   `fs.stat(<project>/.git)`. A subdirectory of a monorepo looks repo-less to
   `stat`, and initializing there creates a nested repo the parent sees as a
   bare gitlink — the worst outcome this feature can produce.
2. **Never touch a git identity.** No probing, no setting, no env overrides —
   `__tests__/gitIdentityUntouched.test.ts` scans every shipped source file for
   the literals involved. A missing identity is detected from git's stderr
   (`/Author identity unknown|Please tell me who you are|unable to auto-detect/i`)
   and surfaced as `422 git-identity-missing` with git's RAW stderr as `detail`;
   the user-facing fix instructions live in the frontend, which that test does
   not scan.

Other standing rules this module inherits: `init` stays OFF the `projectGit`
whitelist (the pre-`.git` `init`/`rev-parse` calls use plain `exec`, everything
after goes through `projectGit`), and nothing here deletes anything except
the single-file `index.lock` unlink above (and `clearStaleGitLocks`'s own) —
`fs.rm` never appears, recursively or otherwise.
