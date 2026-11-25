---
name: pymc-markets
description: "Bayesian inference for financial markets using PyMC. Stochastic volatility models, regime-switching, Bayesian portfolio optimization, factor models, and Markov chain Monte Carlo for risk estimation."
tags: [bayesian, pymc, stochastic-volatility, portfolio-optimization, risk, markets, zorai]
---
## Overview

PyMC provides Bayesian inference for financial modeling: stochastic volatility, regime-switching, Bayesian portfolio optimization, factor models, and MCMC risk estimation using the NUTS sampler. ArviZ provides diagnostics and visualization.

## Installation

```bash
uv pip install pymc arviz
```

## Stochastic Volatility Model

```python
import pymc as pm
import numpy as np
import arviz as az

# Simulated daily returns
returns = np.random.randn(500) * 0.02

with pm.Model() as sv_model:
    sigma = pm.InverseGamma("sigma", alpha=2, beta=1)
    log_vol = pm.GaussianRandomWalk("log_vol", sigma=sigma, shape=len(returns))
    obs = pm.Normal("returns", mu=0, sigma=pm.math.exp(log_vol / 2), observed=returns)
    trace = pm.sample(1000, tune=1000, chains=4)

print(az.summary(trace, var_names=["sigma"]))
az.plot_trace(trace)
```

## References
- [PyMC docs](https://www.pymc.io/)
- [Bayesian Methods for Hackers](https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers)