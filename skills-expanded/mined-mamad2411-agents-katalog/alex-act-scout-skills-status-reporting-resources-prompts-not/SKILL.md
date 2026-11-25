---
description: "Write a quick pending-action note to repo-root HANDOFF.md"
lastReviewed: 2026-07-30
---

# Note

Use this as a short handoff-note workflow. Capture a concise note in repo-root
`HANDOFF.md` so pending actions remain visible at the project root.

This prompt complements the [Status Reporting skill](../../SKILL.md). If the
skill cannot be used directly, follow the steps below.

See [`save-session-note.prompt.md`](save-session-note.prompt.md) for the full steps.

## Quick Form

If the user's request already includes the note text, skip the "what should I capture?" question and write it directly. Resolve repo root, append checkbox item to `HANDOFF.md`, confirm.

**Would revise if**: the [save-session-note](save-session-note.prompt.md) prompt changes its capture protocol, or `HANDOFF.md` is no longer the canonical pending-action surface. Re-evaluate 2026-10-30.
