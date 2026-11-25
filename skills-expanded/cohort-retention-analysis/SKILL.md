---
name: cohort-retention-analysis
description: "Analyze retention by cohort to understand how and why users stick around or leave. Moves beyond vanity metrics like MAU to actionable retention insights. Use when retention looks bad and you don't know where to focus, measuring impact of product changes, or comparing retention across segments."
---

# Cohort Retention Analysis

Understand retention by isolating who joined when and tracking what they did after.

## How to use

- `/cohort-retention-analysis` Apply cohort analysis constraints to this conversation.
- `/cohort-retention-analysis <context>` Analyze retention for the described product and data.

## Constraints

### Why Cohorts Matter
- Aggregate retention numbers lie. A growing product masks terrible retention with new users.
- MUST isolate groups by when they joined and track behavior over time
- NEVER report retention as a single aggregate number without cohort breakdown

### Cohort Types
- Time-based: weekly signup cohorts (fast products), monthly (most SaaS), quarterly (long sales cycles)
- Behavioral: users who completed onboarding vs. didn't, used Feature X vs. didn't
- Segment: by plan tier, company size, acquisition channel, geography
- SHOULD use at least two cohort types for any retention analysis

### Retention Metrics
- User retention: did they come back? (Day 1, 7, 14, 30, 60, 90)
- Revenue retention: did they keep paying? NRR includes expansion; GRR only contraction and churn.
- Activity retention: did they do the core action? (Define what "active" actually means)
- MUST pick the metric that matches your product type. "Active" for a chat tool is different than a tax tool.

### Curve Shape Interpretation
- Steep early drop then flattens: normal. Focus on getting more people past the initial drop.
- Gradual continuous decline: dangerous. Product delivers diminishing value over time.
- Flattens then drops again: something triggers later churn. Investigate the inflection point.
- Newer cohorts retain better: product or onboarding is improving.
- Newer cohorts retain worse: product-market fit may be weakening or user quality declining.

### Diagnosing Drop-Off Points
- Day 0-1 drop: onboarding too complex? Aha moment not reached?
- Day 1-7 drop: no reason to return? No habit loops?
- Day 7-30 drop: novelty wore off? Hitting plan limitations?
- Day 30+ drop: product not delivering ongoing value? Competitor pulling them away?
- MUST compare cohorts to find what drives differences, not just observe the drops

### Anti-Patterns
- Reporting DAU/MAU without cohort context
- Averaging retention across segments that behave completely differently
- Measuring only one retention metric when multiple views tell different stories
- Ignoring that improving one stage can sometimes hurt a later stage
