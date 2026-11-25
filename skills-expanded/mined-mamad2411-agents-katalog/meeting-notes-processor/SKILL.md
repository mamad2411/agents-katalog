---
name: meeting-notes-processor
description: Turn raw meeting transcripts, voice notes, or messy bullet-point notes into structured meeting summaries with decisions, action items, owners, and deadlines. Use when the user pastes a call transcript, meeting notes, or audio transcription and needs a clean, shareable summary. Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today."
---

# Meeting Notes Processor

Source: @ai_slacker "25 Powerful AI Skills, Agents & Automations You Can Build Today" (Beginner Tier, #2).

> Turns raw meeting transcripts into structured summaries with action items and owners.

## What this skill produces

From any raw meeting input (transcript, voice-to-text dump, rough bullet notes):
- **Meeting header**: date, attendees, topic/goal
- **Summary**: 3–5 sentences covering what was discussed and decided
- **Key decisions**: what was agreed, who decided, any vote or condition
- **Action items table**: task | owner | deadline | priority
- **Open questions**: things raised but not resolved — needs a next meeting or async follow-up
- **Optional**: suggested follow-up meeting agenda based on open items

## Copy-paste prompt to use

```
You are an expert meeting facilitator and note-taker.

Here are the raw notes/transcript from a meeting:

[PASTE MEETING TRANSCRIPT OR NOTES HERE]

Context (optional):
- Meeting type: [STANDUP / PROJECT REVIEW / CLIENT CALL / BRAINSTORM / etc.]
- Attendees and their roles: [IF KNOWN]
- Project or context: [BRIEF DESCRIPTION]

Please produce a structured meeting summary with:

1. Meeting header (date if mentioned, attendees, topic)
2. Executive summary (3–5 sentences — what was discussed, what was decided)
3. Key decisions (bullet list — each decision on one line, with owner if clear)
4. Action items table:
   | Task | Owner | Deadline | Priority |
   |------|-------|----------|----------|
5. Open questions (unresolved items that need follow-up)
6. Suggested next-meeting agenda (2–3 items based on open questions)

Rules:
- Only capture what was actually said — do not invent or infer decisions
- If an owner is unclear for an action item, mark it [TBA]
- If no deadline was mentioned, mark it [No date set]
- Keep the summary factual and neutral — no interpretation
```

## Automation option

Pair with `n8n-agent-builder` to build a fully automated pipeline:
- Trigger: email arrives with meeting transcript attachment, or Otter.ai/Fireflies webhook fires
- Action: Claude processes it with this prompt
- Output: structured summary posted to Slack, saved to Notion, or emailed to attendees

## Related skills

- **n8n-agent-builder**: Automate transcript → summary pipeline
- **internal-comms**: Format the summary output for team-wide distribution
- **doc-coauthoring**: Turn recurring meeting summaries into a running project log
