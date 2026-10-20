---
name: logfood-querier
description: Queries Databricks internal data and metrics to understand consumption, feature usage, account information, and more. Triggers on consumption queries, product adoption, new product usage, feature usage trends, customer spending, DBU consumption, or usage analysis. Invoke this skill even if the customer name is not yet specified — the skill handles clarification.
---


# Internal Data Querier Skill

Queries Databricks internal data and metrics to understand consumption, feature usage, account information, and more.

## Step 1: Load Related Skills (Before Querying)

**Proactively load the `salesforce-actions` skill** into context before starting:
```
/salesforce-actions
```
This is important because Logfood queries often involve Salesforce data (use cases, accounts, opportunities). Having the Salesforce schemas and query patterns in context prevents incorrect queries and ensures proper use of processDate filters.

## Critical: Profile Configuration

**ALWAYS use `--profile=logfood` for all Logfood queries.**

The Logfood workspace is: `https://adb-2548836972759138.18.azuredatabricks.net/`

Do NOT use any other profile name (e.g., `fe-logfood`, `fe-dogfood`, `fe-central-sa`). The profile is simply `logfood`.

## Critical: Regional Scoping for BU Filters

**BU names (like DNB, FSI, PubSec) are NOT globally unique!** The same BU can exist in multiple regions (AMER, EMEA, APJ).

**⚠️ WRONG - captures data from ALL regions:**
```sql
WHERE ur.Name LIKE '%DNB%'
```

**✓ CORRECT - properly scoped to one region:**
```sql
WHERE ur.Name LIKE '%DNB%'
  AND u.FEPhysicalRegion__c = 'AMER'
```

When filtering by BU, ALWAYS also filter by region (FEPhysicalRegion__c) to avoid cross-regional data leakage.

## Critical: Schema Selection Guide

Choose the right schema based on what you need:

| Need | Schema | Resource |
|------|--------|----------|
| **Account consumption analysis** (16 queries: spend, products, workspaces, contract, users, competitors, BI tools, whitespace) | `main.fin_live_gold` + `main.gtm_gold` + `main.data_dbsql` | resources/ACCOUNT_CONSUMPTION_QUERIES.md |
| **Consumption dollars (SOT)** — workspace + SKU + date grain, finance-grade accuracy | `main.fin_live_gold` | resources/FIN_LIVE_GOLD.md |
| **Contract burndown & burst forecasting** | `main.fin_live_gold` | resources/FIN_LIVE_GOLD.md |
| **Product line breakdowns** (AI, Lakeflow, etc. via nested structs) | `main.fin_live_gold` | resources/FIN_LIVE_GOLD.md |
| **GTM-contextualized consumption** — pre-joined with territories, BUs, hierarchies | `main.gtm_gold` | resources/GTM_GOLD.md |
| **Individual/rep-level consumption roll-ups** | `main.gtm_gold` | resources/GTM_GOLD.md |
| **Account, opportunity, pipeline data** with GTM dimensions | `main.gtm_gold` / `main.gtm_silver` | resources/GTM_GOLD.md |
| **Field hierarchy, headcount, org structure** | `main.gtm_silver` | resources/GTM_GOLD.md |
| **Salesforce objects** (use cases, blockers, escalations, ASQs) | `main.sfdc_bronze` | Use `salesforce-actions` skill |

**Data flows downstream:** `fin_live_gold.paid_usage_metering` (SOT) → `gtm_silver` → `gtm_gold`

> **WARNING:** `main.gtm_data` was fully deprecated in February 2026. Do NOT use it — use `main.gtm_gold` / `main.gtm_silver` instead.

### Instructions
1) Ensure authenticated: `databricks auth profiles | grep logfood` - if not valid, run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`
2) Select a warehouse using the databricks-warehouse-selector skill (use `--profile=logfood`)
3) Execute queries with: `databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{"statement": "<SQL>", "warehouse_id": "<id>", "format":"JSON_ARRAY", "wait_timeout":"50s"}'`
4) **For consumption/dollar queries:** refer to resources/FIN_LIVE_GOLD.md — this is the source of truth for all dollar-denominated consumption data
5) **For GTM-contextualized data** (sales hierarchies, territories, pipeline, account dimensions): refer to resources/GTM_GOLD.md
6) For Salesforce data (use cases, opportunities, blockers, escalations, ASQs, etc) use the `salesforce-actions` skill instead
7) If you encounter unfamiliar acronyms or jargon (e.g., DNB, FSI, EDNB) in queries or results, use the `internal-jargon` skill to look them up
8) **When filtering by BU, always include region filter** (FEPhysicalRegion__c) to avoid cross-regional data
9) For specialized analysis areas, refer to the dashboard resources below which contain source tables, example queries, and query patterns

## Quick-Start SA Queries

Common questions SAs and AEs need to answer about their customers. All queries use `main.fin_live_gold.paid_usage_metering` (PUM). Replace `<ACCOUNT_ID>` with the Salesforce Account ID.

### "How much is my customer spending?"

```sql
SELECT
  sfdc_account_name,
  ROUND(SUM(usage_dollars), 2) AS total_dollars,
  ROUND(SUM(usage_amount), 2) AS total_dbus
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = '<ACCOUNT_ID>'
  AND date >= DATEADD(DAY, -30, CURRENT_DATE())
  AND paying_status = 'PAYING_STATUS_PAYING'
GROUP BY sfdc_account_name
```

### "What products are they using?"

```sql
SELECT
  product_type,
  ROUND(SUM(usage_dollars), 2) AS dollars,
  ROUND(SUM(usage_dollars) / SUM(SUM(usage_dollars)) OVER () * 100, 1) AS pct
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = '<ACCOUNT_ID>'
  AND date >= DATEADD(DAY, -30, CURRENT_DATE())
  AND paying_status = 'PAYING_STATUS_PAYING'
GROUP BY product_type
ORDER BY dollars DESC
```

### "Are they growing or shrinking? Why?"

Compares current month vs prior month, broken down by product type to show what's driving the change.

```sql
WITH monthly AS (
  SELECT
    product_type,
    SUM(CASE WHEN date >= DATEADD(DAY, -30, CURRENT_DATE()) THEN usage_dollars ELSE 0 END) AS current_30d,
    SUM(CASE WHEN date >= DATEADD(DAY, -60, CURRENT_DATE()) AND date < DATEADD(DAY, -30, CURRENT_DATE()) THEN usage_dollars ELSE 0 END) AS prior_30d
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = '<ACCOUNT_ID>'
    AND date >= DATEADD(DAY, -60, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
  GROUP BY product_type
)
SELECT
  product_type,
  ROUND(prior_30d, 2) AS prior_30d,
  ROUND(current_30d, 2) AS current_30d,
  ROUND(current_30d - prior_30d, 2) AS delta,
  CASE WHEN prior_30d > 0 THEN ROUND((current_30d - prior_30d) / prior_30d * 100, 1) ELSE NULL END AS pct_change
FROM monthly
WHERE current_30d > 0 OR prior_30d > 0
ORDER BY ABS(current_30d - prior_30d) DESC
```

### "Which workspace drives the most spend?"

```sql
SELECT
  sfdc_workspace_id,
  sfdc_workspace_name,
  platform,
  ROUND(SUM(usage_dollars), 2) AS dollars,
  ROUND(SUM(usage_dollars) / SUM(SUM(usage_dollars)) OVER () * 100, 1) AS pct
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id = '<ACCOUNT_ID>'
  AND date >= DATEADD(DAY, -30, CURRENT_DATE())
  AND paying_status = 'PAYING_STATUS_PAYING'
GROUP BY sfdc_workspace_id, sfdc_workspace_name, platform
ORDER BY dollars DESC
```

## New Product Adoption Detection

Identify products a customer started using recently by comparing the last N days against the prior period. Useful for weekly account reviews.

```sql
WITH recent AS (
  SELECT DISTINCT product_type
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = '<ACCOUNT_ID>'
    AND date >= DATEADD(DAY, -7, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
    AND usage_dollars > 0
),
prior AS (
  SELECT DISTINCT product_type
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = '<ACCOUNT_ID>'
    AND date >= DATEADD(DAY, -37, CURRENT_DATE())
    AND date < DATEADD(DAY, -7, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
    AND usage_dollars > 0
)
SELECT r.product_type AS newly_adopted_product
FROM recent r
LEFT JOIN prior p ON r.product_type = p.product_type
WHERE p.product_type IS NULL
```

Adjust the time windows as needed: `-7` / `-37` for weekly reviews, `-30` / `-90` for monthly reviews.

## Whitespace / Upsell Detection

Show which products a customer is using vs the full product catalog, highlighting upsell opportunities.

```sql
WITH all_products AS (
  SELECT DISTINCT product_type
  FROM main.fin_live_gold.paid_usage_metering
  WHERE date >= DATEADD(DAY, -30, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
    AND usage_dollars > 100
),
customer_products AS (
  SELECT DISTINCT product_type
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id = '<ACCOUNT_ID>'
    AND date >= DATEADD(DAY, -90, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
    AND usage_dollars > 0
)
SELECT
  ap.product_type,
  CASE WHEN cp.product_type IS NOT NULL THEN 'USING' ELSE 'NOT USING' END AS status
FROM all_products ap
LEFT JOIN customer_products cp ON ap.product_type = cp.product_type
ORDER BY status DESC, ap.product_type
```

## Product Type Reference

Complete list of `product_type` values in PUM (as of FY26), grouped by category:

**Compute:**
- `JOBS` — Automated jobs (workflows)
- `SQL` — Databricks SQL (warehouses)
- `ALL_PURPOSE` — All-purpose compute (notebooks, interactive)
- `DLT` — Delta Live Tables / Lakeflow pipelines
- `INTERACTIVE` — Interactive clusters

**AI / ML:**
- `FOUNDATION_MODEL_API` — Foundation Model APIs (pay-per-token)
- `MODEL_SERVING` — Model serving endpoints
- `MOSAIC_ML` — Mosaic ML training
- `AI_RUNTIME` — AI runtime
- `AI_GATEWAY` — AI Gateway
- `AI_FUNCTIONS` — AI functions (ai_query, ai_classify, etc.)
- `FOUNDATION_MODEL_TRAINING` — Fine-tuning API
- `VECTOR_SEARCH` — Vector Search
- `AGENT_BRICKS` — Agent Bricks
- `SUPERVISOR_AGENT` — Supervisor agents (multi-agent)
- `AGENT_EVALUATION` — Agent evaluation

**Data Platform:**
- `LAKEBASE` — Lakebase (managed PostgreSQL)
- `LAKEFLOW_CONNECT` — Lakeflow Connect (ingestion connectors)
- `PREDICTIVE_OPTIMIZATION` — Predictive optimization
- `DATA_QUALITY_MONITORING` — Lakehouse monitoring
- `DATA_CLASSIFICATION` — Data classification
- `ONLINE_TABLES` — Online tables
- `DATA_SHARING` — Delta Sharing

**BI:**
- `AI_BI_GENIE` — AI/BI Genie spaces

**Infrastructure:**
- `APPS` — Databricks Apps
- `NETWORKING` — Private networking (PrivateLink, etc.)
- `FINE_GRAINED_ACCESS_CONTROL` — Row/column-level security
- `DEFAULT_STORAGE` — Default storage
- `BASE_ENVIRONMENTS` — Base environments
- `DATABASE` — Legacy database compute

## Schema Resources

Core schema documentation with table catalogs, column details, and example queries:

| Schema | Resource | Use For |
|--------|----------|---------|
| Finance Live Gold | resources/FIN_LIVE_GOLD.md | Consumption dollars (SOT), contracts, burndown, product line breakdowns via PUM |
| GTM Gold & Silver | resources/GTM_GOLD.md | GTM-contextualized data, account/rep roll-ups, hierarchies, OBTs |

## Internal Dashboards Reference

The following dashboard resources document the source tables, SQL query patterns, and example queries used by popular internal Lakeview dashboards. Use these as references when building queries for similar analysis areas.

| Dashboard | Resource | Use For |
|-----------|----------|---------|
| Zerobus Ingest Global | resources/ZEROBUS_INGEST.md | Zerobus streaming ingestion volume, throughput, protocol/cloud breakdown, customer adoption |
| Central Jobs System Tables | resources/CENTRAL_JOBS.md | Job costs, performance, failure analysis, optimization recommendations, forecasting |
| Global Lakeflow Connect Usage | resources/LAKEFLOW_CONNECT_USAGE.md | Lakeflow Connect adoption, consumption trends, pipeline operations, partner tool detection |
| Feature Previews | resources/FEATURE_PREVIEW.md | Feature preview lifecycle, enrollment/enablement status, workspace ring assignments |
| DBSQL Endpoint Analysis (V2.0) | resources/DBSQL_ENDPOINT_ANALYSIS.md | Warehouse utilization, query performance, auto-stop efficiency, cost optimization |
| Cluster 360 V2 | resources/CLUSTER_360.md | Cluster performance troubleshooting - CPU, heap, GC, infrastructure metrics, crash detection |
