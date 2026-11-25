---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior - requires finding root cause before attempting any fixes
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Always find root cause before fixing.

**Core principle:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

**Violating the letter of this process is violating the spirit of debugging.**

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes

4. **Gather Evidence in Multi-Component Systems**

   For EACH component boundary:
   - Log what data enters component
   - Log what data exits component
   - Verify environment/config propagation

### Phase 2: Pattern Analysis

1. **Find Working Examples**
   - Locate similar working code
   - What works that's similar to what's broken?

2. **Compare Against References**
   - Read reference implementation COMPLETELY
   - Don't skim - understand fully

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"

2. **Test Minimally**
   - Make SMALLEST possible change
   - One variable at a time

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? NEW hypothesis

### Phase 4: Implementation

1. **Create Failing Test Case**
   - Simplest possible reproduction
   - MUST have before fixing

2. **Implement Single Fix**
   - Address root cause
   - ONE change at a time

3. **Verify Fix**
   - Test passes now?
   - No other tests broken?

4. **If 3+ Fixes Failed: Question Architecture**
   - Pattern indicates architectural problem
   - STOP and discuss with human partner

## Red Flags - STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- **"One more fix attempt" (when already tried 2+)**
- Each fix reveals new problem in different place

**ALL mean: Return to Phase 1.**

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too |
| "Emergency, no time" | Systematic is FASTER than guess-and-check |
| "Just try this first" | First fix sets pattern - do it right |
| "I'll write test after" | Untested fixes don't stick |
| "I see the problem" | Symptoms ≠ root cause |

## When 3+ Fixes Failed

Question the architecture:
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing?

**Discuss with human partner before more fixes.**
