---
name: Test-Driven Development
description: Guidance for using a red-green-refactor cycle before changing production behavior.
---

# Test-Driven Development

> No production code without a failing test. RED-GREEN-REFACTOR, every time.

## Triggers

- User asks to implement a feature, function, or component
- User asks to add behavior to existing code
- Any task that produces production code

## HARD GATE: Failing Test Required

**Before writing ANY production code**, you MUST:

1. Write a test that describes the desired behavior
2. Run the test and **show the failure output**
3. Only then write the production code

If you catch yourself writing production code first, **STOP immediately**, delete it, and write the test.

## The RED-GREEN-REFACTOR Cycle

### RED Phase: Write a Failing Test

```
1. Identify the smallest unit of behavior to implement
2. Write a test that asserts the expected behavior
3. Run the test
4. VERIFY: The test MUST fail (if it passes, your test is wrong or the feature already exists)
5. Show the failure output to confirm RED state
```

**What to test**: The public interface, not implementation details. Test behavior, not structure.

### GREEN Phase: Make It Pass

```
1. Write the MINIMUM code to make the failing test pass
2. Do not add extra logic, error handling, or optimizations yet
3. Run the test
4. VERIFY: The test MUST pass
5. Show the pass output to confirm GREEN state
```

**Minimum means minimum**: If a hardcoded return value makes the test pass, that's valid for GREEN. The next RED cycle will force generalization.

### REFACTOR Phase: Clean Up

```
1. Improve the code WITHOUT changing behavior
2. Remove duplication, improve naming, extract helpers
3. Run ALL tests (not just the new one)
4. VERIFY: All tests still pass
5. Show the test output to confirm no regressions
```

## Anti-Rationalization Table

| Excuse | Response |
|--------|----------|
| "It's too small for a test" | If it's too small for a test, it's too small to get wrong. Write the test. |
| "I'll add tests after" | Tests written after are verification, not design. Write the test first. |
| "The code is obvious" | Obvious code still needs a test to prevent regression. Write the test. |
| "Testing this is hard" | Hard-to-test code is a design smell. Refactor for testability. |
| "There's no test framework set up" | Set it up. That's part of the task. |
| "The user didn't ask for tests" | TDD is a Non-Negotiable (#6). Tests are not optional. |

## Integration with Existing Tools

- Use `context7` MCP to look up framework-specific testing patterns (pytest, jest, vitest, etc.)
- Use `testing-methodology` skill for test strategy decisions (unit vs integration)
- Use `confidence-check` skill before starting TDD if approach is uncertain
- Tests written here satisfy the `verification-before-completion` evidence requirement

## Cycle Size

Each RED-GREEN-REFACTOR cycle should be **2-5 minutes**. If a cycle takes longer:
- The unit of behavior is too large. Break it down.
- You're writing too much code in GREEN. Only write the minimum.

## Exceptions

TDD applies to **production code**. It does NOT apply to:
- Exploratory/spike code (explicitly marked as throwaway)
- Configuration files (YAML, JSON, TOML)
- Documentation
- One-off scripts the user explicitly labels as scratch work

The user can override with explicit instruction: "skip TDD for this" or `--skip-gate`.
