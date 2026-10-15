---
name: meeting-action-item-extractor
description: Vendor-neutral skill to extract action items (task, owner, due date) from a meeting transcript into structured JSON.
---

## When to invoke
- You have a meeting transcript and want a to-do list with owners and deadlines.
- You need consistent structure for feeding tasks into any project management system.

## Inputs needed
- `--transcript`: plain-text transcript file.
- (Optional) `--participants`: JSON array of participant names to help owner matching.

## Workflow
1. Read transcript and split into lines.
2. Detect action-item cues:
   - "action item", "AI:", "todo", "we should", "I'll", "I will", "can you"
3. Extract:
   - `task`: normalized imperative text
   - `owner`: inferred from speaker prefix (e.g., "Alex:") or matched participant name
   - `due_date`: parse simple natural phrases like "by Friday", "by 2026-06-01" (best-effort)
4. Deduplicate similar tasks.
5. Output JSON.

## Output format
JSON:
- `action_items`: list of `{task, owner, due_date, evidence}`
- `notes`: parsing assumptions and any ambiguous items

## Guardrails
- If owner or due date cannot be inferred confidently, set them to `null` and add a note.
- Do not fabricate tasks that are not present in the transcript.
- Evidence must quote the original line(s).

## Reference code
`extract_action_items.py`
