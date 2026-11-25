---
name: enhance
description: Transforms a raw development request into a structured task.md spec. Reads developer/requests/[name].md or an inline description, consults the architecture-guardian, and creates developer/tasks/[name]/task.md with full scope definition.
user-invocable: true
argument-hint: [request-name or inline description]
allowed-tools: Read, Write, Glob, Grep, Agent
---

# /enhance

Transforms a raw development request into a structured `task.md` spec.

## Trigger

User runs `/enhance [request-name]` or provides an inline request description.

## Flow

### Step 1: Read the request
If `developer/requests/$ARGUMENTS.md` exists, read it.
Otherwise, use `$ARGUMENTS` as the inline request.

### Step 2: Consult architecture
Use the `architecture-guardian` agent to understand:
- Which modules or files are affected
- What existing patterns apply
- What files will need to be created or modified

Read `CLAUDE.md` and relevant `docs/` files for the domain.

### Step 3: Create `developer/tasks/$ARGUMENTS/task.md`

```markdown
# Task: [Descriptive Title]

## Request
[Original request verbatim]

## Context
[Why this is needed, what problem it solves]

## Scope

### Module(s) Affected
- `[path/to/module/]` — [what changes here]

### Pages / Routes Affected
- `[path/to/page]`

## Requirements

### Functional Requirements
1. [What the feature must do]

### Technical Requirements
1. [Specific patterns to follow from CLAUDE.md]

### Acceptance Criteria
- [ ] [Testable criterion]

## Files to Create
- [path/to/new/file.ts]

## Files to Modify
- [path/to/existing/file.ts] — reason

## Files to Delete
- [if any]

## Out of Scope
- [explicit exclusions to prevent scope creep]

## Dependencies
- [other tasks this depends on, if any]

## Risks
- [unknowns or potential issues]
```

### Step 4: Output

```
Task created: developer/tasks/[name]/task.md

Scope:
- [bullet]
- [bullet]

Files to create: N | Files to modify: N

Run /planner [name] to decompose into executable tasks.
```

## Success Criteria
- [ ] `developer/tasks/[name]/task.md` created
- [ ] All affected files listed
- [ ] Acceptance criteria are testable (not vague)
- [ ] Out of scope is explicitly defined
