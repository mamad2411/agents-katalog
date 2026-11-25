---
name: testing-anti-patterns
description: Use when reviewing tests for fragility, over-mocking, false positives, missing production wiring, or assertions that do not prove the requirement.
---

# Testing Anti-patterns

Watch for:
- Tests that assert implementation details instead of behavior.
- Mocks that replace the behavior being tested.
- No negative, boundary, or failure-path coverage.
- Snapshot-only assertions.
- Tests that pass without production wiring.
- Flaky timing or network dependencies without isolation.

For each issue, propose the smallest test change that would fail on the current bug.

