---
name: m-and-a
description: "When to activate: mergers and acquisitions, M&A, acquisition, due diligence, letter of intent, LOI, valuation, integration, buy-side, sell-side"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: c-level
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Mergers & Acquisitions

## M&A Process Overview

### Buy-side Process (Acquiring)
```
1. Strategy → 2. Target Identification → 3. Approach → 4. NDA + Information Sharing
→ 5. LOI → 6. Due Diligence → 7. Definitive Agreement → 8. Close → 9. Integration
```

### Sell-side Process (Being Acquired)
```
1. Prepare (clean house) → 2. Banker selection → 3. Information memorandum
→ 4. Investor outreach → 5. IOI (Indication of Interest) → 6. Management presentations
→ 7. LOI / Term sheet → 8. Exclusivity → 9. Due diligence → 10. Definitive agreement → 11. Close
```

---

## Buy-side vs. Sell-side

| Dimension | Buy-side (Acquirer) | Sell-side (Target) |
|-----------|--------------------|--------------------|
| Objective | Deploy capital, gain capabilities/market | Maximize valuation, find right partner |
| Timeline | 3–12 months typical | 6–18 months for full process |
| Leverage | Controls deal structure | Runs competitive process for leverage |
| Advisors | Buy-side advisor (optional at smaller deals) | Investment banker mandatory for $10M+ |
| Risk | Overpayment, integration failure | Getting locked into low valuation, cultural mismatch |

---

## Strategic Rationale (Why Acquire)

**Common M&A Rationales:**
- **Market expansion**: New geographies, customer segments
- **Product extension**: Add adjacent capabilities
- **Talent / acqui-hire**: Acquire the team, shut down the product
- **Technology**: Buy IP or proprietary tech
- **Market share / consolidation**: Remove competitor, gain scale
- **Vertical integration**: Control supply or distribution

**Acquirer red flags**: "Strategic fit" without financial model; synergies defined vaguely; deal driven by FOMO or competitive pressure.

---

## Letter of Intent (LOI)

Non-binding document establishing deal intent. Key elements:

```
1. Purchase price (or range)
2. Deal structure (stock vs. asset purchase; cash vs. equity consideration)
3. Exclusivity period (typically 30–60 days)
4. Key conditions (closing conditions)
5. Representations and warranties intent
6. Break-up fee (if applicable)
7. Timeline to definitive agreement
```

**LOI is binding only for**: exclusivity, confidentiality, no-shop provisions.

---

## Due Diligence Checklist

### Commercial DD
- [ ] Customer list + contract terms + concentration
- [ ] Pipeline + conversion rates
- [ ] Churn + NRR analysis
- [ ] Competitive positioning interview (3-5 customers)
- [ ] Channel and partnership agreements
- [ ] GTM model and sales efficiency

### Financial DD
- [ ] 3 years audited or reviewed financials
- [ ] Revenue recognition methodology
- [ ] ARR/MRR build and reconciliation
- [ ] Unit economics (CAC, LTV, payback)
- [ ] Working capital analysis
- [ ] Off-balance-sheet liabilities
- [ ] Tax returns + open tax liabilities

### Technical DD
- [ ] Code repository access + architecture review
- [ ] Security posture (penetration test results)
- [ ] IP ownership and assignments
- [ ] Open source license compliance
- [ ] Technical debt assessment
- [ ] Scalability and infrastructure

### Legal DD
- [ ] Certificate of incorporation + cap table
- [ ] Board minutes (last 3 years)
- [ ] Material contracts (customer, vendor, employment)
- [ ] IP ownership + any third-party claims
- [ ] Litigation and regulatory matters
- [ ] Employment agreements (esp. NDAs, non-competes)

### People DD
- [ ] Org chart + key person dependencies
- [ ] Compensation and benefits analysis
- [ ] Culture assessment (team interviews)
- [ ] Reference checks on founders/exec team
- [ ] Flight risk assessment (key employees)

---

## Valuation Methods

### 1. Discounted Cash Flow (DCF)
- Project free cash flows for 5-10 years
- Apply terminal value (Gordon Growth Model or exit multiple)
- Discount at WACC
- Strengths: Forward-looking, intrinsic value. Weakness: Sensitive to assumptions.

### 2. Comparable Company Analysis (Comps)
- Find 6-10 public company peers
- Calculate multiples: EV/Revenue, EV/EBITDA, P/E
- Apply median/mean to target's metrics
- Requires liquidity discount for private companies (15-30%)

### 3. Precedent Transaction Analysis
- Find similar M&A transactions in last 3-5 years
- Extract deal multiples (usually higher than comps due to control premium)
- Apply to target metrics

### SaaS-Specific Valuation Benchmarks
```
ARR Multiple:  Series A/B: 5-10x ARR; Scale: 8-20x ARR
EBITDA Multiple: Profitable SaaS: 15-30x EBITDA
NTM Revenue Multiple: Varies 3-15x based on growth rate
Rule of 40 Score: >40% often commands premium multiple
```

---

## Deal Structures

### Asset Purchase
- Acquirer buys specific assets and liabilities
- Seller retains entity (and remaining liabilities)
- Tax: Buyer gets step-up in basis; seller pays ordinary income
- Common in: distressed acquisitions, IP-only deals

### Stock Purchase
- Acquirer buys all equity from shareholders
- Liabilities transfer with company
- Tax: Seller pays capital gains (preferential)
- Common in: full company acquisitions

### Merger
- Two entities combine into one
- Requires shareholder vote
- Common in: public company M&A

### Consideration Types
- **Cash**: Clean, immediate; dilutes buyer's cash
- **Stock**: Seller shares upside/downside; requires registration if public
- **Earnout**: Portion of consideration tied to future performance milestones

---

## Integration Planning

### Day 1–30: Stabilize
- Communicate to all employees (message: job security, leadership continuity)
- Establish integration team and governance
- Freeze organizational changes (30-day moratorium)
- Address customer and vendor questions proactively

### Day 30–90: Assess
- Culture assessment — identify similarities and friction points
- Systems audit — which tech stacks survive?
- Process mapping — where do workflows conflict?
- Quick wins — identify 3-5 integration wins to deliver fast

### Day 90–180: Integrate
- Org structure finalized
- Systems migration begun
- Key employees retention packages finalized
- Revenue synergy plans activated

### Integration Workstreams
- People & Culture
- Technology & Systems
- Finance & Legal
- Customer & Revenue
- Operations & Supply Chain

---

## Culture Integration

**Most acquisitions fail due to culture mismatch, not financial assumptions.**

### Integration Approaches
| Approach | When to Use |
|----------|-------------|
| **Absorption**: Target adopts acquirer's culture | Acqui-hire; distressed acquisition |
| **Preservation**: Target operates independently | Acquirer buys distribution; target has strong brand |
| **Symbiosis**: Best of both cultures merged | Strategic merger of equals |
| **Holding**: Separate entities; no integration | Conglomerate; portfolio diversification |

### Culture Due Diligence Questions
- What decisions require approval and at what level?
- How does the company handle failure?
- What do top performers care about most?
- How do teams collaborate across functions?

---

## M&A Red Flags

**In targets:**
- Revenue concentration in 1-2 customers (>30% = high risk)
- Founder dependency — company can't operate without them
- Undisclosed litigation or regulatory exposure
- Unrealistic financial projections without support
- High voluntary churn in last 6 months

**In buyers:**
- Acquisition as substitute for organic strategy
- Integration team under-resourced
- Overpayment rationalized by aggressive synergy assumptions
- Cultural incompatibility ignored during deal excitement
