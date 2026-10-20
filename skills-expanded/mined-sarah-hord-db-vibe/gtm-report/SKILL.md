---
name: gtm-report
description: "Generate an HTML consumption intelligence report for a Databricks customer account. Accepts an account name or Salesforce Account ID."
user_invocable: true
---

# GTM Consumption Report

Generate a full HTML consumption intelligence report for a customer account using the GTM Gold SQL functions deployed on Databricks.

## Input

The user provides one of:
- An **account name** (e.g., "Mastercard", "Block")
- A **Salesforce Account ID** (18-char, e.g., "0016100001BMQc7AAH")

Optional flags:
- **include_analysis** — Include AI-generated strategic insight (slower, ~20s). Default: off.
- **model** — AI model endpoint for analysis. Options: `databricks-gpt-5-2` (default), `databricks-claude-opus-4-5` (premium), `databricks-gemini-2-5-pro` (budget).

## Workflow

### Step 1: Resolve Account ID

If the user provides an account name (not an 18-char ID), look up the account ID:

```sql
SELECT DISTINCT account_id, account_name
FROM main.gtm_gold.workspace_consumption_daily
WHERE LOWER(account_name) LIKE '%<search_term>%'
LIMIT 10
```

Use the `query_gtm_gold` MCP tool or the Databricks `execute_sql` tool. If multiple matches, ask the user to pick one.

### Step 2: Generate Report

Call `fn_consumption_report` via SQL:

```sql
-- Fast mode (no AI analysis)
SELECT main.gtm_functions.fn_consumption_report('<account_id>')

-- With AI analysis
SELECT main.gtm_functions.fn_consumption_report('<account_id>', TRUE)

-- Premium AI model
SELECT main.gtm_functions.fn_consumption_report('<account_id>', TRUE, 'databricks-claude-opus-4-5')
```

Use the `query_gtm_gold` MCP tool or Databricks `execute_sql` to run this query.

> **Schema note:** The production functions are deployed to `main.gtm_functions`. For dev/testing, use `users.<your_schema>` if you deployed your own copy via the DAB bundle.

### Step 3: Save and Present

1. The function returns a complete HTML string.
2. Save the HTML to a local file: `/tmp/gtm-report-<account_name>-<date>.html`
3. Open the file in the browser: `open /tmp/gtm-report-<account_name>-<date>.html`
4. Tell the user the report is ready and provide the file path.

## Report Sections

The generated HTML report includes:
- **Account metadata** — AE, industry, T3M spend, active workspaces
- **Quarterly progress** — QTD attainment vs target with progress bar (when target data exists)
- **Strategic Insight** — AI-generated analysis (when `include_analysis=TRUE`)
- **Executive Summary (BLUF)** — Daily spend, 7-day trend, top mover, conviction level, recommended action
- **Top Movers** — Workspaces with largest 7-day change (spike/drop/shift badges)
- **Spend by Product** — SKU breakdown (Jobs, SQL, All Purpose, Model Serving, etc.)
- **Top Workspaces** — Ranked by daily spend with change indicators
- **Business Unit Breakdown** — Spend grouped by BU with workspace counts
- **Recommended Actions** — Prioritized next steps (AI-generated when analysis enabled)

## Example Usage

```
/gtm-report Mastercard
/gtm-report 0016100001BMQc7AAH
/gtm-report Block --with-analysis
/gtm-report Instacart --model databricks-claude-opus-4-5
```

## Prerequisites

- Databricks authentication configured (use `databricks-authentication` skill if needed)
- SQL warehouse accessible
- GTM Gold SQL functions deployed to `main.gtm_functions` (prod) or `users.<your_schema>` (dev). See `gtm-functions/` DAB bundle.
