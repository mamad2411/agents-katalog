---
name: kanban-task-planner
description: >
  Creates a Kanban-style TASK-PLAN.md with CARD-XXX cards from a free-text task description.
  Each card has Description, Scope, Acceptance Criteria, Dependencies, and Checklist.
  Use when the user describes a feature or task and wants a structured Kanban plan,
  card decomposition, TASK-PLAN.md, structured cards, kanban planning, or runs
  /kanban-task-planner.
user-invocable: true
argument-hint: [description]
allowed-tools: Read, Write, Glob, Agent
---

# /kanban-task-planner

Creates a `TASK-PLAN.md` with structured Kanban cards from a free-text task description.
The user describes what needs to be done; the skill handles the full decomposition.

## Trigger

User runs `/kanban-task-planner [description]` where description is a free-text
explanation of what needs to be implemented.

Example:
```
/kanban-task-planner Implement CRUD routes for Funcionario entity with LDAP auth
```

## Flow

### Step 1: Gather context

Derive a short kebab-case name from `$ARGUMENTS` to use as the output directory.
Examples:
- "Implement CRUD for Funcionario with LDAP" → `crud-funcionario-ldap`
- "Create user authentication flow" → `user-auth-flow`

Read `CLAUDE.md` if it exists at the project root and capture its full content.
If not found, note "CLAUDE.md not found" and proceed — the agent will infer from the description.

### Step 2: Delegate to kanban-card-writer

Spawn one `kanban-card-writer` agent:

```
Agent(
  subagent_type: "kanban-card-writer",
  prompt: "Task description: $ARGUMENTS
           CLAUDE.md: [full content of CLAUDE.md, or 'not found']
           Output file: developer/tasks/[derived-name]/TASK-PLAN.md
           Task name: [derived-name]

           Decompose the description into Kanban cards.
           Group cards by type (Schema, Types, API, Hook, UI, Component, Integration, Config).
           Assign sequential IDs starting from CARD-001.
           Map dependencies between cards.
           Identify which cards can run in parallel within each group.
           Write the complete TASK-PLAN.md to the output file."
)
```

### Step 3: Validate output

Read `developer/tasks/[derived-name]/TASK-PLAN.md` after the agent completes.

Verify:
- At least one card exists
- Every card has all five sections (Description, Scope, Acceptance Criteria, Dependencies, Checklist)
- Execution groups section is present
- No circular dependencies

If validation fails, re-invoke the agent with the specific issue.

### Step 4: Report

```
TASK-PLAN created: developer/tasks/[derived-name]/TASK-PLAN.md

Cards: N total
  Group 1 (parallel): CARD-001, CARD-002
  Group 2 (after Group 1): CARD-003, CARD-004
  Group 3 (after Group 2): CARD-005

Run /run-kanban [derived-name] to execute.
```

## Success Criteria
- [ ] `developer/tasks/[derived-name]/TASK-PLAN.md` created
- [ ] Every card has all five required sections
- [ ] Execution groups are present and ordered by dependency
- [ ] No code in the plan — specs and checklists only
- [ ] `/run-kanban [derived-name]` can be run immediately after
