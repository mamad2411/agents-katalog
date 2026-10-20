---
name: testability
description: Testability as a software design property — not a testing process. Use when code is difficult to test and the reason is unclear, when designing new code that must have a test suite, when reviewing why a test suite is slow or brittle, or when refactoring to improve testability without changing tests. Covers controllability, observability, and isolation as design concerns; test smells and their root causes; and design moves that improve testability. Does not cover writing or running tests (use the /test command for that).
---

# Testability

Testability is a design property, not a testing activity. Code that is hard to test is usually hard to test because of decisions made when it was written — hidden dependencies, missing seams, state that cannot be controlled from outside.

The question "why is this hard to test?" almost always has a design answer.

For the three testability properties and design moves see [testability-properties.md](testability-properties.md).
For symptoms of poor testability in existing tests see [test-smells.md](test-smells.md).
For concrete design moves see [design-for-testability.md](design-for-testability.md).

## Testability in the quality model

Testability sits within maintainability in the ISO/IEC 25010 quality model — it is a design-time property that affects how much effort is required to validate that the system works.

Low testability does not just make tests hard to write. It makes:
- Test suites slower (because tests cannot isolate what they are testing)
- Test suites less reliable (flaky tests from shared state or timing dependencies)
- Bugs harder to locate (because failures point to large areas rather than specific causes)
- Refactoring riskier (because the test suite does not provide a reliable safety net)

## The fundamental question

Before asking "how do I test this?", ask: **why can't I test this directly?**

The answer is usually one of three things:
1. I cannot set it up in the state I need (controllability problem)
2. I cannot observe what happened (observability problem)
3. I cannot isolate it from things I don't want to test (isolation problem)

Each has a design solution. See [testability-properties.md](testability-properties.md).

## Testability is not the same as test coverage

High test coverage on untestable code produces tests that:
- Test implementation details rather than behaviour
- Break on every refactoring
- Require complex mocking setups that test the mock, not the code
- Give false confidence because they pass on code that is functionally wrong

Coverage is a metric. Testability is a property. They are not the same thing.
