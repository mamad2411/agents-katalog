---
name: test-first-by-evidence
description: >-
  Write the test first, watch it fail, then write the least code that passes.
  Covers where the test belongs, what makes it honest, what a passing test proves
  and what it does not, recovering when code was written before the test, and
  starting a bug fix from a red run. A test nobody watched fail proves nothing.
  Use when implementing a feature or a bugfix, when a test was written after the
  code, when a test passes the first time you run it, or when the user says
  "write tests for this", "add coverage", or "TDD this". Not for judging tests
  inside a change under review, and not for choosing a test framework.
---

# Test First by Evidence

**Core principle.** A test you did not watch fail proves nothing. It might test the wrong thing, and you would never know.

- **This is `debugging-by-evidence` pointed forward.** One says no hypothesis before a command that reproduces. This one says no implementation before a test that failed.
- **The weight sits in *Watch it fail*.** Everything else is what to do once the red is real.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## The law

```
NO PRODUCTION CODE WITHOUT A TEST YOU WATCHED FAIL
```

- **Code written before its test is unproven**, and gets re-derived from a red rather than wrapped in a test that passes immediately.
- **Make it recoverable before removing anything.** Discarding work the human has not agreed to discard is not yours to do.
- **A test that passes the first time you run it is not a test yet.** It describes what the code already does.
- **A test that errors is not a red.** An error is a broken test; a failure is a working test with nothing to satisfy it.

## Establish before the first test

- **Never ask what the repository answers.** Three things settle the setup, and it holds all three.
  - The command this project already uses to run tests.
  - Where its tests live, and what a neighbouring test looks like.
  - The runner, so the failure output means something to you.
- **Read one nearby test before writing yours.** Style is local, and a test that fights the local style is a second convention.

## Which rules to read

**This table is a gate, not a checklist.** Match the left column against what is in front of you.

- **One rule per row.** Enter at the matched row, then follow the cycle in order.
- **A small change reads two rows.** A new subsystem reads most of them. That difference is the point.
- **Where two rows match, read both.** Under-reading costs a wrong test. Over-reading costs one file.

| If you see... | Read |
| --- | --- |
| **a test about to be written**, or one that passed on its first run | `rules/watch-it-fail.md` |
| **a red you trust** and code to write against it | `rules/smallest-green.md` |
| **no obvious place for the test**, or a choice between unit, integration, and end to end | `rules/where-the-test-goes.md` |
| **mocks, fixtures, or assertions on calls** rather than on results | `rules/tests-that-cannot-lie.md` |
| **implementation that already exists** with no test behind it | `rules/code-written-first.md` |
| **a bug report, a stack trace, or a regression** | `rules/bug-fix-starts-red.md` |
| **a test that is hard to write, or needs everything mocked** | `rules/hard-to-test-is-a-signal.md` |

**Discriminators.**

- **Watch it fail against code written first.** The first owns the normal path. The second owns the recovery when the order was already broken.
- **Where it goes against what makes it honest.** Placement decides which seam. Honesty decides what it asserts once it is there.
- **Bug fix against watch it fail.** A bug fix starts from a red that reproduces a defect. The general case starts from a red that describes a wish.

**Default stance.**

- **Write the test, run it, and watch it fail before writing any implementation.**
- **Then write the least code that passes**, and run the whole suite.
- **Never claim a phase you have not observed.** A predicted failure is not a red.

## Say which phase you are in

**Report it every time.** Each phase licenses only what it names.

| Phase | Means | Licenses |
| --- | --- | --- |
| `NO-TEST` | nothing written yet | writing one test, nothing else |
| `RED` | the test ran and failed for the stated reason | implementation |
| `GREEN` | the test passes and so does everything else | refactoring |
| `REFACTORED` | duplication and names cleaned, still green | the next test |

- **Skipping a phase is the failure this skill exists to prevent.**
- **`RED` requires a run you performed.** Not a prediction that it would fail.
- **`GREEN` includes the rest of the suite.** One new green and three new reds is not green.

## Do not skip this when

- **The change is one line.** A one-line change to the wrong line is still wrong.
- **The code is too simple to break.** Simple code breaks. The test costs thirty seconds.
- **You already tested it by hand.** Manual testing leaves no record and does not re-run.
- **You will add tests after.** Tests written after pass immediately, which proves nothing about whether they can catch anything.
- **You are only exploring.** Fine. Throw the exploration away and start again with a test.

## Routing

- **The table above selects the rule.** Read a selected rule in full, and say which one you opened, in one line.
- **Judging tests inside a change under review belongs to a review of the diff**, not here.
- **Choosing a framework is a project decision**, not this skill's.
- **A direct instruction from the user outranks anything here.**
