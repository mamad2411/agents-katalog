---
name: act-loss-reserving-chain-ladder
description: "Compute Incurred But Not Reported (IBNR) claim reserves using Chain Ladder, Bornhuetter-Ferguson, and Cape Cod actuarial triangle methods."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - loss-reserving
  - ibnr
  - chain-ladder
  - insurance
  - statistics
---

# Actuarial Loss Reserving & Chain Ladder IBNR Estimation

## Overview & Core Principles
Compute Incurred But Not Reported (IBNR) claim reserves using Chain Ladder, Bornhuetter-Ferguson, and Cape Cod actuarial triangle methods.

### Actuarial Triangle & Reserve Calculation
1. **Development Triangle Mechanics**:
   - Let $C_{i,j}$ be cumulative claims for accident year $i$ at development year $j$.
   - Age-to-Age Development Factors (Link Ratios):
     $$f_j = \frac{\sum_{i=1}^{n-j} C_{i, j+1}}{\sum_{i=1}^{n-j} C_{i, j}}$$
2. **Ultimate Claim & IBNR Estimation**:
   - Projected Ultimate Claims: $\hat{U}_i = C_{i, n-i+1} \times \prod_{j=n-i+1}^{m-1} f_j$.
   - $\text{IBNR}_i = \hat{U}_i - C_{i, n-i+1}$.
3. **Bornhuetter-Ferguson Hybrid Method**:
   - When recent accident years have volatile link ratios, blend actual losses with an a priori expected loss ratio (ELR):
     $$\text{Reserve}_{BF} = \text{Premium}_i \times \text{ELR} \times \left(1 - \frac{1}{\prod f_j}\right)$$
