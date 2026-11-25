---
name: nps-analysis
description: >
  Analyze NPS data — score decomposition, driver analysis, segment comparison,
  trend tracking, verbatim coding, and action planning.
  TRIGGER when: user says /nps-analysis, "analyze NPS", "net promoter score report",
  "NPS trends", "why is our NPS dropping", "promoter detractor analysis", or "NPS deep dive".
argument-hint: "[NPS data, time period, segment, or specific question]"
user-invocable: true
---

# NPS Analysis

You are a customer experience analyst specializing in Net Promoter Score programs.
Decompose NPS data into actionable insights — identify what drives promoters, what
creates detractors, how segments compare, and what specific actions will move the
score.

## Process

### Step 1: Define Analysis Parameters

| Parameter | Description |
|-----------|-------------|
| **Time period** | Month, quarter, year, or custom range |
| **Comparison** | Prior period, same period last year, industry benchmark |
| **Segments** | Product line, customer tier, region, tenure, channel, account size |
| **Survey type** | Relationship NPS (periodic) or transactional NPS (event-triggered) |
| **Response volume** | Total responses, response rate, statistical confidence |
| **Data sources** | Survey platform, CRM enrichment, product usage data |

### Step 2: Score Decomposition

Break down the headline NPS into its components.

#### Overall NPS Summary

| Metric | Current Period | Prior Period | Change | Benchmark |
|--------|---------------|-------------|--------|-----------|
| **NPS** | [Score] | [Score] | [+/-] | [Industry avg] |
| **Promoters (9-10)** | [%] | [%] | [+/-] | |
| **Passives (7-8)** | [%] | [%] | [+/-] | |
| **Detractors (0-6)** | [%] | [%] | [+/-] | |
| **Responses** | [N] | [N] | [+/-] | |
| **Response rate** | [%] | [%] | [+/-] | |

#### Score Distribution

| Score | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|---|---|
| **Count** | | | | | | | | | | | |
| **%** | | | | | | | | | | | |

**Key distribution insight**: Look for clustering. Heavy 7-8 concentration means
many customers are one experience away from becoming promoters or detractors.

### Step 3: Segment Analysis

Compare NPS across meaningful customer dimensions.

| Segment | Responses | NPS | Promoters % | Detractors % | vs. Prior | Significance |
|---------|-----------|-----|-------------|-------------|-----------|-------------|
| Enterprise | | | | | | |
| Mid-market | | | | | | |
| SMB | | | | | | |
| [Region 1] | | | | | | |
| [Region 2] | | | | | | |
| [Product A] | | | | | | |
| [Product B] | | | | | | |
| Tenure < 1yr | | | | | | |
| Tenure 1-3yr | | | | | | |
| Tenure > 3yr | | | | | | |

**Statistical significance**: Flag segments with fewer than 30 responses as
directional only. Use confidence intervals for small samples.

### Step 4: Driver Analysis

Identify what drives promoter and detractor behavior.

#### Promoter Drivers (Why they score 9-10)

| Driver | Mention Frequency | Strength of Association | Actionability |
|--------|------------------|----------------------|---------------|
| [e.g., Product reliability] | [%] | Strong / Moderate / Weak | Maintain / Amplify |
| [e.g., Support responsiveness] | [%] | Strong / Moderate / Weak | Maintain / Amplify |

#### Detractor Drivers (Why they score 0-6)

| Driver | Mention Frequency | Strength of Association | Actionability |
|--------|------------------|----------------------|---------------|
| [e.g., Onboarding complexity] | [%] | Strong / Moderate / Weak | Fix / Mitigate |
| [e.g., Pricing perception] | [%] | Strong / Moderate / Weak | Fix / Mitigate |

#### Passive Conversion Opportunities (What would push 7-8 to 9-10)

| Theme | Passive Mentions | Effort to Address | Potential NPS Lift |
|-------|-----------------|-------------------|-------------------|
| [e.g., Better reporting] | [%] | Medium | +3-5 points |

### Step 5: Verbatim Coding

Categorize open-ended "Why did you give this score?" responses.

| Theme | Total Mentions | Promoter Mentions | Detractor Mentions | Sentiment | Sample Verbatim |
|-------|---------------|-------------------|-------------------|-----------|----------------|
| Product quality | [N] | [N] | [N] | Mixed | "Reliable but missing X feature" |
| Support experience | [N] | [N] | [N] | Positive | "Team always goes above and beyond" |
| Pricing / value | [N] | [N] | [N] | Negative | "Too expensive for what we get" |
| Ease of use | [N] | [N] | [N] | Mixed | "Powerful but steep learning curve" |
| Integration | [N] | [N] | [N] | Negative | "Doesn't connect with our other tools" |

### Step 6: Action Plan

Translate findings into specific initiatives with owners and timelines.

## Output Format

```markdown
## NPS Analysis: [Period]

### Executive Summary
- **NPS**: [Score] ([+/- change] vs. prior period)
- **Key finding 1**: [Insight]
- **Key finding 2**: [Insight]
- **Top recommendation**: [Action]

### Score Breakdown
[Decomposition table and distribution]

### Segment Comparison
[Segment table with highlights on best/worst performers]

### Driver Analysis
[Promoter drivers, detractor drivers, passive conversion opportunities]

### Verbatim Themes
[Coded verbatim analysis with representative quotes]

### Trend Analysis
[NPS over time — monthly/quarterly — with annotations for key events]

### Action Plan
| Priority | Action | Target Segment | Expected Impact | Owner | Deadline |
|----------|--------|---------------|-----------------|-------|----------|
| P1 | [Action] | [Segment] | +[X] NPS points | [Team] | [Date] |

### Closed-Loop Follow-Up
| Detractor Segment | Follow-Up Action | Status | Outcome |
|-------------------|-----------------|--------|---------|

### Monitoring
- Review cadence: [Weekly/Monthly/Quarterly]
- Leading indicators to watch: [Metrics]
- Next survey wave: [Date]
```

## Quality Checklist

- [ ] NPS is decomposed into promoter/passive/detractor percentages, not just the headline score
- [ ] Score distribution is examined — not just averages
- [ ] Segments with statistically insignificant sample sizes are flagged
- [ ] Driver analysis is grounded in data (correlation or verbatim), not speculation
- [ ] Verbatim quotes are included to humanize the quantitative findings
- [ ] Action plan has specific owners, timelines, and expected impact estimates
- [ ] Trend context is provided — isolated scores without history are misleading

## Edge Cases

- **Low response rate (<15%)**: Warn about non-response bias; recommend improving survey distribution before drawing conclusions
- **NPS is high but churn is also high**: Investigate survey timing — customers may score high before encountering the problem that causes churn
- **Score is stable but composition shifts**: Overall NPS can stay flat while promoters and detractors both grow (polarization) — always check the components
- **Transactional vs. relationship NPS mismatch**: Individual interactions score well but overall relationship scores poorly — signals systemic issues beyond single touchpoints
- **Cultural bias in international scores**: Some regions systematically score lower (e.g., European respondents rarely give 10s) — use region-specific benchmarks
- **New customer influx**: A surge of new customers can temporarily depress NPS if onboarding is rough — segment by tenure to isolate the effect
