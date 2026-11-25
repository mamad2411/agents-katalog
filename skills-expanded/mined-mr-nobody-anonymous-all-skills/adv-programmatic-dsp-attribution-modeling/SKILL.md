---
name: adv-programmatic-dsp-attribution-modeling
description: "Engineer digital advertising campaigns, optimize programmatic Real-Time Bidding (RTB) algorithms, and construct statistical Marketing Mix Models."
category: advertising
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - advertising
  - programmatic
  - rtb
  - marketing-mix-modeling
  - dsp
  - analytics
---

# Programmatic Media Buying & Marketing Mix Modeling (MMM)

## Overview & Core Principles
Engineer digital advertising campaigns, optimize programmatic Real-Time Bidding (RTB) algorithms, and construct statistical Marketing Mix Models.

### Programmatic RTB & Attribution Framework
1. **Real-Time Bidding (RTB) OpenRTB Protocol**:
   - Process bid requests under 100ms SLA.
   - Dynamic CPM bid calculation: $\text{eCPM} = \text{pCTR} \times \text{pCVR} \times \text{Target CPA} \times 1000$.
2. **Marketing Mix Modeling (MMM) Specification**:
   - Adstock transformation: Carryover effect modeled via geometric decay or Weibull distribution:
     $$A_t = X_t + \lambda A_{t-1}$$
   - Diminishing returns modeled via Hill function:
     $$\text{Response}(A_t) = \frac{A_t^S}{K^S + A_t^S}$$
3. **Campaign Structure Best Practices**:
   - Negative keyword pruning lists refreshed weekly.
   - High-intent search campaigns separated from broad-match discovery campaigns.
