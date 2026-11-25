---
name: test-driven-development
description: Use when implementing any feature or bugfix - requires writing a failing test before writing any production code
---

# Test-Driven Development

## Overview

Write a failing test first, then implement the minimal code to pass it, then refactor.

**Core principle:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.

**This is mandatory. No exceptions for production code.**

## The Red-Green-Refactor Cycle

### RED: Write Failing Test

1. Write a minimal test demonstrating desired behavior
2. Run test - it MUST fail
3. Verify it fails for the right reason

### GREEN: Implement Minimal Code

1. Write the simplest code to pass the test
2. No extra features, no optimization
3. Run test - it MUST pass

### REFACTOR: Clean Up

1. Improve code while maintaining test pass
2. Remove duplication
3. Improve naming
4. Run tests to ensure nothing breaks

## Why This Matters

- Tests written after code pass immediately - proving nothing
- Manual testing is ad-hoc and non-repeatable
- TDD catches bugs before deployment
- Tests become safety net for future changes

## Critical Requirements

Tests must be:
- **Minimal** - one behavior each
- **Clear** - descriptive naming
- **Real** - avoiding unnecessary mocks

## Verification Checklist

- [ ] Test fails before implementation (RED)
- [ ] Test passes after implementation (GREEN)
- [ ] Refactoring maintains pass
- [ ] Test actually exercises the code

## Red Flags - STOP

- Code written before test
- Tests that pass immediately
- Manual verification instead of tests
- "I'll write tests after"
- Skipping the cycle

**If you wrote code before test:** Delete it. Start over with test first.

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| Test passes immediately | You wrote code before test |
| Manual testing | Ad-hoc, non-repeatable |
| "This is simple" | Simple code breaks too |
| "No time for tests" | Testing saves time by preventing rework |

## Integration

- **Phase 4.1 of debugging** - Create failing test before fixing
- **Plan execution** - Each task includes test-first step
- **Subagent-driven development** - Implementation includes test creation
