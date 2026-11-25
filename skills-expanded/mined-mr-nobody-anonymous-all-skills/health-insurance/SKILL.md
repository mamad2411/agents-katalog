---
name: health-insurance
description: "Calculate medical loss ratios (MLR), incurred claims cost per member per month (PMPM), and aging curve morbidity adjustments."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - health-insurance
  - morbidity
  - mlr
  - pmpm
---

# Health Insurance Morbidity Reserving & Pricing

## Overview & Core Principles
Calculate medical loss ratios (MLR), incurred claims cost per member per month (PMPM), and aging curve morbidity adjustments.

### PMPM Claim Projection
$$\text{Expected PMPM} = \sum_{\text{services}} \text{Utilization Rate} \times \text{Unit Cost}$$
- Calculate minimum 80-85% MLR compliance threshold under ACA statutory accounting.
