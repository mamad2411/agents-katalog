---
name: market-gap-finder
description: >-
  Research any industry or market to find underserved niches, unmet customer
  needs, and untapped opportunities. Analyzes competitor blind spots, customer
  complaints, emerging trends, and geographic gaps to surface specific business
  opportunities most people miss. No API keys or paid tools required — works
  with web search alone. Use when asked to find a niche, discover market gaps,
  identify business opportunities, find underserved markets, spot trends, or
  research where demand exceeds supply.
license: MIT
metadata:
  author: mloki23
  version: "1.0"
  category: business
---

# Market Gap Finder

Discover underserved niches and untapped opportunities in any market using structured research. Surfaces specific, actionable gaps — not generic advice.

## When to Use This Skill

- "Find me a niche in [industry]"
- "What gaps exist in [market]?"
- "Where's the opportunity in [sector]?"
- "Find underserved customers in [industry]"
- "What's missing in the [product/service] market?"
- "I want to start a business but don't know what niche"
- "What trends are creating new opportunities?"
- "Find me a market gap I can fill"

## Inputs

Ask the user for (if not already provided):

1. **Industry or market** — what space to research (e.g. "fitness," "home services," "SaaS for restaurants")
2. **Location** — geographic focus, or "global/online" (optional — defaults to global)
3. **Constraints** — budget, skills, time, or other limitations that narrow what's realistic (optional)

If the user says something vague like "find me a business idea," ask them for at least a broad category of interest before proceeding.

## Research Process

Cap total research at 15-20 searches across all phases. After gathering solid data, STOP researching and compile findings.

### Phase 1: Industry Landscape (3-5 searches)

Establish the current state of the market:
- Who are the major players and what do they focus on?
- How big is the market and is it growing?
- What's the standard business model?
- What customer segments exist?

Search: `[industry] market overview [year]`, `[industry] major companies`, `[industry] customer segments`

### Phase 2: Pain Point Mining (4-6 searches)

Find what customers hate about existing options. This is where gaps hide.

#### 2a. Customer Complaints
Search for what people complain about in this industry. Forums, review sites, and social media are gold mines.

Search: `[industry] complaints reddit`, `[industry] frustrations customers`, `[top competitor] negative reviews`, `[industry] "I wish" OR "why can't" OR "nobody offers"`

#### 2b. Underserved Segments
Look for customer groups that existing players ignore or serve poorly.

Search: `[industry] underserved market`, `[industry] niche opportunities`, `[industry] small business OR rural OR elderly OR [demographic] gap`

#### 2c. Pricing Gaps
Find price points where no good option exists — too expensive for budget buyers or too cheap/basic for premium buyers.

Search: `[industry] affordable alternative`, `[industry] premium luxury`, `[industry] pricing complaints`

### Phase 3: Trend & Disruption Scanning (3-4 searches)

Identify forces creating new gaps:

#### 3a. Emerging Trends
What new technologies, regulations, demographics, or cultural shifts are reshaping this market?

Search: `[industry] trends [year]`, `[industry] emerging technology disruption`, `[industry] new regulations impact`

#### 3b. Adjacent Market Spillover
What's happening in related industries that could create crossover opportunities?

Search: `[industry] adjacent markets`, `[related industry] impact on [industry]`

### Phase 4: Geographic & Channel Gaps (2-3 searches)

#### 4a. Location Gaps
Are there geographic areas where demand exists but supply doesn't?

Search: `[industry] [location] gap`, `[industry] rural OR regional underserved`

#### 4b. Channel Gaps
Are there distribution channels nobody is using? (e.g. mobile-first, subscription, marketplace, B2B when everyone is B2C)

Search: `[industry] online OR mobile OR subscription model`, `[industry] B2B opportunity`

### Phase 5: Validation Signals

For each gap identified, check for validation:
- **Demand signals:** Are people searching for this? Are there forum posts asking for it?
- **Willingness to pay:** Would people pay for a solution? Is there evidence of spending in adjacent areas?
- **Feasibility:** Can this gap actually be filled? What would it take?

## Gap Scoring

Score each identified gap on these dimensions (1-10):

1. **Demand Evidence (1-10):** How strong is the evidence that people want this? 1 = speculation. 10 = people are actively searching/asking for it with money in hand.

2. **Competition Vacuum (1-10):** How empty is the space? 1 = well-served by existing players. 10 = literally nobody is doing this.

3. **Revenue Potential (1-10):** How much money is here? 1 = tiny niche with minimal spend. 10 = large market with high willingness to pay.

4. **Accessibility (1-10):** How easy is it to enter? 1 = requires massive capital, rare expertise, or regulatory approval. 10 = anyone with basic skills could start.

5. **Timing (1-10):** Is the window open now? 1 = too early (market not ready) or too late (already filling). 10 = perfect timing — demand is emerging and supply hasn't caught up.

**Gap Score** = average of all five dimensions.

## Output Format

```
# Market Gap Analysis
## [Industry/Market]
### Researched: [Date]

---

## Industry Overview
[2-3 paragraphs on the current state of the market — size, major players, standard business models, customer segments]

---

## Gaps Identified

### Gap #1: [Clear, Specific Gap Name]
**The opportunity:** [What's missing and why it matters — 2-3 sentences]
**Evidence:** [Specific data points, complaints, search trends, or forum posts that prove this gap exists]
**Who it serves:** [The specific customer segment that's underserved]
**Why nobody's doing it:** [Why existing players have missed or ignored this]
**What it would take:** [Resources, skills, and investment needed to fill this gap]
**Example business model:** [A specific, concrete way to monetise this gap]

| Dimension | Score |
|-----------|-------|
| Demand Evidence | X/10 |
| Competition Vacuum | X/10 |
| Revenue Potential | X/10 |
| Accessibility | X/10 |
| Timing | X/10 |
| **Gap Score** | **X.X/10** |

[Repeat for each gap — aim for 4-6 gaps total]

---

## Gap Ranking

| Rank | Gap | Score | Best For |
|------|-----|-------|----------|
| 1 | [Gap name] | X.X/10 | [Type of entrepreneur this suits] |
| 2 | [Gap name] | X.X/10 | [Type of entrepreneur this suits] |
| 3 | [Gap name] | X.X/10 | [Type of entrepreneur this suits] |

---

## The #1 Opportunity

[2-3 paragraphs on the top-ranked gap — why it's the strongest, what the first-mover play looks like, and what you'd do in the first 30 days to test it]

---

## Trends Reshaping This Market

[Brief section on 2-3 macro trends creating new gaps — technology shifts, regulatory changes, demographic shifts, cultural changes. Each trend should connect to specific opportunities.]

---

## Sources
[List key sources referenced during research]
```

## Important Guidelines

- **Specificity is everything.** "There's a gap in customer service" is useless. "No mobile mechanic in Australia offers EV-specific servicing despite 200% growth in EV registrations" is actionable. Every gap should be specific enough that someone could start building a business around it tomorrow.
- **Evidence over opinion.** Every gap must be backed by at least one concrete data point — a customer complaint, a search trend, a forum post, a missing competitor, a pricing analysis. No "I think there might be an opportunity."
- **Aim for 4-6 gaps.** Fewer than 4 means you didn't dig deep enough. More than 8 means you're listing everything rather than curating the strongest opportunities.
- **Research thoroughly but don't loop.** Cap at 15-20 total searches. Once you have solid data, STOP and compile. A good analysis now beats a perfect one never.
- **Compile promptly.** After completing research, immediately write the analysis. Do not run additional searches.
- **Review before saving.** Scan for formatting artifacts or broken tables. Fix before saving.
- **Save the analysis.** If the agent supports file output, save as a markdown file the user can keep.
- **Connect gaps to action.** Every gap should include a concrete "what it would take" and "example business model" so the user can immediately evaluate whether it's for them.
