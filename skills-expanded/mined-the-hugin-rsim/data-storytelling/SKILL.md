---
name: data-storytelling
description: Transform raw data into persuasive business narratives using Setup→Conflict→Resolution framework. Templates for problem-solution, trend analysis, and comparison stories. Use when presenting data to stakeholders or building data-driven reports.
group: domain
triggers:
  - "данные в презентацию"
  - "бизнес отчёт"
  - "data storytelling"
  - "нарратив из данных"
  - "инсайты для стейкхолдеров"
output: "structured data narrative with headline, context, insight, recommendation, and call-to-action"
calls: []
---

# Data Storytelling

Transform raw data into persuasive narratives that drive business decisions.

## When to Activate

- Preparing data for stakeholders / executives
- Building reports or slide decks from analytics
- Writing data-driven recommendations
- Turning dashboards into actionable insights

## Three Pillars

| Pillar | Role | Without it... |
|---|---|---|
| **Data** | Evidence — numbers and trends | Opinions, not facts |
| **Narrative** | Meaning — context and implications | Numbers without story |
| **Visuals** | Clarity — charts and highlights | Complex tables nobody reads |

## Core Framework: Setup → Conflict → Resolution

```
Setup:      Context — where are we? What do we track?
Conflict:   Problem or opportunity — what changed? What's at risk?
Resolution: Recommendation — what do we do about it?
```

## Story Templates

### 1. Problem–Solution

```
HEADLINE: We're Losing $2.4M to Preventable Churn

SETUP:     Monthly churn has held at ~2.1% for 8 months.
           120 customers cancel monthly. LTV = $20K avg.

CONFLICT:  Analysis shows 68% of churners share a pattern:
           — No action in first 14 days after signup
           — Never used core Feature X
           Exit surveys: "Didn't understand the value"

RESOLUTION: Onboarding intervention for at-risk users (day 7 trigger):
           — Projected churn reduction: 35% (based on cohort A/B data)
           — Revenue impact: +$840K/year
           — Implementation cost: ~80 eng hours

CALL TO ACTION: Approve Q2 onboarding sprint. Review cohort data →
```

### 2. Trend Analysis

```
HEADLINE: Mobile Revenue Up 340% — Desktop Still Declining

SETUP:     18 months ago, mobile = 12% of revenue.
           Today: mobile = 41%, desktop = 59%.

CONFLICT:  Mobile conversion rate (2.8%) still lags desktop (4.1%).
           If mobile matched desktop conversion → +$1.1M ARR.

RESOLUTION: Mobile checkout redesign (UX audit shows 3 friction points).
           Q3 sprint → target mobile CVR 3.5% by EOY.
```

### 3. Comparison (Option Evaluation)

```
HEADLINE: Option B Delivers 2.3× ROI vs. Option A

METRIC        OPTION A    OPTION B    WEIGHT
Cost          $120K       $85K        30%
Time to value 6 months    3 months    25%
Scalability   Medium      High        25%
Risk          Low         Medium      20%

WEIGHTED SCORE: A = 62pts / B = 78pts

RECOMMENDATION: Proceed with Option B, mitigate risk via staged rollout.
```

## Presentation Arc

```
1. HEADLINE       — Specific + business impact (not "Q3 Report")
2. CONTEXT        — Why this matters, scope, timeframe
3. DISCOVERY      — What the data shows (key findings, 2–3 max)
4. ANALYSIS       — Why it happened (root cause, contributing factors)
5. RECOMMENDATION — What to do (specific, actionable)
6. IMPACT         — Expected outcome, metrics to track
7. CALL TO ACTION — Clear next step, owner, deadline
```

## Headline Formula

**"[Metric] + [Impact] + [Context]"**

| Bad headline | Good headline |
|---|---|
| "Sales Report Q3" | "Q3 Sales Up 23% — Enterprise Segment Drove 80% of Growth" |
| "Churn Analysis" | "Churn Costs $2.4M/Year — 3-Week Fix Can Recover $840K" |
| "User Engagement" | "DAU/MAU Dropped to 18% — Feature X Adoption is the Leading Indicator" |

## Visualization Principles

### Progressive Reveal

Build complexity across slides — don't dump all data at once:
```
Slide 1: Headline metric only
Slide 2: Add trend line
Slide 3: Add cohort breakdown
Slide 4: Root cause annotation
Slide 5: Recommendation + projected impact
```

### Annotation Over Decoration

```
❌ Pretty chart with no callouts
✅ Chart with annotation at inflection point:
   "← Launched Feature X here. Retention +12pp in 30 days."
```

### Before/After Contrast

Show the gap visually — don't leave audience to calculate it:
```
BEFORE: Conversion 2.1% → AFTER intervention: 3.4%
Impact: +$840K ARR (highlighted as large number, not hidden in table)
```

## Key Principles

1. **Start with the "so what"** — lead with insight, not methodology
2. **Curate ruthlessly** — 3 key findings beat 12 mediocre ones
3. **Quantify the impact** — "$840K" > "significant revenue opportunity"
4. **End with a decision** — every presentation needs a clear ask
5. **Use accessible language** — no jargon for executive audiences
