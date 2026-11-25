---
name: ent-unit-economics-cac-ltv
description: "Compute and stress-test customer acquisition cost (CAC), customer lifetime value (LTV), payback period, and net retention economics for technology ventures."
category: entrepreneurship
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - entrepreneurship
  - finance
  - unit-economics
  - saas
  - financial-modeling
---

# Unit Economics & CAC/LTV Financial Modeling

## Overview & Core Principles
Compute and stress-test customer acquisition cost (CAC), customer lifetime value (LTV), payback period, and net retention economics for technology ventures.

### Formulaic Specifications & Cohort Analysis
1. **True Fully-Burloaded CAC**:
   - $\text{CAC} = \frac{\text{Total Sales & Marketing Expenses (Salaries, Commissions, Ad Spend, Tools)}}{\text{New Customers Acquired in Cohort Period}}$
2. **Customer Lifetime Value (LTV)**:
   - $\text{LTV} = \frac{\text{ARPU} \times \text{Gross Margin (\%)}}{\text{Customer Churn Rate}}$
3. **CAC Payback Period**:
   - $\text{Payback Months} = \frac{\text{Blended CAC}}{\text{ARPU} \times \text{Gross Margin (\%)}}$
4. **Healthy SaaS Thresholds**:
   - LTV / CAC Ratio $\ge 3.0$ (ratio $> 5.0$ indicates under-investment in growth).
   - CAC Payback Period $\le 12$ months for SMB; $\le 18$ months for Enterprise.
   - Magic Number = $\frac{(\text{Q}_t \text{ ARR} - \text{Q}_{t-1} \text{ ARR}) \times 4}{\text{Q}_{t-1} \text{ S&M Spend}} \ge 0.75$.
