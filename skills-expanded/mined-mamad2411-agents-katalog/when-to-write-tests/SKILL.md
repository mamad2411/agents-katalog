---
name: when-to-write-tests
description: Decide whether to add a test. Use before writing or requesting tests. Default is no new test. Prefer a few end-to-end happy-path tests of the public contract over unit tests of internals.
---

# When to write tests

Do not unit-test every little thing. Prefer a few end-to-end happy-path tests of the public contract.

## Default

No new test.

Smoke the changed path (run the thing). That is verification.

## Write a test only when

- The user asked for one, or
- A **public observable contract** changed and nothing already covers the happy path (store API, HTTP route, migration backfill of live rows).

If you write one, make it end-to-end on that happy path. Do not add a unit-test layer underneath.

## Do not write a test for

- Comment / docs-only edits
- Internal helpers, encoders, bind-list rewrites
- "Every new function/method"
- Edges an advisory invented that are not the contract
- Refactors that keep the same public behavior (existing tests are the regression net)

## Instruction-stack trap

These used to fire too often. Treat them as opt-in; this preference wins:

- Bundled `test-driven-development` — "any feature or bugfix", "every new function has a test"
- `using-superpowers` 1% match — does **not** mean invoke TDD on every implement
- `AGENTS.md` "regression tests for behavior changes" — means public contract, not every internal change
- Session advisories asking for another unit test of plumbing

`verification` is end-to-end smoke, not a vitest file.

User instructions beat skills. This preference is a user instruction.

## Fair example

Seed old inbound tables, apply the migration, list events, assert facts and metadata survived and the matches table is gone.

## Unfair example

A test per helper or per comment rewrite.
