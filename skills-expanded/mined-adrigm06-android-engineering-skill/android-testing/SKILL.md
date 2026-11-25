---
name: android-testing
description: Android testing strategy skill for unit, integration, UI, screenshot, contract, macrobenchmark, and baseline profile planning. Use this when users ask what to test, how much to test, or how to reduce flaky test suites.
---

# Purpose

Define risk-weighted Android testing strategy that maximizes confidence under cost, speed, and maintainability constraints.

## Scope and authority

This skill is lead authority for verification depth, confidence strategy, and flakiness controls.

Supporting interactions:

- defer production ship/no-ship to `android-release-engineering`
- align boundary-sensitive coverage with `android-architecture`
- coordinate runtime/perf validation with `android-performance`

## When to use

- defining test strategy for new modules/features
- recovering from flaky CI suites
- selecting minimum viable coverage under deadlines
- hardening refactor and migration confidence

## Decision engine workflow

1. Identify business-critical and failure-prone journeys.
2. Classify risk by impact, probability, and detectability.
3. Allocate test depth per layer by ROI.
4. Design deterministic data and environment controls.
5. Stage rollout and gate criteria by release risk.

## Branching decision tree

### Branch A: delivery context

- `deadline-critical`:
  - prioritize high-risk integration and contract tests
  - defer lower-value UI coverage with explicit follow-up date
- `stability-critical`:
  - increase integration and failure-path depth
  - tighten flaky-test budget and quarantine policy

### Branch B: architecture maturity

- `legacy-coupled`:
  - add characterization tests before deep refactor
- `modular and bounded`:
  - bias toward fast unit + boundary-focused integration tests

### Branch C: UI strategy

- if UI churn is high:
  - use focused behavior tests, avoid brittle screenshot overuse
- if visual fidelity is contractual:
  - add disciplined screenshot review workflow

## Quantitative gates

Use measurable gates and label each `pass | at-risk | fail`:

- critical-flow coverage gate (required behavior paths covered)
- flaky-rate gate (suite-level instability budget)
- execution-time gate (CI viability budget)
- regression-detection gate (failure-path and contract-test coverage on high-risk boundaries)

If coverage and flake baselines are missing, return a measurement-first stabilization plan.

## Tradeoff realism

Accept "imperfect but justified" decisions when explicit:

- temporary test debt is acceptable with owner, deadline, and risk cap
- selective retries may be acceptable while fixing root-cause flakiness

Never normalize persistent flaky failures as expected behavior.

## Uncertainty protocol

Always report confidence:

- `High` (>= 0.80)
- `Medium` (0.60-0.79)
- `Low` (< 0.60)

If confidence is medium/low:

- state assumptions and unknowns
- provide at least one lower-risk fallback
- request minimum extra evidence (failure stats, flaky rate, risk incidents)
- escalate to `android-release-engineering` when unresolved risk affects go/no-go

## Cross-skill handoff payload

Use the standard payload defined in `../../AGENTS.md` (section: Cross-skill handoff contract).
Set `requesting_skill` to `android-testing`.

## Output contract

Follow the global section order from `../../AGENTS.md`:

1. `Context and constraints`
2. `Decision and rationale`
3. `Alternatives considered`
4. `Tradeoffs`
5. `Risks and mitigations`
6. `Confidence and unknowns`
7. `Cross-skill impacts`
8. `Next implementation steps`

Also include:

- `Test pyramid recommendation`
- `Test boundaries by layer`
- `What not to test`
- `Flakiness risks and controls`
- `Performance test additions`

## Anti-pattern detection

- excessive UI tests for risks coverable at lower layers
- tests asserting implementation details over behavior/contracts
- nondeterministic test inputs (time/network/randomness)
- missing failure-path coverage on high-impact journeys

## Related resources

- `templates/test-strategy.md`
