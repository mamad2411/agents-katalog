---
name: task
description: Create a new task in MASTER_PLAN.md with auto-generated sequential IDs. Supports TASK, BUG, FEATURE, and INQUIRY types. Triggers on "/task", "add task", "new task", "create task", "track this".
---

# Task Creator

Quickly add new tasks to MASTER_PLAN.md with automatic sequential ID generation.

## Triggers

- `/master-plan:task` - Main command
- "add task", "new task", "create task", "track this", "log a bug"

## Workflow

### Step 1: Find MASTER_PLAN.md

Search for the plan file in order:
1. `docs/MASTER_PLAN.md`
2. `MASTER_PLAN.md`
3. `master-plan.md`
4. `docs/master-plan.md`

**If not found**: Create `docs/MASTER_PLAN.md` using the template structure (see "Initial Setup" section below).

### Step 2: Generate Next Task ID

Read the MASTER_PLAN.md file and find all existing task IDs:

1. Scan for all occurrences matching `(TASK|BUG|FEATURE|ROAD|IDEA|ISSUE|INQUIRY)-(\d+)`
2. Extract the numeric part from each match
3. Find the highest number
4. Next ID = highest + 1

**CRITICAL**: IDs are sequential across ALL types. If TASK-42 and BUG-43 exist, the next ID is 44 regardless of type.

**Immediately output to user:**
```
Using task number: [ID]
```

This must happen BEFORE asking any questions.

### Step 3: Gather Task Information

Use `AskUserQuestion` to collect:

1. **Task Type** (header: "Type")
   - `TASK` — New feature or improvement
   - `BUG` — Bug fix
   - `FEATURE` — Major new feature
   - `INQUIRY` — Investigation (not a fix, just understanding something)

2. **Priority** (header: "Priority")
   - `P0` — Critical / Blocker
   - `P1` — High priority
   - `P2` — Medium priority (Recommended)
   - `P3` — Low priority / Backlog

Then ask in plain text: "What's the task title? (Keep it concise, under 50 chars)"

Optionally ask: "Any additional description? (Or just press enter to skip)"

### Step 4: Add to MASTER_PLAN.md

#### 4a. Add to Roadmap Table (if one exists)

Look for a markdown table with task IDs. Insert a new row:

```markdown
| **[TYPE]-[ID]** | **[Title]** | **[Priority]** | PLANNED | - |
```

#### 4b. Add Detailed Section

Add a new `###` section at the appropriate place (typically at the end of the active work area, before completed tasks):

```markdown
### [TYPE]-[ID]: [Title] (PLANNED)
**Priority**: [Priority]
**Status**: PLANNED (YYYY-MM-DD)

[Description if provided]

**Tasks**:
- [ ] [First step — infer from context or ask user]
```

For P0/P1 tasks, add a note that this is high priority.

### Step 5: Confirm

Output to user:
```
Task added to MASTER_PLAN.md:
- **ID**: [TYPE]-[ID]
- **Title**: [Title]
- **Priority**: [Priority]
- **Status**: PLANNED

Use `/master-plan:next` to start working on it, or `/master-plan:done [ID]` when complete.
```

## Initial Setup

If no MASTER_PLAN.md exists, create `docs/MASTER_PLAN.md` with this structure:

```markdown
# MASTER PLAN

> Project task tracking and roadmap.

## Roadmap

| ID | Title | Priority | Status | Dependencies |
|----|-------|----------|--------|--------------|

## Active Work

<!-- New task sections are added here -->

## Completed

<!-- Done tasks are moved here -->
```

Also create the `docs/` directory if it doesn't exist.

## ID Format Reference

| Prefix | Usage |
|--------|-------|
| `TASK-XXX` | Features and improvements |
| `BUG-XXX` | Bug fixes |
| `FEATURE-XXX` | Major features |
| `ROAD-XXX` | Roadmap items |
| `IDEA-XXX` | Ideas for later |
| `ISSUE-XXX` | Known issues |
| `INQUIRY-XXX` | Investigations |

## Important Rules

1. **NEVER reuse existing task IDs** — Always scan the file first
2. **IDs are global** — Sequential across all types (TASK, BUG, etc.)
3. **Use strikethrough** (`~~ID~~`) only when marking tasks DONE
4. **Keep titles concise** — Under 50 characters
5. **P0 tasks** should always get an immediate detailed section
