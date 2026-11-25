---
name: write-tests
description: Add or update tests by following repo-local test conventions, choosing the right test scope, isolating dependencies, and validating risky paths before delivery. Use when behavior needs regression coverage or release confidence.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Write Tests

Use this skill to author independent, property-verified, contract-driven, and fault-resilient test suites that provide regression protection across microservices and clean architecture backends.

## When to Use

- new business logic, service endpoint, or data transformation requires regression coverage
- practicing Anti-Tautological TDD with independent test authoring and verified Red phase before coding
- verifying structural and mathematical invariants via Property-Based Testing (PBT) with automated shrinking
- establishing Consumer-Driven Contract Testing (CDCT) across HTTP, gRPC, or messaging boundaries
- enforcing Protobuf wire compatibility gates (`buf breaking`) or OpenAPI 3.1 diff validation
- injecting in-test network chaos (latency, jitter, resets) to verify circuit breakers and retries
- testing Go 1.27+ Kratos Clean Architecture services with Testcontainers and transactional rollbacks
- enforcing mutation test kill score thresholds (≥75–80%) on critical packages
- verifying concurrent thread safety, data race freedom (`-race`), and goroutine leak absence
- validating consumer-provider compatibility matrices using Pact Broker `can-i-deploy` prior to release
- generating pairwise combinatorial test matrices to prevent test explosion across multi-parameter services
- authoring deterministic failing reproduction tests during 4-phase systematic root cause analysis

## Core Rules

- **Anti-Tautological TDD & Red-phase verification**:
  - author tests strictly from immutable contracts, schemas, or specs *before* writing code.
  - execute against the baseline codebase to confirm deterministic failure (Red phase).
  - verify failures pinpoint the absence of functionality, preventing false-positive tautologies and test-implementation co-leakage.
  - confirm failure reasons match expected assertion mismatches rather than compilation, syntax, or environmental errors.
- **Property-based invariant testing (PBT)**:
  - verify algebraic and domain invariants: round-trip serialization $f^{-1}(f(x)) = x$, operation idempotency $f(f(x)) = f(x)$, monotonicity, and state machine transitions.
  - use generative engines (`fast-check` for TypeScript, `Hypothesis` for Python, `RapidCheck` for C++).
  - mandate automated counter-example shrinking to isolate minimal reproduction inputs.
- **Consumer-Driven Contract Testing (CDCT)**:
  - author consumer pacts using structural matchers (`like`, `eachLike`, `regex`) via PactV3 rather than brittle static values.
  - verify provider interactions against real service adapters using isolated `ProviderState` setup handlers.
  - enforce Pact Broker `can-i-deploy` verification matrices across environments prior to promotion.
- **Protobuf wire compatibility & schema evolution**:
  - enforce binary wire compatibility and JSON field tag invariance via `buf breaking --against` with `WIRE_JSON` rules.
  - validate REST APIs against breaking contract changes with semantic OpenAPI 3.1 diffs (`oasdiff breaking --fail-on ERR`).
- **In-test chaos & fault injection**:
  - inject network latency, jitter, TCP resets (`reset_peer`), and packet drops via `Shopify/toxiproxy`.
  - assert circuit breaker state transitions (CLOSED $\to$ OPEN $\to$ HALF-OPEN $\to$ CLOSED) under degraded network conditions.
  - verify single-canary probe dispatch in the HALF-OPEN state and graceful fallback handling during the OPEN state.
  - enforce exponential backoff retries with full jitter to eliminate thundering herd problems.
- **Go 1.27+ Kratos Clean Architecture ephemeral test isolation**:
  - enforce 4-layer separation (`api`/`service`/`biz`/`data`); `biz` layer must never leak database handlers (`gorm.DB`) or transport adapters.
  - isolate dependencies via compile-time Wire DI (`TestProviderSet`) injecting real ephemeral repositories.
  - provision real PostgreSQL 18 Alpine containers via `testcontainers/testcontainers-go` with automated Ryuk cleanup.
  - execute table-driven subtests sequentially with GORM `InTx` transactional rollbacks (`tx := db.Begin()`, `t.Cleanup(func() { _ = tx.Rollback() })`) to guarantee zero dirty-state contamination without container restarts.
  - forbid global database instances; pass transactions and connections explicitly via context or repository constructors.
  - detect data races and concurrency hazards via `go test -race` and goroutine leaks via `uber-go/goleak`.
- **Edge case synthesis & boundary testing**:
  - systematically cover boundary cases across numeric extremes (min/max integers, floating-point precision, overflow).
  - test Unicode edge cases (RTL markers, zero-width characters, multibyte strings) and temporal/timezone transitions.
- **Combinatorial test reduction & systematic RCA**:
  - apply pairwise combinatorial testing (`combinatorial-testing`) to compress multi-factor parameter matrices into minimal 2-way covering arrays.
  - follow 4-phase systematic debugging (`systematic-debugging`) to reproduce defects deterministically before authoring fixes.
- **Mutation testing quality gate**:
  - enforce mutation score ≥75–80% using Stryker, mutmut, or cargo-mutants on core domain packages.
  - reject raw line coverage that fails to kill mutants; eliminate surviving non-equivalent mutants by tightening assertions.
- **Testing Trophy & Level 0 air-gapped sandbox**:
  - follow Testing Trophy distribution: heavy integration suites, focused unit tests, and lean E2E verification.
  - stub external HTTP dependencies with MSW v2 or local fixtures; forbid live unmanaged network calls in CI.
  - execute test suites in isolated Level 0 air-gapped sandboxes (`--network=none`, non-root user) per `core/policies/execution-sandbox.md`.
- **AI/LLM feature testing & determinism**:
  - evaluate prompt outputs via structural JSON Schema assertions and calibrated LLM judges (≥85% human agreement).
  - record and replay model responses using VCR cassettes to ensure deterministic CI execution without API flakiness.
- **Deep testing methodologies & reference guides**:
  - advanced testing patterns: [`references/advanced-testing-methodologies.md`](references/advanced-testing-methodologies.md).
  - AI testing and trophy architecture: [`references/patterns-and-ai-testing.md`](references/patterns-and-ai-testing.md).

## Suggested Process

### Step 1: Contract Review & Test Scoping

1. Read the target specification (OpenAPI 3.1, Protobuf, Pact contract, or issue description).
2. Select test scope using the Testing Trophy (unit for pure biz logic, integration for persistence/queries, contract for API boundaries).
3. Confirm whether upstream dependencies provide existing contract definitions or require consumer-driven pact authoring.

### Step 2: Anti-Tautological Test Authoring & Red Phase Verification

1. Author deterministic tests based solely on the specification before modifying implementation code.
2. Run the test suite against the baseline codebase to confirm all new assertions fail deterministically (Red phase).
3. Verify failure output pinpoints missing business functionality rather than compilation, syntax, or environmental issues.

### Step 3: Property Invariants & Ephemeral Container Setup

1. Formulate property-based invariants (round-trip serialization, idempotency, state transitions) using `Hypothesis` or `fast-check`.
2. Configure automated shrinking to ensure failing executions yield minimal reproduction inputs.
3. For Go Kratos data-layer tests, bootstrap an ephemeral PostgreSQL 18 Testcontainer and configure Wire DI test providers (`TestProviderSet`).

### Step 4: In-Test Chaos Fault Injection & Resilience Probing

1. For downstream client integrations, configure Toxiproxy proxies between client and mock/stub services.
2. Inject network latency, jitter, or connection resets (`reset_peer`) to verify circuit breaker trip to OPEN.
3. Confirm fallback response handling and verify single-canary probe recovery to CLOSED upon toxic removal.

### Step 5: Clean Architecture Implementation & Green Phase Verification

1. Author the minimal production code satisfying the specifications according to clean architecture layer rules.
2. Execute the test suite inside the Level 0 sandbox (`--network=none`).
3. Verify all tests pass cleanly without environment contamination or uncommitted state.

### Step 6: Concurrency Safety & Schema Wire Compatibility Verification

1. Run `go test -race` to verify thread safety and race freedom across concurrent flows.
2. Check for goroutine leaks in background worker pools using `uber-go/goleak`.
3. Execute `buf breaking --against` with `WIRE_JSON` and `oasdiff` to verify backward compatibility of API contracts.

### Step 7: Mutation Testing, Coverage Audit & Report Emission

1. Run mutation testing (Stryker / mutmut / cargo-mutants) to verify mutation score ≥75–80%.
2. Eliminate surviving non-equivalent mutants by tightening assertions and covering boundary branches.
3. Emit `test-report.json` with execution details, pass/fail status, coverage, and mutation kill evidence.

## Checklist

- [ ] tests authored independently from spec and verified failing (Red phase) on baseline code
- [ ] property-based tests (PBT) formulated for core data invariants using Hypothesis or fast-check
- [ ] automated shrinking counter-examples verified for failing property test runs
- [ ] consumer contracts verified with PactV3 structural matchers (like, eachLike, regex)
- [ ] provider verification executed with isolated ProviderState handlers and can-i-deploy release checks
- [ ] Protobuf wire compatibility gates verified via buf breaking --against with WIRE_JSON rules
- [ ] in-test chaos injected via Toxiproxy (latency, jitter, resets) verifying circuit breaker trip and recovery
- [ ] single-canary probe dispatch verified during circuit breaker HALF-OPEN state transition
- [ ] Go 1.27+ Kratos clean architecture tested with Testcontainers PostgreSQL 18 and Wire DI isolation
- [ ] table-driven subtests isolated sequentially using GORM InTx transactional rollbacks with zero dirty state
- [ ] data race detector passes cleanly via go test -race and goroutine leaks verified absent with goleak
- [ ] edge case synthesis applied across numeric boundaries, Unicode, timezones, and null states
- [ ] mutation testing executed with kill score meeting or exceeding ≥75–80% threshold
- [ ] tests executed inside isolated Level 0 air-gapped sandbox (--network=none, non-root user)
- [ ] test-report.json emitted and validated against contracts/schemas/test-report.json

## Red Flags

| Rationalization Thought | Positive Corrective Action |
|---|---|
| "Too simple to need a Red-phase test first." | Author the spec-derived test first and watch it fail on baseline before editing production code. |
| "I'll write the tests after the implementation works." | Tests written after mirror code bugs; derive assertions from the contract first. |
| "100% line coverage proves assertions are strong." | Run mutation testing or verify negative paths actually fail when invariants break. |
| "Mocking the core service makes this test faster." | Keep mocks strictly at external I/O boundaries; exercise real business logic and state mutations. |

## Output Contracts

When executing or updating automated tests for behavior verification, emit:

- **`contracts/schemas/test-report.json`** — Documents test suite configurations, pass/fail execution results, mutation scores, coverage metrics, and identified test failures. Set `produced_by_role` to the executing role.

Skip emission for rapid local test iterations during interactive development.

## Failure Modes

- **Tautological / co-leaked tests**: author writes implementation and assertions together, mirroring faulty assumptions. Mitigation: enforce independent specification-based test authoring and mandatory Red-phase failure verification.
- **Coverage theater without mutation testing**: 100% line coverage masking absent or weak assertions. Mitigation: enforce mutation score ≥75–80% on critical packages.
- **Database dirty-state contamination**: subtests pollute shared database tables, causing flaky sequential failures. Mitigation: enforce GORM `InTx` uncommitted transactional rollbacks per subtest with Testcontainers PostgreSQL 18.
- **Unverified circuit breaker failure**: downstream service times out but client blocks indefinitely due to missing chaos testing. Mitigation: inject Toxiproxy latency and reset toxics in CI integration tests.
- **Silent Protobuf wire drift**: schema changes alter wire tag numbering or JSON transcoding fields, breaking microservice consumers. Mitigation: execute `buf breaking --against` with `WIRE_JSON` in CI.
- **Swallowed goroutine leaks**: unmanaged background workers remain active after test teardown, corrupting subsequent runs. Mitigation: enforce `uber-go/goleak` in test cleanup.
- **Live external network calls in CI**: tests query third-party APIs directly, causing flaky builds. Mitigation: enforce Level 0 airgap (`--network=none`), MSW v2, and VCR fixtures.
- **Flaky sleep-based waits**: tests rely on arbitrary sleep intervals. Mitigation: replace sleeps with explicit polling, channel synchronization, and condition watchers.

## Security Guardrails (OWASP ASI)

- **ASI01 Agent Goal Hijack**: cross-check test assertions against source spec to prevent locking in unintentional drift or malicious scope changes.
- **ASI04 Agentic Supply Chain**: validate test fixtures, VCR cassettes, and mocking libraries against project manifests; reject untrusted test packages.
- **ASI05 Unexpected Code Execution**: test suites must run inside an isolated sandbox per `core/policies/execution-sandbox.md` without root privileges.
- **ASI07 Insecure Inter-Agent Communication**: emit structured `test-report.json` for CI and reviewer verification.
- **ASI09 Human-Agent Trust Exploitation**: surface skipped tests, surviving mutants, and mock fidelity limitations transparently.

## Related Skills

- **commit-code**: Prepare test changes for delivery
- **review-service**: Check whether coverage is sufficient for release risk
- **troubleshoot-service**: Debug failing or flaky tests
- **review-code**: Review whether tests match the change risk
- **navigate-service**: Understand the target flow before adding tests
- **systematic-debugging**: Formulate root-cause hypotheses and author deterministic reproduction tests
- **combinatorial-testing**: Generate pairwise covering arrays to optimize multi-parameter test matrices
