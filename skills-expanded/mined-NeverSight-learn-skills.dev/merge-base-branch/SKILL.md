---
name: merge-base-branch
version: 2.0.1
description: Select base branch (from .agent, git history, or main), fetch, stop if already up to date, commit all WIP, merge, resolve conflicts, then lint, tests at 100% coverage, and build—with commits after each fix phase.
argument-hint: ""
---

Merge the chosen base branch into the current branch and finish with a clean lint, full test coverage, and successful build. Use when you want the branch fully reconciled with its parent and CI-quality checks passing locally.

**Usage:**
- `/merge-base-branch` — Run the full workflow below

**Prerequisites:**
- Repository root must be a git checkout on a named branch (not detached HEAD).
- If the project uses Node/npm, `package.json` must define scripts `lint`, `test:coverage`, and `build`. If `package.json` is missing or any of those scripts is missing, report what is absent and **STOP** (do not merge or proceed without the mandated checks).

**Instructions:**

1. **Current branch:**
   - Run `git branch --show-current`. If detached HEAD, inform the user and **STOP**.

2. **Determine base branch candidate, then let the user choose:**
   - **First**, if `.agent` exists at the repo root, read it for `baseBranch=<value>`. That value is the **detected candidate** (if present).
   - **Else**, infer from git: run `git merge-base --fork-point main HEAD`, `git merge-base --fork-point master HEAD`, and `git merge-base --fork-point develop HEAD`. Any branch name that returns a commit is a match. If exactly one matches, that is the **detected candidate**. If several match, choose by priority: `main`, then `master`, then `develop`. If none match, **detected candidate** is unset.
   - Use `AskUserQuestion` so the user picks the base branch to merge. **Always** include `main` as an option. Include the **detected candidate** as an option when it is set and differs from `main`. Include `master` and `develop` as additional options when they exist on `origin` (or locally). Include a short label on each option (e.g. “Detected from history: develop”). Wait for the answer; the selected branch is `<base-branch>`.

3. **Verify base branch and fetch:**
   - Confirm with `git rev-parse --verify origin/<base-branch>` or, failing that, `git rev-parse --verify <base-branch>`. If neither exists, inform the user and **STOP**.
   - Run `git fetch origin <base-branch>`. On failure, show the error and **STOP**.

4. **Stop if already up to date with the base:**
   - Let `<merge-ref>` be `origin/<base-branch>` when that ref exists after fetch; otherwise `<base-branch>` (local only).
   - Run `git rev-list --count HEAD..<merge-ref>` (or equivalent: no commits in `git log --oneline HEAD..<merge-ref>`).
   - If the count is **0**, inform the user that the current branch already contains everything from `<merge-ref>` and no merge is needed. If the working tree is not clean, note that uncommitted changes remain. **STOP** (do not commit WIP for this workflow, merge, or run lint/tests/build).

5. **Commit all uncommitted work before merge:**
   - If `git status` shows no unstaged/staged/untracked changes that need committing, skip to step 6.
   - Otherwise stage and commit **everything** in the working tree (not limited to files touched in the current session). Split into **multiple commits** when the diff clearly contains separate logical chunks (e.g. group by feature area or directory); each commit gets a clear message. Use `git add` selectively (or `git add -p`) to build coherent commits—do not squash unrelated work into one commit when multiple distinct chunks exist.

6. **Merge base branch:**
   - Run `git merge origin/<base-branch> --no-edit` (use `git merge <base-branch> --no-edit` only if there is no `origin/<base-branch>` but the local branch exists).
   - If the merge succeeds, summarize merged commits briefly.

7. **Resolve conflicts and conclude merge:**
   - On conflicts: list with `git diff --name-only --diff-filter=U`, resolve each file (remove conflict markers; combine or choose per intent—prefer base for upstream fixes, keep branch work for feature code), `git add` each resolved file, then `git merge --continue --no-edit` until the merge completes.

8. **Lint:**
   - From repo root, run `npm run lint`. Fix all reported issues; re-run until it passes.

9. **Commit after lint (if anything changed):**
   - If lint fixes (or formatter churn) changed files, commit with an appropriate message (one or more commits if chunks warrant it).

10. **Tests with coverage:**
    - Run `npm run test:coverage`. If it fails, read the coverage report and any failure output; add or adjust tests until **all lines are covered at 100%** (per project/tooling). Re-run and iterate until the command succeeds.

11. **Commit test/coverage changes:**
    - Commit any test or source changes from step 10 with a clear message.

12. **Build:**
    - Run `npm run build`. Fix compile/bundler errors; re-run until it passes.

13. **Commit build fixes (if any):**
    - Commit if step 12 produced file changes.

**Summary for the user:** base branch used, merge result (or “already up to date”), lint/test/build outcomes, and list of commits created during the run.
