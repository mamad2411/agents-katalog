---
name: systematic-debugging
description: Systematic debugging methodology - 4-phase root cause analysis. Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes.
category: engineering
exposure: standard
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

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

## The Four Phases

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - They often contain the exact solution
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably?
   - What are the exact steps?
   - Does it happen every time?
   - If not reproducible → gather more data, don't guess

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes
   - Environmental differences

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI → build → signing, API → service → database):**

   **BEFORE proposing fixes, add diagnostic instrumentation:**
   ```
   For EACH component boundary:
     - Log what data enters component
     - Log what data exits component
     - Compare: are they the same?
   ```

   **THEN run the failing operation and READ the logs.**

### Phase 2: Hypothesis and Verification

1. **Form ONE hypothesis** based on evidence
2. **Design a test** to verify/refute the hypothesis
3. **Run the test** and observe results
4. **Document findings** (even if hypothesis was wrong)

**Don't:**
- Jump to conclusions
- Fix symptoms without understanding cause
- Make multiple changes at once
- Assume "it must be X" without evidence

### Phase 3: Root Cause Confirmation

**Before fixing, confirm you understand:**

1. **What** is happening (the symptom)
2. **Where** it's happening (the location)
3. **Why** it's happening (the root cause)
4. **When** it started (the trigger)

**If you can't answer all 4, you don't understand the bug yet.**

### Phase 4: Fix and Verify

1. **Fix the root cause**, not the symptom
2. **Write a test** that reproduces the bug
3. **Verify the test fails** without the fix
4. **Apply the fix**
5. **Verify the test passes**
6. **Run full test suite** to check for regressions

## Anti-Patterns

| Anti-Pattern | Reality |
|--------------|---------|
| "I'll just try this fix" | Guessing wastes time |
| "It's probably X" | Probably ≠ definitely |
| "Quick patch for now" | Technical debt accumulates |
| "Works on my machine" | Environment differences are real bugs |
| "I've seen this before" | Past experience helps, but verify anyway |

## Evidence Collection Checklist

- [ ] Error message captured (exact text)
- [ ] Stack trace captured
- [ ] Steps to reproduce documented
- [ ] Expected vs actual behavior documented
- [ ] Recent changes reviewed (git log)
- [ ] Environment details noted (OS, versions, config)

## Quick Reference

```
Phase 1: Read → Reproduce → Check changes → Gather evidence
Phase 2: Hypothesize → Test → Document
Phase 3: Confirm What/Where/Why/When
Phase 4: Fix → Test → Verify → Regression check
```

## Integration with Our Workflow

- **When bug found:** Immediately invoke this skill
- **During investigation:** Document findings in explore/ directory
- **After fix:** Use `test-driven-development` for regression test
- **Code review:** Use `receiving-code-review` skill
