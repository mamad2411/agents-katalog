---
description: Morning standup - scan todos from yesterday, plan today. Run every morning to start the day.
---

# /standup - Morning Standup

## Step 0: Pull Latest

Before anything else, pull the latest from main:
```
git pull origin main
```
This ensures todos, memory, and skills are up to date.

## Step 1: Scan

1. **Yesterday's Todos** (use todo-manager agent): Read the most recent `todos/YYYY-MM-DD/todos.md`. Identify incomplete items to roll over. Use today's date to calculate yesterday.

2. **Memory Check**: Read `memory/MEMORY.md` for any pending items or context from previous sessions.

If integration agents are available (check `.claude/agents/index.md`), also scan:
3. **GitHub** (if pr-agent or github agent exists): Check for PRs pending review, overnight merges.
4. **Issue Tracker** (if tracker agent exists): Pull recently updated issues.
5. **Messages** (if slack-reader agent exists): Check for mentions and DMs.

Run available scans in parallel using the Task tool.

## Step 2: Reconcile

Before creating todos:
- Cross-reference yesterday's incomplete items against any overnight activity
- If something was already handled, mark it done — don't roll it over
- Deduplicate items that appear in multiple sources

## Step 3: Create Today's Todos

1. Create today's folder at `todos/YYYY-MM-DD/` with `todos.md`, `drafts/`, `notes/`
2. Roll over genuinely incomplete items
3. Add new items from scans
4. Prioritize: High / Medium / Low
5. Give a concise briefing: what's urgent, what's in progress, what can wait

## Step 4: Commit and PR

After creating the todo file:
1. Create branch: `chore/standup-YYYY-MM-DD`
2. Stage the new `todos/YYYY-MM-DD/` folder
3. Commit: `chore: standup YYYY-MM-DD`
4. Push and create PR (if `gh` is available), otherwise commit to current branch

End by asking: "Anything else you want to add to today's list?"
