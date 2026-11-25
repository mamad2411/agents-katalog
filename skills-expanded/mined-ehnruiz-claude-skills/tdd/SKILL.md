---
name: tdd
description: Test-driven development, red then green, one vertical slice at a time. Use when building a feature, a rule, a config option or a bug fix test-first, when the user says "TDD", "red-green" or "write the test first", or when a subagent is handed a ticket to build.
---

# Test-driven development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests
worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the
loop. Every section applies on every cycle: consult them before and during the loop, not
after. Credit and license: `LICENSE.md` in this folder.

**Project copy first.** If the repository has its own `.claude/skills/tdd/SKILL.md`, read it and follow it instead of this file. A skill installed for all your projects outranks a project skill with the same name, so without this step a repository's own version of this skill would never run.

Before exploring, read the project's own testing notes (README, CONTRIBUTING, an architecture
doc, `AGENTS.md`/`CLAUDE.md`) so test names use the project's words and the tests land where
the project keeps them.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change
entirely; tests shouldn't. A good test reads like a specification: "rejects an order with an
empty cart" says what capability exists, and it survives refactors because it doesn't care
about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior
without reaching inside. Tests live at seams, never against internals. Most projects have
some of these, from cheapest to dearest:

1. **A pure function or module API** with hand-built inputs. No I/O. Most logic belongs here.
2. **A module with its system boundaries faked**: the HTTP client, the clock, the database
   behind an interface (see [mocking.md](mocking.md)).
3. **An integration test** against real dependencies: a test database, a fixture site, a
   container.
4. **The entry point**: the CLI, the HTTP handler, the UI, driven from outside.

**Test only at pre-agreed seams.** Before writing any test, write down the seams under test and
confirm them with the user (or, for a subagent, with the ticket). Give each proposed seam a
one-line note on what it catches and what it misses, so the choice between seams is not a guess.
No test is written at an unconfirmed seam. Use the lowest seam that reaches the behavior.

Every heuristic, validator or detector ships with at least one **negative test**: legitimate
input it must stay quiet on. A false positive is a bug, and the negative test is how a change
proves it did not add one.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private helpers, or verifies
  through a side channel. The tell: the test breaks when you refactor but behavior hasn't
  changed.
- **Tautological**: the assertion recomputes the expected value the way the code does, so it
  passes by construction. Expected values come from an independent source: a known-good
  literal, the spec, the issue.
- **Horizontal slicing**: writing all tests first, then all implementation. Work in **vertical
  slices**: one test → one implementation → repeat, each test a **tracer bullet** that responds
  to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first and watch it fail for the reason you
  expect, then write only enough code to pass it.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Run one test file while looping, everything once at the end.** Before reporting done, run
  the project's full gates (typecheck, lint, the whole suite). Judge each by its exit code,
  never by reading the output for the word "pass", and never through a pipe.
- **A fix's test must prove it.** For a bug fix, the new test has to fail on the code without
  the fix. The `regression-proof` skill shows how to check that in a scratch worktree.
- **Wait on the condition, not the clock.** A test that needs something to happen polls for it
  with an explicit timeout (`vi.waitFor`, Playwright's `expect.poll`, a retry-until helper) and
  returns as soon as it does. A fixed sleep guesses how long it takes, and the guess loses on a
  loaded machine or in a full suite. A sleep stays only to show that something did not happen,
  with a comment naming the event it waits out.
- **Fake the clock for time-based code.** Debounce, quiet windows and retry delays run under the
  test framework's fake timers, and the test advances the clock. Fake only the timers the code
  uses: faking everything can freeze an HTTP client's keep-alive. A speed or size claim is
  asserted as a count (calls, comparisons, bytes), not a duration.
- **Refactoring is not part of the loop.** It belongs to review, not to the red → green cycle.
