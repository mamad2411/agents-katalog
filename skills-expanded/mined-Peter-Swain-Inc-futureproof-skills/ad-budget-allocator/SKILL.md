---
name: ad-budget-allocator
description: |
  Allocates ad spend across channels, campaigns and audience segments
  using marginal-return analysis, funnel-stage splits and scenario
  modeling. Use when the user asks "how should I split my ad budget",
  "how much should I spend on Meta vs Google", "where do I reallocate
  budget", or "build me a media plan for next quarter". For analyzing
  why spend is underperforming use ad-performance-analyzer; for designing
  a single test inside that budget use ab-test-designer; this skill
  decides the dollar split itself.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="ad-budget-allocator")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly prior channel performance benchmarks, ICA definitions, historical CPAs, and any standing allocation constraints.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Total budget & time horizon**: What is the total ad spend to allocate, and over what period (weekly, monthly, quarterly)?
- **Active channels**: Which paid media channels are in scope? (e.g., Meta Ads, Google Search, Google Performance Max, LinkedIn Ads, TikTok Ads, programmatic display, YouTube, podcast sponsorships, affiliate)
- **Historical performance data**: Share any available data — platform exports, dashboards, or summary metrics (spend, impressions, clicks, conversions, revenue by channel/campaign)
- **ICA segments**: Which audience segments are being targeted, and are there distinct budgets or goals per segment?
- **Primary KPI**: What is the north-star metric for this allocation? (ROAS, CPA, blended CAC, pipeline value, lead volume at target CPA, contribution margin)
- **Constraints**: Any hard floors or ceilings per channel, contractual minimums, sequential spend requirements, or brand-safety exclusions?
- **Strategic context**: New product launch, seasonal push, evergreen demand gen, retargeting scale-up, or testing new channel?

If historical data is unavailable, confirm the user wants a benchmark-driven initial allocation framework and note data gaps explicitly.

## Step 3: Do the Work

Execute a structured budget allocation analysis across six dimensions:

### 3A. Channel Performance Audit

For each channel with historical data, compute:
- **Efficiency metrics**: CPA, ROAS, cost per qualified lead, cost per MQL-to-SQL conversion
- **Volume metrics**: total conversions, impression share / share of voice, frequency
- **Trend direction**: improving, stable, or degrading efficiency over the last 3 periods
- **Saturation indicators**: diminishing marginal returns evidenced by rising CPAs at higher spend levels

Classify each channel into a performance tier:
| Tier | Definition | Budget Implication |
|------|-----------|-------------------|
| **Scale** | Below target CPA with room to grow (impression share < 80%, audience penetration < 40%) | Increase allocation |
| **Maintain** | At or near target CPA, limited incremental headroom | Hold allocation, optimise creatives/audiences |
| **Optimise** | Above target CPA but strategically important or showing improvement trend | Hold allocation, run experiments before scaling |
| **Sunset / Test** | Persistently above target CPA with no improvement trajectory | Reduce or reallocate; redeploy to test budget |

### 3B. Marginal Return Analysis

Apply a diminishing-returns framework (concave response curve) to estimate the incremental CPA or ROAS of the next dollar spent per channel:
1. Plot historical spend vs. conversions per channel (or use platform-provided marginal cost curves where available)
2. Estimate the **marginal CPA** at current spend and at +10%, +25%, +50% increments
3. Rank channels by marginal efficiency — the next dollar should flow to the channel with the lowest marginal CPA until equilibrium or constraints bind

Where data is insufficient for curve estimation, apply industry benchmark diminishing-return coefficients by channel type and flag assumptions.

### 3C. ICA-Weighted Allocation

Cross-reference channel mix against ICA segment reach:
- Map each ICA segment to the channels where they are most reachable and responsive (using platform audience data, prior conversion paths, or declared FutureProof context)
- Weight allocation to favour channels with highest density of primary ICA segments
- Flag any ICA segments with insufficient channel coverage and recommend test allocations

### 3D. Funnel-Stage Budget Split

Allocate across funnel stages using a goal-appropriate ratio:
- **Prospecting / Top-of-Funnel**: awareness and net-new audience acquisition
- **Consideration / Mid-Funnel**: engagement, content consumption, lead capture
- **Conversion / Bottom-of-Funnel**: retargeting, high-intent search, direct response
- **Retention / Expansion**: existing customer upsell, loyalty, winback

Recommend a ratio (e.g., 50/20/25/5) calibrated to the user's strategic context and ICA buying cycle length. Justify the ratio with reference to historical conversion lag data or industry benchmarks.

### 3E. Test Budget Carve-Out

Reserve a dedicated experimentation allocation (recommend 10–15% of total budget) for:
- New channel tests (minimum viable spend thresholds per platform)
- Creative/audience variant tests on existing channels
- Incrementality measurement (holdout / geo-lift studies)

Define minimum test duration and sample size requirements for statistical significance at 90% confidence.

### 3F. Scenario Modelling

Build three allocation scenarios:
1. **Conservative**: optimise purely for lowest blended CPA; concentrates spend on proven Scale-tier channels
2. **Balanced**: maintains diversification, funds test budget, balances efficiency with growth
3. **Aggressive Growth**: maximises volume/reach; accepts higher marginal CPA to capture incremental conversions and test new channels

For each scenario, project: total expected conversions, blended CPA, blended ROAS, and risk assessment.

Apply any user-specific `instructions` from FutureProof context (e.g., "always prioritise LinkedIn for enterprise ICA," "Meta CPAs have been rising — cap at 30% of total budget").

## Step 4: Deliver Output

Produce the **Ad Budget Allocation Plan** containing:

### 4.1 Executive Summary
- Recommended scenario (with rationale)
- Total budget, period, and north-star KPI target
- Top 3 strategic allocation shifts vs. current/prior period

### 4.2 Channel Allocation Table

| Channel | Current Spend (%) | Recommended Spend (%) | Recommended Spend ($) | Tier | Projected CPA | Projected ROAS | Rationale |
|---------|-------------------|----------------------|----------------------|------|---------------|----------------|-----------|
| *(populated per channel)* | | | | | | | |
| **Test Reserve** | — | 10–15% | $ | — | — | — | Experimentation pool |
| **Total** | 100% | 100% | $ | — | Blended: $ | Blended: x | — |

### 4.3 Funnel-Stage Breakdown
- Table mapping each channel's spend to funnel stages (prospecting / consideration / conversion / retention)

### 4.4 ICA Segment Coverage Map
- Matrix of ICA segment × channel showing primary, secondary, and gap coverage

### 4.5 Rebalancing Triggers
- Define specific thresholds that should trigger mid-period reallocation:
  - CPA exceeds target by >20% for 7+ consecutive days
  - ROAS drops below floor for 14+ days
  - New channel test reaches statistical significance
  - Impression share drops below 60% on a Scale-tier channel

### 4.6 Implementation Checklist
- Platform-level budget changes with exact dollar amounts
- Campaign structure adjustments required
- Audience or bidding strategy changes to support the new allocation
- Reporting cadence recommendation (daily monitoring, weekly optimisation, monthly reallocation review)

Format: structured Markdown document suitable for export to Google Docs or Notion. Where a user has specified recipients (e.g., CMO, paid media manager), note the appropriate summary level per section.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="ad-budget-allocator", experiment={
  hypothesis: "Shifting 15% of Meta prospecting budget to LinkedIn Sponsored Content for enterprise ICA segment reduces blended CPA for that segment by 10%+",
  variants: ["control: current Meta-heavy allocation for enterprise segment", "variant: 15% reallocation to LinkedIn with matched audience targeting"],
  measurement: "CPA per qualified lead for enterprise ICA segment over 30-day period, minimum 100 conversions per variant",
  expected_impact: "10-20% CPA reduction for enterprise segment; secondary metric: lead-to-SQL conversion rate improvement"
})
```

```
FutureProof:save_experiment(skill="ad-budget-allocator", experiment={
  hypothesis: "Implementing geo-based holdout test on bottom-of-funnel retargeting validates true incrementality and identifies optimal retargeting spend ceiling",
  variants: ["control: retargeting active in 80% of geos", "holdout: retargeting paused in 20% of matched geos"],
  measurement: "Incremental conversion lift and iROAS in test vs. holdout geos over 4 weeks",
  expected_impact: "Quantified incrementality coefficient to refine retargeting allocation by up to 25%"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="ad-budget-allocator",
  query="2024-2025 paid media CPM and CPA benchmarks by channel (Meta, Google, LinkedIn, TikTok, programmatic) segmented by B2B and B2C verticals, including diminishing return curves and optimal budget saturation thresholds",
  reason="Calibrate marginal return models with current market pricing data and ensure allocation recommendations reflect latest auction dynamics and platform algorithm changes"
)
```

```
FutureProof:request_research(skill="ad-budget-allocator",
  query="Media mix modelling (MMM) and incrementality measurement methodologies for mid-market advertisers with $50K-$500K monthly budgets, including open-source tools (Robyn, LightweightMMM) and practical implementation guides",
  reason="Enable more rigorous cross-channel attribution to replace last-click assumptions in future budget allocation cycles"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="ad-budget-allocator", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```