---
name: ml-experiments
description: Runs trustworthy machine learning experiments - problem and metric framing, baselines, correct train/validation/test splits, leakage prevention, reproducibility, experiment tracking, imbalance, cross-validation, hyperparameter search, error analysis, model cards, train/serve skew and drift monitoring. Use when training or evaluating a classical ML or deep learning model, results look too good, a model fails in production, or setting up an ML project or notebook. Not for prompting or evaluating LLM APIs (use llm-evals).
license: MIT
---

# ML Experiments

A model is only as good as its evaluation. Fix the metric and the split before training anything, beat a simple baseline, never let information from the test set or the future leak into training, and make every result reproducible.

## When to use

- Starting a modeling project, notebook or Kaggle-style task.
- Comparing models, features or hyperparameters.
- Results look suspiciously good, or offline gains don't show up in production.
- Preparing a model for deployment or monitoring.

## Workflow

1. **Frame the problem.** What decision will the prediction drive? What is predicted, for which unit (user, transaction, day), at what moment, with what data available at that moment? Write it down.
2. **Choose the metric tied to the goal**, plus guardrail metrics. Agree on what improvement matters before running experiments.
3. **Define the split** to mirror how the model will be used (see table). Lock away a test set.
4. **Build baselines**: a trivial one (majority class, last value, mean) and a simple one (logistic/linear regression, gradient-boosted trees, or a heuristic the business uses today).
5. **Check for leakage** before trusting any number. See [references/leakage-checklist.md](references/leakage-checklist.md).
6. **Iterate on the validation set**, tracking every run (code version, data version, parameters, metrics).
7. **Do error analysis** by slice before adding complexity.
8. **Evaluate once on the test set** with the final choice. Report with uncertainty.
9. **Prepare for production**: same feature code for training and serving, a model card, and monitoring.

## Metrics

| Problem | Typical metrics | Watch out for |
|---|---|---|
| Balanced classification | Accuracy, F1, ROC AUC | Accuracy hides per-class failures |
| Imbalanced classification | PR AUC, precision/recall at the operating threshold, recall at fixed precision | ROC AUC looks good even when positives are rare |
| Probabilities used directly | Log loss, Brier score, calibration plot | A good ranker can be badly calibrated |
| Regression | MAE, RMSE, MAPE (only if no near-zero targets) | RMSE dominated by outliers |
| Ranking / recommendation | nDCG@k, recall@k, MAP | Offline metrics vs online behavior |
| Forecasting | MAE/MASE per horizon, against a naive seasonal baseline | Evaluating on shuffled time series |

Choose the decision threshold on validation data against the business cost of false positives vs false negatives, not 0.5 by default.

## Splits

| Data | Split | Why |
|---|---|---|
| Independent rows | Random (stratified for classification) | Simple case |
| Time matters (forecasting, churn, fraud, anything predicting the future) | Time-based: train on the past, validate and test on later periods; gap if labels mature late | Random splits leak the future |
| Several rows per entity (user, patient, device, document) | Group split: all rows of an entity in one split | Otherwise the model memorizes entities |
| Small data | Cross-validation (stratified, grouped or time-series folds as above) | More stable estimate |

Rules:

- The test set is touched once, at the end. If you look at it to make decisions, it becomes a validation set; carve out a new one if you can.
- Fit all preprocessing (scalers, imputers, encoders, feature selection, oversampling) inside the training fold only. Use pipelines (e.g. scikit-learn `Pipeline`) so cross-validation does this correctly.
- Deduplicate before splitting; near-duplicates across splits inflate scores.

## Reproducibility

- Seed every source of randomness (Python, NumPy, framework, data loaders) and record the seed. GPU training may still be nondeterministic; know which ops are, and report variance across seeds for important comparisons.
- Pin the environment (lock file or container image) and record library versions.
- Version data: a dataset snapshot ID, hash or a data versioning tool, plus the query that produced it.
- Record the git commit for each run and refuse to report results from uncommitted code.
- Keep notebooks for exploration; move training and evaluation into scripts or modules that run end to end from one command.

## Experiment tracking

Log for every run: code commit, data version, config and hyperparameters, metrics on train and validation, training time, hardware, and artifacts (model, plots, confusion matrix). Use a tracker such as MLflow or Weights & Biases, or at minimum an append-only results file. Name the question each experiment answers.

## Common techniques, used carefully

- **Class imbalance**: first use the right metric and threshold. Then try class weights. Resampling (under/oversampling, SMOTE) only inside training folds, never before the split.
- **Hyperparameter search**: random search or Bayesian optimization over sensible ranges beats a large grid. Tune on validation (or inner CV), with a fixed budget. Nested CV when the dataset is small and you need an unbiased estimate.
- **Feature engineering**: every feature must be computable at prediction time with the data available then.
- **Deep learning**: overfit a tiny batch first to prove the pipeline learns; watch train vs validation curves; use early stopping on validation; check the input pipeline (augmentations, normalization) by looking at actual batches.

## Error analysis

- Break metrics down by slice: segment, region, device, data source, time period, label class, input length.
- Read the worst errors and a random sample of errors. Look for label noise, missing features, distribution gaps.
- Fix data and labels before reaching for bigger models.
- Check fairness-relevant slices where the model affects people, and report gaps.

## Reporting results

Every comparison you report should include:

- The metric on validation (and test, once, for the final model) with uncertainty: standard deviation across CV folds or seeds, or a bootstrap confidence interval.
- The baselines on the same split, so the gain is visible.
- The split method, dataset version and date range, and the number of rows and positives.
- Guardrail metrics (latency, model size, calibration, slice gaps) next to the main metric.
- What was tried and didn't work, briefly. It saves the next person from repeating it.

If two candidates are within noise of each other, prefer the simpler, cheaper, more explainable one.

## Production readiness

- **Train/serve skew**: use the same feature code (or feature store) in training and serving; compare feature distributions from serving logs against training data.
- **Model card**: intended use, out-of-scope uses, training data, metrics overall and by slice, known limitations, ethical considerations, owner.
- **Monitoring**: input drift (feature distributions), prediction drift, data quality (nulls, ranges, schema), and actual performance once labels arrive. Alert thresholds and a retraining or rollback plan.
- **Shadow or canary** before full rollout when the model drives real decisions; ask the user before switching production traffic.

## Anti-patterns

- **No baseline** - a complex model that barely beats predicting the mean.
- **Random split on time-dependent data.**
- **Preprocessing fit on the full dataset**, then split.
- **Tuning on the test set**, or reporting the best of many test-set runs.
- **Single-run comparisons** where seed variance exceeds the difference.
- **Accuracy on imbalanced data.**
- **Notebook-only pipelines** that can't be re-run from scratch.
- **Ignoring calibration** when probabilities are used as probabilities.

## Done when

- The prediction task, unit, timing and metric are written down and agreed.
- The split mirrors production use, the test set was used once, and the leakage checklist passed.
- The model beats trivial and simple baselines by more than run-to-run variance.
- Every reported run is reproducible from a commit, data version, config and seed.
- Error analysis by slice is done, a model card exists, and serving uses the same features as training with drift monitoring in place.

## References

- [references/leakage-checklist.md](references/leakage-checklist.md) - read before trusting any result, and whenever validation scores look too good.
