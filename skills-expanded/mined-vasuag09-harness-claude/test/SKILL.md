---
name: test
description: Run the full test suite and confirm coverage meets the floor before shipping. Use in the Verify phase after review. Adds missing tests for uncovered acceptance criteria.
---

# /test — suite & coverage gate

Goal: every acceptance criterion is covered and the suite is green.

## Do this
1. Detect the runner from the repo (vitest/jest/pytest/...) — don't assume.
2. Run the **full** suite (not just the files you touched) to catch regressions.
   Run long suites inside tmux.
3. Run coverage. Compare against the spec's acceptance criteria:
   - Any criterion without a test → delegate to `harness-claude:tdd-guide` to add it (test-first).
   - Coverage < 80% on changed code → add tests for the gaps.
4. For web, add/refresh e2e for any critical flow the change affects (Playwright);
   add visual regression for visual-heavy UI.
5. Fix the implementation, not the test — unless the test is wrong.

## Exit criterion
Suite green, coverage ≥ 80% on changed code, every acceptance criterion has a test.
Then `/harness-claude:verify`.
