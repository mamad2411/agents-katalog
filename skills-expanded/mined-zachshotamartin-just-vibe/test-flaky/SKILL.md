---
name: test-flaky
description: "Repair nondeterminism using repeated evidence. Use for nondeterministic failures; debug first identifies the relevant failing test/environment."
---

# test-flaky

Repair nondeterminism using repeated evidence.

## Choose this workflow

Use for nondeterministic failures; debug first identifies the relevant failing test/environment.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Testing methods](../../references/packs/testing.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; flaky test, failure history, environment, and repetition budget.

**Pack prerequisites:** Defined behavior, existing test conventions/runners, isolated fixtures, and relevant dependencies. Requested bounded verification may use owned isolated fixtures without authorizing product edits or live-system tests. Never test destructive behavior against production by default; distinguish mocked behavior from real integration evidence.

- **Infer from evidence:** Read behavior contracts, existing runners and test conventions; distinguish fixture setup failure from a behavioral failure.
- **Reasonable default:** Use the smallest existing local runner and isolated synthetic fixtures that distinguish the requested behavior. When the method needs a library, runner, container runtime or load tool the project lacks, name the exact package or tool, the files it changes and any download, and add it only when the request authorizes new dev dependencies or tools; label a hand-written generator without shrinking, or a fake in place of a real dependency, as such.
- **Ask only when needed:** Ask about an unresolved contract that changes the expected result, or the target/load limits before external testing; do not ask the user to choose a runner already configured.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Nondeterminism from shared state, order, time, async behavior, randomness, or environment.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Record order, seed, clock and shared-resource conditions and the repeat budget. Without a stated budget, derive one from single-run duration and the observed failure rate, cap total wall time (state the cap once) and report the detection power of the chosen sample.
2. Reproduce under controlled repeats, varying one factor at a time within the budget, and inspect the first divergent evidence.
3. Fix isolation or synchronization, replacing timing guesses with explicit synchronization, and rerun bounded stress checks.

## Technical method

- **Inspect:** Gather repeated outcomes, order, seed, clock, shared resources and cleanup evidence.
- **Method:** Force the suspected race or shared-state condition deterministically before changing implementation or tests.
- **Avoid misdiagnosis:** Increasing timeouts, retries or skips can hide nondeterminism rather than repair it.
- **Check the result:** Run a bounded repeated sample with retained counts and the targeted interleaving; zero observed failures remains finite evidence.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Testing worked example](../../references/examples/testing.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves windows desktop, ui automation, cross-agent regression, benchmark harness; load only the matching method: [Desktop and cross-host regression testing](../../references/methods/desktop-regression.md).

## Decision branches

- **When no failure occurs during bounded repeats:** Report the sample and uncertainty; do not declare the flake eliminated solely from absence.

## Deliver and verify

- Cause and trigger conditions, the isolation or synchronization fix, repeat counts, failure rates and residual uncertainty.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The triggering interleaving/order is exercised; no failures across a stated sample is not described as mathematical proof.

## Stop and recover

- Do not hide failures with retries, sleeps, skipped tests, or inflated timeouts without evidence. Stop at the repeat budget.

## Example requests

- **Normal (apply):** Fix the test that fails only in suite order; cap diagnosis at 30 repeats.
- **Edge (apply):** Repair a test that fails only after another test changes global state.
- **Blocked (inspect):** Inspect flake logs without rerunning expensive suites or adding arbitrary sleeps.
