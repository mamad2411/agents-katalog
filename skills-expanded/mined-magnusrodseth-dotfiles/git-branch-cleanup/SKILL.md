---
name: git-branch-cleanup
description: Safely delete local git branches that are already merged, squash/rebase-merged, or whose remote was deleted, while protecting the current branch, the default branch, and any worktree-checked-out branch. Use when the user wants to clean up, prune, tidy, or delete "done"/merged/stale local branches, shrink a long `git branch` list, or remove branches after merging a PR.
---

# git-branch-cleanup

Remove finished local branches without risking unmerged work. The hard part is
that `git branch --merged` only sees branches reachable from the default branch —
it MISSES squash- and rebase-merged PRs (the common GitHub workflow). This skill
layers three signals and only auto-deletes the provably-safe set.

## Quick start

```bash
bash scripts/cleanup-branches.sh --fetch          # delete safe-merged, list the rest
bash scripts/cleanup-branches.sh --dry-run        # classify only, delete nothing
bash scripts/cleanup-branches.sh --fetch --force  # also -D the PR-merged / gone set
```

The script classifies every local branch into four buckets, deletes the **merged**
bucket with safe `git branch -d`, and prints the rest. Present its output to the
user; only re-run with `--force` after they confirm the squash-merged / gone set.

## What it protects (never deleted)

- The **current** branch and the **default** branch (`origin/HEAD`, else main/master/develop)
- Any branch **checked out in a worktree** (git refuses these anyway; the script skips them)

## Classification

| Bucket | Signal | Action |
|--------|--------|--------|
| Merged | `git for-each-ref --merged=<default>` (ancestor of default) | auto `git branch -d` (safe) |
| PR-merged | `gh pr list --state merged` head matches branch | list; `-D` only with `--force` |
| Gone | upstream tracking shows `[gone]` (remote branch deleted) | list; `-D` only with `--force` |
| Active | none of the above | KEPT |

## Workflow

1. `git fetch --prune` (or pass `--fetch`) so `[gone]` detection is accurate.
2. Run the script; review the four buckets with the user.
3. The merged bucket is already gone (safe `-d`). For the PR-merged / gone buckets,
   confirm with the user, then re-run with `--force` (or delete individually).
4. Mention deletions are recoverable from reflog (`git reflog`) for ~30 days.

## Safety rules

- Prefer `git branch -d` (refuses unmerged work). Use `-D` **only** for branches
  confirmed merged via a PR or whose remote is `[gone]`, and only after confirmation.
- Never delete the current branch, default branch, or worktree branches.
- Squash/rebase-merged branches are NOT ancestors of the default branch, so `-d`
  will refuse them — that is expected; rely on the `gh`/`[gone]` signals instead.

## Manual fallback (no script / explaining the steps)

```bash
default=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD | sed 's#origin/##')
git for-each-ref --merged="$default" --format='%(refname:short)' refs/heads/   # merged
git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads/ \
  | grep '\[gone\]'                                                            # gone
gh pr list --state merged --limit 300 --json headRefName --jq '.[].headRefName' # squash-merged
git worktree list                                                              # protect these
```

> Footgun encoded here: enumerate with `git for-each-ref` (porcelain), never
> `git branch | grep`. A naive `grep -v main` also strikes "**main**tenance",
> "do**main**", etc. Use exact, anchored matches.
