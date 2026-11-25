---
name: tdd
description: "Test-driven development: the agent writes the failing test, then the code, one behavior at a time. Use when building a feature or fixing a bug test-first, or when the user says tdd, red-green, or test-first."
---

# Test-driven development

Write the failing test, then the code that passes it, one **slice** at a time.

## Before the first test

1. Name the behavior in one line: input, expected outcome, non-goals.
2. Pick the **seam**, the public boundary you test at (function, CLI, HTTP route, rendered UI).
3. Find the repo's test command and run it once for the baseline.

## The loop

1. **Red.** One test for the next smallest behavior; run only it. It must fail because the behavior is missing; a typo, import or fixture failure is not red. If it passes at once, it is a characterization test: pick a behavior that is actually missing.
2. **Green.** The smallest code that passes; rerun that test.
3. **Next slice.** Let this slice shape the next test; never write them all up front.

Refactor once the behavior is complete and green, then rerun the relevant suite.

Code written before its test is deleted, not kept "as reference": a test written after passes at once and proves nothing. Exploring first is fine; throw the exploration away, then start at red. A test that is hard to write means an interface that is hard to use: simplify the interface.

## A good test

- Checks behavior through the seam and survives a refactor that keeps it.
- Has one reason to fail; deterministic and fast.
- Takes its expected value from an independent source. `assert add(a, b) == a + b` can never fail; `assert add(2, 3) == 5` can.
- Mocks only external boundaries (network, paid APIs, clock); makes no paid calls. A fake proves only the fake's boundary: say so.
- For model and ML code, test the deterministic parts (transforms, parsing, shapes, prompt assembly, scoring math); model quality is an experiment.

## Bugs

Write the regression test first and show it failing on the current code for the intended reason; a regression test that never failed proves nothing.

## Done

Show the test command's red output before, the same command green after, and the wider suite green. Label the work honestly: TDD, regression test, characterization test or refactor.

Sources: `mattpocock/skills` (`tdd`); [obra/superpowers](https://github.com/obra/superpowers) (`test-driven-development`, MIT).
