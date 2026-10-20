<!-- owner: shared | audience: all-pms | last-updated: 2026-04 -->
<!-- purpose: Find mutual availability and schedule a meeting with one or more people -->

# Meeting Schedule

Find a mutually available time slot and schedule a meeting, respecting focus time and meeting clustering preferences.

## Instructions

### Step 0: Parse arguments

- The user provides arguments in the format: `$ARGUMENTS`
- Expected format: `{name1}, {name2}, ... [| duration: {minutes}] [| title: {text}]`
- Pipe `|` separates the attendee names from optional parameters
- **Names**: comma-separated list of people to meet with
- **duration**: meeting length in minutes (default: 30)
- **title**: meeting title (default: auto-generated from attendee names, e.g. "{YOUR_NAME} / Alex sync")
- If no arguments are provided, use `AskUserQuestion` to ask who the meeting is with

Examples:
- `{PM 5}` → 30 min meeting with Alex
- `Alex, Sam | duration: 60` → 60 min meeting with Alex and Sam
- `{CPO} | duration: 45 | title: Product strategy check-in` → 45 min meeting with {CPO}

### Step 1: Resolve names to email addresses

For each name provided, resolve to an email address using Slack:

1. Use `mcp__claude_ai_Slack__slack_search_users` for each name — run all searches in parallel
2. Handle results:
   - **1 match** — use the email from their Slack profile
   - **Multiple matches** — present the options via `AskUserQuestion` and ask the user to pick
   - **0 matches** — ask the user to provide the email address directly via `AskUserQuestion`

Collect all resolved email addresses before proceeding.

### Step 2: Find candidate time slots

Use `mcp__claude_ai_Google_Calendar__gcal_find_meeting_times` with:
- All attendee email addresses
- `startHour: 9`
- `endHour: 17`
- `maxResults: 15`
- Search window: next 5 working days (Monday–Friday)
- Duration: as parsed from arguments (default 30 mins)

From the results, **filter out** any slots starting before 09:30.

If no slots are returned:
1. Expand the search window to 10 working days
2. If still no slots, inform the user and ask if they want to try a different duration or time range

### Step 3: Filter and score candidates

#### 3a: Get the organiser's calendar

Use `mcp__claude_ai_Google_Calendar__gcal_list_events` to pull the organiser's events for the same search window.

#### 3b: Filter out focus time conflicts

Remove any candidate slots that overlap with events matching these keywords (case-insensitive) in the event title:
- "focus", "deep work", "planning time", "heads down", "no meetings", "focus time", "blocked", "do not book"

If **all** candidate slots overlap with focus time:
- Re-include them but flag each with a warning: "⚠ overlaps with {event name}"
- Note this when presenting options to the user

#### 3c: Score by adjacency

For each remaining candidate slot, score based on proximity to existing meetings:

| Condition | Score |
|-----------|-------|
| Back-to-back with another meeting (gap ≤ 15 mins) | +2 |
| Within 30 mins of another meeting | +1 |
| Would fragment a free block of 2+ hours | -1 |

#### 3d: Rank and present

1. Sort candidates by: score (descending), then chronological order (ascending)
2. Select the top 3 candidates
3. Present via `AskUserQuestion` with format:
   ```
   {Day} {Date} at {time}–{time} (score: {n}) {warnings if any}
   ```
4. Include a 4th option: "None of these — widen search or relax constraints"

### Step 4: Create the event

Once the user selects a slot:

1. Use `mcp__claude_ai_Google_Calendar__gcal_create_event` with:
   - **title**: as provided or auto-generated (e.g. "{YOUR_NAME} / Alex sync")
   - **startTime** and **endTime**: from the selected slot
   - **attendees**: all resolved email addresses
   - **addGoogleMeetLink**: `true`
   - **sendUpdates**: `"all"`
2. Confirm to the user: "Scheduled {title} on {day} {date} at {time} with {names}. Calendar invite sent to all attendees."

### Step 5: Handle "none of these"

If the user selects the "none" option:

1. Ask via `AskUserQuestion`:
   - "Expand search to 10 working days"
   - "Try a different duration"
   - "Include slots that overlap focus time"
   - "I'll schedule manually"
2. If they choose to expand or relax, re-run from Step 2 with adjusted parameters
3. If they choose manual, end the command

## Important Notes

- Always use UK date format (e.g. Wednesday 2 April, not April 2)
- Keep the interaction quick — the whole flow should feel faster than manually checking calendars
- Don't over-explain scores to the user. Present the ranked options clearly; scores are internal logic
- If Calendar or Slack MCP is unavailable, inform the user and suggest they schedule manually
- The organiser is always the current user (whoever runs the command)
