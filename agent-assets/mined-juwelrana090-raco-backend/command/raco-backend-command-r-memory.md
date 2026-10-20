> ⚠️ PROJECT SCOPED: Read and write .claude/ only. SAFE MODE always active.
> SAFE MODE: NEVER delete or overwrite existing content. Only append or add missing.

Handles all memory maintenance. Behaviour depends on argument.

## /r-memory scan — full project rescan (use after big changes)

1. Read every file in the project
2. For each file in .claude/memory/: read first, ADD missing sections, APPEND new findings
3. For each .claude/modules/ file: read first, append new findings only; create fresh if missing
4. Update CLAUDE.md missing sections only — never overwrite
5. Bump .claude/memory/VERSION minor version
   Report: ✅ updated / ✅ created / ⏭️ skipped / ⚠️ nothing deleted / ⚠️ nothing overwritten

## /r-memory update — incremental sync (use after a task)

1. Read changed files in the project since last task log
2. Compare against .claude/memory/ and .claude/modules/
3. ADD missing info only, APPEND new findings, flag outdated fields:
   <!-- previous: old value here -->
4. Set confidence: 🟢 High / 🟡 Medium / 🔴 Stale
5. Bump VERSION minor version
   Report all changes made with file paths.

## /r-memory status — health check (read-only)

Read all .claude/modules/ files and .claude/memory/VERSION.
Report:

| Module                                                                                | Confidence | Last Updated | Notes |
| ------------------------------------------------------------------------------------- | ---------- | ------------ | ----- |
| Then: list all 🔴 Stale with fix action, 🟡 Medium with reason, overall health score. |
| Suggest: run /r-memory scan if 3+ modules are 🔴 Stale.                               |

## /r-memory (no argument) — defaults to status
