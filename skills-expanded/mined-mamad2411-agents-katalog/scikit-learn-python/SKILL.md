---
        name: scikit-learn-python
        description: >-
          Use for writing, reviewing, debugging, or evaluating Python machine-learning workflows with scikit-learn estimators, transformers, pipelines, model selection, metrics, preprocessing, and persistence. Do not use for PyTorch or JAX training loops, statistical inference, or generic NumPy calculations.
        argument-hint: "[scikit-learn Python task, code, contract, or failure]"
        ---

        # scikit-learn Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `estimator` | An object whose fit learns state from X and possibly y. | Never fit it on validation or test information. |
| `transformer` | An estimator that maps features through transform. | Learn preprocessing inside the same training split as the estimator. |
| `Pipeline` | An ordered preprocessing and final-estimator unit. | Cross-validation clones and fits the whole unit per split. |
| `splitter` | A policy yielding train/test indices. | Choose it from independence, grouping, ordering, and class-balance assumptions. |
| `scorer` | A maximization-oriented evaluation contract. | Loss scorers may be negated; inspect sign and response method. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Define prediction unit, target, feature provenance, and leakage boundary.
2. Choose preprocessing and estimator as one cloneable pipeline.
3. Choose a splitter that preserves the data-generating independence structure.
4. Evaluate with explicit scoring and inspect per-split failures and variance.
5. Refit only after selection, then verify schema and test-set behavior.

        ## Decision rules

        - Place every data-dependent preprocessing step inside a Pipeline or ColumnTransformer before cross-validation.
- Choose KFold, StratifiedKFold, GroupKFold, or a time-ordered splitter from the sampling process; random splitting is not a neutral default.
- Keep the untouched test set outside model selection and threshold tuning; report both selection and final evaluation procedures.
- Set random_state on stochastic estimators and splitters, but do not confuse repeatability with uncertainty estimation.
- Use task-appropriate metrics and state positive class, averaging, sample weights, and threshold policy.
- Validate feature order, names, dtypes, missing-value handling, and learned-version compatibility at prediction boundaries.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `sklearn.pipeline-cross-validation` and `sklearn.verify-no-preprocessing-leakage`: cross-validate preprocessing and classification as one unit.
- `sklearn.group-aware-splitting` and `sklearn.verify-group-disjointness`: prevent entity leakage across validation folds.
- `sklearn.inference-schema-guard` and `sklearn.verify-feature-and-class-contract`: reject drifted feature schemas at inference.

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
