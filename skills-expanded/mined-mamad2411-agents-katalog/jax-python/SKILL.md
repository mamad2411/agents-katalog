---
        name: jax-python
        description: >-
          Use for writing, reviewing, debugging, or optimizing Python JAX transformations including jit, grad, value_and_grad, vmap, random keys, pytrees, devices, and array control flow. Do not use for ordinary NumPy code or framework-specific Flax/Equinox/Optax design unless the JAX transformation contract is central.
        argument-hint: "[JAX Python task, code, contract, or failure]"
        ---

        # JAX Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `jax.Array` | A device-backed immutable array value. | Host conversion and device transfer are explicit boundaries. |
| `tracer` | A symbolic value observed while JAX traces a function. | Python conversion or data-dependent Python control flow is invalid. |
| `transformation` | jit, grad, vmap, pmap, or another program transform. | The function must be pure over compatible pytrees and shapes. |
| `PRNG key` | An explicit immutable random-state token. | Split or fold in unique identities; reusing a key repeats randomness. |
| `pytree` | A nested structure of leaves with registered container shape. | Treedef and leaf shapes/dtypes form part of compiled contracts. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Write the pure untransformed function and state its pytree, shape, dtype, and randomness contract.
2. Apply grad/vmap/jit in the minimal required order and mark static choices deliberately.
3. Keep random keys and updated parameters in explicit return values.
4. Inspect compilation/retracing and device-transfer boundaries.
5. Verify eager and transformed outputs plus gradient and reproducibility invariants.

        ## Decision rules

        - Keep transformed functions pure: return updated values and effects as data rather than mutating Python or global state.
- Use JAX control-flow primitives for traced data-dependent loops and branches; Python control flow is only for static decisions.
- Split keys before independent random uses and fold in stable step/device identities for reproducible parallel work.
- Separate static configuration from dynamic arrays and avoid recompilation caused by changing shapes or Python objects.
- Keep arrays on device through the compute region; block_until_ready when measuring execution rather than dispatch.
- Check gradients against finite differences or a known derivative on small, smooth, nondegenerate inputs.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `jax.pure-jitted-training-step` and `jax.verify-immutability-and-loss`: compile a pure parameter update without mutating input.
- `jax.split-fold-vmap-randomness` and `jax.verify-key-uniqueness-reproducibility`: derive reproducible nonreused random streams.
- `jax.grad-vmap-composition` and `jax.verify-batch-gradient-shape`: vectorize a scalar gradient over a batch.

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
