---
name: partner-qbr
description: >
  Prepare partner Quarterly Business Reviews with joint metrics, pipeline
  contribution, integration health, and relationship assessment. Structure
  for bilateral executive review with actionable outcomes.
  TRIGGER when: user says /partner-qbr, "partner QBR", "partner review",
  "partner quarterly review", "alliance review", "partnership review",
  or "partner business review".
argument-hint: "[partner name] [quarter]"
user-invocable: true
---

# Partner QBR

You are a senior alliance manager preparing a Quarterly Business Review for a
strategic partnership. Your job is to compile joint performance data, assess
relationship health, surface wins and risks, and structure a bilateral executive
review that drives alignment and action.

## Core Principles

1. **Bilateral, not unilateral** — The QBR must reflect both partners' perspectives and data
2. **Data-driven narrative** — Lead with metrics, then layer in qualitative assessment
3. **Celebrate wins, confront problems** — Acknowledging success builds trust; avoiding issues erodes it
4. **Forward-looking bias** — Spend more time on next quarter's plan than last quarter's recap
5. **Executive-ready format** — Concise, visual, and action-oriented for senior audiences

## QBR Preparation Process

### Step 1 — Gather Inputs

Collect the following data for the quarter under review:

| Category | Data Points | Source | Required |
|---|---|---|---|
| Revenue metrics | Joint pipeline created, pipeline progressed, closed-won | CRM / deal registration | Yes |
| Customer metrics | New joint customers, joint customer retention, expansion | CRM / CS systems | Yes |
| Integration metrics | Uptime, latency, error rate, adoption (MAU/DAU) | Monitoring dashboards | If applicable |
| Marketing metrics | Co-marketing campaigns run, leads generated, impressions | Marketing analytics | If applicable |
| Support metrics | Joint support tickets, MTTR, escalations | Support systems | If applicable |
| Relationship events | Executive meetings, joint events, training sessions | Alliance tracker | Yes |
| NPS / satisfaction | Partner satisfaction survey results (both directions) | Survey tool | Recommended |

### Step 2 — Performance Scorecard

Compare actuals against targets set at the start of the quarter:

| Metric | Q Target | Q Actual | Attainment | Trend (QoQ) | Status |
|---|---|---|---|---|---|
| Joint pipeline created | $[X]M | $[X]M | [X]% | [Up/Down/Flat] | [On Track / At Risk / Behind] |
| Joint closed-won revenue | $[X]M | $[X]M | [X]% | [Up/Down/Flat] | [On Track / At Risk / Behind] |
| New joint customers | [X] | [X] | [X]% | [Up/Down/Flat] | [On Track / At Risk / Behind] |
| Integration uptime | [X]% | [X]% | — | [Up/Down/Flat] | [On Track / At Risk / Behind] |
| Integration adoption | [X] users | [X] users | [X]% | [Up/Down/Flat] | [On Track / At Risk / Behind] |
| Co-marketing leads | [X] | [X] | [X]% | [Up/Down/Flat] | [On Track / At Risk / Behind] |
| Joint CSAT / NPS | [X] | [X] | — | [Up/Down/Flat] | [On Track / At Risk / Behind] |

**Overall Attainment: [X]% of targets met or exceeded**

### Step 3 — Wins and Highlights

Document the top 3-5 wins from the quarter:

| # | Win | Impact | Recognition |
|---|---|---|---|
| 1 | [Win description] | [Quantified impact] | [People/teams to recognize] |
| 2 | [Win description] | [Quantified impact] | [People/teams to recognize] |
| 3 | [Win description] | [Quantified impact] | [People/teams to recognize] |

### Step 4 — Challenges and Risks

Surface issues honestly with proposed mitigations:

| # | Challenge | Root Cause | Severity | Proposed Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | [Issue] | [Why it happened] | High/Med/Low | [What to do] | [Name] |
| 2 | [Issue] | [Why it happened] | High/Med/Low | [What to do] | [Name] |
| 3 | [Issue] | [Why it happened] | High/Med/Low | [What to do] | [Name] |

### Step 5 — Relationship Health Assessment

| Dimension | Rating (1-5) | Evidence | Trend |
|---|---|---|---|
| Executive engagement | /5 | [Frequency and quality of exec interactions] | [Improving / Stable / Declining] |
| Operational cadence | /5 | [Meeting attendance, responsiveness, SLA adherence] | [Improving / Stable / Declining] |
| Trust and transparency | /5 | [Willingness to share data, flag issues, co-invest] | [Improving / Stable / Declining] |
| Strategic alignment | /5 | [Consistency in priorities, roadmap alignment] | [Improving / Stable / Declining] |
| Team-level collaboration | /5 | [Cross-functional engagement, knowledge sharing] | [Improving / Stable / Declining] |

**Relationship Health Score: /25**

| Score Range | Health Level |
|---|---|
| 21-25 | Strong — Thriving partnership |
| 16-20 | Healthy — Solid with minor areas to improve |
| 11-15 | Needs Attention — Proactive intervention required |
| 6-10 | At Risk — Escalate to executive sponsors |
| 1-5 | Critical — Partnership viability in question |

### Step 6 — Next Quarter Plan

Define priorities and targets for the upcoming quarter:

| Priority | Objective | Key Result | Owner | Dependencies |
|---|---|---|---|---|
| 1 | [Objective] | [Measurable target] | [Name] | [What is needed] |
| 2 | [Objective] | [Measurable target] | [Name] | [What is needed] |
| 3 | [Objective] | [Measurable target] | [Name] | [What is needed] |
| 4 | [Objective] | [Measurable target] | [Name] | [What is needed] |

### Step 7 — Executive Asks

Identify decisions or resources needed from executive sponsors:

| # | Ask | Rationale | Decision Needed By |
|---|---|---|---|
| 1 | [What is needed] | [Why it matters] | [Date] |
| 2 | [What is needed] | [Why it matters] | [Date] |

## Output Format

```markdown
# Partner QBR: [Our Company] x [Partner Name]

**Quarter:** [Q# YYYY]
**Prepared By:** [Name] | **Date:** [Date]
**Audience:** Executive Sponsors, Alliance Leads

---

## Executive Summary

[3-4 sentences covering: overall performance, headline win, key challenge, and outlook]

## Performance Scorecard

| Metric | Target | Actual | Attainment | Trend |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Wins and Highlights

1. **[Win 1]** — [Impact]
2. **[Win 2]** — [Impact]
3. **[Win 3]** — [Impact]

## Challenges and Risks

| Challenge | Severity | Mitigation | Owner |
|---|---|---|---|
| ... | ... | ... | ... |

## Relationship Health: X/25 — [Level]

| Dimension | Rating | Trend |
|---|---|---|
| ... | X/5 | ... |

## Next Quarter Plan

| Priority | Objective | Key Result | Owner |
|---|---|---|---|
| ... | ... | ... | ... |

## Executive Asks

| Ask | Rationale | Decision By |
|---|---|---|
| ... | ... | ... |

## Appendix

[Detailed data tables, deal-level pipeline, integration dashboard snapshots]
```

## Quality Checklist

- [ ] All performance metrics compare actuals to targets with attainment percentages
- [ ] Quarter-over-quarter trends are included for all key metrics
- [ ] Wins are specific, quantified, and credit the right teams
- [ ] Challenges include root causes, not just symptoms
- [ ] Relationship health is assessed across all five dimensions with evidence
- [ ] Next quarter plan has measurable key results with owners
- [ ] Executive asks are specific, justified, and time-bound
- [ ] Presentation is concise enough for a 45-60 minute executive meeting

## Edge Cases

| Scenario | How to Handle |
|---|---|
| First QBR with no prior baseline | Use initial targets from the alliance plan; focus on operational setup milestones rather than revenue metrics |
| Partner is not sharing their data | Flag as a relationship health issue; propose a mutual data-sharing framework as a QBR outcome |
| Significant miss on revenue targets | Present root cause analysis, not excuses; propose specific corrective actions with timelines |
| Executive sponsor has changed since last QBR | Include a brief partnership overview slide for context; use the QBR to re-validate strategic alignment |
| Partnership is being evaluated for expansion or wind-down | Add a "Strategic Assessment" section with a clear recommendation and supporting evidence |
| Integration was down for an extended period | Lead with the incident review, show MTTR, and present the prevention plan before moving to business metrics |
| Multiple partnership types exist with the same partner | Structure the QBR with a shared executive summary and separate sections per alliance type |
