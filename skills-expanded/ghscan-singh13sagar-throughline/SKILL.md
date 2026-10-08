---
description: Update .claude/STATE.md — the working memory that survives compaction and restarts. Use when the goal/next-step/open-questions change, before a long task, or when context is getting full.
allowed-tools: Read, Edit, Write, Bash(git status:*), Bash(git log:*)
---
# /save-state — write down where we are

Update `.claude/STATE.md` (create it if missing) so the thread survives `/compact` and a fresh session. Keep it SHORT — it loads every session and after every compaction.

Current context:
!`git -C "$PWD" log --oneline -5 2>/dev/null; echo '---'; git -C "$PWD" status --short 2>/dev/null`

Rewrite STATE.md with these sections, a few bullets each:
- **Now** — the one thing we're doing right now.
- **Done** — finished this session (trim stale items).
- **Next** — the next concrete step(s).
- **Open questions / decisions** — anything unresolved, and any decision made + why.
- **Gotchas** — non-obvious durable facts discovered.

Keep the whole file under ~40 lines. Then confirm in one line what you saved.
