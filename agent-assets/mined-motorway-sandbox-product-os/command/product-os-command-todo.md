<!-- owner: shared | audience: all-pms | last-updated: 2026-04-03 -->
<!-- purpose: Extract action items from Granola meetings into a PM's todo list -->

# Todo List Generator

Extract action items from recent Granola meeting notes and update the PM's todo list.

## Instructions

### Step 0: Parse arguments

- The user provides arguments in the format: `$ARGUMENTS`
- Expected format: `{initials}, {first name}` (e.g. `CR, {YOUR_NAME}` or `JK, James`)
- If only initials are provided, ask for the PM's first name
- If no arguments are provided, check the auto-memory (MEMORY.md) for the user's initials and name before asking
- Use **initials** for file paths (e.g. `team/{initials}/todo_list.md`)
- Use **first name** when searching for action items assigned to the PM in meeting notes

### Step 1: Housekeep the todo list

Before fetching meetings, run a lightweight housekeeping pass on `team/{initials}/todo_list.md`. This keeps the list clean between weekly reviews.

#### 1a) Fix malformed rows

- Scan the main table for rows that don't match the expected 6-column format (`# | Action Item | Priority | Due Date | Source | Done`)
- For rows with missing columns: flag them in the terminal output as "Malformed items — please review" with the row content. Preserve them in the table rather than silently dropping them
- Fix minor Done-column typos (e.g. `x]` → `[x]`, `[X]` → `[x]`)

#### 1b) Archive completed and dropped items

- Move all `[x]` (completed) and `[-]` (dropped) items from the main table to the Archive section at the bottom
- Group under a week heading matching the format used by `/weekly-review` (e.g. `### Week of Mar 31`)
- If a heading for the current week already exists (from a previous `/todo` run this week), append to it rather than creating a duplicate
- Mark items as **Done** or **Dropped** in the archive table
- Don't prune old archive entries (that's the weekly review's job)

#### 1c) Renumber items sequentially

- After removing archived items, renumber remaining open items starting from 1
- Eliminate letter suffixes (75a, 75b → sequential integers)
- Sort order: H first, then M, then L; within each priority, earliest due date first, TBD last

#### 1d) Recalculate summary counts

- Count actual open `[ ]` items by priority (H/M/L)
- Count Waiting on Others items
- Update the Summary section with accurate numbers

#### 1e) Refresh the Stale Items section

- Scan open items for due dates in the past (specific dates, "This week" from 2+ weeks ago, "OVERDUE" tags)
- Regenerate the "Stale Items for Review" section with current data
- Remove entries for items that have since been completed or dropped
- Calculate weeks late based on today's date

#### Housekeeping output

After housekeeping completes, before the meeting extraction results, output a brief summary:

```
## Housekeeping
- Archived: X completed, Y dropped
- Malformed rows: Z (see below)
- Stale items: N open items overdue
- Renumbered: [old count] → [new count] open items
```

### Step 2: Get recent meetings from Granola

1. Use `mcp__claude_ai_Granola__list_meetings` to get all meetings from the last 2 working days
   - Working days = Monday-Friday, skip weekends when calculating
   - Use `time_range: "this_week"` if the last 2 working days fall within the current week
   - Use `time_range: "custom"` with `custom_start` and `custom_end` (ISO date format) if you need to span across weeks (e.g. Monday looking back to Thursday/Friday)
   - This returns ALL meetings in the range — no keyword matching needed
2. Filter the returned meetings to only those within the last 2 working days

### Step 3: Get meeting content

1. Use `mcp__claude_ai_Granola__get_meetings` to retrieve notes and summaries in batch (up to 10 meeting IDs per call)
2. For meetings with sparse summaries, use `mcp__claude_ai_Granola__get_meeting_transcript` to get the full transcript
3. Extract all action items, particularly those assigned to the PM's name or "me"
4. Also extract items marked for monitoring or follow-up

### Step 4: Process action items

1. For each action item, determine:
   - **Priority**: H (High), M (Medium), L (Low) based on urgency language, deadlines mentioned, or business impact
   - **Due Date**: Extract from meeting notes if mentioned (e.g., "before next week", "tomorrow", "by Friday"), otherwise set as "TBD"
2. High priority indicators: "urgent", "ASAP", "before next", "critical", "blocker", specific near-term dates
3. Medium priority indicators: general follow-ups, ongoing work, no specific deadline
4. Low priority indicators: "when possible", "eventually", nice-to-haves

### Step 5: Read existing todo list and check for stale items

1. Read the file at `team/{initials}/todo_list.md`
2. If the file doesn't exist, create it with the standard table header
3. Parse existing action items to avoid duplicates
4. **Stale check**: Scan open items for due dates that have passed (e.g. "This week" from 2+ weeks ago, specific dates in the past). Flag these in the output summary so the PM can decide whether to update, drop, or re-prioritise them

### Step 6: Update the todo list file

1. Add new action items to `team/{initials}/todo_list.md`
2. The file uses a single table sorted by priority (H first, then M, then L), then by due date (earliest first, TBD last)
3. Maintain the format:
   ```
   | # | Action Item | Priority | Due Date | Source | Done |
   |:-:|-------------|:--------:|----------|--------|:----:|
   | 1 | Action description | H | Date or TBD | Meeting Name (Feb 10) | [ ] |
   ```
4. The "Source" column records which meeting the item came from, with date in parentheses
5. Keep existing completed items (marked with `[x]`) in a separate "Completed" section at the bottom
6. Renumber items sequentially after sorting
7. Update the summary counts at the bottom

### Step 6a: Update Today's Focus section

1. After updating the main table, pick the **top 5 most actionable H-priority items due this week**
   - Prefer items that are blocking others, time-bound (specific dates this week), or have been explicitly requested by an exec
   - If fewer than 5 H items are due this week, include the most urgent M items to fill the list
2. Write (or overwrite) the "Today's Focus" section at the top of the todo list file, between the `# Action Items` heading and the `## How to use` section:
   ```
   ## Today's Focus ({day} {date, e.g. Monday 31 March})

   1. **{Action item}** — {1-line context on why now}
   2. **{Action item}** — {context}
   3. **{Action item}** — {context}
   4. **{Action item}** — {context}
   5. **{Action item}** — {context}

   _Refreshed by /todo on {date}. Full list below._
   ```
3. This section serves as the PM's daily "what matters" view — keep each item to one line

### Step 6b: Store key meeting notes in 1:1 context files

For each meeting processed in Steps 2-3, update the relevant 1:1 context file:

1. Determine the other person in each meeting (from the title or participants)
2. Generate the slug (lowercase, hyphenated, e.g. `alex-smith`)
3. Check if `team/{initials}/recurring-meeting-context/{slug}.md` exists
4. If the file exists:
   - Extract **key direction changes or decisions** from the meeting (not action items — those go in the todo list)
   - Update the "Latest Direction" section with a heading noting the date (e.g. `### From {date}`)
   - Move the previous "Latest Direction" content under a "### Previous Direction" sub-heading if it exists
   - Add any new carry-forward items (with `— added {date}`) to the "Carry-Forward Items" section
   - Do NOT duplicate items that already exist in carry-forwards
5. If the file does not exist but this person appears in meetings regularly (2+ times in the last 30 days), mention in the output: "No context file for {name}. Consider creating one at `team/{initials}/recurring-meeting-context/{slug}.md`"
6. Keep context file updates concise — capture direction and decisions, not a transcript summary

### Step 6d: Extract feedback signals for direct reports

After updating 1:1 context files (Step 6b), check if any processed meetings were 1:1s with one of {YOUR_NAME}'s 5 direct reports: {PM 1}, {PM 2}, {PM 3}, {PM 4}, {PM 5}.

For each direct report 1:1 found:

1. Re-read the meeting notes and transcript, looking for feedback-worthy signals:
   - Development theme discussions (progress, setbacks, coaching moments)
   - Specific examples of strength: clear thinking, good stakeholder management, strong execution, team leadership
   - Specific examples of growth areas: missing evidence, poor framing, scope creep, communication gaps
   - Commitments about behaviour change ("I'll try to...", "Next time I'll...")
   - {YOUR_NAME}'s coaching observations (what she noticed, what she pushed on)
2. For each signal found, append a lightweight dated entry to `team/{initials}/team-mgmt/feedback/{pm-slug}.md`:
   ```
   ### YYYY-MM-DD — 1:1
   - **Signal:** {What was observed or discussed — specific, factual}
   - **Theme:** {Which development theme this relates to, if any}
   ```
3. Read the existing feedback log first to avoid duplicating signals already recorded
4. Keep entries concise — this is a rolling signal log. Full theme synthesis happens quarterly via `/cr-quarterly-review`
5. If no feedback-worthy signals are found in a 1:1, skip silently

### Step 6c: Extract and log decisions

For each meeting processed in Steps 2-3, extract key decisions:

1. Re-read the meeting notes and transcripts, looking for:
   - Explicit decisions ("we decided", "agreed to", "going with", "confirmed", "signed off")
   - Direction changes ("instead of X, we'll do Y", "pivot to", "shifting approach")
   - Commitments with deadlines ("launching on", "shipping by", "targeting")
   - Approvals or rejections ("approved", "rejected", "not pursuing", "pausing")
2. For each decision, capture:
   - **Decision**: What was decided (one clear sentence)
   - **Meeting**: Which meeting, with date
   - **People involved**: Key participants in the decision
   - **Context**: Why this was decided (1 sentence)
   - **Follow-up**: Any immediate next steps or dependencies
3. Read `team/{initials}/decision-log.md`
4. Check for duplicate decisions — compare by meaning, not exact text
5. Add new decisions at the top of the "## Decisions" section, grouped under a date heading:
   ```
   ### {date, e.g. 31 March 2026}

   **{Decision summary}**
   - Meeting: {Meeting name}
   - People: {Names}
   - Context: {Why}
   - Follow-up: {Next steps, if any}
   ```
6. If no decisions were found, skip this section silently

### Step 7: Identify kudos opportunities

1. Re-read the meeting notes and transcripts from Step 3, looking for:
   - Explicit praise or thanks ("great job", "really impressed", "well done", "shout out")
   - Implicit recognition moments — someone delivered something ahead of schedule, unblocked a team, solved a difficult problem, went above and beyond, or had a notable impact
   - Positive mentions of a team member by name from other attendees
2. For each kudos opportunity found, capture:
   - **Who**: The person being recognised
   - **What**: What they did (specific and evidence-based)
   - **Source**: Which meeting and approximate context
3. Draft a short kudos message for each, written in {YOUR_NAME}'s voice (direct, warm, specific). Two versions:
   - **DM version**: A personal message to the individual (1-2 sentences, specific about what they did and why it mattered)
   - **Channel version**: A message suitable for a team kudos channel (slightly more public-facing, still specific)
4. If no kudos opportunities are found, skip this section silently

### Step 8: Report new actions, decisions, stale items, and kudos

1. Output a summary of NEW action items added to the terminal
2. Format as a clean list showing: Action, Priority, Due Date
3. If no new actions found, report "No new action items found"
4. If decisions were logged in Step 6c, list them after the actions summary
5. If stale items were found in Step 5, list them with a recommendation (update date, drop, or re-prioritise)
6. If kudos opportunities were found, output them after the stale items

## Step Priority

Steps 1-6a are **core** — always complete these. Steps 6b (context file updates), 6c (decision log), 6d (feedback signals), and 7 (kudos) are **best-effort** enhancements. If context is running low, skip 6b/6c/6d/7 and proceed to Step 8 (reporting). These can be run separately if needed.

## Output Format

```
## Housekeeping
- Archived: X completed, Y dropped
- Malformed rows: Z (see below)
- Stale items: N open items overdue
- Renumbered: [old count] → [new count] open items

## New Action Items Added

| Action | Priority | Due Date |
|--------|----------|----------|
| Item 1 | H | Feb 3 |
| Item 2 | M | TBD |

Total: X new items added to team/{initials}/todo_list.md

## Decisions Logged

| Decision | Meeting | People |
|----------|---------|--------|
| Decision summary | Meeting name (date) | Names |

Total: X new decisions added to team/{initials}/decision-log.md

## Stale Items (due dates passed)

| # | Action | Original Due | Suggestion |
|:-:|--------|-------------|------------|
| 3 | Item description | This week (Feb 3) | Update to next week / Drop / Re-prioritise |

## Kudos Opportunities

### {Person Name}
**What:** {Specific thing they did}
**Source:** {Meeting name (date)}

**DM to {first name}:**
> {Draft personal message}

**#kudos channel:**
> {Draft public message}
```
