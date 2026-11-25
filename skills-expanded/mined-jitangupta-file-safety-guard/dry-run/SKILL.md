---
name: dry-run
description: >
  Plan-first execution for multi-step file operations. Use when a task involves more than
  2 file operations or when the user explicitly asks for a dry run. Creates a plan.md file
  listing all planned changes, waits for user approval before executing, and updates the
  plan with actual results after completion.
---

# Dry Run — Plan First, Act Later

No surprises — you see the plan before anything happens.

## Rules

### 1. When to Create a Plan

- For any task that involves **more than 2 file operations**, create a `plan.md` file in the working directory BEFORE executing anything.
- A "file operation" includes: creating, modifying, moving, renaming, or deleting a file.

### 2. What the Plan Must Include

The `plan.md` file must contain these sections:

```markdown
# Operation Plan

**Task:** [Brief description of what was requested]
**Date:** [YYYY-MM-DD HH:MM]

## Files to be Created
- filename.ext — purpose/description

## Files to be Modified
- filename.ext — what will change

## Files to be Moved or Renamed
- old/path/filename.ext → new/path/filename.ext

## Files to be Deleted
- NONE (unless explicitly requested by the user)

## Summary
[1-2 sentence overview of what will change]

---

## Execution Log
_To be filled after execution_
```

### 3. Deletion Default

- The "Files to be Deleted" section should always say **NONE** unless the user has specifically and explicitly asked for file deletion.
- If the user did request deletions, list each file with its full path.

### 4. Wait for Approval

- After creating and showing the plan, **stop and wait**.
- Only proceed when the user says one of: "go ahead", "proceed", "approved", "yes", "do it", or similar explicit confirmation.
- If the user requests changes to the plan, update `plan.md` and show it again before proceeding.

### 5. Post-Execution Update

After all operations are complete, update `plan.md` with an **Execution Log** section:

```markdown
## Execution Log
**Executed at:** 2026-02-09 14:45
**Status:** Complete

- ✅ Created: report.docx
- ✅ Modified: index.html (updated header section)
- ⚠️ Skipped: styles.css (no changes needed after review)
- ✅ Backup created: _backups/index_backup_20260209_1445.html
```

## Activation

This skill activates when:
- A task involves more than 2 file operations
- The user explicitly asks for a dry run or plan
- A complex multi-file operation is requested
