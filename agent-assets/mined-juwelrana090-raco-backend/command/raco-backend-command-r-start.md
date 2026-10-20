> ⚠️ PROJECT SCOPED: Read only from this project's .claude/ directory.

## Local Cache First — load in this order before anything else

1. .claude/skills/_base.md
2. .claude/skills/_stack.md
3. .claude/skills/_modules-index.md
   If any of the above are marked 🔴 Cold, note it and continue — do not stop.

## Then load full memory

4. CLAUDE.md (already loaded by Claude Code)
5. .claude/memory/context.md
6. .claude/memory/architecture.md
7. .claude/memory/rules.md
8. .claude/memory/patterns.md
9. .claude/memory/gotchas.md
10. .claude/memory/dependencies.md
11. Last 3 files in .claude/tasks/logs/
12. Last file in .claude/tasks/eod/ if exists
13. Scan all .claude/modules/ — flag any 🔴 Stale
14. Read .claude/tasks/todo/ — count and sort by priority
15. Read .claude/tasks/inprogress/ — list what is in progress

Report:

- ✅ Memory loaded — what you know about this project
- ⚠️ Cache status — if skills/ files are cold, show: "Run /r-cache-warm to speed up future sessions"
- ⚠️ Stale modules — list with suggested action
- 🔴 Risk flags — anything broken or outdated
- 📋 Todo: [count] tasks — top 3 by priority
- 🔄 In Progress: [what is being worked on]
- 💡 Suggested focus — highest priority todo task
- 🛠️ Dev commands quick ref

At the very end of the report show a token usage meter:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 TOKEN USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Used: [████░░░░░░░░░░░░░░░░] ~XX% (~XXk / 200k)
Remaining: [████████████████░░░░] ~XX% (~XXk tokens)
Status: 🟢 Safe / 🟡 Medium / 🔴 Critical
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 Safe 0–60% → keep working
🟡 Medium 60–80% → wrap up current task, run /r-end soon
🔴 Critical 80%+ → run /r-end NOW before context cuts off
Tip: run /r-tokens anytime to check remaining context.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are now senior dev partner for this session.
Never ask to re-explain anything already in memory.
