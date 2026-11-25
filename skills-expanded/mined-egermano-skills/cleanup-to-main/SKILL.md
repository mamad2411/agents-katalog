---
name: cleanup-to-main
description: Clean up local git branches that have been removed from the remote repository. Use when the user wants to tidy up their local git branches, remove stale branches, clean up after merging PRs, or mentions 'cleanup branches', 'remove old branches', 'prune local branches', 'git branch cleanup'. Safely handles uncommitted changes, preserves local-only branches, and provides a detailed report.
---

# Cleanup to Main

Cleans up local git branches that have been deleted from the remote repository, with safety checks and detailed reporting.

## Workflow

1. **Pre-flight safety checks** → Abort if uncommitted changes or branch not synced
2. **Switch to default branch** → Detect and checkout `main` or `master`
3. **Fetch and prune** → Update remote references with `git fetch -p`
4. **Identify deletion candidates** → Local branches whose remote no longer exists
5. **Safe delete** → Use `git branch -d` for each candidate
6. **Generate report** → Summarize deleted, skipped, and kept branches

## Execution

Run the cleanup script directly:

```bash
./scripts/cleanup_branches.sh
```

Or execute step-by-step using git commands following the workflow above.

## Safety Guarantees

- **Aborts on uncommitted changes** - Working directory must be clean
- **Aborts on unsynced branch** - Current branch must match origin
- **Preserves local-only branches** - Branches never pushed are kept
- **Safe delete only** - Uses `git branch -d` (fails if not merged)
- **Never deletes main/master** - Protected branches always kept

## Branch Categories

| Category | Action | Reason |
|----------|--------|--------|
| Deleted from remote | Delete | Tracking branch gone, safe to remove |
| Not fully merged | Skip | May contain unmerged work |
| Local-only (never pushed) | Skip | User's local work in progress |
| main/master | Keep | Protected default branches |

## Exit Codes

- `0` - Success (branches cleaned or nothing to clean)
- `1` - Safety abort (uncommitted changes or unsynced branch)
- `2` - Partial failure (some branches couldn't be deleted)
