---
name: rc-tdd
description: "Test-driven development — red then green, one vertical slice, at agreed seams. Use to build or fix test-first. Not for picking a framework."
model: sonnet
effort: high
---

# Test-Driven Development

TDD is the red → green loop. This skill is what makes that loop produce tests worth keeping: what a
good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on
every cycle — consult them during the loop, not after.

## What a good test is

A test verifies **behaviour through a public interface**, never an implementation detail. The
implementation can change entirely; the test should not. A good test reads like a specification — *"user
can check out with a valid cart"* tells you exactly what capability exists — and survives a refactor
because it never cared about internal structure.

**Test what the code does, not what the mocks do.** A mock is a means of isolation, never the subject.

## Seams — where tests go

A **seam** is a place where you can alter behaviour without editing in that place — the interface
where behaviour is observable without reaching inside. `rc-codebase-design` owns that vocabulary
(module, interface, depth, seam, adapter) and the design decisions behind it; read it when the
question is *where the seam should be* rather than *what to test at the one that exists*.

Its third principle is this section's premise: **the interface is the test surface.** If a test has
to reach past the interface — poking at internals, asserting through a side channel, needing a
test-only accessor — that is information about the design, not about the test.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and confirm
them with the user. No test is written at an unconfirmed seam. You cannot test everything — agreeing
the seams up front is how testing effort lands on the critical paths and the complex logic instead of
on every edge case.

Ask: *"What is the public interface here, and which seams should we test?"*

## The loop

- **Red before green.** Write the failing test first, watch it fail, then write only enough code to
  pass it. A test that has never been red proves nothing — it may be passing by construction.
- **One vertical slice at a time.** One seam, one test, one minimal implementation per cycle. Each test
  is a **tracer bullet** that responds to what the last cycle taught.
- **Refactoring is not part of the loop.** It belongs to review, not to the red → green cycle.
- **Never weaken a test to make it pass.** If the test is wrong, fix the test deliberately and say so;
  if the code is wrong, fix the code.

## Anti-patterns

- **Implementation-coupled** — mocks internal collaborators, tests private methods, or verifies through
  a side channel (querying the database instead of using the interface). The tell: the test breaks on a
  refactor when behaviour did not change.
- **Tautological** — the assertion recomputes the expected value the way the code does
  (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal
  to itself), so it passes by construction and can never disagree with the code. Expected values come
  from an **independent** source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing** — all the tests first, then all the implementation. Bulk tests verify
  *imagined* behaviour: you test the shape of things rather than what a user experiences, the tests go
  insensitive to real change, and you commit to a test structure before understanding the
  implementation. Work in vertical slices instead.
- **Testing the mock** — asserting that a stub rendered, that a spy was constructed, that a fake
  returned what you told it to return. It passes whenever the mock is present and tells you nothing.
- **Test-only production code** — a method, flag or hook that exists on a production type solely so a
  test can reach inside. It ships to users and it couples the test to internals twice over.

The mocking traps — incomplete mocks that model three fields of a real ten-field payload, mocking a
dependency whose contract you have not read, and the point where mock complexity means you wanted an
integration test — are in [`references/mocking.md`](references/mocking.md), with the gate for each.

## Coverage

Coverage is a floor, not a goal: it tells you what was *executed*, never what was *verified*. A suite at
95% built from tautological assertions verifies nothing. Chase the uncovered branch only after asking
whether the covered ones are actually asserted.
