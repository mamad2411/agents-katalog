---
name: execute-todo
description: Orchestrates parallel execution of all tasks in a plan. Reads developer/tasks/[name]/MAIN.md, launches task-executor agents respecting dependencies, verifies each task with task-verifier, and runs the project's type-check at the end.
user-invocable: true
argument-hint: [task-name]
allowed-tools: Read, Write, Edit, Agent, Bash(pnpm type-check:*), Bash(npm run type-check:*), Bash(npx tsc:*)
---

# /execute-todo

Orchestrates task execution from a plan created by `/planner`.

## Trigger

User runs `/execute-todo [task-name]`.

## Flow

### Step 1: Read the plan
Read `developer/tasks/$ARGUMENTS/MAIN.md` completely.

### Step 2: Identify ready tasks
A task is **ready** when:
- Status is `[ ]` (pending)
- All dependencies are `[x]` (complete)

### Step 3: Execute in parallel
For each group of independent ready tasks:
1. Launch `task-executor` agents simultaneously
2. Update MAIN.md: `[ ]` → `[-]` as tasks start

### Step 4: Verify each completed task
After `task-executor` reports COMPLETE:
1. Launch `task-verifier` for that task
2. `CONFIRMED` or `FIXED` → update `[-]` → `[x]`
3. `FAILED` → update `[-]` → `[!]`, re-run executor with failure context

### Step 5: Continue until all `[x]`
Repeat steps 2–4 until the plan is fully complete.

### Step 6: Final type-check
Run the project's type-check command (check `CLAUDE.md` or `package.json`):

```bash
pnpm type-check   # or
npm run type-check  # or
npx tsc --noEmit
```

## MAIN.md Status Symbols

| Symbol | Meaning |
|--------|---------|
| `[ ]` | Pending |
| `[-]` | In progress |
| `[x]` | Complete + verified |
| `[!]` | Failed — needs rework |

## Rules

1. **Respect dependencies** — never start before deps are `[x]`
2. **Maximize parallelism** — launch all ready tasks simultaneously
3. **Always verify** before marking `[x]`
4. **Stop on double failure** — if a task fails twice, halt and report
5. **Type-check at end** — always run after all tasks complete

## Output

```
[execute-todo] Plan: developer/tasks/[name]/MAIN.md
[execute-todo] Group 1: TODO-TYPE-1, TODO-SCHEMA-1 → launching in parallel...
[execute-todo] TODO-TYPE-1 COMPLETE → verifying...
[execute-todo] TODO-TYPE-1 ✅ CONFIRMED
...
[execute-todo] All tasks complete. Running type-check...
[execute-todo] ✅ Type check PASSED

COMPLETE: N/N tasks | Files created: N | Files modified: N
```

## Success Criteria
- [ ] All tasks in MAIN.md marked `[x]`
- [ ] Type-check passes with 0 errors
- [ ] No `[!]` tasks remaining
