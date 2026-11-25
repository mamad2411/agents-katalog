---
name: session-end
description: Close the session properly. Use when $user says end session, wrap up, closing, thanks, bye, we're done. Captures what mid-session writes missed, rewrites executive state and critique, then calls brain_session('end') which drains the queue, writes the HSAM close line, the sync file, and the clean-close marker.
---

## Session END

Say "Closing session." then run all four steps. Never ask permission; never skip step 3.

### 1. Final capture

Re-scan the conversation. Anything not yet stored (URLs, numbers, names, ideas, $user's questions, mood, corrections) → `brain_remember(kind='note', extra={section: '<HSAM section>'})`. Sections: What We Discussed · URLs & Links Shared · Decisions Made · Facts & Numbers · Ideas & Possibilities · Questions · Tools/Services/Products · Files & Resources · Mood & Context · Corrections & Feedback.

### 2. Draft the three bodies (full markdown)

- **executive_state** — `# Executive State — <date>`, then `## Primary Objective`, `## Top Missions` (advance / block / stall / complete each one touched), `## Pending Decisions ($user)` (table with classification), `## Open Loops`, `## Context Pack`, `## Critical Reminders`.
- **critique** — `# Session Critique — <date>`: What Went Well, What To Improve, User Feedback Observed, Apply Next Session.
- **sync** — under 15 lines: `## <name> — Session Sync (<date>)`, `**Key decisions:**`, `**Facts changed:**`, `**Status:**`.

### 3. Close

`brain_session('end', executive_state=<body>, critique=<body>, sync=<body>)`. It drains the capture queue, appends the close line to today's session file, writes the three files (the executive state and critique it replaces stay beside them as `.prev.md`), and writes the close marker. A `warning` in the reply means the executive state lacks the headings `brain_session('start')` reads: fix the body and call it again. Report its reply: writes this session, queue drained, files rewritten.

### 4. Done

Say "Session closed."
