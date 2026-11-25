---
name: risk-theory
description: "Calculate finite and infinite-horizon ruin probabilities for surplus processes governed by compound Poisson claim arrivals."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - ruin-theory
  - cramer-lundberg
  - surplus
---

# Ruin Theory and Cramér-Lundberg Approximations

## Overview & Core Principles
Calculate finite and infinite-horizon ruin probabilities for surplus processes governed by compound Poisson claim arrivals.

### Cramér-Lundberg Ruin Formula
$$\psi(u) \le e^{-R u}$$
- Surplus $U(t) = u + c t - \sum_{i=1}^{N(t)} X_i$.
- $R$: Lundberg adjustment coefficient satisfying $E[e^{R X}] = 1 + (1 + \theta) E[X] R$.
