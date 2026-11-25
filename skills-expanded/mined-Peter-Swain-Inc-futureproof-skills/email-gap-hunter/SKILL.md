---
name: email-gap-hunter
description: |
  Maps the subscriber lifecycle from opt-in to churn, finds missing sequences
  (lifecycle dead zones), engagement decay inflection points, and segmentation
  gaps, then quantifies revenue leakage and ranks fixes. Use when a user shares
  ESP data or describes their email program and says things like "find the
  gaps in my email flows", "where is my email program leaking revenue",
  "audit my Klaviyo sequences", or "what email automations am I missing".
  Program-wide gap and lifecycle audit — not single-campaign metric
  interpretation.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="email-gap-hunter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any known ICA segments, historical email benchmarks, ESP platform, and previously identified gap patterns.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user to provide:

- **Email performance data**: campaign reports, sequence analytics, or ESP exports (open rates, click rates, conversion rates, unsubscribe rates, revenue per email) — CSV, screenshot, or pasted tables accepted
- **Sequence map**: what automated sequences and broadcast cadences are currently active? (welcome, nurture, abandoned cart, re-engagement, post-purchase, winback, etc.)
- **ICA definition**: who is the intended audience for these emails, and what is the primary monetisation action? (purchase, booking, upgrade, renewal)
- **Known pain points**: are there specific sequences underperforming, or is this a full-programme audit?
- **Time window**: what date range does the data cover?

If the user cannot provide structured data, guide them to export from their ESP (Klaviyo, ActiveCampaign, ConvertKit, Mailchimp, HubSpot) using the platform-specific report path.

## Step 3: Map the Subscriber Lifecycle

Before analysing gaps, construct the **Subscriber Lifecycle Map** — a complete picture of every email touchpoint from opt-in to churn:

1. **Acquisition stage**: opt-in source → welcome sequence → first conversion prompt
2. **Activation stage**: onboarding/education → engagement triggers → initial purchase or action
3. **Monetisation stage**: promotional sequences → upsell/cross-sell → loyalty/VIP triggers
4. **Retention stage**: re-engagement sequences → winback sequences → sunset/suppression logic
5. **Expansion stage**: referral prompts → advocacy sequences → community nurture

For each stage, document:
- Whether a sequence **exists** or is **absent** (structural gap)
- The **entry trigger** and **exit conditions**
- The **number of emails** and **cadence spacing**
- The **transition mechanism** between stages (tag-based, time-based, behaviour-based)

Flag any stage where no sequence exists as a **Lifecycle Dead Zone** — these represent the highest-priority structural gaps.

## Step 4: Perform Gap Analysis

Analyse the data across six diagnostic dimensions:

### 4.1 — Engagement Decay Analysis
- Plot open rate and click rate trends across each sequence position (Email 1, Email 2, … Email N)
- Identify the **decay inflection point** — the specific email where engagement drops below the sequence average by >20%
- Flag sequences where the decay inflection occurs before the primary conversion prompt

### 4.2 — Conversion Leakage Audit
- For each sequence with a revenue or conversion objective, calculate the **stage-to-stage conversion rate**
- Identify the **largest absolute drop-off** between consecutive emails (the leakage point)
- Calculate **revenue leakage estimate**: (subscribers at leakage point) × (sequence average conversion rate) × (average order value or deal value) = unrealised revenue

### 4.3 — Timing & Cadence Diagnostics
- Evaluate send-time consistency and day-of-week patterns against engagement data
- Identify cadence mismatches: sequences sending too aggressively (high unsubscribe rate relative to benchmark) or too passively (engagement decay from inactivity)
- Flag any gaps of >14 days between subscriber touchpoints where no intentional cooling period is designed

### 4.4 — Segmentation Gap Detection
- Assess whether sequences differentiate by ICA segment, engagement tier, or purchase history
- Identify **one-size-fits-all sequences** being sent to behaviourally distinct cohorts
- Flag high-value segments receiving the same messaging as low-intent segments

### 4.5 — Content & CTA Coherence
- Evaluate whether email subject lines, body copy, and CTAs align with the ICA's awareness stage at each sequence position
- Identify **premature asks** (hard sell before value establishment) and **delayed asks** (excessive nurture without conversion prompt)
- Flag emails with high open rates but low click rates (compelling hook, weak CTA) and emails with low open rates but high click-to-open rates (weak subject line, strong content)

### 4.6 — List Hygiene & Deliverability Signals
- Review unsubscribe rate trends, bounce rates, and spam complaint indicators
- Identify sequences or campaigns with anomalous deliverability signals that may indicate list health degradation
- Flag the absence of sunset or suppression logic for chronically disengaged subscribers

Apply any user-specific `instructions` from FutureProof context — such as industry benchmarks, known ICA response patterns, or ESP-specific nuances — to calibrate the analysis.

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


Produce the **Email Gap Hunter Report** with the following structure:

### A. Executive Summary
- Total gaps identified (categorised: structural, performance, strategic)
- Estimated total revenue leakage across all identified gaps
- Top 3 highest-impact gaps ranked by estimated revenue recovery potential

### B. Subscriber Lifecycle Map
- Visual or tabular lifecycle map showing all stages, active sequences, and identified dead zones
- Colour-coded status: 🟢 Performing | 🟡 Underperforming | 🔴 Missing/Critical

### C. Gap Register
A prioritised table of all identified gaps:

| Priority | Gap ID | Gap Type | Lifecycle Stage | Description | Estimated Revenue Impact | Recommended Fix |
|----------|--------|----------|-----------------|-------------|--------------------------|-----------------|
| P1 | GAP-001 | Structural | Retention | No winback sequence for churned buyers | £X,XXX/month | Build 5-email winback triggered at 90 days inactive |
| P2 | GAP-002 | Performance | Activation | 68% engagement drop at welcome email #3 | £X,XXX/month | Rewrite E3 — replace product feature dump with ICA pain-point story |
| ... | ... | ... | ... | ... | ... | ... |

### D. Critical Fix Briefs (Top 3)
For each of the top 3 gaps, provide:
- **Root cause analysis**: why the gap exists and what is driving the underperformance
- **Specific fix**: exact changes to implement — including rewritten subject lines, revised CTAs, new sequence logic, or segment splits (not vague recommendations)
- **Implementation spec**: trigger conditions, email count, cadence, and KPIs to track post-fix
- **Expected recovery**: quantified estimate of revenue or conversion improvement

### E. Benchmark Comparison
- Compare the user's key metrics against FutureProof-informed industry benchmarks or, if unavailable, against published benchmarks for their vertical and list size tier
- Highlight metrics that fall >1 standard deviation below benchmark as priority attention areas

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="email-gap-hunter", experiment={
  hypothesis: "Inserting a segmentation branch at the welcome sequence decay inflection point (Email 3) based on click behaviour will recover engagement and increase sequence completion rate",
  variants: ["control: current linear welcome sequence", "variant: behaviour-branched sequence splitting high-engagers to accelerated offer path and low-engagers to extended nurture path"],
  measurement: "sequence completion rate, click-through rate at Email 4+, conversion rate to first purchase within 30 days of opt-in",
  expected_impact: "20-30% improvement in welcome sequence conversion rate, 15% reduction in early unsubscribes"
})
```

```
FutureProof:save_experiment(skill="email-gap-hunter", experiment={
  hypothesis: "Closing the highest-priority lifecycle dead zone with a purpose-built sequence will recover currently unrealised revenue",
  variants: ["control: no sequence (current state)", "variant: new [N]-email sequence targeting [specific lifecycle stage gap]"],
  measurement: "reactivation rate, revenue attributed to new sequence, unsubscribe rate",
  expected_impact: "Capture estimated £X,XXX/month in previously leaked revenue within 60 days"
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
FutureProof:request_research(skill="email-gap-hunter",
  query="Current email marketing benchmark data by industry vertical 2024-2025: open rates, click rates, conversion rates, revenue per email, and optimal sequence lengths for welcome, nurture, and winback sequences",
  reason="Maintain calibrated benchmark comparisons and ensure gap severity scoring reflects current deliverability landscape and subscriber behaviour norms post-MPP"
)
```

```
FutureProof:request_research(skill="email-gap-hunter",
  query="Emerging best practices for email lifecycle automation: behavioural branching logic, predictive send-time optimisation, and AI-driven content personalisation frameworks",
  reason="Ensure recommended fixes incorporate leading-edge sequence architecture rather than legacy linear designs"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="email-gap-hunter", session={
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