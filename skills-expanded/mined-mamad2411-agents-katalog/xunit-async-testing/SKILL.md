---
name: xunit-async-testing
description: Use when xUnit tests must verify asynchronous behavior, cancellation, exception flow, and concurrency outcomes with deterministic assertions.
---

# xUnit Async Testing

## Specialization

Use this skill to design robust async xUnit tests that avoid deadlocks, race-sensitive flakiness, and weak cancellation assertions.

This skill is specialized for async and concurrency test behavior in xUnit.

## Objective

Produce a deterministic async-testing design package that defines await discipline, cancellation checks, exception assertions, and concurrency safety boundaries.

## Trigger Conditions

- Target behavior includes `Task`, `ValueTask`, or async streams.
- Tests are flaky due to timing or concurrency sensitivity.
- Cancellation and async exception paths are currently untested.

## Scope Boundaries

In scope:

- Async assertion design and await discipline.
- Cancellation token behavior and timeout posture.
- Exception-flow assertions for async methods.
- Concurrency-sensitive test boundaries and isolation controls.

Out of scope:

- Production-threading architecture design.
- Benchmarking throughput or latency.
- Non-xUnit async test frameworks.

## Inputs

- Async behavior contracts and expected cancellation semantics.
- Scheduler/time dependencies and external side effects.
- Failure modes and known flaky behavior.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.

## Required Outputs

- Async behavior-to-assertion matrix.
- Cancellation test contract.
- Async exception verification plan.
- Concurrency risk and stabilization controls table.
- Final recommendation with residual risk statements.

## Deterministic Workflow

1. Identify async behavior contracts, including completion and cancellation expectations.
2. Define explicit await strategy for each test path.
3. Map cancellation semantics into deterministic assertions.
4. Design exception assertions for async failure paths.
5. Identify concurrency-sensitive areas and isolation controls.
6. Remove timing-dependent assertions that do not encode behavior intent.
7. Publish one recommendation with unresolved risks.

## Decision Rules

- Always await the operation under test to capture true async outcomes.
- Prefer behavior assertions over elapsed-time assertions.
- Assert cancellation using expected cancellation contract, not generic failure.
- Keep async tests single-purpose to improve diagnosis under failure.

## Anti-Pattern Checks

- Fire-and-forget operations without observation.
- `Thread.Sleep`-based assertions.
- Assertions tied to non-deterministic scheduling order.
- Timeout values used as behavior proof instead of guardrails.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Expert async test design | Deterministic Workflow |
| Deterministic cancellation coverage | Decision Rules + Required Outputs |
| Concurrency flake reduction | Anti-Pattern Checks |
| Cross-project reusability | Scope Boundaries + Pragmatic Stop Rule |

## Reasoning Package

Assumptions:

- Async correctness requires explicit observation of completion, cancellation, and exception contracts.
- Most async flakiness comes from timing-based assertions and hidden shared state.

Trade-offs:

- Stricter async assertions improve reliability but increase test authoring effort.
- Broader concurrency coverage catches more defects but can increase test runtime.

Open blockers:

- Unspecified cancellation semantics reduce assertion precision.
- Hidden thread-affinity dependencies can invalidate otherwise correct async tests.

Recommendation:

- Encode async behavior as explicit contracts in tests and ban timing-only evidence for correctness decisions.

## Source Governance Summary

- Active sources and evaluation status are tracked in [source-catalog.md](./references/source-catalog.md).

## Pragmatic Stop Rule

Stop when each async behavior has one explicit completion assertion, one cancellation decision (if applicable), and one exception-path check.

## Done Criteria

- Trigger conditions are satisfied.
- Required outputs are complete.
- Async decision logic is explicit.
- Source catalog is current for this evaluation cycle.
