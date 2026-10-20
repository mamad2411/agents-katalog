---
name: testing
description: Create, repair, and evaluate tests for unit, integration, end-to-end, contract, regression, CI, and bug-fix workflows. Use when implementing code with meaningful risk, fixing bugs, reviewing test gaps, or investigating failing test suites.
---

# Testing

## Workflow

1. Find the existing test framework, naming style, fixtures, mocks, and scripts.
2. Cover the behavior that matters, not implementation details.
3. Include normal path, error path, and boundary condition when risk justifies it.
4. Add regression tests for bug fixes.
5. Keep mocks at system boundaries and avoid mocking the function under test.
6. Run the narrowest relevant test first, then broader checks when needed.

## Priorities

1. Security or data integrity paths.
2. User-visible behavior.
3. Cross-module contracts.
4. Previously broken behavior.
5. Complex branching logic.

## Output

Report what was tested, command used, result, and any untested risk.
