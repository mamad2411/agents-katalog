---
name: overnight-loop
description: Set up Claude Code to safely run autonomously for hours (overnight, multi-hour batch work). Use this skill when the user wants to leave Claude working unattended on a well-defined batch of tasks. Triggers on phrases like "leave this overnight", "run while I sleep", "autonomous run", "process this batch". Establishes guardrails so the user wakes up to working code instead of disasters.
---

# Overnight Loop Skill

## When to Trigger

User wants Claude to run autonomously for 1+ hour without supervision. Examples:
- "Leave this running overnight"
- "Process all 50 of these tickets"
- "Refactor every component to use the new pattern"
- "Migrate all tests from X to Y"

## The Risk Profile of Unattended Runs

Without guardrails, an unattended Claude can:
- Push broken code to main
- Burn through tokens on a loop with no progress
- Make a single irreversible mistake that costs hours to undo
- Get stuck in a doom loop trying to fix something it broke

This skill sets up the safety net.

## Workflow

### Step 1: Define a clear scope

The user MUST give:
- A finite list of tasks OR a clear stopping condition
- Definition of done for each task
- A safe blast radius (which files/services/databases can change)

Bad scope: "Improve the codebase overnight."
Good scope: "Migrate all 23 components in `src/components/legacy/` to use the new design tokens from `tokens.css`. Each migration: import the tokens, replace hardcoded values, run the component story, take a screenshot, save the screenshot to `screenshots/migrated/`. Done when all 23 are migrated and tests pass."

### Step 2: Set up the work queue

Write to `.claude/overnight/queue.md`:

```markdown
# Overnight Run - <date>

**Started:** <time>
**Operator:** <user>
**Estimated tasks:** N
**Stop condition:** <when to stop>

## Queue

- [ ] Task 1: <specific instruction>
- [ ] Task 2: <specific instruction>
- [ ] ...
```

### Step 3: Set up the safety net

#### 3a. Git safety

```bash
# Create a dedicated branch
git checkout -b overnight/<date>-<scope-slug>

# Commit current state as backup
git commit --allow-empty -m "checkpoint: before overnight run"

# Note the SHA - this is the rollback point
git rev-parse HEAD > .claude/overnight/rollback-sha.txt
```

If anything goes catastrophically wrong, `git reset --hard $(cat .claude/overnight/rollback-sha.txt)` restores everything.

#### 3b. Per-task commits

Configure the loop to commit after EACH task succeeds:

```bash
# Commit pattern after each task
git add -A
git commit -m "task <N>: <description>

- Files changed: <count>
- Tests: <result>
- Verification: <result>
"
```

Granular commits = easy to bisect if something is broken in the morning.

#### 3c. CI gate

Configure pre-commit hook OR per-task verification that runs the full test suite. If tests fail:
1. Roll back the changes for that task only (`git checkout -- .`)
2. Mark task as failed in the queue
3. Move to next task
4. Do NOT push to remote with broken tests

#### 3d. Token budget

Set a hard upper limit:
```bash
# In .claude/overnight/limits.txt
MAX_TOKENS_TOTAL=10000000   # 10M tokens, adjust per budget
MAX_TASKS_FAILED_BEFORE_STOP=3
MAX_HOURS=8
```

Loop checks these every iteration. If exceeded, STOP gracefully and write a status report.

### Step 4: Configure the loop command

Use Claude Code's built-in `/loop` if available, or set up a shell loop:

```bash
# Option A: built-in /loop (if available in your Claude Code version)
/loop /process-next-task

# Option B: shell-driven loop with claude -p
while true; do
  TASK=$(grep -m 1 '^- \[ \]' .claude/overnight/queue.md)
  if [ -z "$TASK" ]; then
    echo "Queue empty - done"
    break
  fi
  
  # Hand the task to Claude in a fresh session
  claude -p "Execute task per .claude/CLAUDE.md and the overnight protocol. Task: $TASK"
  
  # Check exit code, log, sleep briefly
  sleep 5
done
```

### Step 5: Per-task protocol

For EACH task in the queue, the agent must:

1. **Read** the task from queue
2. **Plan** in Plan Mode (Shift+Tab x2). Save plan to `.claude/overnight/plans/task-N.md`
3. **Execute** following the plan
4. **Verify** - run tests, lint, run the app for affected paths
5. **If fail:** revert, mark failed, log details to `.claude/overnight/logs/task-N-failure.md`, move on
6. **If pass:** commit, mark done, move on
7. **Status update** every 10 tasks (or every 30 minutes): write summary to `.claude/overnight/status.md`

### Step 6: Status reporting

Maintain `.claude/overnight/status.md`:

```markdown
# Overnight Run Status - <date>

**Started:** <time>
**Last update:** <time>
**Tasks completed:** X / N
**Tasks failed:** Y
**Tokens used:** Z (of budget B)

## Recent activity

- HH:MM Task 12 done (commit abc123)
- HH:MM Task 13 failed - tests broke. See logs/task-13-failure.md
- HH:MM Task 14 done (commit def456)

## Failed tasks (need human review)

- Task 13: Component X migration - test "renders with token" failing. Suspect token name mismatch. Did NOT push.

## Estimated completion

<extrapolation based on velocity>
```

The user reads this in the morning to see what happened.

### Step 7: Notification on done or failure-cluster

If `/loop` supports it OR via a webhook:
- Send a system notification when done
- Send a notification if failure rate exceeds 20% (something is wrong, stop and ask)

### Step 8: Morning report

At the end (or when user comes back), produce a final report:

```markdown
# Overnight Run Report - <date>

## Summary
- Total tasks: N
- Done: X (XX%)
- Failed: Y
- Skipped: Z (reason)
- Time: H hours
- Tokens: T (cost ~$M)

## Done (commits to review)
- abc123 - Task 1
- def456 - Task 2
...

## Failed (need attention)
- Task 13: <one-line description, link to log>
- Task 27: <...>

## Recommendations
- <patterns observed across failures>
- <improvements for next overnight run>
- <code review priorities for the diff>
```

### Step 9: User reviews the diff

The user reviews the morning's diff:
```bash
git log --oneline overnight/<date>-<slug> ^main
git diff main..overnight/<date>-<slug>
```

If happy: merge. If not: cherry-pick the good commits, drop the bad.

## Hard Rules for Overnight Runs

- **Never push to main directly.** Always a feature branch.
- **Never deploy.** Overnight runs build code, they don't ship it.
- **Never modify infrastructure** without explicit scope.
- **Never run destructive operations** (DB migrations on prod, file deletes outside the workspace).
- **Always commit per task.** No "big WIP commit at end".
- **Always revert on failure.** Don't leave the workspace in a broken state for the next task.
- **Always log enough to debug** in the morning.

## Pre-flight Checklist

Before starting any overnight run, verify:

- [ ] Scope is finite and clearly defined
- [ ] Tasks queue is written and reviewed by user
- [ ] Branch is created, rollback SHA saved
- [ ] Test command is fast enough (< 5 min) to run after every task
- [ ] Token budget is set
- [ ] Notifications configured
- [ ] User has signed off

## Recommendations

After every overnight run:
- Patterns of failure (these become new tests or new linter rules)
- Tasks that took 3x estimate (estimating model needs update)
- Successful patterns that should become slash commands
- Things that should be code-reviewed especially carefully (anything in the failed list)
