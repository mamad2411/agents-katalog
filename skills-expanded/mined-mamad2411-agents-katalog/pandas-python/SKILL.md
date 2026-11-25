---
        name: pandas-python
        description: >-
          Use for writing, reviewing, debugging, testing, or optimizing Python pandas Series, DataFrame, Index, groupby, merge, reshape, dtype, missing-value, and time-series code. Do not use for Polars-only expressions, Xarray named arrays, PySpark, or generic table tasks without a pandas boundary.
        argument-hint: "[pandas Python task, code, contract, or failure]"
        ---

        # pandas Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `Series` | A one-dimensional labeled array with one dtype. | Operations align by index labels unless explicitly converted to positions. |
| `DataFrame` | A two-dimensional labeled collection of Series. | Column dtypes and index semantics remain independent. |
| `Index` | The label and alignment key for an axis. | Duplicate labels can make selection and joins non-scalar. |
| `GroupBy` | A deferred split/combine object. | Complete it with an explicit aggregation, transform, filter, or apply contract. |
| `Extension dtype` | Nullable or semantic dtype beyond NumPy primitives. | Preserve it explicitly across missing values and interchange. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Inspect shape, index uniqueness, column labels, dtypes, nulls, and row grain.
2. Choose label or positional semantics and state alignment behavior.
3. Define join/group/reshape cardinality and output ordering.
4. Preserve nullable and temporal types through the transformation.
5. Test duplicates, missing keys, empty groups, and Copy-on-Write independence.

        ## Decision rules

        - Use `.loc` for labels and `.iloc` for positions; never infer which one integer-looking labels mean.
- Treat binary operations as label-aligned; use arrays only when positional semantics are explicitly required.
- Declare join keys, expected cardinality, null-key policy, suffixes, and row-order contract; use `validate` when known.
- Use one assignment operation such as `.loc[...] = ...` and rely on Copy-on-Write semantics; do not chain indexers.
- Choose nullable dtypes deliberately and test missing values without equating `NA`, `NaN`, and `None` in every context.
- Prefer vectorized/grouped operations; use apply only when its input/output shape and dtype are explicit and tested.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `pandas.validated-many-to-one` and `pandas.verify-join-cardinality`: join facts to unique dimensions without silent row multiplication.
- `pandas.nullable-named-aggregation` and `pandas.verify-missing-group-policy`: aggregate nullable values with an explicit missing-key policy.
- `pandas.copy-on-write-update` and `pandas.verify-input-independence`: return an independent updated frame without chained assignment.

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
