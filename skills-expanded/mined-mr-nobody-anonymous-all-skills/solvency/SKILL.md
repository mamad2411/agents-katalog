---
name: solvency
description: "Compute Solvency Capital Requirement (SCR) across Life, Non-Life, Health, and Market underwriting modules conforming to EIOPA regulations."
category: actuarial
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - actuarial
  - solvency-ii
  - scr
  - eiopa
  - capital-adequacy
---

# Solvency II Standard Formula & SCR Valuation

## Overview & Core Principles
Compute Solvency Capital Requirement (SCR) across Life, Non-Life, Health, and Market underwriting modules conforming to EIOPA regulations.

### SCR Aggregation Matrix
$$SCR_{\text{overall}} = \sqrt{\sum_{i,j} \text{Corr}_{i,j} \cdot SCR_i \cdot SCR_j} + SCR_{\text{op}}$$
- Technical Provisions = Best Estimate Liabilities (BEL) + Risk Margin (CoC at 6%).
