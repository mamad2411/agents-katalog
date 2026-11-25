---
name: test-strategy
description: Decide what should be tested, at which seam, and at which level before or during implementation. Use when implementing a meaningful feature, creating or changing tests, building a behavior test-first, touching payment/auth/data-integrity logic, when a review finds insufficient verification, or when the user asks what needs testing. For an unexplained failure or regression, load `systematic-debugging` first to find the cause, then this skill to cover the fix.
---
# Test Strategy

## Principle

Risk-driven, not coverage-driven. Do not optimize for test count or arbitrary coverage percentages.

## Seams

A seam is the public boundary you observe behavior through, without reaching inside the implementation. Tests live at seams, never against internals.

**Name the seams before writing any test, and confirm them.** Everything cannot be tested, so agreeing the seams first is how effort lands on critical paths and complex logic instead of scattered edge cases. For each proposed seam, state in one line what it catches and what it misses.

Prefer existing seams. Where the shape of an interface is itself in question, that is a design question for `architecture-review`, not a testing decision.

## What makes a test worth keeping

A good test reads like a specification and survives refactoring, because it does not care about internal structure. Code can change entirely; the test should not break when behavior is unchanged.

Expected values must come from an independent source of truth: a known-good literal, a worked example, or the stated requirement.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel such as querying the database instead of using the interface. The tell is a test that breaks during refactoring while behavior did not change.
- **Tautological**: the assertion recomputes the expected value the way the code does, so it passes by construction and can never disagree with the implementation. If the test restates the formula, it proves nothing.
- **Horizontal slicing**: writes every test first, then every implementation. Bulk tests verify imagined behavior, go insensitive to real change, and commit to structure before understanding the implementation.

Work in vertical slices instead: one failing test, the smallest implementation that passes it, then the next. Each slice is a tracer bullet that responds to what the previous one taught you.

## Choose the right level

- Unit: pure logic, calculations, validation, transformations, state transitions.
- Integration: real module boundaries, database queries, service calls, transactions.
- Contract: request/response shapes and consumer expectations between components or teams.
- API: routing, auth, validation, status codes, and error contracts on endpoints.
- End-to-end: critical user journeys only, kept few and stable.
- Smoke: post-change or pre-release confidence that the app still starts and core paths work.
- Manual QA: flows automation cannot judge reliably, such as visual layout, device behavior, or third-party dashboards.
- Regression: previously fixed defects that must stay fixed.

## Identify what to cover

- Happy paths.
- Edge cases: boundaries, empty and maximum values, ordering, timezones, encoding.
- Invalid input: malformed, oversized, unexpected types, and hostile input.
- Permission boundaries: unauthorized, wrong role, and cross-user access.
- Failure and retry behavior: timeouts, partial failure, retries, and recovery.
- Concurrency where relevant: races, parallel writes, ordering guarantees.
- Duplicate events and webhooks where relevant: idempotency and replay.
- Rollback and recovery where relevant for risky flows.

## The loop, when a behavior change warrants it

1. Write a failing test that asserts the required behavior.
2. Confirm it fails for the intended reason, not an incidental one.
3. Write the smallest implementation that makes it pass.
4. Refactor with the test green throughout.

Do not anticipate future tests or add speculative support for cases not yet required.

## Distinguish kinds of verification

A regression test, a build check, a static check, and manual runtime verification are different things. State which one actually ran. A green build is build evidence only; it does not demonstrate behavior.

When automation is impractical, document the exact manual steps and their limits rather than implying coverage.

## Rules

- Match the project's existing test framework, file layout, and naming; do not introduce a second framework without a reason.
- Test observable behavior and contracts, not private implementation details.
- Keep tests deterministic; control time, randomness, network, and ordering.
- Do not weaken or delete an existing test to make a suite pass; fix the cause with `systematic-debugging` when a test fails for the wrong reason.
- Do not write tests against production or shared resources. Skip unsafe tests and say so.
- Keep real customer data and credentials out of fixtures. Use synthetic values that preserve the shape.
- Do not create a large testing framework for trivial work.
- Prefer a few high-value tests over many shallow ones.

## Reporting

State the seams chosen and why, which levels were chosen and why, what was added or changed, what was deliberately not covered, and the exact commands that were run with their observed outcomes. Never claim coverage or passing tests without executing them.
