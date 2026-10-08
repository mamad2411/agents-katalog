# Meeting Follow-up — Fullerton Rotary Club

## Metadata
- **Name:** meeting-follow-up
- **Description:** Detect completed meetings and extract action items for task creation
- **Schedule:** Every 30 min, 8 AM–6 PM PT weekdays
- **Model:** claude-sonnet-4-6 (detection), claude-opus-4-6 (task creation)
- **Channel:** slack:#internal-rotary

## Two-Phase Architecture

### Phase 1: Detection (Sonnet — fast, frequent)
1. Check Google Calendar for meetings that ended in the last 30 minutes
2. Look for meeting notes in Google Docs or calendar event descriptions
3. If a new completed meeting is found with notes, proceed to extraction
4. If no new meetings, exit silently

### Phase 2: Extraction & Approval (Opus — deep reasoning)
1. Parse meeting notes for:
   - **Action items** — things someone committed to doing
   - **Decisions made** — conclusions the group reached
   - **Follow-ups needed** — items requiring further discussion
2. Format extracted items and post to #internal-rotary for approval
3. Wait for human response before creating ClickUp tasks

## Approval Flow

Post to Slack:
```
Meeting follow-up: [Meeting Name] ([Date])

Action items detected:
1. [Action] — suggested assignee: [Name], due: [Date]
2. [Action] — suggested assignee: [Name], due: [Date]
3. [Action] — suggested assignee: [Name], due: [Date]

Reply with numbers to create as tasks (e.g., "1, 3"), "all", or "none".
```

On approval:
- Create ClickUp tasks in the Rotary folder
- Set assignee and due date as approved
- Confirm creation with task links

## Meeting Types to Track

- **Weekly club meeting** — primary source of action items
- **Board meetings** — governance decisions and committee assignments
- **Committee meetings** — project-specific tasks
- **District events** — external commitments and deadlines

## Rules

- Never create tasks without approval
- If meeting notes are ambiguous, ask for clarification rather than guessing
- Group related action items together
- Include the meeting context (who was there, key discussion topics) in task descriptions
