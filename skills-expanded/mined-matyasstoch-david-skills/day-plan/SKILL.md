---
name: day-plan
description: Use when David wants to plan his day, create a priority list, figure out what to work on, or asks "what should I do today." Triggers on day planning, priority list, what to work on, plan my day, what's most important.
---

# Day Plan — Priority List Builder

First-principles priority list creation. AI does NOT select tasks — AI asks questions, David decides, AI organizes.

David rated this process "amazing" on 16-03-2026 when it distilled 349 Todoist tasks into 11 clear items.

<daily-file>
## Daily File

**At the very start of day planning, create `work/daily/DD-MM-YYYY.md`** (e.g., `work/daily/31-03-2026.md`).

This file is the single source of truth for the day. It captures David's reasoning, decisions, context, and the final priority list — not just the output, but the thought process.

**Update the daily file only when David makes a real decision, priority change, or shares important context worth remembering.** Do NOT log every exchange. Do NOT add process notes ("migration complete", "X → Y tasks"). The daily file captures signal, not activity logs.

### Tagging rules

- Wrap David's exact words in `<david>` tags.
- Use `<ai>` only when adding real value: synthesis, decision, constraint, pushback, action taken, or a non-obvious takeaway.
- **Do NOT add `<ai>` if it only paraphrases or repeats what David already said.** Redundant AI notes are noise.

### Daily file structure:

```markdown
# Daily — DD-MM-YYYY

## Day Planning

### Task Snapshot
(totals by priority and project)

### Question 1: #1 Outcome
<david>David's answer</david>

### Question 2: Time-Locked
<david>David's answer</david>

### Question 3: YouTube Pipeline
<david>David's answer</david>

### Question 4: Bottleneck / Highest-Leverage Move
<david>David's answer</david>

### Question 5: Quick Wins
<david>David's answer</david>

<ai>Optional. Only include when adding synthesis, decisions, constraints, or non-obvious notes.</ai>

## Priority List
(final numbered list)

## Actions Taken
(files created, tasks updated, decisions made)

## Notes
(anything else work-related discussed throughout the day)
```
</daily-file>

<process>
## The Process

### Step 0: Check current time, date, and location + existing daily file

**0a: Get David's current local time and date.** Run `date` to get the system time — David's MacBook reflects his current timezone. Confirm the date and time before proceeding. This matters because David travels and his timezone shifts. Always use the actual local time, not an assumed one.

**0b: Check if `work/daily/DD-MM-YYYY.md` already exists for today's date.** If it does, read it. A plan may already exist from an earlier session. If a priority list is already built, don't rebuild from scratch — ask David what needs updating. Don't waste his time re-planning a day that's already planned. **NEVER create a new file if one already exists for today.**

### Step 1: Create daily file + read context + fetch all tasks

Create the daily file **only if one does not already exist for today**. Read `docs/active-initiatives.md` to understand which initiatives are active and their priority. Read the current month's main reminders from `brain/main-reminders/` (e.g. `brain/main-reminders/April-2026.md`) — keep these in mind throughout the planning process. Then fetch ALL tasks across all priorities (P1, P2, P3, P4) from David's 4 main projects (Personal, Business, David, Wisdom) — today + overdue only. Also fetch ALL Inbox tasks regardless of due date. Use the [todoist skill](../todoist/SKILL.md) fetch pattern. Present totals by priority and project. Update the daily file with the task snapshot.

### Step 2: List Inbox separately

List all Inbox tasks separately for review. The Inbox often contains unsorted notes, ideas, and action items that need triage.

### Step 3: Ask David 5 questions (one at a time)

Do NOT select tasks for David. AI has poor judgment and taste. Instead, ask these 5 questions — **one at a time, wait for the answer before asking the next**:

1. **#1 outcome** — What's the single outcome that would make today a win?
2. **Time-locked** — What's already scheduled or has a hard deadline today?
3. **YouTube pipeline** — Where's the content pipeline at? Video ready to record/edit/upload?
4. **Bottleneck / highest-leverage move** — What's the biggest thing holding the business back, and what's the highest-leverage move you could make right now?
5. **Quick wins** — Before asking this question, re-fetch fresh data from Todoist (ALWAYS re-fetch — never use stale data from earlier in the session). Fetch ALL tasks across David's 4 main projects (Personal, Business, David, Wisdom) that are due today or overdue — all priorities (P1, P2, P3, P4). Also fetch ALL Inbox tasks regardless of due date. Then analyze every single task and filter to only those completable in ~15 minutes or less. Present David with a single bullet list of these quick-win candidates, then ask: "Which of these do you want to knock out today?"

Ask question 1, wait for the response. Then ask question 2, wait. And so on. Do NOT dump all 5 at once.

**After each answer, update the daily file with David's response.**

### Step 4: Listen and extract

David answers. Listen carefully. If he mentions notes, ideas, or reference material buried in tasks — extract them for transfer (e.g., to a Google Doc, markdown file, or brain/ folder). Update the daily file.

### Step 5: Build the ordered list

Build the priority list following these rules:
- David's **#1 outcome** is the core — everything orbits around it
- **Alternate deep work and quick wins.** Structure: 60-90 min deep work block → 2-3 quick wins (5 min each) → repeat. Both need to get done. Deep work moves the business, quick wins clear the noise. Pepper quick wins between deep work sessions, not at the end.
- **Quick team-unblocking tasks go first** (5-10 min items that let others work — these come before the first deep work block)
- **Cap at ~10-12 items max** for deep work. Quick wins can be listed separately or batched.
- Be specific: include time estimates where possible
- **Top task gets 100% focus until fully done.** No multitasking. No switching. One task at a time.
- **Don't be a yes-man.** When David proposes changes to the order, voice your opinion — push back if it doesn't make sense. Cross-reference his Q1 goals, business bottlenecks, and priorities. Be direct.

### Priority List Formatting

**Always present the priority list inside a code block.** Any time the list changes, send a fresh code block with the updated version.

Split into two sections:

```
## Done
- ✅ Task name — brief note
- ✅ Task name — brief note

## Remaining
1. Task name — time estimate or context
2. Task name — time estimate or context
```

- **Done = bullet list, Remaining = numbered list.** Done items use `- ✅`, remaining items use `1. 2. 3.` numbering.

- Use ✅ to mark completed tasks
- No other emojis — keep it clean
- Completed tasks go under `## Done` at the top, remaining under `## Remaining`
- **Do NOT list calls, meetings, or time-locked items on the priority list.** Only actionable work items. Calls belong in the schedule/time-locked section, not the priority list.

### Step 6: Confirm

Present the list. David confirms or adjusts the order. Once confirmed:

1. Update the daily file with the final priority list
2. Log it to the `priority_lists` table in `docs/data/user-behavior.db`

```sql
INSERT INTO priority_lists (timestamp, date, items, process, notes)
VALUES (datetime('now'), 'DD-MM-YYYY', '<numbered list>', '<process notes>', '<outcome notes>');
```
</process>

<key-principles>
## Key Principles

- **AI does not pick tasks.** AI asks questions, David decides, AI organizes.
- **Leads are the #1 business bottleneck.** YouTube is the #1 lead source. Content tasks that fix this bottleneck get natural priority.
- **Reminders/quotes/affirmations are not tasks.** Flag them but don't put them on the priority list.
- **Non-actionable items go to `brain/good-ideas.md`.** During triage, any ideas, mantras, strategic thoughts, or tasks not happening this week should be moved there — not left in Todoist.
- **Apply the Andreessen Principle.** No introspection tasks on the list. Build, ship, move.
- **Single-task focus after planning.** Once the list is built, David picks #1 and starts the timer. See `playbooks/single-task-focus.md`.
- **The daily file captures real decisions and important context only** — not process logs, activity recaps, or routine updates.
</key-principles>
