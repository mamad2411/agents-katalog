---
name: meeting-decision-log-extractor
description: Vendor-neutral skill to extract decisions and action items from a meeting transcript and produce a decision log plus an action register.
---

## When to invoke
- You have a meeting transcript (or notes) and need structured decisions/action items.
- You want to standardize follow-ups and ownership.

## Inputs needed
- Transcript text file (UTF-8).
- Optional participant list.

## Workflow
1. Segment transcript into lines and identify speaker prefixes.
2. Detect decision statements (e.g., “we will…”, “decided…”, “approved…”).
3. Detect action items (e.g., “ACTION:”, “owner”, “by <date>”, “TODO”).
4. Extract owner and due date with lightweight heuristics.
5. Output Markdown with two tables: decisions and actions.

## Output format
Markdown with:
- Decisions table (id, decision, owner, date)
- Action items table (id, action, owner, due date)
- “Uncertain extractions” section

## Guardrails
- Mark low-confidence rows as uncertain; do not invent owners/dates.
- Keep raw quoted text snippets so a human can verify.

## Reference code
- `extract_decisions.py` reads a transcript (.txt) and writes Markdown.
