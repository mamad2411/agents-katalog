---
name: causal-analysis
description: >
  Use when designing, executing, or reviewing causal inference analyses — covers
  difference-in-differences, regression discontinuity, instrumental variables,
  synthetic control, propensity score matching, CATE estimation, meta-learners,
  DML, and uplift modeling. Trigger on "causal analysis", "causal inference",
  "treatment effect", "diff-in-diff", "regression discontinuity", "instrumental
  variables", "synthetic control", "propensity score", "counterfactual", "uplift
  model", "CATE", "double machine learning", "causal forest", "A/B test beyond
  ATE", "heterogeneous treatment effects", "observational study design",
  "natural experiment".
owners:
  - analytics
---

# Causal Analysis Copilot

Guide the user through the full causal inference workflow: problem formulation, method selection, implementation, evaluation, and validation.

## Causal Inference Workflow

Follow these five steps in order. Each step builds on the previous one — skipping steps leads to invalid conclusions.

### 1. Formulate

Define the causal question precisely:

- **Treatment (T):** The intervention or exposure of interest
- **Outcome (Y):** The variable you want to affect
- **Covariates (X):** Pre-treatment features that predict the outcome
- **Confounders (W):** Variables that affect both T and Y

State the estimand explicitly — ATE (average treatment effect), ATT (effect on the treated), CATE (conditional/heterogeneous effects), or LATE (local average for compliers). Draw a DAG if the causal structure is complex or ambiguous.

### 2. Identify

Before selecting a method, verify the assumptions that make causal estimation possible. Challenge each assumption explicitly — this is where most causal analyses go wrong.

| Assumption | What it means | When it matters |
|---|---|---|
| Unconfoundedness | No unmeasured common causes of T and Y | All observational methods |
| Overlap / positivity | Every unit has nonzero probability of each treatment | IPW, matching, DML |
| SUTVA | One unit's treatment doesn't affect another's outcome | Everything (violated in marketplace/network settings) |
| Parallel trends | Treatment and control groups would have followed the same trend absent treatment | Difference-in-differences |
| Continuity at cutoff | No manipulation or discontinuity in potential outcomes at the threshold | Regression discontinuity |
| Exclusion restriction | Instrument affects Y only through T | Instrumental variables |

If an assumption is questionable, say so. Recommend sensitivity analysis rather than proceeding as if everything holds.

### 3. Select Method

Use this table to match the data situation to the right method:

| Scenario | Method | Key Assumption | Python Library |
|---|---|---|---|
| RCT data, want heterogeneous effects | Meta-learners (T/X/DR-Learner), CausalForest | Randomization | `econml`, `causalml` |
| Observational, continuous treatment | Double Machine Learning (DML) | Unconfoundedness + overlap | `econml` (`LinearDML`, `NonParamDML`) |
| Observational, discrete treatment | DR-Learner or DML | Unconfoundedness + overlap | `econml` |
| Policy change with pre/post data | Difference-in-Differences | Parallel trends | `statsmodels`, `linearmodels` |
| Policy with sharp eligibility cutoff | Regression Discontinuity (RDD) | Continuity at cutoff | `rdrobust` |
| Endogenous treatment, valid instrument available | Instrumental Variables (IV/2SLS) | Exclusion restriction + relevance | `linearmodels`, `econml` (IV variants) |
| No good control group, few treated units | Synthetic Control Method | Convex combination fits pre-period | `SparseSC`, `SyntheticControlMethods` |
| Observational, strong covariate imbalance | Propensity Score Matching/Weighting (IPW, AIPW) | Unconfoundedness + overlap | `causalml`, `econml`, `dowhy` |
| RCT, want optimal treatment policy | Policy learning / uplift targeting | Randomization | `econml` (`PolicyTree`, `DRPolicyForest`) |

When multiple methods are viable, present the trade-offs rather than picking one silently.

### 4. Implement

Generate analysis code using the appropriate Python library. Key implementation principles:

- **Always use cross-fitting** for ML-based estimators (DML, DR-Learner, CausalForest). Without it, nuisance model overfitting biases CATE estimates.
- **Include diagnostic checks** — covariate balance tables for matching, first-stage F-statistics for IV, pre-trend tests for DiD.
- **Report confidence intervals**, not just point estimates.

### 5. Evaluate and Validate

Never skip validation. The right evaluation approach depends on the data context.

**With experimental holdout data:**

- CATE band monotonicity — top predicted band should have highest observed ATE
- Cumulative gain curve — should dominate random baseline
- Qini curve and AUUC for uplift model comparison
- Uplift@K for budget-constrained targeting

**Without ground truth (observational):**

- `RScorer` (`econml.score.RScorer`) — positive score means the model captures heterogeneity beyond a constant effect
- `DRTester` (`econml.validate.DRTester`) — runs BLP test, calibration test, and Qini test
- DR-Loss as cross-check to avoid referee bias

**Robustness checks (always run these):**

- Placebo treatment refutation — effect should vanish with random treatment
- Random common cause refutation — estimate should be stable
- Data subset refutation — estimate should be stable across subsets
- Sensitivity analysis — minimum confounding strength needed to invalidate the result

Never use prediction metrics (MSE, R-squared) to evaluate causal models. The counterfactual outcome is unobserved, so predictive accuracy is meaningless for causal estimation.

## Meta-Learner Hierarchy

When estimating CATE from RCT data, meta-learners vary in complexity and robustness:

- **S-Learner** — single model with T as a feature. Simplest, but regularization can shrink the treatment effect toward zero.
- **T-Learner** — separate models per treatment arm. Better separation, but ignores shared structure and can be noisy with small samples.
- **X-Learner** — imputed residuals with propensity weighting. Generally preferred when treatment/control group sizes differ substantially.
- **DR-Learner** — doubly robust. Preferred when confidence intervals matter — robust to misspecification of either the outcome or propensity model.

Start with DR-Learner as the default unless there's a reason to prefer something simpler.

## Common Pitfalls

Watch for these mistakes — they invalidate causal conclusions:

- **Prediction vs. causation confusion** — E[Y|X] is not the same as dE[Y|X]/dT. Predictive models answer "what will happen?" while causal models answer "what would change if we intervened?"
- **Prediction metrics for causal models** — MSE and R-squared evaluate predictions, not causal effects. The counterfactual is never observed.
- **Skipping cross-fitting** — overfits nuisance models, biasing CATE estimates downward or upward unpredictably.
- **Post-treatment variable leakage** — including variables affected by treatment in covariates absorbs the treatment effect.
- **Feedback loops** — if model predictions influence future treatment assignment, the training data distribution shifts.
- **Overlap violations** — propensity scores near 0 or 1 mean some units are practically never (or always) treated. Trim or truncate extreme weights.
- **Ignoring SUTVA** — interference between units (e.g., marketplace network effects, cannibalization) violates the independence assumption.
- **DiD without parallel trends testing** — claiming causality from DiD without evidence that trends were parallel pre-treatment is unsupported.
- **Weak instruments** — first-stage F-statistic below 10 indicates the instrument barely predicts treatment, making IV estimates unreliable.
- **Cherry-picking RDD bandwidth** — use data-driven bandwidth selection (e.g., `rdrobust`) rather than manual tuning.

## Python Libraries Reference

| Library | Best for |
|---|---|
| `econml` | CATE estimation: DML, meta-learners, DR-Learner, CausalForest, DRTester, RScorer, policy learning |
| `dowhy` | End-to-end causal framework: identify, estimate, refute. DAG-based reasoning. Integrates with econml estimators |
| `causalml` | Uplift modeling, meta-learners, uplift trees (Uber open-source) |
| `scikit-uplift` | Uplift evaluation metrics: AUUC, Qini coefficient |
| `statsmodels` | DiD, regression-based methods |
| `linearmodels` | IV/2SLS, panel data models, fixed effects |
| `rdrobust` | Regression discontinuity with optimal bandwidth selection |
