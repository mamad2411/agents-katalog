---
name: evaluate-model
description: Evaluate a trained model the way its problem type actually demands — the right metric family for classification, regression, ranking or forecasting, calibration checked rather than assumed, performance broken out by subgroup, comparison against the baseline restated with uncertainty, error analysis on real misclassified/mispredicted cases, and an explicit statement of what the numbers do NOT license someone to conclude. Use before a model is approved for production, before a stakeholder repeats an accuracy or R² number in a meeting, when a metric was picked before the problem was understood, or when subgroup or fairness performance has never been checked. Produces docs/models/<model>.evaluation.md.
allowed-tools: Read Grep Glob Bash Write Edit mcp__plugin_foundry-core_foundry__blackboard_read
argument-hint: "[model-card] [--subgroup column]"
user-invocable: true
context: fork
agent: foundry-data:model-evaluator
model: sonnet
effort: medium
background: false
metadata:
  foundry.vertical: data
  foundry.io: "plan.v1 (from train-model) -> review.v1 + docs/models/<model>.evaluation.md"
license: Apache-2.0
---

# Evaluate a model

One model, one metric family chosen for the right reason, and one written statement of what the
result does and does not support. The deliverable is not a metrics dashboard — it is a document a
sceptic can use to decide whether to ship, and that names its own blind spots.

Run this after `train-model` has already produced a baseline-comparison verdict; this skill goes
deeper than that gate — calibration, subgroups, error analysis, and the limits of the numbers.

## When not to use this

- **No baseline comparison exists yet** → `train-model` step 6 first; evaluating a model in
  isolation, with no comparison point, invites a number to be read as good with nothing to be good
  relative to.
- **The system under evaluation is an LLM or agent producing free-form or judged output** →
  `foundry-ai:build-eval-suite`. That skill's judge calibration, rubric and k-run protocol are for
  non-deterministic, judged output — using accuracy/F1 machinery on generated text produces a
  number that looks rigorous and measures nothing meaningful.
- **You are evaluating retrieval quality**, not a predictive model → `foundry-ai:build-rag-pipeline`
  step 2 and its recall/MRR/nDCG metrics.
- **The goal is choosing which model to train, not judging one already trained** → back to
  `train-model`.

## Step 1 — pick the metric family for the actual problem, before computing anything

State the task type and the metric family it implies; do not default to accuracy or R² out of
habit. Full table with when each metric misleads: `references/metrics-by-problem-type.md`.
Non-exhaustive pointers:

- **Imbalanced classification** — accuracy is close to meaningless; use precision/recall/F1 per
  class, PR-AUC (more informative than ROC-AUC under strong imbalance), and confusion matrices with
  counts, not only rates.
- **Regression with a skewed target or business-asymmetric errors** — report MAE and RMSE together
  (RMSE penalises large errors more; the gap between them tells you about outlier sensitivity), and
  check whether over- and under-prediction have different real costs before picking one number to
  headline.
- **Forecasting** — MAPE breaks near zero values; prefer MASE or a comparison against the seasonal-
  naive baseline's error, and always report per-horizon error (1-step-ahead error is not
  10-steps-ahead error).
- **Ranking/recommendation** — precision@k/recall@k/nDCG at the k that matches how the ranking is
  actually consumed (top-3 shown to a user is not top-100).

## Step 2 — restate the baseline comparison with uncertainty

Pull the baseline score and the model score from the `train-model` card — and from the artifact
this skill declares as its input, with `blackboard_read` on
`.foundry/blackboard/<wave>/train-model.json`, so the comparison is made against what the
predecessor actually recorded rather than a doc that may have drifted from it — then report the
difference with a confidence interval or a paired significance test across the same folds
(bootstrap over rows/folds, or McNemar's test for paired binary classification outcomes). "The
model scores 3 points higher" without an interval is not yet a finding — report whether the
interval excludes zero, and if it does not, say plainly that no improvement is demonstrated at
this sample size.

## Step 3 — calibration, for any model whose output is used as a probability or a score

A model can rank cases correctly (good AUC) while its predicted probabilities are wrong in
absolute terms (bad calibration) — and both properties matter for different downstream uses.

- Plot or tabulate a **reliability diagram**: bucket predictions by predicted probability, compare
  to the observed frequency in each bucket.
- Report the **Brier score** as a single-number summary, alongside the reliability diagram, not
  instead of it — a good Brier score can still hide a badly miscalibrated middle range.
- If miscalibrated and the probability itself is used downstream (for thresholding, for ranking by
  expected value, for a risk score shown to a human), apply and report a calibration method
  (Platt scaling, isotonic regression) fit **only on a calibration split disjoint from the test
  set used to report final numbers** — calibrating on the same data you report performance on
  reuses it a second time.

Full method and worked reliability-diagram construction: `references/calibration-and-subgroups.md`.

## Step 4 — performance per subgroup, not only in aggregate

Pick subgroups from the domain, not arbitrarily: the groups a stakeholder will ask about (region,
age band, customer tier, device type, protected characteristics where legally and ethically
appropriate to check), and any group flagged during `explore-dataset` as under-represented.

- Report the primary metric **per subgroup**, with the subgroup's row count next to it — a
  subgroup with too few rows supports no independent conclusion, and that must be said rather than
  quietly averaged away into the aggregate.
- An aggregate improvement that hides a regression in one subgroup is the single most common way a
  "the model is better" claim turns into an incident after deployment. Check for this explicitly,
  every time.

Method: `references/calibration-and-subgroups.md`.

## Step 5 — error analysis on real cases

- Pull a sample of the model's worst misses (highest-confidence wrong classifications, largest
  residuals) and read them, not just their statistics.
- Build a lightweight failure taxonomy from what is actually there (e.g. "confuses class A and B
  under condition X", "systematically over-predicts for a specific subgroup", "residuals grow with
  a specific feature's magnitude — a sign of a missing interaction or heteroscedasticity"). Count
  occurrences per category; the counts decide what to fix next, the same way they decide an eval
  taxonomy's priorities in `foundry-ai:build-eval-suite` step 1.
- For regression, plot or tabulate residuals against each major feature and against the predicted
  value — a pattern (residuals growing with the prediction, or clustering by a feature) signals a
  missing feature or the wrong model family, not just noise.

Playbook and worked failure taxonomy: `references/error-analysis-playbook.md`.

## Step 6 — write what the numbers do NOT license

State explicitly, as its own section: what population the test set represents and what it does
not (a model tested on last quarter's data says nothing certain about a shifted population next
year); whether performance was checked under the specific conditions production will actually
present (latency-truncated input, adversarial input, a subgroup too small to have been checked);
and whether "beats the baseline" has been confirmed to survive normal week-to-week variation, or
was observed on one run. A model card that omits this section is asserting more than it measured.

## Step 7 — write it down

`docs/models/<model>.evaluation.md`: task type and metric family with the reason it was chosen;
baseline comparison with interval/test result; calibration findings (reliability diagram summary,
Brier score, and whether recalibration was applied); per-subgroup performance table with row
counts; error-analysis taxonomy with counts and example cases; the explicit "what this does not
show" section; recommendation (ship / do not ship / ship with a named mitigation); review date
≤ 90 days.

Emit `review.v1` to `.foundry/blackboard/<wave>/evaluate-model.json`: `dimension`
`model-evaluation`, `target` the model version, `verdict` carrying the ship gate
(`pass` = ship, `pass-with-comments` = ship with the named mitigation, `block` = do not ship),
`metrics` carrying the per-subgroup, calibration and baseline-comparison numbers, and one
`finding.v1` entry in `findings[]` for every subgroup or condition left unchecked — each with the
`failureScenario` that entry requires. A ship recommendation is not a `finding.v1`: that schema
sets `additionalProperties: false`, requires `failureScenario`, and its `verdict` enum is
confirmed/plausible/refuted, so a recommendation written into one cannot validate.

## Exit criteria

1. Metric family matches the task type, with the choice justified in one sentence, not assumed.
2. Baseline comparison restated with an interval or a paired significance test, not a bare
   difference.
3. Calibration checked (reliability diagram plus Brier score) for any model whose output is used
   as a probability or score.
4. Performance reported per relevant subgroup, each with its row count, including a check for
   aggregate-hides-subgroup-regression.
5. Error analysis performed on real misses with a counted failure taxonomy, not only aggregate
   statistics.
6. An explicit "what this evaluation does not show" section is present and specific to this model,
   not boilerplate.
7. A ship/do-not-ship/ship-with-mitigation recommendation is stated.
8. `docs/models/<model>.evaluation.md` exists; `review.v1` validates, with the ship gate in
   `verdict` and every unchecked subgroup as a `finding.v1` in `findings[]`.

## Degradation

- **Test set too small for a subgroup breakdown to be meaningful** → report the subgroup counts
  anyway, mark subgroups below a stated minimum count (state it) as "insufficient data to
  conclude", and do not average them silently into a number that implies they were checked.
- **No ground truth available yet for calibration** (e.g. long-delayed labels) → report what can be
  checked now (discrimination via AUC/ranking metrics) and record calibration as an open item with
  an owner and a date when labels will be available, rather than skipping the section.
- **Protected-characteristic subgroup analysis is legally or organisationally out of scope for this
  evaluator** → say so explicitly and name who owns that check, rather than silently omitting it.
- **`foundry` MCP server unavailable** → read
  `.foundry/blackboard/<wave>/train-model.json` with `Read` instead of `blackboard_read`, write the
  `review.v1` artifact to that path yourself, and state in the summary that it was not
  schema-validated.
- **`superpowers` installed** → use `superpowers:verification-before-completion` before the
  ship/do-not-ship recommendation is communicated to a stakeholder; treat a recommendation stated
  without this check as unverified. If absent, re-derive the headline numbers from the raw
  per-row/per-fold results by hand as the equivalent check before writing the recommendation.

## Deliberately not covered

Choosing the model or the baseline (`train-model`), dataset-level leakage and quality
(`explore-dataset`), packaging and monitoring a model already approved (`productionise-notebook`),
and judged evaluation of generative/agentic output (`foundry-ai:build-eval-suite`).

## Bundled references

- `references/metrics-by-problem-type.md` — classification, regression, ranking, forecasting and
  clustering metrics, with the condition under which each one misleads.
- `references/calibration-and-subgroups.md` — reliability diagrams, Brier score, recalibration
  methods, and the subgroup-breakdown protocol including minimum-count handling.
- `references/error-analysis-playbook.md` — building a failure taxonomy from real misses, residual
  analysis for regression, and turning findings into a prioritised fix list.
