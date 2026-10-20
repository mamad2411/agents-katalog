---
        name: asyncio-python
        description: >-
          Use for writing, reviewing, debugging, or testing Python asyncio code involving coroutines, Tasks, TaskGroup, cancellation, timeouts, queues, synchronization, or blocking-call boundaries. Do not use for SimPy models, ordinary synchronous code, Trio-only programs, or FastAPI routing without an asyncio lifecycle defect.
        argument-hint: "[asyncio Python task, code, contract, or failure]"
        ---

        # asyncio Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `coroutine` | A suspended computation created by calling an async function. | It does not run until awaited or scheduled. |
| `Task` | An event-loop-owned running coroutine with a result or exception. | Keep a strong owner until completion. |
| `TaskGroup` | A structured scope that owns sibling tasks. | A non-cancellation failure cancels remaining siblings and exits with an exception group. |
| `Queue` | A bounded handoff and backpressure point. | Every accepted item requires exactly one task_done call. |
| `timeout` | A cancellation scope transformed into TimeoutError at its boundary. | Cleanup must remain cancellation-safe. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Identify the coroutine owner, task scope, result ordering, and maximum concurrency.
2. Mark every cancellation and timeout boundary plus the cleanup that must finish.
3. Choose TaskGroup, a bounded queue, or direct awaiting from those semantics.
4. Keep blocking work outside the event-loop thread and document its termination limit.
5. Test success, sibling failure, cancellation, timeout, and cleanup before completion.

        ## Decision rules

        - Use `TaskGroup` when sibling work should fail and clean up as one unit; use `gather` only when its different failure semantics are intentional.
- Bound concurrency at the resource operation, not only at task creation, and preserve input ordering explicitly when the result contract requires it.
- Re-raise `CancelledError` after local cleanup; do not convert cancellation into an ordinary failure or successful result.
- Use a bounded queue when producers can outpace consumers; pair `put`, `task_done`, `join`, and worker shutdown deliberately.
- Move blocking callables through `asyncio.to_thread`; state that cancelling the await does not forcibly terminate the underlying thread.
- Inject clocks, events, and test doubles; do not verify concurrency with long sleeps or wall-clock races.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `asyncio.bounded-ordered-map` and `asyncio.verify-bounded-ordered-map`: run bounded concurrent work while preserving input order.
- `asyncio.timeout-owned-resource` and `asyncio.verify-timeout-cleanup`: bound an async operation and close its owned resource after timeout.
- `asyncio.to-thread-boundary` and `asyncio.verify-loop-progress`: isolate a blocking callable without freezing the event loop.

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
