---
name: sign-commits
description: Re-sign unsigned commits on the current branch or pull request without changing code content by rewriting only from the first unsigned commit onward on a temporary branch. Use when asked to sign commits, add GPG signatures to an existing branch, satisfy signed-commit requirements, or make a PR show verified commits. Creates a backup branch first, runs the rebase non-interactively, verifies the rewritten final tree exactly matches the original branch tip, and stops immediately if any check, conflict, drift, or GPG step fails.
license: MIT
---

# Sign Existing Commits

Re-sign unsigned branch commits while preserving commit messages and file content.

## When to Use This Skill

- When a branch or pull request has several unsigned commits
- When a repository or branch protection rule requires signed commits
- When you need to re-sign history without changing the code snapshots
- When you want a backup branch before rewriting commit history

Keywords: sign commits, GPG sign branch, re-sign PR commits, verified commits, signed history.

## Prerequisites

- Run from the repository root
- `git` is available and authenticated to the remote
- The wrapper script is available at `scripts/sign-commits.sh`
- The signing configuration check script is available at `scripts/git/check-commit-signing-configuration.sh`
- The branch contains only commits that are safe to rewrite

## Safety Model

- Create a backup branch before rewriting history
- Rewrite on a temporary branch so the original branch stays untouched until verification passes
- Fail fast on any errors or obstacles
- Stop immediately on any rebase conflict or GPG failure
- Skip commit hooks during `--amend` so hooks cannot block a metadata-only rewrite
- Preserve commit messages and the exact final tree of the original branch tip

## Scripted Workflow

Use the wrapper script for the normal path:

```bash
bash scripts/sign-commits.sh
```

The script performs the same workflow documented below:

- checks for a clean working tree and a checked-out branch
- fetches `origin/main`
- validates Git and GPG signing configuration
- verifies the branch already contains the latest `origin/main`
- creates a backup branch
- creates a temporary rewrite branch
- finds the first unsigned branch commit and rewrites only that suffix of history
- re-signs each rewritten commit with `--no-verify --allow-empty`
- suppresses rebase todo and commit-message editors for non-interactive execution
- verifies the rewritten final tree exactly matches the original branch tip before updating the real branch ref
- verifies signatures and checks for zero content drift after switching the real branch to the verified rewrite
- pushes with `--force-with-lease`

## Step-by-Step Workflow

### 1. Inspect Current Branch

Run:

```bash
git branch --show-current
git status --short
```

Stop and report to the user if:

- no branch is checked out
- the working tree is not clean

### 2. Refresh Main and Run Checks

Run:

```bash
git fetch origin main
bash scripts/git/check-commit-signing-configuration.sh
git merge-base --is-ancestor origin/main HEAD
```

Interpretation:

- `git fetch origin main` must succeed
- `bash scripts/git/check-commit-signing-configuration.sh` must succeed
- `git merge-base --is-ancestor origin/main HEAD` must exit with code `0`

Stop and report to the user if:

- fetch fails
- the signing configuration check fails
- the current branch is not up to date with `origin/main`

If the branch is behind `origin/main`, stop. Rebase or merge `origin/main` first, resolve that separately, and only then return to this workflow.

### 3. Create Backup Branch First

Run:

```bash
iso_timestamp="$(date -u +%Y-%m-%dT%H-%M-%SZ)"
current_branch="$(git branch --show-current)"
backup_branch="backup/${current_branch}/${iso_timestamp}"

git branch "$backup_branch"
git branch --list "$backup_branch"
```

Stop and report to the user if:

- the backup branch cannot be created
- the backup branch cannot be verified

Recovery path:

```bash
git switch "$backup_branch"
```

### 4. Create a Temporary Rewrite Branch

Run:

```bash
temporary_branch="tmp/sign-commits/<branch-name>/<timestamp>"
git switch -c "$temporary_branch"
```

Purpose:

- keep the original branch ref unchanged during the rewrite
- make it safe to abandon a failed rewrite without moving the user-facing branch

### 5. Find the First Unsigned Commit

Run:

```bash
git rev-list --reverse --format='%H %G?' origin/main..HEAD | sed '/^commit /d'
```

Interpretation:

- find the first commit whose signature status is not `G` or `U`
- if no such commit exists, stop successfully because nothing needs rewriting
- rewrite starts from that unsigned commit through `HEAD`

### 6. Re-sign the Necessary Branch Suffix

Run:

```bash
first_unsigned_commit='<first unsigned sha>'
rewrite_base_commit="$(git rev-parse "${first_unsigned_commit}^")"

GIT_SEQUENCE_EDITOR=: GIT_EDITOR=: \
git rebase --exec 'git commit --amend --no-edit -S --no-verify --allow-empty' "$rewrite_base_commit"
```

This does the following:

- rewrites only commits from the first unsigned commit onward
- amends each replayed commit with a GPG signature
- keeps the existing commit message with `--no-edit`
- skips commit hooks with `--no-verify`
- tolerates empty replayed commits with `--allow-empty`
- suppresses the rebase todo editor with `GIT_SEQUENCE_EDITOR=:`
- suppresses the commit-message editor with `GIT_EDITOR=:`

Stop and report to the user immediately if:

- the rebase stops for a conflict
- GPG signing fails
- the `--exec` amend step fails for any commit

Do not continue automatically after a failure. Surface the exact failure and wait for the user.

### 7. Verify Exact Final-Tree Equality

Run:

```bash
original_head_tree="$(git rev-parse <original-branch-tip>^{tree})"
rewritten_head_tree="$(git rev-parse HEAD^{tree})"
```

Expected result:

- `rewritten_head_tree` exactly equals `original_head_tree`
- if they differ, stop and leave the original branch unchanged

Only after this check passes:

```bash
git switch <original-branch>
git reset --hard <temporary-branch>
```

### 8. Verify the Result

Run:

```bash
git log --show-signature --oneline origin/main..HEAD
git diff --stat "$backup_branch"..HEAD
```

Expected result:

- every rewritten branch commit shows a valid signature
- `git diff --stat "$backup_branch"..HEAD` shows no file-content changes

Stop and report to the user if:

- any commit is still unsigned
- the diff shows unexpected content changes

### 7. Update the Remote Branch

Run:

```bash
git push --force-with-lease
```

Stop and report to the user if the push fails.

## Troubleshooting

| Problem | Cause | Fix |
| --- | --- | --- |
| Working tree is dirty | Local changes would be mixed into the rewrite | Stop and clean or stash changes first |
| Signing configuration check fails | Git or GPG is not configured for commit signing | Run `bash scripts/git/check-commit-signing-configuration.sh`, fix the reported issue, and stop until it passes |
| Branch is behind `origin/main` | The rewrite would also need to integrate upstream changes | Stop and rebase or merge `origin/main` first |
| Rebase conflict occurs | A commit does not replay cleanly | Stop and let the user decide whether to resolve or abort; the original branch remains untouched because the rewrite runs on a temporary branch |
| Final code differs after re-signing | The replay did not produce the original branch tip's exact tree | Compare the temporary branch against the original tip and stop; do not move the original branch ref |
| VS Code opens the interactive rebase or commit-message editor | Git is using VS Code as its editor | Use `GIT_SEQUENCE_EDITOR=:` and `GIT_EDITOR=:` for this workflow |
| GPG prompts repeatedly | GPG agent is not caching the passphrase | Prime `gpg-agent` before running the workflow |
| Push is rejected | Remote branch changed since last fetch | Review remote changes, then retry with care |

## Completion Criteria

- Checks passed
- Backup branch exists
- Temporary rewrite branch was used during the rewrite
- Rebase completed without manual conflict resolution
- Rewritten commits are signed
- Final tree exactly matches the original branch tip
- Remote branch was updated with `--force-with-lease`

## References

- Create backups first with [backup-code](../backup-code/SKILL.md)
- Run the wrapper script with `bash scripts/sign-commits.sh`
