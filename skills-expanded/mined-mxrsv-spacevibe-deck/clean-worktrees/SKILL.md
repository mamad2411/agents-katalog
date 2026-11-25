---
name: clean-worktrees
description: Report which git worktrees and local branches of this repo are safe to remove, then remove only the rows the owner confirms. Use when the owner asks to clean or prune worktrees or branches, or `git worktree list` shows more than the three-worktree limit. Not for creating worktrees, merging, or deleting `backup/*` branches.
---

# Clean worktrees

[AGENTS.md](../../../AGENTS.md#sessions-and-checkouts) sets no cap on live worktrees; this skill
clears the ones made by hand under `../spacevibe-deck-worktrees/`. It reports first and removes only what the owner confirms, row by row. Run all
git commands from the primary checkout and read plans there by absolute path.

## Step 1: report only

Run `git fetch --prune origin` first so the `origin/main` and unpushed columns are not judged
against stale remote-tracking refs. No other git write command in this step. For every
worktree in `git worktree list --porcelain`, except the primary checkout, collect:

| Column | How |
| --- | --- |
| Path, branch or `detached` | porcelain output |
| Last commit date | `git log -1 --format=%cs <head>` |
| Merged | `git merge-base --is-ancestor <head> origin/main` exits 0, **or** the tip equals the `head.sha` of a merged PR (command below). Squash and rebase merges leave the branch off `origin/main`, so the ancestor test alone misses them. Note "local `main` only" separately |
| Dirty | the ignored-aware status below prints anything. Ignored files count: `git worktree remove` deletes them without `--force`, and `.env*` and `docs/plans/` are ignored here |
| Unpushed | `git rev-list <head> --not --remotes` is non-empty. A tip that equals a merged PR's `head.sha` has nothing unpushed |
| Detached, orphaned | `git branch -a --contains <head>` is empty |
| Live process | `lsof -a -d cwd -Fn` lines equal to `n<path>` or starting with `n<path>/` (the slash keeps `landing` from matching `landing-standout`). Never `lsof +D` (slow) |
| Recently touched | `find <path> -mmin -1440 -not -path '*/node_modules/*' -not -path '*/.git/*' -print -quit` prints a file. Agent sessions run from the primary checkout and edit worktrees by absolute path, so the process column cannot see them; this one can |
| Named by a plan | `grep -rl` the path and the branch name in the primary checkout's `docs/plans/` |

```bash
# Merged PR for a branch: prints "<number> <head.sha>"; compare with `git rev-parse <branch>`
gh api "repos/mxrsv/spacevibe-deck/pulls?state=closed&head=mxrsv:<branch>" \
  --jq '.[] | select(.merged_at) | "\(.number) \(.head.sha)"'
# Dirty, ignored files included; build output at any depth is dropped
git -C <path> status --porcelain --ignored \
  | grep -vE '^!! (.*/)?(node_modules|dist|dist-electron|dist-electron-app)/$'
```

Then list local branches that have no worktree, with the merged, unpushed and named-by-a-plan
columns. `backup/*` branches are left out of the table; report only their count.

Print one table and propose a verdict per row:

- `remove`: merged, clean, nothing unpushed, not orphaned, no live process, not recently
  touched, not named by a plan.
- `keep (reason)`: dirty, unpushed, orphaned or a live process — name which.
- `ask`: every other case — named by a plan, recently touched, merged into local `main` only.

Never propose `remove` for: the primary checkout, a dirty worktree (ignored files included), one
with unpushed or unreachable commits, a live process, a recent touch, a plan naming it, or a
`backup/*` branch.

End the report with two lines:

- `Not checked:` each column that could not be computed, and why.
- `Skill gaps:` edits you would make to this skill. Suggest only; do not edit it.

Stop here until the owner replies.

## Step 2: remove the confirmed rows

Only rows the owner named. Re-run the merged, dirty, unpushed, process and recently-touched
checks on each one first; the state may have changed since the report.

1. `git worktree remove <path>`. No `--force`.
2. `git branch -d <branch>`. Never `-D`, with one exception: `-d` refuses a squash- or
   rebase-merged branch, so `-D` is allowed only when the re-check just showed its tip equals a
   merged PR's `head.sha` (those commits stay on GitHub as `refs/pull/<n>/head`); name the PR in
   the report. Any other refusal: report it and leave the branch.

If any command fails or times out, stop. Report `git worktree list` and whether the directory
still exists. Do not retry, do not force, do not clean up the half-done state: a timed-out
worktree command is not a rollback (see [traps](../../../docs/internals/traps.md#data-and-contracts)).

## After removals

Run `git worktree prune --dry-run` and show its output. Run `git worktree prune` only if the
owner agrees. Finish by showing `git worktree list` and the count against the limit.
