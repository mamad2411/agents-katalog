---
name: soc-causal-inference-econometrics
description: "Formulate and estimate causal effects using Difference-in-Differences (DiD), Instrumental Variables (2SLS), and Regression Discontinuity Designs (RDD)."
category: social-science
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - social-science
  - causal-inference
  - econometrics
  - did
  - instrumental-variables
  - rdd
---

# Econometric Causal Inference & Quasi-Experimental Design

## Overview & Core Principles
Formulate and estimate causal effects using Difference-in-Differences (DiD), Instrumental Variables (2SLS), and Regression Discontinuity Designs (RDD).

### Quasi-Experimental Identification Strategies
1. **Difference-in-Differences (DiD) Identification**:
   - Model: $Y_{it} = \beta_0 + \gamma \text{Treated}_i + \lambda \text{Post}_t + \delta (\text{Treated}_i \times \text{Post}_t) + \varepsilon_{it}$.
   - Core Invariant: **Parallel Trends Assumption** — in the absence of treatment, average outcomes for treated and control groups would have evolved in parallel.
   - Pre-trend test: Estimate dynamic event-study leads and lags; verify pre-treatment coefficients are statistically indistinguishable from zero.
2. **Instrumental Variables (IV / 2SLS)**:
   - Relevance condition: $\text{Cov}(Z, X) \ne 0$ (first-stage $F$-statistic $> 10$).
   - Exclusion restriction: $\text{Cov}(Z, \varepsilon) = 0$ (instrument affects outcome $Y$ *only* through treatment $X$).
