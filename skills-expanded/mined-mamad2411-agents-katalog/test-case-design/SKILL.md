---
name: test-case-design
description: Test pyramid structure, boundary analysis, equivalence partitioning, and coverage threshold guidelines. Use when defining what to test and how much coverage to require for a feature.
---

# Test Case Design

Test case design determines WHAT to test. Test automation determines HOW to test it. This skill covers the frameworks for systematically defining test cases from acceptance criteria, identifying the boundaries worth testing, and setting coverage requirements that balance risk against velocity.

## When to Use This Skill

- Translating acceptance criteria into test case definitions
- Identifying which boundary conditions need tests
- Setting coverage thresholds for a feature or module
- Reviewing test coverage for gaps before a launch
- Balancing test pyramid proportions for a new feature

## The Test Pyramid

The test pyramid defines the proportions of different test types:

```
           ┌─────┐
           │ E2E │  ← Fewest. Tests complete user journeys.
          ─┼─────┼─
         ─ │ Int │  ← More. Tests component interactions.
        ─  ─┼─────┼─ ─
           │Unit │  ← Most. Tests individual functions/units.
           └─────┘
```

| Layer | What It Tests | Speed | Cost | Quantity |
|-------|--------------|-------|------|----------|
| **Unit** | Individual functions, methods, classes in isolation | Fast | Low | Many |
| **Integration** | How components interact (API → DB, service → service) | Medium | Medium | Moderate |
| **E2E** | Complete user journeys through the full stack | Slow | High | Few |

### Anti-Pattern: The Ice Cream Cone

```
     ─────────────────
    │       E2E       │  ← Too many. Slow, brittle, expensive.
   ─┼─────────────────┼─
   │   Integration    │  ← OK
  ─┼─────────────────── ─
  │       Unit        │  ← Too few. Errors found late.
  └───────────────────┘
```

If your test suite has more E2E tests than unit tests, the pyramid is inverted. Refactor toward more unit tests.

## Equivalence Partitioning

Equivalence partitioning groups inputs into classes where the system should behave the same way for any input in the class. Test one representative from each class rather than exhaustively testing every value.

### Example: Age Validation (must be 18–120)

| Partition | Values | Test Representative | Expected Behavior |
|-----------|--------|--------------------|--------------------|
| Below minimum | < 18 | 17 | Reject |
| At minimum boundary | 18 | 18 | Accept |
| Valid range | 19–119 | 45 | Accept |
| At maximum boundary | 120 | 120 | Accept |
| Above maximum | > 120 | 121 | Reject |
| Non-integer | 18.5 | 18.5 | Reject |
| Non-numeric | "abc" | "abc" | Reject |
| Empty | null / "" | "" | Reject |

**Rule:** Test at least one value from each partition, plus the boundary values between partitions.

## Boundary Value Analysis

Boundary values are where bugs live. When validating a range, test:
- The value just below the minimum (should fail)
- The minimum itself (should pass)
- A typical value in the middle (should pass)
- The maximum itself (should pass)
- The value just above the maximum (should fail)

```
For a quantity field (1–99):
  Test: 0 → reject
  Test: 1 → accept (lower boundary)
  Test: 50 → accept (mid-range)
  Test: 99 → accept (upper boundary)
  Test: 100 → reject
```

## Test Case Template

```markdown
## Test Case: [TC-ID] [Feature Name — Scenario]

**Type:** Unit / Integration / E2E
**Priority:** P0 (blocking) / P1 (high) / P2 (medium) / P3 (low)
**AC Reference:** [AC-ID this test verifies]

**Preconditions:**
- [System state required before test]
- [User state / permissions required]

**Test Data:**
- [Specific data values to use]
- [Or data setup instructions]

**Steps:**
1. [Action]
2. [Action]

**Expected Result:**
[Exactly what should happen — measurable and specific]

**Notes:**
[Any known issues, dependencies, or edge cases to be aware of]
```

## Coverage Thresholds

Coverage thresholds should be calibrated to risk, not set uniformly at an arbitrary number.

### Risk-Based Coverage Guidelines

| Module Risk Level | Description | Coverage Target |
|------------------|-------------|-----------------|
| **Critical** | Payment processing, auth, data write operations | ≥ 90% |
| **High** | Core business logic, user-facing flows | ≥ 80% |
| **Medium** | Supporting features, admin functions | ≥ 70% |
| **Low** | Reporting, display-only features | ≥ 60% |
| **Configuration** | Config files, constants, migrations | Not required |

### What Coverage Measures (and What It Doesn't)

- **What it measures:** Which lines/branches were executed during tests
- **What it does NOT measure:** Whether the tests verify correct behavior

100% coverage with no assertions is worthless. 70% coverage with well-designed assertions is excellent. Coverage is a floor, not a ceiling.

### Critical Path Coverage

Regardless of overall coverage thresholds, these paths must have dedicated test coverage:
- Any path that involves money (charges, refunds, payouts)
- Any path that involves authentication or authorization
- Any path that writes or deletes data
- Any path with a time dependency or race condition risk
- Any path with an external service dependency

## Test Type Selection Guide

| Scenario | Best Test Type |
|----------|---------------|
| Input validation logic | Unit |
| Business rule calculation | Unit |
| Database query correctness | Integration |
| API request/response contract | Integration |
| Auth middleware behavior | Integration |
| Full user journey (happy path) | E2E |
| Critical cross-system workflow | E2E |
| UI state rendering | Unit (component test) or E2E |

## Regression Test Suite Definition

The regression suite is the subset of tests that must pass before every release. It should:

1. **Cover all critical paths** — every feature that, if broken, blocks launch
2. **Be fast enough to run frequently** — target < 10 minutes for the core regression suite
3. **Be stable** — flaky tests destroy confidence; remove or fix them aggressively
4. **Be maintained** — when a feature changes, its regression tests must be updated

### Regression Suite Composition

```
Core regression suite:
  Unit tests: All P0 + P1 unit tests (~80% of unit tests)
  Integration tests: All P0 + P1 integration tests
  E2E tests: All P0 E2E tests (happy paths for critical journeys only)

Extended regression suite (run on release candidates only):
  + All P2 unit and integration tests
  + P1 E2E tests (major variant flows)
```

## Best Practices

1. **Write test cases before writing tests** — the discipline of defining expected outcomes reveals spec gaps
2. **Test behavior, not implementation** — tests that break when you refactor (without changing behavior) are testing the wrong thing
3. **One assertion per test** — multiple assertions in one test obscure which assertion failed
4. **Name tests as specifications** — `test_order_cannot_be_placed_with_expired_card` is a better name than `test_payment_error`
5. **Test data is part of the spec** — define the exact data values for each test; "any valid input" is not a test case
