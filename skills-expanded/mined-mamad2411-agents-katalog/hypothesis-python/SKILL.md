---
        name: hypothesis-python
        description: >-
          Use for writing, reviewing, debugging, or testing property-based Python tests with Hypothesis, including strategies, invariants, shrinking, composite data, stateful tests, settings, and regression examples. Do not use for ordinary example-based pytest tests or random fuzz loops without Hypothesis.
        argument-hint: "[Hypothesis Python task, code, contract, or failure]"
        ---

        # Hypothesis Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `strategy` | A lazy description of a value space and shrink order. | Construct valid structure rather than filtering broad invalid values. |
| `example` | One generated or explicit test input. | The test must be independent and deterministic for that input. |
| `property` | An invariant checked across generated examples. | It must be stronger than restating the implementation. |
| `shrinker` | The search for a smaller failing example. | Opaque setup, global state, and catching assertion failures obstruct it. |
| `state machine` | Generated sequences of operations over mutable state. | Use only when history affects validity or outcomes. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. State the domain, invariant, forbidden values, and independent oracle.
2. Build primitive then composite strategies with meaningful size bounds.
3. Write a pure property and preserve useful shrinking.
4. Add stateful rules only for history-dependent behavior.
5. Run with the project profile and retain minimized failures as regressions.

        ## Decision rules

        - Derive strategies from the input contract and construct valid relationships directly with composite or flatmap strategies.
- Assert semantic invariants, round trips, or agreement with an independent oracle; do not duplicate the implementation algorithm.
- Avoid `.filter` and `assume` when a constructive strategy can express the domain and shrink better.
- Keep generated tests free of shared mutable state, real network, wall clocks, and uncontrolled randomness.
- Use a rule-based state machine only when operation sequences expose defects that single calls cannot.
- Retain production regressions with `@example` while keeping the general property that found them.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `hypothesis.recursive-json-strategy` and `hypothesis.verify-json-round-trip`: test a serialization round trip over recursive JSON values.
- `hypothesis.constructive-intervals` and `hypothesis.verify-shrinkable-relations`: construct ordered intervals without rejection filtering.
- `hypothesis.stateful-model` and `hypothesis.verify-operation-sequences`: compare operation sequences against a simple model.

        Recipes are anchors, not blind templates. Preserve their named invariants and
        adapt types and names only after inspecting the actual boundary.

        ## Verification contract

        - Test observable behavior, not the presence of API tokens.
        - Exercise empty, singleton, malformed, and failure inputs when the operation
          accepts them.
        - Assert shape, dtype or type, ordering, ownership, and error semantics where
          they are part of the contract.
        - Keep external I/O deterministic with injected clocks, transports, processes,
          files, random state, or test doubles.
        - Run the narrow test first, then the relevant project suite. Do not declare
          completion when warnings, background failures, convergence flags, or cleanup
          errors remain unexplained.

        Use [the verification matrix](references/verification.md) for completion checks.

        ## Failure routing and adaptation

        Classify a failure before changing code: input-contract failures require a
        precise rejection; environment or version failures require inspection; execution
        failures require lifecycle, convergence, or cleanup evidence; invariant failures
        require a semantic correction. Do not relax a check, coerce a value, broaden a
        failure handler, or materialize data merely to make the symptom disappear.

        When adapting a recipe:

        1. Match its objects, ownership, execution timing, and output contract to the task.
        2. Preserve every branch condition and completion check while changing domain names.
        3. Add the project's real empty, malformed, duplicate, cancellation, precision, or
           boundary case before removing any guard.
        4. If the installed API differs, inspect the signature and primary documentation,
           then update implementation, test, and authoring evidence together.

        ## Version grounding

        Inspect the installed package and signature when editing an existing project.
        Treat examples here as verified anchors for the version recorded by the Foundry,
        not as permission to overwrite a repository's compatibility policy. When current
        behavior differs, preserve the project target and update tests and authoring
        evidence together.

        ## Completion

        Complete the task only when the implementation preserves the declared object
        model, no accidental materialization or lifetime extension was introduced, all
        failures are surfaced at the correct boundary, and deterministic tests prove the
        critical behavior. Report any environment or version fact that could not be
        verified.
