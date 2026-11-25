---
name: eng-testing-strategy
version: 1.0.0
description: Design a test strategy that matches test types to risk, targets meaningful cases over coverage percentage, and keeps the suite fast, deterministic, and trustworthy.
author: matrixx0070
tags: [testing, test-strategy, coverage, quality, ci, pyramid]
capabilities: []
---

## When to use

When planning how to test a new feature, service, or system — or when an existing suite is slow, flaky, or gives false confidence. Coverage percentage is a means; the goal is catching regressions cheaply.

**Not for:** writing one specific test case (just write it), or chasing a coverage number for its own sake. This is strategy — the mix and the gate — not individual assertions.

## Method

1. **Map the risk.** List what breaking would hurt most: core business logic, money paths, auth, data integrity, external contracts. Test heaviest where risk is highest.
2. **Choose the mix along the pyramid.** Unit tests for logic and edge cases (fast, many); integration tests for seams and real dependencies; end-to-end for critical journeys only (few, high-value). If e2e count is climbing, push cases down to cheaper layers.
3. **Cover the right cases:** happy path, boundaries, error/failure paths, and known past bugs (regression). Include at least one adversarial/invalid-input case per surface.
4. **Decide isolation.** Mock external systems and nondeterminism (clock, network, randomness); do *not* mock your own logic into meaninglessness. If a mock stops mirroring the real contract, it tests fiction — pin it to the real shape or use the real thing.
5. **Design for trust and speed.** Tests must be deterministic, independent, and fast enough to run on every commit. A flaky test is a defect — quarantine and fix it, don't retry-loop around it.
6. **Define the gate:** what must be green before merge vs. what runs nightly or pre-release.

## Example

```
Feature: checkout discount codes.
Risk map: money path (High), code validation (High), UI banner (Low).
Mix: ~20 unit (validation, expiry, stacking rules, negative totals),
     ~5 integration (discount service + real DB),
     1 e2e (apply valid code -> correct charged total).
Cases: valid, expired, already-used, malformed, discount > cart total.
Isolation: mock payment gateway; use real DB in integration.
Gate: unit + integration block merge; e2e runs pre-release.
```

## Pitfalls

- **Coverage theater** — 90% coverage that never asserts on failure paths or money math.
- **Inverted pyramid** — slow, flaky e2e doing work a unit test should own.
- **Over-mocking** until tests pass regardless of whether the real code works.
- **Tolerating flakes with retries** instead of treating them as defects, eroding trust in green.

## Output format

```
Risk map: <what to protect, ranked>
Test mix: unit / integration / e2e — rationale + rough counts
Coverage plan: <cases per critical area, including failure paths>
Mocking & isolation: <what's mocked vs. real, and why>
CI gate: <blocking suites vs. nightly/pre-release>
Gaps & risks accepted: <what you deliberately don't test, and why>
```
