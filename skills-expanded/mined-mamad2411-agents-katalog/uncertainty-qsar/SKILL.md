---
name: uncertainty-qsar
description: Use when building QSAR/ML models that need calibrated uncertainty estimates. Covers epistemic vs aleatoric uncertainty theory, conformal prediction with MAPIE (guaranteed coverage), Gaussian processes with Tanimoto kernel, deep uncertainty (MC dropout, deep ensembles, Laplace), and applicability domain (AD) assessment. Critical for active learning and reliable property prediction.
---

# Uncertainty-Aware QSAR

QSAR models that output only point predictions are insufficient for drug discovery decisions. Uncertainty quantification (UQ) transforms predictions into actionable confidence intervals: "LogD = 2.3 ± 0.4 (90% CI)" is far more useful than "LogD = 2.3".

## When to Use This Skill

- Build QSAR models with calibrated prediction intervals (not just point predictions)
- Assess whether a query molecule is within the applicability domain (AD) of the model
- Design active learning loops: prioritize compounds with high epistemic uncertainty
- Rank compounds when model uncertainty is high (don't trust raw predictions alone)
- Regulatory/submission context requiring prediction confidence bounds
- Compare model calibration (is the stated 90% CI actually 90% coverage?)

## Uncertainty Types

| Type | What it means | How to reduce | Methods |
|------|--------------|--------------|---------|
| **Epistemic** | Model doesn't know (lack of training data) | Add more training data | GP variance, ensemble disagreement, MC dropout std |
| **Aleatoric** | Intrinsic noise (measurement error) | Can't be reduced | Heteroscedastic models, learned noise σ |
| **Total** | Combined uncertainty | — | Epistemic + Aleatoric in prediction |

## Quick Start — Conformal Prediction (MAPIE)

```python
from mapie.regression import MapieRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Fit + calibrate
base_model = RandomForestRegressor(n_estimators=100, random_state=42)
mapie = MapieRegressor(base_model, method="plus", cv=5)
mapie.fit(X_train, y_train)

# Predict with intervals (alpha = desired error rate)
y_pred, y_pi = mapie.predict(X_test, alpha=0.10)  # 90% CI
# y_pi shape: (n_samples, 2, n_alpha)
lower = y_pi[:, 0, 0]
upper = y_pi[:, 1, 0]

# Coverage check
coverage = np.mean((y_test >= lower) & (y_test <= upper))
print(f"Empirical coverage: {coverage:.2%}")  # should be ~90%
```

## Quick Start — Tanimoto GP

```python
import gpytorch
import torch
from rdkit.Chem import rdMolDescriptors

class TanimotoKernel(gpytorch.kernels.Kernel):
    """Tanimoto similarity kernel for binary fingerprints."""
    has_lengthscale = False

    def forward(self, x1, x2, **params):
        x1_sum = x1.sum(-1, keepdim=True)
        x2_sum = x2.sum(-1, keepdim=True)
        dot = torch.matmul(x1, x2.transpose(-1, -2))
        intersection = dot
        union = x1_sum + x2_sum.transpose(-1, -2) - dot
        return intersection / union.clamp(min=1e-8)

# Usage:
# fps = np.array([get_morgan_fp(smi) for smi in smiles_list])
# X = torch.tensor(fps, dtype=torch.float32)
# y = torch.tensor(activities, dtype=torch.float32)
# → see references/gaussian-processes.md for full GP model
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Theory: epistemic vs aleatoric, GP kernel validity, conformal coverage proof, AD concepts | `references/uncertainty-theory.md` |
| Conformal prediction with MAPIE: split/cross conformal, regression/classification, calibration | `references/conformal-prediction.md` |
| GP regression with Tanimoto kernel: GPyTorch, hyperopt, posterior sampling, active learning | `references/gaussian-processes.md` |
| Deep uncertainty: MC dropout, deep ensembles, evidential regression, Laplace approximation | `references/deep-uncertainty.md` |
| Applicability domain: distance-based AD, Williams plot (leverage), visualization, thresholds | `references/applicability-domain.md` |

## Software Stack

| Package | Install | Role |
|---------|---------|------|
| `MAPIE` | `pip install mapie` | Conformal prediction (classification + regression) |
| `gpytorch` | `pip install gpytorch` | GP models on PyTorch (GPU-ready) |
| `botorch` | `pip install botorch` | Bayesian optimization (uses GPyTorch) |
| `laplace-torch` | `pip install laplace-torch` | Laplace approx for any PyTorch model |
| `torch` | `pip install torch` | Deep ensembles, MC dropout |
| `sklearn` | `pip install scikit-learn` | RF/SVM baselines, calibration |
| `rdkit` | conda/pip | Fingerprints (Morgan, MACCS) for features |
| `uncertainty-toolbox` | `pip install uncertainty-toolbox` | Calibration plots, ECE, sharpness |

## Key Concepts Summary

| Concept | Formula / Key Point |
|---------|-------------------|
| Coverage guarantee | P(y ∈ Ĉ(x)) ≥ 1−α for conformal (finite-sample) |
| Prediction interval | [ŷ − q̂, ŷ + q̂] where q̂ = (1−α) quantile of calibration residuals |
| GP posterior variance | σ²(x*) = k(x*,x*) − k(x*,X)[K+σ²I]⁻¹k(X,x*) |
| Ensemble uncertainty | σ²_epistemic = Var{f̂_m(x)} across M models |
| MC dropout σ | std of T forward passes with dropout active |
| Leverage h_ii | h = x(XᵀX)⁻¹xᵀ; Williams plot flags h > 3p/n |
| AD distance | D = min_train Tanimoto; D < threshold → inside AD |

## Key Pitfalls

- **Overconfident RF**: RF standard deviation of tree predictions is NOT a calibrated CI — always use conformal on top
- **GP scaling**: naive GP is O(n³) — for >5000 training points use sparse GP (inducing points) or `ExactGP` + KeOps
- **Conformal requires i.i.d. calibration**: if training/calibration sets have distribution shift, coverage guarantee breaks
- **MC dropout depth**: dropout only captures epistemic if placed at multiple layers; single output layer dropout ≈ ensemble of linear heads only
- **AD threshold is task-specific**: there is no universal threshold for "inside AD" — always validate on held-out temporal/spatial split

## Related Skills

- `scientific-skills:scikit-learn` — RF/SVM/GBM base models, cross-validation
- `scientific-skills:pymc` — full Bayesian QSAR (MCMC-based posterior)
- `active-learning` (upcoming) — using uncertainty for experimental design
- `mmpa` — MMPA + uncertainty: only apply transforms where model is confident
- `generative-design` — uncertainty filter on generated molecules (discard low-confidence predictions)
