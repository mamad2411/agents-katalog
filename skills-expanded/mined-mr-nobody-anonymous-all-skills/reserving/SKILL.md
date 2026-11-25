---
name: reserving
description: "Estimate ultimate liabilities using Chain-Ladder, Bornhuetter-Ferguson, and Mack stochastic volatility confidence intervals."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - reserving
  - chain-ladder
  - ibnr
---

# Actuarial Reserving & Loss Development Triangles

## Overview & Core Principles
Estimate ultimate liabilities using Chain-Ladder, Bornhuetter-Ferguson, and Mack stochastic volatility confidence intervals.

### Mack Chain-Ladder Variance
$$V(\hat{C}_{i,I}) = \hat{C}_{i,I}^2 \sum_{k=I+1-i}^{J-1} \frac{\sigma_k^2}{f_k^2} \left( \frac{1}{C_{i,k}} + \frac{1}{\sum_{j=1}^{I-k} C_{j,k}} \right)$$
