---
name: meeting-notes-distiller
description: Use when given a meeting transcript or raw notes to produce a structured summary — decisions made, action items (with owner + due date), risks/blockers, open questions, and a follow-up email draft. Vendor-neutral; works with output from any transcription provider.
---

# Meeting Notes Distiller

## When to invoke
- "Summarize this meeting transcript."
- "Extract action items from these notes."
- "Draft a follow-up email from this meeting."

## Inputs needed
1. **Transcript or notes** — plain text, Markdown, VTT, or SRT.
2. **Attendees** (optional) — to disambiguate owner attribution.
3. **Meeting purpose** (optional) — improves the summary framing.

## Workflow
1. **Clean** — strip timestamps, speaker tags, filler tokens.
2. **Extract**:
   - Decisions (what was agreed)
   - Action items (action, owner, due date)
   - Risks / blockers
   - Open questions
3. **Validate** — every action item must have an owner; flag unowned ones.
4. **Draft** a follow-up email summarizing the above.

## Output format
```
## Summary
## Decisions
## Action items
| # | Action | Owner | Due | Source line |
## Risks / blockers
## Open questions
## Follow-up email (draft)
```

## Guardrails
- Never invent owners, dates, or decisions not in the source.
- Mark items missing an owner as `(unowned)` and surface them.
- Quote the source line/index for every action item.

## Reference code
`distill.py` does pattern-based extraction (timestamps, speaker tags, action verbs, due-date phrasing).
