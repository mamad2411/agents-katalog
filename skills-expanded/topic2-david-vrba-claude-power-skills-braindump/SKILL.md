---
name: braindump
description: Turn a messy voice ramble into clean, structured output — fixes transcription slips and organizes stream-of-consciousness into a spec, task list, outline, or decision.
argument-hint: <your ramble> (or leave empty to use your last message)
allowed-tools: Read, Write
---

The user thinks out loud through voice-to-text, so the input is a raw, possibly garbled ramble. Turn it into clean, organized output. The content is in `$ARGUMENTS`, or the user's most recent message if empty.

## Step 1 — Clean the transcription
Silently fix likely voice-to-text errors: homophones, mangled technical terms, dropped or duplicated words, run-on sentences. If a fix would change the *meaning* and you're not sure, keep the user's wording and flag it — never silently invent intent.

## Step 2 — Detect the shape
Work out what they're actually producing and pick the structure that fits:
- **Spec / plan** → goal, requirements, approach, open questions.
- **Task list** → grouped, ordered, actionable checkboxes.
- **Notes / outline** → headings + bullets by theme.
- **Decision** → options with honest trade-offs + a recommendation.
If genuinely ambiguous, pick the most useful one and say which you chose — don't block on it.

## Step 3 — Output
- Lead with a one-line summary of what they were getting at.
- Then the structured version — tight, deduplicated, logically ordered.
- End with **Open questions / gaps** if the ramble left anything undecided or contradictory.

## Principles
- Organize and clarify; **do not pad or add ideas they didn't express.**
- Preserve every distinct point — structuring must never drop content.
- Surface contradictions you find rather than smoothing them over.
- Offer to save it to a file if it's substantial (a spec/plan worth keeping).
