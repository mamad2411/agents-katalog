---
name: survey-analysis
description: "Analyzes survey results with statistical summaries, cross-tabulations, trend identification, and actionable insight recommendations. Use when interpreting survey data for decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Survey Analysis

## When to Use This Skill

Use this skill when you need to:
- Analyze results from a customer, employee, or market research survey
- Generate statistical summaries and identify meaningful patterns
- Create cross-tabulations to find segment differences
- Turn raw survey data into actionable business recommendations

**DO NOT** use this skill for designing surveys, running statistical software, or academic research analysis. This is for practical business survey interpretation.

---

## Core Principle

SURVEY DATA IS ONLY VALUABLE WHEN IT LEADS TO A DECISION — EVERY ANALYSIS MUST END WITH "HERE IS WHAT TO DO ABOUT IT."

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Survey type** | "What kind of survey? (customer satisfaction, NPS, market research, employee engagement)" | Customer satisfaction |
| **Response count** | "How many responses did you receive?" | Must be provided |
| **Key questions** | "What business questions should the analysis answer?" | Must be provided |
| **Data format** | "How is the data stored? (CSV, Google Sheets, raw platform export)" | Spreadsheet |
| **Segments** | "Any segments to compare? (customer type, plan tier, demographics)" | None — overall analysis |
| **Prior benchmarks** | "Do you have previous survey results or industry benchmarks to compare against?" | No prior data |

**GATE: Confirm brief and review the data before proceeding.**

---

## Phase 2: Analyze

### Analysis Framework

1. **Response overview** — total responses, response rate, completion rate
2. **Summary statistics** — means, medians, distributions for quantitative questions
3. **Frequency analysis** — response counts and percentages for categorical questions
4. **Cross-tabulations** — compare responses across key segments
5. **Trend identification** — patterns, outliers, and notable clusters
6. **Open-ended theming** — categorize free-text responses into themes

### Statistical Guidelines

- Report response rate and note if it is below 20% (potential non-response bias)
- Use median for skewed distributions, mean for normal distributions
- Note sample sizes per segment — do not draw conclusions from groups under 30
- Flag statistically small differences — a 2% gap with 50 responses is noise

**GATE: Present preliminary findings and confirm focus areas before building the full report.**

---

## Phase 3: Build

### Deliverables

**1. Executive Summary (1 page)**
- Top 3-5 findings in plain language
- Key metric headline numbers
- Recommended actions

**2. Detailed Analysis Report**
- Section for each survey question or question group
- Visualizations: bar charts for categorical, distribution plots for scale questions
- Cross-tabulation tables for segment comparisons
- Open-ended response themes with representative quotes

**3. Insight-Action Map**
| Finding | Implication | Recommended Action | Priority |
|---------|------------|-------------------|----------|
| NPS dropped 15 points | Customer sentiment declining | Investigate top complaints, prioritize fixes | High |

**4. Raw Data Summary Tables**
- Clean tables with all response data aggregated
- Ready for copy-paste into presentations or reports

---

## Phase 4: Polish

### Presentation Package

Format the key findings for sharing:
- 5-slide summary deck structure (overview, top findings, segment insights, recommendations, next steps)
- Talking points for each slide
- Anticipated questions and answers

### Follow-Up Recommendations

- What to investigate further based on findings
- Suggested follow-up survey questions for the next cycle
- Recommended timeline for the next survey

---

## Example 1: NPS Survey (200 responses, SaaS product)

**Key outputs:** NPS score with promoter/passive/detractor breakdown, NPS by customer segment, top 5 themes from detractor comments, 3 priority actions to improve score.

## Example 2: Post-Purchase Survey (500 responses, e-commerce)

**Key outputs:** Satisfaction score, top reasons for purchase, product quality ratings, delivery experience ratings, repurchase likelihood, open-ended improvement suggestions themed and ranked.

---

## Anti-Patterns

- **Reporting without interpreting** — "42% said yes" is data, not analysis. Always add "which means..." and "therefore we should..."
- **Cherry-picking results** — reporting only favorable findings undermines trust. Include the bad news with recommendations.
- **Over-interpreting small samples** — 10 responses from enterprise customers is not enough to draw segment conclusions. State limitations.
- **Ignoring open-ended responses** — free-text answers often contain the most actionable insights. Always theme and analyze them.
- **Analysis paralysis** — a 50-page report nobody reads is worse than a 2-page summary with clear actions.

---

## Recovery

- **Low response rate:** Acknowledge the limitation upfront. Focus on directional insights rather than precise percentages.
- **Contradictory results:** Segment the data — contradictions often resolve when you split by customer type or demographics.
- **No actionable findings:** Reframe the analysis around the original business questions. If the survey did not answer them, recommend better questions for next time.
- **Data quality issues:** Flag invalid or suspicious responses (all same answers, impossible combinations). Clean before analyzing.
