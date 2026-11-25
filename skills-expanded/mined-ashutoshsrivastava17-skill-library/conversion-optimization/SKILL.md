---
name: conversion-optimization
description: >
  Optimize conversion rates — funnel analysis, hypothesis generation, test design, landing page review, CTA optimization, and results analysis.
  TRIGGER when: user says /conversion-optimization, needs to improve conversion rates, or asks about CRO and A/B testing.
argument-hint: "[relevant context]"
user-invocable: true
---

# Conversion Optimization
## Process
### Step 1: Map the Funnel
| Stage | Page/Step | Current Rate | Benchmark |
|-------|----------|-------------|-----------|
| Visit → Engage | Landing page | X% | X% |
| Engage → Lead | Form/CTA | X% | X% |
| Lead → Qualify | Nurture sequence | X% | X% |
| Qualify → Convert | Purchase/sign-up | X% | X% |
### Step 2: Identify Drop-Off Points
| Signal | Analysis Method |
|--------|---------------|
| High bounce rate | Landing page relevance, load speed |
| Form abandonment | Form analytics, field analysis |
| Cart abandonment | Checkout flow analysis |
| Pricing page exit | Pricing clarity, comparison |
### Step 3: Generate Hypotheses
For each drop-off:
```
IF we [change], THEN [metric] will [improve] BECAUSE [reason].
Priority: Impact (H/M/L) × Confidence (H/M/L) × Ease (H/M/L)
```
### Step 4: Design Tests
| Element | Test Type | Variants |
|---------|----------|---------|
| Headlines | A/B | 2-3 variants |
| CTA text/color | A/B | 2 variants |
| Page layout | A/B | 2 variants |
| Form length | A/B | Short vs long |
| Social proof | A/B | With vs without |
| Pricing display | A/B | Monthly vs annual first |
### Step 5: Run and Analyze
| Metric | Control | Variant | Lift | Significance |
|--------|---------|---------|------|-------------|
| Conversion rate | X% | X% | +X% | p = X |
| Revenue/visitor | $X | $X | +X% | p = X |
### Step 6: Implement Winners
- Ship winning variants to 100%
- Document learnings for future tests
- Move to next priority hypothesis
- Track cumulative impact over time
## Output Format
```markdown
## CRO Report: [Page/Flow]
### Funnel: [Current rates by stage]
### Opportunities: [Prioritized hypotheses]
### Test Results: [Results table]
### Impact: [Cumulative conversion lift]
```
## Quality Checklist
- [ ] Funnel mapped with current conversion rates
- [ ] Hypotheses prioritized by impact × confidence × ease
- [ ] Tests have adequate sample size for statistical significance
- [ ] Results analyzed correctly (avoid peeking)
- [ ] Winning changes documented and shipped
## Edge Cases
- For low-traffic sites, use qualitative methods (user testing, heatmaps) instead of A/B tests
- For B2B with long sales cycles, track micro-conversions
- If running multiple tests, ensure no interaction effects
