---
name: handoff
description: Prepare the repo for another agent or session (Codex, a fresh Claude Code session, a human) to continue the work — check STATUS/PLAN/git consistency, write the resume note, list open questions. Use when the user says "handoff", "I'll continue with Codex", "ادامه‌ش رو با کدکس می‌دم", "آماده‌ی تحویل کن".
---

# handoff

## Steps

1. Run `/status` first so `docs/STATUS.md` is current.
2. Consistency checks: every PLAN checkbox ticked has evidence (test, file, screenshot note); every item in STATUS "Next up" maps to a PLAN line; `git status` is clean or the dirty files are named in STATUS; `pnpm test` passes (or failures are listed under Blocked).
3. Write the resume note into STATUS "How to resume": commands, read order, the one file to open first for the next task, and any environment prerequisites (e.g. `claude` login).
4. Verify `AGENTS.md` still describes reality (repo map, commands) and is ≤150 lines.
5. Reply with a 5-line handoff summary in the user's language.
