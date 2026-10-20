---
name: david-sql-task-importance
description: Use when David wants to score or rate the importance of his Todoist tasks in docs/data/todoist-task-dimensions.db. Presents tasks 7 at a time (A-G), David gives scores (0-10), AI saves them. Also updates brain/ and docs/data/user-behavior.db.
---

# David SQL Task Importance — Batch Scoring

**Goal:** Score every task in `docs/data/todoist-task-dimensions.db` with a `david_importance` value (0-10 integer). David scores, AI records. No guessing.

## Why This Matters

`david_importance` is fundamentally different from daily priority lists. Priority = "what should I do today?" Importance = "how much does this matter to my life, goals, and business?" A task can be low-priority today but importance-10. This column captures what David truly cares about — the signal that no daily triage can surface. Tasks scored 0 are archived to `not_relevant` automatically.

## Scale

| Score | Meaning |
|---|---|
| 0 | Dead. Irrelevant. Completed with no future bearing. |
| 1 | Lowest leverage. Taking out trash, vacuuming. Does not matter long-term. |
| 5 | Mid-range. Has some value but not a priority mover. |
| 10 | Massive implications to David personally, the business, or the long-term vision/mission. |

## Rules

- **AI NEVER guesses scores.** Only David assigns `david_importance`. AI presents, David scores, AI saves.
- **Check DB before asking questions.** Before presenting any task, check if `david_reasoning` and other columns are already populated. Never ask redundant questions.
- **Voice-to-text decimals are errors.** If David says "8.8" or "7.7", assume the repeated digit is a transcription artifact. Always round DOWN (8.8 → 8, 7.7 → 7).
- **Voice-to-text duplicates are confirmation.** If David repeats a score ("Task E, 9. Task E, 9."), take the first instance.

## Presentation Format

Present 7 tasks per batch, lettered A-G:

```
**X/Y scored, Z remaining**

A. task name here
B. task name here
C. task name here
D. task name here
E. task name here
F. task name here
G. task name here
```

- **Always show progress** (scored / total, remaining) before each batch.
- **Letters A-G only.** No numbers. David uses voice-to-text and letters are clearer.
- **Task name only.** No project, no priority, no metadata. Keep it minimal.

## Scoring Method (CRITICAL — NO OFFSETS)

**Never use SQL OFFSET to map scores to tasks.** Offsets shift when rows are added/deleted and cause cascading errors.

### Step 1: Fetch with explicit IDs

```sql
SELECT DISTINCT todoist_id, task_name
FROM tasks
WHERE todoist_id IS NOT NULL AND david_importance IS NULL
GROUP BY todoist_id
ORDER BY id
LIMIT 7;
```

Store the 7 `todoist_id` values explicitly before presenting to David.

### Step 2: Present task names (A-G)

### Step 3: David gives scores

### Step 4: Update using explicit todoist_id

Write each UPDATE as a separate, explicit SQL statement:

```sql
UPDATE tasks SET david_importance = 8 WHERE todoist_id = '<TODOIST_ID_1>';
UPDATE tasks SET david_importance = 0 WHERE todoist_id = '<TODOIST_ID_2>';
```

**Never use subqueries, offsets, or shell loops.** One todoist_id per UPDATE. No ambiguity.

### Step 5: Auto-advance

After saving, immediately present the next 7. No confirmation needed.

## Source of Tasks

Default: all tasks in `docs/data/todoist-task-dimensions.db` where `david_importance IS NULL`.

David may specify a different scope:
- "score all inbox tasks" → filter by domain or project
- "re-score my 9s and 10s" → filter by existing score
- "score today's Todoist tasks" → fetch fresh from Todoist API first (use [todoist skill](../todoist/SKILL.md)), upsert into DB, then score

## Fetching Fresh Tasks from Todoist

When David wants to score tasks not yet in the DB:

1. Fetch from Todoist API using the [todoist skill](../todoist/SKILL.md)
2. Check each task against DB by `todoist_id`
3. INSERT new tasks (with whatever columns can be inferred from task text)
4. Present for scoring

## Companion Updates

After each batch of David's responses:

- **`docs/data/user-behavior.db`** — log a message entry if behavior-tracking is active
- **`brain/`** — update relevant files if David's scores reveal new patterns about how he thinks or prioritizes

## Database Location

`docs/data/todoist-task-dimensions.db` — column: `david_importance INTEGER DEFAULT NULL`

## Wrap Up

When all tasks scored:
- Report total scored, distribution (how many 0s, how many 10s, etc.)
- Show top 20% (scores 8-10) as a ranked list
- Stage and push to GitHub
