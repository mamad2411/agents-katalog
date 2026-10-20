<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: Generate full daily brief — day plan with prioritised todos, meeting prep, and delivery to file/Telegram/Slack -->

# Daily Prep

Prep me for the day: review my calendar, prioritise my todo list, find focus time for high-priority work, and prep for each meeting. Save the output and deliver it to Telegram and Slack.

## Instructions

### Step 0: Identify the user

- Check auto-memory (MEMORY.md) for the user's initials, name, direct reports, and manager
- Set `{initials}` accordingly (e.g. `CR`)

### Step 1: Gather inputs (parallelise all of these)

1. **Todo list** — Read `team/{initials}/todo_list.md`
   - Extract ALL open (not done) items from the main table
   - Note priority (H/M/L), due date, and whether overdue
   - Also extract "Waiting on Others" items

2. **Calendar** — Use `mcp__claude_ai_Google_Calendar__gcal_list_events` to get all events for today
   - Set `condenseEventDetails: false` — you need the full attendee list to filter by meeting size
   - If Calendar MCP is unavailable, fall back to reading 1:1 context files for known recurring meetings

3. **Current priorities** — Read `context/current-priorities.md` for squad RAG statuses and initiative updates

4. **Agent state files** — Read the following files if they exist (skip silently if missing):
   - `team/{initials}/agents/cos.md` — extract overdue follow-ups (Active items with status "chasing" where follow-up date is past by >3 working days), extract watch list items relevant to today or this week
   - `team/{initials}/agents/analyst.md` — extract Active items (metric anomalies being watched), Segment health flags, any Experiments concluding this week
   - `team/{initials}/agents/uxr.md` — extract Active items (converging themes), any signals relevant to today's meetings
   - `team/{initials}/agents/coach.md` — extract Development tracker ratings and trends, Review compliance (flag any overdue reviews), Active items (operating themes)
   - `team/{initials}/agents/manager.md` — extract PM tracker (per-PM three-pillar status), Active items (flags needing attention), any overdue Q1 reviews or Q2 goals
   - `team/{initials}/agents/strategist.md` — extract Active items (open commitments to leadership), Exec feedback tracker, any approaching deadlines
   - `team/{initials}/agents/product-manager.md` — extract Active investigations (what's being investigated and at what phase), Experiment pipeline (what's running), any blocked items or open threads
   - For each agent, note the "Last refreshed" timestamp — if stale (>48 hours on a working day), flag it in the brief

5. **Shared memory** — Read `team/{initials}/agents/memory/shared.md` if it exists. Use this for cross-cutting institutional knowledge that may be relevant to today's meetings or decisions (e.g. seasonal patterns, known data gotchas, stakeholder preferences). Do not read per-agent memory files — they're too detailed for a daily brief.

### Step 2: Identify qualifying meetings

From the calendar, keep only:
- 1:1s, recurring syncs, small group meetings (6 or fewer attendees)
- Meetings the user is actively participating in
- Skip: all-hands, town halls, focus time, lunch blocks, travel blocks, interviews with external candidates, social events (drinks etc.)

Flag any time conflicts between qualifying meetings.

### Step 3: Identify focus windows

Look at the full calendar (including non-qualifying events) and find gaps of 30+ minutes where no meeting is scheduled. These are potential focus windows for working on todo items.

### Step 4: Prioritise today's todos

From the full todo list, select the top items to focus on today. **Cross-reference against `context/current-priorities.md`** to ensure Today's Focus advances the Big Bets and top company priorities, not just the most urgent operational items.

Prioritise by:
1. Items that directly advance a Big Bet or Must Deliver initiative (check current-priorities.md)
2. Items due today
3. H-priority items that are overdue
4. H-priority items due this week
5. Items that can be actioned in a specific meeting today (tag which meeting)
6. Quick wins (items that can be closed in <15 mins)

If Today's Focus ends up being entirely operational (no strategic/priority-aligned items), flag this explicitly: "Today's focus is operational — no Big Bet or strategic items are progressing today."

Select up to 5 items for "Today's Focus" and tag each with when to tackle it:
- A specific meeting (e.g. "raise in 1:1 with {person}")
- A specific focus window (e.g. "09:30–10:00 gap")
- Async (e.g. "send a message/email between meetings")

### Step 5: Gather meeting context (parallelise where possible)

For each qualifying meeting in chronological order:

1. **Identify** the key person, determine the slug (lowercase, hyphenated, e.g. `alex-smith`)
2. **Classify** as: `report`, `manager`, or `other`
3. **Recurring meeting context file** — Read `team/{initials}/recurring-meeting-context/{slug}.md` if it exists
4. **Previous meetings (Granola)** — Use `mcp__claude_ai_Granola__query_granola_meetings` or `mcp__claude_ai_Granola__list_meetings` to find recent meetings with this person. Get details with `mcp__claude_ai_Granola__get_meetings`. If notes are sparse, use `mcp__claude_ai_Granola__get_meeting_transcript`
5. **Todo list** — Filter for items mentioning this person in the Source column or Waiting on Others
6. **Goals** (reports and manager only) — From `context/current-priorities.md`, get their squad's RAG status and latest update. For manager meetings, use the user's own initiatives
7. **Slack context** — Use `mcp__claude_ai_Slack__slack_search_public` to search for recent messages from or mentioning this person (last 3 days). Look for active threads, questions, decisions. Summarise anything relevant. Skip if nothing useful

### Step 6: Compile the brief

Use Slack mrkdwn formatting (compatible with both Slack and markdown).

**Slack formatting rules** (critical — the Slack API rejects invalid formatting):
- Do NOT use emoji shortcodes (`:dart:`, `:calendar:`, `:warning:`, `:speech_balloon:`, `:laptop:`, etc.) — these cause `invalid_blocks` errors in `slack_send_message`
- Use Unicode emoji instead: dart → target emoji, calendar → calendar emoji, warning → triangle emoji, etc.
- Or simply omit emoji entirely — plain text with bold headers is fine

#### Section 1: Today's Focus

```
*:dart: Today's Focus — {Day Date Month, e.g. Thursday 2 April}*

1. {Focus item 1} — _{when to tackle}_ _(H)_
2. {Focus item 2} — _{when to tackle}_ _(H)_
3. {Focus item 3} — _{when to tackle}_ _(H)_
4. {Focus item 4} — _{when to tackle}_ _(H)_
5. {Focus item 5} — _{when to tackle}_ _(H/M)_
```

#### Section 1b: Chase List (from COS state)

If COS state exists and has overdue Active items (follow-up date past by >3 working days):

```
*Chase List*

- {item} — {owner} — {N} days overdue
- {item} — {owner} — {N} days overdue
```

If COS state is stale (>48 hours), show: `_COS state is {N} days old — follow-up data may be outdated_`

If no COS state file exists, omit this section entirely.

#### Section 1c: Agent Insights (from agent state files)

Include if any agent state file exists. Keep this tight — max 8 bullets total across all agents for actionable items. Only surface items that are actionable today or relevant to today's meetings.

**Coverage requirement:** For every peer agent state file read in step 4 (cos, analyst, uxr, coach, manager, strategist, product-manager), include a one-line entry in this section — either an actionable bullet OR an explicit "nothing to surface today" line. This makes absence intentional rather than silent and lets {YOUR_NAME} audit that every agent was checked.

```
*Agent Insights*

- {Analyst} {metric} is {status} — {1-line context, e.g. "engagement softening for 3 weeks, approaching alert threshold"}
- {UXR} {theme} — {strength, e.g. "Converging across 3 sources"} — relevant to {today's meeting if applicable}
- {Coach} Development: {priority} rated {rating} for {N} weeks — {observation}
- {Manager} {PM name}: {flag, e.g. "Q1 review overdue" or "recurring 1:1 theme: X"}
- {Strategist} Commitment to {exec}: {item} — due {date}
- {Agent name} — _nothing to surface today_   ← use this line when an agent state was read but has no actionable items
```

If any agent state is stale (>48 hours), add: `_{Agent} state is {N} days old_`

If no agent states exist, omit this section entirely.

#### Section 2: Day Plan (chronological)

Show the full day as a timeline, interleaving meetings with focus windows. This is the core of the brief — it should read as a plan for the day.

```
*:calendar: Day Plan*

*{time}* — :speech_balloon: *{Meeting Name}* ({type})
_Prep: {1-line summary of what to cover — reference suggested topics}_

*{time}–{time}* — :laptop: *Focus: {todo item or theme}*
_{why now: e.g. "30-min gap before next meeting", "prep for afternoon 1:1"}_

*{time}* — :speech_balloon: *{Next Meeting}* ({type})
_Prep: {1-line summary}_

... and so on through the day
```

Rules for the Day Plan:
- Show ALL calendar events (meetings, travel, lunch) so the user sees the full picture
- For qualifying meetings, include the 1-line prep summary
- For non-qualifying events (travel, lunch, drinks), just show the name
- For focus windows of 30+ mins, suggest a specific todo item to work on, chosen from Today's Focus or the extended list
- For short gaps (15–30 mins), suggest quick wins or async actions (messages, emails)
- Flag conflicts clearly with a :warning: emoji and a recommendation on which to attend

#### Section 3: Meeting Prep (detailed)

For each qualifying meeting, include the full prep block:

```
---

*{time} — {Person Name}* ({report / manager / other})
_Last met: {date} - {1-sentence summary of last meeting}_

*Open actions:*
- {action — owner — status}
(or "None" if no relevant items)

*Goals:* {squad} — {RAG emoji :large_green_circle: :large_orange_circle: :red_circle:} {1-line status update}
_(only for reports and manager meetings)_

*Suggested topics:*
1. {topic} — _{reason}_
2. {topic} — _{reason}_
3. {topic} — _{reason}_

*Dev themes:* {1-line per theme, comma-separated}
_(only for report meetings)_
```

Keep each meeting brief to ~10-12 lines.

#### Section 4: Extended Todo List

At the bottom, include a broader view of open work. This helps the user see what else is on the horizon beyond today's focus.

```
---

*:clipboard: Open Todos*

*High priority (not in today's focus):*
- #{num} {item} — _{due date or "overdue"}_
- #{num} {item} — _{due date}_
...

*Waiting on others (overdue):*
- {item} — {who} — _{requested date}_
...

*This week (medium):*
- #{num} {item}
...

_{X} total open items | {Y} high priority | {Z} overdue_
```

### Step 7: Save and deliver

1. **Save to file** — Write to `team/{initials}/daily-prep/daily-prep-{YYYY-MM-DD}.md`. Create the `daily-prep` folder if it doesn't exist
2. **Send to Slack** — Use `mcp__claude_ai_Slack__slack_send_message` to post a **condensed version** to `{your-agent-channel}` (channel ID: `{your-slack-channel-id}`)
   - Slack has a ~4000 character limit per message. The full brief will exceed this
   - Send only Section 1 (Today's Focus), Section 1b (Chase List), Section 1c (Agent Insights), and Section 2 (Day Plan) to Slack
   - Omit the detailed Meeting Prep and Extended Todo List sections
   - Add a footer: `_Full brief with meeting prep: team/{initials}/daily-prep/daily-prep-{YYYY-MM-DD}.md_`
   - If the condensed version still exceeds the limit, send just Section 1 (Today's Focus) and Section 2 (Day Plan)
3. **Send to Telegram** — Run the Telegram notification via bash, sending the **condensed version** (same content as Slack: Today's Focus + Agent Insights + Day Plan):
   ```
   source scripts/notify-telegram.sh && source scripts/.env && send_telegram "{condensed brief text}"
   ```
   Do NOT just send a "brief ready" notification — send the actual plan content so {YOUR_NAME} can read it on her phone. If the content exceeds Telegram's 4096 character limit, truncate after the Day Plan section and add a note to check Slack for the full version.
   If Telegram fails, note it but don't block
4. **Update COS state** — If `team/{initials}/agents/cos.md` exists, update "Last refreshed" timestamp to now and "Next due" to the next working day
5. **Show in terminal** — Display the brief to the user

## Important

- Run Granola, calendar, Slack, and file reads in parallel where possible
- If a data source fails (Granola down, no context file), note it briefly and continue with what's available
- Use UK date format (2 April, not April 2)
- Do not include raw file contents — synthesise into concise bullets
- The Day Plan section is the most important part — it should feel like an actionable schedule, not just a list
- If there are no qualifying meetings today, still generate the Day Plan with focus windows and the todo sections
