---
title: Supplier Evaluation & Qualification
description: Manage supplier qualification using Platinum/Gold/Silver/Bronze tier system with performance monitoring, risk assessment, and continuous improvement
version: 1.0
frequency_percent: 75.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/supplier-evaluation
gigabrain_tags: disciplines, 01900_procurement, supplier-management, supplier-qualification, vendor-evaluation, performance-monitoring, risk-assessment
openstinger_context: supplier-management, vendor-qualification, supply-chain-integration
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_PROCUREMENT_ORDER_PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
related_skills:
  - pre-task-assessment-readiness
  - procurement-order-management
---

# Supplier Evaluation & Qualification

## Overview

Manage supplier qualification using the Platinum/Gold/Silver/Bronze tier classification system with performance monitoring across delivery reliability, quality metrics, and responsiveness. Includes risk assessment for financial stability, compliance history, and production capacity.

**Announce at start:** "I'm using the supplier-evaluation skill to assess or manage a supplier."

## When to Use This Skill

**Trigger Conditions:**
- Evaluating a new supplier for qualification and onboarding
- Assessing an existing supplier for re-qualification or tier reassignment
- Investigating supplier performance issues or delivery failures
- Pre-qualifying suppliers before issuing RFQs
- Annual or periodic supplier performance review

**Prerequisites:**
- Supplier company information available (registration, financials, capabilities)
- Performance data available for existing suppliers (delivery history, quality records)
- Risk assessment information available (credit checks, audit history)

## Step-by-Step Procedure

### Step 1: Pre-Qualification Assessment

Evaluate the supplier against minimum qualification requirements:

| Criteria | Assessment | Pass/Fail |
|----------|-----------|-----------|
| Registration | Valid business registration and licenses | |
| Financial Stability | Acceptable credit rating, no bankruptcy risk | |
| Technical Capability | Can deliver required goods/services per specification | |
| Production Capacity | Can deliver required volumes within timeline | |
| Quality System | Has documented quality management system (ISO 9001 or equivalent) | |
| Safety Record | Acceptable safety history (TRIR < 1.0 preferred) | |
| Compliance History | No major regulatory violations or sanctions | |
| References | Positive references from similar projects or clients | |

If **any** criteria fails, the supplier cannot be qualified until the issue is resolved.

### Step 2: Tier Classification

Assign the supplier to a tier based on the following criteria:

#### Platinum Tier
- **Delivery Reliability:** >98% on-time delivery
- **Quality Performance:** Zero critical defects, <0.5% defect rate
- **Financial Score:** Excellent financial stability (A+ rating)
- **Capacity:** Exceeds demand, with dedicated production lines
- **Compliance:** Zero compliance issues in past 5 years
- **Responsiveness:** <4-hour response time, same-day resolution
- **Preferred Status:** First choice for new orders, strategic partner consideration

#### Gold Tier
- **Delivery Reliability:** >95% on-time delivery
- **Quality Performance:** <1% defect rate, no major defects
- **Financial Score:** Good financial stability (A or A- rating)
- **Capacity:** Meets demand with some buffer
- **Compliance:** No compliance issues in past 3 years
- **Responsiveness:** <8-hour response time, next-day resolution
- **Preferred Status:** Preferred supplier, receives majority of orders

#### Silver Tier
- **Delivery Reliability:** >85% on-time delivery
- **Quality Performance:** <3% defect rate, isolated issues managed
- **Financial Score:** Acceptable financial stability (BBB+ or higher)
- **Capacity:** Adequate for current demand but limited flexibility
- **Compliance:** No major compliance issues in past year
- **Responsiveness:** <24-hour response time, 2-day resolution
- **Preferred Status:** Approved but not preferred, used when Platinum/Gold unavailable

#### Bronze Tier
- **Delivery Reliability:** >70% on-time delivery
- **Quality Performance:** <5% defect rate, improvement plan required
- **Financial Score:** Marginal financial stability (BBB or higher)
- **Capacity:** Limited capacity, may need lead time to scale
- **Compliance:** Minor compliance issues documented and addressed
- **Responsiveness:** <48-hour response time, 5-day resolution
- **Preferred Status:** Provisional approval, requires improvement plan, no new orders until upgraded

### Step 3: Performance Monitoring Setup

Establish monitoring metrics and tracking for the supplier:

| Metric | Measurement | Target | Frequency |
|--------|------------|--------|-----------|
| On-Time Delivery Rate | Delivered by promised date / Total deliveries | >95% | Per order + quarterly aggregate |
| Quality Defect Rate | Defective items / Total items received | <1% | Per shipment + quarterly aggregate |
| Responsiveness | Response time to inquiries or issues | <8 hours | Per interaction |
| Documentation Accuracy | Correct documents (packing list, certificate, invoice) / Total documents | >98% | Per shipment |
| GRN Discrepancy Rate | Shipments with quantity/quality discrepancies | <2% | Per shipment |
| Price Trend | Unit price changes over time | Stable or decreasing | Quarterly review |

### Step 4: Risk Assessment

Evaluate the supplier's risk profile across the following dimensions:

| Risk Category | Assessment Factors | Risk Level |
|---------------|--------------------|------------|
| Financial Risk | Credit rating, cash flow, debt-to-equity ratio, bankruptcy risk | Low / Medium / High |
| Operational Risk | Production capacity, equipment age, maintenance program, backup systems | Low / Medium / High |
| Quality Risk | QMS maturity, audit findings, defect history, corrective actions | Low / Medium / High |
| Supply Chain Risk | Single-source dependency, logistics complexity, import/customs issues | Low / Medium / High |
| Compliance Risk | Environmental violations, labor issues, sanctions screening | Low / Medium / High |
| Geopolitical Risk | Supplier location stability, trade restrictions, currency volatility | Low / Medium / High |

### Step 5: Evaluation Report

Produce a supplier evaluation report with the following structure:
```
SUPPLIER EVALUATION REPORT — [Supplier Name]
═══════════════════════════════════════════
Generated: [Date]
Evaluated By: [Agent Name]
Report Type: [Pre-Qualification / Annual Review / Performance Investigation]

EXECUTIVE SUMMARY:
- Tier: [Platinum/Gold/Silver/Bronze]
- Overall Score: [X/100]
- Recommendation: [Approve / Approve with Conditions / Reject / Upgrade / Downgrade]

PRE-QUALIFICATION RESULT: [PASS / FAIL]
  - [List each criteria result]

TIER CLASSIFICATION:
  - Delivery Reliability: [Score + Tier]
  - Quality Performance: [Score + Tier]
  - Financial Stability: [Score + Tier]
  - Responsiveness: [Score + Tier]
  - Compliance: [Score + Tier]

RISK ASSESSMENT:
  - Financial Risk: [Low/Medium/High]
  - Operational Risk: [Low/Medium/High]
  - Quality Risk: [Low/Medium/High]
  - Supply Chain Risk: [Low/Medium/High]
  - Compliance Risk: [Low/Medium/High]
  - Geopolitical Risk: [Low/Medium/High]

RECOMMENDATIONS:
- [Improvement areas if applicable]
- [Monitoring enhancements if applicable]
- [Order allocation recommendation]

NEXT REVIEW DATE: [Date]
```

### Step 6: Continuous Improvement

For suppliers not meeting their tier targets or with identified improvement areas:
1. Document specific improvement areas with measurable targets
2. Set a timeline for improvement (typically 60-90 days)
3. Schedule follow-up review to verify improvement progress
4. If improvement is achieved, consider tier upgrade
5. If improvement is not achieved, escalate to tier downgrade or removal from approved vendor list

## Success Criteria

- [ ] Pre-qualification criteria assessed for all required criteria
- [ ] Tier classification assigned based on documented criteria (not subjective assessment)
- [ ] Performance monitoring setup complete with targets defined
- [ ] Risk assessment completed for all 6 risk categories
- [ ] Evaluation report produced with clear recommendation
- [ ] Continuous improvement plan created for suppliers below target
- [ ] Next review date scheduled

## Common Pitfalls

1. **Subjective Assessments** — Base tier classification and risk assessment on documented criteria and measurable data, not opinions or relationships.
2. **Incomplete Risk Evaluation** — Evaluate all 6 risk categories. A supplier with excellent delivery but poor financial stability is high-risk.
3. **Missing Baseline Metrics** — Establish performance baselines when onboarding new suppliers. You cannot measure improvement without a baseline.
4. **Ignoring Near-Misses** — Track near-misses (late deliveries caught by expediting, defects caught by inspection) — these are indicators of systemic risk.
5. **No Follow-Up** — Continuous improvement plans without follow-up reviews are worthless. Always schedule the next review when producing the evaluation report.

## Cross-References

### Related Skills
- `procurement-order-management` — Use supplier evaluation when assigning orders to vendors
- `pre-task-assessment-readiness` — Assess readiness before starting supplier evaluation

### Related Agents
- `Supplier Management Specialist` (DomainForge) — Primary agent for supplier evaluation and monitoring
- `Procurement Strategy Specialist` (DomainForge) — Strategic supplier selection and category management
- `Financial Compliance Specialist` (DomainForge) — Financial risk assessment and stability evaluation
- `Procurement Analytics Specialist` (DomainForge) — Performance metrics and analytics

## Example Usage

**Scenario:** Evaluate SteelWorks Ltd for structural steel supply qualification

1. **Pre-Qualification:** Check registration (PASS, valid), Financial stability (PASS, A- rating), Technical capability (PASS, ISO 9001), Production capacity (PASS, 500t/month), Quality system (PASS, ISO 9001 certified), Safety record (PASS, TRIR 0.8), Compliance history (PASS, no violations), References (PASS, 3 positive project references)
2. **Tier Classification:** Based on historical data: 96% on-time delivery, 0.8% defect rate
3. **Risk Assessment:** Financial (Low), Operational (Low), Quality (Low), Supply Chain (Medium - single-source for specialized sections), Compliance (Low), Geopolitical (Low)
4. **Report:** Gold Tier recommendation, approved for structural steel supply
5. **Monitoring:** Setup on-time delivery, quality, responsiveness tracking per order

## Performance Metrics

**Target Performance:**
- Pre-qualification turnaround: <5 business days
- Full evaluation report: <15 business days
- Performance monitoring data accuracy: >95%
- Tier classification accuracy: >98% (validated by subsequent performance)
- Re-assessment cycle: Annual for existing suppliers, or triggered by performance events