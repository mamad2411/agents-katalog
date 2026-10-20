---
name: anderson-ksamp
description: Compute the anderson_ksamp metric — provided by scipy.stats. Use when the user has predictions and ground-truth and needs to compute anderson_ksamp, or asks how to score with anderson_ksamp.
metadata:
  skill_kind: metric
  source_lib: scipy.stats
  import_path: scipy.stats.anderson_ksamp
  source: library_introspection
---

# anderson-ksamp

> Metric `anderson_ksamp` from `scipy.stats` (scipy.stats.anderson_ksamp)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with anderson_ksamp, or
mentions `scipy.stats.anderson_ksamp` directly, or wants the standard scipy.stats implementation.

## Reference signature

```python
from scipy.stats import anderson_ksamp

# anderson_ksamp(samples, midrank=<object object at 0x72cab25435f0>, *, variant=<object object at 0x72cab25435f0>, method=None)
```

## Library docstring

```
The Anderson-Darling test for k-samples.

The k-sample Anderson-Darling test is a modification of the
one-sample Anderson-Darling test. It tests the null hypothesis
that k-samples are drawn from the same population without having
to specify the distribution function of that population. The
critical values depend on the number of samples.

Parameters
----------
samples : sequence of 1-D array_like
    Array of sample data in arrays.
midrank : bool, optional
    Variant of Anderson-Darling test which is computed. Default
    (True) is the midrank test applicable to continuous and
    discrete populations. If False, the right side empirical
    distribution is used.

    .. deprecated::1.17.0
        Use parameter `variant` instead.
variant : {'midrank', 'right', 'continuous'}
    Variant of Anderson-Darling test to be computed. ``'midrank'`` is applicable
    to both continuous and discrete populations. ``'discrete'`` and ``'continuous'``
    perform alternative versions of the test for discrete  and continuous
    populations, respectively.
    When `variant` is specified, the return object will not be unpackable as a
    tuple, and only attributes ``statistic`` and ``pvalue`` will be present.
method : PermutationMethod, optional
    Defines the method used to compute the p-value. If `method` is an
    instance of `PermutationMethod`, the p-value is computed using
    `scipy.stats.permutation_test` with the provided configuration options
    and other appropriate settings. Otherwise, the p-value is interpolated
    from tabulated values.

Returns
-------
res : Anderson_ksampResult
    An object containing attributes:

    statistic : float
        Normalized k-sample Anderson-Darling test statistic.
    critical_values : array
        The critical values for significance levels 25%, 10%, 5%, 2.5%, 1%,
        0.5%, 0.1%.

        .. deprecated::1.17.0
             Present only when `variant` is unspecified.

    pvalue : float
        The approximate p-value of the test. If `method` is not
        provided, the value is floored / capped at 0.1% / 25%.

Raises
------
ValueError
    If fewer than 2 samples are provided, a sample is empty, or no
    distinct observa
```

## Quick recipe

```python
import scipy.stats as _m
score = _m.anderson_ksamp(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
