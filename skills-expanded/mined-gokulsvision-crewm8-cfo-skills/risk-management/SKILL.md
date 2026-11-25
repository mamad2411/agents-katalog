---
name: risk-management
description: Identify, assess, and manage financial and operational risks — concentration risk, compliance risk, market risk, operational risk, and insurance coverage recommendations for startup resilience.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, risk-management, operational-risk, insurance, concentration-risk, business-continuity]
related_skills: [scenario-planning, internal-controls-design, audit-preparation, tax-compliance-management]
inputs_required: [current-risk-register-if-exists, customer-concentration-data, insurance-policy-list, operational-dependencies-list, financial-data-revenue-cash-burn]
deliverables: [comprehensive-risk-register-scored-and-owned, top-10-risks-with-mitigation-status, insurance-coverage-gap-analysis, business-continuity-essentials]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Risk Management

Identify, assess, and manage the full spectrum of startup risks — financial, operational, market, and strategic. Maintain a risk register, prioritize by likelihood and impact, and ensure mitigations are in place. Goal: the company isn't blindsided by preventable risks.

## Purpose

Startups operate with extreme uncertainty and very little margin for error. A single risk event — losing a key customer, a data breach, a co-founder leaving, a fundraising freeze — can be existential. Yet most startups manage risks reactively, only addressing them after they materialize. This skill provides the systematic framework to identify risks early, score them by likelihood and impact, assign owners, implement mitigations, and review quarterly so the company isn't blindsided.

## When to Use

- "What are our biggest risks?"
- "Build / review our risk register"
- "Are we adequately insured?"
- "What's our customer concentration risk?"
- "Risk assessment for the board"
- "Business continuity planning"
- "Vendor / supply chain risk"

## Inputs Required

- Current risk register (if one exists)
- Customer concentration data (top customers by revenue)
- Insurance policies (current coverage and limits)
- Operational dependencies (key vendors, systems, people)
- Financial data (revenue, cash burn, runway)
- Employee list (key person identification)

## Quick Reference

| Risk Category | Key Risks for Startups | Typical Score |
|---------------|----------------------|---------------|
| Financial | Customer concentration, cash shortfall, fraud | Highest |
| Operational | Key person dependency, data breach, vendor lock-in | High |
| Market & Strategic | Competitor launch, market contraction, fundraising freeze | Medium-High |

| Insurance Type | When to Get | Approx. Annual Cost |
|---------------|-------------|-------------------|
| General Liability | Day 1 | $500-1,500 |
| D&O | First outside funding | $2,000-5,000 |
| EPLI | First employee | Often bundled with D&O |
| Cyber / Data Breach | Collecting customer data | $1,500-4,000 |
| Key Person | Seed+ | $2,000-8,000 |
| Errors & Omissions | Enterprise customers | $3,000-8,000 |

## Procedure

### 1. Initial Risk Assessment

For each risk category, identify risks with the leadership team. Don't do this alone — finance sees financial risks, but engineering sees tech risks, sales sees market risks, etc.

### 2. Score Each Risk

```
Likelihood (1-5):
  1 = Very unlikely ( < 5% in next 12 months)
  2 = Unlikely (5-15%)
  3 = Possible (15-35%)
  4 = Likely (35-65%)
  5 = Very likely ( > 65%)

Impact (1-5):
  1 = Negligible ( < $10k or < 1 week impact)
  2 = Minor ($10k-$50k or 1-4 weeks)
  3 = Moderate ($50k-$250k or 1-3 months)
  4 = Severe ($250k-$1M or 3-6 months)
  5 = Existential ( > $1M or company survival at risk)

Risk Score = Likelihood × Impact
  ≥ 15 = Critical — must mitigate now
  10-14 = High — mitigate this quarter
  5-9 = Medium — monitor and plan
  < 5 = Low — accept
```

### 3. Assign Owners & Mitigations

Every risk rated High or above needs:
- A named owner.
- A concrete mitigation plan.
- A review date.

### 4. Quarterly Review

Review the register with the leadership team. Risks change as the company evolves.

### Risk Categories

#### Financial Risks

| Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|
| **Customer concentration** (>20% revenue from one customer) | High in early stage | Very High | Diversify pipeline, negotiate multi-year contracts | In progress |
| **Revenue concentration** (one product/channel/geo) | Medium | High | Diversify over time, don't over-invest in one vector | Monitor |
| **Cash shortfall** (< 6 months runway) | Low | Existential | Maintain > 12 months runway, weekly cash monitoring | Controlled |
| **Currency / FX risk** (significant non-USD exposure) | Medium | Medium | Natural hedging (match revenue and costs by currency) | Monitor |
| **Bad debt** (large AR write-offs) | Low | Medium | AR aging monitoring, payment terms for risky customers | Controlled |
| **Fraud** (internal or external) | Low | Very High | Segregation of duties, dual approvals, fraud awareness training | Controlled |

#### Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Key person dependency** (CEO, CTO, key engineer) | Medium | Very High | Document processes, cross-train, key person insurance |
| **Data breach / security incident** | Medium | High | SOC 2, penetration testing, incident response plan, cyber insurance |
| **System outage / downtime** | Medium | Medium | SLA commitments, redundancy, incident response, status page |
| **Vendor lock-in** (AWS, Salesforce, etc.) | High (by design) | Medium | Multi-cloud where practical, data portability, migration plan on file |
| **IP / legal risk** (unclear IP ownership, patent troll) | Low | High | IP assignment from all founders/employees/contractors, patent review |
| **Regulatory change** (new law affects business model) | Low | High | Regulatory monitoring, trade association membership, legal counsel retained |
| **Bank failure / loss of access to funds** | Low | Very High | Two-bank rule, sweep accounts, FDIC coverage verification |

#### Market & Strategic Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Competitor launch** (well-funded competitor in your space) | Medium | High | Competitive moat (network effects, switching costs), speed of execution |
| **Market contraction** (TAM shrinking or budget cuts) | Low-Medium | High | Multi-segment strategy, recession-resistant value prop |
| **Technology disruption** (new tech makes you obsolete) | Low | Very High | R&D investment, startup agility advantage, watch the edges |
| **Talent market** (can't hire critical roles) | Medium | High | Employer brand, remote-first, competitive comp |
| **Fundraising market freeze** | Medium (cyclical) | High | Extend runway to 24+ months, path to profitability, relationship-building pre-need |
| **Founder conflict** | Low | Existential | Clear equity and role agreements, founder vesting, regular check-ins |

### Risk Register Format

Maintain as a living document:

| ID | Risk | Category | Likelihood (1-5) | Impact (1-5) | Risk Score (L×I) | Owner | Mitigation | Last Reviewed | Status |
|---|---|---|---|---|---|---|---|---|---|
| FIN-01 | Customer concentration | Financial | 4 | 5 | 20 | VP Sales / CFO | Pipeline diversification tracking | Apr 2026 | 🟡 |
| OPS-04 | Key person (CTO) | Operational | 3 | 5 | 15 | CEO | Document processes, identify internal successor candidate | Mar 2026 | 🟡 |
| FIN-06 | Cash shortfall | Financial | 1 | 5 | 5 | CFO | Weekly cash monitoring, 13-week forecast, 20+ mo runway | Apr 2026 | 🟢 |

### Insurance Coverage Review

At minimum, every startup should evaluate:

| Insurance Type | When to Get It | Typical Coverage | Approx. Annual Cost |
|---|---|---|---|
| **General Liability** | Day 1 | Bodily injury, property damage, personal injury | $500-1,500 |
| **Directors & Officers (D&O)** | First outside funding | Protects directors/officers from lawsuits, covers defense costs | $2,000-5,000 for $1M coverage |
| **Employment Practices Liability (EPLI)** | First employee | Wrongful termination, discrimination, harassment claims | Often bundled with D&O |
| **Cyber / Data Breach** | Collecting any customer data | Breach response, notification costs, forensic investigation, fines | $1,500-4,000 for $1M coverage |
| **Key Person** | Seed+ | Pays the company if a key person dies or becomes disabled. Funds transition/search. | $2,000-8,000 depending on coverage amount |
| **Workers Comp** | First employee (legally required in most states) | Employee injury/illness on the job | Varies by state and payroll |
| **Errors & Omissions (E&O) / Tech E&O** | Enterprise customers demand it | Professional negligence, failure to perform, product defects | $3,000-8,000 for $1-2M coverage |
| **Commercial Property** | Physical office/equipment | Damage to office, equipment, inventory | $500-2,000 |

## Output Format

- Comprehensive risk register (scored, owned, tracked)
- Top 10 risks with mitigation status
- Insurance coverage gap analysis
- Business continuity essentials (what's the plan if the office burns down / bank account is frozen / AWS goes down?)

## Done Criteria

The skill is complete when:
1. Risks are identified across all four categories (financial, operational, market, strategic).
2. Each risk is scored (Likelihood × Impact) and ranked.
3. High and Critical risks have named owners and concrete mitigation plans.
4. Insurance coverage is reviewed against a startup checklist and gaps are identified.
5. A quarterly review cadence is established.
6. The risk register is documented as a living document.

## Pitfalls

- **Building a risk register and never reviewing it** — the risk register that sits on a shelf is worse than useless because it creates a false sense of security. Review it quarterly, or it's not a risk management tool, it's a document.
- **Assessing risks in a silo** — if only finance builds the risk register, you'll miss tech risks (data breach), market risks (competitor launch), and people risks (key person dependency). The risk assessment must include the full leadership team.
- **Ignoring correlated risks** — a recession doesn't just lower revenue. It also makes fundraising harder, increases churn, and makes it harder to hire. Never model risks independently; always stress at least one scenario where multiple levers break simultaneously.
- **Over-insuring** — startups overpay for insurance because they bundle everything their broker recommends. Shop annually. Most brokers will cut renewals by 10-20% if you ask.
- **Not buying D&O insurance before you need it** — the best time to buy D&O is when there are no claims. Once a lawsuit is filed, it's too late or prohibitively expensive.

### Heuristics

- **Customer concentration is the #1 startup risk**: if one customer is > 20% of revenue, it's a material risk. Disclose to investors, work to diversify.
- **D&O insurance is worth it from the first outside dollar**: founders can be personally sued. D&O protects them.
- **Key person risk is underappreciated**: in a 10-person startup, losing the CTO can kill the company. Insurance + documentation + succession thinking.
- **Don't over-insure**: startups overpay for insurance. Shop annually. Most brokers will cut renewals by 10-20% if you ask.

### Edge Cases

- **Hardware / physical product startups**: additional risks — supply chain, manufacturing quality, inventory obsolescence, product liability.
- **Regulated industries** (fintech, healthtech, edtech): regulatory risk is elevated. Invest in compliance early.
- **International operations**: country risk, sanctions compliance, FCPA/anti-bribery, currency repatriation restrictions.

## Verification

Can you answer "What are our top 3 risks right now and who owns each one?" and "When was the last time we reviewed the risk register?" and "If our largest customer left tomorrow, what would we do and how much cash would we lose?" If not, risk management is incomplete.

## Example

> **User**: "Build our risk register. What are our biggest risks and how do we mitigate them?"
> **Expected behavior**: You lead a cross-functional risk assessment with the leadership team, identify risks across all four categories, score each risk (Likelihood × Impact), build the risk register with named owners and concrete mitigations, present the top 10 risks with status indicators, and establish a quarterly review cadence.

> **User**: "Review our insurance coverage — are we missing anything?"
> **Expected behavior**: You audit current policies against the startup insurance checklist, identify gaps (e.g., no cyber insurance, D&O coverage limits too low for Series A stage), get competitive quotes from 2-3 brokers, recommend adjustments (add cyber insurance, increase D&O from $1M to $2M, shop renewal for 15% savings), and create an insurance renewal calendar.

## Linked Skills

- Financial scenario modeling → `scenario-planning`
- Operational controls → `internal-controls-design`
- Tax compliance risks → `tax-compliance-management`
- Audit & assurance → `audit-preparation`
