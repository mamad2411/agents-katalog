---
name: endless-ideas-migration
description: Use when David wants to mass-migrate tasks out of Todoist into brain/good-ideas.md. Filters all tasks against David's current priorities, keeps only actionable tasks, moves everything else. Triggers on purge, migrate, clean todoist, too many tasks, overwhelmed, move to endless ideas.
---

# Endless Ideas Migration

Mass-migrate non-actionable Todoist tasks to `brain/good-ideas.md`. Todoist should only contain focused, actionable tasks. Everything else — ideas, mantras, quotes, strategic thoughts, tasks not happening this week — goes to the endless ideas file.

Origin: David was overwhelmed with 92+ tasks due today. We filtered them against his 6 real priorities and moved 173 tasks out in one session. Todoist went from 92 → 7. David approved this process on 29-03-2026.

## The Process

### Step 1: Fetch tasks

Fetch all tasks from David's 5 projects using the [todoist skill](../todoist/SKILL.md) fetch pattern. Scope depends on what David asks for — could be today+overdue, tomorrow, a specific project, or all undated tasks.

**CRITICAL: Always use bash script files for jq operations — never inline in zsh.**

### Step 2: Get David's priorities

Read `work/daily/YYYY-MM-DD.md` (today's file) for current priorities. If no daily file exists or priorities aren't defined, ask David:

> "What are the few things that actually matter right now? Business and personal."

These become the filter. Every task must directly support one of these priorities to stay in Todoist.

### Step 3: Split into two buckets

Run every task through one question: **"Does this directly support one of David's stated priorities?"**

- **YES → KEEP** in Todoist
- **NO → MOVE** to endless ideas

**BATCHING (when task count > 20):** If there are more than 20 tasks to go through, split it into 2-3 batches as you see fit and process ONE BATCH AT A TIME. Show only the current batch's KEEP/MOVE split. Never dump the full task list first and then try to batch — David explicitly hated this ("WHAT THE FUCK HAPPENED. why did you list out all 91 tasks again?!"). Go straight to batch 1. Keep each batch small enough that David is not overwhelmed.

**Between batches:** Items David kept in batch N may get re-evaluated and moved in batch N+1. This is normal. Don't treat previous batch decisions as locked — David's judgment evolves as he sees the full picture.

Present both lists to David as two concise **numbered lists** — no bullet lists, no sections, no grouping by type. Just:

```
**KEEP (N):**
1. task text
2. task text

**MOVE (N):**
1. task text
2. task text
```

Keep it flat, concise, numbered. No other formatting.

**Do NOT execute until David confirms.** David will often move items between the lists (keep some you proposed to move, move some you proposed to keep). Show the corrected KEEP/MOVE lists after his adjustments — don't skip this. He needs to see what he approved before execution starts.

### Step 4: Migrate (EXACT ORDER — NO SHORTCUTS)

After David approves, execute these steps in this exact sequence. Do not combine or skip steps.

**Step 4a: Write to file first.**
Append all MOVE tasks to `brain/good-ideas.md` under a new date header:
```
## DD-MM-YYYY — [scope label]

- task content
- task content
```

When doing multiple batches, use `batch N` in the scope label (e.g., `Inbox migration batch 1`).

**Step 4b: Verify the write.**
Re-read the file. Count lines starting with `- ` under the new header. The count MUST match the expected number of tasks. If it doesn't, fix it before proceeding. Do NOT touch Todoist until this is confirmed.

**Step 4c: Re-fetch fresh task IDs from Todoist API.**
Do a fresh `GET /api/v1/tasks` for the Inbox project. NEVER use cached/stale IDs from an earlier fetch. Todoist IDs change when tasks are moved, and new tasks added between fetches will have completely different IDs. The API returns 204 even when deleting already-gone IDs — so stale deletes appear to succeed while real tasks survive. Match tasks by `content` (exact text match) to get the current ID from THIS fresh fetch. This is non-negotiable.

**Step 4d: Delete from Todoist (prefer Sync batch).**
Best path = ONE Sync batch call: `POST /api/v1/sync` with a `commands` array of `item_delete` ops (≤100 per request), each with a unique `uuid` (idempotent — safe to retry). This kills two old bugs at once: no redaction-prone per-task curl loop, and no trailing-newline trap from looping over a file. Easiest via the Python SDK (`for id in ids: api.delete_task(id)`) which avoids the token-literal redaction problem entirely — see the todoist skill's auth/fix-order section.
If you must loop REST `DELETE /api/v1/tasks/{id}` (returns 204): iterate `for ID in $(jq -r '.[].id' ids.json)`, NEVER `while read < file` (drops the last ID if no trailing newline — happened 29-05, "remember" survived).

**Handling "NOT FOUND" on exact match:** Todoist sometimes stores curly/smart quotes (' ' " ") where the skill has straight quotes (' "). If exact content match fails, retry with jq `test("keyword")` partial match on a unique substring (use first 4 words — 3 is sometimes too short for uniqueness), then delete by that ID. This is the #1 cause of failed deletes.

**Handling duplicate tasks:** Sometimes the same content appears 2+ times in Todoist (e.g., "go buy more towels" twice). The MOVE list may include one but not the other. Match by content gives ALL matching IDs — handle each duplicate explicitly: count matches, delete only the number on the MOVE list (use `head -n N` to pick), leave the rest. Don't accidentally delete David's KEEP copy.

**Step 4e: Verify remaining tasks.**
Re-fetch all Inbox tasks. Confirm the count matches expectations. If any MOVE task survived, flag it immediately. After all batches are done, show final Inbox count.

### Step 5: Report to David

Report the migration result in one line per batch (e.g., "Batch 1: Inbox 91 → 73. 18 archived."). After the final batch, give the overall summary (e.g., "Total: 91 → 14."). Do NOT write a summary to the daily file — it's process noise, not signal.

## Rules

- **Zero data loss.** Every task must be written to the file BEFORE deleting from Todoist.
- **ALWAYS re-fetch IDs right before deleting.** Never reuse IDs from a previous fetch. Match by task content text, get the fresh ID, then delete. Stale IDs = wrong tasks deleted.
- **Delete by ID only.** Never use bulk operations that could hit wrong tasks.
- **David confirms before any deletion.** Always show the split first.
- **AI does not decide what matters.** AI proposes the split, David approves. AI has poor judgment.
- **Keep the file minimal.** One bullet per item, no categorization within the file. Date headers only.

## The Filter Question

One question per task: **"Does this directly support one of David's current priorities?"**

Things that fail this filter:
- Mantras, quotes, affirmations, self-talk
- Strategic musings ("what if we...", "imagine if...")
- Ideas for future projects
- Shopping lists not needed this week
- Vague directives ("go hard on X")
- Tasks for initiatives that are paused or deleted (see `docs/active-initiatives.md`)

## Post-Migration Leftover Moves

When David says "just move the remaining N tasks" (assigning leftover Inbox items to projects with due date + priority), execute immediately. Do NOT ask for confirmation on the proposed (project, priority, date) mapping. Propose mapping → execute in one turn. He's already approved by asking.

## Pitfalls

- **Never dump the full task list then batch.** If David asks for batches, split immediately and only show batch 1. Showing all tasks first then saying "let's batch" wastes David's time and triggers frustration.
- **David's "confirm" often includes reshuffling.** He'll say "keep #2, #7, #14 from the MOVE list" — meaning those move back to KEEP. Always show the updated lists after his corrections before executing.
- **Smart/curly quote mismatch.** Todoist content may contain Unicode curly quotes (' ' " ") while your bash script has straight quotes. When exact match fails in deletion, use jq `test()` with a unique keyword substring as fallback. This saved batch 2 in the 12-05-2026 session.
- **Scope label for multi-batch runs.** Use `batch 1`, `batch 2` etc. in the date header scope label so entries in good-ideas.md are distinguishable.
- **Todoist move API returns an OBJECT, not array.** When moving a task via `POST /api/v1/tasks/{id}/move`, the response shape can vary. Always handle both: `jq -r 'if type=="array" then .[0].id else .id end // empty'`. Assuming one shape breaks the script mid-batch and leaves tasks half-migrated (moved but no due date/priority applied).
- **Move + update in one pass is slow.** 19 tasks with 2 API calls each (move + update) can exceed 60s. Use a 300s timeout for migrate operations, or use a single pre-fetch of ALL 5 projects and then operate from that snapshot.

- **SECRET-REDACTION TRAP (29-05-2026).** Writing a script file containing the literal `Bearer <token>` corrupts the line on write → `unexpected EOF` at runtime (10+ call cascade). Don't fight it with string tricks — use the Python SDK or MCP so the token value never appears in agent-written text. Full fix order in the todoist skill's auth section.

## API Reference

Uses the [todoist skill](../todoist/SKILL.md) for all API operations.

- **Delete:** `DELETE /api/v1/tasks/{id}` — returns 204 on success
- Auth: `$TODOIST_API_TOKEN` from `.env` file. Always `source .env` first.
