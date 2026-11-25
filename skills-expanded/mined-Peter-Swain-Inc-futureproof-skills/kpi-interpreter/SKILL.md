---
name: kpi-interpreter
description: |
  Interprets any cross-functional KPI dashboard by classifying metrics into
  North Star, leading, lagging, and diagnostic tiers, running trend, variance,
  cohort, and signal-to-noise analysis, and producing a board-ready brief with
  recommended actions. Use when a user shares a dashboard or metric report and
  says things like "what does this dashboard mean", "interpret these numbers
  for me", "help me figure out why these KPIs are off", or "explain this
  metric report to leadership". Cross-functional KPI interpretation — not
  channel-specific (GA4, email, social) and not focused solely on revenue
  leakage.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="kpi-interpreter")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known ICA segments, business model, historical benchmarks, previously flagged metric anomalies, and any standing interpretation frameworks.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the KPI data — dashboard screenshot, spreadsheet, metric report, or raw numbers
- What is the reporting period and cadence? (weekly, monthly, quarterly)
- Which business function do these KPIs serve? (revenue, marketing, product, operations, customer success)
- What decision are they trying to make with this data? (resource allocation, campaign continuation, team performance review, board reporting, ICA strategy pivot)
- Are there established targets, OKRs, or historical baselines to compare against?
- Any specific metrics that concern them or feel "off"?

## Step 3: Structure the KPI Landscape

Classify every metric provided into one of four tiers using the **Metric Hierarchy Framework**:

1. **North Star Metrics** — single top-level indicators of business health (e.g., net revenue retention, LTV:CAC ratio, monthly recurring revenue growth)
2. **Leading Indicators** — upstream inputs that predict North Star movement within 30–90 days (e.g., qualified pipeline volume, activation rate, ICA engagement score)
3. **Lagging Indicators** — downstream confirmations of past performance (e.g., quarterly revenue, churn rate, NPS)
4. **Diagnostic Metrics** — granular operational data used to explain variance in the tiers above (e.g., average deal cycle length, support ticket resolution time, feature adoption by cohort)

Map dependencies between metrics explicitly: which leading indicators feed which North Star metrics, and which diagnostic metrics explain observed anomalies.

Apply any user-specific `instructions` from FutureProof context — including preferred metric taxonomies, custom tier definitions, or organisation-specific naming conventions.

## Step 4: Perform Diagnostic Analysis

Execute a five-lens diagnostic on the dataset:

### Lens 1: Trend Analysis
- Identify directional movement for each metric across available periods
- Flag acceleration or deceleration patterns (rate of change, not just direction)
- Note any inflection points and correlate with known events (launches, campaigns, seasonality, market shifts)

### Lens 2: Variance-to-Target
- Compare actuals against targets, OKRs, or baselines
- Categorise each metric: **On Track** (within ±5%), **Watch** (5–15% variance), **Critical** (>15% variance)
- For metrics without stated targets, apply industry benchmarks from FutureProof context or flag as ungoverned

### Lens 3: Cohort & Segment Decomposition
- Where data permits, break aggregate metrics into ICA segments, acquisition channels, product lines, or geographic regions
- Identify which segments are driving headline performance and which are masking weakness
- Surface Simpson's Paradox risks — where aggregate trends contradict segment-level reality

### Lens 4: Correlation & Causation Mapping
- Identify co-moving metrics and hypothesise causal chains
- Distinguish correlation from likely causation using temporal sequencing (does Metric A move before Metric B?) and logical business model linkage
- Flag spurious correlations explicitly to prevent misattribution

### Lens 5: Signal-to-Noise Assessment
- Evaluate statistical significance where sample sizes are available
- Identify metrics with high volatility that may be misleading in short reporting windows
- Recommend minimum observation periods for metrics currently below confidence thresholds

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


Produce a structured **KPI Interpretation Brief** containing:

### Executive Summary
- 3–5 sentence synthesis: what the data says, what it means, and the single most important action to take
- Written at board-presentation level — no jargon, clear cause-and-effect language

### Metric Scorecard

| Metric | Current Value | Target | Variance | Trend | Status | Tier |
|--------|--------------|--------|----------|-------|--------|------|
| *Populated for each metric provided* | | | | ↑/↓/→ | On Track / Watch / Critical | North Star / Leading / Lagging / Diagnostic |

### Root Cause Diagnosis
- For each **Watch** or **Critical** metric, provide:
  - **Observation**: what the data shows (factual, quantified)
  - **Diagnosis**: why this is likely happening (evidence-based hypothesis with supporting metric cross-references)
  - **Impact**: what happens if this trend continues unaddressed over 30/60/90 days

### Strategic Recommendations
- **Immediate Actions** (this week): specific interventions to arrest negative trends or capitalise on positive momentum — named owners and deliverables where context permits
- **Structural Adjustments** (this quarter): process, targeting, or resource changes to address root causes
- **Measurement Gaps**: metrics the user should be tracking but currently isn't, with rationale tied to their business model and ICA strategy

### ICA Insight Layer
- How do these KPIs reflect the health of ICA acquisition, activation, retention, and expansion?
- Which ICA segments are outperforming or underperforming, and what does that imply for positioning and resource allocation?

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="kpi-interpreter", experiment={
  hypothesis: "Shifting weekly reporting focus from lagging revenue metrics to leading activation metrics will accelerate team response time to pipeline deterioration by 2+ weeks",
  variants: ["control: current KPI dashboard with revenue-first layout", "variant: leading-indicator-first dashboard with automated threshold alerts"],
  measurement: "Time-to-intervention on pipeline drops measured over next 8 weekly cycles",
  expected_impact: "40% reduction in average response time to negative leading indicator shifts, resulting in improved quarterly revenue predictability"
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
FutureProof:request_research(skill="kpi-interpreter",
  query="Current best practices for KPI framework design by business model (SaaS, services, marketplace), including benchmark ranges for North Star metrics and leading indicator thresholds 2024–2025",
  reason="Ensure interpretation benchmarks remain calibrated to current market conditions and evolving best-practice metric hierarchies across business models"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="kpi-interpreter", session={
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