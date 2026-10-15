---
name: meeting-action-items-extractor
description: Vendor-neutral skill to extract decisions, action items, and owners from meeting transcripts and output an actionable task list.
---

## When to invoke
- When turning raw meeting transcripts into assigned tasks.
- When capturing decisions and follow-ups for project execution.

## Inputs needed
- `--input`: Path to a plain-text transcript.
- Optional `--out`: Path to write JSON output.

## Workflow
1. Split transcript into lines.
2. Detect action items using heuristics (e.g., "TODO", "Action:", "I'll", "We should", "Can you").
3. Attempt owner extraction from speaker prefix patterns like `Name:`.
4. Detect decisions using patterns ("Decision:", "We decided").
5. Output a normalized task list.

## Output format
JSON with:
- `decisions`: list of strings.
- `action_items`: list of `{owner, task, evidence_line}`.

## Guardrails
- Heuristic extraction; do not invent owners or tasks.
- If owner cannot be reliably inferred, set owner to `null`.

## Reference code
- `meeting_action_items_extractor.py`
