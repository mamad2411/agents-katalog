---
name: planner
description: Decomposes a task.md spec into atomic, executable tasks with IDs and dependency mapping. Reads developer/tasks/[name]/task.md and creates MAIN.md + todo/*.md files ready for /execute-todo.
user-invocable: true
argument-hint: [task-name]
allowed-tools: Read, Write, Glob
---

# /planner

Decomposes a `task.md` spec into atomic, executable tasks.

## Trigger

User runs `/planner [task-name]`.

## Flow

### Step 1: Read the spec
Read `developer/tasks/$ARGUMENTS/task.md` completely.
Also read `CLAUDE.md` to understand the project's module conventions
so task IDs and file paths are accurate.

### Step 2: Decompose into atomic tasks

Each task must be:
- **Atomic** — single focused implementation unit
- **Independent where possible** — minimal dependencies on other tasks
- **Unambiguous** — clear what to create or modify
- **Verifiable** — has explicit acceptance criteria

### Step 3: Assign task IDs

Use prefixes that match the project's layer conventions. Common prefixes:

| Prefix | Domain |
|--------|--------|
| `TODO-TYPE-N` | Types and interfaces |
| `TODO-SCHEMA-N` | Validation schemas |
| `TODO-API-N` | Endpoint definitions |
| `TODO-HOOK-N` | Data fetching hooks |
| `TODO-SCREEN-N` | Screen/page components |
| `TODO-UI-N` | UI sub-components |
| `TODO-ROUTE-N` | Routing configuration |
| `TODO-PAGE-N` | Page files |
| `TODO-DB-N` | Database schema/migrations |
| `TODO-FT-N` | Feature integration tasks |

Adapt prefixes to match the project structure defined in `CLAUDE.md`.

### Step 4: Create files

**`developer/tasks/$ARGUMENTS/MAIN.md`:**
```markdown
# [Task Name] — Execution Plan

## Status: PENDING

## Tasks

| ID | Description | Status | Depends On |
|----|-------------|--------|------------|
| TODO-TYPE-1 | Create entity types | [ ] | — |
| TODO-HOOK-1 | Create data hooks | [ ] | TODO-TYPE-1 |

## Execution Groups

### Group 1 (parallel)
- TODO-TYPE-1, TODO-SCHEMA-1

### Group 2 (after Group 1)
- TODO-HOOK-1
```

**`developer/tasks/$ARGUMENTS/todo/[ID].md`** (one per task):
```markdown
# [ID]: [Short Description]

## Status: [ ] PENDING

## Objective
[1-2 sentences describing exactly what this task implements]

## Files
### Create
- `path/to/new/file.ts`

### Modify
- `path/to/existing/file.ts` — reason for modification

## Implementation
[Precise spec — enough to implement without guessing]

## Acceptance Criteria
- [ ] [testable criterion]

## Dependencies
Depends on: [IDs] or None
```

### Step 5: Output

```
Plan created: developer/tasks/[name]/MAIN.md
Todo files: N tasks

Execution groups:
Group 1 (parallel): TODO-TYPE-1, TODO-SCHEMA-1
Group 2: TODO-HOOK-1, TODO-HOOK-2
Group 3: TODO-SCREEN-1

Run /execute-todo [name] to begin.
```

## Success Criteria
- [ ] `MAIN.md` created with dependency table and execution groups
- [ ] One `todo/[ID].md` per task
- [ ] No code in plan files — specs only
- [ ] Independent tasks correctly grouped for parallel execution
