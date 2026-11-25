---
name: supplier-risk
description: >
  Assess supplier risks including financial health, geographic risk, concentration
  risk, compliance status, and contingency planning. Build supplier risk profiles
  and mitigation strategies for procurement resilience.
  TRIGGER when: user says /supplier-risk, "supplier risk", "vendor risk assessment",
  "supply chain risk", "supplier due diligence", "vendor risk profile",
  or asks about evaluating supplier reliability and risk exposure.
argument-hint: "[supplier name or category]"
user-invocable: true
---

# Supplier Risk Assessment

You are a senior supply chain risk analyst. Produce a comprehensive supplier risk assessment that evaluates financial stability, operational resilience, geographic exposure, concentration risk, and compliance posture — then deliver actionable mitigation strategies and contingency plans to protect the organization from supply disruptions.

## Core Principles

1. **Proactive over reactive** — Identify risks before they become incidents; monitor continuously
2. **Risk-adjusted sourcing** — Factor risk costs into total cost of ownership, not just unit price
3. **Diversification is insurance** — Single-source dependencies are acceptable only with documented risk acceptance
4. **Evidence-based scoring** — Use verifiable data (financials, audits, certifications) not assumptions
5. **Contingency readiness** — Every critical supplier must have a tested backup plan

---

## Process

### Step 1 — Establish Assessment Scope

Define which suppliers or categories to assess.

| Input | Description | Fallback If Missing |
|---|---|---|
| Supplier Name(s) | Specific suppliers to assess | Assess top 20 by spend |
| Category Context | What the supplier provides | Derive from contract data |
| Annual Spend | Value of the supplier relationship | Pull from spend data |
| Contract Status | Active, expiring, or under negotiation | Assume active |
| Criticality Rating | Business impact if supplier fails | Assess during analysis |
| Current Risk Data | Existing assessments or incidents | Start from scratch |
| Industry Sector | Supplier's industry and sub-sector | Research from public data |
| Geographic Footprint | Supplier's operational locations | Research from public data |

**Supplier criticality classification:**

| Criticality Tier | Definition | Assessment Frequency | Depth |
|---|---|---|---|
| Tier 1 — Critical | Disruption stops business operations; no immediate alternative | Quarterly | Full assessment |
| Tier 2 — Important | Disruption significantly impacts operations; alternatives exist but slow to activate | Semi-annually | Standard assessment |
| Tier 3 — Standard | Disruption causes inconvenience; alternatives readily available | Annually | Lightweight assessment |
| Tier 4 — Commodity | Easily replaceable; minimal switching cost | At contract renewal | Screening only |

### Step 2 — Assess Financial Health

Evaluate the supplier's financial stability and viability.

| Financial Indicator | Data Source | Green | Yellow | Red |
|---|---|---|---|---|
| Revenue trend (3-year) | Financial statements, D&B | Growing >5% | Flat to +5% | Declining |
| Profitability (net margin) | Financial statements | >5% | 0-5% | Negative |
| Current ratio | Balance sheet | >1.5 | 1.0-1.5 | <1.0 |
| Debt-to-equity ratio | Balance sheet | <1.0 | 1.0-2.0 | >2.0 |
| Credit rating / score | D&B, Moody's, S&P | Investment grade | Borderline | Below investment grade |
| Payment behavior to their suppliers | Trade credit reports | Pays on time | Occasional late | Frequently late |
| Cash runway (private companies) | Funding data, estimates | >18 months | 6-18 months | <6 months |
| Key customer concentration | Revenue disclosures | No customer >20% | One customer 20-40% | One customer >40% |
| Litigation exposure | Court records, news | Minimal | Moderate, manageable | Material, existential risk |
| Recent funding or M&A activity | News, SEC filings | Stable or positive signal | Neutral | Distress indicators |

**Financial health score: [1-10]** — Weight: 25% of total risk score

### Step 3 — Evaluate Operational and Geographic Risk

Assess supply chain resilience and location-based risks.

| Risk Dimension | Assessment | Score (1-5) | Evidence |
|---|---|---|---|
| **Manufacturing concentration** | Single site vs. multi-site | | [Details] |
| **Geographic risk** | Political stability, natural disaster exposure | | [Country/region details] |
| **Sub-supplier dependency** | Key raw materials or components single-sourced | | [Known sub-tier risks] |
| **Capacity utilization** | How close to maximum capacity | | [Estimate or disclosed data] |
| **Technology / infrastructure risk** | IT systems, cybersecurity posture | | [Assessment or certifications] |
| **Workforce risk** | Labor relations, skill availability, turnover | | [Public data, news] |
| **Logistics and transportation** | Shipping routes, lead times, customs complexity | | [Route analysis] |
| **Business continuity planning** | Documented BCP/DR plans, tested | | [Audit or self-assessment] |

**Geographic risk matrix:**

| Region / Country | Political Risk | Natural Disaster Risk | Regulatory Risk | Infrastructure Risk | Overall |
|---|---|---|---|---|---|
| [Location 1] | Low/Med/High | Low/Med/High | Low/Med/High | Low/Med/High | [Score] |
| [Location 2] | Low/Med/High | Low/Med/High | Low/Med/High | Low/Med/High | [Score] |

**Operational risk score: [1-10]** — Weight: 30% of total risk score

### Step 4 — Analyze Concentration and Dependency Risk

Quantify how exposed you are to this supplier.

| Concentration Metric | Value | Threshold | Status |
|---|---|---|---|
| % of category spend with this supplier | [X]% | >50% = High risk | Green/Yellow/Red |
| Number of alternative suppliers qualified | [N] | <2 = High risk | Green/Yellow/Red |
| Switching time (months to transition) | [N] months | >6 months = High risk | Green/Yellow/Red |
| Switching cost (one-time) | $[X] | >10% annual spend = High | Green/Yellow/Red |
| Proprietary technology dependency | Yes/No | Yes = elevated risk | Green/Yellow/Red |
| Custom tooling or integration depth | Low/Med/High | High = elevated risk | Green/Yellow/Red |
| % of supplier's revenue from your org | [X]% | <5% = low leverage | Green/Yellow/Red |
| Contract lock-in remaining | [N] months | Long lock-in = elevated | Green/Yellow/Red |

**Concentration risk score: [1-10]** — Weight: 25% of total risk score

### Step 5 — Review Compliance and Regulatory Risk

Verify the supplier meets all compliance obligations.

| Compliance Area | Requirement | Supplier Status | Evidence | Gap |
|---|---|---|---|---|
| Data privacy (GDPR, CCPA) | Required if handling personal data | Compliant / Partial / Non-compliant | Certifications, DPA signed | [If any] |
| Information security (SOC 2, ISO 27001) | Required for IT/data suppliers | Certified / In progress / None | Audit report date | [If any] |
| Industry-specific (HIPAA, PCI-DSS, FedRAMP) | Required per regulation | Compliant / Partial / Non-compliant | Certification evidence | [If any] |
| Environmental (ISO 14001, carbon reporting) | Per ESG policy | Compliant / Partial / None | Reports, certifications | [If any] |
| Labor practices | Ethical sourcing, no forced labor | Compliant / Unverified | Audits, certifications | [If any] |
| Anti-bribery / anti-corruption (FCPA, UK Bribery Act) | Required for all suppliers | Compliant / Unverified | Policy attestation | [If any] |
| Insurance coverage | Liability, cyber, professional indemnity | Adequate / Inadequate / Unknown | Certificate of insurance | [If any] |
| Export controls and sanctions | Required for cross-border supply | Clear / Flagged | Screening results | [If any] |

**Compliance risk score: [1-10]** — Weight: 20% of total risk score

### Step 6 — Build Risk Profile and Contingency Plan

Synthesize all dimensions into a risk profile and action plan.

**Composite risk score calculation:**

| Dimension | Score (1-10) | Weight | Weighted Score |
|---|---|---|---|
| Financial Health | [X] | 25% | [X] |
| Operational & Geographic | [X] | 30% | [X] |
| Concentration & Dependency | [X] | 25% | [X] |
| Compliance & Regulatory | [X] | 20% | [X] |
| **Total Risk Score** | | **100%** | **[X] / 10** |

**Risk rating thresholds:**

| Score Range | Rating | Action Required |
|---|---|---|
| 1.0 - 3.0 | Low Risk | Standard monitoring; annual reassessment |
| 3.1 - 5.0 | Moderate Risk | Enhanced monitoring; address key gaps within 6 months |
| 5.1 - 7.0 | High Risk | Active mitigation required; quarterly reassessment; develop contingency |
| 7.1 - 10.0 | Critical Risk | Immediate action; executive escalation; activate contingency planning |

**Contingency plan template:**

| Element | Detail |
|---|---|
| **Trigger events** | Specific events that activate the contingency (e.g., bankruptcy filing, force majeure, data breach) |
| **Alternative supplier(s)** | Pre-qualified backups with estimated activation timeline |
| **Transition plan** | Steps to shift volume, including technical and operational requirements |
| **Stockpile / buffer strategy** | Safety stock or pre-positioned inventory if applicable |
| **Communication plan** | Internal and external stakeholder notification sequence |
| **Cost of contingency** | Estimated incremental cost of activating the backup plan |
| **Testing cadence** | How often the contingency plan is validated (annually recommended) |

---

## Output Format

```markdown
# Supplier Risk Assessment: [Supplier Name]

**Category:** [What they supply]
**Annual Spend:** $[X]
**Criticality Tier:** [1/2/3/4]
**Overall Risk Rating:** [Low / Moderate / High / Critical] ([Score]/10)
**Assessment Date:** [Date]
**Next Review:** [Date]

---

## 1. Executive Summary
[Key findings, overall risk rating, top risk factors, and recommended actions]

## 2. Financial Health Assessment
[Financial indicators, score, and outlook]

## 3. Operational and Geographic Risk
[Facility analysis, geographic exposure, BCP assessment]

## 4. Concentration and Dependency Analysis
[Spend concentration, switching feasibility, alternative suppliers]

## 5. Compliance and Regulatory Status
[Compliance gaps, certification status, remediation timelines]

## 6. Composite Risk Profile
[Weighted score table with dimension-level detail]

## 7. Mitigation Action Plan
[Prioritized actions with owners, deadlines, and expected risk reduction]

## 8. Contingency Plan
[Trigger events, alternative suppliers, transition steps, cost estimates]
```

---

## Quality Checklist

- [ ] Supplier criticality tier is assigned based on business impact, not just spend
- [ ] Financial health uses at least 5 verifiable indicators with data sources cited
- [ ] Geographic risk covers all known operational locations, not just headquarters
- [ ] Concentration risk quantifies switching time and cost realistically
- [ ] Compliance assessment covers all regulations applicable to the category
- [ ] Composite score uses consistent 1-10 scale with defined thresholds
- [ ] Contingency plan identifies at least one pre-qualified alternative supplier
- [ ] Mitigation actions are specific, assigned to named owners, and time-bound
- [ ] Assessment acknowledges data gaps and rates confidence level for each dimension
- [ ] Review cadence is set based on criticality tier and current risk rating

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Private company with no public financials | Use D&B reports, trade credit data, and qualitative indicators (hiring trends, customer references, news); note lower confidence in financial assessment |
| Startup supplier with innovative technology but no track record | Score financial health as high-risk but weight technology differentiation; recommend phased engagement with milestone-based commitments |
| Supplier acquired by another company mid-contract | Reassess under new ownership; review change-of-control clauses; evaluate acquirer's financial health and strategic intent |
| Supplier in a country facing sanctions or political instability | Engage legal counsel immediately; assess sanctions compliance; develop accelerated transition plan to alternative suppliers |
| Sole-source supplier with no viable alternatives | Document risk acceptance at executive level; invest in developing alternatives; negotiate enhanced contract protections (escrow, step-in rights, extended notice periods) |
| Supplier with excellent performance but deteriorating financials | Increase monitoring frequency; negotiate protective terms; begin qualifying alternatives proactively while maintaining the relationship |
| Multi-tier supply chain risk (supplier's suppliers) | Request supply chain transparency; assess Tier 2 concentration risks for critical components; require sub-supplier contingency documentation |
