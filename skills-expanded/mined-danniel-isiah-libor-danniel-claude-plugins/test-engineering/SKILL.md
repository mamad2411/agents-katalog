---
name: test-engineering
description: Design test cases — UAT (stakeholder-readable acceptance scenarios) and automated tests adapted to the project's stack. Use when planning or writing tests, verifying acceptance criteria, or deciding coverage. Primary skill of the qa-tester; also used by the implementer.
---

# Test Engineering

## Two modes
- **UAT cases** (stack-independent): for each acceptance criterion, a numbered scenario a human/stakeholder can run — Given/When/Then, preconditions, steps, expected result, pass/fail.
- **Automated tests** (stack-dependent): pick the runner via `stack-detection` + `framework-expertise` (Pest/PHPUnit for Laravel, Vitest/Jest for Vue/React, Playwright/Cypress for e2e).

## Test pyramid
Many fast unit tests, fewer integration, few e2e. Test behavior, not implementation. One concept per test; clear arrange/act/assert.

## Coverage strategy
Cover every acceptance criterion (traceability: requirement → UAT case → automated test). Add edge cases: empty/null, boundaries, invalid input, auth failures, concurrency.

## Output (04a-qa.md)
A verdict per acceptance criterion (met/not), UAT cases, automated-test gaps, edge cases found, and repro steps for any failure.
