---
name: sql-analytics-queries
description: Writes readable CTE-based SQL for funnels, cohorts and retention, with the grain stated up front. Use it for product and revenue analytics questions.
---

# SQL analytics queries

Write the query as a story of small named steps. Know the grain of every step.

## Steps

1. Restate the question as a metric: numerator, denominator, time window, and the unit counted (users, orders, sessions). Ask if any is unclear.
2. Inspect the tables first: columns, keys, and a few rows. Confirm the grain of each (one row per what?) and the time zone of timestamps.
3. Build with CTEs, one idea each, named for what they hold: `signups`, `first_purchase`, `weekly_activity`. Put filters in the earliest CTE possible.
4. Funnels: take each user's first event per step with `MIN(event_time)`, join steps on user and require time order. Count distinct users, never events.
5. Cohorts and retention: cohort = `DATE_TRUNC` of first activity; offset = periods between activity and cohort; divide by the cohort size, not by total users.
6. Use window functions (`ROW_NUMBER`, `LAG`, `SUM() OVER`) instead of self-joins where possible.
7. Check: the first funnel step equals a plain `COUNT(DISTINCT user_id)`; every step is less than or equal to the one before; cohort sizes add up to the total.

## Rules

- Never join two tables at different grains without aggregating one first.
- Write `LEFT JOIN` when losing rows would bias the metric, and say why.
- Match the dialect already used in the project.

## Report

The query, a two line explanation of each CTE, the sanity checks and their results, and every assumption such as "excluded internal accounts".
