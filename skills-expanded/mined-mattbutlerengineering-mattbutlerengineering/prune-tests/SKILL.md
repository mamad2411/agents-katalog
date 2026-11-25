---
name: prune-tests
description: Review one test file for practical value and pruning opportunities. Use when the user asks to prune tests, assess test usefulness, find low-value redundancy, reduce internal mocking, or detect out-of-sync tests. Read-only; returns categorized findings with a conservative must-keep group. Invoke with /prune-tests <test file>.
disable-model-invocation: true
---

# Prune Tests

Review a single test file and identify where it can be simplified without losing meaningful behavioral protection.

Adapted from [mattpocock/skills#364 (comment)](https://github.com/mattpocock/skills/issues/364#issuecomment-4892158727) for this repo's Vitest and Playwright suites.

## Scope

- One test file per invocation (`*.test.ts`, `*.test.tsx`, `*.test.mjs`, or `e2e/*.spec.ts`). Asked for a directory or package, list its test files and ask which one to start with.
- **Read-only.** The output is a review. Delete, merge, or rewrite tests only after the user picks findings to apply, and then follow the [Applying findings](#applying-findings) rules.

## Goal

Produce a practical pruning review that:

- prioritizes behavior over implementation details,
- pushes tests away from mocking internal systems when real integration is cheap,
- highlights redundant scenarios with weak incremental value,
- flags tests that no longer match current behavior or naming,
- keeps a conservative group of tests that should remain even when pruning.

## Review Workflow

1. Read the target file fully, then read the source it tests. A test cannot be judged stale or redundant without the current behavior in view.
2. Identify each test's primary behavior contract in one sentence.
3. Group tests by overlap and unique signal.
4. Run a scenario-boundary check before recommending merges:
   - merge tests within the same scenario class (expected use case, edge case, or failure case),
   - merge tests with matching business preconditions (for example: zero-deposit with zero-deposit, fully-booked with fully-booked, admin role with admin role),
   - suggest `merge` when the behavior contract, setup meaning, and outcome type are effectively the same.
5. Re-check recommendations against the repo's test conventions ([AGENTS.md § Testing & Validation](../../../AGENTS.md#testing--validation) and the package's own `CLAUDE.md`):
   - preserve focused tests and "one logical assertion per test" intent,
   - prefer keeping separate tests for distinct behavioral contracts even if setup looks similar.
6. Evaluate mocking strategy:
   - prefer real collaborators for internal systems (service functions, Zod schemas, Fastify routes through `buildApp()` + `app.inject()`, rialto components rendered for real, React Query hooks behind a real `QueryClient`) when practical,
   - keep mocks for external boundaries (network, Stripe, Auth0, Sentry, the clock and randomness only when needed, expensive side effects).
7. Detect out-of-sync indicators:
   - test name says one behavior but assertions prove another,
   - Given/When/Then comments contradict setup/assertions,
   - assertions validate old payload shapes or status contracts no longer used,
   - test intent duplicates newer canonical tests but with stale assumptions.
8. Check whether the test is a named pin. Search `.claude/rules/gotchas*.md`, `docs/adr/` and `docs/fixes/` for the file's basename. A test those documents cite ("pinned by `<test>`") goes in category 5 regardless of how it looks.
9. Return categorized findings with explicit prune confidence.

## Scoring Heuristics

Use these signals to estimate value:

- **High value**: protects a unique business rule, cross-layer contract, permission boundary, backward compatibility, or regression-prone edge case.
- **Medium value**: valid scenario but partially overlaps stronger coverage.
- **Low value**: mostly implementation-detail checks, duplicate setup/assertions, fake-concurrency tests, brittle timing checks, assertions that cannot fail, or stale semantics.

## Required Output Categories

Always return findings in these categories and keep this order:

1. **Low Value Likely Prune**
2. **Consolidate Or Rewrite**
3. **Mocking Improvements (Less Internal Mocking)**
4. **Out Of Sync Tests**
5. **Keep Even If Pruning Conservatively**

For every listed test include:

- test name,
- why it belongs in that category,
- confidence (`high`, `medium`, `low`),
- suggested action (`remove`, `merge`, `rename`, `rewrite with real collaborator`, `keep`).

## Category Guidance

### 1) Low Value Likely Prune

Place tests here when they add little unique confidence:

- timing/perf threshold tests in normal CI suites,
- duplicate assertion sets over the same behavior,
- pseudo-concurrency checks without a concrete race boundary,
- tests proving library behavior (Prisma, Zod, React, Fastify) rather than domain behavior,
- assertions that can never fail (asserting a mock returns what it was told to return, `expect(true).toBe(true)`, a `toBeDefined()` on a value the line above constructed).

### 2) Consolidate Or Rewrite

Place tests here when intent is useful but shape is inefficient:

- same behavior tested through multiple near-identical examples (candidate for `it.each`),
- naming/intent mismatch,
- split tiny tests that should be one clear scenario,
- can be represented by one stronger integration path.
- If scenarios are different but both valuable, prefer `rewrite` or `rename` over `merge`.

### 3) Mocking Improvements (Less Internal Mocking)

Call out tests that mock internals where real objects are better:

- `vi.mock()` of a sibling module in the same package when the real module is cheap to run,
- mocked auth/permission or query internals in integration files,
- heavy stubbing that hides true data flow,
- assertions on mock call counts or argument shapes standing in for an observable result.

Recommend replacing with:

- real fixtures and factories,
- real service calls,
- the request path (`app.inject()`) where the file's scope is integration,
- user-visible queries (`getByRole`, `getByLabelText`) over component internals.

### 4) Out Of Sync Tests

Flag tests likely stale relative to codebase behavior:

- test name contradicts expected outcome,
- expected response/status shape appears outdated,
- comments and assertions disagree,
- legacy assertions no longer tied to active contracts.

### 5) Keep Even If Pruning Conservatively

This is the anti-over-pruning group.

Include tests that should remain because they protect:

- critical business invariants,
- permission/security boundaries,
- compatibility wrappers and migration safety,
- domain edge cases with real user impact,
- end-to-end integration contracts across layers,
- a past incident: any test cited by a gotcha, ADR, or fix doc, or whose name or comment references an issue number.

## Constraints

- Be conservative by keeping low-confidence deletion candidates as `keep` or `rewrite`.
- Prefer merge/rename/rewrite before remove when the behavior contract is still useful.
- Recommend merges for equivalent business scenarios and matching behavior contracts.
- When scenario equivalence is uncertain, choose `keep` (or `rewrite`) guidance.
- Focus pruning recommendations on behavioral value and contract signal.
- Keep recommendations actionable and file-specific.

## Applying findings

Only when the user asks to apply specific findings:

- Apply `high`-confidence findings only, unless the user names others.
- Run the file's suite before and after from inside its package directory (`pnpm vitest run <file>`), and report both counts.
- Coverage must stay at or above the package threshold. A removal that drops it means the test carried unique signal; restore it and move the finding to category 5.
- One test file per commit, `test:` type, with the removed and merged test names in the body.
