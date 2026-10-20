---
allowed-tools: Bash(gh:*, git:*), Task
argument-hint: [issue-number]
description: Create pull request with lean validation
model: claude-sonnet-4-20250514
---

## Create Pull Request

Create a GitHub pull request with proper validation and linking.

### Pre-PR Checks

Validate Genesis worktree and commit status:
1. Verify Genesis commit completed successfully
2. Check worktree validation passes
3. Ensure branch was pushed by Genesis

```bash
# Verify clean working tree (should be clean after Genesis commit)
git status

# Verify we're in Genesis worktree
pwd | grep -q worktrees || echo "⚠️ Not in Genesis worktree"

# Get current branch (should be pushed by Genesis commit)
git branch --show-current

# Verify recent Genesis commit
git log --oneline -5

# Optional: Validate Genesis worktree safety
genesis worktree validate 2>/dev/null || echo "Genesis worktree validation not available"
```

### PR Information

Gather context:
- Issue number: $ARGUMENTS (or detect from branch/commits)
- Changed files summary
- Test results
- Audit results

### PR Creation

Use documentation-minimalist agent to write concise PR description:

```bash
# Create PR linking to issue
gh pr create \
  --title "Title from commits or issue" \
  --body "## Summary

Resolves #$1

## Changes
- Key change 1
- Key change 2

## Testing
- Tests added/updated
- All tests passing

## Validation
- ✅ Lean audit passed
- ✅ No scope creep
- ✅ Complexity within limits
- ✅ No unnecessary dependencies
"
```

### Auto-Detection

If no issue number provided:
1. Extract from Genesis worktree name (fix-123 → 123)
2. Check branch name for issue number
3. Check recent commit messages
4. Ask user if needed

```bash
# Auto-detect issue number from Genesis worktree
ISSUE_NUM=$(basename $(pwd) | sed 's/fix-//' | grep -E '^[0-9]+$' || echo "")
```

### Success Output

Return PR URL and number for tracking.
