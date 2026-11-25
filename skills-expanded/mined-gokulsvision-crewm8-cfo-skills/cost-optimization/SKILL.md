---
name: cost-optimization
description: Identify and execute cost optimization opportunities — vendor renegotiation, tool consolidation, process automation, efficiency improvements, and structural cost reduction for startup efficiency.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, cost-optimization, vendor-negotiation, efficiency, cost-reduction, automation]
related_skills: [budget-creation-management, profitability-analysis, business-case-modeling]
inputs_required: [current-spend-data-by-vendor-and-category, saas-subscription-list, vendor-contracts-and-renewal-dates, cloud-infrastructure-spend, contractor-roster]
deliverables: [spend-diagnostic-by-category, quick-win-list-with-savings-estimates, vendor-negotiation-queue-ranked, structural-improvement-roadmap, savings-tracker-projected-vs-actual]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cost Optimization

Run systematic cost optimization — not knee-jerk cutting, but disciplined, ongoing improvement of the company's cost structure. Renegotiate vendors, consolidate tools, automate processes, and find structural efficiencies. Goal: every dollar of spend is intentional and efficient.

## Purpose

Cost optimization in startups is a constant tension: spend enough to grow, but not so much that you run out of runway. Most startups either ignore costs until a crisis (leading to panic cuts that damage the business) or slash indiscriminately (cutting growth investment along with waste). This skill provides a structured, phased approach to cost optimization — quick wins first, then structural improvements, with strategic restructuring only when necessary. The goal is to find the waste without cutting the growth.

## When to Use

- "Optimize our costs"
- "Find savings in our OpEx"
- "Renegotiate vendor contracts"
- "Are we overspending anywhere?"
- "Cost reduction sprint"
- "Run a zero-based budget review"
- "Find 10% to cut without hurting growth"

## Inputs Required

- Current spend data by vendor and category (from AP and subscription management)
- SaaS subscription list with users, features, and cost
- Vendor contracts and renewal dates
- Cloud infrastructure spend (AWS, GCP, Azure)
- Contractor roster with rates and hours
- Headcount data (salary, benefits, tools per person)

## Quick Reference

| Phase | Timeline | Savings Potential | Risk |
|-------|----------|-------------------|------|
| Quick Wins | 1-4 weeks | 5-15% of OpEx | Low |
| Structural Improvements | 1-3 months | 15-30% of targeted areas | Medium |
| Strategic Restructuring | Crisis only | 20-30%+ of total burn | Severe |

| Cost Category | % of Total Spend | Typical Savings |
|---------------|-----------------|-----------------|
| Headcount (salaries + benefits) | 65-85% | 10-30% (crisis), 0-5% (ongoing) |
| SaaS / Software | 5-15% | 15-30% |
| Cloud Infrastructure | 3-10% | 20-40% |
| Professional Services | 2-8% | 20-50% |
| Marketing / Ads | 2-10% | 20-50% with smarter spend |
| Office / Rent | 2-8% | 20-40% |
| Travel & Entertainment | 1-3% | 50-80% |

## Procedure

### Phase 1: Diagnostic (Understand the Baseline)

Start with clean data from spend, subscriptions, and budget sources.

Break down every cost into types and assess optimization difficulty.

### Phase 2: Quick Wins (1-4 weeks)

These can be done immediately with minimal business disruption:

| Action | Estimated Savings | Time to Implement | Risk |
|---|---|---|---|
| Cancel unused SaaS subscriptions (< 1 active user) | $500-5,000/mo | 1-2 weeks | Low (verify no dependencies) |
| Downgrade over-provisioned SaaS plans (seats, tiers) | $200-2,000/mo | 1-2 weeks | Low |
| Switch SaaS subs to annual billing (save 15-20%) | $1,000-10,000/yr | 2-4 weeks | Low (cash flow timing) |
| Renegotiate top 5 vendors (ask for 10-20% off) | 10-20% of vendor spend | 2-4 weeks | Low-Medium |
| Cut unused or low-ROI marketing channels | $1,000-10,000/mo | 1-2 weeks | Low-Medium (verify attribution) |
| Audit and right-size cloud resources (idle instances, old snapshots) | 20-40% of cloud spend | 2-4 weeks | Medium (engineering time) |
| Cut travel budget, move to virtual events | 50-80% of travel spend | Immediate | Low |
| Audit contractor roster (still needed? full-time cheaper?) | 10-30% of contractor spend | 2-4 weeks | Medium |

### Phase 3: Structural Improvements (1-3 months)

Deeper changes that improve efficiency long-term:

| Action | What It Means | Savings | Effort |
|---|---|---|---|
| Tool consolidation | 2-3 tools that do similar things → pick 1 | 20-50% of those tool costs | Medium (migration) |
| Negotiate multi-year contracts | 2-3 year lock with 20-30% discount | 20-30% of vendor spend | Medium (commitment) |
| Insource vs outsource | Build internal capability vs rely on agencies/contractors | Case-by-case | High |
| Process automation | Automate manual finance/ops workflows | Time savings (1-2 FTE) | Medium-High |
| Vendor RFP / competitive bidding | Bid out your top 3 vendor categories | 10-25% of those categories | Medium |
| Office rationalization | Sublease unused space, renegotiate lease | 20-50% of office costs | Medium |

### Phase 4: Strategic Restructuring (Only in Crisis)

These hurt but save large amounts:

| Action | Savings | Impact |
|---|---|---|
| Hiring freeze | ~5-10% of annual burn (headcount stays flat) | Slows growth |
| Layoffs (10-20% of team) | 10-25% of total burn | Severe — culture, morale, momentum |
| Salary cuts | 10-20% of payroll for cuts applied | High flight risk for top performers |
| Kill a product / feature area | 10-30% of associated team cost | Strategic — refocuses the company |
| Pivot business model | Hard to quantify upfront | Existential — but sometimes necessary |

### Vendor Negotiation Playbook

#### The Framework

```
1. Know your leverage:
   - How much do you spend? (total, growth rate)
   - How hard would it be to switch?
   - Are you a logo they want? (brand value)
   - Is it renewal time? (max leverage is 30-60 days before renewal)

2. Always ask for:
   - Better pricing (10-20% off is standard ask)
   - Better terms (net-30 → net-45, annual billing discount)
   - Added value if they won't move on price (more seats, premium features, training)

3. The conversation:
   "Hi [vendor], we're doing our quarterly vendor review. We value the
    product, but we're under pressure to optimize our cost structure.
    Can we discuss adjusting our plan? We're at $X/mo — would $Y/mo
    work with an annual commitment?"

4. If they say no:
   "Understood. We may need to evaluate alternatives during our next
    budget cycle. Is there anything else you can offer — maybe
    additional seats or premium features at our current price?"

5. Always get it in writing: email confirmation or contract amendment.
```

#### Top Vendor by Category — Negotiation Targets

| Vendor Category | Typical Discount Achievable | Leverage Point |
|---|---|---|
| SaaS tools (< $5k/yr) | 10-20% | "We're consolidating vendors" |
| SaaS tools ($5k-50k/yr) | 15-30% | Annual commitment, competitive alternatives |
| SaaS tools (> $50k/yr) | 20-40% | Multi-year, logo value, formal RFP |
| Cloud (AWS/GCP/Azure) | 5-15% (committed use) | Reserved instances, committed spend discounts |
| Professional services (legal, accounting) | 10-30% | Fixed fee vs hourly, scope bundling |
| Recruiting agencies | 15 → 10% fee | Volume commitment |
| Insurance brokers | 10-20% | Annual re-quote, bundle policies |

## Output Format

- Spend diagnostic (spend by category, vendor, department)
- Quick-win list with estimated savings and timeline
- Vendor negotiation queue (ranked, with talking points)
- Structural improvement roadmap
- Savings tracker (projected vs actual)
- Recommendation for CEO: what to do, what NOT to cut

## Done Criteria

The skill is complete when:
1. A full spend diagnostic is completed (spend by category, vendor, and department, with % of total).
2. Quick wins are identified with estimated savings and implementation timeline.
3. Top 5-10 vendors are ranked for negotiation with talking points and target discounts.
4. Structural improvement opportunities are identified with effort vs impact ranking.
5. A clear CEO recommendation is provided on what to cut and what NOT to cut.
6. Savings tracker is set up to measure projected vs actual savings.

## Pitfalls

- **Cutting growth to save costs** — the #1 startup cost optimization error. Cutting S&M that works, reducing engineering capacity on a growing product, or trimming customer support when NPS is fragile destroys future revenue to save today's dollars.
- **Optimizing costs before you have clean data** — without a full spend diagnostic, you don't know where the money is going. Optimizing blind means you might cut the wrong things and miss the real savings.
- **One-time cost-cutting sprees without ongoing discipline** — the company cuts 20% in a crisis, then creeps back to the old spend level within 6 months. Cost optimization is a muscle, not a one-time event. Build the review cadence.
- **Killing the wrong SaaS tool** — canceling a $200/mo tool that three engineers depend on saves $2,400/yr but costs $50,000 in lost productivity. Before canceling anything, verify usage AND impact.
- **Negotiating from weakness** — starting vendor negotiations when you're desperate (e.g., "we need 30% off or we'll default") is the worst position. Always negotiate from a position of data and options, not desperation.

### Heuristics

- **Don't cut growth to save costs**: the #1 startup cost optimization error. Cutting S&M that works is self-defeating.
- **SaaS sprawl is the easiest win**: most startups have $5-20k/yr in unused/underused SaaS. A quarterly audit is worth it.
- **Renegotiate annually**: vendors expect it. If you haven't asked for a discount in 12 months, you're overpaying.
- **Cloud costs are the sneaky budget-killer**: they grow with usage and nobody watches them until the bill is shocking. Weekly monitoring.
- **Fixed fee > hourly**: for legal, accounting, and consulting — push for fixed-fee arrangements. Hourly billing incentivizes the wrong behavior.

### Edge Cases

- **Hypergrowth mode**: optimizing costs aggressively can slow growth. Be selective — cut waste, not investment.
- **Pre-product-market-fit**: don't optimize. Focus entirely on finding PMF. Cost optimization is for when the model is working.
- **Burning cash with strong unit economics**: it's okay to spend if LTV/CAC > 3x and payback < 12 months. The constraint is cash, not P&L.
- **Vendor dependency risk**: if you're deeply integrated with a vendor, price negotiation leverage is limited. Focus on multi-year price locks instead.

## Verification

Can you answer "Where is every dollar of OpEx going and which 20% of that spend is waste?" and "What are the top 3 things we should NOT cut?" and "Did we actually save what we projected from last quarter's optimization efforts?" If not, cost optimization is incomplete.

## Example

> **User**: "Find 10% savings in our OpEx without hurting growth."
> **Expected behavior**: You run a full spend diagnostic (categorize every vendor, identify unused subscriptions, benchmark cloud costs), identify quick wins (cancel 3 unused tools saving $2k/mo, downgrade over-provisioned plans saving $1.5k/mo, negotiate annual billing on 5 vendors saving $8k/yr), recommend structural improvements (consolidate 3 analytics tools into 1 saving $3k/mo, migrate dev instances to reserved instances saving $1k/mo), and clearly flag what NOT to cut (S&M spend driving 4x ROAS, customer success headcount).

> **User**: "We need to cut $100k/mo from our burn. It's a crisis situation."
> **Expected behavior**: You quickly assess the full cost structure, identify that headcount is 75% of total spend, present a tiered menu of options with human impact (Level 1: hiring freeze saves $15k/mo, Level 2: contractor cuts + marketing hold saves $30k/mo, Level 3: 15% workforce reduction saves $70k/mo), recommend the combination needed to reach $100k/mo, provide a severance and communication plan for the difficult choices, and flag that at $100k/mo savings, runway extends from 9 to 15 months creating a path to the next fundraise.

## Linked Skills

- Budget context → `budget-creation-management`
- Profitability to know what's worth keeping → `profitability-analysis`
- ROI case for bigger changes → `business-case-modeling`
