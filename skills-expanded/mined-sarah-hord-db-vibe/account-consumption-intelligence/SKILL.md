---
name: account-consumption-intelligence
description: "Build account-specific consumption intelligence pipelines. Genericized from proven patterns — taxonomy, agent functions, MVs, forecasting. Use when setting up consumption analytics for a specific customer account."
---

# Account Consumption Intelligence

Build account-specific consumption intelligence pipelines for any Databricks customer account. This is a proven, repeatable pattern for creating deep, actionable analytics that go beyond what GTM Gold provides out of the box.

## When to Use This Skill

Use this skill when you need to:
- Set up deep consumption analytics for a specific account
- Attribute workspace spend to business units, programs, or products
- Build forecasting pipelines for account consumption
- Create reusable agent functions for automated analysis
- Go beyond GTM Gold's standard metrics with account-specific context

**Prerequisite:** Familiarity with GTM Gold tables. Load `gtm-kit:gtm-gold` for core table reference and pre-computed metric patterns.

## What Is Account Consumption Intelligence?

A thin, account-specific layer over GTM Gold that adds:
1. **Account taxonomy** -- Map workspaces to business units, programs, and products
2. **Materialized views** -- Pre-aggregated inputs optimized for analysis
3. **Agent functions** -- Pure, reusable analysis functions that operate on the MVs
4. **Forecasting** -- Ensemble forecast models for consumption prediction

## Key Concepts

### Single Source of Truth

Every account gets one unified consumption view (`{account}_consumption_daily`) built on GTM Gold data. This view is the sole input for all downstream analytics. By filtering and enriching GTM Gold data once, you avoid inconsistencies across reports.

### Account Taxonomy

A dimension table (`{account}_workspace_dim`) maps workspaces to business units, programs, and products:

```
Workspace  -->  Business Unit  -->  Program  -->  Product
```

This mapping enables attribution analysis: "Which business unit is driving spend growth?" "Which program has the highest cost per active user?"

### Agent Functions

Pure, account-agnostic SQL functions or notebooks that take input materialized views (MVs) and produce analysis outputs. These are reusable across accounts -- only the input MVs change. Think of them as parameterized analytics recipes.

### Input MVs (Materialized Views)

Pre-aggregated inputs that serve as the contract between raw data and agent functions:

| MV | Description |
|----|-------------|
| `{prefix}_input_entities` | Workspace and BU-level aggregations with trailing metrics |
| `{prefix}_input_weekly` | Weekly time-series for trend and forecast analysis |
| `{prefix}_input_account` | Account-level rollups across all workspaces |
| `{prefix}_input_jobs` | Job-level metrics (cost, duration, frequency) |

### Forecasting

Ensemble methods (WMA, ETS, ARIMA) applied to the weekly input MV to project future spend. Forecasts are stored alongside actuals in the input MVs for easy comparison.

## Architecture

```
GTM Gold (workspace_consumption_daily)
    |
    v
Account Consumption View ({account}_consumption_daily)
    |                         \
    v                          v
Taxonomy Dimension        SKU Details
({account}_workspace_dim)
    |
    v
Input Materialized Views ({prefix}_input_*)
    |
    v
Agent Functions (fn_agent_*)
    |
    v
Reports, Dashboards, Alerts, QBR Decks
```

Each layer has a clear responsibility:
1. **GTM Gold** -- raw, pre-computed metrics across all accounts
2. **Account Consumption View** -- filtered to one account, enriched with taxonomy
3. **Taxonomy Dimension** -- workspace-to-BU mapping maintained by account team
4. **Input MVs** -- pre-aggregated, standardized inputs for agent functions
5. **Agent Functions** -- reusable analysis logic, account-agnostic
6. **Outputs** -- reports, dashboards, Slack alerts, QBR decks

## Available MCP Tools

### get_account_consumption_weekly

Query account-specific weekly consumption from input MVs. Returns weekly time-series with actuals and forecasts.

```
get_account_consumption_weekly(schema="users.your_schema", table_prefix="prod_acme")
get_account_consumption_weekly(schema="users.your_schema", table_prefix="prod_acme", start_date="2026-01-01")
```

### get_account_forecast

Fetch forecast outputs from the weekly input MV. Returns ensemble forecast with individual model components (WMA, ETS, ARIMA).

```
get_account_forecast(schema="users.your_schema", table_prefix="prod_acme")
```

### refresh_account_mvs

Refresh all materialized views for an account. Triggers recomputation of entities, weekly, account, and jobs MVs.

```
refresh_account_mvs(schema="users.your_schema", table_prefix="prod_acme")
refresh_account_mvs(schema="users.your_schema", table_prefix="prod_acme", mv_suffixes=["input_weekly", "input_account"])
```

## Getting Started: 5-Step Setup

### Step 1: Create the Account Taxonomy Dimension

Map each workspace to its business unit, program, and product. This is the most important step -- it enables all attribution analysis.

```sql
CREATE OR REPLACE TABLE {catalog}.{schema}.{account}_workspace_dim (
  workspace_id STRING,
  workspace_name STRING,
  business_unit STRING,
  program STRING,
  product STRING,
  owner STRING,
  notes STRING
)
```

See [taxonomy-setup.md](taxonomy-setup.md) for detailed step-by-step guidance including how to populate the initial mapping and maintain it over time.

### Step 2: Create the Account Consumption View

Filter GTM Gold to the target account and join with taxonomy.

```sql
CREATE OR REPLACE VIEW {catalog}.{schema}.{account}_consumption_daily AS
SELECT
  c.*,
  d.business_unit,
  d.program,
  d.product,
  d.owner AS workspace_owner
FROM main.gtm_gold.workspace_consumption_daily c
LEFT JOIN {catalog}.{schema}.{account}_workspace_dim d
  ON c.workspace_id = d.workspace_id
WHERE c.account_name = '{Account Name}'
```

### Step 3: Create Input Materialized Views

Pre-aggregate data at the grains needed by agent functions. The 4 standard MVs are:

- **Entities** -- workspace and BU-level summaries with current-period metrics
- **Weekly** -- weekly time-series for trend analysis and forecasting
- **Account** -- single-row account-level rollup
- **Jobs** -- job-level cost and efficiency metrics

### Step 4: Configure Agent Functions

Deploy reusable analysis functions from the standard catalog. See [agent-functions.md](agent-functions.md) for the full set of 12 function categories.

### Step 5: Set Up Forecasting

Apply ensemble forecast models to the weekly input MV. See [forecasting.md](forecasting.md) for method details, setup, and interpretation guidance.

## Quick Reference: Common Operations

| Task | Command |
|------|---------|
| Refresh all MVs | `refresh_account_mvs(schema="...", table_prefix="...")` |
| Weekly consumption | `get_account_consumption_weekly(schema="...", table_prefix="...", weeks=12)` |
| Forecast | `get_account_forecast(schema="...", table_prefix="...")` |
| Full analysis cycle | Refresh MVs -> Run agent functions -> Generate report |
| Add new workspace | Update taxonomy dim -> Refresh MVs |
| QBR preparation | Refresh -> Run executive summary function -> Export to deck |

## Reference Files

- [agent-functions.md](agent-functions.md) -- Agent function patterns and the 12 function categories
- [taxonomy-setup.md](taxonomy-setup.md) -- How to set up and maintain account taxonomy
- [forecasting.md](forecasting.md) -- Forecasting methods, setup, and interpretation
