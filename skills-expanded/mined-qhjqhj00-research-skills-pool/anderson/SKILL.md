---
name: anderson
description: Compute the anderson metric — provided by scipy.stats. Use when the user has predictions and ground-truth and needs to compute anderson, or asks how to score with anderson.
metadata:
  skill_kind: metric
  source_lib: scipy.stats
  import_path: scipy.stats.anderson
  source: library_introspection
---

# anderson

> Metric `anderson` from `scipy.stats` (scipy.stats.anderson)

## When to invoke this skill

The user has predictions + ground truth and asks to evaluate with anderson, or
mentions `scipy.stats.anderson` directly, or wants the standard scipy.stats implementation.

## Reference signature

```python
from scipy.stats import anderson

# anderson(x, dist='norm', *, method=None)
```

## Library docstring

```
Anderson-Darling test for data coming from a particular distribution.

The Anderson-Darling test tests the null hypothesis that a sample is
drawn from a population that follows a particular distribution.
For the Anderson-Darling test, the critical values depend on
which distribution is being tested against.  This function works
for normal, exponential, logistic, weibull_min, or Gumbel (Extreme Value
Type I) distributions.

Parameters
----------
x : array_like
    Array of sample data.
dist : {'norm', 'expon', 'logistic', 'gumbel', 'gumbel_l', 'gumbel_r', 'extreme1', 'weibull_min'}, optional
    The type of distribution to test against.  The default is 'norm'.
    The names 'extreme1', 'gumbel_l' and 'gumbel' are synonyms for the
    same distribution.
method : str or instance of `MonteCarloMethod`
    Defines the method used to compute the p-value.
    If `method` is ``"interpolated"``, the p-value is interpolated from
    pre-calculated tables.
    If `method` is an instance of `MonteCarloMethod`, the p-value is computed using
    `scipy.stats.monte_carlo_test` with the provided configuration options and other
    appropriate settings.

    .. versionadded:: 1.17.0
        If `method` is not specified, `anderson` will emit a ``FutureWarning``
        specifying that the user must opt into a p-value calculation method.
        When `method` is specified, the object returned will include a ``pvalue``
        attribute, but no ``critical_value``, ``significance_level``, or
        ``fit_result`` attributes. Beginning in 1.19.0, these other attributes will
        no longer be available, and a p-value will always be computed according to
        one of the available `method` options.

Returns
-------
result : AndersonResult
    If `method` is provided, this is an object with the following attributes:

    statistic : float
        The Anderson-Darling test statistic.
    pvalue: float
        The p-value corresponding with the test statistic, calculated according to
        the specified `method`.

    If `method` is unspecified, this is an object with the following attributes:

    statistic : float
        The Anderson-Darling test statistic.
    critical_values 
```

## Quick recipe

```python
import scipy.stats as _m
score = _m.anderson(y_true, y_pred)
```

## Don'ts

- Don't reimplement when the library version handles edge cases (NaN, ties, empty inputs) better than a hand-rolled formula.
- Always check the library version's argument order — sklearn is `(y_true, y_pred)` while torchmetrics is `(preds, target)`.
