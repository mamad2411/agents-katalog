---
name: pr-worktree
description: Creates and manages isolated git worktrees for PR workflows. Uses worktrees exclusively—never checkout—to avoid disrupting the main working directory. Handles branch creation, worktree setup, and PR lifecycle management. Enables parallel PR development with clean isolation and safe cleanup.
---

# PR Worktree

**Core Principle**: Use `git worktree` exclusively. Never `git checkout`.

Worktrees provide isolated directories for each PR while keeping your main working directory untouched. This enables parallel development on multiple PRs without stash/reset conflicts.

## When to Use

- Starting work on a new PR
- Fixing issues in an existing PR branch  
- Working on multiple PRs simultaneously
- Reviewing someone else's PR locally
- Hotfixing production issues
- Any git work that requires isolation from main

## Quick Start

### Create New PR Worktree

```bash
# Parse issue/task: type, issue number, description
BRANCH_TYPE="fix"  # fix|feature|refactor|docs|hotfix
ISSUE_NUM="432"
DESC="button-rendering"
BRANCH_NAME="${BRANCH_TYPE}/issue-${ISSUE_NUM}-${DESC}"
WORKTREE_PATH=".worktrees/$(echo ${BRANCH_NAME} | tr '/' '-')"

# Fetch the default branch into the remote-tracking ref (never into the local branch)
git fetch origin main

# Create the branch at origin/main without switching to it
git branch "${BRANCH_NAME}" origin/main

# Add the worktree
git worktree add "${WORKTREE_PATH}" "${BRANCH_NAME}"

# Start working
cd "${WORKTREE_PATH}"
# Install dependencies (use the repo's package manager: npm/pnpm/bun/yarn)
```

### Work on Existing PR

```bash
# Reviewing an existing PR: fetch the PR head ref explicitly
PR_NUMBER=<pr-number>
LOCAL_BRANCH="pr-${PR_NUMBER}-review"
WORKTREE_PATH=".worktrees/pr-${PR_NUMBER}-review"

git fetch origin "pull/${PR_NUMBER}/head:${LOCAL_BRANCH}"
git worktree add "${WORKTREE_PATH}" "${LOCAL_BRANCH}"
cd "${WORKTREE_PATH}"

# Make changes, commit, push
# Push to the PR's head branch (for fork PRs, add the fork as a remote first)
PR_HEAD_BRANCH=$(gh pr view "${PR_NUMBER}" --json headRefName --jq '.headRefName')
git add .
git commit -m "fix: resolve rendering issue

- Fixed DialogContent props
- Verified with tests

Closes #432"
git push origin "${PR_HEAD_BRANCH}"
```

### Parallel PR Management

```bash
# Create multiple worktrees
git worktree add .worktrees/fix-issue-432-rendering fix/issue-432-rendering
git worktree add .worktrees/feature-issue-444-db-check feature/issue-444-db-check
git worktree add .worktrees/hotfix-2026-04-01-security-patch hotfix/security-patch

# Switch between worktrees (main stays clean!)
cd .worktrees/fix-issue-432-rendering     # work on fix
cd ../feature-issue-444-db-check          # work on feature
cd ../hotfix-2026-04-01-security-patch    # work on hotfix
```

### Cleanup After Merge

```bash
# Verify the PR is actually merged (must be MERGED, not CLOSED)
MERGED=$(gh pr view <pr-number> --json state --jq '.state')
[ "$MERGED" = "MERGED" ] || { echo "PR #<n> is $MERGED — refusing to clean up"; exit 1; }

# Ensure nothing is lost
git -C "${WORKTREE_PATH}" status --short   # must be empty

git worktree remove "${WORKTREE_PATH}"
git branch -d "${BRANCH_NAME}"
git fetch --prune

# Verify
git worktree list
git branch -a | grep "${BRANCH_NAME}"
```

## Smart Detection

Before creating, always check:

```bash
# Worktree exists?
git worktree list | grep "<branch-name>"

# Branch exists?
git branch -a | grep "<branch-name>"

# Directory exists? (note: directory name is the branch with '/' replaced by '-')
WORKTREE_DIR=$(echo "${BRANCH_NAME}" | tr '/' '-')
ls -la .worktrees/ | grep "${WORKTREE_DIR}"
```

**If worktree exists** → Use it directly  
**If branch exists, no worktree** → Add worktree to existing branch  
**If neither exists** → Create both fresh

## Key Commands Reference

| Task | Command |
|------|---------|
| Create worktree | `git worktree add <path> <branch>` |
| List worktrees | `git worktree list` |
| Remove worktree | `git worktree remove <path>` |
| Prune stale | `git worktree prune` |
| Lock worktree | `git worktree lock <path>` |
| Unlock worktree | `git worktree unlock <path>` |

## Safety Rules

1. **Never `git checkout` in main repo** — Use worktrees instead
2. **Always verify branch state** — Check `git worktree list` before operations
3. **Commit or stash before removing** — Prevent data loss
4. **Use absolute paths in scripts** — Avoid path confusion
5. **Clean up merged PRs** — Remove worktrees after merge to save disk space

## Integration Patterns

**With pr-opener**: After creating worktree and making changes, pr-opener handles pushing, PR creation, and labeling.

**With pr-feedback-handler**: When PR receives comments, switch to worktree, apply fixes, commit, and push updates.

**With QA/testing**: Run the repo's test suite in the worktree before creating the PR. Only proceed if tests pass. (No dedicated `qa` skill ships with this collection.)

## Naming Convention

```
.worktrees/pr-<number>-<contributor>-<description>   # Reviewing others' PRs
.worktrees/hotfix-<issue-or-timestamp>-<description> # Emergency fixes
.worktrees/fix-issue-XXX-short-desc                 # Bug fixes
.worktrees/feature-issue-YYY-feature-name           # New features
```

## Summary

The pr-worktree skill enables:
- ✅ Parallel PR development without conflicts
- ✅ Clean main working directory at all times
- ✅ Fast context switching between PRs
- ✅ Safe experimentation and isolation
- ✅ Easy cleanup after merge

**All achieved without ever using `git checkout`.**

## References

- [Acceptance Criteria](references/acceptance-criteria.md) — Functional requirements, worktree operations, safety checks
- [Best Practices](references/best-practices.md) — Naming conventions, parallel work management, cleanup strategies
- [Troubleshooting](references/troubleshooting.md) — Common issues and solutions
