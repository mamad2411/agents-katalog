---
name: lifekernel-project-memory
description: Record durable project progress, decisions, verification, and open questions after an agent work session.
---

# Project memory

Use at the end of meaningful project work, or when the user asks to record what was done.

1. Read the project's context note and search for an existing session with the same external session or request ID, so you update instead of duplicating.
2. Record only work actually completed, sources consulted, verification that really ran (with results; never claim tests you did not run), decisions the user accepted, proposals still awaiting a decision, open questions, and one next action.
3. Keep code in the repository. Store a concise durable account in the vault on route `session`, linked from the canonical project note. Tasks stay in the project note as checklist items, not in the session; tick finished ones there and set the project's `next_action` with `set_frontmatter`.
4. Follow the write protocol in the daily-circle skill. Use the external session or request ID as part of `requestId` so a retry is idempotent.
5. When the work changes the user's plans, send a short outcome to the personal vault on route `outcome`: what changed and what it means for them, in at most 600 characters, with a link to the detailed record (for example `startup:sessions/2026-10-01-pricing.md`). The route refuses anything longer or unlinked. Detailed history stays in the project vault.
