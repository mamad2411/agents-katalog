---
name: executing-plans
description: Systematic task-by-task execution with TDD flow, verification checkpoints after each task, and architecture compliance checks. Updates tech debt tracker if shortcuts are taken.
invoke_when: Use when executing an approved implementation plan, starting task-by-task coding from a written plan.
---

# Executing Plans

## Execution Flow

For each task in the plan:

### 1. Announce
Tell the user which task you're starting and what files you'll touch. Mark the corresponding Task as `in_progress` using `TaskUpdate`.

### 2. Write the Test First
- Write the failing test as specified in the plan
- Run it — confirm it FAILS
- If it passes without implementation, the test is wrong — fix it

### 3. Write the Implementation
- Write the minimal code to make the test pass
- Follow architecture.md constraints
- No extra code beyond what the test requires

### 4. Verify
- Run the test — confirm it PASSES
- Run the full test suite — confirm nothing is broken
- Run the build — confirm no type errors

### 5. Refactor (if needed)
- Clean up without changing behavior
- Re-run tests after refactoring

### 6. Mark Complete
- Mark the corresponding Task as `completed` using `TaskUpdate`
- Announce task completion with evidence (test output, build output)
- Move to the next task

## Critical Rules

### Never Skip Verification
After implementing a task, you MUST run the verification command. Do not say "this should work" — prove it works.

### Architecture Compliance Check
Before each task, re-read the relevant Mandatory Rules from architecture.md. If the task would violate a rule, STOP and discuss with the user rather than proceeding.

### Handling Failures
- If a test fails unexpectedly: invoke `systematic-debugging` — do NOT guess-fix
- If 3+ attempts fail: stop and reassess — likely an architectural issue
- If you need to take a shortcut: invoke `tech-debt-tracking` to document it

### Handling Plan Deviations
- If you discover the plan needs changes mid-execution:
  1. Stop executing
  2. Explain what changed and why
  3. Propose plan updates
  4. Get approval before resuming

### Commit Cadence
- Commit after each task (or group of tightly related tasks)
- Commit message should reference the plan task number
- Never batch all tasks into one giant commit

---

## Rationalization Pressure Test

These are excuses you might generate to deviate from the plan without approval. Each one is wrong.

| Rationalization | Why It's Wrong | What To Do Instead |
|----------------|---------------|-------------------|
| "I found a better approach mid-implementation" | The plan was approved. Changing it unilaterally breaks the contract with your human partner | Stop. Explain the better approach. Get approval. Then change the plan |
| "This small deviation doesn't need approval" | Small deviations compound. Three "small" changes can shift the entire architecture | If it changes what files are touched, what APIs look like, or what the user will see — get approval |
| "Asking for approval will slow us down" | Building the wrong thing is infinitely slower than a 30-second approval conversation | Ask. "I found X, suggest we change Y. OK?" takes seconds |
| "The tests pass, so the deviation is fine" | Tests verify behavior, not intent. Code can pass tests and still be the wrong code | Passing tests are necessary but not sufficient. Alignment with the plan matters |
| "I'll tell the user about the change after" | After means the user lost their chance to say no. That's not partnership, that's unilateral action | Tell them before. Always before |
| "The plan didn't account for this edge case" | Correct — that's exactly why you stop and discuss it | Plans are living documents. Update the plan, get approval, continue |
| "I'm just refactoring, not changing behavior" | Refactors change file structure, naming, and patterns — all of which affect the plan | If it changes the File Map, it changes the plan. Get approval |
| "Skipping verification this once is fine" | Verification is not optional. "It should work" is not evidence that it works | Run the command. Read the output. Report the result. Every time |
