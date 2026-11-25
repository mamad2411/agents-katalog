---
name: test-regression
description: "Turn a confirmed bug into a lasting behavioral check. Use to prevent recurrence of a confirmed defect; test adds general coverage."
---

# test-regression

Turn a confirmed bug into a lasting behavioral check.

## Choose this workflow

Use to prevent recurrence of a confirmed defect; test adds general coverage.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Testing methods](../../references/packs/testing.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; confirmed bug, reproduction, expected behavior, and fixed/broken revisions where available.

**Pack prerequisites:** Defined behavior, existing test conventions/runners, isolated fixtures, and relevant dependencies. Requested bounded verification may use owned isolated fixtures without authorizing product edits or live-system tests. Never test destructive behavior against production by default; distinguish mocked behavior from real integration evidence.

- **Infer from evidence:** Read behavior contracts, existing runners and test conventions; distinguish fixture setup failure from a behavioral failure.
- **Reasonable default:** Use the smallest existing local runner and isolated synthetic fixtures that distinguish the requested behavior. When the method needs a library, runner, container runtime or load tool the project lacks, name the exact package or tool, the files it changes and any download, and add it only when the request authorizes new dev dependencies or tools; label a hand-written generator without shrinking, or a fake in place of a real dependency, as such.
- **Ask only when needed:** Ask about an unresolved contract that changes the expected result, or the target/load limits before external testing; do not ask the user to choose a runner already configured.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

A durable test protecting the actual failure mechanism.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Identify the original trigger and intended observable behavior from requirements or independent evidence. Choose the lowest layer that can faithfully exercise the boundary; a database mock cannot establish real transaction behavior.
2. Construct minimal deterministic inputs and an expected result that does not call the implementation under test. Include the failing boundary and a neighboring valid case; for races, control completion order and assert that the losing path has no forbidden effect.
3. Where feasible, run the unchanged test against broken and fixed behavior in an isolated copy or worktree. Preserve unrelated user edits and the real index; do not roll back a dirty working file to perform a sensitivity check.
4. Confirm that the negative run fails on the intended assertion, not an import error, missing fixture, timeout or unrelated refactor. Report actual commands and statuses; if the old revision cannot run, explain the remaining evidence gap.

## Technical method

- **Inspect:** Establish the original trigger, broken revision and expected behavior independent of the proposed patch.
- **Method:** Add the lowest-layer check that observes the real failure; verify sensitivity in an isolated broken copy when feasible.
- **Avoid misdiagnosis:** A missing import or setup timeout on the old revision does not establish regression sensitivity.
- **Check the result:** Record the causal failing assertion or valid-input exception on broken code and a pass on the fix without weakening the expectation.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Testing worked example](../../references/examples/testing.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The affected project uses Flutter: [Flutter](../../references/frameworks/flutter.md).
- The affected project uses React Native / Expo: [React Native / Expo](../../references/frameworks/react-native.md).
- The task specifically involves windows desktop, ui automation, cross-agent regression, benchmark harness; load only the matching method: [Desktop and cross-host regression testing](../../references/methods/desktop-regression.md).

## Decision branches

- **When the old revision cannot execute in this environment:** Explain the limitation and use the strongest available independent reproduction evidence.

## Deliver and verify

- Trigger and independent expected result, test layer, original-defect sensitivity, fixed and neighboring-case results, and unavailable checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- The regression reaches the defective path and rejects its behavior; the fixed path and neighboring valid behavior pass. A syntax/setup failure or a test with no effective assertions is not regression evidence.

## Stop and recover

- If the old revision cannot run, state that limitation. Do not assert implementation details instead of the user-visible invariant.

## Example requests

- **Normal (apply):** Turn the confirmed duplicate-credit bug into a failing-then-passing check.
- **Edge (apply):** Add regression coverage for duplicate events while allowing distinct events.
- **Blocked (inspect):** Design a regression test when the original failing revision is unavailable.
