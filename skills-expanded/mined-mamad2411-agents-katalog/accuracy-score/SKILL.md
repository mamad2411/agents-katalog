---
name: accuracy-score
description: Compute the accuracy_score metric — provided by scikit-learn. Use when the user has predictions and ground-truth and needs to compute accuracy_score, or asks how to score with accuracy_score.
metadata:
  skill_kind: metric
  source_lib: scikit-learn
  import_path: sklearn.metrics.accuracy_score
  source: library_introspection
---

# accuracy-score

> Metric `accuracy_score` from `scikit-learn` (sklearn.metrics.accuracy_score)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with accuracy_score, or
mentions `sklearn.metrics.accuracy_score` directly, or wants the standard scikit-learn implementation.

## Reference signature

```python
from sklearn.metrics import accuracy_score

# accuracy_score(y_true, y_pred, *, normalize=True, sample_weight=None)
```

## Library docstring

```
Accuracy classification score.

In multilabel classification, this function computes subset accuracy:
the set of labels predicted for a sample must *exactly* match the
corresponding set of labels in y_true.

Read more in the :ref:`User Guide <accuracy_score>`.

Parameters
----------
y_true : 1d array-like, or label indicator array / sparse matrix
    Ground truth (correct) labels. Sparse matrix is only supported when
    labels are of :term:`multilabel` type.

y_pred : 1d array-like, or label indicator array / sparse matrix
    Predicted labels, as returned by a classifier. Sparse matrix is only
    supported when labels are of :term:`multilabel` type.

normalize : bool, default=True
    If ``False``, return the number of correctly classified samples.
    Otherwise, return the fraction of correctly classified samples.

sample_weight : array-like of shape (n_samples,), default=None
    Sample weights.

Returns
-------
score : float
    If ``normalize == True``, returns the fraction of correctly classified samples,
    else returns the number of correctly classified samples.

    The best performance is 1.0 with ``normalize == True`` and the number
    of samples with ``normalize == False``.

See Also
--------
balanced_accuracy_score : Compute the balanced accuracy to deal with
    imbalanced datasets.
jaccard_score : Compute the Jaccard similarity coefficient score.
hamming_loss : Compute the average Hamming loss or Hamming distance between
    two sets of samples.
zero_one_loss : Compute the Zero-one classification loss. By default, the
    function will return the percentage of imperfectly predicted subsets.

Examples
--------
>>> from sklearn.metrics import accuracy_score
>>> y_pred = [0, 2, 1, 3]
>>> y_true = [0, 1, 2, 3]
>>> accuracy_score(y_true, y_pred)
0.5
>>> accuracy_score(y_true, y_pred, normalize=False)
2.0

In the multilabel case with binary label indicators:

>>> import numpy as np
>>> accuracy_score(np.array([[0, 1], [1, 1]]), np.ones((2, 2)))
0.5
```

## Quick recipe

```python
import sklearn.metrics as _m
score = _m.accuracy_score(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
