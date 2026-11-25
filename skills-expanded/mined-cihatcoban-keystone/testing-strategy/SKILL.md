---
name: testing-strategy
description: Decides what to test, at which level, with what data, and fixes slow, flaky or false-confidence suites. Triggers - what should we test and at which level, tests pass but bugs still ship, the test suite takes twenty minutes, flaky test, contract or mutation testing.
---

# Testing Strategy

Coverage is a measure of code executed, not of behavior verified. A suite can
run every line and catch nothing — this is common, and it is why "we have 85%
coverage" and "bugs keep shipping" coexist comfortably.

Strategy answers three questions: which level, what data, and how do we know
the suite is any good.

## Choosing the level

Push every test to the **cheapest level that can actually catch the defect**.

| Level | Catches | Cost | Aim for |
|---|---|---|---|
| Unit (pure logic, no I/O) | Calculation, branching, invariants, boundaries | ms | Most of the count |
| Integration (real datastore/broker, one process) | Wiring, queries, transactions, serialization, migrations | 100s of ms | Substantial — this is where real defects hide |
| Contract | Drift between two services | ms | One per consumer/provider pair |
| End-to-end | Critical user journeys through the real stack | seconds | A handful. Only the paths whose failure stops the business |
| Manual/exploratory | The unknown unknowns | human time | Deliberate sessions, not regression |

The "pyramid" is a heuristic, not a law. For an integration-heavy service —
mostly queries and calls — a **trophy** shape (thick integration layer) catches
more real defects than a thick unit layer testing mappers.

**Where the level choice usually goes wrong:** unit-testing code whose only
risk is the SQL it generates, then mocking the database. The mock encodes your
assumption about the database; the defect is in the assumption.

## Test data

The unglamorous part that determines whether the suite is trustworthy.

- **Builders with sensible defaults**, overriding only the field under test.
  A test that sets 14 fields hides which one matters.
- **No shared fixture mutated across tests.** It produces order-dependent
  failures and tests that pass alone and fail together.
- **Realistic shapes.** Unicode, empty strings, very long values, timezone
  boundaries, locale-specific numbers. Production data is never `"test"`.
- **Never copy production data** into a test environment without
  anonymization — it is a privacy incident waiting for an audit.
- **Deterministic**: explicit seeds, frozen clock. Record the seed in the
  output so a failure is reproducible.

## Techniques worth the effort

| Technique | Use when | What it buys |
|---|---|---|
| **Property-based** | Parsers, encoders, sorting, anything with an invariant (round-trip, idempotency, ordering) | Finds edge cases you would never enumerate |
| **Golden/approval** | Complex output (rendered document, report, generated code) | Cheap regression net — but review diffs like code, never bulk-accept |
| **Contract tests** | Any service boundary | Catches drift at build time instead of at 3am |
| **Mutation testing** | Critical modules, occasionally | Tells you whether the tests *assert* or merely execute |
| **Load/soak** | Before a capacity-sensitive launch | Finds the resource that runs out first |
| **Fault injection** | Systems with external dependencies | Verifies the failure paths that reasoning says are fine |

Mutation testing is the honest answer to "is our suite good?" — it changes the
code and checks whether a test notices. Run it on the core domain even once; the
result is usually sobering.

Per-language forms of table cases, fake time and property-based tests:
`references/test-idioms.md`.

## Flakiness is a defect

A flaky test is a bug report about a race, a shared resource, or a timing
assumption — in the test or the system. A retry that turns it green destroys
that information and teaches everyone to ignore red.

Policy: quarantine (out of the gating suite, still running and visible), open an
issue with an owner and a deadline, fix or delete. **Never** auto-retry into the
main suite.

Common causes: waiting on a sleep instead of a condition; real clock and
timezone; shared database state; test order dependence; unawaited async work;
port or filesystem collisions under parallel execution.

## Suite speed

Developers run a suite that takes 2 minutes and avoid one that takes 20. Speed
is a correctness property, because an unrun test verifies nothing.

Tier it: **fast** (< 2 min, every commit, no I/O) · **integration** (every PR) ·
**slow** (nightly: e2e, load, soak). Parallelize with isolated state per worker
(separate schema or database per worker, not a shared one).

## What not to test

- Framework and library behavior — trust it, or replace it
- Getters, setters, trivial pass-throughs
- Implementation details that will change in the next refactor
- Random UI text and layout pixels

Each of these costs maintenance and catches nothing. Deleting a bad test is a
legitimate improvement; deleting a test *because it is failing* is not.

## Exit checklist

- [ ] Every test sits at the cheapest level that could catch its defect
- [ ] Integration tests run against the real datastore, not a mock of it
- [ ] Test data uses builders; no shared mutable fixture
- [ ] Clock frozen, randomness seeded, no sleeps
- [ ] Zero flaky tests in the gating suite; quarantined ones have owners
- [ ] Fast tier under the time budget in `CONSTRAINTS.md`
- [ ] Critical modules have been mutation-tested at least once
- [ ] Every service boundary has a contract test
