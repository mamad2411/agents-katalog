---
name: tdd
description: Test-driven development for data pipelines. Use when the user wants to build a transform or fix a pipeline bug test-first, mentions "red-green-refactor", or wants unit tests for a model, parser, or loader.
---

# Test-Driven Development

TDD is the red → green loop, and in a pipeline it runs on exactly one kind of test: the mock-input unit test. This skill is the reference that makes that loop produce tests worth keeping: which tests the loop can run on, what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## Code tests and data tests

A pipeline has two test planes. A **code test** runs transform logic against fixed mock inputs and asserts exact expected rows. It is deterministic, runs in dev and CI, and goes red only when the logic is wrong. A **data test** audits live data after materialization (unique, non-null, in-range), so it can go red with zero code change and stay green over broken logic.

The loop runs on code tests only. Red on a data test tells you about today's warehouse contents, not about your diff, so you cannot drive implementation from it. Data tests are audit gates that ship *alongside* the loop's output, not inside it: when a cycle fixes a bug, the code test pins the logic and a data test guards the live table. Cross-model behavior is verified elsewhere: real DAG runs in the repo's CI pipeline, whose workflow and gates the repo's testing doc names.

Before writing any test, name its plane. If you can't supply the inputs, it's not a code test. Where each plane lands in the current repo (framework, CI gates, the house oracle) is repo data, not skill logic: read the repo's testing doc (`docs/agents/testing.md`, if present) before agreeing seams; proceed silently if absent.

## What a good test is

Tests verify a transform's behavior through its output rows, not its internal SQL. The model can be rewritten entirely, with CTEs restructured and joins reordered, and the test shouldn't change. A good test reads like a specification. "Late-arriving rows land in their processing-month partition" tells you exactly what behavior exists, and its expected rows are hand-derived from that specification, never from running the code.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mock-input guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. A pipeline has two. At the **model boundary**, the test framework swaps every upstream reference for mock rows and diffs the model's output against expected rows. The other is the **pure function** in loader or parser code, which maps an immutable input batch to output rows with no side effects. The smallest testable unit of SQL is a whole model; there is no per-CTE testing. A model too tangled to hand-derive expected rows for is a seam problem, so split the model.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm them with the user. No test is written at an unconfirmed seam. You can't test everything, so agreeing the seams up front is how testing effort lands on the complex logic (date math, window functions, case-when ladders, dedup) instead of on what the engine already guarantees.

Ask: "Which models and functions are under test, and which behaviors at each?"

When the shape of that boundary is itself in question (how deep the model is, where the seam belongs, what grain and columns it should expose), use the `/codebase-design` skill for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms as this suite grounds them in a warehouse, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Plane-confused**: the "failing test" is a data test: it asserts on live warehouse contents, so red depends on what loaded today, not on your diff. It stays green over broken logic whenever today's data happens not to exercise the bug. Keep it as an audit; drive the loop with a unit test whose mock rows contain the case.
- **Implementation-coupled**: mocks internal helper functions, asserts on intermediate dataframes, or verifies through a side channel (re-querying the built table instead of diffing the declared output). The tell: the test breaks when you restructure CTEs but the output rows haven't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does, or, in the pipeline form, the expected rows were produced by running the model and pasting its output back. That is a snapshot pin: it asserts the code does what the code does, bugs included, and can never disagree with it. Expected rows must come from an independent source of truth: a hand-worked example, the spec, a reconciliation against the source system, or an invariant the formula can't smuggle in (row counts across joins, sums across pivots).
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than consumer-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing unit test first, with mock rows in and expected rows out, then only enough SQL or code to pass it. Don't anticipate future tests or add speculative columns.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Minimal fixtures.** Mock only the columns the transform touches and the fewest rows that force the behavior. The inner loop runs on the warehouse in seconds rather than milliseconds, and fixture bulk is loop drag.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.
