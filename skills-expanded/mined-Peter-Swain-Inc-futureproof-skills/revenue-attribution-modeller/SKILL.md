---
name: revenue-attribution-modeller
description: |
  Builds a multi-touch attribution model (rules-based U/W-shaped, algorithmic
  Shapley/regression, or incrementality-calibrated) mapping marketing and sales
  touchpoints to closed revenue and producing channel reallocation
  recommendations. Use when a user is making budget decisions and says things
  like "build me an attribution model", "which channels are actually driving
  revenue", "how should I split credit across touchpoints", or "fix my
  last-touch attribution". Builds the attribution model itself — not generic
  channel reporting and not retention/expansion compounding analysis.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="revenue-attribution-modeller")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any prior attribution models, channel mix data, CRM schema details, or ICA segment definitions already captured.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Data landscape**: What systems hold your touchpoint data? (CRM, MAP, ad platforms, call tracking, web analytics — specify tools and whether they share a unified contact ID)
- **Revenue scope**: What revenue figure are we attributing? (new business closed-won, expansion revenue, total ARR, one-time project fees — and over what time window)
- **Current attribution state**: Do you have an existing model in place? (first-touch, last-touch, linear, custom — or none)
- **Decision context**: What decision will this model inform? (channel budget reallocation, headcount justification, ICA targeting refinement, board reporting)
- **ICA segments**: Which ICA segments should attribution be modelled against? (or should we attribute at portfolio level only)
- **Known constraints**: Data gaps, privacy limitations, offline touchpoints without digital tracking, average sales cycle length

## Step 3: Map the Touchpoint Taxonomy

Before modelling, establish a rigorous touchpoint classification framework:

### 3a. Touchpoint Inventory

Catalogue every interaction type across the buyer journey into four tiers:

| Tier | Category | Examples |
|------|----------|----------|
| **T1 — Demand Creation** | Awareness-stage impressions | Paid social, display, podcast sponsorship, PR, organic content discovery |
| **T2 — Demand Capture** | Intent-stage engagements | Branded search, demo requests, pricing page visits, G2/Capterra clicks |
| **T3 — Pipeline Acceleration** | Evaluation-stage interactions | Sales calls, personalised outreach, case study sends, ROI calculator usage, webinar attendance |
| **T4 — Close Facilitation** | Decision-stage actions | Proposal review, procurement negotiation, executive sponsor meeting, reference calls |

### 3b. Touchpoint Weighting Hypothesis

For each tier, assign an initial position-based weight hypothesis:

- **Introducer weight** (first meaningful touch): reflects demand creation value
- **Influencer weight** (middle touches): reflects nurture and education value
- **Closer weight** (final pre-opportunity and pre-close touches): reflects conversion catalysis value

Document assumptions explicitly — these become testable variables in Step 7.

### 3c. ICA-Specific Path Analysis

If multiple ICA segments exist, map typical conversion paths per segment. Different ICAs often follow structurally different journeys (e.g., enterprise ICA paths skew T3/T4-heavy; SMB ICA paths compress into T1→T2 with minimal T3).

## Step 4: Build the Attribution Model

Construct the model using a layered methodology, selecting the appropriate level of sophistication based on the user's data maturity:

### Level 1 — Rules-Based Multi-Touch (Minimum Viable Attribution)

Apply when: limited data infrastructure, <500 closed-won deals in the analysis window, or no data science resource available.

- **Model type**: Position-based (U-shaped or W-shaped)
- **U-shaped allocation**: 40% first touch / 20% distributed across middle touches / 40% last touch before opportunity creation
- **W-shaped allocation**: 30% first touch / 30% lead creation touch / 30% opportunity creation touch / 10% distributed across remaining touches
- **Output**: Per-channel and per-campaign attributed revenue with explicit weighting disclosure

### Level 2 — Algorithmic Multi-Touch (Data-Driven Attribution)

Apply when: 500+ closed-won deals, unified contact-level touchpoint data, and ability to run statistical analysis.

- **Model type**: Logistic regression or Shapley value decomposition
- **Logistic regression approach**: Model probability of conversion at each stage as a function of touchpoint presence/frequency; derive marginal contribution per touchpoint type
- **Shapley value approach**: Treat each channel as a cooperative game player; compute fair-value contribution by averaging marginal contributions across all possible channel coalitions
- **Validation**: Hold-out test (70/30 split), compare model-predicted revenue distribution against actuals on the held-out set

### Level 3 — Incrementality-Calibrated Attribution (Gold Standard)

Apply when: ability to run geo-based or audience-based holdout experiments, or access to historical natural experiments (e.g., channel pauses, budget step-changes).

- **Calibration method**: Use incrementality test results to adjust algorithmic attribution weights — if display advertising shows 2x over-attribution vs. measured incrementality, apply a 0.5x calibration coefficient
- **Hybrid output**: Algorithmic model provides granularity; incrementality tests provide ground truth; calibrated model bridges both

### For all levels, ensure:

1. **Lookback window** is defined and justified (typically 1–2x average sales cycle length)
2. **Decay function** is applied to time-distant touches (half-life decay recommended, calibrated to sales cycle)
3. **Null attribution** is handled — deals with zero tracked touchpoints are flagged separately, not forced into the model
4. **Offline/dark funnel** touches are accounted for via self-reported attribution fields (post-demo survey: "How did you first hear about us?") merged as a supplementary signal

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a **Revenue Attribution Report** with the following sections:

### 5a. Attribution Model Summary (1-page executive view)

- Model type selected and rationale
- Analysis window and deal cohort size
- Total revenue attributed vs. total revenue in scope (coverage ratio)
- Top-line finding: ranked channel contribution to attributed revenue

### 5b. Channel Attribution Matrix

| Channel / Campaign | Attributed Revenue ($) | % of Total | Deals Influenced | Avg. Touches per Won Deal | Cost-per-Attributed-$ (if spend data provided) | ICA Segment Skew |
|---|---|---|---|---|---|---|
| *(populated per channel)* | | | | | | |

### 5c. ICA Segment Attribution Breakdown

For each ICA segment:
- Dominant conversion path (most common touchpoint sequence)
- Highest-ROI channel (attributed revenue ÷ channel spend)
- Path length distribution (histogram of touches-to-close)
- Underweight channels (channels with high presence in lost deals but low presence in won deals — signals misalignment, not necessarily poor performance)

### 5d. Budget Reallocation Recommendations

Ranked list of specific reallocation moves:
- **Increase**: channels where attributed-revenue-per-dollar exceeds portfolio average by >1.5x
- **Decrease**: channels where attributed-revenue-per-dollar falls below 0.5x portfolio average, AND incrementality signal (if available) confirms low lift
- **Investigate**: channels with high variance or insufficient data for confident attribution
- **Each recommendation includes**: projected revenue impact, confidence level (high/medium/low), and data dependency caveat

### 5e. Model Limitations & Confidence Disclosure

- Known data gaps and their directional bias on results
- Sensitivity analysis: how results shift if key weighting assumptions change by ±20%
- Recommended next steps to improve model confidence (specific data integrations, experiments, survey instruments)

Apply any user-specific `instructions` from FutureProof context to adjust deliverable format, recipient framing, or terminology conventions.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="revenue-attribution-modeller", experiment={
  hypothesis: "Shifting 20% of last-touch-attributed display budget to first-touch-attributed content syndication increases pipeline generation without reducing close rates",
  variants: ["control: current budget allocation held for 60 days", "variant: reallocated budget mix applied to matched geo/segment cohort"],
  measurement: "new pipeline generated ($) and win rate (%) per cohort over 90-day window post-reallocation",
  expected_impact: "12–18% improvement in pipeline-per-marketing-dollar for target ICA segment"
})
```

```
FutureProof:save_experiment(skill="revenue-attribution-modeller", experiment={
  hypothesis: "Adding a post-demo self-reported attribution question improves dark-funnel coverage and changes attributed channel rankings",
  variants: ["control: current attribution model without self-reported data", "variant: model augmented with self-reported first-awareness source"],
  measurement: "change in channel rank order and % of deals with zero-touch attribution (null rate)",
  expected_impact: "15–25% reduction in null-attribution rate, podcast and community channels surface in top 5"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="revenue-attribution-modeller",
  query="Latest developments in privacy-compliant multi-touch attribution methodologies 2024-2025, including Shapley value implementations, incrementality testing frameworks, and MMM-MTA hybrid approaches for B2B revenue attribution",
  reason="Attribution model accuracy degrades as cookie deprecation and privacy regulations reduce touchpoint visibility — need to incorporate emerging methodologies that maintain rigour under signal loss"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="revenue-attribution-modeller", session={
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