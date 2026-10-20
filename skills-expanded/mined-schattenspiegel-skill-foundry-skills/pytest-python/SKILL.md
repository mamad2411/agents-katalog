---
        name: pytest-python
        description: >-
          Use for writing, reviewing, debugging, or structuring Python tests with pytest, including fixtures, scopes, parametrization, monkeypatch, temporary paths, exceptions, warnings, subprocesses, and teardown. Do not use for Hypothesis property design, unittest-only suites, or application code with no pytest task.
        argument-hint: "[pytest Python task, code, contract, or failure]"
        ---

        # pytest Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `test item` | One collected executable test case. | Parametrization creates distinct items and mutable parameters are not copied. |
| `fixture` | A dependency-provided test context. | Its scope controls cache lifetime, not safe mutation policy. |
| `request` | The active item and fixture-resolution context. | Dynamic fixture lookup hides dependencies and requires justification. |
| `monkeypatch` | A reversible mutation ledger for one test scope. | Patch the name looked up by code under test. |
| `outcome` | Pass, fail, error, skip, or expected failure. | Do not turn known defects into unconditional passing tests. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Identify the behavior, observable result, external dependencies, and cleanup obligations.
2. Choose unit, integration, or subprocess scope and mark it explicitly.
3. Build the smallest fixture graph with visible ownership and deterministic inputs.
4. Parametrize boundaries and patch lookup sites rather than implementations globally.
5. Run the narrow item, then the suite; inspect collection, warnings, skips, and teardown errors.

        ## Decision rules

        - Arrange state in explicit fixtures and release it with `yield` plus `finally`; teardown must work after assertion and setup failures.
- Choose the narrowest fixture scope compatible with cost and isolation; never share mutable function expectations through session scope.
- Patch the symbol in the module that looks it up, before the call under test, and prefer dependency injection for code you own.
- Parametrize behaviorally distinct boundaries with readable IDs; do not mutate parameter values between items.
- Assert exception type and meaningful fields or message fragments, and keep the call that must raise inside the raises block.
- Block real network, clock, randomness, home-directory, and subprocess dependencies unless the test is explicitly an integration test.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `pytest.patch-lookup-site` and `pytest.verify-patch-restoration`: patch the symbol used by the target module instead of its origin.
- `pytest.yield-fixture-owner` and `pytest.verify-teardown-on-failure`: release an owned resource even when a test fails.
- `pytest.parametrize-invalid-boundaries` and `pytest.verify-distinct-items`: cover invalid boundaries as distinct parametrized items.

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
