---
description: Manage git worktrees for autoimprove experiments. Creates isolated worktrees for each experiment so the main codebase is never touched. Handles setup, teardown, and merging winning experiments back to main.
---

# Worktree Management Skill

Every autoimprove experiment runs in an isolated git worktree — a separate directory linked to the same repo but on its own branch. The main working directory is **never modified**. Only winning experiments get merged back.

```
your-project/          ← main worktree (never touched during experiments)
.claude/autoimprove/worktrees/       ← experiment worktrees live here
  experiment-001/      ← branch: autoimprove/experiment-001
  experiment-002/      ← branch: autoimprove/experiment-002
```

---

## Setup worktree environment

Run once before the first experiment in a session:

```bash
# 1. Make sure we're on a clean main branch
git status
git branch --show-current

# 2. Create the worktree container directory (gitignored)
mkdir -p .claude/autoimprove/worktrees

# 3. Add it to .gitignore if not already there
grep -q ".claude/autoimprove/worktrees" .gitignore 2>/dev/null || echo ".claude/autoimprove/worktrees" >> .gitignore

# 4. Record the base commit so all experiments branch from the same point
BASE_COMMIT=$(git rev-parse HEAD)
echo "Base commit: $BASE_COMMIT"
```

---

## Create a new experiment worktree

Run at the start of each iteration:

```bash
EXPERIMENT_ID=$(printf "%03d" $ITERATION_NUMBER)
BRANCH="autoimprove/experiment-$EXPERIMENT_ID"
WORKTREE_PATH=".claude/autoimprove/worktrees/experiment-$EXPERIMENT_ID"

# Create a new branch and worktree from current HEAD
git worktree add -b "$BRANCH" "$WORKTREE_PATH"

echo "Created worktree: $WORKTREE_PATH"
echo "Branch: $BRANCH"
```

Now switch all subsequent file edits and commands to run inside `$WORKTREE_PATH`. The main directory is untouched.

---

## Run measurement in a worktree

All measurement commands must be run from inside the worktree path:

```bash
cd .claude/autoimprove/worktrees/experiment-$EXPERIMENT_ID

# Run the measurement suite from .claude/autoimprove/config.md
# (same commands, different working directory)
```

---

## Winning experiment — merge back to main

If AFTER score > BEFORE score:

```bash
BRANCH="autoimprove/experiment-$EXPERIMENT_ID"

# Option A: Squash merge (recommended — keeps main history clean)
git merge --squash "$BRANCH"
git commit -m "autoimprove($EXPERIMENT_ID): $HYPOTHESIS_ONE_LINE

Score: $BEFORE_SCORE → $AFTER_SCORE (+$DELTA pts)
Files: $CHANGED_FILES"

# Remove the worktree and branch
git worktree remove ".claude/autoimprove/worktrees/experiment-$EXPERIMENT_ID"
git branch -D "$BRANCH"

echo "✅ Experiment $EXPERIMENT_ID merged to main"
```

---

## Losing experiment — discard cleanly

If AFTER score <= BEFORE score:

```bash
# Just remove the worktree and delete the branch — main is untouched
git worktree remove ".claude/autoimprove/worktrees/experiment-$EXPERIMENT_ID" --force
git branch -D "autoimprove/experiment-$EXPERIMENT_ID"

echo "❌ Experiment $EXPERIMENT_ID discarded — no changes to main"
```

---

## Cleanup all worktrees (end of session)

Run after the session completes or if something goes wrong:

```bash
# List all autoimprove worktrees
git worktree list | grep autoimprove

# Remove all experiment worktrees
for wt in .claude/autoimprove/worktrees/experiment-*; do
  git worktree remove "$wt" --force 2>/dev/null
done

# Clean up branches
git branch | grep "autoimprove/experiment" | xargs git branch -D 2>/dev/null

# Remove the container directory
rm -rf .claude/autoimprove/worktrees

echo "All experiment worktrees cleaned up"
```

---

## Emergency recovery

If something goes wrong mid-session and worktrees are left dangling:

```bash
# Check for stale worktrees
git worktree prune

# List all worktrees
git worktree list

# Force remove a specific one
git worktree remove .claude/autoimprove/worktrees/experiment-001 --force
git branch -D autoimprove/experiment-001
```

---

## Key guarantees

- **Main branch is never modified** until a winning experiment is explicitly merged
- **Each experiment starts from the same commit** — experiments are independent, not cumulative
- **No leftover branches** — winning experiments become squash commits, losers are deleted entirely
- **Safe to Ctrl+C** — worktrees can be cleaned up manually with the cleanup commands above
- **Parallel-safe** — each experiment has its own directory and branch, so multiple sessions can run without conflict (advanced use)
