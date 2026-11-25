---
name: follow-lib-fast-check
description: Use fast-check for property-based testing — arbitraries, shrinking, invariants
argument-hint: "[target-or-scope]"
related:
  - run-verify
  - run-test
  - follow-tool-vitest

---

## Goal

Use fast-check for property-based testing — arbitraries, shrinking, invariants

## Scope

Use when the task involves `fast-check` — setup, writing property tests, model-based testing, debugging counterexamples

- Use this skill for property-based testing only — general unit tests go to `/run-test` or `/follow-tool-vitest`
- `fast-check` is a test library — install as a devDependency and there is no standalone CLI (run via the test runner)
- Latest: `fast-check@4.10.2` (verified 2026-09-24) — v4 requires Node ≥12.17 / ES2020 and drops deprecated arbitraries (`unicode*`, `ascii*`, `char`, `uuidV`, `.noBias`, `.noShrink`) while including invalid dates and null-prototype objects by default
- References: [apis](references/apis.md) 
## Execute

### 1. Install And Configure

> Goal: install `fast-check` and set run parameters

1. Run `bun add -D fast-check` — devDependency only, never put it in `dependencies`
2. Install the runner integration matching the test framework: `bun add -D @fast-check/vitest` for vitest (setup: `/follow-tool-vitest`), `@fast-check/jest` for jest, `@fast-check/ava` for ava
3. Install `bun add -D @fast-check/poisoning` if you need prototype-pollution checks during tests
4. Set global defaults with `fc.configureGlobal({ numRuns, seed })` or the env vars `FAST_CHECK_NUM_RUNS` / `FAST_CHECK_SEED`
5. Check the version in `package.json` — the v4 API differs from v3 (deprecated arbitraries removed)

### 2. Write Property Tests

> Goal: write property tests that assert invariants

1. Write a property with `fc.assert(fc.property(arb, (x) => invariant))` — the invariant is a condition that must always hold
2. Use `fc.asyncProperty(arb, async (x) => ...)` for async code
3. Use `fc.pre(condition)` inside the property for preconditions — skip irrelevant inputs instead of hand-generating
4. Pick arbitraries by domain: `fc.string()`, `fc.integer({ min, max })`, `fc.record()`, `fc.oneof()`, `fc.array()`
5. Use `fc.sample(arb, n)` to inspect generated values while debugging
6. Use `fc.statistics(property, classifier)` to measure the distribution of generated inputs

### 3. Handle Failures And Shrinking

> Goal: reproduce and turn counterexamples into regression tests

1. On failure, fast-check automatically shrinks to a minimal counterexample
2. Record the `seed` and `path` from the failure output — replay with `fc.assert(prop, { seed, path })` or the env `FAST_CHECK_SEED`
3. Convert the counterexample into a plain unit test to prevent regression before fixing the bug

### 4. Model-Based And Race Testing

> Goal: test stateful systems and concurrency

1. Use `fc.commands()` for model-based testing — compare model vs real implementation through command sequences
2. Use `fc.scheduler()` / scheduled helpers to detect race conditions in async code
3. Use `it.prop` from `@fast-check/vitest` or the equivalent of your runner for direct integration

### 5. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` to execute the test suite containing the property tests
3. Check the latest official docs at `https://fast-check.dev` before using an uncertain API

## Rules

- Property tests complement unit tests, never replace them — use for pure functions, serializers, and invariants
- Balance `numRuns` between coverage and time (default 100; increase in CI via `fc.configureGlobal` or env `FAST_CHECK_NUM_RUNS`)
- Use a fixed seed in CI for reproducibility — specify `{ seed }` or env `FAST_CHECK_SEED` when replaying a failure
- Compose arbitraries with `.map()`, `.filter()`, `.chain()` instead of writing generators by hand
- Never use deprecated v3 arbitraries (`unicode*`, `ascii*`, `char`, `uuidV`, `.noBias`, `.noShrink`) — removed in v4

- Use `/run-verify` if needed
- Use `/run-test` if needed
- Use `/follow-tool-vitest` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `fast-check` installed as a devDependency and integrated with the project's test runner
- Property tests assert the right invariants with composable arbitraries
- Failures reproduce via `seed`/`path` and counterexamples become regression tests
- Lint, typecheck, tests pass
