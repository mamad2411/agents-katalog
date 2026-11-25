---
name: generate-or-validate-unit-tests
description: Atomic unit-test generation or validation against repo harness and coverage rule
model: sonnet-4-6
token_budget: {input: 6000, output: 3000}
---

# Generate or Validate Unit Tests

**Purpose:** Centralize **how** to run or author unit tests so backend/frontend agents do not restate percentages or frameworks.

## When to invoke

- After implementing a feature or bugfix
- When CI or pre-merge hooks report test failures
- When validating coverage against **`rules/coverage-rule.md`**

## Steps

1. **Detect harness** — Maven/Gradle/npm/xcodebuild/JMeter per `rules/pre-merge-test-enforcement.md` Stage 1.
2. **Run** — Execute the project’s unit-test command; fix failures before merge unless policy allows a documented bypass (`sdlc skip-tests --work-item=…`).
3. **Coverage** — Compare results to **`rules/coverage-rule.md`** and stack rules under `stacks/<stack>/rules/` when present.
4. **Escalate** — If tests cannot run, use **`sdlc skip-tests`** with a work item — not `SDLC_SKIP_TESTS=1` alone.

## Do not

- Lower thresholds in agent prose — **always** cite **`rules/coverage-rule.md`**.
