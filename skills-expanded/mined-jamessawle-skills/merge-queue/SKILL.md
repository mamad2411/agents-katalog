---
name: merge-queue
description: Use this skill whenever someone wants to merge multiple PRs, drain a PR backlog, or process approved PRs in batch. Finds all approved open PRs in a repo, then merges each one sequentially — rebasing, resolving conflicts, fixing CI, waiting for checks to pass, and merging. Re-queries after each merge so later PRs pick up changes from earlier ones. Trigger for "merge all approved PRs", "drain the backlog", "process the merge queue", "merge everything that's ready", "batch merge", "ship all approved PRs", or any request to merge more than one PR at a time.
license: MIT
compatibility: Requires GitHub CLI (gh) authenticated with push and merge access to the target repo
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent
argument-hint: <owner/repo>
metadata:
  author: jamessawle
  version: "1.0"
---

# Merge Queue

Process all approved PRs in a repository through a merge queue, fixing and merging each one sequentially.

For Claude Code-specific guidance (permissions), see `references/claude.md`.

## Arguments

- `$0` — GitHub repository in `owner/repo` format

If the argument is missing, ask the user to provide it: `/merge-queue owner/repo`

## Workflow

### Step 1: Check for approved PRs

Query for approved PRs and repo merge settings in parallel:

```bash
gh pr list --repo $0 --state open --json number,title,author,baseRefName,headRefName,reviewDecision,createdAt,additions,deletions,changedFiles,isDraft --limit 100
```

```bash
gh api repos/$0 --jq '{default_branch: .default_branch, squash: .allow_squash_merge, merge: .allow_merge_commit, rebase: .allow_rebase_merge, auto_merge: .allow_auto_merge}'
```

```bash
gh repo view $0 --json defaultBranchRef --jq '.defaultBranchRef.name'
```

Filter PRs to those where `reviewDecision` is `APPROVED` and `isDraft` is `false`. If none found, report that and stop.

Detect the merge method: use squash if enabled, otherwise merge commit, otherwise rebase.

Report the list of approved PRs to the user before starting. This is informational, not a confirmation — the skill proceeds automatically.

### Step 2: Process loop

Maintain a set of processed PR numbers (merged and skipped). Repeat until no unprocessed approved PRs remain.

#### 2a. Re-query approved PRs

Each iteration, re-query open approved PRs:

```bash
gh pr list --repo $0 --state open --json number,title,author,baseRefName,headRefName,reviewDecision,additions,deletions,changedFiles,isDraft --limit 100
```

Filter to `APPROVED` and not `isDraft`. Exclude any PR numbers already in the processed set. Merged PRs naturally drop out of `--state open`, but the processed set also covers skipped PRs to prevent retries.

If no unprocessed approved PRs remain, exit the loop.

#### 2b. Pick the best next PR

Select the PR with the smallest diff — fewest changed files first, then fewest total lines changed (additions + deletions) as a tiebreaker. This maximises throughput by merging easy PRs first, reducing the chance a conflict blocks the queue.

**Stacked PR constraint:** if a PR's `baseRefName` is not the repo's default branch, it depends on another PR. The base PR must be processed first. If the base PR has been skipped, skip the stacked PR too and record the dependency as the reason.

#### 2c. Fix the PR

Delegate to the **fix-pr** skill to rebase onto the latest base branch, resolve merge conflicts, fix any CI failures, and push the result. Pass the repo (`$0`) and the selected PR number.

If fix-pr reports that the PR is already clean (mergeable, all checks passing), proceed directly to merge.

If fix-pr fails (unresolvable conflicts, ambiguous merges), add the PR number to the skipped set with the failure reason and continue the loop.

#### 2d. Merge the PR

Determine the merge flag based on the detected merge method:

- Squash: `--squash`
- Merge commit: `--merge`
- Rebase: `--rebase`

Attempt to merge with auto-merge if available:

```bash
gh pr merge <number> --repo $0 --squash --auto --delete-branch
```

If auto-merge is not available (the repo has it disabled), poll `gh pr checks <number> --repo $0` every 30 seconds until all checks pass, then merge:

```bash
gh pr merge <number> --repo $0 --squash --delete-branch
```

Use a timeout of 15 minutes for CI polling. If checks haven't passed by then, skip the PR.

If the merge fails for any reason, add the PR to the skipped set with the error and continue.

On successful merge, add the PR number to the merged set.

#### 2e. Wait for base branch CI

After a successful merge, the base branch CI needs to complete before the next PR can be reliably processed. Poll the base branch's latest commit status:

```bash
gh api repos/$0/commits/<default_branch>/status --jq '.state'
```

Wait until the state is `success` (or `pending` resolves). Use the same 15-minute timeout. If the base branch CI fails, report it and stop the queue — there is no point rebasing further PRs onto a broken base.

### Step 3: Summary

Present a summary of all actions taken:

```markdown
## Merge Queue Results for <owner/repo>

### Merged (N)
| PR | Title | Conflicts Resolved | CI Fixes |
|----|-------|--------------------|----------|
| #41 | Add metrics endpoint | 2 files | none |
| #43 | Update dashboard | 0 files | 1 test fix |

### Skipped (N)
| PR | Title | Reason |
|----|-------|--------|
| #45 | Refactor auth | Ambiguous conflict in auth.py |
| #47 | Add caching | Depends on #45 (skipped) |

### Queue complete
- N of M approved PRs merged
- N PRs skipped
```

## Important guidelines

- **Fully autonomous** — no per-PR confirmation. The skill runs unattended after starting.
- **Re-query each iteration** — approval state and mergeable state change as the base branch moves. Always work with fresh data.
- **Smallest diff first** — maximises throughput by getting easy merges done early.
- **Skip, don't block** — if a PR can't be fixed, skip it and continue. Report at the end.
- **Wait for CI** — never rebase onto a base branch that hasn't passed CI.
- **Stop on base branch failure** — if the base branch CI fails after a merge, stop the queue.
