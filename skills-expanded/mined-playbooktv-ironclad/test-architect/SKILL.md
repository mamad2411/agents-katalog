---
name: test-architect
description: Design a test strategy around product risk, business invariants, failure modes, and existing controls, deciding what deserves testing and at which boundary rather than maximising coverage. Use whenever the user asks how to test something, wants a test plan or strategy, is deciding between unit/integration/contract/E2E/property/concurrency testing, or wants to know whether existing tests actually protect what matters. Prefer this over writing tests immediately. Part of the audit suite; inherits the shared constitution while its own job is proving risk coverage.
---

# Test Architect

**Epistemology: prove risk coverage, not line coverage.**

Coverage percentage is supporting information, never the objective. A suite can be 95% covered and still fail to protect the workflow that loses money, corrupts data, crosses tenants, or strands users.

Read `references/CONSTITUTION.md` first.

This skill's output is a defensible test architecture. Its evidence is the chain:

**product context → critical workflows → invariants → failure modes → risk → existing controls → test gaps → appropriate proof boundary**

## Phase 0: Product and failure context

Establish:

- what the system does;
- who uses it;
- critical workflows;
- sensitive data;
- financial or irreversible actions;
- availability expectations;
- contractual/compliance constraints where known;
- historical incidents and regressions;
- deployment architecture and independently deployed components.

If context is unclear, infer from repository and documentation, then ask only about material unknowns.

## Phase 1: Existing-suite archaeology

Before proposing tests, inspect what already exists.

Map:

- test frameworks and runners;
- unit, integration, contract, E2E, accessibility, visual, property, concurrency, and manual coverage;
- fixtures, factories, seed data, mocks, fakes, and test containers;
- CI placement and release gates;
- flake/retry policy;
- parallelism and isolation;
- production-like boundaries available;
- historical regressions already encoded.

Assess test quality, not just quantity.

Flag:

- tests coupled to implementation details;
- assertions that cannot fail meaningfully;
- mocks that bypass the actual risk;
- snapshots without a stable contract;
- arbitrary sleeps;
- shared mutable state;
- unrealistic fixtures;
- E2E tests duplicating lower-level proof;
- green tests that ignore real dependency contracts.

## Phase 2: Build the hierarchy top-down

### 1. Critical workflows

Identify the handful of end-to-end paths the product exists to deliver.

### 2. Business and system invariants

State rules that must hold, such as:

- a logical payment is charged at most once;
- a booking cannot be double-sold;
- acknowledged writes survive refresh;
- one tenant cannot access another tenant's resource;
- retries do not duplicate side effects;
- failed submission preserves recoverable input;
- published data retains ownership and attribution.

### 3. Failure modes

For each workflow/invariant consider:

- malformed input;
- boundary values;
- dependency failure;
- timeout;
- retry;
- duplicate delivery;
- concurrency;
- stale state;
- out-of-order events;
- partial completion;
- permission failure;
- migration/version skew;
- empty/large/unusual data;
- clock/timezone boundaries;
- cache inconsistency.

## Phase 3: Risk model

Rate candidate risks using:

- **Impact** — user harm, financial loss, data loss, security, contractual exposure.
- **Likelihood** — frequency and reachable conditions.
- **Detectability** — whether failure is noticed before harm.
- **Existing controls** — constraints, transactions, policy, tests, monitoring, rollback.

Do not turn scoring into fake precision. Use it to explain priority.

`NOT WORTH TESTING` is a legitimate outcome for low-value risks, but state why and what assumption supports the decision.

## Phase 4: Map existing protection

For each risk record:

- invariant/failure mode;
- current test or control;
- boundary exercised;
- what the current protection actually proves;
- gaps;
- false-confidence risks.

A unit test for a repository mock does not prove a database constraint. An E2E happy path does not prove idempotency under retry.

## Phase 5: Choose the cheapest boundary that can prove the behaviour

- **Unit** — pure logic and local invariants.
- **Integration** — database, cache, framework, persistence, and module seams.
- **Contract** — independently deployed consumer/provider compatibility.
- **E2E** — a small number of critical cross-system user journeys.
- **Property-based** — invariants over broad input spaces.
- **Concurrency** — ordering, idempotency, locking, lost updates, duplicate delivery.
- **Fault injection / chaos** — controlled dependency failure and recovery.
- **Accessibility** — semantic and interaction behaviour.
- **Visual regression** — stable visual contracts, not indiscriminate pixel policing.
- **Manual exploratory** — judgement-heavy or uneconomic-to-automate risks.

Do not duplicate the same assertion at every layer without a reason.

## Phase 6: Build the gap matrix

Produce:

`Risk → Invariant → Existing protection → Gap → Recommended proof → Level → Priority → CI placement`

Prioritise by risk reduction per unit effort.

Suggested sequence:

- **P0:** release-blocking invariants and critical boundaries;
- **P1:** high-value regression protection;
- **P2:** structural confidence and contracts;
- **P3:** optional breadth and lower-risk cases.

## Phase 7: Test architecture

Define:

- fixture/factory strategy;
- seed and data ownership;
- isolation and cleanup;
- deterministic clocks/randomness;
- parallel execution;
- dependency simulation;
- production-like integration boundaries;
- E2E environment;
- contract ownership;
- flake policy;
- retry policy;
- CI stages and release gates;
- manual exploratory cadence.

Avoid using retries to hide flaky tests.

## Phase 8: Implementation rules

When authorised:

- write failing regression tests first for confirmed bugs where practical;
- test behaviour and invariants, not private implementation;
- use the real boundary when that boundary is the risk;
- avoid arbitrary sleeps when events/state conditions can be awaited;
- coordinate concurrency tests deliberately;
- keep E2E journeys few and high-value;
- redact secrets and personal data;
- make failure output diagnosable.

## Phase 9: Confidence review

Ask of each important test:

> If the protected behaviour were broken, would this test actually fail?

Where tooling and value justify it, use mutation testing selectively on critical pure logic or policy code.

Review whether green tests can coexist with:

- broken integration;
- contract drift;
- missing authorization;
- duplicate side effects;
- stale caches;
- flaky timing;
- unrealistic fixtures.

## Report format

```markdown
# Test Strategy — [system/feature]

**Declared scope:** [...]

## Product risk model
[Critical workflows, invariants, failure modes, and prioritisation logic.]

## Existing suite assessment
[What exists, what it proves, and false-confidence risks.]

## Gap matrix
| Risk | Invariant | Existing protection | Gap | Recommended proof | Level | Priority | CI stage |

## Test architecture
[Fixtures, isolation, determinism, environments, contracts, flake policy.]

## Implementation backlog
[P0 → P3]

## Deliberately not tested
[Risks judged not worth the cost, with rationale and assumptions.]

## Coverage note
[Coverage numbers, if discussed, are supporting information only.]

## Residual untested risk
[What remains outside proof and why.]
```

## Anti-patterns

- Coverage worship.
- Test inflation.
- Wrong-level testing.
- Testing the easy instead of the important.
- Proposing tests without inspecting the existing suite.
- Mocking away the boundary under risk.
- Retry-based flake concealment.
- Snapshot accumulation without stable contracts.
- E2E monoculture.
- Fake precision in risk scoring.
- Green-suite confidence without asking what failures can still pass.
