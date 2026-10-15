---
name: zoom-meeting-notes
description: Use when given a Zoom meeting transcript or conversation to extract structured meeting notes, decisions, action items, and insights. Skip casual greetings, off-topic chat, and filler. Output a formatted .md document.
---

# Zoom Meeting Notes

## Overview

Extract structured, complete notes from a Zoom transcript. Capture every substantive point; omit only greetings, farewells, off-topic tangents, and filler ("uh", "um", "like").

## Output Document Structure

Produce `meeting-notes-<YYYY-MM-DD>.md` (use meeting date if known, else today's date).

**Filename convention is mandatory.** NEVER use alternative formats (`zoom_discussion_*`, `david_zoom_notes_*`, `<DD-MM-YYYY>_*`, etc.). If a file for that date already exists, append `-a`, `-b`, `-c` (e.g. `meeting-notes-2026-04-24-a.md`, `meeting-notes-2026-04-24-b.md`) — NEVER overwrite and NEVER invent new naming schemes.

```markdown
# Meeting Notes — <Title or inferred topic>

**Date:** YYYY-MM-DD  
**Attendees:** comma-separated list of names/roles seen in transcript  
**Duration:** (if determinable)

---

## Summary
2–4 sentence executive summary of what the meeting accomplished.

## Key Discussion Points
Numbered list. Each item: topic + what was said/decided/debated.
- Include supporting details, context, concerns raised.
- One sub-bullet per distinct sub-point.

## Decisions Made
- [ ] Decision text — owner (if named)

## Action Items
| # | Action | Owner | Due Date |
|---|--------|-------|----------|
| 1 | ...    | ...   | ...      |

## Open Questions / Parking Lot
- Unanswered questions, deferred topics, items flagged for follow-up.

## Risks / Blockers Mentioned
- Any blockers, dependencies, concerns, or risks called out.

## Insights & Notable Observations
- Non-obvious observations, strategic context, strong opinions, tensions.

## Next Steps / Follow-up Meetings
- Scheduled or proposed follow-ups with dates/owners if mentioned.
```

## Rules

**Always capture:**
- All decisions (even tentative ones)
- Every action item with owner + due date if stated
- Technical details, numbers, metrics, names of systems/tools
- Disagreements and their resolution (or lack thereof)
- Commitments made by any party
- Risks, blockers, dependencies
- Non-obvious context or strategic rationale

**Skip:**
- Greetings/farewells ("Hey!", "Talk soon", "Bye")
- Small talk unrelated to work ("How was your weekend?")
- Pure filler and false starts
- Repeated rephrasing of the same point (consolidate, don't duplicate)

**Handling ambiguity:**
- Infer action item owner from context ("I'll take care of that" → speaker)
- Mark inferred owners with `(inferred)`
- If date missing: write `TBD`
- If topic unclear: use `[unclear — see transcript]`

## Example Invocation

User provides transcript text or file path. You:
1. Parse all speakers and timestamps
2. Build each section above
3. Write to `meeting-notes-<YYYY-MM-DD>.md` in CWD (append `-a`/`-b` if date already exists)
4. Return: file path + count of action items found

## Common Mistakes

- Missing implicit action items (someone says "I should look into that" — capture it)
- Dropping numbers/metrics mentioned in passing
- Collapsing two distinct decisions into one bullet
- Skipping "parking lot" items (things flagged but not resolved)
