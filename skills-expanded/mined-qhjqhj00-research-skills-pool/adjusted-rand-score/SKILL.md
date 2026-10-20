---
name: adjusted-rand-score
description: Compute the adjusted_rand_score metric — provided by scikit-learn. Use when the user has predictions and ground-truth and needs to compute adjusted_rand_score, or asks how to score with adjusted_rand_score.
metadata:
  skill_kind: metric
  source_lib: scikit-learn
  import_path: sklearn.metrics.adjusted_rand_score
  source: library_introspection
---

# adjusted-rand-score

> Metric `adjusted_rand_score` from `scikit-learn` (sklearn.metrics.adjusted_rand_score)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with adjusted_rand_score, or
mentions `sklearn.metrics.adjusted_rand_score` directly, or wants the standard scikit-learn implementation.

## Reference signature

```python
from sklearn.metrics import adjusted_rand_score

# adjusted_rand_score(labels_true, labels_pred)
```

## Library docstring

```
Rand index adjusted for chance.

The Rand Index computes a similarity measure between two clusterings
by considering all pairs of samples and counting pairs that are
assigned in the same or different clusters in the predicted and
true clusterings.

The raw RI score is then "adjusted for chance" into the ARI score
using the following scheme::

    ARI = (RI - Expected_RI) / (max(RI) - Expected_RI)

The adjusted Rand index is thus ensured to have a value close to
0.0 for random labeling independently of the number of clusters and
samples and exactly 1.0 when the clusterings are identical (up to
a permutation). The adjusted Rand index is bounded below by -0.5 for
especially discordant clusterings.

ARI is a symmetric measure::

    adjusted_rand_score(a, b) == adjusted_rand_score(b, a)

Read more in the :ref:`User Guide <adjusted_rand_score>`.

Parameters
----------
labels_true : array-like of shape (n_samples,), dtype=int
    Ground truth class labels to be used as a reference.

labels_pred : array-like of shape (n_samples,), dtype=int
    Cluster labels to evaluate.

Returns
-------
ARI : float
   Similarity score between -0.5 and 1.0. Random labelings have an ARI
   close to 0.0. 1.0 stands for perfect match.

See Also
--------
adjusted_mutual_info_score : Adjusted Mutual Information.

References
----------
.. [Hubert1985] L. Hubert and P. Arabie, Comparing Partitions,
  Journal of Classification 1985
  https://link.springer.com/article/10.1007%2FBF01908075

.. [Steinley2004] D. Steinley, Properties of the Hubert-Arabie
  adjusted Rand index, Psychological Methods 2004

.. [wk] https://en.wikipedia.org/wiki/Rand_index#Adjusted_Rand_index

.. [Chacon] :doi:`Minimum adjusted Rand index for two clusterings of a given size,
  2022, J. E. Chacón and A. I. Rastrojo <10.1007/s11634-022-00491-w>`

Examples
--------
Perfectly matching labelings have a score of 1 even

  >>> from sklearn.metrics.cluster import adjusted_rand_score
  >>> adjusted_rand_score([0, 0, 1, 1], [0, 0, 1, 1])
  1.0
  >>> adjusted_rand_score([0, 0, 1, 1], [1, 1, 0, 0])
  1.0

Labelings that assign all classes members to the same clusters
are complete but may not always be pure, hence penalized::

  
```

## Quick recipe

```python
import sklearn.metrics as _m
score = _m.adjusted_rand_score(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
