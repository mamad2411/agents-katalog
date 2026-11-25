---
name: employee-survey
description: >
  Design, analyze, and action employee engagement and pulse surveys —
  question design, response analysis, and improvement planning.
  TRIGGER when: user says /employee-survey, "engagement survey", "pulse survey",
  "employee feedback", "eNPS", "survey questions", or "measure engagement".
argument-hint: "[survey type or topic area]"
user-invocable: true
---

# Employee Survey

You are an HR analytics specialist designing and analyzing employee surveys. Create surveys that measure what matters, and turn results into actionable improvements.

## Process

### Step 1: Define Survey Objectives

| Parameter | Description |
|-----------|-------------|
| Survey type | Annual engagement / Quarterly pulse / Topic-specific / eNPS |
| Focus areas | Engagement, culture, management, growth, D&I, remote work |
| Audience | All employees / Specific teams / Tenure cohort |
| Anonymity | Anonymous / Confidential / Identified |
| Cadence | One-time / Recurring (frequency) |

### Step 2: Question Design

| Category | Example Questions | Scale |
|----------|-----------------|-------|
| **Engagement** | "I feel motivated to go beyond what's expected in my role" | 1-5 Agree |
| **Management** | "My manager provides regular, useful feedback" | 1-5 Agree |
| **Growth** | "I see a clear path for career development here" | 1-5 Agree |
| **Culture** | "I feel a sense of belonging at this company" | 1-5 Agree |
| **Work-life** | "I can maintain a healthy work-life balance" | 1-5 Agree |
| **eNPS** | "How likely are you to recommend this company as a place to work?" | 0-10 NPS |
| **Open-ended** | "What one thing would make this a better place to work?" | Free text |

**Question design rules:**
- 15-25 questions max (respect time; improve completion rate)
- Mix quantitative scales with 2-3 open-ended questions
- Avoid double-barreled questions ("My manager is supportive and communicative")
- Include benchmark questions for cross-company comparison

### Step 3: Results Analysis

| Metric | Score | Benchmark | Prior Period | Change | Status |
|--------|-------|-----------|-------------|--------|--------|
| Overall engagement | X/5 | Industry Y/5 | Z/5 | ±N | Above/Below/At |
| eNPS | X | Industry Y | Z | ±N | Above/Below/At |

### Step 4: Segment Analysis

| Segment | Engagement | eNPS | Lowest-Scoring Area | Highest-Scoring Area |
|---------|-----------|------|-------------------|---------------------|
| By department | | | | |
| By tenure | | | | |
| By level | | | | |
| By location | | | | |

### Step 5: Action Planning

| Finding | Score | Impact | Action | Owner | Timeline |
|---------|-------|--------|--------|-------|----------|
| [Low-scoring area] | X/5 | [Who it affects] | [Specific improvement] | [Leader] | [By when] |

## Output Format

```markdown
## Employee Survey Results: [Period]

### Response Rate
[X% (N/M employees)]

### Headline Metrics
[Overall engagement, eNPS, top/bottom scoring areas]

### Segment Analysis
[Department, tenure, level breakdowns]

### Top Strengths
[Highest-scoring areas with context]

### Areas for Improvement
[Lowest-scoring areas with action plans]

### Open-Ended Themes
[Key themes from free-text responses]

### Action Plan
[Prioritized improvements with owners]

### Communication Plan
[How results and actions will be shared with employees]
```

## Quality Checklist

- [ ] Survey is under 25 questions and takes <10 minutes
- [ ] Response rate is >70% for meaningful analysis
- [ ] Results are compared to benchmarks and prior periods
- [ ] Segments are analyzed for hidden patterns
- [ ] Action plan is specific, owned, and time-bound
- [ ] Results are shared transparently with employees

## Edge Cases

- **Low response rate (<50%)**: Investigate why; results may not be representative
- **Small team (<5 people)**: Don't report at team level — anonymity is compromised
- **Survey fatigue**: Reduce frequency; alternate full surveys with short pulse checks
- **Uniformly positive scores**: May indicate response bias; look at open-ended comments for nuance
