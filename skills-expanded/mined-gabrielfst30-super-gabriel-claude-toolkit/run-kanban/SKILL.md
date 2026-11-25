---
name: run-kanban
description: >
  Executes a TASK-PLAN.md created by /kanban-task-planner. Reads the plan, executes
  each card's checklist directly in the conversation (no subagents), respects dependency
  groups, and marks cards complete as they finish. Use when the user wants to run a
  kanban plan, execute TASK-PLAN.md, run cards, or runs /run-kanban.
user-invocable: true
argument-hint: [task-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /run-kanban

Executes a `TASK-PLAN.md` directly — no subagents, minimal overhead, maximum speed.
Reads each card's checklist and implements it step by step in the current conversation.

## Trigger

User runs `/run-kanban [task-name]`.

## Flow

### Step 1: Read the plan

Read `developer/tasks/$ARGUMENTS/TASK-PLAN.md` fully.
If not found, halt: "TASK-PLAN.md not found. Run /kanban-task-planner first."

Also read `CLAUDE.md` for project conventions.

Identify the execution groups from the **Execution Groups** section.

### Step 2: Execute Group 1

For each card in Group 1 (all parallel-safe, no dependencies):

1. Update the card's Status in the Cards Summary table: `[ ]` → `[-]`
2. Read the card's full content (Description, Scope, Acceptance Criteria, Checklist)
3. Execute each checklist item in order:
   - Write, Edit, or create files as needed
   - Run CLI commands listed in the checklist
   - Verify each item before moving to the next
4. After all checklist items are done, verify the Acceptance Criteria:
   - For each criterion, confirm it is satisfied
   - If a criterion fails, fix before continuing
5. Update status: `[-]` → `[x]` and note completion in the plan

Since Group 1 cards are independent, execute them in the most efficient order
(Schema and Types first as they are the most foundational).

### Step 3: Execute remaining groups

After each group completes, identify the next group (cards whose dependencies are all `[x]`).

Repeat Step 2 for each group, in order.

**Never start a card whose dependencies are not yet `[x]`.**

### Step 4: Final verification

After all cards are `[x]`:

Run the project's type-check if applicable (check `CLAUDE.md` or `package.json`):
```bash
pnpm type-check   # or
npm run type-check  # or
npx tsc --noEmit
```

If type-check fails, fix the errors before reporting complete.

### Step 5: Report

```
/run-kanban COMPLETE: developer/tasks/[name]/TASK-PLAN.md

Cards executed: N/N
  ✅ CARD-001: [title]
  ✅ CARD-002: [title]
  ...

Type check: PASSED (or N/A)
```

## Status Symbols

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Pending |
| `[-]` | In progress |
| `[x]` | Complete |
| `[!]` | Failed — needs attention |

## Rules

1. **Never skip a checklist item** — each item exists for a reason
2. **Read before writing** — always read existing files before editing them
3. **Verify criteria** — confirm each Acceptance Criterion is met before marking `[x]`
4. **Respect groups** — never start Group N+1 before Group N is fully `[x]`
5. **Fix type errors** — do not leave type-check failures unresolved

## Success Criteria
- [ ] All cards in TASK-PLAN.md marked `[x]`
- [ ] All Acceptance Criteria verified for every card
- [ ] Type-check passes with 0 errors (if applicable)
- [ ] No `[!]` cards remaining
