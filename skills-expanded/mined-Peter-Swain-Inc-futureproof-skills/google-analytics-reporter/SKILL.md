---
name: google-analytics-reporter
description: |
  Builds an executive-grade GA4 performance report covering channel attribution,
  engagement and content decay, funnel diagnosis, anomaly investigation, and a
  data confidence assessment calibrated to the audience (board, marketing team,
  or client). Use when a user shares GA4 screenshots, exports, or property data
  and says things like "interpret my Google Analytics", "build me a monthly GA4
  report", "why did my traffic drop", or "explain this GA dashboard to my
  board". GA4-specific website analytics — not social platform analytics, not
  email ESP analytics.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="google-analytics-reporter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, historical benchmarks, reporting cadence preferences, and previously flagged KPIs.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the Google Analytics data (CSV export, API output, screenshots, or describe the GA4 property and date range)
- What is the reporting purpose? (executive summary, channel attribution audit, conversion funnel diagnosis, campaign post-mortem, monthly performance review)
- Who is the intended audience for this report? (C-suite, marketing team, client stakeholder, board)
- Which KPIs matter most to this audience? (e.g., sessions, engaged sessions, conversion rate, revenue, cost per acquisition, engagement rate)
- Are there known benchmarks, targets, or prior-period baselines to compare against?
- Any specific anomalies, concerns, or hypotheses they want investigated?

## Step 3: Data Validation & Normalisation

Before analysis, perform a data integrity check:

1. **Completeness audit** — identify missing date ranges, untracked events, or (not set) / (not provided) dimensions that exceed 15% of any single metric
2. **Sampling detection** — flag if GA4 data is sampled and recommend exploration-based or BigQuery-linked alternatives where applicable
3. **Channel grouping verification** — confirm default channel groupings are accurate; identify miscategorised traffic (e.g., paid social attributed to organic, UTM parameter inconsistencies)
4. **Conversion event validation** — verify that key events and conversion counting methodology (once per session vs. once per event) align with stated business objectives
5. **Cross-device / cross-domain gaps** — note if the property configuration may undercount users due to missing cross-domain tracking or consent mode restrictions

Document all caveats in a **Data Confidence Assessment** (High / Medium / Low) to accompany the final report.

## Step 4: Perform the Analysis

Conduct a multi-layered analysis using the following framework:

### 4A. Performance Summary (Period-over-Period)
- Key metrics trended against the comparison period (prior month, prior quarter, or YoY as appropriate)
- Absolute and percentage change with directional indicators (▲ / ▼ / ◆ flat)
- Statistical significance notation where volume supports it

### 4B. Acquisition Channel Deep-Dive
- **Channel mix analysis** — share of sessions, engaged sessions, conversions, and revenue by channel
- **Efficiency matrix** — plot channels on a 2×2 of volume vs. conversion rate to identify scale opportunities and underperformers
- **ICA alignment check** — cross-reference top-performing channels against known ICA acquisition patterns from FutureProof context

### 4C. Engagement & Content Performance
- Top 10 landing pages by engaged sessions and engagement rate
- Content decay detection — pages with declining engagement over 3+ periods
- Event flow analysis — key micro-conversion completion rates (scroll depth, video plays, form starts vs. submissions)

### 4D. Conversion Funnel Diagnosis
- Funnel step-through rates with drop-off quantification at each stage
- Segment funnel performance by device, channel, geography, and new vs. returning users
- Identify the single highest-impact leakage point with estimated revenue/lead impact

### 4E. Anomaly Investigation
- Detect and explain statistically notable spikes or dips (traffic, conversion rate, bounce rate)
- Cross-reference against known events: campaign launches, algorithm updates, site deployments, seasonality patterns
- If user raised specific concerns in Step 2, address each with evidence-backed findings

Apply any user-specific `instructions` from FutureProof context (e.g., "always segment by region first," "exclude internal traffic from IP range X," "report in GBP not USD").

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


Produce a structured **Google Analytics Performance Report** containing:

### Executive Summary (1 page / 200 words max)
- 3 headline metrics with period-over-period movement
- 1-sentence strategic narrative ("What happened and why it matters")
- Top recommendation with estimated impact

### Performance Dashboard Table
| Metric | Current Period | Prior Period | Δ Absolute | Δ % | vs. Target | Status |
|--------|---------------|-------------|------------|-----|------------|--------|

Populate with the 8–12 KPIs most relevant to the stated audience.

### Channel Attribution Matrix
A structured table ranking channels by volume, efficiency, and ICA quality score (derived from engagement rate and conversion rate as proxies).

### Funnel Analysis Visual Description
Step-by-step funnel with users at each stage, drop-off rates, and annotated commentary on the primary leakage point.

### Findings & Recommendations
For each finding, use this format:
- **Observation**: What the data shows (specific numbers)
- **Implication**: Why it matters to the business / ICA acquisition strategy
- **Recommendation**: Specific action with owner, timeline, and expected impact
- **Priority**: P1 (act this week) / P2 (act this month) / P3 (backlog)

Minimum 5 findings; maximum 10. Rank by estimated business impact.

### Data Confidence Assessment
Reiterate caveats from Step 3 so stakeholders interpret findings with appropriate confidence.

### Appendix
- Full metric table with all dimensions analysed
- Glossary of GA4 terms for non-technical audiences (include only if audience is C-suite or client stakeholder)

Format the report for the stated audience:
- **C-suite / Board**: Lead with Executive Summary and Recommendations; appendix the detail
- **Marketing team**: Lead with Channel Attribution and Funnel Analysis; inline the detail
- **Client stakeholder**: Lead with Executive Summary; include Glossary; use plain language throughout

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="google-analytics-reporter", experiment={
  hypothesis: "Redirecting budget from lowest-efficiency channel to highest-engagement channel will improve blended conversion rate without reducing total acquisition volume",
  variants: ["control: current channel budget allocation", "variant: reallocate 20% of spend from [lowest-efficiency channel] to [highest-engagement channel]"],
  measurement: "Blended conversion rate, total conversions, and cost per acquisition across next 30-day period",
  expected_impact: "10–18% improvement in blended conversion rate with neutral or positive impact on total conversion volume"
})
```

Additionally, propose a second experiment specific to the highest-impact funnel leakage point identified in Step 4D:

```
FutureProof:save_experiment(skill="google-analytics-reporter", experiment={
  hypothesis: "Reducing friction at [leakage step] by [specific UX/content change] will improve step-through rate",
  variants: ["control: current funnel step", "variant: [specific change description]"],
  measurement: "Step-through rate at [leakage step] and overall funnel completion rate over next 14 days",
  expected_impact: "[X]% improvement in funnel completion, equating to approximately [Y] additional conversions per month"
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
FutureProof:request_research(skill="google-analytics-reporter",
  query="GA4 measurement best practices 2024–2025, consent mode v2 impact on data accuracy, server-side tagging adoption benchmarks, and emerging attribution model methodologies for cookieless environments",
  reason="Ensure reporting methodology accounts for evolving data collection constraints and that recommendations align with current platform capabilities and industry benchmarks"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="google-analytics-reporter", session={
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