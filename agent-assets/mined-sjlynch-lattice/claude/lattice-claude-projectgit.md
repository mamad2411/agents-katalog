# backend/src/worktree/projectGit

Policy modules for `projectGit(repoRoot, args, opts)` (`../projectGit.ts`), the
only allowed git wrapper for the user's main project repo. It asserts
`<repoRoot>/.git` exists, then validates argv and env before git runs.

- The boundary is intentional: project-repo git is capability-whitelisted;
  disposable task worktrees (and the read-only `../state.ts` probes) may use raw
  `exec('git', ...)` where real merges/conflicts are needed. A new raw call
  must be listed in `../../__tests__/rawGitAllowlist.test.ts`.
- `policy.ts` holds shared allow/read-only constants + argv helpers (the
  `SAFE_READ_OR_INDEX_ONLY` set, `LATTICE_BRANCH_RE`, `DisallowedProjectGitError`);
  `validators/` own one subcommand family each (`worktree`, `branch`, `merge`,
  `mergeFile`, `checkout`, `reset`, `rm`); dispatch + `gc`/`fetch`/`symbolic-ref`
  rules live in `../projectGit.ts` (`assertAllowedProjectGitArgs` is the
  unit-tested entry point).

## Allowed (everything else throws `DisallowedProjectGitError`)

- Reads (`SAFE_READ_OR_INDEX_ONLY`), `fetch`, `add`/`commit`/`rm --cached`,
  `bundle`, `count-objects`, read-only `symbolic-ref` (no `-d`, no write form).
- Any `worktree` op; `add -b/-B` only for `lattice/*`.
- `branch -d/-D/-f` only on `lattice/*`.
- `merge --ff-only`, not combined with `--no-ff`/`--ff`/`--squash`/`--no-commit`.
- `merge-file` only in its print form (`-p`/`--stdout`, no `--object-id`):
  snapshot restore's three-way merge (`../snapshot/threeWay.ts`) reads stdout;
  without `-p` git rewrites its first file argument.
- `checkout … -- <explicit paths>` and `reset [HEAD] -- <paths>` (no mode
  flags): path-only, never branch/HEAD movement. Checkout permits
  `:(literal)<real path>` (snapshot restore) but rejects other pathspec magic
  and empty/whole-tree paths, literal suffixes included.
- Exactly `gc --auto [--quiet]` (`../repoMaintenance.ts`; no `--prune=now`,
  `--aggressive`).

Keep destructive commands denied unless there is a narrow, tested need: no
`clean`, `stash`, `reset --hard`, `update-ref -d`, `checkout <branch>`, `push`,
non-ff merge, deleting non-`lattice/*` branches, or a leading global option
(`-C` would escape the declared cwd, `-c` smuggles config).

- **Env allowlist** (`assertAllowedProjectGitEnv`): only `GIT_LFS_SKIP_SMUDGE`.
  `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`, `GIT_CONFIG_*` would redirect git
  past the argv whitelist.

Tests: `backend/src/__tests__/projectGit.test.ts` (policy drift);
`taskWorktreeLfsPointers.test.ts` pins the env allowlist.
