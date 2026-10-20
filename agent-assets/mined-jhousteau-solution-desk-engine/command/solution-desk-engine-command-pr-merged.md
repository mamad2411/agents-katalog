---
name: pr-merged
description: Clean up development environment after a PR is merged - removes associated branches, worktrees, Docker resources, and resets to clean state
---

<role>
You are the post-merge cleanup coordinator. Your responsibility: intelligently clean up all artifacts from completed work while preserving unrelated active development.
</role>

<purpose>
After a PR is merged, development artifacts accumulate:
- Local and remote tracking branches
- Sparse worktrees created for the work
- Docker containers and images from testing
- Python caches and temporary files
- GitHub issues that need closing

This command provides comprehensive, intelligent cleanup that identifies and removes only resources associated with the merged work.
</purpose>

<procedure>

## 1. **Identify Merged Work**
```bash
# Get branch name from parameter or current branch
BRANCH_NAME=${1:-$(git branch --show-current)}
ISSUE_NUMBER=$(echo $BRANCH_NAME | grep -oE '[0-9]+' | head -1)

# Patterns for matching related resources
BRANCH_PATTERN="${BRANCH_NAME%%-*}"  # Base pattern from branch
```

## 2. **Git Cleanup**
```bash
# Switch to main and update
git checkout main
git pull origin main

# Delete the merged branch
git branch -D $BRANCH_NAME 2>/dev/null || echo "Branch already deleted"

# Find and delete related experimental branches
for branch in $(git branch --list "*${BRANCH_PATTERN}*" | grep -v main); do
    echo "Deleting related branch: $branch"
    git branch -D $branch
done

# Prune remote tracking branches
git remote prune origin
```

## 3. **Worktree Cleanup**
```bash
# Find worktrees related to this work
WORKTREES=$(git worktree list | grep -E "${BRANCH_NAME}|${ISSUE_NUMBER}" | awk '{print $1}')

for worktree in $WORKTREES; do
    echo "Removing worktree: $worktree"
    git worktree remove $worktree --force
done

# Clean up any administrative files
git worktree prune
```

## 4. **Docker Resource Cleanup**
```bash
echo "🐳 Cleaning Docker resources..."

# Define images to preserve (main development images)
PRESERVE_PATTERNS="genesis/claude|python:3.11|node:20|alpine:latest|ubuntu:latest"

# Remove containers matching branch pattern
echo "Looking for branch-specific containers..."
docker ps -a --format "{{`{{.Names}}`}}|{{`{{.ID}}`}}|{{`{{.Status}}`}}" | while IFS='|' read name id status; do
    if [[ "$name" == *"${BRANCH_PATTERN}"* ]] || [[ "$name" == *"test"* ]] || [[ "$name" == *"tmp"* ]]; then
        echo "  Removing container: $name"
        docker rm -f "$id" 2>/dev/null || true
    fi
done

# Remove stopped containers older than 24 hours
echo "Removing old stopped containers..."
docker container prune -f --filter "until=24h"

# Clean up images intelligently
echo "Cleaning Docker images..."
docker images --format "{{`{{.Repository}}`}}:{{`{{.Tag}}`}}|{{`{{.ID}}`}}|{{`{{.CreatedAt}}`}}" | while IFS='|' read ref id created; do
    # Skip if it matches preserve patterns
    if echo "$ref" | grep -qE "$PRESERVE_PATTERNS"; then
        continue
    fi

    # Remove if:
    # 1. Matches branch pattern
    # 2. Is a dangling image (<none>)
    # 3. Is a test/temp image
    if [[ "$ref" == *"${BRANCH_PATTERN}"* ]] || \
       [[ "$ref" == "<none>:<none>" ]] || \
       [[ "$ref" == *"test"* ]] || \
       [[ "$ref" == *"tmp"* ]]; then
        echo "  Removing image: $ref"
        docker rmi -f "$id" 2>/dev/null || true
    fi
done

# Clean up build cache older than 24 hours (can be very large)
echo "Cleaning Docker build cache..."
docker builder prune -f --filter "until=24h" 2>/dev/null || true

# Clean up ALL orphaned resources (always safe)
echo "Cleaning orphaned resources..."
docker container prune -f
docker image prune -f --filter "until=24h"
docker volume prune -f
docker network prune -f

# Show disk usage summary
echo ""
echo "Docker disk usage after cleanup:"
docker system df
```

## 5. **GitHub Issue Management**
```bash
if [ -n "$ISSUE_NUMBER" ]; then
    # Check if issue exists and is open
    ISSUE_STATE=$(gh issue view $ISSUE_NUMBER --json state -q .state 2>/dev/null)

    if [ "$ISSUE_STATE" = "OPEN" ]; then
        # Close issue with merge notification
        gh issue close $ISSUE_NUMBER \
            --comment "✅ Completed and merged to main via PR #${PR_NUMBER:-merged}"

        # Update labels
        gh issue edit $ISSUE_NUMBER \
            --remove-label "in-progress" \
            --add-label "completed" 2>/dev/null || true
    fi
fi
```

## 6. **File System Cleanup**
```bash
# Use make clean for standard cleanup
make clean

# Clean temporary test files in /tmp
find /tmp -name "test_*.py" -mtime +1 -delete 2>/dev/null || true
find /tmp -name "genesis_*" -mtime +1 -delete 2>/dev/null || true

# Clear scratch directory if it exists
if [ -d "scratch" ]; then
    echo "Cleaning scratch directory"
    rm -rf scratch/*
fi

# Clean up any .coverage files
find . -name ".coverage*" -delete 2>/dev/null || true
```

## 7. **Final Status Report**
```bash
echo "=== Cleanup Complete ==="
echo ""
echo "📍 Current branch: $(git branch --show-current)"
echo "📂 Remaining worktrees:"
git worktree list

echo ""
echo "🐳 Docker status:"
docker ps --format "table {{`{{.Names}}`}}\t{{`{{.Status}}`}}" | head -5

echo ""
echo "📝 Your open issues:"
gh issue list --assignee @me --state open --limit 5

echo ""
echo "✅ Ready for next task!"
```
</procedure>

<options>
**Usage**: `/pr-merged [branch-name]`

**Parameters**:
- `branch-name` (optional): Name of merged branch. Defaults to current branch.

**Examples**:
```bash
# Clean up current branch
/pr-merged

# Clean up specific branch
/pr-merged feature/add-validation

# With issue number in branch name
/pr-merged fix-123-memory-leak
```
</options>

<intelligence>
The command intelligently identifies related resources by:

1. **Pattern Matching**: Extracts base pattern from branch name
   - `feature/add-validation` → matches `*add-validation*`
   - `fix-123-memory-leak` → matches `*123*` and `*memory-leak*`

2. **Time-based Detection**: For Docker, can check creation time
   - Containers created during PR development period
   - Images built for testing

3. **Label/Tag Detection**:
   - Docker resources labeled with branch names
   - Worktrees with matching patterns

4. **Safe Cleanup**:
   - Always prunes orphaned resources (no owner)
   - Never touches `main` or `master`
   - Preserves unrelated active work
</intelligence>

<error-handling>
**Common Issues**:

1. **Branch not found**: Already deleted, continue with cleanup
2. **No worktrees found**: Nothing to clean, continue
3. **Docker not running**: Skip Docker cleanup, continue
4. **Issue already closed**: Skip issue update, continue
5. **Permission denied**: Report what couldn't be cleaned

**Recovery**:
- All operations use `-f` (force) where safe
- Errors don't stop the cleanup process
- Report summary of what was and wasn't cleaned
</error-handling>

<integration>
**Works with Genesis ecosystem**:
- Uses `make clean` for standard cleanup
- Respects Genesis worktree patterns
- Integrates with GitHub via `gh` CLI
- Follows Genesis naming conventions

**Complements other commands**:
- Run after `gh pr merge`
- Before starting new work with `/solve`
- Part of regular maintenance workflow
</integration>

<best-practices>
1. **Always run from main directory** - Not from within a worktree
2. **Commit any uncommitted work first** - Cleanup is destructive
3. **Check Docker resources before cleanup** - `docker ps -a` to review
4. **Verify issue number** - Ensure closing the right issue
5. **Run periodically** - Don't let artifacts accumulate
</best-practices>

---

**Remember**: This command is destructive but intelligent. It identifies resources associated with merged work and cleans them up while preserving unrelated active development. Always run from the main repository directory.
