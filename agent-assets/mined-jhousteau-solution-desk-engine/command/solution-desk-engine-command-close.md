---
allowed-tools: Bash(gh:*, git:*), Task
argument-hint: [issue-number]
description: Clean up after PR merge
model: claude-sonnet-4-20250514
---

## Genesis Post-Merge Cleanup

Clean up after pull request has been merged using Genesis worktree management.

### Issue Detection

Auto-detect issue number from current context:
```bash
# Auto-detect issue number from argument or worktree
ISSUE_NUM=${1:-$(basename $(pwd) | sed 's/fix-//' | grep -E '^[0-9]+$')}
```

### Issue Cleanup

Close the GitHub issue:
```bash
# Get PR number from GitHub (if available)
PR_NUMBER=$(gh pr list --state merged --limit 1 --json number --jq '.[0].number' 2>/dev/null || echo "merged")

# Close issue with comment
gh issue close $ISSUE_NUM --comment "Resolved in PR #$PR_NUMBER"
```

### Genesis Worktree Cleanup

Use Genesis to clean up worktree and branches:
```bash
# Navigate back to main project (if in worktree)
cd $(git rev-parse --show-toplevel)

# Remove Genesis worktree (handles branch cleanup automatically)
genesis worktree remove fix-$ISSUE_NUM 2>/dev/null || {
    echo "Manual cleanup required"
    # Fallback manual cleanup
    git checkout main || git checkout master
    git pull
    git branch -d fix-$ISSUE_NUM 2>/dev/null || echo "Branch already deleted"
    git push origin --delete fix-$ISSUE_NUM 2>/dev/null || echo "Remote branch already deleted"
}
```

### Documentation Update

Check if docs need updating:
- Use documentation-minimalist to update ONLY if needed
- Remove outdated documentation
- Don't add unless critical

### Final Status

Report cleanup complete:
```
✅ Issue #$ISSUE_NUM closed
✅ Genesis worktree removed
✅ Branch cleaned up automatically
✅ Main branch updated
✅ Ready for next issue
```

### Optional: Update Metrics

If tracking metrics, update:
- Issues resolved count
- Code reduction achieved
- Complexity improvements
