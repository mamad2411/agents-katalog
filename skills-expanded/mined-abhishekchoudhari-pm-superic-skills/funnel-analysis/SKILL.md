---
name: funnel-analysis
description: "Analyze and optimize conversion funnels — identify drop-off points, segment by user attribute, measure time-in-funnel, detect skip patterns, and produce a prioritized fix list with expected lift. Use when diagnosing where users are leaving a flow, comparing funnel performance across segments, building a conversion optimization roadmap, or instrumenting a new funnel."
---

# Funnel Analysis

Identify where users are dropping out of a conversion flow, understand why, and produce a prioritized fix list with estimated impact.

---

## Context

You are analyzing a conversion funnel for **$ARGUMENTS**.

If the user provides data files (CSV, Excel, SQL exports), read and analyze them directly. Generate Python scripts or SQL queries when needed.

---

## Part 1: Funnel Types

Choose the right funnel before collecting data. Each funnel has different conversion benchmarks.

| Funnel type | Stages | Primary question |
|---|---|---|
| Acquisition funnel | Aware → Visited → Signed up | Where does traffic fail to convert to registered users? |
| Activation funnel | Signed up → Onboarded → First value | Where do new users fail to reach the product's core value? |
| Purchase funnel | Intent → Cart/Selection → Payment → Confirmation | Where does purchase intent fail to convert to revenue? |
| Feature adoption funnel | Aware of feature → Tried → Used 3+ times | Where does feature awareness fail to produce habitual use? |
| Re-engagement funnel | Triggered (email/push) → Opened → Clicked → Converted | Where does re-engagement messaging fail to bring users back? |

---

## Part 2: Funnel Benchmarks

### Activation funnel (signup to first value)

| Step | Poor | Median | Strong |
|---|---|---|---|
| Signup to onboarding completion | <25% | 35-50% | >55% |
| Onboarding completion to first core action | <30% | 40-55% | >65% |
| Signup to first transaction | <10% | 20-35% | >45% |

### Purchase funnel (e-commerce and consumer apps)

| Step | Poor | Median | Strong |
|---|---|---|---|
| Product page to add-to-cart | <5% | 8-15% | >20% |
| Add-to-cart to checkout start | <40% | 55-70% | >80% |
| Checkout start to payment | <50% | 65-80% | >85% |
| Overall: session to transaction | <5% | 15-25% | >30% |

### Conversion benchmarks by product type

| Product type | Free to paid conversion | Notes |
|---|---|---|
| Consumer app (freemium) | 2-5% | Of MAU; top apps reach 8-10% |
| B2B SaaS (trial to paid) | 10-20% | Of trial users; PLG-driven SaaS often higher |
| Marketplace (visitor to buyer) | 1-3% | Of monthly visitors |
| Financial product (signup to funded) | 15-30% | Of completed signups |

---

## Part 3: Drop-off Analysis — Absolute vs Relative

Two different metrics, two different prioritization decisions.

**Absolute drop-off** = number of users lost at a step. Prioritize steps with highest absolute loss for revenue impact.

**Relative drop-off** = % of users who reached a step but did not complete it. Prioritize steps with highest relative drop for UX friction.

**Rule:** start with absolute drop-off for business prioritization, then use relative drop-off to validate that fixing a high-absolute step is achievable.

**Example:**

| Step | Users in | Users out | Absolute drop | Relative drop |
|---|---|---|---|---|
| Step 1: Homepage | 100,000 | 100,000 | - | - |
| Step 2: Signup started | 22,000 | 78,000 | 78,000 | 78% |
| Step 3: Email verified | 18,000 | 4,000 | 4,000 | 18% |
| Step 4: Profile completed | 11,000 | 7,000 | 7,000 | 39% |
| Step 5: First action | 8,500 | 2,500 | 2,500 | 23% |

In this example: Step 2 has by far the highest absolute drop (78,000 users). But Step 4 has the highest relative drop among users who made it past email verification (39%). Fix Step 2 first for volume, Step 4 second for quality.

---

## Part 4: Segmentation — Finding the 2x Segment

The overall funnel rarely tells the full story. The segment where conversion is 2x the average is the design blueprint for everyone else.

### Standard segmentation cuts

| Dimension | Why segment it |
|---|---|
| Device type (mobile vs desktop) | UI friction often device-specific; checkout conversion 20-40% lower on mobile |
| Acquisition channel | Organic users convert 30-50% better than paid users in most products |
| New vs returning users | New users face learning curve; returning users know the product |
| Geography | Localization, payment method, and trust signals vary by market |
| User plan / tier | Different intent and willingness to pay |
| Time of day / day of week | Conversion often 30%+ higher on weekdays for productivity tools |

### How to use segmentation findings

1. Find the segment with 2x conversion rate vs average
2. Investigate what that segment experiences differently (A/B test, session replay, user interviews)
3. Apply the insight to the underperforming segment as a test
4. Example: if desktop users convert at 32% and mobile at 11%, the 32% desktop experience is the target — redesign mobile onboarding to match it

---

## Part 5: Time-in-Funnel Analysis

The time between steps reveals whether friction is technical (fast failures) or motivational (slow hesitation).

| Time between steps | Interpretation | Action |
|---|---|---|
| <5 seconds | Automatic / habitual action, or auto-advance | Normal — no friction |
| 5 seconds to 2 minutes | Engaged consideration | Normal |
| 2-10 minutes | Reading, evaluating, or hesitating | Investigate — add social proof or simplify |
| 10+ minutes | Step was abandoned and resumed, or requires external action | Investigate — may need async support (email reminder) |
| Multiple days | User left the app and returned | Expected for high-commitment steps (payment, ID verification) |

**How to compute:** median time between events for each step pair, broken by whether the user completed the next step or churned.

**Key insight:** long median time at a step where most users convert is often not a problem (users are reading). Long median time at a step where most users churn is friction — they hesitated and left.

---

## Part 6: Skip Pattern Analysis

Users who complete step 5 without step 3 are revealing something important: step 3 may be optional, or there is an alternative path.

**How to detect:**
```sql
-- Users who completed step 5 without step 3
SELECT COUNT(DISTINCT user_id) AS skippers
FROM funnel_steps
WHERE step_5 = 1 AND step_3 = 0
```

**Interpretations:**

| Skip pattern | Interpretation |
|---|---|
| Significant % skip step 3 and still convert | Step 3 may be optional — consider making it non-blocking |
| Zero skips (perfect sequential flow) | Steps are strictly gated — any failure at one step blocks all subsequent steps |
| Users skip backward (complete step 5 then step 3) | Multi-session flow or unclear step ordering |

**Action:** remove or make optional any step that a significant % of successful users skipped, while maintaining similar conversion rates.

---

## Part 7: Fix Prioritization Matrix

After identifying all drop-off points, prioritize fixes using this matrix.

| Factor | How to score (1-3) |
|---|---|
| Drop-off volume | 1 = <1,000 users/week lost; 2 = 1,000-10,000; 3 = >10,000 |
| Business impact | 1 = secondary metric only; 2 = affects activation; 3 = directly affects revenue |
| Ease of fix | 1 = requires 2+ sprint effort; 2 = 1 sprint; 3 = <1 day (copy, UI tweak) |

**Priority score = Drop-off volume + Business impact + Ease of fix (max 9)**

| Priority | Score | Action |
|---|---|---|
| P0 | 8-9 | Fix immediately — this week |
| P1 | 6-7 | Next sprint |
| P2 | 4-5 | Backlog — schedule within quarter |
| P3 | 3 or below | Deprioritize — fix only if higher priority items are done |

---

## Part 8: Instrumentation Requirements

Before you can run this analysis, the following events must be tracked. Use this as a checklist when instrumentation is incomplete.

### Required events per step

Each funnel step needs:
- **event_name** — standardized string (snake_case recommended: `checkout_started`, not "Checkout Started")
- **user_id** — consistent identifier across sessions
- **event_timestamp** — UTC, millisecond precision preferred
- **session_id** — to group events within a session
- **step properties** — any attributes needed for segmentation (device_type, acquisition_channel, plan_tier)

### Recommended naming convention

```
[object]_[action]
Examples:
  checkout_started
  payment_submitted
  payment_succeeded
  onboarding_step_1_completed
  feature_first_used
```

Avoid event names that are ambiguous across platforms or that change meaning over time. Document every event name in a tracking plan before implementation.

---

## Part 9: SQL Template for a 5-Step Funnel

```sql
-- 5-step funnel with per-step and cumulative conversion, segmented by device type
-- Replace event names, table names, and column names to match your schema

WITH funnel_steps AS (
  SELECT
    user_id,
    device_type,
    MAX(CASE WHEN event_name = 'signup_started'           THEN 1 ELSE 0 END) AS step_1,
    MAX(CASE WHEN event_name = 'email_verified'           THEN 1 ELSE 0 END) AS step_2,
    MAX(CASE WHEN event_name = 'profile_completed'        THEN 1 ELSE 0 END) AS step_3,
    MAX(CASE WHEN event_name = 'first_feature_used'       THEN 1 ELSE 0 END) AS step_4,
    MAX(CASE WHEN event_name = 'first_transaction_completed' THEN 1 ELSE 0 END) AS step_5
  FROM events
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY) -- BigQuery
  GROUP BY user_id, device_type
),
aggregated AS (
  SELECT
    device_type,
    SUM(step_1) AS s1, SUM(step_2) AS s2, SUM(step_3) AS s3,
    SUM(step_4) AS s4, SUM(step_5) AS s5
  FROM funnel_steps
  GROUP BY device_type
)
SELECT
  device_type,
  s1 AS step_1_users,
  s2 AS step_2_users,
  s3 AS step_3_users,
  s4 AS step_4_users,
  s5 AS step_5_users,
  ROUND(s2 / NULLIF(s1, 0), 4) AS s1_to_s2,
  ROUND(s3 / NULLIF(s2, 0), 4) AS s2_to_s3,
  ROUND(s4 / NULLIF(s3, 0), 4) AS s3_to_s4,
  ROUND(s5 / NULLIF(s4, 0), 4) AS s4_to_s5,
  ROUND(s5 / NULLIF(s1, 0), 4) AS cumulative_conversion
FROM aggregated
ORDER BY device_type
```

---

## Part 10: Analysis Output Format

```
## Funnel Analysis: [Funnel Name]

**Funnel type:** [acquisition / activation / purchase / feature adoption]
**Date range:** [start to end]
**Total users entering funnel:** [N]

### Funnel table

| Step | Event name | Users | Step conversion | Cumulative conversion | Absolute drop |
|---|---|---|---|---|---|
| 1 | signup_started | 100,000 | - | 100% | - |
| 2 | ... | | | | |

### Drop-off analysis
**Highest absolute drop:** Step X — [N users] lost
**Highest relative drop:** Step Y — [%] of users who reached this step did not continue

### Segmentation findings
[Top 2-3 segments with significantly different conversion rates]

### Time-in-funnel insights
[Which step has the longest median time; interpretation]

### Skip pattern findings
[Any significant skip patterns detected]

### Fix prioritization

| Fix | Drop-off volume | Business impact | Ease | Priority score | Recommendation |
|---|---|---|---|---|---|
| | | | | | |

### Expected lift from top fix
[Estimate: if Step X conversion improves from Y% to Z%, overall funnel conversion improves by W%]
```

---

### Further Reading

- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
