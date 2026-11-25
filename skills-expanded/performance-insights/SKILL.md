---
name: performance-insights
description: Explain what changed in Google Ads performance and why, period over period, reconciled with GA4. Use when the user asks "why did cost per lead go up?", "what changed last week?", "how is Demand Gen doing?", "why did conversions drop?", or wants a quick performance brief.
---

# Performance insights

Compare two periods, find the campaigns and segments behind the change, and check the conversions against GA4 before
calling anything a drop.

## When to use

A question about a change in spend, clicks, CPC, conversions, CPL or ROAS. For a full account review use `ads-audit`;
for the Monday routine use `weekly-check`.

## Inputs

- `account`: profile alias.
- Periods: the user's, or last 7 days vs the 7 days before. Use `dateFrom` / `dateTo` (YYYY-MM-DD) for both periods so
  they are exactly comparable.
- The metric they care about (default: conversions and cost per conversion).

## Steps

Call `account_profile` first (currency, linked GA4).

1. **Totals.** `get_account_summary` for each period. State the change in cost, clicks, CTR, CPC, conversions and
   cost per conversion as numbers and percentages.
2. **Where.** `get_campaign_performance` for each period. Rank campaigns by their contribution to the change
   (absolute difference in the metric, not percent).
3. **Why, inside the top 1–3 campaigns.** Use `get_performance_by_date` for the day the change started, then segment
   with `run_gaql_query`, for example:
   - device: `SELECT segments.device, metrics.cost_micros, metrics.conversions FROM campaign WHERE campaign.id = <id> AND segments.date BETWEEN '<from>' AND '<to>'`
   - network: same query with `segments.ad_network_type`
   - search terms: `get_search_terms` for the campaign and both periods (new expensive terms are a common cause)
   - auction pressure: `metrics.search_impression_share`, `metrics.search_budget_lost_impression_share`,
     `metrics.search_rank_lost_impression_share` on `campaign`
   - recent changes: `changes_list` (changes made through this package) and, for Demand Gen, `guide("demand-gen")`
     on reading the first weeks.
4. **Reconcile.** If GA4 is linked, `ga4_conversions` and `ga4_traffic_sources` for both periods. If GA4 lead events
   held steady while Ads conversions fell, the problem is measurement, not demand: say so and point to
   `guide("measurement")`.
5. Read CPC/CTR/CPL movements with `guide("benchmarks")` in mind: they are ranges, not targets.

## Output

```
# <alias>: <period A> vs <period B>

**What changed:** <one sentence with the main number>
| Metric | A | B | Δ |
|---|---|---|---|

**Why:** 2–4 bullets, each with evidence (campaign, segment, number).

**Do next:** 2–3 actions, each naming the tool that would make the change.
```

Keep it under one screen. Name the evidence; say "unclear" when the data doesn't explain the change.

## Never

- Never apply a change from this skill. Suggest it; if the user says yes, preview it first (no `confirm`), then apply
  after a second yes.
- If the profile is read-only (no write tools), say that applying needs
  `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart. Never edit config files.
- Never compare periods of different length or a period that includes today against full days.
- Never report "0 conversions" as "no leads" without the GA4 check in step 4.
