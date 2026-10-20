> ⚠️ PROJECT SCOPED: All outputs save to .claude/ only.

## Local Cache First

1. Read .claude/skills/_base.md ← rules + patterns (fast)
2. Read .claude/skills/_stack.md ← stack guidance (fast)
3. Read .claude/skills/_modules-index.md ← module map (fast)
   Only read .claude/modules/[specific].md if this task touches that module.
   Only read .claude/memory/ files if skills/ cache is cold (🔴).

## Execute

4. Read .claude/memory/pre-task-checklist.md — complete every item
5. Read .claude/modules/[relevant].md if needed
6. State complete plan before writing any code
7. Wait for approval if change touches more than 3 files
8. Execute the task
9. Read .claude/memory/post-task-checklist.md — complete every item
10. Update all affected .claude/modules/ files
11. Update .claude/skills/_modules-index.md if modules changed
12. Save log to .claude/tasks/logs/YYYY-MM-DD-[title].md

Log format:

# Task: [title]

**Date**: **Summary**: **Files Changed**: **Modules Affected**:
**Decisions Made**: **Memory Updated**: **Cache Updated**: **Notes**:

Confirm log saved with full path.
