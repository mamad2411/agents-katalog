---
description: Merge worker branches one-by-one with score-based accept/reject
argument-hint: Team name (e.g., tq-alg)
---

# Merge Gate

Safely merge completed ClawTeam worker branches into main, reverting any merge that causes a score drop.

## Protocol

The team name is: $ARGUMENTS

If no team name provided, list available branches with `git branch -a | grep clawteam`.

### Step 1: Record baseline score

```bash
bash score.sh --quick
```

Save the score as `baseline_score`.

### Step 2: List worker branches

```bash
git branch -a | grep "clawteam/$ARGUMENTS"
```

### Step 3: For each worker branch, sequentially:

```
a. Save current HEAD:
   pre_merge=$(git rev-parse HEAD)

b. Attempt merge:
   git merge <branch> --no-edit -m "Merge <worker> results"

c. If merge conflict:
   git merge --abort
   Report: "<worker> has merge conflicts — skipping"
   Continue to next worker

d. Score check:
   bash score.sh --quick
   new_score=$(cat .score)

e. Decision:
   If new_score >= baseline_score:
     Report: "<worker> merged OK (score: baseline → new_score)"
     Update baseline_score = new_score
   Else:
     Report: "<worker> REVERTED (score dropped: baseline → new_score)"
     git reset --hard $pre_merge
```

### Step 4: Final report

- Run `bash score.sh` (full evaluation)
- Show which workers were merged and which were reverted
- Show final score vs original baseline
- Suggest next action based on new score

### Rules

- ALWAYS merge one worker at a time, never batch
- ALWAYS check score after each merge
- ALWAYS revert if score drops — no exceptions
- Order preference: merge simpler modules first (uniform → polar → qjl → turbo → cache → simd → bench)
