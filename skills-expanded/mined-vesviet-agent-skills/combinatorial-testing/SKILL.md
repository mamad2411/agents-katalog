---
name: combinatorial-testing
description: Design pairwise and n-way combinatorial test suites using orthogonal arrays and covering parameter matrices to prevent combinatorial explosion. Use when testing multi-parameter workflows, distributed configurations, or cross-service API contracts.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Combinatorial Testing

Use this skill to design, reduce, and generate pairwise and n-way combinatorial test matrices using PICT/PyPICT algorithms and orthogonal arrays across multi-parameter systems.

## When to Use

- system under test accepts multiple interacting parameters, headers, flags, or configuration permutations
- full Cartesian product testing is infeasible due to exponential combinatorial explosion ($V^N$)
- testing distributed microservice interfaces with variable protocols, payload encodings, and network states
- designing comprehensive test matrices for API endpoints, search filters, or multi-step checkout forms
- validating complex business logic where failures typically emerge from unforeseen two-way parameter interactions
- isolating multi-factor race conditions in distributed event streaming and message brokers
- verifying complex form validation rules with interdependent field state transitions
- verifying cross-platform, browser viewport, operating system, and localization compatibility permutations
- auditing authorization engines with multi-attribute role, tenant, resource, and permission matrices
- optimizing database query parameter combinations and indexing filter paths for query planners
- verifying cloud deployment matrix variants across regions, runtime versions, and worker instance types

## Core Rules

- **Pairwise Coverage Invariant (2-Way Interaction Principle)**:
  - every valid pair of parameter values must be covered by at least one test case in the test matrix ($t=2$ guarantee).
  - rely on NIST empirical findings: pairwise covers 70–84% of all software defects; 3-way covers >95%.
  - reject naive Cartesian products ($O(V^N)$) that cause test suite bloat and slow CI feedback loops.
  - achieve logarithmic reduction: compress thousands of raw permutations into dozens of high-signal test cases.
- **Mathematical Covering Array Representation ($CA(N; t, k, v)$)**:
  - represent matrices as covering arrays where $N$ is test suite size, $t$ is interaction strength, $k$ is parameters, and $v$ is values.
  - generate mixed-level covering arrays when factors possess varying numbers of levels.
  - escalate interaction strength to $t=3$ or $t=4$ on financial transactions, cryptography, and safety-critical controls.
- **Seed Row Preservation & Golden Journeys**:
  - inject critical business workflows, compliance mandates, and golden journeys as explicit seed rows into the model.
  - guarantee that reduction algorithms preserve required paths while optimizing remaining parameter combinations.
- **Determinism and Pseudorandom Seed Invariance**:
  - set fixed random seeds in covering array generators so that matrix generation is completely reproducible across CI builds.
  - reject non-deterministic generators that produce differing test matrices across identical runs.
- **Rigorous Parameter Equivalence Partitioning**:
  - partition continuous domains into discrete equivalence classes: nominal, boundary min/max, null/empty, invalid.
  - avoid redundant equivalence values that inflate matrix size without increasing fault detection coverage.
  - isolate domain boundaries (e.g., $0$, $1$, $2^{31}-1$, string lengths, special characters) into distinct levels.
- **Constraint Definition & Model Integrity**:
  - declare explicit constraints for mutually exclusive or conditionally dependent parameter values.
  - forbid impossible combinations that generate invalid runtime states or distort test metrics.
  - verify that constraints do not accidentally eliminate valid boundary conditions from the test matrix.
- **Single-Fault Negative Parameter Isolation**:
  - test invalid/error-triggering parameter values strictly one at a time across baseline nominal combinations.
  - prevent error-masking phenomena where one invalid parameter hides bugs in adjacent parameter parsers.
  - group negative test rows separately from the valid pairwise interaction covering array.
- **Algorithmic Reduction over Ad-Hoc Sampling**:
  - generate test suites using algorithmic covering arrays (PICT, PyPICT, or orthogonal arrays); never guess combinations.
  - analyze pairwise coverage efficiency to detect sub-optimal factor combinations.
- **Data-Driven Test Implementation**:
  - map reduced combinatorial matrix rows directly into table-driven test fixtures in Go, Python, or TypeScript.
  - ensure test oracles verify both return payloads and stateful persistence side effects for each row.
- **Deep Reference Guide**:
  - advanced matrix verification and review criteria: `core/roles/references/qa-engineer-review-checklist.md`.

## Suggested Process

### Step 1: Interface Analysis & Parameter Extraction
1. Review target interface specifications (OpenAPI 3.1, Protobuf, function signatures, or configuration schemas).
2. Catalog all independent input variables, request headers, environmental conditions, and state flags.
3. Identify system variables that interact during execution (e.g., AuthType, PayloadFormat, Transport, CacheMode).
4. Distinguish independent factors from dependent or calculated values to prevent redundant dimensions.
5. Document the default baseline values for each parameter to serve as stable anchors for negative tests.

### Step 2: Equivalence Partitioning & Boundary Selection
1. Partition each parameter into representative discrete values: nominal, boundary limits, empty, and invalid.
2. Ensure values represent distinct behavioral branches rather than redundant cosmetic variants.
3. Select concrete boundary data instances (e.g., min length, max length, UTF-8 multibyte, null pointer).
4. Verify that each equivalence class tests a unique branch or validation check in the implementation.
5. Validate that continuous numerical ranges are partitioned into minimum, nominal, and maximum threshold points.

### Step 3: Constraint Definition & Model Construction
1. Identify business rules governing parameter interactions (e.g., Protocol=gRPC requires Transport=HTTP/2).
2. Author the combinatorial model in PICT format declaring parameters, values, and conditional constraints.
3. Review constraints to verify they reflect legitimate domain invariants rather than artificial test simplifications.
4. Audit constraint logic to ensure valid edge combinations are not unintentionally pruned.
5. Add explicit conditional rules using `IF ... THEN ... ELSE` clauses to model strict business rules.

### Step 4: Covering Array Generation ($t=2$ Reduction)
1. Run PICT or PyPICT with interaction strength order $t=2$ (pairwise) or $t=3$ for safety-critical pathways.
2. Supply seed test cases to guarantee coverage of standard smoke journeys and critical happy paths.
3. Verify the generated matrix achieves 100% 2-way interaction coverage across all non-constrained parameter pairs.
4. Calculate matrix reduction metrics: compare generated rows against full Cartesian product size.
5. Inspect the generated matrix rows to confirm that all parameter values appear at least once.
6. Record interaction coverage metrics to substantiate test release confidence statements.

### Step 5: Single-Fault Negative Test Case Generation
1. Author explicit negative test rows pairing one invalid parameter value with all nominal valid parameters.
2. Ensure negative tests execute independently to prevent error masking between validation layers.
3. Assert that appropriate HTTP 4xx, gRPC status codes, or domain validation errors are raised.
4. Verify that error responses contain structured error envelopes rather than unhandled server panics.

### Step 6: Executable Table-Driven Test Suite Implementation
1. Transform generated matrix rows into executable data-driven test cases (Go table subtests, pytest parametrize, Vitest each).
2. Construct descriptive subtest names reflecting the parameter tuple (e.g., `test_auth_jwt_payload_json_transport_http2`).
3. Implement explicit pass/fail assertion oracles verifying return payloads, error envelopes, and side effects.
4. Tag test cases with parameter metadata and row identifiers for clear failure reporting and traceability.
5. Verify that test harness execution isolates test state between consecutive parameter tuples.
6. Implement automated cleanup handlers to reset global or database fixtures after each row.

### Step 7: Test Execution, Telemetry Audit & Report Emission
1. Execute the generated combinatorial test suite inside the isolated Level 0 sandbox environment.
2. Collect execution results, identifying any failing parameter interactions for systematic debugging.
3. Emit `test-report.json` capturing matrix dimensionality, reduction ratio, and test outcomes.
4. Document surviving parameter interactions that require higher-order $t=3$ investigation.

## Checklist

- [ ] input parameters, headers, and environment variables cataloged across target interface
- [ ] parameter domains partitioned into valid equivalence classes, boundaries, and negative states
- [ ] inter-parameter constraints modeled to eliminate impossible or conflicting value combinations
- [ ] pairwise covering array generated via PICT/PyPICT achieving 100% 2-way interaction coverage
- [ ] single-fault negative test cases isolated to prevent invalid parameter masking
- [ ] domain boundary limits (min, max, empty, null) explicitly evaluated in equivalence classes
- [ ] mandatory happy-path journeys injected into the model as explicit seed rows
- [ ] deterministic random seed configured to guarantee matrix generation reproducibility
- [ ] generated combinatorial matrix converted into executable table-driven test cases
- [ ] descriptive test identifiers assigned to each matrix parameter combination
- [ ] test matrix executed with pass/fail telemetry captured for every parameter tuple
- [ ] test-report.json emitted detailing parameter matrix dimensions, reduction ratio, and results
- [ ] validation-result.json emitted with test run execution evidence and exit code 0
- [ ] interaction defects surfaced by matrix execution routed to 4-phase systematic debugging
- [ ] reduction ratio verified demonstrating at least 85–95% savings over full Cartesian product

## Output Contracts

When completing combinatorial test design and execution, emit:

- **`contracts/schemas/test-report.json`** — Documents parameter models, interaction coverage order ($t$), reduction metrics, executed matrix rows, and failure traces.
- **`contracts/schemas/validation-result.json`** — Captures test execution outcomes for Coordinator release gating.

## Failure Modes

- **Combinatorial explosion**: unpartitioned continuous inputs causing unmanageable matrix sizes. Mitigation: apply equivalence partitioning.
- **Error masking in negative tests**: combining multiple invalid parameters in one test. Mitigation: enforce single-fault negative isolation.
- **Over-constrained models**: constraints accidentally eliminate valid edge combinations. Mitigation: audit constraints against specification.
- **Under-specified constraints**: generating combinations that crash test setups before reaching business logic. Mitigation: model physical dependencies as preconditions.
- **Ad-hoc manual matrices**: manually selecting combinations without covering array algorithms. Mitigation: mandate PICT/PyPICT generation.
- **Missing golden journeys**: reduced matrix omits primary happy paths. Mitigation: inject mandatory seed rows into model.
- **Oracle ambiguity**: generating many combinations without automated verification oracles. Mitigation: enforce explicit invariant oracles per row.
- **Ignoring interaction strength**: using $t=2$ for safety-critical flight or financial control logic. Mitigation: escalate to $t=3$ or $t=4$ for high-risk domains.
- **State contamination across rows**: shared test state causes later table rows to fail falsely. Mitigation: reset state between table test subtests.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: verify parameter models against schema contracts to prevent testing unintended capability vectors.
- **ASI04 Supply Chain**: utilize verified PICT binaries or trusted PyPICT packages; validate package integrity hashes.
- **ASI05 RCE Guard**: sanitize parameter values before feeding into test execution harnesses to prevent injection attacks.
- **ASI07 Inter-Agent Communication**: emit structured `test-report.json` detailing interaction coverage order and excluded constraints.
- **ASI09 Human-Agent Trust Exploitation**: surface interaction coverage level ($t=2$, $t=3$) and excluded constraints transparently.

## Related Skills

- **write-tests**: Implement executable table-driven tests from generated combinatorial matrices
- **systematic-debugging**: Isolate multi-parameter interaction defects surfaced by combinatorial test failures
- **frontend-testing**: Apply pairwise combinations across browser viewports, user permissions, and component states
- **performance-profiling**: Stress-test high-dimension parameter combinations under load
- **review-code**: Audit combinatorial models and constraint definitions during pull request review
