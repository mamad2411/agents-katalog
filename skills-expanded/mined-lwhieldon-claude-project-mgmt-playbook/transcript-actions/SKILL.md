---
name: transcript-actions
description: Extract action items, decisions, open questions, and risks from a meeting transcript or rough notes, with a short summary. Use after any client or internal call. Usage - /transcript-actions path/to/transcript.txt
---

# Transcript Actions

Parse a meeting transcript and extract every action item, decision, open question, and risk, plus
a brief summary. Saves the 20 to 30 minutes of note cleanup that follows every call.

## Input

`$ARGUMENTS` is the path to a `.txt`, `.md`, `.docx`, or `.vtt` transcript exported from Teams,
Zoom, Otter.ai, or typed notes. Speaker labels help ("Sarah: We need to...") but are not required.
Partial or rough notes are fine.

If no path was given, ask for one.

If your organization has connected Microsoft 365 or another meeting tool to Claude and the
transcript is not on disk, you may fetch it through that connector, but name the meeting and
confirm with the user before reading it. Never work around a connector that is not available.

## Output

**Meeting Summary** (3 to 5 sentences): who attended, the stated purpose, and the top outcomes or
decisions.

**Decisions Made:**
- List each decision with context. Format: "[Decision]: [Rationale if stated]"

**Action Items:**
| # | Action | Owner | Due Date | Priority | Notes |
|---|---|---|---|---|---|

Extract all explicit and implied action items. If owner or due date is not stated, use `[TBD]`
and flag it. Never invent an owner or a date. Priority: High / Medium / Low based on language and
context.

**Open Questions / Parking Lot:**
- Items raised but not resolved during the meeting

**Risks or Concerns Flagged:**
- Any risks, blockers, or concerns mentioned, including informal ones

**Disagreements left open:**
- Any point where two people took different positions and the meeting moved on. These are the
  items someone will need to find later. Record positions, not impressions of people.

Be thorough. Do not summarize away specifics. The value is in the detail.

## Example Output

**Meeting Summary:** Sprint 3 retrospective with 6 team members and 2 client stakeholders (May 6, 2025). Team reviewed velocity showing a 12% shortfall against plan. Main outcome: agreed to reduce scope on the reporting module and add one buffer week before UAT. Client stakeholders requested a revised project plan by Friday.

**Action Items:**
| # | Action | Owner | Due Date | Priority | Notes |
|---|---|---|---|---|---|
| 1 | Revise project plan with updated UAT dates | Sarah M. | Fri May 10 | High | PMO sign-off required |
| 2 | Send updated scope reduction memo to client | PM | Mon May 13 | High | Draft first, PM to review |
| 3 | Schedule UAT kick-off call with client SMEs | Coordinator | Wed May 8 | Medium | Include test script overview |
