---
name: superpowers-tdd
agent_created: true
version: 1.0.0
description: RED-GREEN-REFACTOR enforcement. Write failing test first, watch it fail, write minimal code to pass. This skill should be used when implementing any feature, bugfix, or behavior change that involves writing code.
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over. Don't keep it as "reference", don't "adapt" it — delete means delete. Implement fresh from tests.

## Red-Green-Refactor

### RED — Write Failing Test

Write one minimal test showing what should happen. One behavior, clear name, real code (no mocks unless unavoidable).

### Verify RED — Watch It Fail

**MANDATORY. Never skip.** Run the test. Confirm: test fails (not errors), failure message is expected, fails because feature missing (not typos).

### GREEN — Minimal Code

Write simplest code to pass the test. Don't add features, refactor other code, or improve beyond the test.

### Verify GREEN — Watch It Pass

**MANDATORY.** Run the test. Confirm: test passes, other tests still pass, output pristine.

### REFACTOR — Clean Up

After green only: remove duplication, improve names, extract helpers. Keep tests green. Don't add behavior.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Already manually tested" | Ad-hoc is not systematic. No record, can't re-run. |
| "Deleting hours is wasteful" | Sunk cost fallacy. Unverified code is technical debt. |
| "TDD will slow me down" | TDD is faster than debugging. |

## Red Flags — STOP and Start Over

Code before test. Test after implementation. Test passes immediately. Tests added "later". Rationalizing "just this once". "Keep as reference" or "adapt existing code". "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

## Verification Checklist

Before marking work complete:

- Every new function/method has a test
- Watched each test fail before implementing
- Each test failed for expected reason (feature missing, not typo)
- Wrote minimal code to pass each test
- All tests pass, output pristine

## Final Rule

Production code must have a test that existed and failed first. Otherwise it is not TDD.
