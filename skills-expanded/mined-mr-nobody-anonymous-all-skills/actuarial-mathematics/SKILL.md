---
name: actuarial-mathematics
description: "Calculate present values of contingent life annuities, assurances, and net premium reserves using actuarial commutation functions and force of interest."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - actuarial-mathematics
  - annuities
  - reserves
---

# Actuarial Mathematics & Compound Contingencies

## Overview & Core Principles
Calculate present values of contingent life annuities, assurances, and net premium reserves using actuarial commutation functions and force of interest.

### Commutation Mechanics & Force of Interest
- Present value of an n-year term assurance: $A_{x:\overline{n}|}^1 = \sum_{k=0}^{n-1} v^{k+1} \cdot {}_k p_x \cdot q_{x+k}$.
- Force of interest $\delta = \ln(1 + i)$.
- Equivalence Principle: Set expected present value of benefits equal to expected present value of net premiums at policy inception.
