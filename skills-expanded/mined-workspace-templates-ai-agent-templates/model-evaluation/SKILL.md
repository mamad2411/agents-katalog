---
name: model-evaluation
description: Chooses metrics, splits and baselines for a model, then reports results with uncertainty. Use it before claiming a model is good or better than another.
---

# Model evaluation

Report what a skeptical reviewer would accept, not the best-looking number.

## Steps

1. State the decision the model supports and the cost of each error type. Choose the metric from that: precision and recall or PR AUC for rare positives, MAE or RMSE for regression (pick by outlier cost), calibration for probabilities used as such. Accuracy alone is wrong for imbalanced classes.
2. Split to match deployment. Use time-based splits for anything that predicts the future, group splits when rows share an entity (user, patient), and stratified splits otherwise. Fit all preprocessing on the training part only.
3. Keep three sets: train, validation for tuning, and a test set touched once at the end.
4. Build baselines first: majority class or mean, then a simple model such as logistic regression or last value. A complex model must beat these.
5. Run cross validation or several seeds. Report the mean and the spread, and a bootstrap confidence interval for the headline metric.
6. Slice results: by segment, by time period and by input difficulty. Look at the worst slice and at a sample of the worst errors.
7. For classifiers, check the threshold choice and a calibration curve.
8. Check leakage: features derived from the target, duplicates across splits, and suspiciously perfect scores.

## Rules

- Never tune against the test set.
- Never report a gain smaller than the run to run noise as an improvement.

## Report

A table of model against baseline with intervals, the slice results, the three most telling error examples, and a plain statement of what the numbers do not show.
