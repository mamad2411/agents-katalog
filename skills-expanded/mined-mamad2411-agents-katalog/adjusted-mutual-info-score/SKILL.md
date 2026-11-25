---
name: adjusted-mutual-info-score
description: Compute the adjusted_mutual_info_score metric — provided by scikit-learn. Use when the user has predictions and ground-truth and needs to compute adjusted_mutual_info_score, or asks how to score with adjusted_mutual_info_score.
metadata:
  skill_kind: metric
  source_lib: scikit-learn
  import_path: sklearn.metrics.adjusted_mutual_info_score
  source: library_introspection
---

# adjusted-mutual-info-score

> Metric `adjusted_mutual_info_score` from `scikit-learn` (sklearn.metrics.adjusted_mutual_info_score)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with adjusted_mutual_info_score, or
mentions `sklearn.metrics.adjusted_mutual_info_score` directly, or wants the standard scikit-learn implementation.

## Reference signature

```python
from sklearn.metrics import adjusted_mutual_info_score

# adjusted_mutual_info_score(labels_true, labels_pred, *, average_method='arithmetic')
```

## Library docstring

```
Adjusted Mutual Information between two clusterings.

Adjusted Mutual Information (AMI) is an adjustment of the Mutual
Information (MI) score to account for chance. It accounts for the fact that
the MI is generally higher for two clusterings with a larger number of
clusters, regardless of whether there is actually more information shared.
For two clusterings :math:`U` and :math:`V`, the AMI is given as::

    AMI(U, V) = [MI(U, V) - E(MI(U, V))] / [avg(H(U), H(V)) - E(MI(U, V))]

This metric is independent of the absolute values of the labels:
a permutation of the class or cluster label values won't change the
score value in any way.

This metric is furthermore symmetric: switching :math:`U` (``label_true``)
with :math:`V` (``labels_pred``) will return the same score value. This can
be useful to measure the agreement of two independent label assignments
strategies on the same dataset when the real ground truth is not known.

Be mindful that this function is an order of magnitude slower than other
metrics, such as the Adjusted Rand Index.

Read more in the :ref:`User Guide <mutual_info_score>`.

Parameters
----------
labels_true : int array-like of shape (n_samples,)
    A clustering of the data into disjoint subsets, called :math:`U` in
    the above formula.

labels_pred : int array-like of shape (n_samples,)
    A clustering of the data into disjoint subsets, called :math:`V` in
    the above formula.

average_method : {'min', 'geometric', 'arithmetic', 'max'}, default='arithmetic'
    How to compute the normalizer in the denominator.

    .. versionadded:: 0.20

    .. versionchanged:: 0.22
       The default value of ``average_method`` changed from 'max' to
       'arithmetic'.

Returns
-------
ami: float (upperlimited by 1.0)
   The AMI returns a value of 1 when the two partitions are identical
   (ie perfectly matched). Random partitions (independent labellings) have
   an expected AMI around 0 on average hence can be negative. The value is
   in adjusted nats (based on the natural logarithm).

See Also
--------
adjusted_rand_score : Adjusted Rand Index.
mutual_info_score : Mutual Information (not adjusted for chance).

References
----------
.. [1] `Vinh, 
```

## Quick recipe

```python
import sklearn.metrics as _m
score = _m.adjusted_mutual_info_score(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
