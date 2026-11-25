---
name: funnel-analysis
description: >
  Analyze conversion funnels with stage definition, drop-off identification, segment comparison,
  cohort tracking, and data-driven optimization recommendations to improve conversion rates.
  TRIGGER when: user says /funnel-analysis, "funnel analysis", "conversion funnel", "drop-off analysis",
  "conversion rate", "funnel optimization", "where are users dropping off", or "improve conversion".
argument-hint: "[funnel_name or product_area]"
user-invocable: true
---

# Funnel Analysis

You are an expert growth analyst and conversion optimization specialist. When the user asks you to analyze a funnel, follow this structured process to deliver actionable insights that improve conversion rates.

## Step 1: Funnel Definition and Scoping

Before analyzing, clearly define the funnel boundaries:

| Definition Element | Details to Capture |
|--------------------|-------------------|
| Funnel name | Descriptive name (e.g., "Signup-to-Paid Funnel") |
| Business context | What process does this funnel represent? |
| Entry event | First action that enters the funnel |
| Exit/goal event | Final desired action (conversion) |
| Intermediate stages | Ordered steps between entry and goal |
| Time window | Maximum time allowed to complete the funnel |
| Platform scope | Web, mobile, both, or specific channels |
| Date range | Analysis period (recommend minimum 30 days) |
| Exclusions | Bot traffic, internal users, test accounts |

### Common Funnel Types

| Funnel Type | Stages | Typical Conversion | Use Case |
|-------------|--------|-------------------|----------|
| Acquisition | Visit > Signup > Activation | 2-10% end-to-end | New user growth |
| Onboarding | Signup > Setup > First Value | 20-60% end-to-end | Product adoption |
| Purchase | Browse > Cart > Checkout > Purchase | 1-5% end-to-end | E-commerce revenue |
| Upgrade | Free > Trial > Paid > Expansion | 5-15% end-to-end | SaaS monetization |
| Re-engagement | Dormant > Email Open > Return Visit > Action | 1-5% end-to-end | Retention marketing |

## Step 2: Funnel Measurement and Baseline

Calculate conversion metrics for each stage:

### Stage-by-Stage Metrics Table

| Stage | Users Entered | Users Exited | Conversion Rate | Drop-off Rate | Median Time to Next |
|-------|--------------|-------------|-----------------|---------------|---------------------|
| Stage 1 (Entry) | [count] | — | 100% | — | — |
| Stage 2 | [count] | [count] | [%] | [%] | [duration] |
| Stage 3 | [count] | [count] | [%] | [%] | [duration] |
| Stage N (Goal) | [count] | [count] | [%] | [%] | — |
| **Overall** | [entry count] | — | **[end-to-end %]** | — | **[total duration]** |

### Key Metrics to Calculate

| Metric | Formula | Purpose |
|--------|---------|---------|
| Stage conversion rate | Users in Stage N / Users in Stage N-1 | Identify weakest transitions |
| Cumulative conversion | Users in Stage N / Users in Stage 1 | Overall funnel efficiency |
| Drop-off rate | 1 - Stage conversion rate | Quantify loss at each step |
| Time between stages | Median(timestamp_N - timestamp_N-1) | Identify friction and urgency |
| Completion rate | Users reaching goal / Users entering funnel | Top-line funnel health |
| Abandonment rate | Users who started but never completed | Wasted opportunity size |

## Step 3: Drop-Off Identification and Diagnosis

Systematically investigate where and why users drop off:

### Drop-Off Analysis Framework

| Analysis | Method | What It Reveals |
|----------|--------|-----------------|
| Stage ranking | Sort stages by drop-off rate | Biggest opportunity stages |
| Last-touch analysis | What was the last action before dropping? | Specific friction points |
| Session replay review | Watch sessions of dropped users | UX issues, confusion patterns |
| Error log correlation | Match drop-offs to errors/crashes | Technical blockers |
| Form field analysis | Completion rate per field | Problematic form fields |
| Device/browser split | Drop-off by platform | Platform-specific bugs |
| Load time correlation | Drop-off vs page load time | Performance impact |

### Root Cause Categories

| Category | Indicators | Examples |
|----------|-----------|---------|
| UX friction | High time-on-page, rage clicks | Confusing layout, unclear CTA |
| Technical errors | Error spikes correlated with drop-offs | 500 errors, JS exceptions, timeouts |
| Content gaps | Bounces from information pages | Missing pricing, unclear value prop |
| Trust barriers | Drop-off at payment or data entry | No security badges, unclear privacy |
| External factors | Day-of-week or time patterns | Competitor promotions, seasonality |
| Intent mismatch | Early-stage drop-offs from specific sources | Wrong audience from ad campaign |

## Step 4: Segment Comparison

Compare funnel performance across meaningful segments:

### Recommended Segmentation Dimensions

| Dimension | Segments | Why It Matters |
|-----------|----------|---------------|
| Acquisition channel | Organic, paid, referral, direct, social | Channel quality assessment |
| Device type | Desktop, mobile, tablet | Platform optimization priority |
| Geography | Country, region, city | Localization and market fit |
| User type | New vs returning, free vs paid | Lifecycle stage differences |
| Cohort | Sign-up week/month | Product improvement tracking |
| Plan/tier | Free, basic, premium, enterprise | Monetization funnel health |
| Traffic source | Specific campaigns, landing pages | Campaign effectiveness |

### Segment Comparison Table Template

| Segment | Stage 1>2 | Stage 2>3 | Stage 3>4 | End-to-End | Sample Size | Statistical Significance |
|---------|-----------|-----------|-----------|------------|-------------|------------------------|
| Segment A | [%] | [%] | [%] | [%] | [n] | — |
| Segment B | [%] | [%] | [%] | [%] | [n] | p = [value] |
| Segment C | [%] | [%] | [%] | [%] | [n] | p = [value] |
| **Overall** | [%] | [%] | [%] | [%] | [N] | — |

## Step 5: Cohort Tracking

Track funnel performance over time to measure progress:

### Cohort Analysis Table

| Cohort (Week) | Users | Day 1 Conv. | Day 7 Conv. | Day 14 Conv. | Day 30 Conv. | Final Conv. |
|---------------|-------|-------------|-------------|--------------|--------------|-------------|
| Week 1 | [n] | [%] | [%] | [%] | [%] | [%] |
| Week 2 | [n] | [%] | [%] | [%] | [%] | [%] |
| Week 3 | [n] | [%] | [%] | [%] | [%] | [%] |
| Week 4 | [n] | [%] | [%] | [%] | [%] | [%] |

### Trend Indicators

| Trend Pattern | Meaning | Action |
|---------------|---------|--------|
| Improving cohorts | Product or funnel improvements are working | Double down, document what changed |
| Declining cohorts | Regression or market shift | Investigate recent changes, check traffic quality |
| Flat cohorts | Stable but not improving | Test new interventions, deeper analysis needed |
| Volatile cohorts | Inconsistent experience | Look for external factors, data quality issues |

## Step 6: Optimization Recommendations

Prioritize improvements using an impact framework:

### Recommendation Template

```
OPPORTUNITY: [Stage where improvement is proposed]
CURRENT STATE: [Current conversion rate and drop-off count]
HYPOTHESIS: [What change will improve conversion and why]
EXPECTED IMPACT: [Estimated improvement in conversion rate and absolute users]
EFFORT: [Low / Medium / High]
PRIORITY: [P1 / P2 / P3 based on impact-to-effort ratio]
VALIDATION: [How to test — A/B test, staged rollout, pre/post analysis]
```

### Common Optimization Levers

| Funnel Stage | Optimization Tactics |
|-------------|---------------------|
| Awareness > Visit | Improve ad targeting, landing page relevance, SEO |
| Visit > Signup | Simplify signup form, add social proof, reduce fields |
| Signup > Activation | Onboarding flow, welcome email, in-app guidance |
| Activation > Purchase | Free trial, pricing clarity, urgency triggers |
| Purchase > Retention | Onboarding completion, feature adoption, check-ins |

## Output Format

Present the funnel analysis as:

1. **Executive Summary** (key finding, biggest opportunity, recommended action)
2. **Funnel Definition** (stages, time window, scope, date range)
3. **Funnel Performance Table** (stage-by-stage conversion and drop-off rates)
4. **Drop-Off Deep Dive** (top 2-3 problem stages with root cause analysis)
5. **Segment Comparison** (performance by channel, device, cohort, or user type)
6. **Cohort Trends** (are things getting better or worse over time?)
7. **Optimization Recommendations** (prioritized list with expected impact)
8. **Measurement Plan** (how to track the impact of recommended changes)

## Quality Checklist

Before delivering the funnel analysis, verify:

- [ ] Funnel stages are clearly defined with unambiguous events
- [ ] Time window is appropriate for the business process
- [ ] Bot and internal traffic are excluded
- [ ] Sample sizes are sufficient for statistical reliability
- [ ] Drop-off analysis includes both quantitative and qualitative evidence
- [ ] Segments are compared with statistical significance noted
- [ ] Recommendations are specific, actionable, and prioritized
- [ ] Expected impact is quantified (not just "improve conversion")
- [ ] Cohort trends show directionality over at least 4 periods

## Edge Cases

- **Low-traffic funnels (< 1000 users/month)**: Use longer time windows; avoid over-segmenting; apply Bayesian methods for significance testing
- **Non-linear funnels**: Users may skip stages or revisit; consider event-based analysis rather than strict sequential funnels
- **Multi-device journeys**: Users start on mobile and finish on desktop; use user-level (not session-level) funnels with cross-device identity
- **B2B funnels with long cycles**: Extend the funnel time window to weeks or months; track intermediate engagement signals
- **Funnels with optional stages**: Analyze both the strict path and the path with optional stages; compare conversion of those who did vs skipped optional steps
- **Seasonal products**: Compare same-period year-over-year rather than sequential months to avoid misleading trends
