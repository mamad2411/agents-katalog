---
name: debugging
version: 1.0.0
description: Systematic root cause analysis for code failures
uses:
  - analysis/deep-analysis
requires:
  tools: []
  env: []
security:
  risk_level: write
  capabilities:
    - file:read
    - command:execute
  requires_approval: false
---

# Debugging

Systematic root cause analysis for code failures. This skill provides a structured approach to diagnosing bugs — from reproducing the problem to identifying the root cause to verifying the fix.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `debug` is invoked, you (the agent) apply the methodology below using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it.

## When to Use

- A test is failing and the cause isn't obvious
- An error is occurring in production or staging
- Code behaves differently than expected
- A previously working feature is broken
- Performance degradation needs diagnosis
- Flaky behavior needs systematic investigation

## Methodology

### 1. Reproduce

Before diagnosing, confirm you can reproduce the problem:
- **Get the exact error**: Error message, stack trace, log output
- **Get the exact steps**: What triggers the failure?
- **Get the environment**: OS, language version, dependencies, configuration
- **Confirm it's reproducible**: Does it fail consistently or intermittently?

If it can't be reproduced, gather more evidence before proceeding.

### 2. Isolate

Narrow down where the problem is:

| Technique | How | When |
|-----------|-----|------|
| **Binary search** | Bisect the code path to find where behavior diverges | Large codebase, unclear location |
| **Input reduction** | Find the minimal input that triggers the bug | Complex inputs |
| **Dependency elimination** | Remove/mock dependencies to isolate the component | Could be in dependencies |
| **Version bisect** | `git bisect` to find the commit that introduced the bug | Regression |
| **Log injection** | Add logging at key points to trace execution flow | Need to see runtime behavior |

### 3. Diagnose

Once isolated, identify the root cause:

**Common root causes:**

| Category | Examples |
|----------|---------|
| **Logic error** | Off-by-one, wrong operator, missing condition |
| **State error** | Uninitialized variable, stale cache, race condition |
| **Type error** | Wrong type passed, null where non-null expected |
| **Boundary error** | Empty collection, max int, unicode, special chars |
| **Concurrency error** | Race condition, deadlock, data corruption |
| **Environment error** | Missing config, wrong version, path issues |
| **Integration error** | API contract changed, schema mismatch |

**Diagnosis process:**
1. Read the error message carefully — it usually points to the proximate cause
2. Read the stack trace — trace from the crash point back to the root
3. Read the code at the crash point — understand what it's trying to do
4. Check the inputs — are they what the code expects?
5. Check the state — is the system in the state the code assumes?
6. Form a hypothesis — "The bug is because X"
7. Verify the hypothesis — add a test or log that confirms

### 4. Fix

Apply the minimal fix:
- Fix the root cause, not the symptom
- Don't change unrelated code
- Preserve existing behavior for non-buggy cases

### 5. Verify

Confirm the fix works:
1. **Reproduce check**: Does the original failure no longer occur?
2. **Regression check**: Do existing tests still pass?
3. **Edge case check**: Does the fix handle related edge cases?
4. **Write a regression test**: Ensure this specific bug can't recur

### 6. Document

Record what was found:
- What was the symptom?
- What was the root cause?
- What was the fix?
- Why did it happen (prevention lesson)?

## Output Format

```
## Debug: [Symptom]

### Reproduction
- Error: [error message/behavior]
- Steps: [how to reproduce]
- Consistent: [yes/no/intermittent]

### Isolation
- Location: [file:line]
- Component: [module/function]
- Technique used: [binary search/input reduction/etc.]

### Root Cause
- Category: [logic/state/type/boundary/concurrency/environment/integration]
- Cause: [specific explanation]
- Evidence: [how we confirmed this is the cause]

### Fix
- Change: [what was changed]
- Scope: [minimal — only the root cause]

### Verification
- Original failure: [resolved]
- Existing tests: [pass]
- Regression test: [written — test name]

### Prevention
- Lesson: [what to do differently to prevent this class of bug]
```

## Quality Criteria

- Problem is reproducible before diagnosis begins
- Root cause is identified (not just the symptom)
- Fix addresses the root cause, not a symptom
- Fix is minimal (doesn't change unrelated code)
- Existing tests still pass after the fix
- A regression test is written for the specific bug
- Diagnosis process is documented for future reference

## Common Mistakes

- **Fixing symptoms instead of root causes**: Adding a null check at the crash point instead of fixing why null got there. The real bug is elsewhere.
- **Not reproducing first**: Guessing at the cause without confirming the failure. You might fix the wrong thing.
- **Changing too much**: While debugging, "cleaning up" surrounding code. This makes it impossible to verify the fix in isolation.
- **Not writing a regression test**: Fixing the bug but not adding a test. The same bug will come back later.
- **Stopping at the first theory**: The first hypothesis might be wrong. Verify before committing to a fix.
- **Debugging by print statement only**: Print debugging works but is slow. Use structured techniques (binary search, git bisect) to narrow down faster.
- **Ignoring intermittent failures**: Flaky failures indicate real problems (race conditions, time dependencies). They require more investigation, not less.

## Completion

Debugging is complete when:
- The problem is reproducible and understood
- The root cause is identified with evidence
- A minimal fix is applied
- Existing tests pass
- A regression test prevents recurrence
- The diagnosis is documented
