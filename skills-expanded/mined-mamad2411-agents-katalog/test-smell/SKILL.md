---
name: test-smell
description: Detect test smells/anti-patterns — over-mocking, fragile assertions, slow setup, flaky timing; flag each with its layer and a refactor. Reviews existing tests, not authoring them (unit-tests).
---

# test-smell

> Read an existing test suite the way a reviewer would — find the tests that will rot, mislead, or flake, and say how to fix each.

## When to use

- A test suite is slow, flaky, or brittle and you want the *causes*, not just a green/red.
- Reviewing a test file or test diff for quality (distinct from reviewing the production code).
- A workflow invokes `polymath-qa:test-smell`.

This scans *existing* tests. It does not write tests (`polymath-qa:unit-tests`), find untested behavior (`polymath-qa:coverage-gap`), or judge assertion strength specifically (`polymath-qa:assertion-quality`).

## Inputs

- The test files or test diff to review.
- Optionally the production code under test, to judge over-coupling.

## Smells to flag

- **Over-mocking** — mocking internal collaborators; the test asserts the mock, not behavior.
- **Fragile assertions** — asserting incidental output (full strings, ordering, timestamps) that breaks on unrelated change.
- **Eager / multi-behavior tests** — one test covering several behaviors; unclear reason-to-fail.
- **Slow setup** — per-test heavy fixtures, real I/O where a seam would do.
- **Flaky timing** — `sleep`, wall-clock, ordering, shared mutable state across tests.
- **Test interdependence** — tests that pass only in a given order or share state.
- **Misplaced layer** — an integration concern tested as a unit (or vice versa).

## Procedure

1. Read the tests; for each smell found, cite the test by name and the line/pattern.
2. Name the layer the test *should* live at (unit / integration / e2e) if misplaced.
3. Recommend a concrete refactor per finding (introduce a seam, narrow the assertion, hoist setup, remove the sleep).
4. Rank findings by blast radius (flake-causing > brittle > slow > cosmetic).

## Quality bar

- Every finding cites a specific test, not "the suite generally".
- Each finding pairs the smell with a concrete fix and the correct layer.
- Does not propose rewriting passing tests with no smell — churn is not a finding.
