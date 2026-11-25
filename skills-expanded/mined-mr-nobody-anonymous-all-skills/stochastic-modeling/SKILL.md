---
name: stochastic-modeling
description: "Generate risk-neutral and real-world interest rate paths (Hull-White, Cox-Ingersoll-Ross) for asset-liability management (ALM)."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - esg
  - stochastic-modeling
  - monte-carlo
  - hull-white
---

# Economic Scenario Generators (ESG) & Monte Carlo Asset-Liability

## Overview & Core Principles
Generate risk-neutral and real-world interest rate paths (Hull-White, Cox-Ingersoll-Ross) for asset-liability management (ALM).

### 1-Factor Hull-White Dynamics
$$dr(t) = [\theta(t) - a r(t)] dt + \sigma dW(t)$$
- Calibrate mean reversion speed $a$ and volatility $\sigma$ against swaption implied volatility surfaces.
