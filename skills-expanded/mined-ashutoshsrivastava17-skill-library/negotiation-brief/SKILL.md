---
name: negotiation-brief
description: >
  Prepare negotiation strategies with BATNA analysis, concession planning,
  target pricing, and term priorities. Structure negotiation playbooks for
  procurement discussions with vendors and suppliers.
  TRIGGER when: user says /negotiation-brief, "negotiation brief", "negotiation prep",
  "vendor negotiation", "contract negotiation strategy", "prepare for negotiation",
  "negotiation playbook", or asks about preparing for a procurement negotiation.
argument-hint: "[vendor name] [deal context]"
user-invocable: true
---

# Negotiation Brief

You are a senior procurement negotiator and commercial strategist. Produce a comprehensive negotiation brief that equips the team to negotiate from a position of strength, with clear targets, fallback positions, and tactical guidance.

## Core Principles

1. **Prepare more than you think you need** — 80% of negotiation success is preparation
2. **Know your BATNA** — Your power comes from your ability to walk away
3. **Separate people from positions** — Focus on interests, not fixed demands
4. **Anchor strategically** — The first credible number shapes the entire negotiation
5. **Document everything** — Verbal agreements are forgotten; written terms survive

---

## Process

### Step 1 — Define Negotiation Context

Establish the landscape before planning strategy.

| Element | Description | Details |
|---|---|---|
| **Vendor** | Vendor name and key contacts | [Name, roles, relationship history] |
| **Deal Type** | New contract, renewal, amendment, or expansion | [Type] |
| **Contract Value** | Estimated total or annual value | [$Amount] |
| **Current State** | Existing terms (if renewal) or market baseline | [Summary] |
| **Timeline Pressure** | Contract expiry, business deadlines, budget cycles | [Dates and drivers] |
| **Decision Authority** | Who can approve the final deal on your side | [Name, approval limits] |
| **Relationship Temperature** | Current vendor relationship quality | Strong / Neutral / Strained |
| **Competitive Alternatives** | Other vendors considered or available | [List with readiness level] |

### Step 2 — BATNA Analysis

Define your Best Alternative to a Negotiated Agreement.

| Component | Your Side | Vendor's Side (Estimated) |
|---|---|---|
| **BATNA** | What you will do if no deal is reached | What the vendor will do if no deal |
| **BATNA Quality** | Strong / Moderate / Weak | Strong / Moderate / Weak |
| **Walk-Away Point** | Maximum price or minimum terms you will accept | Minimum price or terms they need |
| **Time Pressure** | How urgently you need this deal closed | How urgently they need this revenue |
| **Switching Cost** | Cost and effort to switch to alternative | Cost of losing you as a customer |
| **Information Advantage** | What you know that they do not | What they know that you do not |

**BATNA Strengthening Tactics:**

| Action | Impact | Effort |
|---|---|---|
| Obtain a competing quote | High — creates real alternative pressure | Medium |
| Identify an open-source or in-house option | Medium — shows you have options | Low |
| Align with peer companies for volume leverage | High — increases buying power | High |
| Extend current contract short-term | Medium — removes time pressure | Low |
| Pre-approve budget for the alternative | High — makes walk-away credible | Medium |

### Step 3 — Set Targets and Ranges

Define specific positions for every negotiable term.

| Term | Current / Market | Target (Ideal) | Acceptable | Walk-Away | Priority |
|---|---|---|---|---|---|
| Annual price | $X | $Y (-15%) | $Z (-8%) | $W (-3%) | Critical |
| Contract length | 1 year | 2 years (with exit) | 3 years (with exit) | > 3 years locked | High |
| Payment terms | Net 30 | Net 60 | Net 45 | Net 30 | Medium |
| Price escalation cap | None | 0% Year 1, CPI cap | 3% annual cap | 5% annual cap | High |
| SLA uptime | 99.5% | 99.95% | 99.9% | 99.5% | Critical |
| SLA credits | None | 10% per 0.1% miss | 5% per 0.1% miss | Any credit clause | High |
| Termination for convenience | None | 30-day notice | 60-day notice | 90-day notice | Critical |
| Data portability | Not addressed | Full export, any time | Export on termination | Any export clause | High |
| Liability cap | Uncapped | 2x annual fees | 1x annual fees | Any cap | Medium |
| Support hours | Business hours | 24/7 for P1 | Extended hours for P1 | Business hours + P1 | Medium |

### Step 4 — Plan Concessions

Prepare your give-to-get strategy.

| What You Can Give | Value to Vendor | Cost to You | What to Get in Return |
|---|---|---|---|
| Longer contract commitment | High — revenue predictability | Medium — reduced flexibility | Lower annual price, price cap |
| Case study or reference | Medium — marketing value | Low — some time investment | Discount or additional services |
| Faster payment terms | Medium — improved cash flow | Low — if cash is available | Unit price reduction |
| Volume commitment | High — guaranteed revenue | Medium — usage obligation | Tiered pricing, volume discounts |
| Public endorsement / logo usage | Medium — brand credibility | Low | Waived implementation fees |
| Early renewal before expiry | High — removes churn risk | Medium — loses leverage window | Multi-year price lock |

**Concession Rules:**
- Never give a concession without getting something in return
- Start with low-cost-to-you, high-value-to-them concessions
- Make concessions progressively smaller to signal you are nearing your limit
- Always frame concessions as conditional: "If you can do X, we could consider Y"

### Step 5 — Prepare Tactical Playbook

Plan for common negotiation scenarios.

| Scenario | Tactic | Script / Approach |
|---|---|---|
| Vendor opens with high anchor | Counter-anchor with data | "Based on our market analysis and competing quotes, the benchmark for this is $X" |
| Vendor says "best and final offer" | Test the claim | "We appreciate that. Let us take this to our alternative vendor and compare before deciding" |
| Vendor pressures for quick close | Remove time pressure | "We need to complete our due diligence regardless of timeline — quality of terms matters more than speed" |
| Vendor bundles unwanted items | Unbundle and reprice | "We only need A and C from this bundle. What is the pricing for those components individually?" |
| Vendor escalates to your executive | Maintain single channel | Brief executives in advance: "If they reach out, redirect to the negotiation team" |
| Stalemate on price | Shift to non-price terms | "If price is firm, let us discuss SLA credits, support tier, and contract flexibility" |
| Vendor threatens to walk away | Assess BATNA calmly | "We respect your position. We have alternatives we can pursue — let us both take time to reconsider" |

---

## Output Format

Deliver the negotiation brief as a structured document:

```markdown
# Negotiation Brief — [Vendor Name]

**Deal Type:** [New / Renewal / Amendment]
**Estimated Value:** [$Amount]
**Negotiation Date:** [Date]
**Prepared by:** [Name]
**Approved by:** [Decision Authority]

---

## 1. Context and Background
[Deal context, relationship history, current state]

## 2. BATNA Analysis
[Your BATNA, vendor's estimated BATNA, walk-away points]

## 3. Negotiation Targets
[Term-by-term target, acceptable, and walk-away positions]

## 4. Concession Strategy
[Planned give-to-get trades, ordered by priority]

## 5. Tactical Playbook
[Scenario-based tactics and prepared responses]

## 6. Team Roles
| Role | Person | Responsibility |
|---|---|---|
| Lead Negotiator | [Name] | Drives discussion, makes offers |
| Technical Expert | [Name] | Validates technical claims and feasibility |
| Commercial Analyst | [Name] | Tracks terms against targets in real time |
| Decision Authority | [Name] | Final approval — not present at table |

## 7. Red Lines (Non-Negotiable)
[List of absolute deal-breakers that trigger walk-away]

## 8. Post-Negotiation Checklist
- [ ] All agreed terms documented in writing
- [ ] Legal review of final contract language
- [ ] Comparison of final terms to original targets
- [ ] Debrief with negotiation team on lessons learned
```

---

## Quality Checklist

- [ ] BATNA is realistic, not aspirational — you could actually execute it
- [ ] Walk-away points are defined for every critical term
- [ ] Concession plan follows the give-to-get principle — nothing is given for free
- [ ] Tactical playbook covers at least 5 common vendor scenarios
- [ ] Team roles are assigned with clear boundaries (especially decision authority)
- [ ] Red lines are genuinely non-negotiable, not wish-list items relabeled
- [ ] Competing quotes or market data are available to support anchor positions
- [ ] The brief has been reviewed with the decision authority before negotiation
- [ ] Vendor's likely BATNA and pressure points have been researched
- [ ] All financial calculations have been verified (TCO, savings, ROI)

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Sole-source vendor with no alternatives | Focus on non-price terms (SLAs, support, flexibility); build long-term alternative in parallel |
| Vendor is a strategic partner, not just a supplier | Balance hard negotiation with relationship preservation; use collaborative framing |
| Multi-year renewal with significant price increase | Benchmark against market; obtain competing quotes even if not planning to switch |
| Negotiating with a startup or small vendor | Be cautious of over-leveraging; a vendor pushed too hard may fail or under-deliver |
| Cross-border deal with currency risk | Negotiate currency clause or cap; define which party bears FX risk |
| Multiple stakeholders on vendor side with different agendas | Identify the actual decision-maker; tailor messaging to their interests |
| Prior negotiation left a negative impression | Acknowledge history; reset the tone; focus on mutual value creation |
