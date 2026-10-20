---
        name: datetime-zoneinfo-python
        description: >-
          Use for writing, reviewing, debugging, or testing Python datetime, date, timedelta, timezone, and zoneinfo code, especially UTC conversion, DST gaps and folds, recurring local schedules, parsing, and interval boundaries. Do not use for Polars/pandas-only time-series operations or generic string formatting.
        argument-hint: "[datetime and zoneinfo Python task, code, contract, or failure]"
        ---

        # datetime and zoneinfo Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `instant` | One point on the UTC timeline. | Represent it with an aware datetime and compare after UTC normalization. |
| `wall time` | A calendar reading in a locality. | It can be nonexistent or ambiguous at an offset transition. |
| `ZoneInfo` | Rules for a named IANA time zone. | It is not a fixed offset and requires available time-zone data. |
| `fold` | The selected occurrence of an ambiguous wall time. | It does not repair nonexistent times. |
| `interval` | A start and end with an inclusion policy. | Default to half-open only when the contract states it. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Classify each value as instant, wall time, date, duration, recurrence, or interval.
2. Establish the source zone, target zone, ambiguity policy, and precision.
3. Resolve or reject local times before converting them to UTC instants.
4. Perform timeline arithmetic on instants and calendar arithmetic on civil schedules.
5. Test gaps, folds, boundaries, serialization, and round trips.

        ## Decision rules

        - Use aware UTC datetimes for instants and named zones for user-facing civil time; never compare aware and naive values.
- Validate local wall times by round-tripping through UTC; require an explicit fold when both occurrences are valid.
- Add calendar recurrences in local date/time space, then resolve each occurrence; do not add 24 hours to preserve a local appointment.
- Define interval inclusion and normalize both endpoints and probes to UTC before comparison.
- Parse only accepted formats and offsets; do not attach `tzinfo` to reinterpret an instant from another zone.
- Inject `now` into business logic and test transition dates with the same tzdata policy as production.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `datetime.resolve-local` and `datetime.verify-gap-fold`: reject nonexistent local times and require an ambiguity choice.
- `datetime.weekly-civil-recurrence` and `datetime.verify-dst-recurrence`: preserve a recurring local appointment across DST.
- `datetime.half-open-window` and `datetime.verify-window-boundaries`: apply an explicit half-open UTC interval contract.

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
