<!-- owner: shared | audience: all-pms | last-updated: 2026-03 -->
<!-- purpose: Generate a structured prep brief for an upcoming 1:1 or recurring meeting -->

# Meeting Prep

Generate a prep brief for an upcoming meeting by pulling context from previous meetings, open actions, quarterly goals, and the person's 1:1 context file.

## Instructions

### Step 0: Parse arguments and identify the meeting

- The user provides arguments in the format: `$ARGUMENTS`
- Expected format: `{person name}` (e.g. `{CPO}`, `Alex`, `Product small group`)
- If no argument is provided:
  1. Use `mcp__claude_ai_Google_Calendar__gcal_list_events` to get events in the next 24 hours
  2. Filter to meetings that look like 1:1s or recurring syncs (exclude all-hands, large group meetings, focus time)
  3. Present the next 3 candidate meetings using `AskUserQuestion` and ask the user to confirm which one to prep for
- Once the meeting is identified, determine:
  - **Person name** — the other attendee (for 1:1s) or the meeting name (for group meetings)
  - **Slug** — lowercase, hyphenated version (e.g. `alex-smith`, `jane-doe`)
- Check the auto-memory (MEMORY.md) to identify the user's initials and their direct reports/manager
- Classify the meeting type:
  - **report** — if the person is one of the user's direct reports
  - **manager** — if the person is the user's manager
  - **other** — any other meeting (peer, exec, group sync)

### Step 1: Gather context (run in parallel)

Pull from all available sources. Run independent queries in parallel.

1. **Recurring meeting context file** — Read `team/{initials}/recurring-meeting-context/{slug}.md`
   - If the file exists: extract standing topics, development themes, carry-forward items, and relationship notes
   - If the file does not exist: note this and proceed. After the brief is generated, offer to create one

2. **Previous meeting notes (Granola)** — Use `mcp__claude_ai_Granola__list_meetings` (with `last_30_days` or a custom range) to find recent meetings, then filter by this person's name in the title or participants to identify the most recent 1-3 meetings
   - Use `mcp__claude_ai_Granola__get_meetings` (batch, up to 10 IDs) to retrieve notes and summaries
   - If notes are sparse (just a few words or empty), use `mcp__claude_ai_Granola__get_meeting_transcript` and extract key points
   - From the most recent meeting, extract:
     - Topics discussed
     - Decisions made
     - Open actions (especially anything assigned to the user or the other person)
     - Unresolved questions or threads

3. **Todo list** — Read `team/{initials}/todo_list.md`
   - Filter for items where the Source column mentions this person's name or a meeting with them
   - Also check any "Waiting on Others" section for items assigned to or involving this person
   - Note overdue items separately

4. **Goals and priorities** (for `report` and `manager` types only) — Read `context/current-priorities.md`
   - For **reports**: find their squad's initiatives and extract current RAG status and latest update
   - For **manager**: find the user's own initiatives and extract current RAG status and latest update

5. **Feedback context** (for `report` type only) — Read `team/{initials}/feedback/my-team/{slug}.md`
   - Extract the Q2 development priorities (or most recent quarter's priorities) — just the headlines, not the full narrative
   - Note any gaps flagged for filling in 1:1s

### Step 2: Build the prep brief

Compile the gathered information into a structured brief. Keep it concise and scannable — this is a working document, not a report.

**For report 1:1s:**

```
# {Name} 1:1 Prep — {Date}

## Last Meeting
- **Date:** {date of last meeting}
- **Key topics:** {bulleted list}
- **Decisions:** {what was agreed}
- **Open actions:**
  - [ ] {action — who owns it — status if known}

## Their Goals & Progress
- **Squad:** {squad name}
- **Metric:** {owned outcome metric}
- **Initiatives:** {from current-priorities.md with RAG status}

## Open Actions (from todo list)
- {items sourced from or related to this person}

## Waiting On Them
- {items from "Waiting on Others" involving this person}

## Development Themes
- {concise themes from feedback file — just enough to prompt the right questions}

## Suggested Agenda
1. {topic} — {why: e.g. "overdue action", "RAG change", "development theme to revisit"}
2. {topic}
3. {topic}

## Standing Topics & Carry-Forward
- {from context file — recurring items to check}
```

**For manager 1:1s:**

```
# {Name} 1:1 Prep — {Date}

## Last Meeting
- **Date:** {date of last meeting}
- **Key topics:** {bulleted list}
- **Outcomes:** {what was decided}
- **Open actions:**
  - [ ] {action — who owns it — status if known}

## My Updates to Share
- **Initiative progress:** {from current-priorities.md — the user's RAG items and latest status}
- **Team updates:** {notable progress or blockers from reports, if known from recent context}
- **Decisions needed:** {anything requiring the manager's input or sign-off}

## Open Actions
- {items from todo list sourced from meetings with this person}

## Waiting On Them
- {items from "Waiting on Others" involving this person}

## Topics to Raise
1. {topic} — {why}
2. {topic}

## Standing Topics & Carry-Forward
- {from context file}
```

**For other meetings:**

```
# {Meeting Name} Prep — {Date}

## Last Meeting
- **Date:** {date of last meeting}
- **Key topics:** {bulleted list}
- **Open actions:**
  - [ ] {action}

## Related Open Actions (from todo list)
- {items with source matching this meeting or person}

## Suggested Topics
1. {topic} — {why}
```

### Step 3: Prioritise the suggested agenda

Order suggested agenda items by:
1. Overdue actions or commitments not yet delivered
2. Items with RAG changes or emerging blockers (reports only)
3. Development themes that haven't been discussed recently (reports only)
4. Carry-forward items from the context file
5. New topics surfaced from the most recent Granola meeting

### Step 4: Present and refine

1. Display the prep brief in the terminal
2. Ask: "Anything to add, change, or remove before the meeting?"
3. If the user adds or changes items, update the brief

### Step 5: Update carry-forward items

1. If the 1:1 context file exists:
   - Ask if any carry-forward items should be marked as resolved
   - Add any new carry-forward items the user mentioned
   - Update the file
2. If the file does not exist:
   - Ask: "No context file exists for {name}. Want me to create one at `team/{initials}/recurring-meeting-context/{slug}.md`?"
   - If yes, create it using the basic template, pre-populated with what was gathered

## Important Notes

- Keep the brief concise. Each section should be scannable in under 30 seconds
- Don't fabricate information. If Granola returns no previous meetings, say "No previous meeting found in Granola." If there are no relevant todo items, say "None." Gaps are useful signal
- If multiple recent meetings are found, use the most recent for the recap but note if themes recurred across meetings
- The command should work even with minimal data — a useful brief can be generated from just the todo list and current priorities
- Don't save the brief to a file unless the user asks. It's ephemeral — Granola captures what actually happens in the meeting
- Read reference files silently — don't output their raw content, just synthesise into the brief
