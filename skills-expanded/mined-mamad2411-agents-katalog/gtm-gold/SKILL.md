---
name: gtm-gold
description: "GTM Gold analytics with MCP tools. Use for workspace consumption analysis, account metrics, and pre-computed GTM Gold measures. Complements logfood-querier with direct tool access."
---

# GTM Gold Analytics

This skill provides MCP tool access to GTM Gold and pre-computed analytics patterns. It **complements** the `fe-internal-tools:logfood-querier` skill, which covers schema reference and migration mapping.

**When to use this skill vs logfood-querier:**
- Use **gtm-gold** when you need to run MCP tool queries (get_workspace_consumption, get_account_metrics, query_gtm_gold) or need pre-computed metric pattern guidance
- Use **logfood-querier** when you need full schema reference, column documentation, or migration mapping from legacy Logfood tables

## Available MCP Tools (gtm-kit server)

### query_gtm_gold
Ad-hoc SQL against any GTM Gold table. Use fully-qualified names.
```
query_gtm_gold(sql_query="SELECT * FROM main.gtm_gold.workspace_consumption_daily WHERE account_name = 'Acme' LIMIT 10")
```

### get_workspace_consumption
Workspace-level daily consumption for an account. Supports date range filtering.
```
get_workspace_consumption(account_name="Acme Corp", start_date="2026-01-01", end_date="2026-02-27")
```

### get_account_metrics
Account-level metrics from the account one-big-table (OBT). Includes pre-computed t7d/t28d/t91d metrics, forecasts, and rankings.
```
get_account_metrics(account_name="Acme Corp")
```

## Core Tables (Brief)

For full schema reference, load `fe-internal-tools:logfood-querier` and read its GTM_GOLD.md.

| Table | Grain | Key Use |
|-------|-------|---------|
| `workspace_consumption_daily` | workspace x date | Daily spend, rankings, period metrics |
| `workspace_sku_consumption_daily` | workspace x sku x date | SKU-level breakdowns |
| `account_obt` | account | Account-level totals, forecasts, rankings |
| `account_active_users_daily` | account x date | DAU/WAU/MAU metrics |
| `account_consumption_daily` | account x date | Account-level daily trends |

## Pre-computed Metric Patterns

GTM Gold pre-computes many common aggregations. **Always check for pre-computed columns before writing your own aggregation.**

| Pattern | Meaning | Example Columns |
|---------|---------|-----------------|
| `*_t7d_*` | Trailing 7-day | `dbu_dollars_t7d_avg`, `dbu_dollars_t7d_sum` |
| `*_t28d_*` | Trailing 28-day | `dbu_dollars_t28d_avg` |
| `*_t91d_*` | Trailing 91-day (quarterly) | `dbu_dollars_t91d_avg` |
| `*_qtd*` | Quarter-to-date | `dbu_dollars_qtd` |
| `*_ytd*` | Year-to-date | `dbu_dollars_ytd` |
| `*_mtd*` | Month-to-date | `dbu_dollars_mtd` |
| `*_wow_*` | Week-over-week change | `dbu_dollars_wow_pct` |
| `*_mom_*` | Month-over-month change | `dbu_dollars_mom_pct` |
| `*_dod_*` | Day-over-day change | `dbu_dollars_dod_pct` |
| `*_pop_*` | Period-over-period | `dbu_dollars_pop_pct` |
| `*_rank*` | Rankings | `biggest_gainer_rank`, `biggest_loser_rank` |
| `biggest_*` | Top movers | `biggest_gainer`, `biggest_loser` |
| `forecast*` | Forecast values | `forecast_dbu_dollars` |
| `vs_*` | Variance / comparison | `vs_forecast_pct` |

## Common Workflows

### Weekly Account Review
1. `get_account_metrics("Account Name")` — snapshot of current state
2. `get_workspace_consumption("Account Name", start_date="YYYY-MM-DD")` — last 7 days
3. Look at `*_wow_*` columns for week-over-week trends
4. Check `biggest_gainer_rank` / `biggest_loser_rank` for workspace-level movers

### Consumption Trend Analysis
1. `get_workspace_consumption("Account Name", start_date="2026-01-01")` — pull period data
2. Compare `dbu_dollars_t7d_avg` vs `dbu_dollars_t28d_avg` for acceleration/deceleration
3. Use `query_gtm_gold` for SKU-level drill-down if needed

### Workspace Ranking
```sql
query_gtm_gold("SELECT workspace_name, dbu_dollars_t7d_sum, biggest_gainer_rank FROM main.gtm_gold.workspace_consumption_daily WHERE account_name = 'Acme Corp' AND usage_date = CURRENT_DATE - 1 ORDER BY dbu_dollars_t7d_sum DESC")
```

## Reference Files

- [account-analytics.md](account-analytics.md) — Account-level analytics patterns
- [metric-patterns.md](metric-patterns.md) — How to discover and use pre-computed metrics
- [workspace-consumption.md](workspace-consumption.md) — Workspace consumption analysis patterns
