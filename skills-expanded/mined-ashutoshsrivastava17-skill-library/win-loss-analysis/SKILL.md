---
name: win-loss-analysis
description: >
  Analyze won and lost deals to identify patterns — competitive factors, pricing,
  timing, process gaps, and product feedback for strategic improvement.
  TRIGGER when: user says /win-loss-analysis, "why did we lose", "why did we win",
  "deal analysis patterns", "win rate analysis", or "loss review".
argument-hint: "[deal set, time period, or segment to analyze]"
user-invocable: true
---

# Win/Loss Analysis

You are a sales strategy analyst examining patterns in won and lost deals. Extract actionable insights to improve win rates, competitive positioning, and sales process.

## Process

### Step 1: Define Analysis Scope

| Parameter | Description |
|-----------|-------------|
| Time period | Deals closed in last quarter/half/year |
| Segments | By product, market, deal size, rep, region |
| Data sources | CRM, buyer interviews, rep debriefs, competitor intel |
| Sample size | All deals or representative sample |

### Step 2: Win/Loss Metrics

| Metric | Won | Lost | No Decision | Benchmark |
|--------|-----|------|------------|-----------|
| Count | | | | |
| Total value | | | | |
| Average deal size | | | | |
| Average sales cycle | | | | |
| Win rate | | | | Industry avg |

### Step 3: Factor Analysis

| Factor | Won (% mentioned) | Lost (% mentioned) | Insight |
|--------|-------------------|-------------------|---------|
| Product capability | | | |
| Pricing / value | | | |
| Competitive preference | | | |
| Relationship / trust | | | |
| Sales process / responsiveness | | | |
| Technical fit | | | |
| Implementation / support | | | |
| Timing / urgency | | | |
| Internal champion | | | |

### Step 4: Competitive Analysis

| Competitor | Deals Lost To | Primary Reasons | Our Weakness | Action |
|-----------|-------------|----------------|-------------|--------|
| [Competitor] | N deals ($Xk) | [Top reasons] | [Gap] | [How to address] |

### Step 5: Insights and Recommendations

| Category | Finding | Evidence | Recommendation | Owner |
|----------|---------|----------|---------------|-------|
| Product | [Gap or strength] | [Data] | [Action] | [Team] |
| Process | [Gap or strength] | [Data] | [Action] | [Team] |
| Pricing | [Gap or strength] | [Data] | [Action] | [Team] |
| Enablement | [Gap or strength] | [Data] | [Action] | [Team] |

## Output Format

```markdown
## Win/Loss Analysis: [Period]

### Summary
- Win rate: X% (N deals won / M total)
- Top win factor: [Factor]
- Top loss factor: [Factor]
- Biggest competitive threat: [Competitor]

### Win Rate by Segment
[Breakdown tables]

### Key Factors
[Factor analysis with data]

### Competitive Insights
[Competitor comparison]

### Recommendations
| Priority | Action | Expected Impact | Owner |

### Data Gaps
[Where more buyer feedback is needed]
```

## Quality Checklist

- [ ] Analysis includes both won and lost deals for comparison
- [ ] Findings are backed by data, not anecdotes
- [ ] Competitive patterns are identified with specific remediation
- [ ] Recommendations span product, process, and enablement
- [ ] "No decision" outcomes are analyzed separately
- [ ] Buyer feedback (not just rep opinion) is incorporated where possible

## Edge Cases

- **Small sample size**: Flag statistical limitations; focus on qualitative patterns
- **New market entry**: Compare to analogous markets; adjust expectations
- **Enterprise vs. SMB**: Analyze separately — different dynamics
- **Channel deals**: Include partner effectiveness as a factor
