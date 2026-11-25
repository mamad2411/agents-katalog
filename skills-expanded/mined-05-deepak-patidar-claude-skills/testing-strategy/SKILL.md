---
name: testing-strategy
description: Deciding what to test, at which level, and how to keep tests trustworthy. Use when writing tests, setting up a test suite, reviewing test coverage, fixing flaky tests, doing TDD, or when the user says "test", "coverage", "unit test", "integration test", "e2e", or "how do I test this".
---

# Testing Strategy

Tests exist to let you change code fearlessly. A suite you don't trust, don't run, or that breaks on every refactor provides negative value. Optimize for **bugs caught per minute of maintenance**, not coverage percentage.

## What to test — priority order (spend your budget top-down)

1. **Money and state-machine paths**: anything computing totals, tax, discounts, stock, balances, status transitions. These get exhaustive unit tests including the ugly inputs (zero, negative, rounding boundaries, max values, illegal transitions).
2. **Authorization**: for each protected route, at least one test proving the wrong principal is refused — wrong tenant's object (the IDOR test), insufficient role, no auth. These tests are cheap and catch breaches.
3. **The golden paths, end-to-end-ish**: one integration test per core user journey (signup→login, create invoice→stock decrements→payment records). Through the real API surface against a real (containerized) database — this is where wiring bugs live.
4. **Regression pins**: every production bug you fix gets a test that fails on the old code, forever. This is the highest-signal test category that exists; never skip it.
5. **Contract edges**: validation rejects what it should; error envelope shape is stable; pagination boundaries.

Below the line (test only with a reason): getters, framework glue, UI cosmetics, third-party libraries' own behavior.

## Which level — the honest trade

- **Unit** (pure logic, no I/O): milliseconds, pinpoint failures — put all *calculation and decision* logic here, which is an argument for extracting logic from I/O (see code-quality). If testing a function needs 5 mocks, the function's design is the finding.
- **Integration** (service + real DB): the default level for CRUD apps — most real bugs are query/transaction/constraint bugs that mocks hide. Use a real disposable database (Docker); an in-memory fake with different semantics tests a different app.
- **E2E** (browser/UI): few, only golden paths, because they're slow and flaky. They answer "is the product alive?", not "is the logic right?".

Mock only at *system boundaries you don't own* (SMS, payment gateway, clock, external HTTP) — that's what adapter interfaces are for (architecture-design). Mocking your own internals welds the test to the implementation: every refactor breaks tests without catching bugs.

## Writing tests that stay trustworthy

- Test behavior through the public surface, not private internals. Assert outcomes (response, DB state, emitted event) not call sequences.
- Each test: one behavior, named as a sentence (`test_payment_over_balance_is_rejected`), arrange-act-assert visible, independent of other tests and of execution order.
- Test data: build minimal explicit fixtures per test; shared mega-fixtures rot into "nobody knows what depends on this".
- Determinism is non-negotiable: inject the clock, seed randomness, never `sleep`-and-hope (wait on conditions), never depend on network or wall-clock date (an Apr–Mar financial-year bug that only fails in April is a test bug too).

## Flaky tests — the policy

A flaky test is a broken alarm: quarantine it same-day (skip with a ticket), fix the root cause (real race? test race? shared state?) within days, or delete it honestly. Re-running until green trains the team to ignore red — after that, the suite is decoration.

## TDD, pragmatically

Red-green-refactor shines for algorithmic/rule-heavy code (write the pricing test first) and for bug fixes (reproduce first — mandatory). It's ceremony for exploratory UI work. Either way, the invariant holds: **watch each new test fail once** — a test you've never seen fail may be asserting nothing (this catches ~1 in 10 AI-written tests).

## Definition of tested (for a feature to be called done)

- New logic: units for the decisions, one integration test for the wiring.
- The failure paths are tested, not just success — the catch blocks, the validation rejections, the insufficient-permission case.
- Suite runs green from a clean checkout with one command; the command is documented.
- You ran it. "Tests written" without a passing run reported is not tested (report the actual output).
