---
name: account-consumption-report
description: "Generate a comprehensive weekly or monthly consumption trend report for any Databricks customer account. Includes 16 embedded charts covering spend trends, product breakdown, workspace analysis, contract burndown, user adoption, competitive landscape, BI tool ecosystem, and whitespace opportunities. Delivered as an HTML email with inline charts. Use when the user says 'consumption report', 'account health email', 'weekly consumption email', 'spending report', 'consumption trend', or wants to generate a recurring consumption analysis for a customer."
user-invocable: true
---

# Account Consumption Report

Generate a data-rich consumption trend report with 16 embedded charts for any Databricks customer account. The report covers spend trends, product breakdown, workspace analysis, contract burndown, user adoption, competitive landscape, BI tool ecosystem, and whitespace opportunities — delivered as a self-contained HTML email with inline base64-encoded charts.

> **How this differs from similar skills:**
> - **`gtm-kit:gtm-report`** generates a standalone HTML file for interactive viewing. This skill produces a **self-contained email** with inline base64-encoded charts designed for scheduled delivery via `launchd`/cron — no browser needed.
> - **`fe-cemea-nonreg:account-review-report`** creates markdown/PDF/Google Doc output for account reviews. This skill is **email-first** with a locked HTML template optimized for inbox rendering.
> - **`logfood-querier`** is a general-purpose query tool. This skill runs a **fixed set of 16 curated queries** and assembles them into a single cohesive report with charts — no manual query composition needed.
>
> Use this skill for **automated, recurring email delivery** of consumption reports. Use the others for interactive or document-based workflows.

## Quick Start

```
/account-consumption-report
```

Or describe your intent naturally:

```
Generate a weekly consumption report for Acme Corp and email it to [email protected]
Create a monthly account health email for Rivian
Send a spending trend report for BigBank to the account team
```

## Prerequisites

- **Logfood Access:** Databricks CLI with `--profile=logfood` configured (for consumption data queries)
- **Google Auth:** `/google-auth` configured (for sending email via Gmail)
- **Python 3:** With `matplotlib` and `pandas` available (for chart generation)

## Input Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `account_name` | Yes | Customer account name as it appears in Logfood | — |
| `recipients` | Yes | Comma-separated email addresses | — |
| `report_period` | No | `weekly` or `monthly` | `weekly` |
| `lookback_months` | No | How many months of history to include | `6` |

**Derived variables (computed at runtime):**
- `{DATE_RANGE}` — The human-readable date range covered by the report (e.g., "Feb 3 – Mar 2, 2026" for weekly, "Sep 2025 – Mar 2026" for monthly). Computed from the query results' min/max dates.
- `{REPORT_PERIOD}` — Capitalized version of `report_period` input ("Weekly" or "Monthly"). Used in the email subject line.

## Workflow

### Step 1: Authenticate

**Databricks (Logfood):**

```bash
databricks auth token --host https://adb-2548836972759138.18.azuredatabricks.net --profile logfood
```

If this fails, run `/databricks-authentication` and configure the `logfood` profile.

**Google (Gmail):**

```bash
python3 $(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py 2>/dev/null | sort -V | tail -1) status
```

If not authenticated, run `/google-auth`.

### Step 2: Select Warehouse

Pick a SQL warehouse in the logfood workspace. Use the smallest available serverless warehouse:

```bash
databricks warehouses list --profile logfood -o json | python3 -c "
import json, sys
whs = json.load(sys.stdin)
for w in whs:
    if w.get('state') == 'RUNNING' or w.get('warehouse_type') == 'PRO':
        print(f\"{w['id']} - {w['name']} ({w.get('state','UNKNOWN')})\")
" | head -5
```

Store the warehouse ID as `{WAREHOUSE_ID}` for all subsequent queries.

### Step 3: Run 16 SQL Queries

Execute each query against the logfood workspace. Replace `{ACCOUNT_NAME}` with the customer's account name and `{WAREHOUSE_ID}` with the selected warehouse.

**Execution pattern for each query:**

```bash
databricks api post /api/2.0/sql/statements/ --profile logfood --json '{
  "warehouse_id": "{WAREHOUSE_ID}",
  "statement": "<SQL_QUERY>",
  "wait_timeout": "30s"
}'
```

#### Query 1: Monthly Spend Trend (7 months)

```sql
SELECT DATE_TRUNC('month', usage_date) AS month,
       SUM(usage_quantity * list_price) AS total_spend
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1 ORDER BY 1
```

#### Query 2: Weekly Spend Trend (8 weeks)

```sql
SELECT DATE_TRUNC('week', usage_date) AS week,
       SUM(usage_quantity * list_price) AS total_spend
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -56)
GROUP BY 1 ORDER BY 1
```

#### Query 3: Product Breakdown (current 30d vs prior 30d)

```sql
SELECT product_name,
       SUM(CASE WHEN usage_date >= DATE_ADD(CURRENT_DATE(), -30) THEN usage_quantity * list_price ELSE 0 END) AS current_30d,
       SUM(CASE WHEN usage_date >= DATE_ADD(CURRENT_DATE(), -60) AND usage_date < DATE_ADD(CURRENT_DATE(), -30) THEN usage_quantity * list_price ELSE 0 END) AS prior_30d
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -60)
GROUP BY 1 ORDER BY 2 DESC
```

#### Query 4: Product Line MECE Monthly Breakdown

```sql
SELECT DATE_TRUNC('month', usage_date) AS month,
       product_lines_metric.product_line AS product_line,
       SUM(usage_quantity * list_price) AS spend
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1, 2 ORDER BY 1, 3 DESC
```

#### Query 5: Workspace Breakdown (current 30d vs prior 30d)

```sql
SELECT workspace_name,
       SUM(CASE WHEN usage_date >= DATE_ADD(CURRENT_DATE(), -30) THEN usage_quantity * list_price ELSE 0 END) AS current_30d,
       SUM(CASE WHEN usage_date >= DATE_ADD(CURRENT_DATE(), -60) AND usage_date < DATE_ADD(CURRENT_DATE(), -30) THEN usage_quantity * list_price ELSE 0 END) AS prior_30d
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -60)
GROUP BY 1 ORDER BY 2 DESC
```

#### Query 6: Workspace Monthly Trend

```sql
SELECT DATE_TRUNC('month', usage_date) AS month,
       workspace_name,
       SUM(usage_quantity * list_price) AS spend
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1, 2 ORDER BY 1, 3 DESC
```

#### Query 7: Contract Burndown

Use `contract_daily_burn_down` (NOT `consolidated_active_contracts` — that table's `paid_usage` equals `workload_commitment` and produces incorrect results).

```sql
SELECT burn_date,
       workload_commitment,
       cumulative_burn,
       workload_commitment - cumulative_burn AS remaining_commitment,
       contract_end_date
FROM main.fin_live_gold.contract_daily_burn_down
WHERE account_name = '{ACCOUNT_NAME}'
  AND burn_date >= DATE_ADD(CURRENT_DATE(), -210)
ORDER BY burn_date
```

#### Query 8: User Adoption Monthly

```sql
SELECT DATE_TRUNC('month', date) AS month,
       COUNT(DISTINCT user_id) AS active_users
FROM main.gtm_gold.account_active_users_daily
WHERE account_name = '{ACCOUNT_NAME}'
  AND date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1 ORDER BY 1
```

#### Query 9: Day-of-Week Usage Pattern

```sql
SELECT DAYOFWEEK(u.usage_date) AS day_of_week,
       DATE_FORMAT(u.usage_date, 'EEEE') AS day_name,
       AVG(usage_quantity * list_price) AS avg_daily_spend,
       AVG(au.user_count) AS avg_users
FROM main.fin_live_gold.paid_usage_metering u
LEFT JOIN (
  SELECT date, COUNT(DISTINCT user_id) AS user_count
  FROM main.gtm_gold.account_active_users_daily
  WHERE account_name = '{ACCOUNT_NAME}'
  GROUP BY 1
) au ON u.usage_date = au.date
WHERE u.account_name = '{ACCOUNT_NAME}'
  AND u.usage_date >= DATE_ADD(CURRENT_DATE(), -90)
GROUP BY 1, 2 ORDER BY 1
```

#### Query 10: Spend Per User Efficiency

```sql
SELECT DATE_TRUNC('month', u.usage_date) AS month,
       SUM(u.usage_quantity * u.list_price) AS total_spend,
       COUNT(DISTINCT au.user_id) AS active_users,
       SUM(u.usage_quantity * u.list_price) / NULLIF(COUNT(DISTINCT au.user_id), 0) AS spend_per_user
FROM main.fin_live_gold.paid_usage_metering u
LEFT JOIN main.gtm_gold.account_active_users_daily au
  ON u.account_name = au.account_name AND u.usage_date = au.date
WHERE u.account_name = '{ACCOUNT_NAME}'
  AND u.usage_date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1 ORDER BY 1
```

#### Query 11: Serverless vs Classic Breakdown

```sql
SELECT DATE_TRUNC('month', usage_date) AS month,
       CASE WHEN product_features.is_serverless = true THEN 'Serverless' ELSE 'Classic' END AS compute_type,
       SUM(usage_quantity * list_price) AS spend
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1, 2 ORDER BY 1
```

#### Query 12: Whitespace Products (zero spend in last 90d)

```sql
SELECT p.product_name
FROM (SELECT DISTINCT product_name FROM main.fin_live_gold.paid_usage_metering) p
LEFT JOIN (
  SELECT product_name, SUM(usage_quantity * list_price) AS spend
  FROM main.fin_live_gold.paid_usage_metering
  WHERE account_name = '{ACCOUNT_NAME}'
    AND usage_date >= DATE_ADD(CURRENT_DATE(), -90)
  GROUP BY 1
  HAVING SUM(usage_quantity * list_price) > 10
) a ON p.product_name = a.product_name
WHERE a.product_name IS NULL
ORDER BY 1
```

#### Query 13: Competitor Landscape

```sql
SELECT technology_name, technology_category, compete_status, last_updated
FROM main.gtm_gold.rpt_account_tech_compete
WHERE account_name = '{ACCOUNT_NAME}'
ORDER BY technology_category, technology_name
```

#### Query 14: BI & Partner Tool Revenue (current 30d)

Note: `dbsql_workload_agg` uses `canonicalCustomerName` (not `account_name`) as the account identifier.

```sql
SELECT partner_name, tool_type,
       SUM(dbus_consumed) AS total_dbus,
       SUM(dollar_amount) AS total_dollars
FROM main.data_dbsql.dbsql_workload_agg
WHERE canonicalCustomerName = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -30)
GROUP BY 1, 2 ORDER BY 4 DESC
```

#### Query 15: BI Tool Monthly Trend

```sql
SELECT DATE_TRUNC('month', usage_date) AS month,
       partner_name,
       SUM(dollar_amount) AS spend
FROM main.data_dbsql.dbsql_workload_agg
WHERE canonicalCustomerName = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -210)
GROUP BY 1, 2 ORDER BY 1, 3 DESC
```

#### Query 16: Recent Product Activation (new products in last 30d vs prior 30d)

```sql
SELECT workspace_name, product_name,
       MIN(usage_date) AS first_seen,
       SUM(usage_quantity * list_price) AS spend_since_activation
FROM main.fin_live_gold.paid_usage_metering
WHERE account_name = '{ACCOUNT_NAME}'
  AND usage_date >= DATE_ADD(CURRENT_DATE(), -60)
GROUP BY 1, 2
HAVING MIN(usage_date) >= DATE_ADD(CURRENT_DATE(), -30)
ORDER BY 3 DESC
```

### Step 4: Generate 16 Charts

Use matplotlib with Databricks brand colors to generate charts. Save each as a PNG to `/tmp/consumption_report/{ACCOUNT_NAME}/` (account-specific directory to avoid conflicts when running multiple reports concurrently).

**Brand colors:**

```python
COLORS = {
    'dark': '#1B3A4B',
    'red': '#FF3621',
    'blue': '#1B73E8',
    'green': '#00A972',
    'orange': '#FF6F00',
    'purple': '#7B1FA2',
}
```

| # | Chart | Type |
|---|-------|------|
| 1 | Monthly spend trend | Line chart with markers |
| 2 | Weekly spend trend | Bar chart |
| 3 | Product breakdown (current vs prior) | Grouped horizontal bar |
| 4 | Product line stacked monthly | Stacked area chart |
| 5 | Workspace breakdown (current vs prior) | Grouped horizontal bar |
| 6 | Workspace monthly trend | Stacked bar chart |
| 7 | Contract burndown | Dual-axis line (commitment vs burn) |
| 8 | User adoption monthly | Line chart with markers |
| 9 | Day-of-week usage pattern | Bar chart with line overlay |
| 10 | Spend per user efficiency | Dual-axis (bar for spend, line for per-user) |
| 11 | Serverless vs Classic | Stacked bar chart |
| 12 | Whitespace products | Horizontal list/badge chart |
| 13 | Competitor landscape | Grouped bar by category |
| 14 | BI tool revenue | Horizontal bar chart |
| 15 | BI tool monthly trend | Stacked area chart |
| 16 | Recent product activation | Timeline/scatter chart |

Set `figsize=(10, 5)`, `dpi=150`, transparent background, and tight layout for all charts.

### Step 5: Build HTML Email

Construct a self-contained HTML email with all charts embedded as base64 inline images (`<img src="data:image/png;base64,...">`).

**Email structure (11 sections):**

At the top, include:
- **TL;DR box** — 6 bullet summary: total spend (current period), MoM/WoW change %, top product, top workspace, contract runway, active user count
- **Action Items box** — 6 actionable recommendations derived from the data (e.g., serverless migration opportunity, underutilized workspaces, contract renewal timeline)

Then the 11 report sections:

| # | Section | Charts/Tables |
|---|---------|---------------|
| 1 | Spend Trend | Charts 1 + 2 |
| 2 | Product Breakdown | Charts 3 + 4 + table of product spend with % change |
| 3 | Workspace Analysis | Charts 5 + 6 |
| 4 | Contract Burndown | Chart 7 + table with key contract dates and remaining commitment |
| 5 | User Adoption & Efficiency | Charts 8 + 10 |
| 6 | Usage Patterns | Chart 9 |
| 7 | Serverless Migration | Chart 11 |
| 8 | Competitive Landscape | Chart 13 |
| 9 | BI & Partner Tool Ecosystem | Charts 14 + 15 + table of BI tool spend |
| 10 | Recent Product Activation | Chart 16 + table of newly activated products |
| 11 | Whitespace Opportunities | Chart 12 + bulleted list of unused products |

Use clean, professional HTML styling with Databricks brand colors. The email must be fully self-contained — no external CSS or image references.

### Step 6: Send Email

Use the gmail skill's `gmail_builder.py` to send the HTML email:

```bash
GMAIL_BUILDER=$(ls ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/gmail/resources/gmail_builder.py 2>/dev/null | sort -V | tail -1)

python3 "$GMAIL_BUILDER" send \
  --to "{RECIPIENTS}" \
  --subject "[Databricks] {REPORT_PERIOD} Consumption Report — {ACCOUNT_NAME} ({DATE_RANGE})" \
  --html /tmp/consumption_report/{ACCOUNT_NAME}/email.html
```

Confirm with the user before sending.

## Scheduling

To run this report on a recurring basis (e.g., every Monday morning), use the `fe-macos-scheduler` plugin:

```
Schedule a weekly task every Monday at 8am to generate a consumption report for Acme Corp and email it to [email protected]
```

This creates a local macOS launchd job that invokes Claude with the consumption report prompt on the specified schedule.

## Data Source Reference

| Table | Data | Used In |
|-------|------|---------|
| `main.fin_live_gold.paid_usage_metering` | Spend, products, workspaces, serverless flags | Queries 1-6, 11-12, 16 |
| `main.fin_live_gold.contract_daily_burn_down` | Contract commitment and cumulative burn | Query 7 |
| `main.gtm_gold.account_active_users_daily` | Daily active user counts | Queries 8-10 |
| `main.gtm_gold.rpt_account_tech_compete` | Competitor technology landscape | Query 13 |
| `main.data_dbsql.dbsql_workload_agg` | BI/partner tool usage and revenue | Queries 14-15 |

## Troubleshooting

- **"Table not found" errors:** Ensure you're using `--profile logfood` and have access to the logfood workspace. Run `databricks auth token --profile logfood` to verify authentication.
- **Empty results:** Verify the account name matches exactly (case-sensitive). Try a LIKE query first: `WHERE account_name LIKE '%{partial_name}%'` to find the exact name. The `dbsql_workload_agg` table uses `canonicalCustomerName` instead of `account_name`.
- **Contract burndown shows equal values:** You may be hitting `consolidated_active_contracts` by mistake — always use `contract_daily_burn_down`.
- **Charts not rendering:** Ensure `matplotlib` is installed: `pip install matplotlib pandas`.
- **Warehouse timeout:** If queries take longer than 30s, increase `wait_timeout` to `"60s"` or use a larger warehouse. Alternatively, reduce `lookback_months` to narrow the date range.
- **Logfood authentication expired:** Re-authenticate with `databricks auth login --host https://adb-2548836972759138.18.azuredatabricks.net --profile logfood`.
- **Gmail send fails:** Verify Google auth with `/google-auth`. The HTML file is saved to `/tmp/consumption_report/{ACCOUNT_NAME}/email.html` — you can attach it manually if Gmail API is unavailable.

## Empty Data Handling

If any query returns zero rows, handle gracefully:

- **Charts:** Skip chart generation for that query. In the email section, show a gray placeholder: "No data available for this period."
- **Tables:** Show a single row: "No data found for {ACCOUNT_NAME} in this date range."
- **TL;DR:** Only include bullets for sections with data. If spend data is empty, note "No consumption data found — verify account name."
- **Contract burndown:** If no contract data, show "No active contract found" instead of a chart.
- **Competitor/BI tools:** If empty, show "No competitive intelligence data available" or "No BI tool attribution data found."
