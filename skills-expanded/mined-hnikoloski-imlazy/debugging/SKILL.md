---
name: debugging
description: Systematic root-cause investigation before any fix attempt. Four phases — Root Cause → Pattern Analysis → Hypothesis → Implementation. If 3+ fixes fail, question the architecture
---

# debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you have not completed Phase 1, you cannot propose fixes.

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read error messages carefully.** Don't skip past errors. Read stack traces completely. Note line numbers, file paths, error codes.

2. **Reproduce consistently.** Can you trigger it reliably? What are the exact steps? If not reproducible, gather more data before guessing.

3. **Check recent changes.** What changed that could cause this? git diff, recent commits, new dependencies, config changes.

4. **Gather evidence in multi-component systems** (CI → build → signing, API → service → DB):
   Before proposing fixes, add diagnostic instrumentation at each component boundary — log what data enters, log what data exits. Run once to see WHERE it breaks, then investigate that component. See `references/multi-component-debugging.md` for a worked example.

5. **Trace data flow.** Where does the bad value originate? What called this with the bad value? Keep tracing up until you find the source. Fix at source, not at symptom.

### Phase 2: Pattern Analysis

1. Find working examples — locate similar working code in the codebase.
2. Read the reference implementation completely if implementing a pattern — don't skim.
3. Identify differences — what's different between working and broken? List every difference.
4. Understand dependencies — what config, environment, or state does this need?

### Phase 3: Hypothesis and Testing

1. **Form one hypothesis:** "I think X is the root cause because Y." Write it down. Be specific.
2. **Test minimally:** make the smallest possible change to test the hypothesis. One variable at a time.
3. **Verify before continuing.** Worked? → Phase 4. Didn't work? → form new hypothesis. Don't add more fixes on top.
4. If you don't know, say "I don't understand X." Ask for help. Don't pretend.

### Phase 4: Implementation

1. **Create a failing test** that reproduces the bug. Use `Skill(imlazy-tdd)` for writing proper failing tests.
2. **Implement one fix** addressing the root cause identified. No "while I'm here" improvements.
3. **Verify the fix:** test passes, no other tests broken, issue resolved.
4. **If fix doesn't work:** STOP. Count attempts.
   - Under 3 attempts: return to Phase 1 with new information.
   - 3+ attempts: question the architecture (see below).

### If 3+ fixes failed: question the architecture

Pattern that indicates architectural problem: each fix reveals new shared-state coupling or problem in a different place; fixes require "massive refactoring"; each fix creates new symptoms.

STOP and discuss with the user before attempting more fixes. This is not a failed hypothesis — this is a wrong architecture.

## Red flags — stop and follow the process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)
- Each fix reveals new problem in different place

## Quick reference

| Phase | Key activities | Success criteria |
|-------|---------------|-----------------|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare, identify differences | Know what differs |
| 3. Hypothesis | Form one theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |

## Common rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes. Process is fast for simple bugs. |
| "Emergency, no time" | Systematic is FASTER than guess-and-check thrashing. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "One more fix attempt" (after 2+) | 3+ failures = architectural problem. Question the pattern. |
