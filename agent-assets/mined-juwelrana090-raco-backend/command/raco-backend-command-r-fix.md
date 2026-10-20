> ⚠️ PROJECT SCOPED: All reads and updates stay in .claude/ only.

## Local Cache First

1. Read .claude/skills/_base.md ← includes top gotchas
2. Read .claude/skills/_modules-index.md ← find the affected module fast
   Only read full .claude/memory/gotchas.md or .claude/modules/ if cache is cold.

## Diagnose and fix

3. Read .claude/memory/gotchas.md if not covered by cache
4. Read .claude/modules/[relevant].md
5. Trace actual root cause — never guess
6. Explain what is broken and exactly why
7. Propose fix with clear reasoning
8. Apply the fix
9. Verify fix works
10. New gotcha? Add to .claude/memory/gotchas.md AND .claude/skills/_base.md
11. Update .claude/modules/[relevant].md gotchas section + changelog
12. Save log to .claude/tasks/logs/YYYY-MM-DD-fix-[title].md
