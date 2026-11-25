---
description: Emergency cleanup of all autoimprove experiment worktrees. Use this if a session was interrupted, Claude crashed mid-experiment, or you want to abort the loop and clean up all branches and worktrees.
---

# Rollback / Cleanup Skill

Since experiments run in isolated worktrees, there's nothing to "rollback" from the main branch — it was never touched. This skill cleans up any leftover experiment worktrees and branches from an interrupted or aborted session.

## Step 1 — Show what will be removed

```bash
echo "=== Active worktrees ==="
git worktree list

echo "=== Experiment branches ==="
git branch | grep "autoimprove/experiment"

echo "=== Worktree directory ==="
ls .claude/autoimprove/worktrees/ 2>/dev/null || echo "(empty or missing)"
```

Show the user what will be removed and confirm before proceeding.

## Step 2 — Remove all experiment worktrees

```bash
# Remove worktrees
for wt in .claude/autoimprove/worktrees/experiment-*; do
  [ -d "$wt" ] && git worktree remove "$wt" --force && echo "Removed worktree: $wt"
done

# Prune any stale worktree references
git worktree prune
```

## Step 3 — Delete experiment branches

```bash
git branch | grep "autoimprove/experiment" | xargs -r git branch -D
echo "Experiment branches deleted"
```

## Step 4 — Remove the container directory

```bash
rm -rf .claude/autoimprove/worktrees
echo "Cleaned up .claude/autoimprove/worktrees/"
```

## Step 5 — Verify clean state

```bash
echo "=== Main branch status ==="
git status
git branch --show-current

echo "=== Remaining worktrees ==="
git worktree list
```

Report: "✅ Cleanup complete. Main branch is clean and untouched."

## Safety notes
- This skill never touches the main branch
- Already-merged winning experiments stay in the main branch history — only pending/discarded experiments are removed
- If a worktree can't be removed cleanly, use `--force` (already included above)
