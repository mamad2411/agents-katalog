---
title: Procurement Supplier Tier Classification
description: Evaluate, score, and classify suppliers into tier levels (Platinum, Gold, Silver, Bronze, Suspended) based on qualification criteria and performance metrics
version: 1.0
frequency_percent: 20.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/01900_procurement/procurement-supplier-tier-classification
gigabrain_tags: disciplines, 01900_procurement, supplier-management, tier-classification, qualification, procurement
openstinger_context: 01900_procurement_operations, skill-execution
last_updated: 2026-04-02
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
---

# Procurement Supplier Tier Classification

## Overview
Evaluate, score, and classify suppliers into tier levels (Platinum, Gold, Silver, Bronze, Suspended) based on qualification criteria and performance metrics.

**Announce at start:** "I'm using the procurement-supplier-tier-classification skill for supplier evaluation."

## When to Use This Skill
**Trigger Conditions:** New supplier onboarding, periodic re-evaluation, or performance-based tier review

**Prerequisites:**
- Supplier qualification data available
- Performance metrics collected (minimum 3 months of history for existing suppliers)
- Financial stability data (credit reports, audited financials)
- Delivery performance records

## Tier Classification Criteria

### Qualification Framework
| Criterion | Weight | Evidence Required |
|-----------|--------|-------------------|
| Technical Capability | 25% | ISO 9001, product certifications, datasheets, test reports |
| Financial Stability | 20% | Audited financials, credit rating, bank references |
| Delivery Performance | 20% | On-time delivery %, lead-time adherence |
| Quality Performance | 15% | Defect rate, NCR history, warranty claims |
| Commercial Competitiveness | 10% | Price vs. market benchmark |
| Compliance & ESG | 10% | Safety record, environmental compliance |

### Tier Thresholds
| Tier | Score Range | Key Requirements |
|------|-------------|-----------------|
| **Platinum** | 90-100 | financial_risk=LOW, OTD >= 95% |
| **Gold** | 75-89 | financial_risk <= MEDIUM, OTD >= 85% |
| **Silver** | 60-74 | No critical NCRs, OTD >= 70% |
| **Bronze** | 40-59 | Active improvement plan required |
| **Suspended** | < 40 | No new orders, investigation required |

## Evaluation Procedure

### Step 1: Data Collection
1. Gather technical certification documents
2. Obtain latest financial/credit reports
3. Compile delivery performance data (last 12 months)
4. Review quality NCR history
5. Compare pricing against market benchmarks
6. Verify compliance certifications

### Step 2: Scoring
1. Score each criterion (0-100)
2. Apply weightings to calculate weighted score
3. Determine overall score

### Step 3: Tier Assignment
1. Apply tier threshold rules
2. Check mandatory requirements (financial_risk, OTD, NCRs)
3. Assign tier level
4. If gap between score and tier requirements, assign next lower tier

### Step 4: Documentation
1. Record evaluation results
2. Document tier assignment with justification
3. Set next review date
4. Update supplier registry

## Success Criteria
- [ ] All qualification criteria scored with documented evidence
- [ ] Weighted score calculation verified
- [ ] Tier assignment matches threshold rules
- [ ] Next review date scheduled
- [ ] Supplier registry updated
- [ ] Supplier notified of tier status

## Common Pitfalls
1. **Insufficient Performance Data** — New suppliers need minimum observation period
2. **Outdated Financial Data** — Use latest audited reports, not projections
3. **Ignoring Mandatory Requirements** — Even with high score, missing OTD or financial criteria lowers tier
4. **No Improvement Plan for Bronze** — Bronze tier requires documented improvement plan