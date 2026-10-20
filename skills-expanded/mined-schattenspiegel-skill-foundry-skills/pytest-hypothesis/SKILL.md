---
        name: pytest-hypothesis
        description: >-
          Use when pytest fixtures, parametrization, markers, plugins, or collection interact with Hypothesis generated examples, settings, stateful tests, or regression examples. Do not use for pytest-only examples or standalone Hypothesis properties with no fixture or runner integration boundary.
        argument-hint: "[pytest and Hypothesis Integration task, code, contract, or failure]"
        ---

        # pytest and Hypothesis Integration

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `pytest item` | One collected test function and parameter instance. | Hypothesis executes many generated examples inside that item. |
| `fixture value` | State created according to pytest fixture scope. | Function-scoped fixtures are not recreated for every generated example. |
| `generated example` | One Hypothesis input and shrink candidate. | It must begin from equivalent clean state. |
| `settings profile` | Named budgets and health-check policy. | CI and local profiles should be selected explicitly and recorded. |
| `failure database` | Stored examples that replay previous failures. | It complements deterministic seeds and explicit regression examples. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Identify pytest item boundaries, fixture scopes, and which state must reset per generated example.
2. Move per-example construction into a factory or pure helper called inside the test.
3. Compose pytest parameters and generated arguments without hidden cross-products or shared mutation.
4. Select a named Hypothesis profile and preserve minimized failures.
5. Run repeated examples plus teardown and regression checks through pytest.

        ## Decision rules

        - Assume a function-scoped pytest fixture is shared across all Hypothesis examples for one item; use a fixture-provided factory or explicit reset for per-example state.
- Keep `@pytest.mark.parametrize` outside `@given` conceptually: each pytest parameter is one item with its own generated example stream.
- Use `@example` for known regressions and generated strategies for the general invariant; do not replace either with the other.
- Register named settings profiles with explicit max_examples, deadline, and database policy; do not suppress health checks without a documented cause.
- Do not catch Hypothesis assertion failures or share mutable globals, real network, or wall-clock state across examples.
- Run pytest through the pinned environment so plugin discovery, profile, and Hypothesis version match CI.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `integration.fixture-factory-per-example` and `integration.verify-example-isolation`: create fresh mutable state for every generated example.
- `integration.parametrize-given-composition` and `integration.verify-collected-cross-product`: combine finite algorithm modes with generated input domains.
- `integration.named-profile-regression-example` and `integration.verify-profile-and-example`: combine deterministic regression replay with an explicit CI budget.

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
