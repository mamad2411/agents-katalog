---
name: evidence-driven-validation
description: Show that code works with evidence instead of guesswork. Define contracts and invariants, add observability, run deterministic checks, and save artifacts that show what passed and what failed.
---

# Evidence-Driven Validation

Use this skill when the user wants more than a quick test and explicitly cares about showing that programmed behavior is correct.

Typical triggers:

- "prove it works"
- "don't just eyeball it"
- "show me why this is correct"
- "I want a real validation plan"
- "this transition / workflow / interaction must be exact"
- "I want measurable correctness, not vibes"

## Goal

Turn the programmed system into an observable model and then check:

1. what the valid states are
2. which transitions are allowed
3. which invariants must hold during and after every transition
4. which artifacts prove the result

## Workflow

1. Define the state model

- inputs
- internal state
- outputs
- persisted state
- task-specific runtime state such as queue progress, active step, or selected entity

2. Define validation obligations

Write them in an if-then form:

- If preconditions hold,
- and transition `T` is applied,
- then invariant set `I` must still hold,
- and the resulting observable state must match the expected state.

3. Add diagnostics

Add the smallest observability layer that makes the obligations checkable.

Expose at least:

- current state values
- transition phase
- counters
- derived outputs
- persisted snapshot checksum when persistence matters
- error count or failure signals

4. Add deterministic runs

Use automation to run repeatable cases such as:

- idle stability
- transition sequences
- persistence roundtrip
- boundary conditions
- failure handling
- regression cases for bugs that were already found

5. Save artifacts

For every validation case, save:

- JSON state snapshot
- pass/fail verdicts
- log output
- screenshot or trace when visuals matter
- optional video when motion or timing matters

6. Keep one manual protocol

If a critical behavior cannot be simulated reliably, write a short manual protocol with exact pass rules and required evidence.

## Output Standard

The result is only complete when all of these exist:

- diagnostics mode or equivalent observability hook
- deterministic validation runner
- artifact directory
- readable report
- clear list of currently passing vs failing validation cases

## Important Rule

Do not claim success from appearance alone.

If the validation runner says a case fails, report it as failing even if the feature looks mostly right.

