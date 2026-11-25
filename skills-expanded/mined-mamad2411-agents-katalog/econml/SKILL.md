---
name: econml
description: "EconML (Microsoft) — heterogeneous treatment effect estimation. Double ML, Causal Forest, Deep IV, and metalearners (S-Learner, T-Learner, X-Learner). Orthogonal learning for causal effects from observational data."
tags: [econml, causal-inference, heterogeneous-treatment-effects, causal-forest, microsoft, econometrics, zorai]
---
## Overview

EconML is a Microsoft library for causal inference and heterogeneous treatment effect estimation using machine learning. Implements Double ML, Causal Forest, DML, IV methods, and orthogonal statistical learning. Designed for observational data where treatment effects vary across individuals.

## Installation

```bash
uv pip install econml
```

## Double ML (Linear)

```python
from econml.dml import LinearDML
import numpy as np

X = np.random.randn(500, 5)  # features
T = np.random.randn(500)     # treatment
Y = T * (0.5 + X[:, 0]) + np.random.randn(500)  # outcome

est = LinearDML(model_y="auto", model_t="auto", discrete_treatment=False)
est.fit(Y, T, X=X)
print(f"ATE: {est.ate():.3f} ± {est.ate_inference().stderr:.3f}")
```

## Causal Forest

```python
from econml.grf import CausalForest

cf = CausalForest(n_estimators=100, min_samples_leaf=10)
cf.fit(X, T, Y)
treatment_effects = cf.effect(X)
print(f"Heterogeneous effects range: {treatment_effects.min():.3f} to {treatment_effects.max():.3f}")
```

## References
- [EconML docs](https://econml.azurewebsites.net/)
- [EconML GitHub](https://github.com/py-why/EconML)