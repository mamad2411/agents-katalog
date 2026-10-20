---
name: "stakeholder-report"
description: "Weekly and monthly stakeholder data report: headline metrics, trends, root cause analysis, action items — structured for executive and cross-functional audiences"
---

# Stakeholder Report Skill

## When to activate
- Writing the weekly or monthly data report for leadership, board, or cross-functional stakeholders
- Translating raw analytics into a decision-ready document — not just a data dump
- You need to present both what happened and why, not just metrics
- Preparing the analytical section of a business review, QBR, or board packet
- Communicating data findings to a mixed audience (technical and non-technical)

## When NOT to use
- Live dashboard updates — set those up in your BI tool
- Raw data exports — stakeholders don't need to see CSVs
- Statistical research papers — this is business communication, not academic analysis
- One-off exploratory analysis — use `/sql` or `/pandas-polars` for ad-hoc work

## Instructions

### Weekly stakeholder report

```
Write a weekly data report for [audience: leadership team / department heads / board].

COMPANY/TEAM: [name]
WEEK OF: [date range]
REPORT AUTHOR: [your name/team]

HEADLINE METRICS (vs. last week and vs. target):

Growth:
- [Metric 1]: [value] ([+/-X%] WoW, [+/-X%] vs. target)
- [Metric 2]: [value] ([+/-X%] WoW, [+/-X%] vs. target)

Revenue:
- [Metric]: [value] ([change])

Engagement / Product:
- [Metric]: [value] ([change])

Efficiency:
- [Metric]: [value] ([change])

WHAT HAPPENED THIS WEEK (events that explain the numbers):
- [Event 1: product release, campaign, incident, partner deal, etc.]
- [Event 2]

ANALYSIS:
- Root cause of biggest positive movement: [describe]
- Root cause of biggest negative movement: [describe]
- Any anomalies that don't fit the pattern: [describe or "none"]

DECISIONS NEEDED THIS WEEK:
[List any decisions that the data is informing — what should the team do differently?]

NEXT WEEK PREVIEW:
- Metrics to watch: [which metrics are most likely to move next week and why]
- Planned changes that will affect data: [releases, campaigns, etc.]

Generate a report in narrative + data format. Lead with a one-paragraph executive summary. Use headers for each section. Include specific data points. Avoid vague language ("relatively good" → "14% above plan"). Total length: 600-800 words.
```

---

### Monthly stakeholder report

```
Write a monthly data report. More detailed than weekly — includes trends, cohort analysis, and forward-looking commentary.

MONTH: [Month Year]
AUDIENCE: [leadership / board / investors / all-hands]

EXECUTIVE SUMMARY:
- Month in one sentence: [the most important thing that happened]
- Month vs. plan: [on track / ahead / behind — primary driver]

MONTHLY METRICS (vs. last month and vs. same month last year):

[Metric] | [This month] | [Last month] | [MoM %] | [Last year] | [YoY %] | [vs. plan]
Revenue | $[X]M | $[X]M | [+/-X%] | $[X]M | [+/-X%] | [+/-X%]
[Metric 2] | ... | ... | ... | ... | ... | ...
[Continue for each KPI]

TREND ANALYSIS:
- 3-month trend on [most important metric]: [describe direction and rate of change]
- 12-month trend on [revenue or primary KPI]: [describe]
- Leading indicators for next month: [what do early signals say about next month?]

ROOT CAUSE ANALYSIS — WINS:
[For the biggest positive movement: what drove it, is it repeatable, what should we do more of?]

ROOT CAUSE ANALYSIS — MISSES:
[For the biggest miss: what caused it, is it one-time or structural, what's the plan?]

COHORT INSIGHTS (if applicable):
[New user cohort performance, retention curves, LTV by acquisition source]

FORECAST UPDATE:
- Revised Q[?] forecast: $[X]M (was $[X]M, change due to: [reason])
- Annual forecast: $[X]M ([X]% above/below original plan)
- Key assumption changes: [what changed in the model]

ACTIONS AND OWNERS:
| Action | Owner | Due Date | Success Metric |
|---|---|---|---|
| [Action 1] | [Name] | [Date] | [How we measure it] |
| [Action 2] | [Name] | [Date] | [How we measure it] |

Generate the full monthly report. Narrative tone — not a bullet dump. Each section should connect to the next.
```

---

### Root cause analysis section

This is the most valuable and hardest section to write. Use this prompt to structure it:

```
Write a root cause analysis for [metric name] [increasing/decreasing] by [X%] in [period].

SYMPTOM:
[Metric] changed from [X] to [X] — a [X%] [increase/decrease].
This was [expected / unexpected / partially expected].

DATA I HAVE:
- Segment breakdown: [how does this metric break down by [channel / cohort / geography / product line]?]
- Correlation with other metrics: [what moved at the same time?]
- Timeline: [when exactly did it start moving? Was it gradual or sudden?]

HYPOTHESES (list in order of likelihood):
1. [Most likely cause] — supported by: [what data supports this]
2. [Second hypothesis] — supported by: [data]
3. [Third hypothesis] — supported by: [data]

WHAT I'VE RULED OUT:
- [Hypothesis X] — because [evidence against it]

CONCLUSION:
- Primary cause: [your best assessment]
- Confidence: [High / Medium / Low]
- How to verify: [what analysis would confirm this]
- Recommended action: [what to do about it]
- Expected impact of action: [X% improvement in metric over X weeks]

Write this as a 300-word RCA section ready to drop into a stakeholder report.
```

---

### Board-level data summary

```
Write the data/metrics section of a board update.

BOARD MEETING: [date]
REPORTING PERIOD: [quarter or month]
COMPANY STAGE: [seed / Series A / growth / pre-IPO]

HEADLINE METRICS vs. PLAN:
[Paste your key metrics with plan comparison]

Key items boards care about (by stage):

SEED/SERIES A:
- Revenue/ARR and growth rate vs. plan
- Burn rate and runway
- Key product or customer milestones
- Hiring vs. plan

GROWTH STAGE:
- Revenue, gross margin, and unit economics trends
- CAC and payback period — improving or deteriorating?
- NRR — expansion vs. churn
- Path to profitability (if relevant)

PRE-IPO:
- GAAP vs. non-GAAP metrics
- Rule of 40 position
- Quarterly guidance and variance explanation

Write the metrics section:
1. 2-sentence performance summary (honest — boards see through spin)
2. Key metrics table with vs. plan
3. 3 bullets: what drove performance (positive and negative)
4. 1 forward-looking sentence: revised forecast or key watch item for next quarter

Under 300 words. No jargon. Lead with facts.
```

---

### QBR (quarterly business review) data package

```
Write the data package for a quarterly business review with [audience: customers / internal leadership / partners].

QUARTER: Q[?] [Year]
TYPE: [Internal QBR / Customer QBR / Partner QBR]

INTERNAL QBR (leadership team):
- Quarter performance vs. OKRs
- Top 3 wins with data
- Top 3 misses with root cause
- Revised annual forecast
- Resource recommendations for next quarter

CUSTOMER QBR (for a SaaS customer success review):
Customer: [name]
- Usage metrics: [DAUs, key features used, adoption vs. contracted seats]
- Value delivered: [outcomes they achieved — quantify where possible]
- Upcoming roadmap features relevant to them
- Renewal risk level: [Green / Yellow / Red]
- Recommended next steps for their account

PARTNER QBR:
- Joint pipeline generated: $[X]M
- Joint wins: [N] customers, $[X]M ARR
- Pipeline at risk: [N] deals, reasons
- Co-marketing performance
- Recommended investments for next quarter

Generate the appropriate QBR data package based on the type selected.
```

---

### Metrics glossary section

When your stakeholders don't know what the metrics mean:

```
Generate a plain-English metrics glossary for our stakeholder report.

METRICS TO DEFINE:
[List your metrics]

For each metric:
- Name: [official name]
- Plain English: [what it measures in one sentence — no jargon]
- Why it matters: [why this metric tells us whether the business is healthy]
- How it's calculated: [formula or brief description]
- Target range: [what "good" looks like for our business]
- What causes it to move: [the main drivers]

Keep each definition under 80 words. Write for a non-technical executive who is smart but not a data analyst.
```

## Example

**User:** Monthly report for the leadership team. October revenue: $2.1M (plan was $2.0M, +5%). MoM growth: +12%. YoY: +47%. Churn: 2.1% (was 1.8% last month). NRR: 108% (was 112% last month). Biggest event: enterprise customer churned mid-month (was 8% of ARR). New logo wins: 14 (best month ever). Audience: CEO, CFO, VP Sales, VP Product.

**Expected output:** Full monthly report opening with "October was a record new business month that was partially offset by our largest customer churn event to date." Revenue section shows $2.1M vs. $2.0M plan. Root cause on churn: the enterprise customer departure drove the NRR decline from 112% to 108% — a structural, not trend event. New logo record is genuine signal. Actions table: post-mortem on churned account (VP Customer Success, Nov 7), ICP refinement to screen out customers with similar risk profile (VP Product + VP Sales, Nov 14). Watch list: enterprise renewal pipeline for Q4.

---
