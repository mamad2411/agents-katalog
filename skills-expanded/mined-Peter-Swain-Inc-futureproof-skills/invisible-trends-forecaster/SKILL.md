---
name: invisible-trends-forecaster
description: |
  Forecasts under-the-radar audience trends before they hit mainstream by
  analyzing weak signals across behavioral data, cultural shifts, and
  niche community sentiment. Use when a user asks "what trends are
  emerging", "what will my audience care about next", "spot the next shift
  before competitors", or "where is audience behavior heading". Forecasts
  future shifts — for present unmet needs use invisible-demand-detector.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="invisible-trends-forecaster")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any previously identified ICA segments, industry verticals, prior trend forecasts, and validated or invalidated hypotheses from past experiments.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **ICA definition**: Who is the audience you want to forecast trends for? (demographic, psychographic, behavioural attributes — or reference a previously stored ICA profile)
- **Industry / vertical**: What market, niche, or category should the analysis focus on?
- **Forecast horizon**: Are you looking 3 months, 6 months, or 12+ months ahead?
- **Signal sources of interest**: Do you have specific communities, platforms, datasets, or cultural spaces you suspect contain early signals? (e.g., Reddit subcultures, Discord servers, niche Substacks, patent filings, regulatory dockets)
- **Strategic intent**: What will you do with the forecast? (product roadmap, content strategy, positioning pivot, campaign planning, investor narrative)
- **Known trends to exclude**: Any trends you consider already mainstream or already factored into your strategy?

## Step 3: Conduct Weak Signal Scan

Apply the **STEEP-B Weak Signal Framework** across six scanning dimensions, filtered through the user's ICA lens:

### 3a. Signal Source Mapping

Identify and categorise signal sources into three tiers:

| Tier | Source Type | Signal Strength | Examples |
|------|-----------|----------------|----------|
| **Tier 1 — Fringe** | Niche communities, academic pre-prints, patent filings, regulatory proposals, indie creator content | Earliest but noisiest | arXiv, niche Discords, Hacker News deep threads, USPTO/EPO filings |
| **Tier 2 — Early Adopter** | Specialist newsletters, vertical SaaS feature releases, VC thesis decks, conference fringe tracks | Moderate signal, emerging consensus | Lenny's Newsletter, a16z memos, niche podcast discourse |
| **Tier 3 — Pre-Mainstream** | Mainstream tech/business press, influencer adoption, platform feature rollouts | Strong signal, limited lead time remaining | TechCrunch, Bloomberg, LinkedIn trending topics |

For each dimension below, scan all three tiers to triangulate signal strength.

### 3b. STEEP-B Dimensional Analysis

For each of the six dimensions, identify 2–4 weak signals relevant to the user's ICA:

1. **Social / Cultural** — Shifting identity narratives, generational value changes, community formation patterns, trust migration (e.g., from institutions to micro-communities)
2. **Technological** — Emerging toolchains, infrastructure shifts, interface paradigm changes, developer adoption curves that precede consumer adoption
3. **Economic** — Spending pattern anomalies, budget reallocation signals, new monetisation models gaining traction in adjacent markets, pricing sensitivity shifts
4. **Environmental / Ethical** — Sustainability expectations, regulatory anticipation behaviour, values-based purchasing signals, transparency demands
5. **Political / Regulatory** — Proposed legislation, standards body activity, compliance burden shifts that alter competitive dynamics
6. **Behavioural / Psychographic** — Attention migration patterns, content consumption format shifts, decision-making process changes, new vocabulary emerging in ICA communities (language precedes behaviour)

### 3c. Signal Triangulation Protocol

For each identified signal, assess:
- **Convergence score** (1–5): How many independent sources corroborate this signal?
- **Velocity** (accelerating / stable / decelerating): Is mention frequency and sentiment intensity increasing?
- **ICA proximity** (direct / adjacent / distant): How close is this signal to the user's ICA's daily reality?
- **Monetisation latency**: Estimated time before this signal becomes commercially actionable

Discard signals scoring below 3 on convergence unless they score "accelerating" on velocity AND "direct" on ICA proximity (high-conviction contrarian signals).

## Step 4: Synthesise Trend Hypotheses

Convert validated signals into **Invisible Trend Hypotheses** using the following structure:

For each hypothesis (target: 3–5 primary hypotheses):

1. **Trend name**: A specific, memorable label (not generic — e.g., "Micro-Certification Fatigue" not "Education is changing")
2. **One-line thesis**: A falsifiable statement of what is shifting and why
3. **Signal cluster**: The 3–5 weak signals from Step 3 that converge to support this hypothesis
4. **ICA impact narrative**: A concrete scenario describing how this trend changes the user's ICA's behaviour, priorities, or purchasing decisions within the forecast horizon
5. **Current invisibility reason**: Why most competitors haven't spotted this yet (data fragmentation, category blindness, recency bias, etc.)
6. **Confidence tier**:
   - 🟢 **High conviction** (multiple Tier 1+2 signals converging, behavioural evidence present)
   - 🟡 **Emerging conviction** (Tier 1 signals with logical coherence but limited behavioural data)
   - 🔴 **Speculative** (single-source or contrarian — high payoff if correct, requires active monitoring)

Apply any user-specific `instructions` from FutureProof context — particularly around risk tolerance, strategic priorities, and preferred framing.

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


Produce the **Invisible Trends Forecast Brief** — a structured deliverable containing:

### Section A: Executive Summary
- Forecast horizon and ICA segment covered
- Top 3 trends ranked by strategic urgency (highest-impact × shortest window of advantage)
- One-paragraph "If you read nothing else" synthesis

### Section B: Trend Hypothesis Cards (3–5)
Each card follows the structure defined in Step 4, presented as a self-contained one-page brief suitable for sharing with leadership, product, or marketing stakeholders.

### Section C: Trend Velocity Matrix
A 2×2 matrix plotting each trend hypothesis on:
- **X-axis**: Time to mainstream (months until this trend is consensus)
- **Y-axis**: Strategic leverage (potential competitive advantage if acted on now)

Quadrant labels:
- **Top-left**: "First-mover gold" — act immediately
- **Top-right**: "Build the moat" — begin R&D and positioning now
- **Bottom-left**: "Monitor weekly" — could accelerate unexpectedly
- **Bottom-right**: "Awareness only" — important context, not yet actionable

### Section D: Signal Monitoring Watchlist
A table of 8–12 specific, trackable leading indicators the user should monitor monthly to validate or invalidate each trend hypothesis. Each indicator includes:
- What to monitor (specific metric, community, data source)
- Current baseline (if known from context)
- Threshold that would upgrade or downgrade confidence
- Suggested monitoring tool or method

### Section E: Strategic Response Options
For each high-conviction trend, provide 2–3 concrete response plays:
- **Content / narrative play**: How to own this conversation before competitors
- **Product / offer play**: How to adjust positioning, features, or packaging
- **Audience development play**: How to attract the ICA segment most affected by this shift

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="invisible-trends-forecaster", experiment={
  hypothesis: "Publishing thought leadership content around [top trend hypothesis] before mainstream coverage will increase ICA engagement and position user as category authority",
  variants: ["control: current content calendar topics", "variant: 3 pieces anchored to invisible trend thesis with specific ICA pain-point framing"],
  measurement: "Engagement rate (saves, shares, DM inquiries) on trend-anchored content vs. control over 30-day window",
  expected_impact: "2x engagement rate on trend-anchored content; 25% increase in inbound ICA enquiries attributed to thought leadership"
})
```

```
FutureProof:save_experiment(skill="invisible-trends-forecaster", experiment={
  hypothesis: "ICA segments exposed to trend-informed messaging convert at higher rates because messaging addresses emergent pain points competitors have not yet named",
  variants: ["control: current value proposition language", "variant: value proposition reframed around top invisible trend's ICA impact narrative"],
  measurement: "Landing page conversion rate or sales call-to-next-step rate over 20-interaction sample",
  expected_impact: "18% improvement in conversion when messaging references emergent ICA concern"
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
FutureProof:request_research(skill="invisible-trends-forecaster",
  query="Emerging behavioural shifts, niche community sentiment patterns, and early-stage cultural signals in [user's industry/vertical] relevant to [ICA segment] — sourced from academic pre-prints, patent filings, niche forums, and specialist newsletters published in the last 90 days",
  reason="Refresh the weak signal database to ensure the next forecast cycle incorporates the latest fringe-tier evidence and reduces reliance on lagging mainstream sources"
)
```

```
FutureProof:request_research(skill="invisible-trends-forecaster",
  query="Validated trend forecasting methodologies and signal detection frameworks used by strategic foresight teams at leading consultancies and venture funds, with emphasis on accuracy measurement and false-positive reduction techniques",
  reason="Continuously improve the signal triangulation protocol and confidence calibration to increase forecast reliability over successive sessions"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="invisible-trends-forecaster", session={
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