---
name: biostatistics
description: "Medical biostatistics hypothesis testing toolkit: t-tests, ANOVA, chi-square, Fisher exact, Mann-Whitney, Kruskal-Wallis, sample size calculation, power analysis, multiple testing correction, survival analysis, and clinical trial biostatistics."
tags: [biostatistics, hypothesis-testing, clinical-trials, statistics, sample-size, power-analysis, zorai]
---
## Overview

Medical biostatistics for hypothesis testing, clinical trial design, and survival analysis. Covers t-tests, ANOVA, chi-square, Fisher exact, Mann-Whitney, Kruskal-Wallis, sample size calculation, power analysis, and multiple testing correction.

## Installation

```bash
uv pip install scipy statsmodels
```

## Common Tests

```python
import numpy as np
from scipy import stats

# Two-sample t-test
t_stat, p = stats.ttest_ind(np.random.normal(100, 15, 30), np.random.normal(110, 15, 30))

# Mann-Whitney
u_stat, p = stats.mannwhitneyu(np.random.normal(100, 15, 30), np.random.normal(110, 15, 30))

# Chi-square
chi2, p, dof, _ = stats.chi2_contingency(np.array([[30, 10], [20, 40]]))
```

## Sample Size

```python
from statsmodels.stats.power import TTestIndPower
n = TTestIndPower().solve_power(effect_size=0.5, power=0.80, alpha=0.05)
print(f"N per group: {np.ceil(n):.0f}")
```

## References
- [SciPy stats](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels](https://www.statsmodels.org/)