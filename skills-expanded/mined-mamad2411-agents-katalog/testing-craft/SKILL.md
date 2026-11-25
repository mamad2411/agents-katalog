---
name: testing-craft
description: "Use when writing, reviewing, or refactoring tests, or choosing verification for a code change."
user-invocable: true
argument-hint: "[rust|typescript|go|python] [target]"
---

# Testing Craft

Choose tests for the defects they catch. Preserve useful regression coverage
without binding tests to incidental implementation details.

## Scope and verification

- Identify the behavior being changed and the specific defect each new or
  modified test should catch. A test need not detect unrelated defects.
- Follow project instructions and existing test conventions over these defaults.
- Run affected tests and required checks. Broaden coverage when the change's
  dependencies, failures, or unresolved risks justify it.
- Do not change production architecture merely to satisfy a testing preference.
  Restructure when needed for the requested fix; propose independent refactors.
- Read only the relevant language file below when runner or fixture guidance is
  needed. General code guidance lives in `code-craft`.

## Choose the boundary and layer

Prefer inputs and observable outputs through the feature's public boundary.
Private helpers can merit direct tests for substantial algorithms or invariants;
do not make them public solely for testing.

Use the cheapest layer that catches the risk:

| Risk | Suitable starting point |
|---|---|
| Parsing, pure logic, state transitions | Unit test |
| Collaboration between components | Real objects or a maintained fake |
| Service or HTTP contract | Integration test with a hermetic server or contract-tested fake |
| UI wiring | Drive the rendered control rather than calling its handler |
| Cross-system behavior | Focused end-to-end test |

Use existing automation when it covers the changed behavior. Manual exercise is
useful when it catches a risk that automation does not, such as visual layout.

## Avoid implementation-mirroring tests

Source-text assertions and exact internal call scripts often pin an
implementation without protecting its contract. For a suspect test, identify:

- The behavior it protects.
- A concrete defect that would make it fail.
- Whether it rejects a valid implementation with the same behavior.

Rewrite brittle assertions to check results, state, rendered output, or external
effects. Remove a test only when it has no useful contract to protect or its
coverage is redundant. A test passing while some other behavior breaks is not
a reason to delete it.

Interaction assertions are useful when the interaction is itself the contract,
such as sending one email, avoiding a network request on a cache hit, or checking
authorization before a write. Assert only the relevant calls and arguments.

## Choose collaborators

Prefer the real implementation when it is fast, deterministic, and isolated.
Use temporary directories, throwaway repositories, or local servers where useful.

When the real dependency is unsuitable:

- Use a narrow working fake for stateful behavior. Check shared fakes against
  the real contract where practical.
- Use a stub for canned query results or to force a failure.
- Use a mock for interactions whose occurrence, absence, or order is the contract.

Avoid elaborate mock setups that duplicate implementation details. A wrapper
around a third-party dependency can provide a stable seam, but do not add one
solely to obey a ban on mocking types you do not own. Use the project's existing
seams and library-supported testing tools when they fit.

## Write readable tests

- Name the scenario and expected outcome. Keep cause and effect visible.
- Keep relevant inputs and expectations in the test body. Helpers may hide
  irrelevant construction; table-driven cases are useful for parallel scenarios.
- Do not compute expected results by repeating the production algorithm.
- Choose distinct values that expose swapped inputs or accidental defaults.
  Include empty, zero, and boundary values when those are the behavior under test.
- Assert the fields that matter. Use full-object equality when the whole object
  is the contract, rather than a broad snapshot of incidental details.
- Make failures show expected and actual values.
- Cover relevant failure paths and boundaries. Use property tests when invariants
  or a large input space justify them, not merely because a library is available.

## Keep tests deterministic

- Wait for completion signals or observable conditions with a timeout; do not
  sleep for an arbitrary duration and assume work finished.
- Control time and randomness when they affect the result.
- Isolate mutable state between tests.
- Make important failures reproducible through a controlled dependency or input.

## Establish regression sensitivity

For a bug fix, reproduce the actual failure before changing production code when
feasible. Confirm the regression test fails for the intended reason, then passes
with the fix.

For other changes, identify the defect the assertion detects. Use targeted
mutation when sensitivity is uncertain or the risk warrants it. If mutating
production code, isolate the experiment and restore it before continuing.

Inverting an assertion checks execution, not sensitivity to the intended defect.
Routine test edits and green-to-green refactors do not require production
mutations. Preserve the behaviors covered and compare relevant results before
and after a refactor. Report verification you could not perform.

## Language references

Read the relevant file when runner, fixture, or async-test details are needed:

- [Rust](languages/rust.md)
- [TypeScript / JavaScript](languages/typescript.md)
- [Go](languages/go.md)
- [Python](languages/python.md)

For other languages, follow the project's conventions.

## Provenance

Adapted from Google's Testing on the Toilet series, including behavior-focused
tests, test doubles, DAMP, and SMURF. The source episodes are indexed in
[references/episodes.md](references/episodes.md), by way of
[shamashel/testing-on-the-toilet](https://github.com/shamashel/testing-on-the-toilet).
