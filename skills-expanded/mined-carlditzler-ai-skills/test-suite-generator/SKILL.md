---
name: test-suite-generator
description: Use for adding or improving targeted tests around features, bugs, refactors, contracts, and risky state transitions across Swift, Kotlin/Android, Flutter, Tauri, Rust, and frontend code.
---

# Test Suite Generator

## Use when
- the main task is increasing confidence with tests
- a feature, bug fix, or refactor needs targeted regression protection
- the user asks for tests, coverage improvement, or release confidence

## Do not use when
- the repo or request clearly cannot support meaningful automated tests and the real task is elsewhere
- the user needs architecture or implementation first and tests are secondary

## Working rules
- Prefer the lowest-level test that proves the behavior.
- Name tests around behavior and risk, not implementation details.
- Reuse existing helpers, fixtures, and conventions before inventing new ones.
- Avoid brittle snapshots and broad end-to-end coverage unless the repo already relies on them.
- Call out untestable areas explicitly instead of faking confidence.

## Workflow
1. Identify the behavior, invariant, or regression risk that must be protected.
2. Choose the smallest useful test layer: unit, integration, UI, or end-to-end.
3. Implement the minimum realistic coverage for the happy path and the most important edge or failure path.
4. Run the narrowest relevant tests.
5. Report what risk is now covered and what remains uncovered.

## Quality bar
- Tests should be deterministic, focused, and easy to read.
- High-value release risks such as serialization, migrations, async ordering, permissions, and core UI states should be prioritized.
- If the safest choice is not to add a test, explain why concretely.

## Reference routing
- Read `references/test-strategy.md` for layer selection and test heuristics.
- Read `references/release-quality-gates.md` when the change affects release confidence.
- Read `references/official-docs.md` only when framework test guidance matters to the test design.

## Output contract
Provide:
- what behavior the tests protect
- tests added or updated
- commands run and outcomes
- remaining uncovered risk
