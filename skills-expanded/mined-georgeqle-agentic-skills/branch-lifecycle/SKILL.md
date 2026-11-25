---
name: branch-lifecycle
description: "Evaluate feature branches and decide whether to merge, salvage, keep open, or delete based on branch health, PR status, and stale-branch heuristics"
type: ops
version: v0.2
required_conventions: [alignment-page]
argument-hint: "[--force] [list | pr [branch...] | review <branch-or-pr> | merge <branch-or-pr> | salvage <branch-or-pr> [--onto <base>] [--commits <sha,...>] | cleanup]"
---

# Branch Lifecycle

Invoke as `$branch-lifecycle`.

Evaluate feature branches after review and drive one of four outcomes: `merge`, `salvage`, `keep-open`, or `delete`.

This is an exception workflow. The default repository policy is direct-to-primary development on `main`/`master`; use this skill for legacy branches, externally introduced branches, explicit user requests for branch/PR work, or `agent-team` lane branches created by an approved parallel plan.

## Arguments

- **No args** or **`list`**: inventory candidate branches and recommend an action for each.
- **`pr [branch...]`**: create PRs for branches that do not already have one and pass basic readiness checks.
- **`review <branch-or-pr>`**: classify a branch or PR as `merge`, `salvage`, `keep-open`, or `delete`.
- **`merge <branch-or-pr>`**: merge only if the strict merge gate passes.
- **`salvage <branch-or-pr> [--onto <base>] [--commits <sha,...>]`**: cherry-pick selected commits onto a fresh target branch.
- **`cleanup`**: delete merged branches and prompt for stale unmerged branches.
- **`--force`**: skip confirmations for safe-destructive actions (PR creation, approved merge, merged-branch deletion). Never skips confirmation for deleting an unmerged branch.

## Process

1. **Resolve repository context:**
   - Detect the base branch in this order: repository default branch, `main`, then `master`.
   - Run `git status` and report uncommitted changes before any mutating action.
   - Use `gh` for PR metadata and merge operations when available. If `gh` is unavailable or unauthenticated, report that limitation and continue with local-only facts where possible.
   - State clearly that normal solo-dev work should land directly on the base branch, not stay on a feature branch.

2. **Build branch inventory:**
   - Enumerate local branches except the current branch and base branch.
   - For each branch, gather:
     - Ahead/behind counts vs base: `git rev-list --left-right --count <base>...<branch>`
     - Last commit date/author: `git log -1 --format="%cr|%an" <branch>`
     - Unique commits vs base: `git log --reverse --oneline <base>..<branch>`
     - PR status and checks, when a PR exists
   - Flag a branch as **stale** when it has no open PR and its last commit is older than 30 days.

3. **Apply the decision policy:**
   - **Merge** only when all strict-gate checks pass:
     - focused scope
     - passing CI/tests or no required checks
     - no merge conflicts
     - approval requirements satisfied, or no required review
     - no unresolved high-severity review findings
   - **Salvage** when the branch is outdated, mixed in scope, or not merge-ready but contains specific commits worth keeping.
   - **Keep-open** when the branch is active and still worth finishing on its current line of development.
   - **Delete** when the branch is stale or below standards and no clearly valuable commits remain.
   - Increase confidence in a `delete` recommendation when stale is combined with any of:
     - behind base by 10 or more commits
     - failing or missing checks on an abandoned PR
     - obviously mixed or abandoned scope

4. **Execute the requested subcommand** using the rules below.

## Subcommand Actions

### `list`

1. Print a table with:
   - branch
   - age
   - ahead/behind
   - PR status
   - checks
   - recommendation
2. Use `merge`, `salvage`, `keep-open`, or `delete` in the recommendation column.
3. Include a brief reason for non-merge recommendations, such as `stale`, `mixed scope`, `behind base`, or `failing checks`.

### `pr [branch...]`

1. Use the supplied branches, or find local branches without an open PR.
2. Refuse to create a PR for:
   - the current branch
   - the base branch
   - branches already marked `delete`
3. For each eligible branch:
   - summarize commits unique to the branch
   - confirm with the user unless `--force`
   - create the PR with `gh pr create`
4. If a branch is a better `salvage` candidate than a PR candidate, say so and do not open the PR automatically.

### `review <branch-or-pr>`

1. Resolve the target to a branch and, if present, its PR.
2. Evaluate:
   - scope focus
   - CI/tests
   - conflicts
   - approval state
   - stale status
   - whether the branch contains a small set of clearly reusable commits
3. Output:
   - target summary
   - branch facts
   - findings
   - recommended action: `merge`, `salvage`, `keep-open`, or `delete`
   - the reason tied to the decision policy

### `merge <branch-or-pr>`

1. Resolve the target to an open PR. If the branch has no PR, stop and recommend `pr` or `salvage`.
2. Re-check the strict merge gate.
3. If any merge gate fails, stop and explain which requirement failed.
4. Confirm with the user unless `--force`.
5. Merge with squash by default: `gh pr merge <number> --squash`
   - Respect `CLAUDE.md` if it specifies a different merge strategy.
6. Report the merged PR and resulting commit hash.

### `salvage <branch-or-pr> [--onto <base>] [--commits <sha,...>]`

1. Resolve the source branch and target base branch.
   - Default target base is the detected repository base branch.
   - If `--onto` is provided, use that branch as the target base.
2. Show the commit list unique to the source branch in chronological order.
3. Determine which commits to keep:
   - if `--commits` is provided, use those SHAs in the given order
   - otherwise, ask the user to choose commits explicitly
4. Create a fresh target branch from the chosen base, using a name derived from the source branch such as `salvage/<source>-<date>`.
5. Cherry-pick the selected commits in order.
6. If a conflict occurs:
   - stop immediately
   - report the conflicted files and the standard `git cherry-pick --continue` / `--abort` next steps
   - do not auto-resolve or continue
7. Report the new branch name and the preserved commits.
8. Never delete the source branch automatically after salvage.

### `cleanup`

1. Find merged branches and confirm deletion unless `--force`.
2. Delete local merged branches with `git branch -d`.
3. If the matching remote branch exists, delete it too after the same confirmation scope.
4. Identify stale unmerged branches and print their recommendation reasons.
5. Ask for confirmation before deleting each unmerged branch individually.
   - Even with `--force`, never auto-delete an unmerged branch.
6. If a stale branch looks salvageable, recommend `salvage` instead of deleting it immediately.

## Constraints

- Never force-push or rewrite history.
- Never merge a PR that fails the strict gate.
- Never auto-delete an unmerged branch.
- Never auto-delete a source branch after salvage.
- Never cherry-pick the full branch implicitly; salvage is commit-selective by default.
- If the working tree is dirty and the requested action is mutating, warn first and stop unless the user explicitly wants to continue.
- Prefer reporting and stopping over making branch-history decisions silently.


## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/branch-lifecycle-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
