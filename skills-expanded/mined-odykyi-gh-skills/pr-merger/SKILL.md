---
name: pr-merger
description: |
  Merges approved Pull Requests safely with verification and cleanup. Handles merge 
  conflicts, CI checks, and post-merge cleanup including worktree removal. Use when 
  PR is approved and ready to land, for batch merging, or when completing the PR 
  lifecycle. Triggers on requests like "merge PR", "land PR", "merge approved PRs", 
  or "complete task". **PR merged = Definition of Done achieved**.
---

# PR Merger

Safely merges approved PRs with full verification and cleanup.

## Overview

**Purpose**: Achieve Definition of Done by merging approved PRs to main.

**Critical Rule**: PR merged = DONE. Creating a PR or getting approval is NOT completion.

## When to Use

Use this skill when:
- PR is approved and ready to merge
- User requests "merge PR", "land PR", "complete task"
- Batch merging multiple approved PRs
- Completing the PR lifecycle
- Cleaning up after merge (worktrees, branches)

## Definition of Done

| Stage | Status | DoD Met? |
|-------|--------|----------|
| Issue linked | ✅ Required | No |
| PR opened | ⏳ Intermediate | No |
| PR approved | ⏳ Intermediate | No |
| **PR merged** | ✅ **DONE** | **YES** |

**Success Criteria**:
1. ✅ PR shows as **MERGED** on GitHub (`gh pr view <number> --json state`)
2. ✅ The merge commit is present on the base branch

## Prerequisites

Before merging, verify ALL of:
- [ ] PR has approval review
- [ ] CI checks passing (required — `gh pr merge` fails if required checks are not green; do NOT use `--admin` to bypass)
- [ ] No merge conflicts with base branch
- [ ] Branch is up to date with main
- [ ] Worktree exists and is clean

## Commands

### 1. Merge Single PR

```
@pr-merger Merge PR #<number>
```

**Workflow**:
1. Verify PR state — STOP if any check fails:
   ```bash
   gh pr view <number> --json state,isDraft,reviewDecision,mergeable,mergeStateStatus,statusCheckRollup
   ```
   Require: `state == OPEN`, `isDraft == false`, `reviewDecision == APPROVED`, `mergeable == MERGEABLE`, and every entry in `statusCheckRollup` in `SUCCESS`/`SKIPPED`/`NEUTRAL`.
2. Check for conflicts — `mergeable != MERGEABLE` → go to Conflict Resolution below
3. Update branch if behind — `gh pr update-branch <number>`
4. Merge — `gh pr merge <number> --squash --delete-branch`
   Use the repository's configured default strategy (usually squash); confirm with the user if the branch is long-lived.
5. Verify merge — `gh pr view <number> --json state` must be `MERGED`
6. Clean up worktree and branch (Cleanup Process below)

### 2. Batch Merge

```
@pr-merger Merge all approved PRs
```

### 3. Merge with Verification

```
@pr-merger Merge PR #<number> and clean up
```

## Merge Strategies

| Strategy | Command | Best For |
|----------|---------|----------|
| **Squash** | `gh pr merge <n> --squash` | Feature branches with many commits |
| **Merge** | `gh pr merge <n> --merge` | Long-lived branches |
| **Rebase** | `gh pr merge <n> --rebase` | Clean linear history |

Add `--delete-branch` only after the merge is verified and cleanup has succeeded.

## Cleanup Process

### Worktree Removal

```bash
# Get branch name
branch_name=$(gh pr view <pr-number> --json headRefName -q .headRefName)

# Find worktree path (the "worktree <path>" line is 2 lines above the branch line)
worktree_path=$(git worktree list --porcelain | \
  grep -B2 "branch refs/heads/$branch_name" | head -1 | sed 's/^worktree //')

# Remove worktree (only if clean; never --force)
if [ -n "$worktree_path" ]; then
  if [ -n "$(git -C "$worktree_path" status --porcelain)" ]; then
    echo "Worktree $worktree_path has uncommitted changes — NOT removing. Report and stop."
  else
    git worktree remove "$worktree_path"
  fi
fi
```

### Branch Cleanup

```bash
# Ensure we are not on the branch being deleted
repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
default_branch=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' || echo main)
git switch "$default_branch" 2>/dev/null || git checkout "$default_branch" 2>/dev/null || git switch main 2>/dev/null || true

# Delete local branch (safe: refuses if not merged)
git branch -d "$branch_name" || {
  echo "Local branch not fully merged — keeping it. Review with: git log origin/main..$branch_name"
}

# Prune remote references
git fetch --prune origin 2>/dev/null || true
```

## Conflict Resolution

### Auto-Resolve (Simple Cases)
Only for text-only conflicts where the feature branch's version is authoritative
(e.g. a changelog entry). NEVER auto-resolve `package.json`, lockfiles, `VERSION`,
or any file where the base branch has newer changes — resolve those manually.
```bash
# 1. Start the merge (this is what creates the conflicted state)
git fetch origin
git merge origin/<default-branch>

# 2. List conflicted files
git diff --name-only --diff-filter=U

# 3. Take the feature branch's version (only for the approved file list)
git checkout --ours <approved-files>
git add <approved-files>

# 4. Commit and push
git commit -m "Merge main into <branch> - auto-resolved"
git push origin <branch>
```

### Manual Resolution

```
⚠️ Merge Conflict Detected

PR #<n> has conflicts with main:
- Conflicting files: <list>
- Worktree: <path>

Options:
1. Resolve manually in worktree, then retry merge
2. Ask pr-manager to rebase and retry
3. Request author to resolve
```

## Error Handling

### CI Failure

```
❌ PR #<n> CI status: FAILURE

Failed checks:
- test/unit (failed)
- lint (passed)

Action required: Fix tests before merging
```

### Merge Failed

```
❌ Merge failed for PR #<n>

Possible causes:
- Branch protection rules
- Required reviews not met
- Status checks failing
- Merge conflicts

Details: <error message>
```

## Integration

**Called by**:
- pr-manager (batch merging approved PRs)
- pr-workflow-orchestrator (completing workflow)
- User for single PR merge

**Calls to**:
- GitHub CLI for merge operations
- Git for worktree cleanup
- Test runner for verification

**Reports to**:
- pr-manager for queue updates
- User for completion status

## References

This skill is self-contained. Merge strategies are in the table above, conflict handling in "Conflict Resolution", and post-merge cleanup in "Cleanup Process".
