---
name: property-casualty
description: "Structure property and casualty premium indications using Pure Premium and Loss Ratio approaches with credibility weighting."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - property-casualty
  - rate-making
  - credibility
---

# P&C Actuarial Rate-Making & Exposure Base Modeling

## Overview & Core Principles
Structure property and casualty premium indications using Pure Premium and Loss Ratio approaches with credibility weighting.

### Indicated Rate Change
$$\Delta R = \frac{\text{Experience Loss Ratio} + \text{Fixed Expense Ratio}}{1 - \text{Variable Expense Ratio} - \text{Profit Margin}} - 1$$
- Credibility blending: $Z = \sqrt{N / 1082}$ for full credibility at 95% confidence within 5% error.
