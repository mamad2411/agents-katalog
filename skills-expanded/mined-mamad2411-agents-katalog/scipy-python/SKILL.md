---
        name: scipy-python
        description: >-
          Use for writing, reviewing, debugging, or verifying Python numerical work with SciPy optimization, roots, integration, interpolation, sparse matrices, signal, spatial, or statistical routines. Do not use for symbolic algebra, arbitrary-precision arithmetic, or generic NumPy array manipulation alone.
        argument-hint: "[SciPy Python task, code, contract, or failure]"
        ---

        # SciPy Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `objective/residual` | A callable encoding the numerical problem. | Scale, domain, differentiability, and finite-value behavior determine solver suitability. |
| `solver result` | An estimate plus convergence and diagnostic fields. | A returned vector is not success until status and residual checks pass. |
| `sparse matrix` | A structure storing selected entries and layout metadata. | Choose CSR/CSC/COO from construction and operation patterns. |
| `distribution` | A parameterized probability model with numerical methods. | State parameterization and tail/log-space requirements. |
| `tolerance` | An error scale in input, output, or residual space. | Set it from the application scale, not an unexplained tiny literal. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. State the mathematical problem, domain, scale, and acceptable error.
2. Choose the routine and derivative/sparsity representation from those properties.
3. Run with explicit bounds, bracket, tolerances, and iteration budget.
4. Reject nonconvergence, nonfinite outputs, and excessive residuals.
5. Test a known solution, boundary case, and failure case.

        ## Decision rules

        - Choose a solver from smoothness, bounds, derivative availability, sparsity, and bracketing information.
- Check success or convergence flags and independently verify finite objective, residual, constraint, or reconstruction error.
- Scale variables and residuals when magnitudes differ materially; report tolerances in the resulting units.
- Provide analytic derivatives only when tested against finite differences or another independent check.
- Prefer log-space survival and likelihood functions in tails where direct subtraction loses precision.
- Use sparse formats deliberately and avoid accidental dense conversion in production-size paths.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `scipy.minimize-with-residual-guard` and `scipy.verify-optimality-status`: solve and independently verify a bounded smooth optimum.
- `scipy.bracketed-root-solve` and `scipy.verify-root-residual`: solve a scalar root with a proof-bearing bracket.
- `scipy.sparse-solve-with-residual` and `scipy.verify-sparse-residual`: solve a sparse system without accidental densification.

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
