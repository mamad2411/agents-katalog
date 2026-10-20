---
description: Remove finished git worktrees — merged and clean ones by default; `all` force-removes every worktree after confirmation
argument-hint: [all]
---

# /clean-worktree — remove finished worktrees

Input: `$ARGUMENTS` — empty for the safe default (remove only merged, clean worktrees), or `all` to force-remove every worktree.

## Gather state

1. `git fetch --prune origin`
2. `git worktree list --porcelain` — the first entry is the **primary checkout**: never remove it and never delete its branch. Every other entry is a candidate, wherever it lives on disk (not just `.claude/worktrees/`).
3. For each candidate collect:
   - **Branch** — or detached HEAD.
   - **Dirty?** — `git -C <path> status --porcelain` prints anything.
   - **Merged?** — `git merge-base --is-ancestor <branch> origin/main` succeeds, **or** the branch has a merged PR: `gh pr list --head <branch> --state merged --json number` returns a non-empty array. The second check matters — squash/rebase merges are never ancestors of `main`.

## Default mode (no argument)

Remove each candidate that is **merged and not dirty**; skip everything else.

For each removal:

1. If the session is currently inside that worktree, leave it first with ExitWorktree (`action: "keep"`); if leaving isn't possible, skip the worktree and say so.
2. `git worktree remove <path>` — if it refuses and the blockers are only disposable untracked files (build output and the like), retry with `--force`; anything else, skip and report.
3. `git branch -D <branch>` (`-D` because squash-merged branches are not ancestors of `main`; merge status was already verified above).

Detached-HEAD, dirty, and unmerged worktrees are skipped in this mode — never silently: report each skip with its reason.

## `all` mode

This mode destroys unmerged work, so it confirms first:

1. List every candidate with its branch, merged state, and dirty state.
2. Confirm with the user (AskUserQuestion) before deleting anything, explicitly calling out which worktrees are unmerged or have uncommitted changes — those changes are lost for good.
3. On confirmation: leave the current worktree if needed (as above), then for each candidate `git worktree remove --force <path>` and `git branch -D <branch>`.

## Wrap up

Run `git worktree prune`, then report a summary: which worktrees were removed, which were skipped and why.
