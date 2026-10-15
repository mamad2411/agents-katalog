---
name: segmentation-analysis
description: Use when grouping customers or users into actionable segments and the AI should define thresholds, profiles, and differentiated actions.
source: perlytics-skill
version: 1.0.0
---

# Segmentation Analysis

## Purpose

Identify and characterize meaningful groups in a population in ways that support different decisions for each group.

## When to use

Use this skill when:

- asked "who are our best customers?" or "how do we group our users?"
- building targeting lists for different campaigns, offers, or interventions
- conducting RFM (Recency, Frequency, Monetary) analysis
- evaluating whether different customer segments have different needs or behaviors
- deciding which users to prioritize for retention, upsell, or onboarding attention

## When not to use

Do not use this skill when:

- the goal is to understand why a KPI changed (use `root-cause-analysis`)
- the goal is to predict future behavior for individual entities (requires a predictive model)
- segments are already defined and documented - just apply them rather than re-deriving

## Required thinking discipline

- A segment is only useful if you would do something different for each group. If the action is the same for all groups, the segmentation adds no value.
- Define the decision use case before defining the segments. Segments derived backward from a decision question are more actionable than segments derived from data patterns alone.
- Validate segment stability. A segmentation scheme that reclassifies 60% of customers month over month is operationally unusable.
- Name segments by behavior, not by rank. "High-value retained buyers" is more actionable than "Tier 1."
- **Evidence constraint:** Every conclusion must cite specific data — a number, a rate, a segment, or a timeframe. Do not speculate without evidential basis. If data is insufficient, state what is missing rather than asserting an unsupported inference.

## Workflow

1. **Define the decision use case:** Why are we segmenting? What action will differ by segment? (Examples: different email cadences, different onboarding tracks, different discount thresholds, different retention interventions.)

2. **Choose the segmentation basis:**
   - **Behavioral:** what the entity does (purchase frequency, feature usage, engagement level, product mix)
   - **RFM:** Recency (when did they last transact?), Frequency (how often?), Monetary (how much value?)
   - **Attribute-based:** firmographic (industry, size, geography), demographic, plan type
   - **Lifecycle stage:** new, active, at-risk, churned, reactivated

3. **Define the time window and entity scope:** Which time period defines the behavioral signals? Are we segmenting all users, or a specific cohort?

4. **Assign entities to segments:** Define the boundaries clearly - use explicit thresholds rather than vague labels. Example: "Frequent" = 4+ purchases in the last 90 days, not "more than average."

5. **Characterize each segment:** For each group, describe:
   - Size (count and % of population)
   - Key behavioral metrics (average revenue, frequency, recency, product usage)
   - Distinguishing characteristics compared to other segments
   - What makes this group different and why it matters

6. **Validate segment stability:** Check whether segment membership is consistent across two or three comparable time periods. High churn between segments indicates the boundaries are noisy or the time window is too short.

7. **Map segments to actions:** State explicitly what you would do differently for each segment. If the action is the same, merge the segments.

## Output format

- Decision use case and segmentation basis
- Segment definitions (explicit thresholds or rules)
- Segment profiles table (size, key metrics, distinguishing behaviors)
- Stability assessment
- Action mapping (what is different for each segment)
- Recommended monitoring cadence

## Good example

Segmentation basis: RFM for ecommerce customer base, last 12 months.

| Segment | Definition | Size | Avg Revenue | Avg Orders | Action |
|---|---|---|---|---|---|
| Champions | R <= 30d, F >= 6, M top 20% | 8% | $890 | 9.2 | Loyalty reward, early access |
| At-Risk High Value | R 61-120d, F >= 4, M top 30% | 6% | $640 | 5.1 | Win-back campaign, discount offer |
| New Customers | R <= 30d, F = 1 | 22% | $110 | 1.0 | Onboarding sequence, second purchase nudge |
| Dormant | R > 180d | 31% | $95 | 1.4 | Low-cost reactivation or suppress |

Stability check: 84% of Champions retained segment membership month over month. Segment boundaries are stable.

## Bad example

> Our customers can be grouped into High, Medium, and Low.

Why this is bad:

- no definition of what "high," "medium," and "low" mean behaviorally
- no thresholds - who exactly falls into each group?
- no stability check
- no action mapping - what would you do differently for each group?
- the segmentation is not connected to any decision

## Practical notes

- RFM is the most robust entry point for ecommerce segmentation because all three dimensions are directly actionable.
- For B2B SaaS, account health score (combining login recency, feature adoption, support tickets) often works better than transactional RFM.
- Segment count should reflect the number of distinct actions you can actually execute - if you can only run two campaigns, four segments add no value over two.
- When presenting segments to a business team, name them descriptively (Champions, At-Risk, New) rather than with cluster IDs (Segment 0, Segment 1) - the names signal the action.

## Optional variants

- **RFM (ecommerce):** use recency, frequency, and monetary value with explicit quantile thresholds. Standard output is a 3x3 or 5x5 grid.
- **Product engagement tiers (SaaS):** use feature adoption depth, session frequency, and time-to-value as the behavioral signals. Tie segments to onboarding and expansion playbooks.
- **Account health scoring (B2B):** combine product usage, stakeholder engagement, support volume, and contract signals into a composite score. Map to customer success intervention triggers.
- **Lifecycle segmentation:** new, active, at-risk, churned, reactivated. Useful when retention is the primary objective and behavioral signals are less granular.
