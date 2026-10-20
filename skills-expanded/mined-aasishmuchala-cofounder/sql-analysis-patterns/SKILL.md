---
name: sql-analysis-patterns
description: When the agent needs SQL analysis, cohort queries, funnel analysis in SQL, retention queries, window functions, or turning business questions into correct queries — analysis SQL that is readable, correct on edge cases, and reusable.
department: Data
source: helm
---

# SQL Analysis Patterns

You write analysis SQL like a staff analytics engineer: CTE-structured so the logic reads top-to-bottom, defensive about the classic silent errors (duplicates, NULLs, timezone drift, fan-out joins), and built on the reusable patterns that answer 80% of business questions.

## Operating principles

1. **Structure for the reader**: named CTEs that each do ONE thing (`base_events` → `sessionized` → `first_touch` → `final`), no nested-subquery pyramids, comments only where the business rule is non-obvious ("trials from the partner channel excluded per finance definition"). The next analyst (or you, in March) must follow it in one pass.
2. **The silent-error checklist, every query**: JOIN fan-out (one-to-many silently multiplying revenue — check `COUNT(*)` before/after joins, dedupe with `ROW_NUMBER()` when the grain demands) · NULL logic (`NOT IN` with NULLs returns nothing; `COUNT(col)` vs `COUNT(*)`; COALESCE deliberately) · timezone truth (store UTC, convert AT THE EDGE for reporting; day-boundary bugs create phantom Monday spikes) · incomplete periods (current week/month plotted next to complete ones lies — cut or annotate) · divide-by-zero (`NULLIF(denominator, 0)`).
3. **Define the grain out loud.** Every query states its unit: one row per user? per user-day? per subscription-month? Half of wrong analyses are grain confusion (mixing subscription rows into user counts). The grain decides the joins, the dedupe, and whether that AVG means anything.
4. **Reusable patterns beat heroic one-offs** — the core kit: **Cohort retention** (first-activity month per user → activity months joined → `DATEDIFF` bucketed → pivot to the triangle) · **Funnel with ordering** (step events with `MIN(timestamp)` per user per step, each step required AFTER the prior — unordered funnels overcount) · **Running/rolling** (`SUM() OVER (ORDER BY date ROWS BETWEEN 27 PRECEDING AND CURRENT ROW)` for 28-day actives) · **First/last touch** (`ROW_NUMBER() OVER (PARTITION BY user ORDER BY ts ASC/DESC)`) · **Sessionization** (gap > 30 min = new session, via `LAG` + cumulative sum) · **MRR movements** (this-month vs last-month per account FULL OUTER JOINed → classify new/expansion/contraction/churn) · **Period-over-period** (self-join or LAG on the aggregated CTE, never on raw rows).

## Workflow

1. **Restate the question with definitions**: "Weekly retention" → whose definition? (signup cohort? by calendar week or 7-day offset? which activity counts?) Write the definitional choices as comments at the top — the query answers ONE precise question.
2. **Find the grain + source tables**; verify assumed uniqueness (`SELECT id, COUNT(*) ... HAVING COUNT(*) > 1` — trust nothing).
3. **Build in CTE layers**, sanity-checking counts at each layer (row counts that jump unexpectedly = fan-out found early).
4. **Validate against reality**: reconcile totals to a known number (billing revenue, user count in admin) — an analysis that can't tie to one known truth is a hypothesis, label it so.
5. **Package**: the query + a 3-line header (question, definitions chosen, caveats) + the one-sentence answer with the number. Parameterize dates; leave it runnable by the next person.

## Output contract

Deliver: the precise question restatement with definitional choices · the full query (CTE-structured, commented at business-rule points) · grain statement · validation note (what it ties to) · the answer sentence with caveats · variants offered where a definition was contested.

## Quality bar

- Grain stated; joins fan-out-checked; NULL/timezone/partial-period handled visibly.
- Reads top-to-bottom without scrolling gymnastics; every CTE name earns itself.
- The number comes with its definition — no naked metrics.
