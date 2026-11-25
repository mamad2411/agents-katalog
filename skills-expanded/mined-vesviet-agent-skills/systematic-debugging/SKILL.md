---
name: systematic-debugging
description: Apply 4-phase systematic root cause analysis (Observe, Hypothesize, Test, Fix) and verification-before-completion guardrails to eliminate trial-and-error patching. Use when diagnosing defects, investigating test failures, or isolating runtime regressions.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Systematic Debugging

Use this skill to investigate, isolate, and remediate defects using 4-Phase Systematic Root Cause Analysis (RCA) and empirical Verification-Before-Completion gates.

## When to Use

- diagnosing defects, flakiness, or test failures across microservices, background workers, or UI components
- unexpected runtime exceptions, data corruption, state desynchronization, or memory leaks occur
- tempted to apply speculative quick fixes or trial-and-error edits without empirical proof
- establishing a minimal deterministic reproduction test before touching production code
- verifying fixes with rigorous verification-before-completion gates to eliminate false-green sign-offs
- investigating complex distributed failures involving eventual consistency, race conditions, or timing windows
- isolating state transition errors in stateful workflows, distributed sagas, or payment lifecycles
- resolving non-deterministic flakiness in async message queues, outbox patterns, or cache invalidation
- auditing intermittent test failures in CI/CD pipelines before escalating or skipping checks

## Core Rules

- **The Iron Law of Root Cause Analysis (RCA)**:
  - never apply production code fixes without prior root-cause proof; symptom patches are engineering failures.
  - reject guess-and-check loops; all code modifications must test an explicit, evidence-backed hypothesis.
  - treating symptoms by wrapping exceptions in catch-alls or adding speculative null checks masks defects.
  - confirm the failure mechanism before editing code; speculative edits inflate architectural debt.
- **4-Phase Systematic RCA Loop**:
  - **Phase 1: Observe**: capture verbatim stack traces, logs, execution inputs, and environment configurations; establish invariant boundaries.
  - **Phase 2: Hypothesize**: formulate falsifiable, mechanistic hypotheses ranked by evidence weight; reject ungrounded assumptions.
  - **Phase 3: Test**: author an independent, minimal failing reproduction test proving the defect on unmodified baseline code (Red phase).
  - **Phase 4: Fix**: apply the minimal surgical remediation addressing the proven root cause; verify reproduction passes (Green phase).
- **Hypothesis Ranking by Disproof Cost**:
  - prioritize testing hypotheses that can be decisively disproved with minimal diagnostic overhead before investing in heavy instrumentation.
  - reject ambiguous theories that cannot be subjected to a concrete empirical test.
- **Verification-Before-Completion Gate Function**:
  - enforce the mandatory 5-step gate before declaring any task, bug fix, or ticket complete:
    `IDENTIFY` -> `RUN` -> `READ` -> `VERIFY` -> `REPORT`.
  - **IDENTIFY**: identify the exact automated command (test runner, build, linter, or health probe) validating the fix.
  - **RUN**: execute the command freshly in the current environment; never rely on stale runs or prior turn passes.
  - **READ**: parse complete terminal output, inspect raw assertion logs, and confirm exit code 0.
  - **VERIFY**: confirm modified code paths were executed and negative paths fail as expected (epistemic doubt).
  - **REPORT**: state task completion accompanied by verbatim command invocations and raw output proof.
  - ban rationalization phrases ("should work now", "minor fix", "passed earlier", "assumed clean").
- **Epistemic Doubt & Anti-Rationalization**:
  - reject rationalization trap 1: *"It should work now"* — run the test command and verify raw terminal output.
  - reject rationalization trap 2: *"I am confident this fixes it"* — confidence is not evidence; demand empirical proof.
  - reject rationalization trap 3: *"Tests passed in a previous turn"* — verify current working tree state freshly.
  - reject rationalization trap 4: *"Minor change, no verification needed"* — every change requires automated validation.
  - audit assertions to eliminate assertion theater; prove assertions evaluate real state mutations.
- **Single-Variable Change Discipline**:
  - modify exactly one variable or code statement at a time during diagnostic experimentation.
  - revert exploratory changes immediately if the test does not validate the specific hypothesis.
- **Minimal Surgical Footprint**:
  - isolate fixes strictly to the root cause; do not bundle opportunistic refactoring with bug fixes.
  - execute full regression suites to guarantee zero collateral breakage across adjacent modules.
- **Tight Feedback-Loop-First & Diagnostic Hygiene (`diagnosing-bugs`)**:
  - establish the fastest deterministic red-capable feedback loop (in-process unit test $\rightarrow$ CLI harness $\rightarrow$ container integration test) before reading code to speculate on causes.
  - minimise the reproduction input/configuration down to the smallest failing surface before hypothesizing.
  - formulate 3–5 competing falsifiable hypotheses using `"If X is the root cause, changing Y will eliminate the defect"`.
  - prefix any temporary diagnostic log lines with `[DEBUG-...]` and grep-purge all `[DEBUG-` markers prior to completion.
- **Deep Reference Guide**:
  - advanced RCA patterns and verification contracts: `core/roles/references/qa-engineer-review-checklist.md`.

## Suggested Process

### Step 1: Observation & Defect Characterization (Phase 1)
1. Collect verbatim error output, stack traces, system logs, and telemetry spans without mutation.
2. Determine environment variables, runtime versions, configuration flags, and active dependencies.
3. Define the precise expected invariant versus observed anomalous behavior.
4. Check recent git commit history and deployment logs to identify candidate regression windows.
5. Record reproduction preconditions including database states, network topology, and active tenancy context.
6. Correlate distributed trace spans to isolate the exact microservice boundary where divergence begins.
7. Confirm whether the defect occurs deterministically under single-threaded execution or requires concurrency.

### Step 2: Falsifiable Hypothesis Formulation (Phase 2)
1. Trace the execution call stack backward from failure point to source inputs.
2. Formulate explicit hypotheses explaining the mechanistic cause of the state or invariant divergence.
3. Prioritize hypotheses by empirical probability; document what specific observation would disprove each.
4. Eliminate superficial explanations until a concrete, reproducible code path mechanism remains.
5. Identify the exact architectural boundary or invariant that failed to protect system state.
6. Frame each hypothesis as a causal prediction: "If input X occurs under state Y, component Z violates invariant W because of mechanism M."
7. Cross-reference the suspected component with architectural specifications to confirm designed behavior.

### Step 3: Minimal Deterministic Reproduction (Phase 3: Red Phase)
1. Author the smallest possible automated unit, integration, or contract test reproducing the failure.
2. Run the test against the unmodified codebase inside an isolated Level 0 sandbox.
3. Confirm deterministic failure matching the exact production symptom, error signature, and stack frame.
4. Verify the test fails due to the hypothesized defect rather than environment or setup discrepancies.
5. Ensure the reproduction test is self-contained and free of external network or timing dependencies.
6. Verify failure determinism across consecutive runs to rule out test harness flakiness.
7. Confirm that mocks or test doubles do not stub out the suspect code path under evaluation.

### Step 4: Surgical Root-Cause Remediation (Phase 4: Green Phase)
1. Implement the minimal code change addressing the proven root cause directly.
2. Run the reproduction test; confirm it transitions from Red to Green cleanly.
3. Inspect the diff to ensure zero unnecessary edits, leaked debug code, or scope creep.
4. Preserve the reproduction test as a permanent automated regression test in the repository.
5. Reinforce invariants with type constraints, schema validation, or domain assertions to prevent recurrence.
6. Verify that clean architectural layer separation is maintained without cross-layer leakage.

### Step 5: Verification-Before-Completion Gate Sweep
1. **IDENTIFY**: pinpoint the test runner invocation, target file, and specific test case name.
2. **RUN**: invoke the test command in a clean terminal session without cached artifacts.
3. **READ**: inspect raw terminal stdout/stderr, verify exit code 0, and confirm assertions executed.
4. **VERIFY**: verify that the modified code path was traversed and negative cases fail on error.
5. Run full package and dependent test suites to confirm zero regressions across adjacent features.
6. Verify linter, typechecker, and build pass cleanly with exit code 0.
7. Confirm stateful persistence, message queues, and cache layers reflect correct side effects.
8. Assert that no newly added tests are tautological or skipped by the test framework runner.

### Step 6: Artifact Emission & Delivery
1. Record defect etiology, reproduction steps, fix diff, and verification logs.
2. Emit machine-readable validation artifacts for Coordinator and Reviewer sign-off.
3. Document any residual risk or operational monitoring recommendations for deployment.
4. Update post-incident knowledge base or test checklists with the discovered failure pattern.
5. Confirm that the test suite executes deterministically in continuous integration pipelines.

## Checklist

- [ ] defect symptoms, stack traces, telemetry logs, and execution inputs captured verbatim
- [ ] mechanistic, falsifiable root cause hypothesis formulated based on observed evidence
- [ ] minimal, deterministic failing reproduction test authored and verified Red on baseline
- [ ] reproduction failure signature verified matching the hypothesized causal defect mechanism
- [ ] surgical fix implemented addressing confirmed root cause without speculative edits
- [ ] reproduction test freshly executed and verified passing Green with exit code 0
- [ ] full regression test suite executed with zero collateral failures or state leaks
- [ ] Verification-Before-Completion gate executed (Identify -> Run -> Read -> Verify -> Report)
- [ ] epistemic doubt checks performed confirming modified code path execution and negative paths
- [ ] test-report.json emitted with reproduction steps, root cause analysis, and evidence
- [ ] validation-result.json emitted with fresh command outputs and exit code 0
- [ ] permanent regression test committed alongside surgical code remediation
- [ ] invariant reinforcement added to prevent architectural regression

## Red Flags

| Rationalization Thought | Positive Corrective Action |
|---|---|
| "This bug is obvious; I can patch it right away." | Write and run the failing Red reproduction test first to prove the causal mechanism. |
| "It should work now — small one-line fix." | Execute `IDENTIFY -> RUN -> READ -> VERIFY -> REPORT` and quote fresh exit-code-0 output. |
| "Tests passed in an earlier turn." | Re-run the exact test command against the current working tree before reporting success. |
| "Let me add a defensive null check / try-catch to silence it." | Trace backward to the invariant violation and fix the source instead of masking symptoms. |

## Output Contracts

When completing defect investigations and applying verified fixes, emit:

- **`contracts/schemas/test-report.json`** — Documents defect reproduction steps, root cause analysis, test execution results, and verified fix evidence.
- **`contracts/schemas/validation-result.json`** — Captures Verification-Before-Completion command runs, exit codes, and gate validation status.

## Failure Modes

- **Guess-and-check thrashing**: applying speculative patches hoping tests pass. Mitigation: enforce Iron Law and mandatory Red reproduction test.
- **Symptom masking**: wrapping exceptions in catch-alls or adding ungrounded null checks. Mitigation: trace root cause to original invariant violation.
- **Premature completion claim**: reporting fix complete without running fresh verification command. Mitigation: enforce 5-step Verification-Before-Completion gate.
- **Tautological reproduction**: reproduction test mocks away the failure path. Mitigation: ensure reproduction runs against real business logic.
- **Collateral regression**: fix introduces secondary defects in adjacent flows. Mitigation: execute full regression suite and linter before sign-off.
- **False-green assertion theater**: tests assert HTTP 200 without checking database state mutations. Mitigation: enforce side-effect verification in Phase 4.
- **Confirmation bias**: stopping at the first plausible hypothesis without testing alternatives. Mitigation: formulate falsifiable tests for top two competing hypotheses.
- **Flaky reproduction**: reproduction depends on unmanaged race conditions or sleep delays. Mitigation: replace sleeps with explicit synchronization barriers.
- **Incomplete environmental capture**: reproducing under dev settings when the bug requires production concurrency. Mitigation: mirror container memory and thread limits.
- **Diagnostic pollution**: leaving temporary debug logs or tracing flags in production code. Mitigation: audit git diff before signing off.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: cross-reference reproduction test against contract specification to prevent locking in invalid behavior.
- **ASI05 RCE Guard**: execute reproduction scripts and tests within isolated sandboxes (`--network=none`, non-root user).
- **ASI07 Inter-Agent Communication**: emit structured `test-report.json` with machine-verifiable verification evidence.
- **ASI09 Human-Agent Trust Exploitation**: never claim a bug is resolved without providing verbatim verification commands and exit codes.

## Related Skills

- **write-tests**: Author permanent regression test cases and property-based invariant checks
- **combinatorial-testing**: Design pairwise interaction test suites to reproduce multi-parameter edge cases
- **troubleshoot-service**: Inspect system logs, runtime traces, and platform diagnostics
- **review-code**: Verify surgical fixes against architectural boundaries and coding standards
- **commit-code**: Package verified reproduction tests and fixes into atomic commits
