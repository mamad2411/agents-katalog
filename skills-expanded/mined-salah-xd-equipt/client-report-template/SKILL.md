---
name: client-report-template
description: "Designs client reporting templates with executive summaries, data visualizations, and next-step recommendations."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Client Report Template

## When to Use This Skill

Use this skill when you need to:
- Create recurring client report templates (weekly, monthly, quarterly)
- Structure executive summaries that busy decision-makers actually read
- Present data with clear visualizations and narrative context
- Include actionable next-step recommendations in every report

**DO NOT** use this skill for internal team reports, financial statements, or one-time project deliverables. This is for ongoing client-facing progress and performance reports.

---

## Core Principle

A CLIENT REPORT SHOULD TAKE 3 MINUTES TO SCAN AND 10 MINUTES TO READ IN FULL — IF THE CLIENT HAS TO ASK "SO WHAT?" AFTER READING IT, THE REPORT FAILED.

---

## Phase 1: Report Requirements

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Report type** | "Is this weekly, monthly, or quarterly?" | Monthly |
| **Service area** | "What are you reporting on — marketing, development, consulting, other?" | No default — must be provided |
| **Key metrics** | "What 3-5 KPIs does your client care about most?" | No default — must be provided |
| **Client's goal** | "What outcome is the client paying you to deliver?" | No default — must be provided |
| **Audience** | "Who reads this — founder, marketing director, C-suite?" | Business owner / founder |

**GATE: Confirm report structure and KPIs before building the template.**

---

## Phase 2: Report Template

### Report Structure

```
## [Client Name] — [Month/Period] Report
**Prepared by:** [Your name]
**Date:** [Date]
**Reporting period:** [Start date] — [End date]

---

### Executive Summary

[3-4 sentences maximum. State the top result, the most important trend,
and the #1 recommended action. A busy CEO should be able to read only
this section and understand how things are going.]

**Bottom line:** [One sentence — are we on track, ahead, or behind the goal?]

---

### Key Metrics Dashboard

| Metric | This Period | Last Period | Change | Target | Status |
|--------|-----------|------------|--------|--------|--------|
| [KPI 1] | [value] | [value] | [+/-X%] | [target] | ✓ On Track / ⚠ Watch / ✗ Behind |
| [KPI 2] | [value] | [value] | [+/-X%] | [target] | ✓ / ⚠ / ✗ |
| [KPI 3] | [value] | [value] | [+/-X%] | [target] | ✓ / ⚠ / ✗ |

---

### What We Did

[Bullet list of completed activities and deliverables this period.
Keep it factual — actions taken, not just plans made.]

- [Activity 1] — [result or output]
- [Activity 2] — [result or output]
- [Activity 3] — [result or output]

---

### What Worked

[Highlight 1-2 wins with context. Explain WHY it worked so the
client understands the strategy, not just the result.]

---

### What Needs Attention

[Flag 1-2 areas of concern with honest assessment. Include what
you are doing about it — never present a problem without a plan.]

---

### Recommendations & Next Steps

1. **[Action item]** — [Why and expected impact]. Owner: [who]. By: [date].
2. **[Action item]** — [Why and expected impact]. Owner: [who]. By: [date].
3. **[Action item]** — [Why and expected impact]. Owner: [who]. By: [date].

---

### Appendix (Optional)

[Detailed data tables, screenshots, campaign breakdowns, or
supporting information for clients who want to go deeper.]
```

---

## Phase 3: Data Presentation

### Visualization Guidelines

| Data Type | Best Format | Avoid |
|-----------|------------|-------|
| Trend over time | Line chart | Pie chart |
| Comparison between categories | Bar chart | 3D charts |
| Part of a whole | Stacked bar or simple table | Complex pie charts |
| Single key number | Large bold number with context | Buried in a paragraph |
| Before/after | Side-by-side comparison | Long narrative description |

### Narrative Rules

- Every number needs context — "2,400 visitors" means nothing without "up 35% from last month"
- Compare to the goal, not just the previous period
- Explain anomalies — spikes and dips need one-sentence explanations
- Use plain language — "conversion rate improved" not "we observed a positive delta in CR"

---

## Phase 4: Delivery & Follow-Up

### Delivery Checklist

- [ ] Executive summary is under 4 sentences
- [ ] All KPIs show period-over-period comparison and target status
- [ ] Every section answers "so what?" — not just data, but interpretation
- [ ] Recommendations are specific, assigned, and time-bound
- [ ] Report is formatted cleanly — consistent fonts, alignment, spacing
- [ ] Proofread for accuracy — one wrong number destroys credibility

### Delivery Best Practices

- Send the report 24 hours before any review meeting
- Include a 1-sentence email summary: "Revenue is up 18% — full report attached"
- Schedule a 15-30 minute call to walk through the report and discuss next steps
- Archive all reports for trend analysis and annual reviews

---

## Anti-Patterns

- **Data dump with no narrative** — raw numbers without interpretation make clients feel like they are doing your job for you.
- **Burying bad news** — hiding underperformance in an appendix erodes trust. Address it head-on with a plan.
- **Reports that take 30+ minutes to read** — if the client needs a meeting just to understand the report, it is too long.
- **No recommendations** — a report without next steps is a history lesson. Always tell the client what to do.
- **Inconsistent formatting** — changing the report layout every month makes it impossible to compare periods.
- **Vanity metrics only** — reporting impressions and followers when the client cares about revenue and leads.

---

## Recovery

- **Client never reads the report:** Shorten it drastically. Lead with the executive summary and offer details on request.
- **Client questions a number:** Always have the source data ready. Show the calculation and methodology transparently.
- **Metrics are not improving:** Acknowledge it directly. Present the diagnosis and a revised strategy. Do not spin bad results.
- **Client wants different metrics:** Update the KPI dashboard immediately. Ask why the new metrics matter to align your work.
- **Report takes too long to create:** Templatize everything. Use the same structure each period and only update the data and narrative.
