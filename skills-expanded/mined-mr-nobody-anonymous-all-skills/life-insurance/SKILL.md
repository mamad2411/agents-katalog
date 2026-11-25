---
name: life-insurance
description: "Price whole life, term life, and universal life contracts incorporating mortality charges, acquisition expense amortization, and lapse margins."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - life-insurance
  - pricing
  - underwriting
---

# Life Insurance Product Design and Actuarial Pricing

## Overview & Core Principles
Price whole life, term life, and universal life contracts incorporating mortality charges, acquisition expense amortization, and lapse margins.

### Gross Premium Valuation
$$\text{Premium} = \frac{\text{PV(Benefits)} + \text{PV(Expenses)} + \text{Target Profit Margin}}{\ddot{a}_{x:\overline{n}|}}$$
- Incorporate Zillmer expense loading to amortize upfront broker commissions against renewal premiums.
