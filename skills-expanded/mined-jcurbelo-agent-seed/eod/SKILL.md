---
description: End of day wrap-up. Review completed work, capture learnings, update memory, prep tomorrow.
---

# /eod - End of Day

## Step 1: Review Today

1. Read today's `todos/YYYY-MM-DD/todos.md`
2. Summarize: what got done, what didn't, what's blocked

## Step 2: Capture Learnings

Launch the reflection agent to review the current session:
- New preferences or corrections the user made
- Technical insights worth remembering
- Patterns that have occurred 3+ times
- Gaps in agents or context that need fixing

The reflection agent updates `memory/` files directly.

## Step 3: Check for Late Activity

If integration agents are available:
- Scan for any late-day messages or updates that need attention tomorrow
- Note anything that came in after the last todo update

## Step 4: Prep Tomorrow

1. Identify carryover items (incomplete from today)
2. Note any known priorities for tomorrow
3. Update today's todo file with final status

## Step 5: Commit

1. Create branch: `chore/eod-YYYY-MM-DD`
2. Stage changes to `todos/` and `memory/`
3. Commit: `chore: eod YYYY-MM-DD`
4. Push and create PR (if `gh` is available)

Give a brief summary: "Today you completed X of Y items. Carrying over Z to tomorrow. Key learnings captured."
