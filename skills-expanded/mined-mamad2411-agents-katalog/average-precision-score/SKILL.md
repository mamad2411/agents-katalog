---
name: average-precision-score
description: Compute the average_precision_score metric — provided by scikit-learn. Use when the user has predictions and ground-truth and needs to compute average_precision_score, or asks how to score with average_precision_score.
metadata:
  skill_kind: metric
  source_lib: scikit-learn
  import_path: sklearn.metrics.average_precision_score
  source: library_introspection
---

# average-precision-score

> Metric `average_precision_score` from `scikit-learn` (sklearn.metrics.average_precision_score)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with average_precision_score, or
mentions `sklearn.metrics.average_precision_score` directly, or wants the standard scikit-learn implementation.

## Reference signature

```python
from sklearn.metrics import average_precision_score

# average_precision_score(y_true, y_score, *, average='macro', pos_label=1, sample_weight=None)
```

## Library docstring

```
Compute average precision (AP) from prediction scores.

AP summarizes a precision-recall curve as the weighted mean of precisions
achieved at each threshold, with the increase in recall from the previous
threshold used as the weight:

.. math::
    \text{AP} = \sum_n (R_n - R_{n-1}) P_n

where :math:`P_n` and :math:`R_n` are the precision and recall at the nth
threshold [1]_. This implementation is not interpolated and is different
from computing the area under the precision-recall curve with the
trapezoidal rule, which uses linear interpolation and can be too
optimistic.

Read more in the :ref:`User Guide <precision_recall_f_measure_metrics>`.

Parameters
----------
y_true : array-like of shape (n_samples,) or (n_samples, n_classes)
    True binary labels or binary label indicators.

y_score : array-like of shape (n_samples,) or (n_samples, n_classes)
    Target scores, can either be probability estimates of the positive
    class, confidence values, or non-thresholded measure of decisions
    (as returned by :term:`decision_function` on some classifiers).
    For :term:`decision_function` scores, values greater than or equal to
    zero should indicate the positive class.

average : {'micro', 'samples', 'weighted', 'macro'} or None,             default='macro'
    If ``None``, the scores for each class are returned. Otherwise,
    this determines the type of averaging performed on the data:

    ``'micro'``:
        Calculate metrics globally by considering each element of the label
        indicator matrix as a label.
    ``'macro'``:
        Calculate metrics for each label, and find their unweighted
        mean.  This does not take label imbalance into account.
    ``'weighted'``:
        Calculate metrics for each label, and find their average, weighted
        by support (the number of true instances for each label).
    ``'samples'``:
        Calculate metrics for each instance, and find their average.

    Will be ignored when ``y_true`` is binary.

pos_label : int, float, bool or str, default=1
    The label of the positive class. Only applied to binary ``y_true``.
    For multilabel-indicator ``y_true``, ``pos_label`` is fixed to 1.

sample_weight : 
```

## Quick recipe

```python
import sklearn.metrics as _m
score = _m.average_precision_score(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
