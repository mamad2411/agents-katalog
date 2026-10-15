---
name: woostack-init
description: Use when initializing, scaffolding, or repairing the .woostack/ workspace — creates the memory store, specs and plans directories, config.json, and .gitignore from canonical templates, then runs the index builder and the `woostack-doctor` store linter. For ongoing workspace-health checks and convention repair, use [`woostack-doctor`](../woostack-doctor/SKILL.md). Invoke at project setup (brownfield) or from woostack-bootstrap (greenfield).
---

# woostack-init

## Overview

Creates or repairs the `.woostack/` workspace directory tree for a project. It
writes every missing piece from the skill's `templates/` directory, runs
`build-index.sh` to regenerate the derived memory index, and then runs
`doctor.sh` to lint the store. At the end it reports what was created, what
was skipped, and any doctor warnings or errors.

Two callers:

- **Brownfield (user-invoked):** the developer runs `/woostack-init` once to
  set up `.woostack/` in an existing project, or later to repair a partial or
  stale workspace.
- **Greenfield (via woostack-bootstrap):** the bootstrap skill calls
  `/woostack-init` as a step in its scaffolding sequence so every new project
  starts with a consistent workspace.

## Procedure

1. **Resolve the target directory.** If an argument is given, treat it as the
   project root; otherwise use the current working directory. Check whether
   `.woostack/` already exists and note each file that is present — these are
   candidates for the keep/overwrite prompt.

2. **Create missing pieces from `templates/`.** For each item below, create it
   only if it is absent (unless `--force` is active):

   | Item | Source |
   |---|---|
   | `.woostack/memory/` directory | (create empty) |
   | `.woostack/memory/.gitkeep` | (touch) |
   | `.woostack/specs/` directory | (create empty) |
   | `.woostack/plans/` directory | (create empty) |
   | `.woostack/fixes/` directory | (create empty) |
   | `.woostack/fixes/.gitkeep` | `templates/fixes/.gitkeep` |
   | `.woostack/wisdom/` directory | (create empty) |
   | `.woostack/wisdom/.gitkeep` | `templates/wisdom/.gitkeep` |
   | `.woostack/config.json` | `templates/config.json` (`{ "models": {}, "review": {}, "status": { "staleDays": 14 } }`) |
   | `.woostack/.gitignore` | `templates/gitignore` |
   | `.woostack/worktrees/` directory | (create empty — per-PR git worktrees, gitignored) |

   `config.json` ships as `{ "models": {}, "review": {}, "status": { "staleDays": 14 } }`. Each tool owns
   its own namespace inside that object: for the `review` namespace see
   [references/memory.md](references/memory.md); the `status` namespace holds `staleDays`
   (default 14 — the age in days past which an executing spec is flagged stale on the
   `/woostack-status` board), defined in
   [../woostack-status/references/conventions.md](../woostack-status/references/conventions.md).

   The optional top-level `base_branch` key sets the integration/trunk branch that base branches
   are cut from and PRs target; unset, it auto-detects the remote default (`origin/HEAD`, else
   `main`). Resolution lives in [`scripts/resolve-base.sh`](scripts/resolve-base.sh); the per-PR
   worktree lifecycle that consumes it is the [worktree contract](references/worktrees.md).

   **Host-specific scaffold:** after writing `config.json` (or if it is already present), run any
   scaffold step the current host's reference file names. **Host mechanics:** before any host-dependent step (subagent dispatch, scaffold, draft), load `skills/using-woostack/references/hosts/<current-host>.md`; no matching file -> treat the host as having no per-call routing and say so (degraded).
   (Under omp: run the generator to produce the gitignored tier defs — mechanics in `hosts/omp.md`.)

3. **Handle existing files.** For any file that already exists and `--force`
   is not active: prompt the user to keep or overwrite it. Under `--no-clobber`
   skip all existing files silently without prompting. After the run, state
   which mode was used (interactive / force / no-clobber) in the summary.

4. **Obsidian vault config (optional).** If `--obsidian` was passed, or if
   `--no-obsidian` was not passed and the user accepts the prompt ("Set up
   Obsidian vault config? [y/N]", default no), copy
   `templates/obsidian/` into `.woostack/.obsidian/`. Never clobber an
   existing `.woostack/.obsidian/` directory — skip silently if it is
   already present. This makes `.woostack/` an Obsidian vault so
   `memory/`, `specs/`, and `plans/` appear as a `[[wikilink]]` graph in the
   desktop app. Obsidian is **optional** — all memory tooling (`recall`,
   `doctor`, `build-index`) works without it.

5. **Run the scripts.**

   ```
   bash scripts/build-index.sh .woostack/memory
   bash ../woostack-doctor/scripts/doctor.sh .woostack/memory
   ```

   Run `build-index.sh` first so the index is current before `doctor.sh` checks
   for wikilink targets.

6. **Report.** Print a summary listing each file as `created` or `skipped`,
   then echo the doctor output (warnings and error count). If doctor exits
   non-zero, surface the errors prominently so the user can act on them before
   committing.

## Flags

- `--force` — overwrite every existing file without prompting. Use with
  caution: this will replace `memory.md`, `config.json`, and any notes that
  happen to share a template name.
- `--no-clobber` — skip every existing file silently, no prompts. Useful in
  automated contexts (CI, bootstrap) where the workspace may already be
  partially initialized.
- `--obsidian` — force-enable the optional Obsidian vault config scaffold
  (step 4) without prompting.
- `--no-obsidian` — force-skip the optional Obsidian vault config scaffold
  (step 4) without prompting.

## Hard constraints

- **Never clobber `memory.md`, notes, or `config.json`** without an explicit
  overwrite instruction (user confirmation or `--force`). These files contain
  project-specific knowledge that cannot be regenerated.
- **Legacy memory files are out of scope.** `/woostack-init` creates and repairs
  only the scoped `.woostack/memory/` store.
- **Other skills' files are out of scope.** Do not touch anything under
  `skills/`, `action.yml`, or any path outside `.woostack/` in the target
  project.
- **Pure bash, no new runtime dependencies.** The scripts (`build-index.sh`,
  `doctor.sh`, `scope-match.sh`) use only bash and coreutils. Do not introduce
  node, python, or any other runtime to fulfill this verb.
- **Obsidian is never required.** The `.obsidian/` scaffold is opt-in (step 4).
  All memory tooling (`recall`, `doctor`, `build-index`) works headlessly
  without Obsidian. See
  [references/memory.md](references/memory.md#9-obsidian-optional) for the
  full Obsidian integration contract.

## Reference

The full memory store contract — note frontmatter schema, glob semantics,
derived index format, recall procedure, and script usage — is in
[references/memory.md](references/memory.md).

The sibling `.woostack/wisdom/` store (generalized findings, wholesale-loaded) has its own
contract in [references/wisdom.md](references/wisdom.md).
