---
name: superpowers-debugging
agent_created: true
version: 1.0.0
description: 4-phase systematic root-cause debugging. Investigate before fixing, form hypotheses, verify. This skill should be used when encountering any bug, test failure, or unexpected behavior.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully** — don't skip past errors; they often contain the exact solution
2. **Reproduce Consistently** — exact steps, every time; if not reproducible, gather more data
3. **Check Recent Changes** — git diff, recent commits, new dependencies, config changes
4. **Gather Evidence in Multi-Component Systems** — instrument each component boundary to find WHERE it breaks
5. **Trace Data Flow** — where does the bad value originate? Keep tracing up.

### Phase 2: Pattern Analysis

Find the pattern before fixing: locate similar working code, compare against references, identify every difference (however small), understand dependencies.

### Phase 3: Hypothesis and Testing

Scientific method: form a single specific hypothesis, test minimally (one variable at a time), verify before continuing. Don't know? Say "I don't understand X" — don't pretend.

### Phase 4: Implementation

Fix the root cause, not the symptom. Create a failing test case first. Implement a single fix — no "while I'm here" improvements. Verify the fix.

**If 3+ fixes have failed: STOP and question the architecture.** Each fix revealing new problems elsewhere is a pattern indicating architectural problems, not a series of independent bugs.

## Red Flags — STOP and Return to Phase 1

"Quick fix for now, investigate later." "Just try changing X and see if it works." "Multiple fixes at once saves time." "Skip the test, I'll manually verify." "It's probably X, let me fix that." "I don't fully understand but this might work." "One more fix attempt" (after 2+ failures).

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| 1. Root Cause | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |

## Real-World Impact

Systematic approach: 15-30 minutes to fix. Random fixes: 2-3 hours of thrashing. First-time fix rate: 95% vs 40%.
