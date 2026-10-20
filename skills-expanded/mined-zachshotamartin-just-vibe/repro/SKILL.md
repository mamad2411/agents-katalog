---
name: repro
description: "Create a minimal, reliable reproduction of a problem. Use to isolate an observable failure; debug diagnoses the cause, test-flaky owns order and timing nondeterminism, test-regression locks the reproduced case, and fix changes production behavior after the trigger is understood."
---

# repro

Create a minimal, reliable reproduction of a problem.

## Choose this workflow

Use to isolate an observable failure; debug diagnoses the cause, test-flaky owns order and timing nondeterminism, test-regression locks the reproduced case, and fix changes production behavior after the trigger is understood.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [General methods](../../references/packs/general.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; failure report, expected behavior, and environment constraints.

**Pack prerequisites:** Resolve the user brief and inspect the relevant project or supplied evidence. External capabilities are optional unless the selected action actually needs them.

- **Infer from evidence:** Resolve the named files, existing scripts, current task and earlier corrections from the conversation and repository.
- **Reasonable default:** Use the narrowest interpretation that completes a reversible local task; state a consequential assumption once.
- **Ask only when needed:** Ask when competing targets or incompatible success conditions would change the result; continue independent inspection first.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Minimal reproducer in an agreed scratch/test location; not a product fix.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Confirm the symptom and freeze input and environment identity.
2. Reduce unrelated dependencies and data one dimension at a time while preserving the failure trigger.
3. Include a negative control that removes the suspected trigger, and document exact run and reset steps.

## Technical method

- **Inspect:** Capture exact input, environment, revision and the observable failure oracle.
- **Method:** Reduce dependencies and data while preserving the causal trigger; keep synthetic substitutes faithful to the failing boundary.
- **Avoid misdiagnosis:** A smaller program with a different failure does not reproduce the original bug.
- **Check the result:** Run from a clean isolated setup and show the same expected-versus-actual mismatch with bounded execution.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [General worked example](../../references/examples/general.md).
- Choosing a test layer, independent assertions, or regression, flaky and property checks: [Testing methods](../../references/packs/testing.md).

## Decision branches

- **When reducing the case removes the failure intermittently:** Preserve the last reliable reproduction and quantify repeats instead of discarding timing evidence.

## Deliver and verify

- Isolated reproduction fixture or script with exact run/reset steps, expected versus actual output, environment identity and required conditions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A fresh isolated run reproduces the issue; removing the critical trigger makes the failure disappear.

## Stop and recover

- Redact production data and secrets. If reduction changes the symptom, keep the last valid reproducer and report the limit.

## Example requests

- **Normal (apply):** Create an isolated minimal reproduction of the double-submission bug.
- **Edge (apply):** Reproduce an order-dependent test failure without copying production secrets.
- **Blocked (inspect):** Describe a reproduction plan when the affected binary is unavailable.
