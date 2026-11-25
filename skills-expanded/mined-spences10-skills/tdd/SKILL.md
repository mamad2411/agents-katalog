---
name: tdd
# prettier-ignore
description: "Test-driven development with a red-green-refactor loop. Use when explicitly asked for TDD, red-green-refactor, test-first development, or integration-test-led feature work."
metadata:
  last_updated: "2026-05-10"
  verified_against: "current local skill refresh"
---

# Test-Driven Development

Drive implementation through tests using a red-green-refactor loop.

> Adapted from [Matt Pocock's TDD skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md).

## Philosophy

Test behavior through public interfaces, not implementation details. Good tests read like specifications for what the system does. They should survive internal refactors because they do not know about private functions, internal collaborators, or storage details.

Prefer integration-style tests that exercise real code paths. Mock only at system boundaries: network calls, databases, file systems, clocks, and third-party services. See [mocking.md](references/mocking.md).

## When to Use

Use this skill only when the user asks for:

- TDD
- red-green-refactor
- test-first development
- integration-test-led feature work
- fixing a bug by first writing a failing regression test

Do not activate for general “write tests” or “add coverage” requests.

## Workflow

### 1. Plan the Interface

Before writing code, identify the public surface area and behaviors:

- What function, endpoint, component, command, or module will callers use?
- What inputs and outputs matter?
- What are the most important success, failure, and edge cases?
- Which behaviors should be tested first?

Confirm the plan with the user when scope is ambiguous. Design for the caller, not the implementation. See [interface-design.md](references/interface-design.md).

### 2. Write One Tracer Bullet Test

Write one test for the simplest meaningful behavior. It must:

- Use the public interface
- Assert observable behavior
- Fail for the expected reason

```text
RED: one behavior test exists and fails
```

Do not write all tests first. That creates horizontal slices: tests for imagined behavior before the implementation teaches you anything.

### 3. Make It Green

Write the minimum implementation needed for that one test to pass.

```text
GREEN: the new test passes with minimal code
```

Hardcoding is acceptable if it is genuinely the smallest step. Do not add speculative features for future tests.

### 4. Repeat Vertically

Add the next behavior one cycle at a time:

```text
RED → GREEN: behavior 1
RED → GREEN: behavior 2
RED → GREEN: behavior 3
```

Each new test should respond to what you learned from the previous cycle.

### 5. Refactor Under Green

Only refactor when tests are green. Remove duplication, improve names, deepen modules, and simplify interfaces while keeping the suite passing. See [refactoring.md](references/refactoring.md).

## Per-Cycle Checklist

- Test describes behavior, not implementation
- Test uses public interface only
- Test would survive an internal refactor
- Code is minimal for the current test
- No speculative behavior was added

## Anti-patterns

- Writing implementation before the test
- Writing many tests before making one pass
- Testing private methods or internal state
- Mocking internal collaborators by default
- Making tests pass by weakening assertions
- Refactoring while red

## References

- [deep-modules.md](references/deep-modules.md) - Why to test surface area, not internals
- [interface-design.md](references/interface-design.md) - Contract-first design
- [mocking.md](references/mocking.md) - When and how to use test doubles
- [refactoring.md](references/refactoring.md) - Safe refactoring under green tests
- [tests.md](references/tests.md) - Test structure, naming, and assertions
