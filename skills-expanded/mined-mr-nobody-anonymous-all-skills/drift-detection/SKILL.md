---
name: drift-detection
description: "Compute Kolmogorov-Smirnov (KS) tests, Population Stability Index (PSI), and Wasserstein distance on live traffic."
category: mlops
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - mlops
  - drift-detection
  - ks-test
  - psi
  - concept-drift
---

# Statistical Concept Drift and Covariate Shift Detection

## Overview & Core Principles
Compute Kolmogorov-Smirnov (KS) tests, Population Stability Index (PSI), and Wasserstein distance on live traffic.

Trigger model retraining alerts when feature PSI exceeds 0.2 threshold across a 7-day rolling window.
