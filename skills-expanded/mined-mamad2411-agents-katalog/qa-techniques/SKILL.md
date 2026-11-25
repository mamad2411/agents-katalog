---
name: qa-techniques
version: 1.0.0
description: Core test-design techniques — equivalence partitioning, boundary value analysis, state transition testing, invariant-based testing, and metamorphic testing — plus how to validate a new check by making it fail and how fixture shape creates blind spots. Load when designing test cases for a feature, endpoint, or function, not just when running existing tests.
---

# QA Test-Design Techniques

Use these to generate test cases systematically rather than by intuition alone. Pick the technique(s) that fit the shape of the thing under test — most non-trivial features need more than one.

## Equivalence Partitioning (EP)

Split the input space into partitions where every value in a partition should behave the same way. Test one representative per partition instead of every value.

- Identify valid partitions (per input field: valid range, valid enum values, valid format) and invalid partitions (out of range, wrong type, malformed, missing/null).
- One test per partition is enough *if* BVA (below) covers the edges separately — don't duplicate boundary values inside EP tests.
- Applies to: form fields, API parameters, config values, any function with a constrained input domain.

## Boundary Value Analysis (BVA)

Defects cluster at edges. For every partition boundary, test: the boundary value itself, one below, one above (min-1, min, min+1, max-1, max, max+1).

- Don't forget structural boundaries beyond numeric ranges: empty collection, single-element collection, max-length string, first/last page, zero, negative zero, empty string vs null vs whitespace.
- Off-by-one errors are the dominant bug class this technique catches — treat any `<` vs `<=` or loop bound as a boundary to test explicitly.

## State Transition Testing

For anything with a lifecycle (order status, user session, workflow/approval states, connection states): model states and legal transitions, then test:

- Every legal transition actually works.
- Every illegal transition is rejected (not silently ignored — rejected with a correct error).
- Transitions triggered from an unexpected state (e.g. "cancel" on an already-cancelled order).
- Re-entrancy: firing the same transition twice, concurrently, or out of order.

A transition table (current state × event → next state / error) makes gaps visible faster than prose.

## Invariant-Based Testing

Identify properties that must hold across *all* inputs and states, not just specific cases — then assert them directly instead of enumerating examples.

- Examples: totals sum to 100%, a sorted list stays sorted after any operation, an ID is never reused, a balance never goes negative, output length relates to input length in a fixed way.
- Where the codebase has property-based testing tooling (e.g. fast-check, Hypothesis, QuickCheck-style), prefer generating random inputs and asserting the invariant over hand-picked examples.
- Invariants are especially valuable for catching regressions EP/BVA won't — they don't require guessing which input matters.

## Metamorphic Testing

Useful when there's no single correct output to assert against (ML models, search ranking, non-deterministic pipelines, anything with "close enough" outputs). Instead of checking an absolute answer, check a *relation* between two related inputs and their outputs.

- Example relations: doubling all prices should double the total; reversing input order shouldn't change a sum; adding a no-op filter shouldn't change result count; running twice with the same seed should give identical output.
- Define the relation first, then generate input pairs that should satisfy it — a violation is a bug even without knowing what the "correct" output was.

## Validating the test itself

Every technique above generates a check; none of them proves the check works. A test written after a fix and only ever observed green is indistinguishable from one that asserts nothing, so before counting it as coverage, make it go red: revert the fix, disable the guard, or feed it the bad input — **one change at a time**, so you learn which assertion covers which defect rather than that the batch does something — then restore and confirm green. Record which assertion went red for which cause; that record is the evidence, not the green run. Common ways a check passes for the wrong reason: it inspects state the code already replaced (a re-rendered document, a reset fixture, a stale handle); the value it searches for was never present; a defensive layer elsewhere masks the defect independently; or it asserts on one encoding of a value while the defect appears in another. An assertion that cannot be made to fail is a finding about the test.

**A fixture defines the blind spot.** This is EP applied to the *shape* of the input, not just its value: if every case in a fixture is the same element type, content type, document, or lifecycle stage, then any defect specific to the shapes left out passes silently, and the suite reports green over exactly the cases that mattered. When a check guards an invariant, vary the dimension the invariant is stated over, and deliberately include cases a platform or framework may already handle for you — those are the ones that hide whether your own code does anything at all.

## Applying these together

For a typical feature: EP + BVA on each input field, state transition testing on any stateful behavior, at least one invariant that should never break, and metamorphic checks only where an absolute oracle isn't available. Don't apply all five reflexively to trivial code — match technique depth to the risk and complexity of what's under test (see the `qa-quality-attributes` skill for weighing risk across quality characteristics, and `qa-triage` for what to do once a technique surfaces a failure).
