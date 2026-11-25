---
name: tdd-pro
description: Test-driven development workflow using red-green-refactor for features, bug fixes, and risky behavior changes. Adapted from Matt Pocock-style TDD for Codex v4.1. Use when tests can clarify requirements, prevent regressions, or guide implementation in small vertical slices.
---

# TDD Pro

## Workflow

1. Identify one externally visible behavior.
2. Write the smallest failing test that proves the missing behavior or bug.
3. Run the narrow test and confirm it fails for the expected reason.
4. Implement the smallest code change to pass.
5. Run the test and relevant adjacent checks.
6. Refactor only after green.
7. Repeat for the next behavior or edge case.

## Good Tests

- Assert behavior, not private implementation.
- Use realistic inputs and domain language.
- Cover one reason to fail per test where practical.
- Include regression tests for fixed bugs.
- Keep mocks at external boundaries.
- Avoid snapshot-only tests for meaningful logic.

## When Not To Force TDD

- Pure styling changes with low behavioral risk.
- Exploratory prototypes intended to be thrown away.
- Codebases with no viable test harness, unless adding one is in scope.

## Output

Report failing test added, implementation change, final test command, and result. If TDD was skipped, state why.
