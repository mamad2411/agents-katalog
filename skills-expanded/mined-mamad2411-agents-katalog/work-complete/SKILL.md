---
name: work-complete
description: 'Work completion handler. Archives the plan file. Example: /work-complete'
---

# Work Completion Handler

Performs cleanup at the end of a work session.

## Usage

```text
/work-complete
```

## Procedure

### 1. Archive the plan file

Move **only the plan file used in the current session** to `.claude/plans/archive/`.

- The file specified when plan mode started (e.g. `.claude/plans/lazy-riding-willow.md`)
- Do not move plan files belonging to other sessions (parallel runs may exist)
- Skip if the plan file does not exist
- The archived file remains available for reference if follow-up work is needed

```bash
# Create the archive directory if it doesn't exist
mkdir -p .claude/plans/archive

# Move the current session's plan file into the archive
mv .claude/plans/<current-session-plan-file>.md .claude/plans/archive/
```

### 2. Report completion

Report the result of the cleanup.
