---
name: mortality-modeling
description: "Model age-specific mortality rates and project future longevity improvements using the Lee-Carter bilinear log-mortality decomposition."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - mortality
  - lee-carter
  - demography
---

# Mortality Modeling & Lee-Carter Forecasting

## Overview & Core Principles
Model age-specific mortality rates and project future longevity improvements using the Lee-Carter bilinear log-mortality decomposition.

### Lee-Carter Specification
$$\ln(m_{x,t}) = \alpha_x + \beta_x \kappa_t + \varepsilon_{x,t}$$
- $\alpha_x$: Baseline age pattern of mortality.
- $\kappa_t$: Time index capturing global mortality improvements over time.
- $\beta_x$: Sensitivity of mortality at age $x$ to changes in the time index $\kappa_t$.
- Fit via Singular Value Decomposition (SVD) subject to $\sum_t \kappa_t = 0$ and $\sum_x \beta_x = 1$.
