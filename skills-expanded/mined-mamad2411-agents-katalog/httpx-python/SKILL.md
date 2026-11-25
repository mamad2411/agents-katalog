---
        name: httpx-python
        description: >-
          Use for writing, reviewing, debugging, or testing Python HTTP clients with HTTPX, including Client/AsyncClient ownership, timeouts, connection limits, streaming, transports, errors, and cancellation. Do not use for requests-only code, FastAPI route design, browser automation, or generic retry policy alone.
        argument-hint: "[HTTPX Python task, code, contract, or failure]"
        ---

        # HTTPX Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `Client` | A sync connection pool and configuration owner. | Create at an application/session boundary, not per request. |
| `AsyncClient` | An async connection pool tied to async lifecycle. | Close it in the same event-loop ownership scope. |
| `Request/Response` | Protocol messages with headers, content, and status. | Streaming bodies hold resources until consumed or closed. |
| `Transport` | The I/O implementation below client policy. | MockTransport replaces network behavior without patching client methods. |
| `Timeout/Limits` | Separate connect/read/write/pool budgets and pool capacity. | They are not an end-to-end retry deadline. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Define client owner, sync/async mode, base URL, authentication, and transport trust boundary.
2. Set timeout phases, pool limits, redirect policy, and accepted status/payload contract.
3. Choose buffered or streaming response handling from maximum body size.
4. Separate transport, HTTP status, decoding, and domain errors.
5. Test with a transport double, including timeout/error and cleanup paths.

        ## Decision rules

        - Inject or application-scope a client so connection pooling survives related requests; a helper borrowing a client must not close it.
- Set connect, read, write, and pool timeouts from the operation contract; do not disable all timeouts as a repair.
- Use `stream` and consume or close the response inside its context when the body can exceed memory.
- Call `raise_for_status` before trusting an HTTP success payload, then validate the domain payload separately.
- Use MockTransport or ASGITransport in tests and assert outgoing request semantics without real network access.
- Retry only replay-safe operations under an explicit budget; HTTPX transport retries do not replace domain retry decisions.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `httpx.borrowed-client-json` and `httpx.verify-request-domain-contract`: use a caller-owned client and validate status before payload.
- `httpx.atomic-stream-download` and `httpx.verify-stream-cleanup`: stream a response to a file with cleanup and atomic replacement.
- `httpx.client-policy` and `httpx.verify-timeout-limit-policy`: construct an application client with phase budgets and bounded pooling.

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
