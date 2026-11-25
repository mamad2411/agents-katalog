---
name: resolve-merge-conflicts
description: "Use when git merge, rebase, or cherry-pick halts on conflict markers, unmerged paths, or merge conflicts in source files or lockfiles."
---

# Resolve Merge Conflicts

## Overview

A merge conflict occurs when two branches make conflicting assumptions about the same lines or files. Resolving a conflict means understanding the intent of both changes, reconciling them into a coherent whole, and verifying syntactic and semantic correctness before continuing.

## When to Use

Use this skill when:
- Git stops during `merge`, `rebase`, `cherry-pick`, or `stash pop` with `CONFLICT (content)` or unmerged paths.
- Files contain conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
- Machine-generated lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `Cargo.lock`) conflict after dependency updates.
- Git status reports unmerged paths (`UU`, `AA`, `UD`, `DU`).

## Quick Reference

| Task | Command | Caveat |
|---|---|---|
| List unmerged files | `git status --short` (look for `UU`, `AA`, `UD`) | Run first before touching code |
| Show conflict markers | `git diff --check` | Detects leftover `<<<<<<<` markers |
| View 3-way diff | `git diff` | Shows conflict blocks with local vs incoming |
| View base, ours, theirs | `git show :1:<file>` (base), `:2:<file>` (ours), `:3:<file>` (theirs) | Inspect original shared ancestor |
| Stage resolved file | `git add <file>` | Only after verifying syntax and tests |
| Continue operation | `git merge --continue` or `git rebase --continue` | Never commit directly during rebase |
| Abort safely | `git merge --abort` or `git rebase --abort` | Returns working tree to clean pre-op state |

## The Rebase Inversion Trap

The meaning of `--ours` and `--theirs` depends on the operation:

| Operation | `HEAD` represents | `--ours` refers to | `--theirs` refers to |
|---|---|---|---|
| `git merge` | Current branch | Current branch (target) | Incoming branch (source) |
| `git rebase` | Upstream target commit | Upstream branch (rebase target) | Your feature branch (commit being replayed) |

In a rebase, Git checks out the upstream target and replays feature commits on top. Running `git checkout --ours` during a rebase discards your feature branch changes and retains upstream. Running `git checkout --theirs` keeps your feature branch and discards upstream.

## Resolution Protocol

### Step 1: Identify and Orient

1. Run `git status` to determine:
   - Operation type: merge, rebase, cherry-pick, or revert.
   - List of unmerged paths.
2. If in a rebase, note the rebase target (`onto`) and the commit being applied.
3. Identify file categories:
   - Source code files (require surgical reconciliation).
   - Lockfiles and generated files (require manifest resolution followed by regeneration).
   - Deleted files (one side deleted, one side modified).

### Step 2: Separate Code from Lockfiles

**Never manually edit conflict markers in generated lockfiles** (`pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `Cargo.lock`, `poetry.lock`).

For lockfiles:
1. Reconcile the human-edited manifest first (`package.json`, `Cargo.toml`, `pyproject.toml`).
2. Accept one version of the lockfile temporarily (e.g. `git checkout --ours -- <lockfile>`).
3. Run the package manager's install command to recalculate the lockfile graph deterministically:
   - pnpm: `pnpm install`
   - npm: `npm install`
   - yarn: `yarn install`
   - cargo: `cargo generate-lockfile` (or `cargo check`)
   - poetry: `poetry lock --no-update`
4. Verify the lockfile updated cleanly and stage both the manifest and the lockfile.

### Step 3: Surgically Reconcile Source Files

1. Open each conflicting file and locate every conflict block:
   ```text
   <<<<<<< HEAD
   current changes
   =======
   incoming changes
   >>>>>>> branch-or-commit
   ```
2. Understand the intent of both sides:
   - Why did branch A make this change?
   - Why did branch B make this change?
3. Combine the changes so both intents survive:
   - If both added imports or dependencies, keep both (sorted, deduplicated).
   - If one updated a function signature and the other added call sites, update the call sites to match the new signature.
   - If both edited the same configuration block, merge keys without dropping either side's new settings.
4. Remove all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
5. Touch only the conflicting lines and necessary call sites. Do not reformat or refactor adjacent code.

### Step 4: Verify Syntactic and Semantic Correctness

Removing conflict markers is only textual reconciliation. You must verify semantics:

1. Check for leftover markers:
   ```bash
   git diff --check
   ```
   If any marker remains, Git prints the file and line number. Fix immediately.
2. Run language typechecking and linting:
   - TypeScript/JavaScript: `npm run typecheck` or `npx tsc --noEmit`
   - Python: `mypy .` or python syntax check `python -m py_compile <file>`
   - Go: `go vet ./...`
   - Rust: `cargo check`
3. Run affected test suites to verify that both features still work together.

### Step 5: Stage and Conclude

1. Stage resolved files:
   ```bash
   git add <resolved-file>
   ```
2. Check status:
   ```bash
   git status
   ```
   Ensure no unmerged paths remain.
3. Conclude the step:
   - If merging: `git commit` (or `git merge --continue`).
   - If rebasing: `git rebase --continue`.
   - If cherry-picking: `git cherry-pick --continue`.
4. If rebasing across multiple commits, repeat Steps 1 to 5 for each conflicting commit until the rebase completes.

## Rationalization Table

| Excuse | Reality |
|---|---|
| "Deploy window closes soon, take ours to make it fast" | Discarding either side breaks production functionality or compliance. Fast bad merges cause immediate production outages. Reconcile both or abort. |
| "I will resolve the text now and fix compilation in a follow-up commit" | Half-merged commits break git bisect, fail CI gates, and risk shipping broken code. Verify before continuing. |
| "The conflict was only 2 lines, running tests is unnecessary" | Two-line changes in signatures or configs cause runtime exceptions. Always run compiler checks or tests. |
| "Teammate said run `checkout --ours`" | During rebase, `--ours` is the upstream branch, not your feature branch. Blind checkout silently deletes feature code. |
| "I can hand-edit the 200 lines of conflict in pnpm-lock.yaml" | Hand-edited lockfiles corrupt dependency trees and checksums. Reconcile package.json and run the package manager install command. |
| "Git status shows no markers, so the merge succeeded" | Removing markers resolves text layout, not semantic compatibility. New calls to changed signatures still fail. |

## Red Flags: STOP and Review

- Using `git checkout --ours` or `git checkout --theirs` on whole source files without line-by-line inspection.
- Staging files before running `git diff --check`.
- Running `git rebase --continue` or `git commit` without running typechecks or tests.
- Manually editing YAML or JSON in lockfiles.
- Running `git reset --hard` or deleting files when confused by rebase state (use `--abort` instead).
- Refactoring lines outside the conflict region during resolution.

## Common Mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Direct commit during rebase | Detached HEAD or nested commit loop | Stage with `git add <file>` and run `git rebase --continue` |
| Dropping settings in configs | Missing feature flag or key | Combine all new keys into the config dictionary |
| Deleted vs Modified (`UD`/`DU`) | `CONFLICT (modify/delete)` | Run `git add <file>` to retain or `git rm <file>` to delete |
