---
name: status
description: >
  Show the current pipeline state and what would dispatch next. Read-only —
  prints story queue table (with track), per-status counts, blocked callouts,
  and the exact next dispatch the orchestrator would make. Use when the user
  types /status or asks "what's the pipeline state", "where are we", "what's
  next".
---

Read `stories/_queue.json` and the effort routing table in `CLAUDE.md`. Print:

1. A table of every story with: slug, title, `track`, status, owner subagent, deps.
2. A count of stories per status.
3. Any `BLOCKED` stories called out at the top.
4. The exact next dispatch the orchestrator would make if the user ran `/next`, including the
   subagent name (track-routed), **effort tier** (`xhigh` or `high`), `identity_marker`, and
   the prompt string (with identity reinjection noted).
5. If every story is `DONE`, say so explicitly.

Do not dispatch anything. This command is read-only.
