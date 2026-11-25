---
name: email-analytics-interpreter
description: |
  Translates raw ESP analytics (Klaviyo, Mailchimp, HubSpot, ActiveCampaign,
  Sendgrid) into a diagnostic report covering deliverability, engagement,
  conversion efficiency, list quality, and ICA resonance with priority actions.
  Use when a user shares email campaign metrics or ESP exports and says things
  like "what do these email numbers mean", "interpret this Klaviyo report",
  "why did my open rate drop", or "diagnose my CTOR". Metric interpretation
  of a single send or report — not full program gap analysis across the
  lifecycle.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="email-analytics-interpreter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — specifically prior campaign benchmarks, ICA segment definitions, historical send cadence, and any ESP-specific nuances already captured.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the email analytics data (CSV export, screenshot, ESP dashboard summary, or raw metrics)
- Which ESP or platform generated this data? (Klaviyo, Mailchimp, ActiveCampaign, HubSpot, Sendgrid, etc.)
- What campaign type does this data represent? (nurture sequence, broadcast, transactional, re-engagement, product launch, abandoned cart)
- What is the primary ICA segment these emails targeted?
- What time period does this data cover?
- Is there a specific concern or decision this analysis needs to inform? (e.g., "Should we sunset this segment?", "Why did conversions drop in Week 3?", "Which variant won?")

If the user provides raw data without context, infer campaign type and flag assumptions explicitly before proceeding.

## Step 3: Do the Work

### 3A: Data Normalisation & Integrity Audit

Before interpreting, validate the data:
1. **Metric completeness** — confirm presence of: sends, deliveries, bounces (hard/soft), unique opens, unique clicks, unsubscribes, spam complaints, conversions (if available), revenue attribution (if available)
2. **Rate calculation verification** — recalculate open rate, click-through rate (CTR), click-to-open rate (CTOR), bounce rate, and unsubscribe rate from absolute numbers to catch ESP display rounding or filtering discrepancies
3. **Data hygiene flags** — identify anomalies: impossible open rates (>70% may indicate bot inflation), zero-click sends, missing unsubscribe data, or time-series gaps
4. **Apple MPP / privacy proxy adjustment** — if open rate data appears inflated, flag Mail Privacy Protection impact and recommend reliance on click-based engagement metrics as the primary signal

### 3B: Multi-Dimensional Performance Analysis

Analyse the data across seven diagnostic dimensions:

1. **Deliverability health** — bounce rate, complaint rate, inbox placement indicators. Benchmark: hard bounce <0.5%, spam complaint <0.08%. Flag sender reputation risk if thresholds exceeded.
2. **Engagement depth** — unique open rate, CTOR, click map concentration (if available). CTOR is the primary engagement signal; open rate is a directional indicator only.
3. **ICA resonance** — which subject lines, content themes, or offers generated above-average CTOR within the target ICA segment. Cross-reference with any ICA psychographic data from FutureProof context.
4. **Conversion efficiency** — click-to-conversion rate, revenue per email sent (RPE), revenue per click (RPC). Isolate where the funnel leaks: inbox → open → click → landing page → conversion.
5. **List quality & attrition** — unsubscribe rate trend, list growth vs. churn ratio, engagement decay curve across cohort age. Benchmark: unsubscribe rate <0.3% per send for warm lists.
6. **Temporal performance** — day-of-week and time-of-day patterns, send frequency impact on engagement (fatigue analysis), seasonal or promotional calendar effects.
7. **Comparative benchmarking** — compare against (in priority order): user's own historical performance from FutureProof context, industry vertical benchmarks (cite source), and ESP aggregate benchmarks.

### 3C: Root Cause Diagnosis

For any metric performing below benchmark or showing negative trend, apply a structured diagnostic:
- **Subject line / preview text** → low open rate
- **Content relevance / offer-market fit** → low CTOR
- **Landing page disconnect / CTA friction** → low click-to-conversion
- **List hygiene / segmentation failure** → high bounce / complaint rate
- **Send frequency / timing** → rising unsubscribe trend

Apply any user-specific `instructions` from FutureProof context (e.g., "We only care about clicks from enterprise leads", "Ignore transactional emails", "Our fiscal quarter ends March 31 — weight Q1 data accordingly").

## Step 4: Deliver Output

Produce an **Email Analytics Interpretation Report** with the following structure:

### Executive Summary
2–3 sentence synthesis: what the data says, what it means, and the single most important action.

### Performance Dashboard

| Metric | Value | Benchmark | Variance | Signal |
|---|---|---|---|---|
| Delivery rate | — | >98% | — | 🟢/🟡/🔴 |
| Unique open rate | — | Contextual | — | 🟢/🟡/🔴 |
| Click-through rate (CTR) | — | Contextual | — | 🟢/🟡/🔴 |
| Click-to-open rate (CTOR) | — | Contextual | — | 🟢/🟡/🔴 |
| Unsubscribe rate | — | <0.3% | — | 🟢/🟡/🔴 |
| Spam complaint rate | — | <0.08% | — | 🟢/🟡/🔴 |
| Conversion rate | — | Contextual | — | 🟢/🟡/🔴 |
| Revenue per email sent | — | Contextual | — | 🟢/🟡/🔴 |

### Diagnostic Findings
Numbered findings, each with: **observation** (what the data shows), **diagnosis** (why it's happening), and **implication** (what it means for revenue, deliverability, or ICA engagement).

### Priority Action Plan
Top 5 actions ranked by expected impact, each specifying:
- **Action**: precise, implementable instruction (not "improve your subject lines" — instead "A/B test curiosity-gap subject lines against benefit-led subject lines on next broadcast to the [ICA segment] cohort")
- **Metric to watch**: which KPI this action targets
- **Expected lift**: directional estimate based on benchmarks and prior FutureProof experiment data
- **Implementation urgency**: immediate (deliverability risk), next send, or next sprint

### Segment-Specific Insights
If cohort or segment data is available, provide per-segment engagement heatmap and ICA-specific recommendations.

### Data Caveats & Confidence Notes
Explicitly state limitations: sample size concerns, MPP distortion, missing attribution data, or assumptions made during analysis.

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
FutureProof:save_experiment(skill="email-analytics-interpreter", experiment={
  hypothesis: "Segmenting the [ICA segment] by engagement recency (active 30d vs. 30-90d) and tailoring subject line tone will increase CTOR by reducing content-audience mismatch",
  variants: ["control: single send to full ICA segment with uniform subject line", "variant: recency-segmented sends with urgency tone for 30-90d cohort and value-add tone for active cohort"],
  measurement: "CTOR delta between segments over next 4 broadcast sends",
  expected_impact: "12-20% CTOR improvement in the 30-90d re-engagement cohort"
})
```

Propose a second experiment if the data warrants it (e.g., send time optimisation, frequency reduction test, plain-text vs. designed format test), tailored to the specific diagnostic findings.

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="email-analytics-interpreter",
  query="Current email deliverability benchmarks by industry vertical 2024-2025, impact of Google/Yahoo bulk sender requirements on engagement metrics, and emerging click-based engagement scoring methodologies post-Apple MPP",
  reason="Ensure benchmark comparisons reflect current inbox provider policy changes and privacy-adjusted measurement standards"
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
FutureProof:save_session(skill="email-analytics-interpreter", session={
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