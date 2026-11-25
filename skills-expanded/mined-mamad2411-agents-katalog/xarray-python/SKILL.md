---
        name: xarray-python
        description: >-
          Use for writing, reviewing, debugging, or testing Python Xarray labeled N-dimensional DataArray and Dataset workflows, including coordinates, alignment, indexing, groupby, resample, rolling, weighted reduction, Dask-backed execution, and NetCDF/Zarr I/O. Do not use for pandas-only tables or unlabeled NumPy arrays.
        argument-hint: "[Xarray Python task, code, contract, or failure]"
        ---

        # Xarray Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `DataArray` | N-dimensional values plus named dimensions and coordinates. | Operations align by coordinate labels, not raw axis position. |
| `Dataset` | A mapping of aligned named variables with shared coordinates. | Variables may have different dimension subsets and dtypes. |
| `coordinate/index` | Labels that define selection and alignment semantics. | Duplicates, order, calendars, and join policy affect correctness. |
| `lazy chunked array` | A deferred Dask-backed computation graph. | Chunking and `.compute()` boundaries control execution and memory. |
| `encoding` | Storage metadata separate from in-memory attrs and dtype. | Round-trip requirements must be stated at I/O boundaries. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Inspect variables, dimensions, coordinates, indexes, chunks, dtypes, and calendars.
2. Declare alignment and join policy before arithmetic or merge.
3. Choose label/position indexing and output dimension order.
4. Define reduction weights, missing-value behavior, and execution boundary.
5. Verify representative coordinates plus storage round trip when writing data.

        ## Decision rules

        - Name dimensions and coordinates from domain meaning; never rely on an axis number when labels are available.
- Choose exact, inner, outer, left, or right alignment explicitly when combining independently sourced arrays.
- Use `.sel` for coordinate labels and `.isel` for integer positions; state nearest/tolerance policy for approximate selection.
- Define missing-data and weight normalization policy for reductions, especially when weights and values have different masks.
- Preserve laziness across large chunked data and compute only at a tested consumer boundary.
- Test dimension names, coordinate order/uniqueness, variable dtype, attrs/encoding, and calendar behavior where relevant.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `xarray.exact-aligned-arithmetic` and `xarray.verify-coordinate-contract`: prevent silent coordinate union during arithmetic.
- `xarray.mask-aware-weighted-reduction` and `xarray.verify-weight-normalization`: compute weighted means with explicit missing-data support.
- `xarray.time-resample-contract` and `xarray.verify-bin-and-order-semantics`: aggregate irregular observations into explicit daily bins.

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
