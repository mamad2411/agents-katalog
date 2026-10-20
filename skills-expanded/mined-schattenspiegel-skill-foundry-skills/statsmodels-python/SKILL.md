---
        name: statsmodels-python
        description: >-
          Use for writing, reviewing, debugging, or interpreting Python statistical models with statsmodels, including formulas, regression, GLM, time series, robust covariance, diagnostics, prediction intervals, and inference. Do not use for sklearn prediction pipelines or Bayesian posterior workflows.
        argument-hint: "[statsmodels Python task, code, contract, or failure]"
        ---

        # statsmodels Python

        Use the smallest explicit execution contract that preserves semantics. Inspect
        the installed version before relying on a drifting signature. State ownership,
        input and output shapes, ordering, failure behavior, and the verification command
        before writing substantial code.

        ## Object and execution model

        | Object | Meaning | Boundary |
        |---|---|---|
        | `model specification` | A likelihood or estimating-equation family plus design. | Formula coding, intercept, link, and covariance assumptions define estimands. |
| `fitted result` | Parameters, covariance, diagnostics, and prediction methods. | Check convergence and data rows retained before inference. |
| `design matrix` | Encoded predictors with column semantics. | Categorical levels and transformations must match prediction data. |
| `covariance estimator` | An uncertainty model such as classical, HC3, cluster, or HAC. | Choose it from dependence and sampling, not coefficient preference. |
| `prediction frame` | Mean and possibly observation uncertainty at new exog. | Mean confidence and observation intervals answer different questions. |

        Read [the object model](references/object-model.md) when the task mixes two
        objects or crosses an execution boundary.

        ## Workflow

        1. Define estimand, outcome family, sampling unit, clustering/order, and missing-data policy.
2. Build and inspect the formula/design matrix and retained observations.
3. Fit with the intended likelihood and covariance estimator.
4. Check convergence, residual, influence, and specification diagnostics.
5. Generate predictions with explicit exog and the correct uncertainty target.

        ## Decision rules

        - State estimand, response distribution, link, design formula, intercept, weights, and dependence assumptions before fitting.
- Choose classical, heteroskedasticity-robust, cluster-robust, or HAC covariance from the sampling process.
- Inspect dropped rows, rank, convergence, residuals, influence, and model-specific diagnostics before interpreting p-values.
- Preserve categorical levels and formula transformations when constructing prediction data.
- Distinguish confidence intervals for the conditional mean from prediction intervals for new observations.
- Treat association and conditional estimates as causal only when the identification design independently supports that claim.

        If a required fact is unknown, inspect the target code, installed signature,
        schema, shape, or lifecycle owner. Do not replace an unknown with a permissive
        fallback. See [the decision guide](references/decision-guide.md).

        ## Complex solution routes

        Load only the matching section of
        [the evaluated recipes](references/recipes-solutions.md):

        - `statsmodels.formula-ols-robust` and `statsmodels.verify-design-and-covariance`: fit a categorical regression with robust covariance.
- `statsmodels.prediction-summary-frame` and `statsmodels.verify-interval-semantics`: return distinct prediction uncertainty targets.
- `statsmodels.hac-ordered-fit` and `statsmodels.verify-time-and-lag-contract`: use HAC covariance only on verified time ordering.

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
