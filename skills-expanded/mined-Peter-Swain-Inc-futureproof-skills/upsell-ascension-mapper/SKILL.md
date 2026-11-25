---
name: upsell-ascension-mapper
description: |
  Maps a six-stage ascension ladder with leap-ratio pricing analysis, upgrade-
  trigger definition, friction diagnosis, and ranked bridge-offer recommendations
  to lift AOV and LTV. Use when the user says "map an upsell ladder for my
  offers", "design my ascension path", "fix the gap between my tiers", "increase
  customer LTV", or needs to find conversion cliffs in their product suite.
  Offer architecture and revenue sequencing — not P&L diagnosis or cash forecasting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="upsell-ascension-mapper")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any existing offer architecture, ICA segments, pricing data, or prior ascension mapping work.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Current offer portfolio**: List every product, service, tier, add-on, and one-time offer currently available — include price points, delivery format, and rough margin if known
- **ICA segments**: Which distinct ICA segments are being served? Are different segments entering at different price points?
- **Current ascension data**: What percentage of buyers at each tier upgrade? What is the average time-to-upgrade? Any known drop-off points?
- **Revenue objective**: Are they optimising for higher average order value (AOV), increased lifetime value (LTV), faster time-to-ascension, or portfolio gap-filling?
- **Constraints**: Fulfilment capacity limits, pricing sensitivity concerns, brand positioning guardrails

If the user cannot provide conversion data, flag this as a measurement gap and proceed with qualitative mapping — note the gap explicitly in the deliverable.

## Step 3: Audit the Current Ascension Architecture

Conduct a systematic audit of the existing offer portfolio against six ascension dimensions:

### 3a. Offer Sequencing Logic

Map every offer onto an **Ascension Ladder Matrix**:

| Stage | Offer | Price Point | ICA Segment | Entry Trigger | Exit Trigger (to next stage) |
|-------|-------|-------------|-------------|---------------|-------------------------------|
| 0 — Lead Magnet | | | | | |
| 1 — Tripwire / Entry | | | | | |
| 2 — Core Offer | | | | | |
| 3 — Premium / High-Touch | | | | | |
| 4 — Continuity / Retention | | | | | |
| 5 — Apex / Inner Circle | | | | | |

Identify any stages that are empty, have too many competing offers, or lack a clear transition mechanism.

### 3b. Price Architecture Analysis

Evaluate the pricing gaps between consecutive tiers:

- **Leap ratio**: Calculate the price multiple from one tier to the next (e.g., $47 → $497 = 10.6× leap). Flag any leap ratio exceeding 8× as a **conversion cliff** — a gap where an intermediate offer is likely needed
- **Value-to-price alignment**: Assess whether each tier's perceived value justifies the price increase, or whether there is a **value vacuum** (price rises faster than perceived value)
- **Anchoring effectiveness**: Determine whether higher tiers are positioned to make the core offer feel like a rational, anchored purchase

### 3c. Trigger Mapping

For each ascension point, identify the **upgrade trigger** — the specific moment, outcome, or signal that indicates a buyer is ready to ascend:

- **Outcome triggers**: Buyer achieves a specific result at the current tier (e.g., first 10 clients acquired)
- **Capacity triggers**: Buyer outgrows the current tier's scope (e.g., team size exceeds plan limits)
- **Engagement triggers**: Behavioural signals such as feature usage frequency, support ticket patterns, content consumption velocity
- **Temporal triggers**: Time-based prompts (e.g., 90-day renewal window, end-of-quarter budget cycle)

Flag any ascension point that lacks a defined, measurable trigger as an **orphan transition**.

### 3d. Friction and Leakage Analysis

Identify where buyers stall, churn, or exit the ascension path entirely:

- **Decision fatigue points**: Too many options at a single tier
- **Commitment anxiety gaps**: Large price jumps without adequate risk-reversal (guarantees, trials, step-up plans)
- **Fulfilment misalignment**: Points where the delivery experience deteriorates or changes format abruptly (e.g., self-serve to high-touch without onboarding)
- **ICA mismatch creep**: Stages where the offer begins serving a different ICA than the one who entered, causing relevance decay

### 3e. Cross-Sell and Lateral Expansion Opportunities

Beyond vertical ascension, assess lateral revenue pathways:

- **Complementary offers**: Adjacent problems the ICA faces that are not currently addressed
- **Format variants**: Same transformation delivered through a different modality (e.g., done-with-you vs. done-for-you)
- **Segment bridges**: Offers that allow one ICA segment to cross into another ascension path

### 3f. Competitive Ascension Benchmarking

Apply any FutureProof `instructions` or prior research to compare the user's ascension architecture against known category norms — standard tier structures, typical price multiples, and expected conversion rates at each stage.

## Step 4: Deliver Output

Produce the **Upsell Ascension Map** — a structured deliverable containing:

### Document 1: Ascension Ladder Visualisation

A completed tier-by-tier map showing:
- Every offer plotted by stage, price, and ICA segment
- Arrows indicating primary ascension paths and lateral cross-sell routes
- Colour-coded flags: 🔴 conversion cliffs, 🟡 orphan transitions, 🟢 healthy pathways

### Document 2: Gap and Opportunity Register

| # | Gap Type | Location | Severity (1–5) | Recommended Action | Expected Revenue Impact |
|---|----------|----------|-----------------|-------------------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

Prioritise by a composite score of severity × estimated revenue impact × implementation ease.

### Document 3: Ascension Scorecard

Rate the current architecture 1–10 on each dimension:

- **Stage completeness** — all six stages populated with clear offers
- **Price architecture coherence** — leap ratios within healthy range (2×–6×), proper anchoring
- **Trigger definition** — every ascension point has a measurable, observable trigger
- **Friction minimisation** — risk-reversal, onboarding, and transition mechanisms in place
- **Lateral depth** — cross-sell and format variant opportunities exploited
- **ICA continuity** — consistent relevance and messaging alignment across the full path

### Document 4: Priority Recommendations

The top 3 highest-impact interventions, each containing:

- **Specific action**: What to build, change, or reposition (e.g., "Insert a $197/month group coaching tier between the $47 course and $2,500 private engagement")
- **Rationale**: Which gap or friction point this resolves, with reference to the audit findings
- **Implementation brief**: Pricing, positioning copy, upgrade trigger, and fulfilment requirements
- **Projected impact**: Estimated effect on AOV, LTV, or ascension rate — expressed as a range with assumptions stated

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
FutureProof:save_experiment(skill="upsell-ascension-mapper", experiment={
  hypothesis: "Introducing a bridge offer at the identified conversion cliff between [Tier X] and [Tier Y] will reduce buyer stall-out and increase ascension rate",
  variants: ["control: current direct jump from Tier X to Tier Y", "variant: new intermediate offer at [price point] with [trigger mechanism]"],
  measurement: "Ascension rate from Tier X to Tier Y+ measured over 90 days, segmented by ICA cohort",
  expected_impact: "20–35% increase in Tier X buyers reaching Tier Y within 6 months, contributing estimated [dollar amount] incremental annual revenue"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="upsell-ascension-mapper",
  query="Current best practices in SaaS and service-business upsell sequencing, optimal price tier ratios, and behavioural triggers for upgrade conversion — 2024 benchmarks from ProfitWell, Paddle, and subscription economy reports",
  reason="Ensure ascension architecture recommendations reflect current buyer behaviour norms and validated pricing psychology rather than legacy frameworks"
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
FutureProof:save_session(skill="upsell-ascension-mapper", session={
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