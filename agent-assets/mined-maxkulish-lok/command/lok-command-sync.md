# /project:sync - Synchronize Project Aggregation Files

**Purpose**: Update PROJECT.md, ROADMAP.md, and DEPENDENCIES.md based on task state changes. Maintains consistency across all three aggregation files.

**Usage**:
- `/project:sync CLO-XX --start` - Task is starting (add to active work)
- `/project:sync CLO-XX --complete` - Task is done (move to completed)
- `/project:sync CLO-XX --complete "Summary text"` - Complete with custom summary
- `/project:sync CLO-XX --block CLO-YY` - Task is blocked by another task
- `/project:sync CLO-XX --unblock` - Task is no longer blocked

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| PROJECT.md | `docs/PROJECT.md` | Dashboard - current state of all work |
| ROADMAP.md | `docs/ROADMAP.md` | Big picture - phases and milestones |
| DEPENDENCIES.md | `docs/DEPENDENCIES.md` | Blockers - what's blocked and ready |

---

## Command Execution Instructions

### Step 1: Parse Arguments

1. **Extract task ID** from arguments (e.g., `CLO-9` or `clo-9`)
2. **Identify action flag**:
   - `--start`: Task is beginning work
   - `--complete`: Task is finished
   - `--block CLO-YY`: Task is blocked by CLO-YY
   - `--unblock`: Remove task from blocked state
3. **Extract optional summary** for `--complete` action

### Step 2: Fetch Task Details

If task title is needed:
```
Use mcp__linear-server__get_issue to fetch:
- Task title
- Task URL (https://linear.app/cloud-ai/issue/CLO-XX)
```

---

## Action: --start

### Validations

1. **Check WIP Limit** in PROJECT.md:
   - Read "## Active Work" section
   - Count non-placeholder rows (rows without `| - |`)
   - If count >= 3:
     ```
     WIP LIMIT REACHED

     Active Work currently has 3 tasks:
     - CLO-XX: [title]
     - CLO-YY: [title]
     - CLO-ZZ: [title]

     Options:
     1. Complete or pause one of these tasks first
     2. Override WIP limit (not recommended)

     Which task should be paused to make room?
     ```
   - Wait for user input before proceeding

2. **Check Task Readiness** in DEPENDENCIES.md:
   - Read "## Current Blockers" section
   - Search for task ID in "Blocked Task" column
   - If found:
     ```
     TASK IS BLOCKED

     CLO-XX is blocked by: CLO-YY ([status])

     Cannot start a blocked task. Options:
     1. Complete the blocker first
     2. Remove the blocking relationship if no longer valid

     How would you like to proceed?
     ```
   - Wait for user input before proceeding

### Updates

#### 1. Update PROJECT.md

**Add to "## Active Work" table**:

Find the table after `## Active Work (WIP Limit: 3)` and add a row:

```markdown
| [CLO-XX](https://linear.app/cloud-ai/issue/CLO-XX) | [Title] | In Progress | Phase N | - |
```

**Remove from "## Up Next" if present**:

Search the "## Up Next (Prioritized Backlog)" table for the task and remove that row.

#### 2. Update ROADMAP.md

**Find the task row** in the appropriate phase table and update status:

Change:
```markdown
| [CLO-XX](url) | Title | Backlog | ... |
```

To:
```markdown
| [CLO-XX](url) | Title | In Progress | ... |
```

#### 3. Update DEPENDENCIES.md

**Move from "Unblocked & Ready" to started** (if present):

Remove the task row from "## Unblocked & Ready" table (task is no longer waiting).

### Output

```
PROJECT SYNC: CLO-XX Started

Updates made:
- PROJECT.md: Added to Active Work
- ROADMAP.md: Status -> In Progress
- DEPENDENCIES.md: Removed from Unblocked & Ready

Current Active Work (2/3):
- CLO-XX: [Title] (just started)
- CLO-YY: [Title]
```

---

## Action: --complete

### Updates

#### 1. Update PROJECT.md

**Remove from "## Active Work"**:

Find and remove the row containing the task ID.

**Add to "## Recently Completed"**:

Add a new row at the TOP of the table (most recent first):

```markdown
| [CLO-XX](https://linear.app/cloud-ai/issue/CLO-XX) | [Title] | YYYY-MM-DD | [Summary or "Completed"] |
```

Use today's date in YYYY-MM-DD format.

#### 2. Update ROADMAP.md

**Find the task row** and update status to Done:

Change:
```markdown
| [CLO-XX](url) | Title | In Progress | ... |
```

To:
```markdown
| [CLO-XX](url) | Title | Done | ... |
```

**Update Summary table**:

Find the phase row in the Summary table and increment the "Completed" count.

Example:
```markdown
| Phase 1: Foundation | 4 | 3 | Complete |
```
becomes:
```markdown
| Phase 1: Foundation | 4 | 4 | Complete |
```

Also update the phase status if all tasks are now complete.

#### 3. Update DEPENDENCIES.md

**Remove from "## Current Blockers"** where this task was the blocker:

Search "Blocked By" column for CLO-XX and remove those rows.

**Add newly unblocked tasks to "## Unblocked & Ready"**:

For each task that was blocked by CLO-XX:
- Check if it has any OTHER blockers still pending
- If no other blockers, add to "## Unblocked & Ready":

```markdown
| CLO-YY | CLO-XX complete | YYYY-MM-DD |
```

### Output

```
PROJECT SYNC: CLO-XX Completed

Updates made:
- PROJECT.md: Moved to Recently Completed
- ROADMAP.md: Status -> Done, Phase 1 (4/4 complete)
- DEPENDENCIES.md: Unblocked 2 tasks

Newly unblocked tasks:
- CLO-YY: [Title] - Ready to start
- CLO-ZZ: [Title] - Ready to start

Current Active Work (1/3):
- CLO-AA: [Title]
```

---

## Action: --block CLO-YY

### Validations

1. **Verify blocker task exists** using Linear API
2. **Check if already blocked** to avoid duplicates

### Updates

#### 1. Update PROJECT.md

**Update "Blocked By" column** in Active Work:

If task is in Active Work, update the "Blocked By" column:

```markdown
| [CLO-XX](url) | Title | Blocked | Phase N | CLO-YY |
```

If task is not in Active Work, add to "## Blocked" section:

```markdown
| [CLO-XX](url) | Title | CLO-YY | [Notes] |
```

#### 2. Update DEPENDENCIES.md

**Add to "## Current Blockers"**:

```markdown
| CLO-XX | CLO-YY | [Blocker Status] | Waiting for CLO-YY completion |
```

**Remove from "## Unblocked & Ready"** if present.

### Output

```
PROJECT SYNC: CLO-XX Blocked

CLO-XX is now blocked by CLO-YY.

Updates made:
- PROJECT.md: Marked as blocked
- DEPENDENCIES.md: Added to Current Blockers
```

---

## Action: --unblock

### Updates

#### 1. Update DEPENDENCIES.md

**Remove from "## Current Blockers"**:

Find and remove the row where CLO-XX is in the "Blocked Task" column.

**Add to "## Unblocked & Ready"**:

```markdown
| CLO-XX | [Previous blocker] complete | YYYY-MM-DD |
```

#### 2. Update PROJECT.md

**Update in "## Blocked" section** if present:

Move task back to "## Up Next" or prompt user about next action.

### Output

```
PROJECT SYNC: CLO-XX Unblocked

CLO-XX is now unblocked and ready to start.

Updates made:
- DEPENDENCIES.md: Removed from Current Blockers, added to Unblocked & Ready
- PROJECT.md: Moved from Blocked to Up Next
```

---

## Table Formats Reference

### PROJECT.md - Active Work
```markdown
| Task | Title | Status | Phase | Blocked By |
|------|-------|--------|-------|------------|
| [CLO-XX](url) | Title Here | In Progress | Phase N | - |
```

### PROJECT.md - Recently Completed
```markdown
| Task | Title | Completed | Summary |
|------|-------|-----------|---------|
| [CLO-XX](url) | Title Here | YYYY-MM-DD | Brief summary |
```

### PROJECT.md - Up Next
```markdown
| Priority | Task | Title | Dependencies |
|----------|------|-------|--------------|
| 1 | [CLO-XX](url) | Title Here | CLO-YY |
```

### PROJECT.md - Blocked
```markdown
| Task | Title | Blocked By | Notes |
|------|-------|------------|-------|
| [CLO-XX](url) | Title Here | CLO-YY | Waiting for... |
```

### ROADMAP.md - Phase Tasks
```markdown
| Task | Title | Status | Dependencies |
|------|-------|--------|--------------|
| [CLO-XX](url) | Title Here | Done/In Progress/Backlog | CLO-YY |
```

### ROADMAP.md - Summary
```markdown
| Phase | Tasks | Completed | Status |
|-------|-------|-----------|--------|
| Phase N: Name | X | Y | Complete/In Progress/Not Started |
```

### DEPENDENCIES.md - Current Blockers
```markdown
| Blocked Task | Blocked By | Blocker Status | Notes |
|--------------|------------|----------------|-------|
| CLO-XX | CLO-YY | In Progress | Waiting for... |
```

### DEPENDENCIES.md - Unblocked & Ready
```markdown
| Task | Dependencies Satisfied | Ready Since |
|------|------------------------|-------------|
| CLO-XX | CLO-YY complete | YYYY-MM-DD |
```

---

## Error Handling

### Task Not Found in Linear
```
Error: Task CLO-XX not found in Linear

Please verify the task ID and try again.
```

### Task Already in Target State
```
No changes needed

CLO-XX is already marked as [In Progress/Complete/Blocked].
```

### File Update Failed
```
Error updating [filename]

The file may have been modified. Please check:
- docs/PROJECT.md
- docs/ROADMAP.md
- docs/DEPENDENCIES.md

And retry the sync operation.
```

---

## Update Timestamps

After any successful update, update the "Last Updated" line at the top of each modified file:

```markdown
**Last Updated**: YYYY-MM-DD
```

---

## Philosophy

This command is designed to:

1. **Maintain consistency**: All three files stay in sync
2. **Enforce constraints**: WIP limits and dependency checks
3. **Be idempotent**: Safe to run multiple times
4. **Provide visibility**: Clear output showing what changed

This command does NOT:

1. **Make workflow decisions**: Only updates based on explicit actions
2. **Modify Linear**: Only reads from Linear, updates are local files only
3. **Skip validations**: Always checks constraints before updating
