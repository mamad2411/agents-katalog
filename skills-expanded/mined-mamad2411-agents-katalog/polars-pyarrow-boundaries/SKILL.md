---
        name: polars-pyarrow-boundaries
        description: >-
          Use when Python code crosses between Polars and PyArrow tables, arrays, schemas, record batches, Parquet, or Arrow C/Data interfaces, especially for timestamp, dictionary, nested, nullability, chunking, and zero-copy contracts. Do not use for Polars-only transformations or PyArrow-only dataset work with no interchange.
        argument-hint: "[Polars and PyArrow Boundaries task, code, contract, or failure]"
        ---

        # Polars and PyArrow Boundaries

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `Polars DataFrame/Series` | Materialized columnar values with Polars dtypes. | Conversion can rechunk, normalize, or reject Arrow representations. |
| `Arrow Table/Array` | Immutable chunked columnar values plus Arrow schema. | Chunking, offsets, dictionary encoding, and metadata are observable. |
| `schema` | Field names, logical types, nullability, and metadata. | Value equality alone cannot prove a boundary contract. |
| `buffer ownership` | The lifetime and sharing of underlying memory. | Zero-copy is conditional and must not be promised without buffer evidence. |
| `storage boundary` | Parquet/IPC or consumer protocol after conversion. | Test the final consumer semantics, not just an intermediate type. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Inspect both installed versions and source/target schemas including field metadata.
2. Classify each dtype as exact, safely normalizable, lossy, unsupported, or version-sensitive.
3. Convert at one named boundary and avoid Python row objects.
4. Verify values, nulls, order, dtype/unit/timezone, nested shape, and consumer behavior.
5. Measure buffer sharing separately if zero-copy affects performance requirements.

        ## Decision rules

        - Declare names, order, Arrow and Polars dtypes, nullability, timezone, precision, nested shape, and metadata requirements before conversion.
- Use `pl.from_arrow` and `.to_arrow()` as explicit boundaries, then compare schemas and representative null/value behavior.
- Treat zero-copy as an optimization requiring compatible representation, stable ownership, and buffer-level evidence; correctness must not depend on it.
- Preserve timezone and timestamp unit deliberately; Python-object conversion can truncate nanoseconds and erase Arrow distinctions.
- Decide whether dictionary encoding and chunk boundaries are semantic, performance-only, or allowed to normalize.
- Version-ground unstable or evolving nested and extension-type behavior against both installed libraries.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `boundary.timestamp-schema-roundtrip` and `boundary.verify-nanosecond-timezone-values`: preserve timestamp units, timezone, nulls, and nanoseconds.
- `boundary.chunk-normalization` and `boundary.verify-nullability-and-values`: normalize chunks while preserving typed nullable values.
- `boundary.dictionary-nested-policy` and `boundary.verify-decoded-and-nested-values`: cross categorical and nested columns without silent semantic loss.

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
