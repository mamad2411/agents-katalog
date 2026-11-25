---
name: test-driven-development
description: Test-first development that produces tests worth keeping. Use when implementing a feature, fixing a bug, or changing behavior that can be tested, when the user mentions TDD, red-green-refactor, regression tests, or test coverage, and whenever a bug fix needs a test proving it stays fixed. Works in vertical slices (one failing test, minimal code, repeat), tests behavior through public interfaces, and avoids mock-heavy, tautological, and implementation-coupled tests.
license: MIT
metadata:
  category: craft
  version: "1.2.0"
---

# Test-Driven Development

A test written first proves two things a test written later can't: that the test can fail, and that the code you wrote is what made it pass. TDD is not about coverage numbers. It is about building in small steps where each step is proven before the next one starts.

## The loop

1. **Red.** Write one small test for the next piece of behavior. Run it and watch it fail **for the right reason**: an assertion about the missing behavior, not a typo, import error, or missing fixture.
2. **Green.** Write the minimum code that makes it pass. Hard-coding is allowed if the next test will force generality.
3. **Refactor.** With tests green, clean up names, duplication, and structure. Run the tests after each change.
4. Repeat with the next behavior.

Work in **vertical slices**: one test, one implementation, repeat. Writing all the tests first commits you to a design before you've learned anything from implementing it, and produces tests of imagined behavior.

For a bug fix, the first test reproduces the bug. It must fail before the fix and pass after. If you can't make it fail, you haven't reproduced the bug yet (see `systematic-debugging`).

## What makes a test worth keeping

- **Tests behavior through the public interface.** It reads like a specification ("rejects checkout when cart is empty") and survives refactoring, because it doesn't know how the code is structured inside.
- **Independent expected values.** Expected results come from the spec, a worked example, or a known-good literal, never from recomputing them the way the code does.
- **One reason to fail.** When it fails, the name and message tell you what broke.
- **Fast and deterministic.** No real network, wall-clock time, or shared global state. Inject a clock, seed randomness, and use in-memory or containerized dependencies.
- **Mocks only at real boundaries.** Mock what you don't own and can't run cheaply (payment APIs, email, time). Don't mock your own internal collaborators; use the real ones.

## Anti-patterns

| Anti-pattern | Tell | Fix |
|---|---|---|
| Implementation-coupled | Breaks on refactor while behavior is unchanged | Assert on outputs and observable effects at the interface |
| Tautological | `expect(add(a, b)).toBe(a + b)` | Use independent known values |
| Mock theater | The test mostly verifies that mocks were called | Use real collaborators; mock only external boundaries |
| Snapshot dumping | Huge snapshots nobody reads, updated blindly | Assert the few properties that matter |
| Testing the framework | Asserting that the ORM saves or the router routes | Test your logic, not the library's |
| Flaky by design | Sleeps, real time, order-dependent tests | Inject time, await conditions, isolate state |
| Green without red | Test never seen failing | Break the code (or revert the fix) and confirm the test fails |

## Choosing what to test

You can't test everything, so put tests where bugs are likely and expensive: business rules, state transitions, parsing and validation, money and time calculations, permission checks, and anything that has broken before. Thin glue code and pure configuration rarely earn dedicated tests.

Prefer the lowest test level that can observe the behavior: unit for pure logic, integration for boundaries (database queries, HTTP handlers), end-to-end for a few critical user journeys.

## When test-first doesn't fit

- **Exploratory spikes.** Prototype freely to learn, then throw the spike away and rebuild test-first, or at least add tests before calling it done.
- **Visual layout.** Use screenshots or visual review, and test the logic behind the view.
- **Legacy code without seams.** Start with characterization tests that pin current behavior at the highest practical level, then refactor toward testable seams.

In every case, behavior changes ship with tests, and the tests have been seen to fail.
