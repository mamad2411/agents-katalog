---
name: ent-cap-table-dilution-modeling
description: "Model multi-round venture financing, convertible instruments (SAFEs, convertible notes with valuation caps and discounts), and option pool expansions."
category: entrepreneurship
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - entrepreneurship
  - venture-capital
  - cap-table
  - equity
  - finance
---

# Cap Table Management and Equity Dilution Modeling

## Overview & Core Principles
Model multi-round venture financing, convertible instruments (SAFEs, convertible notes with valuation caps and discounts), and option pool expansions.

### Dilution Mechanics & Mathematical Invariants
1. **Post-Money SAFE Conversion**:
   - Ownership $\% = \frac{\text{Investment Amount}}{\text{Post-Money Valuation Cap}}$.
   - Post-money SAFEs dilute existing common shareholders, NOT subsequent post-money SAFE holders in the same round.
2. **Priced Equity Round Invariants**:
   - Pre-Money Valuation + New Cash Raised = Post-Money Valuation.
   - Pre-Money Share Price = $\frac{\text{Pre-Money Valuation}}{\text{Fully Diluted Shares (including unallocated option pool shuffle)}}$.
3. **Option Pool Shuffle**:
   - Model the employee pool expansion (e.g. to 10% or 15%) pre-money vs post-money to quantify the exact unannounced dilution absorbed by founders.
