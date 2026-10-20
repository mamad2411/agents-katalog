---
description: Read and update docs/TRACE.md so every session stays on track
alwaysApply: true
---

# Session trace (always on)

Before planning or coding, **read** `docs/TRACE.md` (Current status + Backlog + latest trace entries).

After you complete work for a user request (or a clear chunk of it):

1. **Prepend** a new entry under `## Trace log (newest first)`:
   - `### YYYY-MM-DD — short title`
   - `**User asked:**` one line
   - `**Did:**` what landed (files/features)
   - `**Needs next:**` leftover or next phase item
2. Update **Current status** and **Backlog** if phase or priorities changed.
3. Set **Last updated** to today.

Do not delete old trace entries. Keep the file the source of truth across chats.
