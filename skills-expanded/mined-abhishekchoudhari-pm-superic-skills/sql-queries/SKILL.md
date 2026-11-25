---
name: sql-queries
description: "Generate production-ready SQL queries for product analytics — DAU/MAU, retention cohorts, funnels, feature adoption, growth accounting, NPS, revenue cohorts, power users, A/B test results, and ARPU by segment. Supports BigQuery, Snowflake, Redshift, and PostgreSQL. Use when writing SQL, translating a business question into a query, optimizing existing queries, or building reusable analytics patterns."
---

# SQL Queries for Product Analytics

Generate production-ready SQL for the most important product analytics questions. Every pattern includes annotations, dialect notes, and optimization guidance.

---

## Context

You are writing SQL for **$ARGUMENTS**.

Default dialect: BigQuery. Specify Snowflake, Redshift, or PostgreSQL if different.

If the user provides a schema file or describes their table structure, use actual table and column names. Otherwise use generic names (events, users, sessions) and note where substitution is needed.

---

## Part 1: 10 Production-Ready SQL Patterns

---

### Pattern 1: DAU/MAU Ratio (Engagement Quality Metric)

DAU/MAU ratio measures whether your active user base actually uses the product daily. A ratio above 20% is healthy for a daily-use app; above 30% is strong.

```sql
-- DAU/MAU ratio by day
-- Replace 'events' with your events table and 'user_id', 'event_date' with your column names
-- BigQuery / Snowflake / Redshift compatible

WITH daily_active AS (
  SELECT
    event_date,
    COUNT(DISTINCT user_id) AS dau
  FROM events
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) -- BigQuery syntax
  -- Snowflake: DATEADD(day, -90, CURRENT_DATE())
  -- Redshift: CURRENT_DATE - 90
  GROUP BY 1
),
monthly_active AS (
  SELECT
    DATE_TRUNC(event_date, MONTH) AS month_start, -- BigQuery
    -- Snowflake/Redshift: DATE_TRUNC('month', event_date)
    COUNT(DISTINCT user_id) AS mau
  FROM events
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  GROUP BY 1
)
SELECT
  d.event_date,
  d.dau,
  m.mau,
  ROUND(d.dau / m.mau, 4) AS dau_mau_ratio
FROM daily_active d
LEFT JOIN monthly_active m
  ON DATE_TRUNC(d.event_date, MONTH) = m.month_start
ORDER BY 1

-- Benchmarks: >0.20 healthy (daily-use app), >0.30 strong, <0.10 weak
```

---

### Pattern 2: Retention Cohort Matrix

The most important retention query. Produces a cohort x period heatmap where each cell = % of the cohort active in that period.

```sql
-- Monthly retention cohort matrix
-- Assumes: users table with (user_id, activation_date), events table with (user_id, event_date)
-- Activation event = first meaningful action, not just signup

WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC(activation_date, MONTH) AS cohort_month -- BigQuery
    -- Snowflake/Redshift: DATE_TRUNC('month', activation_date)
  FROM users
  WHERE activation_date IS NOT NULL
),
cohort_activity AS (
  SELECT
    c.user_id,
    c.cohort_month,
    DATE_TRUNC(e.event_date, MONTH) AS activity_month,
    DATE_DIFF(DATE_TRUNC(e.event_date, MONTH), c.cohort_month, MONTH) AS months_since_activation
    -- Snowflake: DATEDIFF('month', c.cohort_month, DATE_TRUNC('month', e.event_date))
    -- Redshift: DATEDIFF(month, c.cohort_month, DATE_TRUNC('month', e.event_date))
  FROM cohorts c
  JOIN events e ON c.user_id = e.user_id
  WHERE e.event_date >= c.cohort_month -- only post-activation activity
),
cohort_sizes AS (
  SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_size
  FROM cohorts
  GROUP BY 1
)
SELECT
  a.cohort_month,
  cs.cohort_size,
  a.months_since_activation AS period,
  COUNT(DISTINCT a.user_id) AS retained_users,
  ROUND(COUNT(DISTINCT a.user_id) / cs.cohort_size, 4) AS retention_rate
FROM cohort_activity a
JOIN cohort_sizes cs ON a.cohort_month = cs.cohort_month
WHERE a.months_since_activation BETWEEN 0 AND 12
GROUP BY 1, 2, 3
ORDER BY 1, 3

-- Pivot in your BI tool (Looker, Metabase, Mode) to get the heatmap view
-- D30 >20% for B2C is strong; SaaS monthly retention >94% is strong
```

---

### Pattern 3: Funnel Conversion Rates

Computes step-by-step and cumulative conversion through a multi-step funnel.

```sql
-- 5-step funnel: adjust event names and step count for your funnel
-- Assumes events table with (user_id, event_name, event_timestamp)
-- Each step is defined by completing a specific event

WITH funnel_steps AS (
  SELECT
    user_id,
    MAX(CASE WHEN event_name = 'signup_started' THEN 1 ELSE 0 END) AS step_1,
    MAX(CASE WHEN event_name = 'email_verified' THEN 1 ELSE 0 END) AS step_2,
    MAX(CASE WHEN event_name = 'profile_completed' THEN 1 ELSE 0 END) AS step_3,
    MAX(CASE WHEN event_name = 'first_feature_used' THEN 1 ELSE 0 END) AS step_4,
    MAX(CASE WHEN event_name = 'first_transaction_completed' THEN 1 ELSE 0 END) AS step_5
  FROM events
  WHERE event_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY) -- BigQuery
  GROUP BY user_id
),
funnel_counts AS (
  SELECT
    SUM(step_1) AS s1_users,
    SUM(step_2) AS s2_users,
    SUM(step_3) AS s3_users,
    SUM(step_4) AS s4_users,
    SUM(step_5) AS s5_users
  FROM funnel_steps
)
SELECT
  'Step 1: Signup Started' AS step,
  s1_users AS users,
  1.0 AS step_conversion,
  1.0 AS cumulative_conversion
FROM funnel_counts
UNION ALL
SELECT 'Step 2: Email Verified', s2_users,
  ROUND(s2_users / NULLIF(s1_users, 0), 4),
  ROUND(s2_users / NULLIF(s1_users, 0), 4)
FROM funnel_counts
UNION ALL
SELECT 'Step 3: Profile Completed', s3_users,
  ROUND(s3_users / NULLIF(s2_users, 0), 4),
  ROUND(s3_users / NULLIF(s1_users, 0), 4)
FROM funnel_counts
UNION ALL
SELECT 'Step 4: First Feature Used', s4_users,
  ROUND(s4_users / NULLIF(s3_users, 0), 4),
  ROUND(s4_users / NULLIF(s1_users, 0), 4)
FROM funnel_counts
UNION ALL
SELECT 'Step 5: First Transaction', s5_users,
  ROUND(s5_users / NULLIF(s4_users, 0), 4),
  ROUND(s5_users / NULLIF(s1_users, 0), 4)
FROM funnel_counts

-- The step with largest absolute drop (not just % drop) is the priority
```

---

### Pattern 4: Feature Adoption Rate

Measures what % of users activated a specific feature within N days of signup.

```sql
-- Feature adoption: % of users who used feature X within 30 days of activation
-- Replace 'feature_used_event' with your specific feature event name

WITH user_cohort AS (
  SELECT user_id, activation_date
  FROM users
  WHERE activation_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) -- last 90 days of cohorts
),
feature_adoption AS (
  SELECT DISTINCT e.user_id
  FROM events e
  JOIN user_cohort u ON e.user_id = u.user_id
  WHERE e.event_name = 'feature_used_event'
    AND e.event_date <= DATE_ADD(u.activation_date, INTERVAL 30 DAY)
    AND e.event_date >= u.activation_date
)
SELECT
  COUNT(DISTINCT uc.user_id) AS total_users,
  COUNT(DISTINCT fa.user_id) AS adopted_users,
  ROUND(COUNT(DISTINCT fa.user_id) / COUNT(DISTINCT uc.user_id), 4) AS adoption_rate_30d
FROM user_cohort uc
LEFT JOIN feature_adoption fa ON uc.user_id = fa.user_id

-- Benchmark: 10-20% breadth in 30 days = healthy for non-core features
-- Core features should reach 50%+ within 90 days
```

---

### Pattern 5: Growth Accounting

Classifies every user by their state each week: new, retained, resurrected, or churned.

```sql
-- Weekly growth accounting: new, retained, resurrected, churned
-- Dormancy threshold: 4 weeks (adjust to 8+ weeks for lower-frequency products)

WITH weekly_active AS (
  SELECT
    user_id,
    DATE_TRUNC(event_date, WEEK) AS week -- BigQuery; use DATE_TRUNC('week', event_date) in Snowflake/Redshift
  FROM events
  GROUP BY 1, 2
),
user_weeks AS (
  SELECT
    w1.user_id,
    w1.week AS current_week,
    w0.week AS prev_week,
    CASE
      WHEN w0.week IS NULL AND w1.week IS NOT NULL THEN 'new'
      -- Check if user was active 1 week ago = retained
      WHEN DATE_DIFF(w1.week, w0.week, WEEK) = 1 THEN 'retained' -- BigQuery
      -- Snowflake/Redshift: DATEDIFF('week', w0.week, w1.week) = 1
      ELSE 'resurrected'
    END AS user_state
  FROM weekly_active w1
  LEFT JOIN weekly_active w0
    ON w1.user_id = w0.user_id
    AND DATE_DIFF(w1.week, w0.week, WEEK) = 1 -- most recent prior active week
    -- Note: for true "resurrected" you need to check the last active week, not just prev week
    -- This simplified version classifies any non-consecutive returner as resurrected
),
churned AS (
  -- Users active last week but not this week
  SELECT
    w0.user_id,
    DATE_ADD(w0.week, INTERVAL 1 WEEK) AS current_week,
    'churned' AS user_state
  FROM weekly_active w0
  WHERE NOT EXISTS (
    SELECT 1 FROM weekly_active w1
    WHERE w1.user_id = w0.user_id
    AND w1.week = DATE_ADD(w0.week, INTERVAL 1 WEEK)
  )
)
SELECT
  current_week,
  user_state,
  COUNT(DISTINCT user_id) AS users
FROM (SELECT user_id, current_week, user_state FROM user_weeks
      UNION ALL
      SELECT user_id, current_week, user_state FROM churned)
GROUP BY 1, 2
ORDER BY 1, 2

-- Quick ratio = (new + resurrected) / churned
-- >4: hyper-growth; 2-4: healthy; 1-2: struggling; <1: shrinking
```

---

### Pattern 6: NPS Score Calculation

Calculates NPS from survey response data.

```sql
-- NPS calculation from survey responses
-- Assumes: nps_surveys table with (user_id, survey_date, score [0-10])

WITH categorized AS (
  SELECT
    survey_date,
    user_id,
    score,
    CASE
      WHEN score >= 9 THEN 'promoter'
      WHEN score >= 7 THEN 'passive'
      ELSE 'detractor'
    END AS category
  FROM nps_surveys
  WHERE survey_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),
monthly_nps AS (
  SELECT
    DATE_TRUNC(survey_date, MONTH) AS month,
    COUNT(*) AS total_responses,
    COUNTIF(category = 'promoter') AS promoters, -- BigQuery
    -- Snowflake/Redshift: SUM(CASE WHEN category = 'promoter' THEN 1 ELSE 0 END)
    COUNTIF(category = 'detractor') AS detractors
  FROM categorized
  GROUP BY 1
)
SELECT
  month,
  total_responses,
  promoters,
  detractors,
  ROUND((promoters - detractors) / total_responses * 100, 1) AS nps_score
FROM monthly_nps
ORDER BY 1

-- NPS benchmarks: >50 excellent, 30-50 good, 0-30 needs improvement, <0 critical
```

---

### Pattern 7: Revenue Cohort Analysis

Shows revenue generated by each signup cohort over time — reveals LTV trajectory.

```sql
-- Monthly revenue by signup cohort
-- Assumes: users (user_id, signup_date), transactions (user_id, transaction_date, revenue)

WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC(signup_date, MONTH) AS cohort_month
  FROM users
),
cohort_revenue AS (
  SELECT
    c.cohort_month,
    DATE_TRUNC(t.transaction_date, MONTH) AS revenue_month,
    DATE_DIFF(DATE_TRUNC(t.transaction_date, MONTH), c.cohort_month, MONTH) AS months_since_signup,
    SUM(t.revenue) AS revenue,
    COUNT(DISTINCT t.user_id) AS paying_users
  FROM cohorts c
  JOIN transactions t ON c.user_id = t.user_id
  GROUP BY 1, 2, 3
),
cohort_sizes AS (
  SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_size
  FROM cohorts
  GROUP BY 1
)
SELECT
  r.cohort_month,
  cs.cohort_size,
  r.months_since_signup AS period,
  r.revenue,
  r.paying_users,
  ROUND(r.revenue / cs.cohort_size, 2) AS revenue_per_cohort_user,
  ROUND(r.paying_users / cs.cohort_size, 4) AS paying_rate
FROM cohort_revenue r
JOIN cohort_sizes cs ON r.cohort_month = cs.cohort_month
WHERE r.months_since_signup BETWEEN 0 AND 12
ORDER BY 1, 3
```

---

### Pattern 8: Power User Identification

Identifies the top 10% of users by engagement — these are the users whose behavior defines product success.

```sql
-- Power users: top 10% by session count in last 30 days
-- Assumes: sessions table with (user_id, session_date, session_duration_seconds)

WITH user_engagement AS (
  SELECT
    user_id,
    COUNT(*) AS session_count,
    SUM(session_duration_seconds) AS total_session_seconds,
    COUNT(DISTINCT session_date) AS active_days,
    MAX(session_date) AS last_active_date
  FROM sessions
  WHERE session_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY 1
),
percentiles AS (
  SELECT
    user_id,
    session_count,
    total_session_seconds,
    active_days,
    last_active_date,
    PERCENT_RANK() OVER (ORDER BY session_count) AS engagement_percentile
  FROM user_engagement
)
SELECT
  user_id,
  session_count,
  ROUND(total_session_seconds / 60, 1) AS total_minutes,
  active_days,
  last_active_date,
  ROUND(engagement_percentile * 100, 1) AS percentile
FROM percentiles
WHERE engagement_percentile >= 0.9 -- top 10%
ORDER BY session_count DESC

-- Use this list for: user interviews, beta testing, feature co-design
```

---

### Pattern 9: A/B Test Result Query

Computes conversion rates and a normal approximation confidence interval for each variant.

```sql
-- A/B test results: conversion rate + 95% CI approximation
-- Assumes: experiment_assignments (user_id, variant, assignment_date),
--          conversions (user_id, conversion_date, converted [0/1])

WITH experiment_data AS (
  SELECT
    ea.variant,
    COUNT(DISTINCT ea.user_id) AS total_users,
    COUNT(DISTINCT CASE WHEN c.converted = 1 THEN ea.user_id END) AS converted_users
  FROM experiment_assignments ea
  LEFT JOIN conversions c
    ON ea.user_id = c.user_id
    AND c.conversion_date >= ea.assignment_date
  WHERE ea.assignment_date BETWEEN '2025-01-01' AND '2025-01-31' -- replace with test dates
  GROUP BY 1
)
SELECT
  variant,
  total_users,
  converted_users,
  ROUND(converted_users / total_users, 4) AS conversion_rate,
  -- 95% CI using normal approximation (Wilson interval is more accurate for low rates)
  ROUND(converted_users / total_users - 1.96 * SQRT(
    (converted_users / total_users) * (1 - converted_users / total_users) / total_users
  ), 4) AS ci_lower,
  ROUND(converted_users / total_users + 1.96 * SQRT(
    (converted_users / total_users) * (1 - converted_users / total_users) / total_users
  ), 4) AS ci_upper
FROM experiment_data
ORDER BY variant

-- For p-value: use Python scipy.stats.proportions_ztest or a statistics tool
-- This query gives you the inputs; the significance test is computed outside SQL
```

---

### Pattern 10: ARPU by Segment Over Time

Average revenue per user, broken by a key segment dimension, tracked monthly.

```sql
-- Monthly ARPU by acquisition channel
-- Assumes: users (user_id, signup_date, acquisition_channel),
--          transactions (user_id, transaction_date, revenue)

WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC(t.transaction_date, MONTH) AS month,
    u.acquisition_channel,
    COUNT(DISTINCT t.user_id) AS paying_users,
    SUM(t.revenue) AS total_revenue
  FROM transactions t
  JOIN users u ON t.user_id = u.user_id
  WHERE t.transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
  GROUP BY 1, 2
),
monthly_mau AS (
  SELECT
    DATE_TRUNC(event_date, MONTH) AS month,
    u.acquisition_channel,
    COUNT(DISTINCT e.user_id) AS mau
  FROM events e
  JOIN users u ON e.user_id = u.user_id
  WHERE e.event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 12 MONTH)
  GROUP BY 1, 2
)
SELECT
  r.month,
  r.acquisition_channel,
  m.mau,
  r.paying_users,
  r.total_revenue,
  ROUND(r.total_revenue / NULLIF(m.mau, 0), 2) AS arpu,
  ROUND(r.total_revenue / NULLIF(r.paying_users, 0), 2) AS arppu -- avg revenue per PAYING user
FROM monthly_revenue r
LEFT JOIN monthly_mau m ON r.month = m.month AND r.acquisition_channel = m.acquisition_channel
ORDER BY 1, 2
```

---

## Part 2: Query Optimization Tips

### Index and partition usage

```sql
-- Always filter on partitioned columns first in BigQuery/Snowflake
-- BAD: WHERE DATE(event_timestamp) = '2025-01-01'  (forces full scan in BigQuery)
-- GOOD: WHERE event_timestamp >= '2025-01-01' AND event_timestamp < '2025-01-02'

-- Avoid SELECT * in production queries
-- BAD: SELECT * FROM events WHERE ...
-- GOOD: SELECT user_id, event_name, event_timestamp FROM events WHERE ...

-- Use COUNTIF or SUM(CASE WHEN ...) instead of subqueries for conditional aggregation
-- BAD: SELECT (SELECT COUNT(*) FROM events WHERE event_name = 'x' AND user_id = u.user_id)
-- GOOD: SUM(CASE WHEN event_name = 'x' THEN 1 ELSE 0 END)

-- Push filters into CTEs, not the outer query
-- Apply WHERE clauses as early as possible to reduce rows before joins
```

### Window function syntax across warehouses

| Function | BigQuery | Snowflake | Redshift |
|---|---|---|---|
| Row number | ROW_NUMBER() OVER (...) | Same | Same |
| Running total | SUM(col) OVER (ORDER BY date) | Same | Same |
| Lag/lead | LAG(col, 1) OVER (...) | Same | Same |
| Date truncation | DATE_TRUNC(date, MONTH) | DATE_TRUNC('month', date) | DATE_TRUNC('month', date) |
| Date difference | DATE_DIFF(d1, d2, DAY) | DATEDIFF('day', d2, d1) | DATEDIFF(day, d2, d1) |
| Conditional count | COUNTIF(condition) | SUM(IFF(condition, 1, 0)) | SUM(CASE WHEN condition THEN 1 ELSE 0 END) |
| Approx distinct | APPROX_COUNT_DISTINCT(col) | APPROX_COUNT_DISTINCT(col) | APPROXIMATE COUNT DISTINCT(col) |

---

## Part 3: Date Spine Pattern

Use a date spine to fill gaps in time-series data. Without it, days with zero events are missing from charts.

```sql
-- Date spine for filling gaps in daily metrics (BigQuery)
WITH date_spine AS (
  SELECT date
  FROM UNNEST(GENERATE_DATE_ARRAY(
    DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY),
    CURRENT_DATE(),
    INTERVAL 1 DAY
  )) AS date
),
daily_metrics AS (
  SELECT event_date, COUNT(DISTINCT user_id) AS dau
  FROM events
  WHERE event_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
  GROUP BY 1
)
SELECT
  ds.date,
  COALESCE(dm.dau, 0) AS dau -- 0 for days with no data
FROM date_spine ds
LEFT JOIN daily_metrics dm ON ds.date = dm.event_date
ORDER BY 1

-- Snowflake alternative: use GENERATOR(ROWCOUNT => 90) with DATEADD
-- Redshift alternative: use a numbers table or recursive CTE
```

---

## Part 4: Query Output Format

When generating a query for the user, always include:

1. **The query** — production-ready, with comments on key lines
2. **Schema assumptions** — table and column names used, and where to substitute
3. **Dialect note** — which SQL dialect is used, and what to change for others
4. **What the output looks like** — describe the columns and what each represents
5. **Benchmark reference** — what the output numbers should look like for a healthy product
6. **Performance note** — if the query may be slow on large tables, suggest partition filters or sampling

---

### Further Reading

- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [How to Become a Technology-Literate PM](https://www.productcompass.pm/p/how-to-become-a-technology-literate)
