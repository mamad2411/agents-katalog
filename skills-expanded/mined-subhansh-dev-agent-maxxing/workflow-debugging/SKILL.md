---
name: workflow-debugging
description: Systematically debug a production issue using the debugging chain.
---

# Multi-Agent Workflow: Debugging a Production Issue

> Systematically debug a production issue using the debugging chain.

## Skills Used

| Skill | Role |
|-------|------|
| [Debugging Patterns](../engineering/debugging-patterns/SKILL.md) | Systematic methodology |
| [Execution Protocol](../engineering/execution-protocol/SKILL.md) | Problem-solving chain |
| [Runtime Verify](../engineering/runtime-verify/SKILL.md) | Run and observe |
| [Code Review Checklist](../engineering/code-review-checklist/SKILL.md) | Verify fix |

## Workflow

### Step 1: Reproduce

```
Load Execution Protocol skill.
Run the code. Hit the error. See it yourself.
Don't guess — observe.
```

### Step 2: Read the Error

```
Read the COMPLETE error message.
Extract: error type, file:line, stack trace, context.
Note: what was the user doing when it failed?
```

### Step 3: Bisect

```
Load Debugging Patterns skill.
Comment out half the code. Does it still happen?
Binary search through the codebase.
Log state at each step.
```

### Step 4: Trace the Flow

```
Follow the data from input to output.
Where does it go wrong?
Check: async timing, null values, state mutations.
Add console.log at each step.
```

### Step 5: Fix and Verify

```
Load Runtime Verify skill.
Apply the fix.
Run the app. Drive the changed path.
Push on it: try edge cases, wrong inputs.
Verdict: PASS / FAIL
```

### Step 6: Prevent Recurrence

```
Load Code Review Checklist.
Add a test case for the bug.
Check: does this pattern exist elsewhere?
Update documentation if needed.
```
