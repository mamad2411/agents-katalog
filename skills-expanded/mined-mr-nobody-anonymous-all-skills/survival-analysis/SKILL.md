---
name: survival-analysis
description: "Estimate survival curves, hazard rates, and right-censored policy duration data using Kaplan-Meier product-limit and Cox proportional hazards."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - survival-analysis
  - kaplan-meier
  - hazard-rate
---

# Actuarial Survival Analysis & Kaplan-Meier Estimation

## Overview & Core Principles
Estimate survival curves, hazard rates, and right-censored policy duration data using Kaplan-Meier product-limit and Cox proportional hazards.

### Product-Limit Estimator
$$\hat{S}(t) = \prod_{t_i \le t} \left(1 - \frac{d_i}{n_i}\right)$$
- $d_i$: Number of policy lapses/deaths at time $t_i$.
- $n_i$: Total individuals at risk just prior to $t_i$.
- Greenwood's formula computes variance of $\hat{S}(t)$.
