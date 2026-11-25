---
name: digest-meeting
description: Digest meeting notes/transcript and route findings to the correct repo files
alwaysApply: false
---

# Digest Meeting

Takes a meeting name or transcript, extracts decisions, action items, and context, then routes them to the correct files in the repo.

## Trigger

"digest the notes from [meeting name]" or "digest this meeting"

## Pre-Run

1. Read `.claude/skills/digest-meeting/gotchas.md` (if it exists)
2. Read the root `CLAUDE.md` meeting → file mapping table to know where content goes

## Execution

### Step 1: Get the Transcript
- If the user provides a meeting name, pull the transcript from your meeting tool (Granola, Otter, etc.)
- Use `get_meeting_transcript` for full verbatim content, then `get_meetings` for structured summary
- If the user pastes a transcript directly, use that

### Step 2: Identify the Meeting Type
- Match against the meeting → file mapping table in CLAUDE.md
- Determine: primary output location, secondary update targets

### Step 3: Extract Content
For each meeting, extract:
- **Decisions made** (with rationale)
- **Action items** (with owners and deadlines — convert relative dates to absolute)
- **Status updates** per project
- **Strategic signals** (anything that updates beliefs, competitive intel, or open questions)
- **Key context** that someone who missed the meeting would need

### Step 4: Route to Files
- **Primary output:** Create/append to the meeting notes file (e.g., `meetings/weekly/YYYY-MM-DD.md`)
- **Decisions:** Route to the relevant project's `decisions.md`
- **Project updates:** Route to the relevant project's `updates.md` (or `CONTEXT.md` if it changes the project narrative)
- **Strategy signals:** Update `strategy/beliefs.md`, `strategy/competitive.md`, or `strategy/open-questions.md` as appropriate
- **Action items:** Include in the meeting notes with clear owners

### Step 5: Propose Changes
- Show the user all proposed file changes before writing
- Include file paths so they can review routing
- Only write after approval

### Step 6: Commit
- Commit with message: `digest: [meeting name] — [date]`

## Post-Run

Append to `.claude/skills/digest-meeting/runs.log`:
```
[date] | [meeting name] | [files updated] | [issues encountered]
```

If any issues were encountered, also update `gotchas.md`.
