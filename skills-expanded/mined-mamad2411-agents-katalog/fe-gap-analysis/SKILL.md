---
name: fe-gap-analysis
description: Generate customer-specific product heatmaps with tiered opportunity scoring across the Databricks portfolio. Pulls data from Logfood, Salesforce UCOs, Google Drive, Slack, and JIRA ES tickets to produce a structured Google Sheet with MRR data, adoption status, and End Analysis scoring.
user-invocable: true
model: opus
---

# Gap Analysis Heatmap Skill

Generate customer-specific gap analysis heatmaps for identifying Databricks product upsell opportunities.

## Skill Invocation

```bash
/fe-gap-analysis <customer_name>
```

**Examples**:
```bash
/fe-gap-analysis "ModMed"
/fe-gap-analysis "Acme Corporation"
```

## Workflow

When this skill is invoked, follow these steps systematically:

### Step 0: Prerequisites - MCP Authentication Check

**CRITICAL**: Before running any data collection, verify MCP connections are authenticated.

**A. Check Databricks CLI Authentication**

```bash
databricks auth profiles | grep logfood
```

If not authenticated:
```bash
databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood
```

**B. Check MCP Connection Credentials**

Get user ID:
```bash
USER_ID=$(databricks current-user me --profile logfood | jq -r '.id')
```

Check each MCP connection:
```bash
# JIRA MCP
databricks api get /api/2.1/unity-catalog/connections/jira-mcp/user-credentials/$USER_ID --profile logfood

# Slack
databricks api get /api/2.1/unity-catalog/connections/slack/user-credentials/$USER_ID --profile logfood

# Glean MCP
databricks api get /api/2.1/unity-catalog/connections/glean-mcp/user-credentials/$USER_ID --profile logfood
```

**C. Evaluate Results**

For each connection, check `access_token_expiration`. If expired, the user must re-authenticate:

| Connection | Re-auth URL |
|------------|-------------|
| JIRA MCP | https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/jira-mcp?o=2548836972759138 |
| Slack | https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/slack?o=2548836972759138 |
| Glean MCP | https://adb-2548836972759138.18.azuredatabricks.net/explore/connections/glean-mcp?o=2548836972759138 |

**D. Check Google Authentication**

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py status
```

If not authenticated, run:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py login
```

**E. Check Salesforce Authentication**

```bash
sf org display | grep "Connected Status"
```

If not connected, run:
```bash
sf org login web --instance-url=https://databricks.my.salesforce.com/
```

**Only proceed to Step 1 once all required MCPs show ACTIVE status or the user has completed re-authentication.**

### Step 1: Data Collection

**CRITICAL - Launch Background Research First**

Before running any Logfood queries, immediately launch the following four research tasks **in parallel** (they are slow and can run while Logfood queries execute):

1. **Google Docs background agent** — Use `Task` tool with `subagent_type=fe-google-tools:google-drive`, `run_in_background=true`:
   - Search Glean for all Google Drive docs mentioning the customer (since January 1, 2024)
   - Read top 4-5 docs (meeting notes, QBR, account plan, onsite notes, exec calls)
   - Return structured insights per product area with dates
   - **Ignore any document content dated before 2024-01-01**

2. **Slack comprehensive search** — Run these searches (separate queries, no OR syntax). **Only use messages from 2024-01-01 onward — discard older results.**
   - `<customer_name> lakebase` or `<customer_name> lakefusion`
   - `<customer_name> jobs serverless` or `<customer_name> workflows`
   - `<customer_name> DLT` or `<customer_name> lakeflow`
   - `<customer_name> model serving` or `<customer_name> AI gateway`
   - `<customer_name> genie` or `<customer_name> AI/BI` or `<customer_name> looker`
   - `<customer_name> vector search` or `<customer_name> MLflow`
   - `<customer_name> unity catalog`
   - General channel: `in:#<customer-slack-channel>` for recent messages
   - For each result, extract key insights with Slack message timestamps (convert UNIX ts to date) — skip any message before 2024-01-01

3. **UCO full details query** — Pull all UCOs including descriptions and next steps:
   ```sql
   SELECT DISTINCT
       u.Name, u.DemandPlanStage__c as stage,
       SUBSTRING(u.Description__c, 1, 500) as description,
       DATE(u.CustomLastModifiedDate__c) as last_modified,
       SUBSTRING(u.Demand_Plan_Next_Steps__c, 1, 300) as next_steps,
       u.Competitor_Status__c
   FROM main.sfdc_bronze.usecase__c u
   JOIN main.sfdc_bronze.account a ON u.Account__c = a.Id
   WHERE LOWER(a.Name) LIKE LOWER('%<customer_name>%')
       AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
       AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
       AND u.CustomLastModifiedDate__c >= '2024-01-01'
   ORDER BY u.CustomLastModifiedDate__c DESC
   ```
   Extract: blockers, action items, timelines, competitor mentions from descriptions and next_steps fields.

4. **JIRA ES ticket search** — Search for ES tickets mentioning the customer (2024 onward only):
   - Use the JIRA MCP to search: `project = ES AND text ~ "<customer_name>" AND created >= "2024-01-01" ORDER BY created DESC`
   - Also try: `project = ES AND "Account Name" ~ "<customer_name>" AND updated >= "2024-01-01" ORDER BY updated DESC`
   - Look for: custom configurations granted, escalations, feature requests, white-glove status, billing anomalies
   - Extract ticket IDs, summaries, and resolution notes for each product area
   - **Skip any ticket created before 2024-01-01**

**Do NOT write any Notes column values until all four research tasks are complete.** Compile all findings first, then do a single batch update of all Notes cells. **Discard any notes, Slack messages, JIRA tickets, or Google Doc content dated before 2024-01-01 — they are not relevant.**

---

**A. Query Logfood for MRR/Usage Data (VERIFIED QUERY)**

Connect to logfood workspace: `https://adb-2548836972759138.18.azuredatabricks.net/`

```sql
-- WORKING QUERY (verified 2026-02-19)
SELECT
    usage_date,
    sku,
    sku_type,
    SUM(dbu_dollars) as dbu_dollars,
    SUM(dbu_quantity) as dbu_quantity
FROM main.gtm_data.c360_consumption_monthly
WHERE LOWER(account_name) LIKE LOWER('%<customer_name>%')
    AND usage_date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY usage_date, sku, sku_type
HAVING SUM(dbu_dollars) > 0
ORDER BY usage_date DESC, dbu_dollars DESC
```

**Key columns in c360_consumption_monthly**:
- `dbu_dollars` - Total DBU dollars
- `dbu_quantity` - Total DBU quantity
- `dbu_dollars_uc` - Unity Catalog dollars (alternative to paid_usage_metering)
- `dbu_dollars_genai_foundation_model_api` - Foundation Model API dollars
- `dbu_dollars_serverless` - Serverless dollars
- `dbu_dollars_sql` - SQL dollars

**CLI Execution**:

> **Note**: Get your warehouse ID first by running `databricks warehouses list --profile=logfood` and picking a running SQL warehouse, or invoke the `fe-workflows:databricks-warehouse-selector` skill.

```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json '{
  "statement": "<SQL_ABOVE>",
  "warehouse_id": "<YOUR_LOGFOOD_WAREHOUSE_ID>",
  "format": "JSON_ARRAY",
  "wait_timeout": "50s"
}'
```

Store results for later use.

**A2. Query Unity Catalog Dollars (paid_usage_metering)**

Unity Catalog consumption is tracked separately in `main.fin_live_gold.paid_usage_metering`:

```sql
-- Unity Catalog dollars by month
SELECT
    YEAR(date) as year,
    MONTH(date) as month,
    SUM(workload_insights_metric.uc_dollars) as uc_dollars,
    SUM(workload_insights_metric.uc_dbu) as uc_dbu
FROM main.fin_live_gold.paid_usage_metering
WHERE LOWER(sfdc_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(date), MONTH(date)
ORDER BY year DESC, month DESC
LIMIT 4
```

This table also contains detailed `product_lines_metric` struct with breakdowns for:
- `interactive` (notebook_classic_dollars, notebook_serverless_dollars)
- `lakeflow` (lakeflow_pipelines_dollars, automated_jobs_dollars)
- `data_warehousing` (dbsql_dollars)
- `ai` (foundation_model_api_dollars, ml_serving_serverless_cpu_dollars, vector_search_dollars, etc.)

**A3. Query Foundation Model API Dollars (paid_usage_metering)**

Foundation Model Serving PPT and PT are in `product_lines_metric.ai`:

```sql
-- Foundation Model API dollars by month (PPT and PT)
SELECT
    YEAR(date) as year,
    MONTH(date) as month,
    SUM(product_lines_metric.ai.foundation_model_api_dollars) as fmapi_ppt_dollars,
    SUM(product_lines_metric.ai.foundation_model_api_pt_dollars) as fmapi_pt_dollars
FROM main.fin_live_gold.paid_usage_metering
WHERE LOWER(sfdc_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(date), MONTH(date)
ORDER BY year DESC, month DESC
LIMIT 4
```

For detailed activity logs (request counts, tokens, models used), query `main.eng_foundation_model_api.1pp_activity_logs_last_30d`:

```sql
-- Foundation Model API activity details
SELECT
    DATE_TRUNC('month', _event_time) as month,
    activity.serving_request_endpoint_log.product_type,
    activity.serving_request_endpoint_log.foundation_model_activity.client_used,
    COUNT(*) as request_count,
    SUM(activity.serving_request_endpoint_log.foundation_model_activity.num_input_tokens) as input_tokens,
    SUM(activity.serving_request_endpoint_log.foundation_model_activity.num_output_tokens) as output_tokens
FROM main.eng_foundation_model_api.1pp_activity_logs_last_30d
WHERE LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
GROUP BY 1, 2, 3
ORDER BY month DESC
```

**A4. Query Lakeflow, DLT, Jobs, DBSQL, and All Purpose Dollars (emerging_data)**

Lakeflow Connect, DLT, Jobs, DBSQL, and All Purpose from `main.field_usage_dashboard.emerging_data`:

```sql
-- Comprehensive compute/SQL dollars by month
SELECT
    YEAR(date) as year,
    MONTH(date) as month,
    -- Lakeflow Connect & DLT
    SUM(lakeflow_connect_dbu_dollars) as lakeflow_connect,
    SUM(dlt_dbu_dollars) as dlt_classic,
    SUM(dlt_serverless_dbu_dollars) as dlt_serverless,
    -- Jobs/Workflows
    SUM(automated_dbu_dollars) as jobs_classic,
    SUM(automated_serverless_dbu_dollars) as jobs_serverless,
    -- DBSQL
    SUM(dbsql_classic_dbu_dollars) as dbsql_classic,
    SUM(dbsql_pro_dbu_dollars) as dbsql_pro,
    SUM(dbsql_serverless_dbu_dollars) as dbsql_serverless,
    -- All Purpose/Interactive
    SUM(interactive_dbu_dollars) as all_purpose_classic,
    SUM(interactive_serverless_dbu_dollars) as all_purpose_serverless,
    -- AI/ML Products
    SUM(cpu_model_serving_dbu_dollars) as serving_cpu,
    SUM(gpu_model_serving_dbu_dollars) as serving_gpu,
    SUM(foundation_model_api_dbu_dollars) as fmapi_ppt,
    SUM(throughput_model_serving_dbu_dollars) as fmapi_pt,
    SUM(batch_inference_model_serving_dbu_dollars) as batch_inference,
    SUM(vector_search_dbu_dollars) as vector_search,
    SUM(foundation_model_training_dbu_dollars) as model_training
FROM main.field_usage_dashboard.emerging_data
WHERE LOWER(Account) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(date), MONTH(date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**Key columns in emerging_data**:
- `lakeflow_connect_dbu_dollars` - Lakeflow Connect (Row 4)
- `dlt_dbu_dollars` - DLT/Lakeflow Pipelines Classic (Row 5)
- `dlt_serverless_dbu_dollars` - DLT/Lakeflow Pipelines Serverless (Row 6)
- `automated_dbu_dollars` - Workflows/Jobs Classic (Row 7)
- `automated_serverless_dbu_dollars` - Workflows/Jobs Serverless (Row 8)
- `dbsql_classic_dbu_dollars` - DBSQL Classic (Row 9)
- `dbsql_pro_dbu_dollars` - DBSQL Pro (Row 10)
- `dbsql_serverless_dbu_dollars` - DBSQL Serverless (Row 11)
- `interactive_dbu_dollars` - All Purpose Classic (Row 12)
- `interactive_serverless_dbu_dollars` - All Purpose Serverless (Row 13)
- `cpu_model_serving_dbu_dollars` - Model Serving CPU (Row 16)
- `gpu_model_serving_dbu_dollars` - Model Serving GPU (Row 17)
- `batch_inference_model_serving_dbu_dollars` - Batch Inference (Row 21)
- `vector_search_dbu_dollars` - Vector Search (Row 22)
- `foundation_model_training_dbu_dollars` - Model Training (Row 24)

**Note**: This table uses `Account` column (not `account_name` or `salesforce_account_name`).

**A5. Query AI Gateway Dollars (account_consumption_daily)**

AI Gateway consumption from `main.gtm_gold.account_consumption_daily`:

```sql
-- AI Gateway dollars by month
SELECT
    YEAR(usage_date) as year,
    MONTH(usage_date) as month,
    SUM(ai_gateway_dbu_dollars) as ai_gateway_dollars
FROM main.gtm_gold.account_consumption_daily
WHERE LOWER(account_name) LIKE LOWER('%<customer_name>%')
    AND usage_date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(usage_date), MONTH(usage_date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**Key columns in account_consumption_daily**:
- `ai_gateway_dbu_dollars` - AI Gateway dollars (Row 15)
- `agent_evals_dbu_dollars` + `agent_evals_synthetic_data_dbu_dollars` - Agent Eval / Synthetic Data (Row 23)
- `foundation_model_training_dbu_dollars` - Model Training (Row 24)

**A6. Query FMAPI by Provider (product_usage_dollars)**

Foundation Model API consumption broken out by provider from `main.data_df_metering.product_usage_dollars`:

```sql
-- FMAPI dollars by provider by month
SELECT
    YEAR(date) as year,
    MONTH(date) as month,
    SUM(CASE WHEN sku LIKE '%ANTHROPIC_MODEL_SERVING' THEN dollars ELSE 0 END) as fmapi_anthropic,
    SUM(CASE WHEN sku LIKE '%GEMINI_MODEL_SERVING' THEN dollars ELSE 0 END) as fmapi_gemini,
    SUM(CASE WHEN sku LIKE '%OPENAI_MODEL_SERVING' THEN dollars ELSE 0 END) as fmapi_openai
FROM main.data_df_metering.product_usage_dollars
WHERE product_type = 'FOUNDATION_MODEL_API'
    AND LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(date), MONTH(date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**FMAPI SKU patterns** (in product_usage_dollars):
- FMAPI Anthropic (Row 18): `%ANTHROPIC_MODEL_SERVING` (includes ENTERPRISE_ and PREMIUM_)
- FMAPI Gemini (Row 19): `%GEMINI_MODEL_SERVING`
- FMAPI OpenAI (Row 20): `%OPENAI_MODEL_SERVING`

**Key columns**:
- `product_type = 'FOUNDATION_MODEL_API'` - filters to FMAPI only
- `salesforce_account_name` - customer account name
- `dollars` - total dollars (not DBU dollars)

**A7. Query Clean Rooms & Model Training Dollars (sku_consumption_daily)**

Clean Rooms and Model Training consumption from `main.gtm_gold.sku_consumption_daily`:

```sql
-- Clean Rooms dollars by month
SELECT
    YEAR(usage_date) as year,
    MONTH(usage_date) as month,
    SUM(dbu_dollars) as clean_rooms_dollars
FROM main.gtm_gold.sku_consumption_daily
WHERE LOWER(account_name) LIKE LOWER('%<customer_name>%')
    AND sku = 'premium_clean_rooms_collaborator'
    AND usage_date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(usage_date), MONTH(usage_date)
ORDER BY year DESC, month DESC
LIMIT 4

-- Model Training dollars by month
SELECT
    YEAR(usage_date) as year,
    MONTH(usage_date) as month,
    SUM(dbu_dollars) as model_training_dollars
FROM main.gtm_gold.sku_consumption_daily
WHERE LOWER(account_name) LIKE LOWER('%<customer_name>%')
    AND sku LIKE '%model_training%'
    AND usage_date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(usage_date), MONTH(usage_date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**Key columns in sku_consumption_daily**:
- `dbu_dollars` - Dollars for the SKU
- `sku` filters:
  - Clean Rooms (Row 32): `premium_clean_rooms_collaborator`
  - Model Training (Row 24): `%model_training%`
  - Managed Storage (Row 37): `%databricks_storage%`

**A7b. Query Unity Catalog Dollars (paid_usage_metering)**

> **CRITICAL**: Unity Catalog does NOT appear as a standalone `product_type` in `product_usage_dollars`. UC charges are embedded as the `workload_insights_metric.uc_dollars` sub-metric within SQL/Jobs/All-Purpose compute rows. Always use this query — querying by product_type will return $0.

```sql
SELECT
    DATE_TRUNC("MONTH", date) as month,
    SUM(workload_insights_metric.uc_dollars) as uc_dollars
FROM main.fin_live_gold.paid_usage_metering
WHERE LOWER(sfdc_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY 1
ORDER BY 1 DESC
LIMIT 4
```

Use the `uc_dollars` result for the **Unity Catalog** row MRR columns in the Heatmap.

**A8. Query Platform Features (product_usage_dollars)**

Lakehouse Monitoring, Predictive Optimization, and Delta Sharing from `main.data_df_metering.product_usage_dollars`:

```sql
-- Platform features dollars by month
SELECT
    YEAR(date) as year,
    MONTH(date) as month,
    SUM(CASE WHEN product_type = 'LAKEHOUSE_MONITORING' THEN dollars ELSE 0 END) as lakehouse_monitoring_dollars,
    SUM(CASE WHEN product_type = 'PREDICTIVE_OPTIMIZATION' THEN dollars ELSE 0 END) as predictive_optimization_dollars,
    SUM(CASE WHEN product_type = 'DATA_SHARING' THEN dollars ELSE 0 END) as delta_sharing_dollars
FROM main.data_df_metering.product_usage_dollars
WHERE product_type IN ('LAKEHOUSE_MONITORING', 'PREDICTIVE_OPTIMIZATION', 'DATA_SHARING')
    AND LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(date), MONTH(date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**Product type values**:
- Lakehouse Monitoring (Row 35): `product_type = 'LAKEHOUSE_MONITORING'`
- Predictive Optimization (Row 36): `product_type = 'PREDICTIVE_OPTIMIZATION'`
- Delta Sharing (Row 34): `product_type = 'DATA_SHARING'`

**A9. Query Genie Dollars (customer_metrics)**

Genie consumption from `data_product_features.customer_metrics`:

```sql
-- Genie dollars by month
SELECT
    YEAR(date) as year,
    MONTH(date) as month,
    SUM(genie_dollars) as genie_dollars
FROM data_product_features.customer_metrics
WHERE LOWER(customer_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(date), MONTH(date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**Key columns in customer_metrics**:
- `genie_dollars` - Genie dollars (Row 31)
- Filter uses `customer_name` column

**A10. Query Apps and Lakebase Dollars (silver_paid_usage_metering)**

Databricks Apps and Lakebase consumption from `main.field_customer_insights.silver_paid_usage_metering`:

```sql
-- Apps and Lakebase dollars by month
SELECT
    YEAR(daily_date) as year,
    MONTH(daily_date) as month,
    SUM(apps_dollars) as apps_dollars,
    SUM(lakebase_dollars) as lakebase_dollars
FROM main.field_customer_insights.silver_paid_usage_metering
WHERE LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
    AND daily_date >= DATE_SUB(CURRENT_DATE(), 120)
GROUP BY YEAR(daily_date), MONTH(daily_date)
ORDER BY year DESC, month DESC
LIMIT 4
```

**B. Query Salesforce for Use Cases (UCO References Column)**

The full UCO details query was already launched in the pre-pass above. Additionally run this joined query to map UCOs to product SKUs for Column I:

```sql
-- Query UCOs with product mapping (deduplicated)
SELECT DISTINCT
    u.Id,
    u.Name,
    u.DemandPlanStage__c as stage,
    f.use_case_product as products,
    f.estimated_quarterly_dollars,
    u.Demand_Plan_Next_Steps__c as next_steps
FROM main.sfdc_bronze.usecase__c u
JOIN main.sfdc_bronze.account a ON u.Account__c = a.Id
LEFT JOIN main.metric_store.fct_salesforce_use_case f
    ON u.Id = f.salesforce_use_case_id
    AND f.ds = (SELECT MAX(ds) FROM main.metric_store.fct_salesforce_use_case)
WHERE LOWER(a.Name) LIKE LOWER('%<customer_name>%')
    AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
    AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
ORDER BY u.DemandPlanStage__c DESC
```

**Search for specific products in UCO name** (when products field doesn't capture all):

```sql
-- Find UCOs mentioning Lakebase/Online Tables in name
SELECT DISTINCT u.Id, u.Name, u.DemandPlanStage__c as stage
FROM main.sfdc_bronze.usecase__c u
JOIN main.sfdc_bronze.account a ON u.Account__c = a.Id
WHERE LOWER(a.Name) LIKE LOWER('%<customer_name>%')
    AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
    AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
    AND (LOWER(u.Name) LIKE '%lakebase%' OR LOWER(u.Name) LIKE '%lakefusion%' OR LOWER(u.Name) LIKE '%online table%')
```

**UCO Stage Values**: U1, U2, U3, U4, U5, U6, Lost

**UCO-to-SKU Product Mapping**:

Search **BOTH** the `use_case_product` field AND the UCO `Name` field for product keywords:

| Search For (in products OR name) | Heatmap Product Rows |
|----------------------------------|----------------------|
| `Lakeflow Jobs` | Workflows/Jobs Classic (Row 7), Workflows/Jobs Serverless (Row 8) |
| `Lakeflow Pipeline` | DLT Classic (Row 5), DLT Serverless (Row 6) |
| `Unity Catalog`, `UC` | Unity Catalog* (Row 27) |
| `DWH`, `Data Warehousing`, `SQL` | DBSQL Classic (Row 9), DBSQL Pro (Row 10), DBSQL Serverless (Row 11) |
| `AI`, `GenAI`, `ML` | Model Serving CPU (Row 16), Model Serving GPU (Row 17), FMAPI rows (18-20) |
| `AI/BI`, `Genie` | AI/BI* (Row 30), Genie* (Row 31) |
| `Collaboration`, `Sharing` | Delta Sharing* (Row 34), Clean Rooms (Row 32) |
| `Vector Search` | Vector Search (Row 22) |
| `AI Gateway` | AI Gateway (Row 15) |
| `Lakebase`, `Online Tables`, `LakeFusion` | Online Tables / Lakebase (Row 26) |
| `Apps`, `Databricks Apps` | Databricks Apps (Row 14) |

**IMPORTANT**: UCO names often contain product references NOT in the structured `use_case_product` field. Always search both fields.

Example: UCO "Widget Experience App via Lakebase" has `use_case_product = "Unity Catalog;AI;Lakeflow Connect"` but name mentions Lakebase.

**Salesforce UCO URL Format**:
`https://databricks.lightning.force.com/lightning/r/Use_Case__c/<UCO_ID>/view`

**Competitive Signal Fields**: Check `Competitor_Status__c` and description for competitor mentions (Snowflake, SageMaker, etc.)

**For Notes**: Extract from `Description__c` and `Demand_Plan_Next_Steps__c`: blockers, action items, timelines, competitor mentions. These feed the Notes column alongside Google Docs and Slack.

**C. Google Drive Research (Background Agent)**

This was launched in the pre-pass. Wait for the background agent to complete before writing Notes.

If the agent has not yet been launched, do so now with `subagent_type=fe-google-tools:google-drive`, `run_in_background=true`:
- Search Glean: `"<customer_name>" datasource:gdrive` to find all relevant docs
- Read the top 4-5 documents (prioritize: onsite notes, exec call notes, QBR, account plan, CDC/technical notes)
- Return structured insights organized by product area with source document name and date

**D. Slack Research (Comprehensive Pre-Pass)**

This was launched in the pre-pass. If not yet done, run these Slack searches before writing Notes (use `search.messages` endpoint, separate queries per topic):

| Topic | Query |
|-------|-------|
| Lakebase/Fusion | `<customer_name> lakebase` |
| CDC/Lakeflow | `<customer_name> DLT` or `<customer_name> lakeflow` |
| Jobs/Workflows | `<customer_name> jobs serverless` |
| AI/Model Serving | `<customer_name> model serving` |
| AI Gateway | `<customer_name> ai gateway` |
| AI/BI & Looker | `<customer_name> looker` or `<customer_name> AIBI` |
| Vector Search/MLflow | `<customer_name> vector search` |
| General | `in:#<customer-channel>` (last 50 messages) |

**Note**: Slack does not support OR syntax between keywords — run separate queries per topic. Convert UNIX timestamps to dates for the `[YYYY-MM-DD]` note format.

**D. Peer Benchmarking**

Compare target account against industry peers to identify over/under-indexed workloads.

**D1. Identify Account's Industry Vertical and Annual Spend**

```sql
SELECT industry_vertical, salesforce_account_name, SUM(dollars) as annual_spend
FROM main.data_df_metering.product_usage_dollars
WHERE LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY industry_vertical, salesforce_account_name
```

**D2. Find Peer Accounts (4-8 companies)**

Select peers based on:
- Same industry vertical
- Annual spend between 10% and 5x of target account (filter out too small/large)
- Minimum $50K annual spend

```sql
SELECT salesforce_account_name, SUM(dollars) as annual_spend
FROM main.data_df_metering.product_usage_dollars
WHERE industry_vertical = '<VERTICAL>'
    AND date >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY salesforce_account_name
HAVING SUM(dollars) BETWEEN <TARGET_SPEND * 0.1> AND <TARGET_SPEND * 5>
    AND SUM(dollars) >= 50000
ORDER BY annual_spend DESC
LIMIT 8
```

**D3. Calculate Peer SKU Mix (% of Total Spend)**

The index must compare **percentage of total spend** per SKU, not raw dollars. This normalizes for account size.

```sql
-- Get peer SKU % of total spend
WITH peer_totals AS (
    SELECT salesforce_account_name, SUM(dollars) as total_spend
    FROM main.data_df_metering.product_usage_dollars
    WHERE salesforce_account_name IN ('<PEER1>', '<PEER2>', '<PEER3>', '<PEER4>')
        AND date >= DATE_SUB(CURRENT_DATE(), 365)
    GROUP BY salesforce_account_name
),
peer_by_product AS (
    SELECT p.salesforce_account_name, p.product_type,
           SUM(p.dollars) as product_spend, t.total_spend,
           (SUM(p.dollars) / t.total_spend * 100) as pct_of_total
    FROM main.data_df_metering.product_usage_dollars p
    JOIN peer_totals t ON p.salesforce_account_name = t.salesforce_account_name
    WHERE p.date >= DATE_SUB(CURRENT_DATE(), 365)
    GROUP BY p.salesforce_account_name, p.product_type, t.total_spend
)
SELECT product_type, AVG(pct_of_total) as avg_pct_of_spend
FROM peer_by_product
GROUP BY product_type
ORDER BY avg_pct_of_spend DESC
```

```sql
-- Get target account SKU % of total spend
WITH target_total AS (
    SELECT SUM(dollars) as total_spend
    FROM main.data_df_metering.product_usage_dollars
    WHERE LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
        AND date >= DATE_SUB(CURRENT_DATE(), 365)
)
SELECT product_type,
       SUM(dollars) as product_spend,
       (SUM(dollars) / (SELECT total_spend FROM target_total) * 100) as pct_of_total
FROM main.data_df_metering.product_usage_dollars
WHERE LOWER(salesforce_account_name) LIKE LOWER('%<customer_name>%')
    AND date >= DATE_SUB(CURRENT_DATE(), 365)
GROUP BY product_type
ORDER BY pct_of_total DESC
```

**D4. Calculate Index and Analyze**

**Index Formula:** `(Target % of Total) / (Peer Avg % of Total) * 100`

Example: If target puts 0.21% into DLT and peers put 12.7%, index = 0.21/12.7 = 1.7%

| Index Range | Interpretation | Action |
|-------------|---------------|--------|
| **<50%** | Significantly under-indexed | 🔴 EXPAND - major growth opportunity |
| **50-80%** | Moderately under-indexed | EXPAND - room for growth |
| **80-120%** | At parity | Maintain current trajectory |
| **>120%** | Over-indexed | ✅ DEFEND - account strength |

**Product Grouping Rules:**
- **Combine ALL_PURPOSE + INTERACTIVE** as "Interactive Compute" - these are similar dev/notebook workloads
- **JOBS over-indexing is positive** - indicates mature ops with production workloads properly scheduled vs ad-hoc notebooks
- High JOBS % with low Interactive % = operationally mature customer (good sign)
- High Interactive % with low JOBS % = opportunity to productionize workloads

**Industry Verticals** (in product_usage_dollars):
- FinServ, Tech, HLS (Healthcare/Life Sciences), Retail & CPG
- Manufacturing & Auto, Travel & Hospitality, Transportation
- Energy & Utilities, PubSec & Fed, Consulting & Services, CME

**Peer Filtering Rules:**
- Exclude if annual spend < $50K (too small for meaningful comparison)
- Exclude if annual spend > 5x target (aspirational but not actionable)
- Target 4-8 peers; minimum 2 required for valid benchmark
- If insufficient industry peers, broaden to adjacent verticals

### Step 2: Create Google Sheet

**A. Create New Spreadsheet**

Title: `Gap Analysis - <customer_name> - <YYYY-MM-DD>`

**B. Build Sheet Structure (3 Tabs)**

Create three tabs:

**Tab 1: Heatmap** (product usage data)
Use this structure:
1. Row 1: `Account: <customer_name>`
2. Row 2: Notes header + "Account Level Usage"
3. Row 3: Column headers (Current Status, Month 1 MRR, Month 2 MRR, Month 3 MRR, Notes)
4. Rows 4+: Product rows (32 products across 7 categories)

**Tab 2: End Analysis** (tier-based opportunity prioritization)
- Tier 1 (Whale Bets): Score 20-25
- Tier 2 (Near-Term): Score 13-19
- Tier 3 (Gap Fillers): Score 7-12
- Blocked: Hard blockers present
- Organic Growth: U6 with expansion path

**Tab 3: Peer Benchmarking** (industry comparison)
- Target account vs similar-sized peers in same vertical
- Index = (Target % of spend) / (Peer avg % of spend)
- Identifies gaps and strengths relative to peers

### Step 3: Populate Data

**For Each Product**:

1. **Current Status** (Column D):

   Five values only — determine by combining signals from UCOs, notes, Logfood, and peer benchmarking. Primary signals are UCO stage and qualitative notes — MRR is a supporting signal only (low flat MRR does not mean Adopted).

   **Decision order: Blocked → UCO stage → Notes/Slack/JIRA → MRR as tiebreaker → Not Sure**

   | Status | Primary signals (in order of weight) |
   |--------|--------------------------------------|
   | **Blocked** | Hard blocker confirmed in notes, UCO description, Slack, or JIRA: compliance gap (HIPAA, encryption, FedRAMP), product limitation confirmed by PM/engineering, budget frozen, champion said "not this fiscal year." **Auto-override — assign Blocked regardless of MRR or UCO stage.** |
   | **Adopted** | UCO at U6 (Live) AND notes/Slack/meetings confirm the product is in stable production use. MRR alone is NOT sufficient — low flat MRR with no qualitative confirmation = Not Sure. |
   | **Adopting** | UCO at U4/U5 (Confirming/Onboarding); OR notes/Slack confirm recent go-live or active ramp with named workloads. MoM MRR growth can support this if qualitative signals agree. |
   | **Evaluating** | UCO at U2/U3 (Scoping/Evaluating); OR notes/Slack/JIRA mention POC, pilot, trial, demo, or active champion interest. Peer benchmarking showing heavy peer adoption + any expressed customer interest qualifies. |
   | **Not Sure** | No UCO, no qualitative notes or Slack signal. MRR may or may not exist — absence of engagement signal is the deciding factor. Default. |

   **CRITICAL — UCOs only apply to their own product category:**

   A U6 UCO for one product does NOT imply adoption of a different product, even if both appear in the same workload. Each product row requires its own independent signal.

   | Common mistake | Correct reasoning |
   |----------------|-------------------|
   | Redshift → DBSQL migration UCO is U6, so mark Jobs as Adopted | ❌ Wrong. That UCO proves DBSQL adoption. Jobs may incidentally run DBT orchestration as a side effect, but there is no strategic ETL workload — mark Jobs as **Adopting** at best, only if MRR exists. |
   | UC adoption at 100% → mark Lakehouse Monitoring as Adopted | ❌ Wrong. UC and Monitoring are separate products. Monitoring needs its own signal. |
   | Model Serving CPU in production → mark Model Serving GPU as Adopting | ❌ Wrong. GPU serving requires its own workload confirmation. |

   **Incidental usage rule**: If a product has MRR only because it is a side effect of another product's adoption (e.g., Jobs running DBT as part of a SQL migration, Managed Storage accumulating as data lands), the status is **Adopting** — not Adopted. Adopted requires the product to be an intentional, named workload in its own right.

2. **MRR Columns** (E, F, G):
   - Map product to SKU keywords (see Row Number Verification table in the Implementation Notes section below)
   - Sum MRR for matching SKUs by month
   - Format as `$X,XXX.XX`

3. **Notes** (Column H) - Enriched from Multiple Sources:

   **CRITICAL**: Do NOT write individual Notes cells as you go. Wait until ALL research from Step 1 pre-pass is complete (Google Docs agent, Slack searches, UCO descriptions), then compile all findings and do a single `batchUpdate` call covering all rows at once.

   **Source Priority:**
   1. **Google Docs** - QBRs, meeting notes, account plans, technical docs (background agent from Step 1)
   2. **UCO Descriptions** - `Description__c` and `Demand_Plan_Next_Steps__c` from UCO full details query
   3. **Slack Conversations** - Product-specific keyword searches from Step 1 pre-pass
   4. **Logfood Insights** - Usage patterns, workspace breakdown

   **Format:** `[YYYY-MM-DD] <Source>: <Key insight>`

   **Examples:**
   - `[2026-01-20] Onsite Notes: Strategic priority - Lakebase as Aurora DB replacement for Fusion use case`
   - `[2026-01-16] Exec Call: Jobs outage - no visibility into failure vs slow start; deep dive assigned to Lucian`
   - `[2026-02-01] UCO: Blocker - DDL column drops not supported; Q2 feature expected`
   - `[2025-12-10] Slack: SA confirmed DLT migration planned for Q2; 1,500 tables in scope`
   - `[2026-02-20] Logfood: 3 workspaces using Jobs Serverless, growing MoM`

   **Compilation approach:** For each heatmap product row, gather all matching insights across all three sources, then write the combined note. Multiple insights per row are separated by newlines or semicolons. Most recent insight first.

4. **UCO References** (Column I):
   - Map Salesforce UCOs to product SKUs based on `use_case_product` field
   - Format: `<UCO Name> (<Stage>)`, comma-separated for multiple UCOs
   - Example: `ADL Phase 1 (U6), State Street (U3)`
   - Only include UCOs with matching products (see UCO-to-SKU mapping below)

### Step 4: Score Opportunities & Populate End Analysis Tab

Use the **Prioritization Scoring Model** to score each opportunity across 5 dimensions (1-5 each, max 25 points).

#### Scoring Dimensions

**1. Revenue Potential (1-5)** - Estimated MRR upside if fully adopted:
| Score | Estimated MRR Potential |
|-------|------------------------|
| 5 | >$50K/month |
| 4 | $20K–$50K/month |
| 3 | $10K–$20K/month |
| 2 | $3K–$10K/month |
| 1 | <$3K/month |

*Estimation tips:*
- Adjacent expansions (Classic → Serverless): use current Classic spend as floor
- New products: compare to similar accounts at similar scale
- Competitor displacement: use known competitor contract value as ceiling

**2. Technical Readiness (1-5)** - Technical lift required:
| Score | Condition |
|-------|-----------|
| 5 | Already uses adjacent product; minimal setup |
| 4 | Right platform/infra exists; moderate config needed |
| 3 | Requires SA engagement; weeks of work |
| 2 | Requires significant new infrastructure |
| 1 | Requires new cloud setup or major migration |

*Signals that increase score:*
- Already using Unity Catalog → lowers barrier for Monitoring, Sharing, AI/BI
- Already using Model Serving CPU → lowers barrier for GPU serving
- Already using DLT/DBSQL Classic → Serverless migration is low-lift

**3. Champion Strength (1-5)** - Named champion driving internally:
| Score | Condition |
|-------|-----------|
| 5 | VP+ executive sponsor actively pushing + SA engaged |
| 4 | Architect/Manager champion + regular SA cadence |
| 3 | Identified champion, infrequent engagement |
| 2 | Interest expressed by one person |
| 1 | No champion identified |

*Sources:* UCO `Demand_Plan_Next_Steps__c`, notes, relationship knowledge

**4. Competitive Urgency (1-5)** - Competitor threat level:
| Score | Condition |
|-------|-----------|
| 5 | Actively evaluating competitor right now |
| 4 | Known incumbent (Snowflake/SageMaker/etc.) in use |
| 3 | Competitor mentioned; no active evaluation |
| 2 | No known competitor |
| 1 | Customer committed Databricks-first |

*Competitive signals:*
- "Snowflake" → DBSQL displacement
- "SageMaker/Vertex AI/Azure ML" → GenAI/ML displacement
- "Airflow/dbt" → Lakeflow displacement
- "Pinecone/Chroma/Weaviate" → Vector Search displacement

**5. UCO Momentum (1-5)** - UCO stage and recency:
| Score | Condition |
|-------|-----------|
| 5 | UCO at U3+, modified within 30 days |
| 4 | UCO at U3+, modified within 90 days |
| 3 | UCO at U1-U2, active discussions |
| 2 | No UCO but opportunity well-understood |
| 1 | No UCO; theoretical opportunity |

#### Tier Thresholds

| Tier | Score | Description |
|------|-------|-------------|
| 🌱 **Organic Growth** | N/A | Live U6 use case; expand within same product |
| 🐋 **Tier 1: Whale Bets** | 20–25 | Highest-priority. Deep SA + AE engagement. |
| 🚀 **Tier 2: Near-Term** | 13–19 | Strong near-term wins. Push for trials/PoCs. |
| 🧩 **Tier 3: Gap Fillers** | 7–12 | Long-term nurture. Enablement content/events. |
| 🚫 **Blocked** | Any | Hard blocker present. Must resolve first. |

#### Hard Blockers (Auto-Override to Blocked)

Assign to **Blocked** if ANY of these are true:
- **Compliance gap**: Product not HIPAA/FedRAMP/SOC2 certified for required data
- **Legal restriction**: Contract prohibits feature; legal review pending >90 days
- **Product limitation**: Known limitation, PM confirmed no near-term fix
- **Customer deferral**: Champion said "not this fiscal year" or "budget frozen"
- **Governance freeze**: Customer in data migration/re-org blocking new work

#### Organic Growth Classification

Separate from tier scoring - list alongside tier items if:
- Has U6 UCO (fully in production) AND
- Clear expansion path: more teams adopting, Classic→Serverless migration, adding adjacent GenAI features, expanding Vector Search, adding AI Gateway

#### Special Opportunity Detection

- **FMAPI Contract Consolidation**: If significant spend across 2+ FMAPI providers (Anthropic, Gemini, OpenAI), flag for **Model Contract Consolidation on Databricks** (unified billing, volume discounts, AI Gateway).
- **Serverless Migration**: If >$20K/mo on Classic compute (Jobs, DLT, DBSQL, All Purpose), flag as Tier 1 migration opportunity.
- **Peer-Identified Gaps**: Products where target is significantly under-indexed vs peer average (e.g., DLT, Clean Rooms, Model Serving) should be flagged with peer comparison data in recommendations.

#### Peer-Adjusted Scoring

Use peer benchmarking to adjust opportunity scores:

| Peer Comparison | Score Adjustment | Rationale |
|-----------------|------------------|-----------|
| **Under-indexed >50%** | +1 to Revenue Potential | Peers prove TAM is achievable |
| **Under-indexed >80%** | +2 to Revenue Potential | Major expansion opportunity |
| **Over-indexed** | -1 to Revenue Potential | Already captured; defend position |
| **Peer has product, target doesn't** | +1 to Technical Readiness | Industry pattern validates fit |

**Example peer insight for recommendation:**
> "DLT spend is $3.5K vs peer average of $750K (99% under-indexed). Peers Coinbase, ADP, Mastercard all have significant DLT adoption. Strong expansion opportunity."

#### End Analysis Tab Structure

Create a separate **End Analysis** tab with:

1. **Row 1**: Title bar — "END ANALYSIS — <Customer Name>" (merged, Databricks brand color, white bold text)
2. **Row 2**: Sources line — list all data sources used (italic, gray background, merged)
3. **Row 3**: Column headers — Opportunity | Rev (1-5) | Tech (1-5) | Champion (1-5) | Competitive (1-5) | UCO (1-5) | Total | Tier | **Rationale (AE-Ready)**
4. **Tier section headers**: Merged full-width rows with colored backgrounds per tier (see colors below), bold white text
5. **Scoring rows**: One row per opportunity with dimension scores + rationale
6. **Organic Growth section**: U6 expansions — no scores needed, just Tier=🌱 Organic and rationale
7. **Scoring Key**: At bottom — dimension rubric table for reference

**Column layout (9 columns A–I)**:
| Col | Content | Width |
|-----|---------|-------|
| A | Opportunity name (bold) | 230px |
| B–F | Dimension scores (centered) | 58–80px each |
| G | Total score (bold, centered) | 55px |
| H | Tier label (bold, centered) | 95px |
| I | Rationale (AE-Ready) | 480px |

**Tier section header colors** (white text, merged A:I):
| Section | Background RGB |
|---------|---------------|
| 🐋 Tier 1: Whale Bets | (255, 140, 0) — dark orange |
| 🚀 Tier 2: Near-Term | (31, 97, 141) — dark blue |
| 🚫 Blocked | (180, 0, 0) — dark red |
| 🧩 Tier 3: Gap Fillers | (100, 100, 100) — dark gray |
| 🌱 Organic Growth | (39, 120, 60) — dark green |
| Scoring Key | (60, 60, 60) — near-black |

**Data row background tints** (columns A–H only):
- Tier 1 rows: (255, 243, 224) — light orange
- Tier 2 rows: (227, 242, 253) — light blue
- Blocked rows: (255, 235, 235) — light red
- Tier 3 rows: (245, 245, 245) — light gray
- Organic rows: (232, 245, 233) — light green

**Example scoring rows:**
| Opportunity | Rev | Tech | Champ | Comp | UCO | Total | Tier | Rationale (AE-Ready) |
|-------------|-----|------|-------|------|-----|-------|------|----------------------|
| Looker Migration | 4 | 4 | 5 | 5 | 3 | 21 | 🐋 Tier 1 | Looker contract renews end-of-Q3 — hard deadline. All data already on Databricks. PS scoping a low-to-mid six-figure deal. Next step: Confirm Google Sheets Live Connector support. |
| AI Gateway | 3 | 5 | 3 | 3 | 2 | 16 | 🚀 Tier 2 | Champion flagged QPS limits at last onsite. AI Gateway sits in front of existing FMAPI calls — zero infra change. Next step: Demo using their actual traffic patterns. |
| Jobs Serverless | — | — | — | — | — | — | 🚫 Blocked | Post-outage trust gap. Pitching expansion now would feel tone-deaf. Resolve observability and escalation SLA first, then revisit. |

**Rationale column — writing guidelines:**

The Rationale column is written **for AEs**, not for scoring reviewers. Each cell should:
1. **State the situation** in customer terms (why this matters, what the urgency is)
2. **End with a clear next step** (one action, not a list)

Do NOT use scoring language (Rev=5, Tech=4, etc.) in the Rationale column — the score columns already capture that. Write it like you're briefing an AE before a call.

**Good:** "Addepar's Looker contract renews end-of-Q3 — hard deadline. All underlying data is already on Databricks. PS (Ken Brink) is scoping a low-to-mid six-figure deal. Next step: Confirm Live Connector to Google Sheets support before PS kickoff."

**Bad:** "Rev=4: low-to-mid 6 figures per PS scoping. Tech=4: data already in Databricks. Champion=5: Ken Brink engaged, end-of-Q3 deadline."

**Peer Benchmarking Section — Tab 3 (Separate Sheet)**

> ⚠️ **CONFIDENTIALITY WARNING**: This tab contains names of other Databricks customers and their relative spend data. It is **internal-only** and **must be deleted before sharing the sheet with the customer**. Remind the SA of this in Step 6.

Populate the **Peer Benchmarking tab** (Tab 3) — do NOT append this to the End Analysis tab. This is a standalone sheet. It has three parts:

**Part 1: Section header + context rows**
- Header row: "📊 PEER BENCHMARKING — How Industry Comparison Informed the Tier Scores" (dark teal bg, white bold, merged)
- Context row: "Vertical: <X> | Peers: <Peer1> ($XM), <Peer2> ($XM)... | Target: <Customer> (~$XM | Index = (Target % of spend) ÷ (Peer avg % of spend) × 100" (merged, italic)
- Usage row: One sentence explaining how peer data was actually used in the analysis (merged, italic, light green tint)

**Part 2: Product-by-product table**
Columns: Product | Target % of Spend | Peer Avg % | Index | Impact on End Analysis Scoring

For each product in the peer benchmarking data, write the **Impact** column to explain how the peer index affected tier assignment:

| Scenario | What to write in Impact column |
|----------|-------------------------------|
| Under-indexed + low UCO momentum | "⬆ ELEVATED: Moved from Tier 3 → Tier 2. Peer gap proves TAM exists." |
| Under-indexed + high UCO/notes | "⬆ SUPPORTS Tier 1/2. Peer data validates Revenue Potential score." |
| Near parity (80-120%) | "✔ CONFIRMED PARITY: Organic Growth / no active expansion needed." |
| Over-indexed | "✔ CONFIRMED STRENGTH: Supports organic growth classification / competitive defense." |
| Over-indexed + competitive threat | "✔ CONFIRMS AI LEAD: Supports competitive urgency score — customer is a leader, must defend." |

**Part 3: Key Takeaway — TWO rows**

- **Row 1 (header)**: "KEY TAKEAWAY" — section header row (dark teal bg `(0, 105, 92)`, white bold text, merged full-width). No content in this row, just the label.
- **Row 2 (content)**: The synthesizing paragraph — wrapped text, merged full-width, light teal tint background. This answers: *"Given the peer pattern, what is the real expansion story for this account?"* This is the most important output — it reframes the entire analysis in terms of what peers reveal about the customer's strategic position.

Example content row: "Addepar over-indexes on AI/ML while severely under-indexing on DLT. Most FinServ peers are the inverse. The story is NOT 'get them to try AI' — they're already leading. It's: (1) protect the AI lead vs. AWS, (2) fix the DLT gap with the Arcion migration, (3) land the Looker deal before Q3."

**IMPORTANT**: These are always two separate rows — the header label row and the paragraph content row. Never combine them into one cell.

**Section formatting**: Dark teal headers `(0, 105, 92)`, alternating light teal row tints, peach column headers. Product name bold, % columns centered.

**Scoring Notes:**
- Score conservatively — better to tier down and over-deliver
- Check with SA for technical readiness assessments
- Revenue estimates based on account profile, comparables, AND peer benchmarks
- Blocked items stay Blocked even if score is high
- Update scores quarterly as UCOs advance
- Use peer insights to justify Revenue Potential scores

### Step 5: Apply Formatting

Use Google Sheets API to apply formatting. See **Google Sheets API Implementation Notes** section below for detailed specifications.

**Summary of formatting to apply:**

1. **Row 1**: Merge A1:H1, white background, bold centered "Account: <customer_name>"
2. **Row 2**:
   - Merge A2:D2 for sticky feature note (italic)
   - Merge E2:G2 for "Account Level Usage" (horizontal text, NO rotation, light blue background)
3. **Row 3**: Header row with peach background, bold text
4. **Column A**: Merge A4:A35, add "Databricks Offerings" rotated 90° vertical, peach background
5. **Column B**: Merge cells per category group (see category row ranges), peach background
6. **Status column (D)**:
   - Apply data validation dropdown
   - Apply conditional formatting for cell background colors per status value
7. **MRR columns (E-G)**: Currency format `$#,##0`
8. **Notes column (H)**: Text wrapping enabled, wide column (600px)
9. **All cells**: Enable text wrapping, auto-resize rows
10. **Freeze**: Top 3 rows

### Step 6: Output Summary

Print:
```
✅ Gap Analysis Heatmap Created for <customer_name>

URL: https://docs.google.com/spreadsheets/d/SHEET_ID/edit

Summary:
- Total MRR (latest month): $X,XXX
- Products in use: X/32
- Tier 1 opportunities: X (list top 3)
- Tier 2 opportunities: X (list top 3)
- Blocked: X (list all)

Data sources: Logfood, Salesforce UCOs, Google Drive, Slack, JIRA ES tickets

⚠️  BEFORE SHARING WITH CUSTOMER: Delete the "Peer Benchmarking" tab (Tab 3).
    It contains names of other Databricks customers and is internal-only.
```

## Important Notes

1. **Do NOT copy template notes** - Derive all notes from actual account data
2. **Include dates on all notes** - Format: `[YYYY-MM-DD]`
3. **Handle missing data gracefully** - If Logfood has no data, rely on UCOs/notes
4. **Map SKUs carefully** - Use the Row Number Verification table in the Implementation Notes section
5. **Be conservative with tiers** - Only Tier 1 if genuinely high potential

## Learnings from Customer Run-Throughs

### GoGuardian (2026-02-10)

**Key Findings**:
1. **ES Ticket Gold Mine**: JIRA ES tickets contain critical context missing from UCOs
   - Custom scaling configurations granted
   - White glove monitoring status
   - Historical escalations and resolutions
   - Feature requests and their status

2. **Data Discrepancy Detection**: Flag when ES tickets show active usage but Logfood shows $0
   - Example: Model Serving CPU/GPU showed $0 in billing but ES tickets showed active custom configs
   - Add "ACTION: Investigate billing/data discrepancy" to notes

3. **Partial Month Labeling**: Last month MRR column should indicate "(partial)" if current month
   - Example: "Feb '26 MRR (partial)" instead of just "Feb '26 MRR"

4. **White Glove Status**: Note when customers have special treatment
   - Dedicated engineering monitoring
   - Custom scaling configs approved
   - Multiple customization requests granted

5. **Historical Context**: Include historical MRR when recent data is $0
   - Example: "*Historical: $2.5K-$6.3K monthly through Feb '25"

### Addepar (2026-03-18)

**Key Findings**:
1. **UCO SQL Alias Bug**: Queries using `DISTINCT` + `ORDER BY` original column names fail with `UNRESOLVED_COLUMN`
   - Root cause: `ORDER BY u.DemandPlanStage__c` references original column, but DISTINCT uses aliases
   - **Fix**: Always `ORDER BY` the alias name when using DISTINCT projections with aliases
   - Example: `SELECT u.DemandPlanStage__c as stage ... ORDER BY stage` (not `ORDER BY u.DemandPlanStage__c`)
   - Applies to both UCO detail queries (Step 1B, Query 9 & 10)

2. **FMAPI Provider Breakdown Always Matters**: Even when FMAPI total is small, break out by provider
   - Use `product_usage_dollars` with SKU pattern filters to split Anthropic / Gemini / OpenAI
   - AI-first accounts may have Anthropic dominant with OpenAI fast-growing — this tells a different story than an aggregate number
   - Example pattern: Addepar = Anthropic $4.2K/mo (dominant), OpenAI $265→$532/mo (fast-growing), Gemini $0

3. **AI-First Company Pattern**: For accounts where FMAPI/Apps/Vector Search are over-indexed vs. peers:
   - Do NOT flag Model Serving or FMAPI as expansion gaps — they're already leading
   - Instead, look for the inverse: under-investment in operational compute (Jobs, DLT) relative to their AI spend
   - Interpretation: "The story is NOT 'get them to try AI' — they're already leading. It's: protect the AI lead and fix the DLT gap."
   - High ALL_PURPOSE relative to Jobs is a *productionization gap*, not necessarily a compute gap

4. **ALL_PURPOSE Under-Indexing Needs Context**: Low Jobs / high ALL_PURPOSE may mean intentional ops design
   - Example: Addepar = 0% Jobs vs 29.2% peer avg, but 46.5% ALL_PURPOSE vs 18.5% peer avg
   - This pattern often means workloads run interactively (notebooks) rather than scheduled — not necessarily a churn risk
   - Check: Does the account have a productionization roadmap? Is Airflow/external scheduler in use?

5. **Peer Benchmarking for AI-first Accounts**: Standard FinServ peer set will systematically under-index AI products
   - If account is AI-first, note in the peer benchmarking tab that peers are likely lagging indicators for AI products
   - Over-indexing on AI Gateway (6000%+ index) confirms early mover advantage — classify as "CONFIRMED LEADER, defend"

6. **Parallel Agent Timing**: ~28 minutes total for a full run with healthy warehouse
   - Logfood is the bottleneck (11 queries, 13 min with PENDING polls at warehouse startup)
   - All 5 background agents should be launched simultaneously in Step 1 pre-pass
   - Sheet build takes ~9 minutes after all data is collected

## Output

The skill creates a new Google Sheets document with:
- **Template-based structure**: Matches the standard gap analysis format
- **Customer-specific data**: Populated from Logfood, Salesforce, and Google Drive
- **Color coding**: Visual indicators for adoption status and MRR levels
- **Actionable insights**: Prioritized opportunities in tier format

**Example Output**:
```
Created Gap Analysis Heatmap for ModMed
URL: https://docs.google.com/spreadsheets/d/ABC123.../edit

Summary:
- Total MRR (last month): $450,123
- Products in use: 18/35
- Tier 1 opportunities: 3 (AI Scribe expansion, DBSQL Serverless migration)
- Tier 2 opportunities: 5 (Serverless Workflows, PPT, Clean Rooms)
- Blocked: 2 (Databricks Apps - HIPAA, Pre-Training - HIPAA)
```

## Data Sources

1. **Logfood** (central-logfood workspace):
   - Dashboard: "DNB Product Gap Analysis"
   - MRR by SKU for last 3 months
   - Feature adoption metrics
   - **Important**: All queries use the Databricks CLI with `--profile=logfood` (see Step 1A for CLI execution pattern)

2. **Salesforce**:
   - Use Case Objects (UCOs) for the account
   - Product adoption stages
   - Business context and blockers

3. **JIRA ES Tickets** (NEW - Learned from GoGuardian):
   - Search: `project = ES AND text ~ "<customer_name>"`
   - Contains technical details not in UCOs
   - Includes: custom configs granted, escalations, feature requests
   - Date-stamp each finding: `[YYYY-MM-DD]`

4. **Google Drive**:
   - QBR notes
   - Meeting notes with customer
   - Technical documentation

## Requirements

**CLI Tools** (primary data access pattern):
- Databricks CLI with `logfood` profile — all Logfood SQL queries use `databricks api post ... --profile=logfood`

**MCP Servers** (must be authenticated - see Step 0):
- `jira-mcp` (for ES ticket search)
- `slack` (for channel history)
- `salesforce-actions` (for UCO search)
- `fe-google-tools:google-sheets` (for sheet creation)

**Authentication Checklist**:
- [ ] Databricks CLI profile `logfood` authenticated
- [ ] JIRA MCP token not expired
- [ ] Slack token not expired
- [ ] Google auth token valid
- [ ] Salesforce CLI connected

**Permissions**:
- Read access to Logfood system tables (`main.field_customer_insights`, `main.fin_live_gold`)
- Read access to Salesforce UCOs
- Read access to Google Drive (customer-related docs)
- Write access to Google Sheets

## Implementation Notes

- Uses template structure from reference sheet
- Derives notes from actual account documents (NOT template notes)
- All notes include dates in `[YYYY-MM-DD]` format
- Queries Logfood for most recent 3 complete months
- Applies conditional formatting for visual heatmap effect

## Error Handling

- If account not found in Logfood: Proceeds with UCO/notes only
- If no UCOs found: Proceeds with Logfood data only
- If no Drive docs found: Uses Logfood and UCO data
- Partial data is acceptable - skill will note gaps in output

## Google Sheets API Implementation Notes

**Authentication**:
```bash
TOKEN=$(python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-auth/resources/google_auth.py token)
```

**Required Header for Quota**:
```bash
-H "x-goog-user-project: gcp-sandbox-field-eng"
```

**URL Encoding for Range Parameters**:
- The `!` character in ranges like `Heatmap!A1:H50` must be URL-encoded as `%21`
- Correct: `Heatmap%21A1:H50`
- Incorrect: `Heatmap!A1:H50` (causes 404 error)

**Current Status Data Validation (Column D)**:

Apply data validation dropdown with these values:
- Adopted
- Adopting
- Evaluating
- Blocked
- Not Sure

**Conditional Formatting Status Colors**:
Apply these conditional formatting rules for cell background colors:
- `Adopted`: Dark green `{"red": 0.22, "green": 0.46, "blue": 0.11}`
- `Adopting`: Light blue `{"red": 0.68, "green": 0.85, "blue": 0.9}`
- `Evaluating`: Yellow `{"red": 1, "green": 0.85, "blue": 0.4}`
- `Blocked`: Red `{"red": 0.92, "green": 0.6, "blue": 0.6}`
- `Not Sure`: Gray `{"red": 0.8, "green": 0.8, "blue": 0.8}`

**Recommended Column Widths**:
- Col A (Databricks Offerings): 40px (rotated text)
- Col B (Category): 130px
- Col C (Product): 280px
- Col D (Status): 130px
- Col E-G (MRR columns): 90px each
- Col H (Notes): 600px

**Sheet Structure**:

1. **Row 1**: "Account: <customer_name>" - merged across all columns (A1:H1), white background, bold centered
2. **Row 2**:
   - A2:D2 merged: "* = sticky feature, but doesn't have direct revenue SKU aligned" (italic)
   - E2:G2 merged: "Account Level Usage" (horizontal text, NO rotation, light blue background `{"red": 0.68, "green": 0.85, "blue": 0.9}`)
3. **Row 3**: Header row with peach background `{"red": 0.988, "green": 0.898, "blue": 0.804}`
4. **Column A**: "Databricks Offerings" - merged A4:A35, rotated 90° vertical, peach background
5. **Column B**: Category labels - merged cells per category group, peach background:
   - Data Engineering (rows 4-6)
   - Data Warehousing (rows 7-11)
   - Interactive Workloads (rows 12-14)
   - GenAI / ML (rows 15-24)
   - Governance (rows 25-29)
   - Collaboration (rows 30-33)
   - Platform (rows 34-35)

**Separate Tabs**:
- **Tab 1: Heatmap** - Main product gap analysis with MRR data
- **Tab 2: End Analysis** - Tier-based opportunity analysis (Whale Bets, Near-Term Expansion, Gap Fillers, Blocked)
- **Tab 3: Peer Benchmarking** - Industry peer comparison with index scores

> ⚠️ **CONFIDENTIALITY WARNING**: The Peer Benchmarking tab contains names of other Databricks customers and their spend data. This tab is **internal-only**. Before sharing this Google Sheet with the customer, the Peer Benchmarking tab **must be deleted**. Add a note to the Step 6 output reminding the SA of this.

**Text Wrapping**:
Enable text wrapping on all cells and auto-resize rows to prevent truncation.

**CRITICAL: Row Number Verification**

Before updating any row, ALWAYS verify the product name matches. Key row mappings:

| Row | Product | SKU |
|-----|---------|-----|
| 4 | Lakeflow Connect | `lakeflow_connect_dbu_dollars` (emerging_data) |
| 5 | DLT Classic | `dlt_dbu_dollars` (emerging_data) |
| 6 | DLT Serverless | `dlt_serverless_dbu_dollars` (emerging_data) |
| 7 | Jobs Classic | `automated_dbu_dollars` (emerging_data) |
| 8 | Jobs Serverless | `automated_serverless_dbu_dollars` (emerging_data) |
| 10 | DBSQL Pro | `enterprise_sql_pro_compute_*` |
| 11 | DBSQL Serverless | `enterprise_serverless_sql_compute_*` |
| 12 | All Purpose Classic | `interactive_dbu_dollars` (emerging_data) |
| 13 | All Purpose Serverless | `interactive_serverless_dbu_dollars` (emerging_data) |
| 16 | Model Serving CPU | `enterprise_serverless_real_time_inference_*` |
| 18 | Foundation Model Serving | `enterprise_anthropic_model_serving`, `enterprise_openai_model_serving` + PT SKUs |
| 22 | Model Training | `enterprise_model_training_*` |
| 25 | Unity Catalog | `workload_insights_metric.uc_dollars` (paid_usage_metering) |
| 35 | Managed Storage | `premium_databricks_storage_*` |

**Note**: 32 products total (rows 4-35). Removed: Programs category (Built on Program, CoDE), DABs. The table above is the complete canonical row mapping — no external file is needed.
