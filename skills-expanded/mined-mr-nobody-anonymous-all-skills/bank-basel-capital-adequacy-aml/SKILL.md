---
name: bank-basel-capital-adequacy-aml
description: "Calculate Risk-Weighted Assets (RWA), Common Equity Tier 1 (CET1) ratios, and engineer anti-money laundering (AML) graph detection rules."
category: banking
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - banking
  - basel-iii
  - regulatory-compliance
  - aml
  - capital-adequacy
  - risk
---

# Basel III/IV Capital Adequacy & AML/KYC Transaction Monitoring

## Overview & Core Principles
Calculate Risk-Weighted Assets (RWA), Common Equity Tier 1 (CET1) ratios, and engineer anti-money laundering (AML) graph detection rules.

### Basel Regulatory Ratios & Calculation Standards
1. **Capital Adequacy Ratios**:
   - $\text{CET1 Ratio} = \frac{\text{Common Equity Tier 1 Capital}}{\text{Total Risk-Weighted Assets (RWA)}} \ge 4.5\% + 2.5\% \text{ (Capital Conservation Buffer)} = 7.0\%$.
   - $\text{Tier 1 Ratio} \ge 8.5\%$; $\text{Total Capital Ratio} \ge 10.5\%$.
   - Liquidity Coverage Ratio (LCR): $\frac{\text{High Quality Liquid Assets (HQLA)}}{\text{Total Net Cash Outflows over 30 days}} \ge 100\%$.
2. **AML Detection Topology**:
   - Structuring (Smurfing): Identify clustered cash deposits strictly below $10,000 threshold within a 72-hour rolling window across distributed branch networks.
   - Rapid Movement of Funds: Graph traversal identifying incoming wire transfers followed by immediate outgoing international wires exceeding 90% of principal within 24 hours.
