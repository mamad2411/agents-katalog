---
name: ae-accounts-signals
description: Scan Logfood data sources and perform external web research per account to surface positive behavioral signals (consumption growth opportunities, feature adoption hooks, expansion signals) and negative patterns (security risks, worst practices, adoption decline, corporate risk events). Delivers a per-account markdown report combining internal platform data with external company intelligence. Invoke when asked for "account signals", "behavioral patterns", "platform health", "worst practices audit", or from ae-biweekly-review with "include signals".
---

# AE Account Signals Skill

**Purpose:** Provide a rapid, data-driven behavioral health check across an AE's territory. Covers workspace security posture, compute and query patterns, new workspace and WAU trends, and feature-level adoption — surfaced as actionable conversation hooks and remediation guidance.

**Execution order:** Phase 1 (workspace metadata + security flags) → Phase 2 (centralized system tables) → **Phase 2f (SKU dollar breakdown from PUM)** → Phase 3 (new workspaces + WAU trends) → Phase 4 (feature-level signals) → Phase 4b (Salesforce campaign + marketing engagement) → Phase 5 (external research: jobs + news) → Phase 5b (upcoming feature recommendations from go/baseline) → Phase 6 (signal classification + output, including **"High Priority Specific Actions" section**) → Phase 7 (Google Doc delivery).

---

## Input

The skill accepts either:
- **From caller (ae-biweekly-review):** `territory_account_ids` (list of SFDC account IDs) and `territory_account_names` (map of ID → name), already resolved by the caller. Also receive the logfood Databricks CLI profile name (usually `logfood`).
- **Standalone:** An AE name or email. In this case, resolve the territory yourself using the same method as ae-biweekly-review Phase 2 steps 1–4:
  1. Query `main.sfdc_bronze.user` for the AE's `Id` by email.
  2. Query `main.sfdc_bronze.accountteammember` + `main.sfdc_bronze.account` filtered by `UserId` and `TeamMemberRole IN ('Account Executive','Additional AE','Secondary AE')` to get all territory accounts.

**Databricks CLI profile:** Use `logfood` profile for all queries.

**Warehouse selection:** Before running any SQL, find a RUNNING warehouse and capture its ID dynamically:
```bash
WAREHOUSE_ID=$(databricks --profile logfood warehouses list --output json | \
  python3 -c "
import json, sys
ws = [w for w in json.load(sys.stdin).get('warehouses', []) if w.get('state') == 'RUNNING']
print(ws[0]['id'] if ws else '')
")
echo "Using warehouse: $WAREHOUSE_ID"
```
Use the returned `$WAREHOUSE_ID` for all queries. Never hardcode a warehouse ID — IDs are environment-specific and a hardcoded ID may not be accessible in your environment. If no warehouse is RUNNING, serverless warehouses start within ~30s once the first query is submitted; retry after 30s or provision one with `databricks --profile logfood warehouses create`.

**Query execution pattern:**
- Small queries (SFDC, workspaces_latest, WAU): use `wait_timeout: "30s"` for inline results.
- Large tables (centralized_system_tables, paid_usage_metering): use `wait_timeout: "0s"` (async), capture the `statement_id`, then poll with **exponential backoff**:

  ```python
  import time, subprocess, json

  def poll_statement(statement_id, profile="logfood",
                     initial_wait=10, max_interval=60, timeout=300):
      """
      Polls a Databricks SQL statement until SUCCEEDED, FAILED, or timeout.
      Backoff: 10s → 15s → 22s → 33s → 50s → 60s (capped) → 60s ...
      Returns parsed result dict or raises on failure/timeout.
      """
      elapsed = 0
      wait = initial_wait
      while elapsed < timeout:
          time.sleep(wait)
          elapsed += wait
          result = json.loads(subprocess.run(
              ["databricks", "--profile", profile, "api", "get",
               f"/api/2.0/sql/statements/{statement_id}"],
              capture_output=True, text=True
          ).stdout)
          state = result.get("status", {}).get("state", "")
          if state == "SUCCEEDED":
              return result
          if state in ("FAILED", "CANCELED"):
              raise RuntimeError(
                  f"Query {statement_id} {state}: "
                  f"{result.get('status', {}).get('error', {})}"
              )
          # Still PENDING or RUNNING — back off
          wait = min(wait * 1.5, max_interval)

      raise TimeoutError(
          f"Query {statement_id} did not complete in {timeout}s. "
          f"Check warehouse load or reduce territory scope."
      )

  # For territories > 50 accounts: use initial_wait=20 — large IN() clauses
  # on centralized_system_tables take longer to compile.
  initial = 20 if len(territory_account_ids) > 50 else 10
  ```

- **Submit all Phase 2 queries (2a–2e) in parallel** — fire all five async statements immediately, collecting all `statement_id` values. Then poll them in a **shared loop**: on each iteration check every pending statement_id and mark it complete when it reaches SUCCEEDED. Do not poll sequentially — fast queries (2e lakeflow_jobs) should not block behind slow ones (2c query_history). Apply the same pattern to Phase 3 and Phase 4 parallel groups. This cuts total wall-clock time by ~70%.

**UUID map (critical for Phase 2):** After Phase 1, build a Python dict mapping each Databricks account UUID → SFDC account ID. Phase 2 results return UUIDs only; you must join back to SFDC IDs to assign signals to accounts. Build this from the Phase 1 result rows: `{account_id_uuid: salesforce_account_id}`.

**Result row format:** All SQL API results return `data_array` as a list of lists. Column order matches the SELECT list exactly. Parse with `d.get("result", {}).get("data_array", [])` after `json.load`.

---

## Phase 1 — Workspace metadata and security flags

**Source:** `main.certified.workspaces_latest`

> **SQL resource file:** `resources/sql/phase1_workspace_security.sql`

Query using `salesforce_account_id IN (<territory_account_ids>)`. Filter `workspace_status = 'RUNNING'` only.

This single query provides:
- `workspace_id`, `account_id` (Databricks UUID — needed for Phase 2)
- `salesforce_account_id` (SFDC account ID)
- `workspace_name`, `cloud_type`, `data_plane_region`, `feature_tier`
- Security flags (see table below)

```sql
SELECT
  workspace_id,
  account_id,
  salesforce_account_id,
  workspace_name,
  cloud_type,
  data_plane_region,
  feature_tier,
  is_public_access_enabled,
  is_no_public_ip_enabled,
  is_identity_federation_enabled
FROM main.certified.workspaces_latest
WHERE workspace_status = 'RUNNING'
  AND salesforce_account_id IN (<territory_account_ids>)
```

**Persist:** `workspace_uuid_map` = map of `salesforce_account_id` → list of `account_id` (UUID). These UUIDs are required for Phase 2.

**Security flag evaluation per workspace:**

| Flag | Desired | Risk if wrong |
|------|---------|---------------|
| `is_public_access_enabled` | `false` (preferred, not required) | NEUTRAL — valid configuration for most accounts; only raise if account has strict compliance requirements (FSI, healthcare, government) |
| `is_no_public_ip_enabled` | `true` | Cluster nodes get public IPs — network exposure risk |
| `is_identity_federation_enabled` | `true` | No SSO/SCIM — manual user management, stale access risk |
| `feature_tier` | `STANDARD_W_SEC_TIER` | Missing security tier — Enhanced Security Monitoring not active |

Flag `is_no_public_ip_enabled = false` or `is_identity_federation_enabled = false` as MEDIUM RISK. **Do NOT flag `is_public_access_enabled = true` as a risk** — public internet access is a neutral configuration choice, not a worst practice.

---

## Phase 2 — Centralized system tables

**Source:** `main.centralized_system_tables.*`

Use `account_id IN (<account_uuids_from_phase1>)` — these are the Databricks UUIDs, NOT SFDC IDs. Use async SQL API (post → poll) as these tables are large.

**Window:** Last 28 days unless stated otherwise.

> **SQL resource files:** All Phase 2 queries are maintained in `resources/sql/` for easier editing and testing. Reference files: `phase2a_compute_clusters.sql`, `phase2b_compute_warehouses.sql`, `phase2c_query_history.sql`, `phase2d_job_run_timeline.sql`, `phase2e_lakeflow_jobs.sql`, `phase2f1_sku_dollars.sql`, `phase2f2_feature_dollars.sql`. Replace `<account_uuids>` / `<territory_account_ids>` placeholders before executing.

### 2a. Compute clusters

```sql
SELECT
  account_id,
  workspace_id,
  data_security_mode,
  cluster_source,
  LEFT(dbr_version, 4) AS dbr_major,
  COUNT(*) AS cluster_count
FROM main.centralized_system_tables.compute_clusters
WHERE account_id IN (<account_uuids>)
  AND change_date >= DATEADD(DAY, -28, CURRENT_DATE())
GROUP BY 1, 2, 3, 4, 5
```

**Signals:**
- `data_security_mode IS NULL` or `'NONE'` → shared isolation mode (neutral — valid for most workloads; only note if account requires strict multi-tenant isolation)
- DBR version starting with `10.`, `11.`, `12.`, `13.` → EOL runtime (14.x+ recommended as of 2026)

### 2b. Compute warehouses

**Verified schema (2026-02-24):** `warehouse_id, workspace_id, account_id, warehouse_name, warehouse_type, warehouse_channel, warehouse_size, min_clusters, max_clusters, auto_stop_minutes, tags, change_time, delete_time, created_by, stw_cloud, stw_region, stw_env`

```sql
SELECT
  account_id,
  workspace_id,
  warehouse_type,
  auto_stop_minutes,
  warehouse_name
FROM main.centralized_system_tables.compute_warehouses
WHERE account_id IN (<account_uuids>)
  AND delete_time IS NULL
```

**Signals:**
- `warehouse_type = 'CLASSIC'` → not serverless — position DBSQL Serverless (30–50% typical savings)
- `auto_stop_minutes > 30` → idle waste — recommend 5–10 min
- `LOWER(warehouse_name) LIKE '%dbt%'` → dbt in stack — position DABs CI/CD, Lakeflow

### 2c. Query history

```sql
SELECT
  account_id,
  workspace_id,
  client_application,
  statement_type,
  execution_status,
  COUNT(*) AS query_count
FROM main.centralized_system_tables.query_history
WHERE account_id IN (<account_uuids>)
  AND start_time >= DATEADD(DAY, -28, CURRENT_DATE())
GROUP BY 1, 2, 3, 4, 5
```

**Signals (Green):**
- `client_application ILIKE '%Databricks SQL Genie Space%'` → Genie active in query history
- `LOWER(client_application) LIKE '%dbt%'` → dbt confirmed via query patterns
- `execution_status = 'FINISHED_FROM_RESULT_CACHE'` with high count → caching working well — serverless + caching story

**Signals (Red/Orange):**
- `LOWER(client_application) LIKE '%azure-data-factory%'` or `%airflow%` → external orchestrator driving queries — position Lakeflow Connect / Workflows
- `LOWER(client_application) LIKE '%jdbc%'` and no named BI tool present → unverified JDBC connector — validate driver version
- `statement_type = 'MERGE'` count > 500 and ADF present → CDC workload via ADF — position DLT Change Data Capture
- High `execution_status = 'FAILED'` ratio (>5% of queries failing)

### 2d. Lakeflow job run timeline (job success rate)

```sql
SELECT
  account_id,
  workspace_id,
  result_state,
  COUNT(*) AS run_count
FROM main.centralized_system_tables.lakeflow_job_run_timeline
WHERE account_id IN (<account_uuids>)
  AND period_start_time >= DATEADD(DAY, -28, CURRENT_DATE())
GROUP BY 1, 2, 3
```

**Compute:** `error_rate = ERROR_count / total_count * 100`. Flag accounts where error_rate > 5%.

### 2e. Lakeflow jobs (automation maturity)

```sql
SELECT
  account_id,
  workspace_id,
  trigger_type,
  COUNT(*) AS job_count
FROM main.centralized_system_tables.lakeflow_jobs
WHERE account_id IN (<account_uuids>)
GROUP BY 1, 2, 3
```

**Signal:** Accounts with near-zero `trigger_type = 'CRON'` jobs but significant consumption → ad-hoc / not automated → low maturity — position DABs / scheduled Workflows.

---

## Phase 2f — SKU dollar breakdown from paid_usage_metering

**Source:** `main.fin_live_gold.paid_usage_metering`

**Purpose:** Enrich all DBU signal findings with actual dollar spend. Always report dollar figures alongside DBU counts in the output — "$X spend (Y DBUs)" is far more actionable than DBU counts alone.

**Filter:** Use `sfdc_account_id IN (<territory_account_ids>)` (SFDC IDs, not UUIDs). Filter `is_paying = 'true'`. Window: last 28 days.

**This is a large table — submit async** (wait_timeout: "0s") and poll.

### 2f-1. Product-level dollar breakdown

Groups spend into the major product areas used throughout the report.

```sql
SELECT
  sfdc_account_id,
  product_type,
  workload_type,
  SUM(usage_dollars) AS total_dollars,
  SUM(usage_amount)  AS total_dbus
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id IN (<territory_account_ids>)
  AND date >= DATEADD(DAY, -28, CURRENT_DATE())
  AND is_paying = 'true'
GROUP BY 1, 2, 3
ORDER BY total_dollars DESC
```

**Product type → report label mapping:**

| `product_type` | Report label |
|---|---|
| `SQL` | DBSQL / SQL |
| `JOBS` | Jobs / Lakeflow Jobs |
| `ALL_PURPOSE` | All-Purpose Compute |
| `APPS` | Databricks Apps |
| `INTERACTIVE` | Interactive Notebooks |
| `DLT` | DLT (on interactive) |
| `MODEL_SERVING` | Model Serving |
| `VECTOR_SEARCH` | Vector Search |
| `DATABASE` | Lakebase |
| `FOUNDATION_MODEL_API` | Foundation Model API |
| `PREDICTIVE_OPTIMIZATION` | Predictive Optimization |

**Note on DLT dollars:** DLT pipelines running on Serverless SQL compute appear under `product_type = 'SQL'` with `workload_type = 'DLT'`. Add `SQL/DLT` and `DLT/DLT` rows together to get the true total DLT spend. Use the struct query (2f-2) for the canonical DLT total via `lakeflow_pipelines_dollars`.

### 2f-2. Feature-level dollar breakdown (struct fields)

`sales_comp_metric` and `product_lines_metric` are STRUCT columns — use **dot notation**, not `get_json_object()`.

```sql
SELECT
  sfdc_account_id,
  SUM(sales_comp_metric.genie_dollars)              AS genie_dollars,
  SUM(sales_comp_metric.genie_dbu)                  AS genie_dbu,
  SUM(sales_comp_metric.lakeview_dollars)           AS lakeview_dollars,
  SUM(sales_comp_metric.lakeview_dbu)               AS lakeview_dbu,
  SUM(sales_comp_metric.lakeflow_pipelines_dollars) AS dlt_dollars,
  SUM(sales_comp_metric.lakeflow_pipelines_dbu)     AS dlt_dbu,
  SUM(sales_comp_metric.sql_dollars)                AS sql_dollars,
  SUM(sales_comp_metric.sql_dbu)                    AS sql_dbu,
  SUM(sales_comp_metric.lakebase_dollars)           AS lakebase_dollars,
  SUM(sales_comp_metric.lakebase_dbu)               AS lakebase_dbu,
  SUM(sales_comp_metric.model_serving_dollars)      AS model_serving_dollars,
  SUM(sales_comp_metric.vector_search_dollars)      AS vector_search_dollars,
  SUM(sales_comp_metric.foundation_model_api_dollars) AS fm_api_dollars,
  SUM(product_lines_metric.ai.apps_dollars)         AS apps_dollars,
  SUM(product_lines_metric.ai.apps_dbu)             AS apps_dbu
FROM main.fin_live_gold.paid_usage_metering
WHERE sfdc_account_id IN (<territory_account_ids>)
  AND date >= DATEADD(DAY, -28, CURRENT_DATE())
  AND is_paying = 'true'
GROUP BY 1
```

**Use these dollar figures throughout the report** to replace bare DBU counts with "$X (Y DBUs)" format.

### 2f-3. Persist dollar signals

```
sku_dollars[sfdc_account_id] = {
  "total_dollars": <sum of all usage_dollars for account>,
  "total_dbus": <sum of all usage_amount>,
  "by_product": {"SQL": {"dollars": X, "dbus": Y}, "JOBS": {...}, ...},
  "feature": {
    "genie_dollars": X, "genie_dbu": Y,
    "lakeview_dollars": X, "lakeview_dbu": Y,
    "dlt_dollars": X, "dlt_dbu": Y,
    "sql_dollars": X, "sql_dbu": Y,
    "apps_dollars": X, "apps_dbu": Y,
    "lakebase_dollars": X,
    "model_serving_dollars": X,
    "vector_search_dollars": X
  }
}
```

**Submit Phase 2f queries in parallel with Phase 3** — they use the same `paid_usage_metering` table.

---

## Phase 3 — New workspaces and WAU trends

> **SQL resource files:** `resources/sql/phase3a_new_workspaces_sfdc.sql`, `resources/sql/phase3b_first_consuming_workspaces.sql`, `resources/sql/phase3c_wau_trends.sql`

Reuses data sources already familiar from ae-biweekly-review. No new tables.

### 3a. New workspaces created (last 28 days) — SFDC source

```sql
SELECT w.Name, w.Status__c, w.CreatedDate, a.Name AS account_name, a.Id AS account_id
FROM main.sfdc_bronze.workspace__c w
JOIN main.sfdc_bronze.account a ON w.Account__c = a.Id
WHERE w.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.workspace__c)
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
  AND w.Account__c IN (<territory_account_ids>)
  AND w.CreatedDate >= DATEADD(DAY, -28, CURRENT_DATE())
ORDER BY w.CreatedDate DESC
```

### 3b. New workspaces first-consuming (last 28 days) — PUM source

Identifies workspaces with consumption in the last 28 days that had zero consumption in the 28 days prior — net-new active workloads.

```sql
WITH recent AS (
  SELECT DISTINCT sfdc_workspace_id, sfdc_workspace_name, sfdc_account_id, sfdc_account_name
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id IN (<territory_account_ids>)
    AND date >= DATEADD(DAY, -28, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
),
prior AS (
  SELECT DISTINCT sfdc_workspace_id
  FROM main.fin_live_gold.paid_usage_metering
  WHERE sfdc_account_id IN (<territory_account_ids>)
    AND date BETWEEN DATEADD(DAY, -56, CURRENT_DATE()) AND DATEADD(DAY, -29, CURRENT_DATE())
    AND paying_status = 'PAYING_STATUS_PAYING'
)
SELECT r.*
FROM recent r
LEFT JOIN prior p ON r.sfdc_workspace_id = p.sfdc_workspace_id
WHERE p.sfdc_workspace_id IS NULL
```

### 3c. WAU trends (QoQ) — `main.gtm_gold.account_active_users_quarterly`

**Schema notes (verified 2026-02-23):**
- `account_id` (STRING) — this IS the Salesforce account ID. Filter directly with territory SFDC IDs.
- `fiscal_year_quarter` (STRING) — format `"FY'27 Q1"` (apostrophe, space before Q). NOT integers.
- `wau_t7d` — current quarter weekly active users.
- `wau_t7d_prior_quarter` — prior quarter WAU, pre-joined.
- No `account_name` column — join to name map from territory list.

```sql
SELECT
  account_id,
  fiscal_year_quarter,
  wau_t7d,
  wau_t7d_prior_quarter,
  ROUND(
    (wau_t7d - wau_t7d_prior_quarter) * 100.0 / NULLIF(wau_t7d_prior_quarter, 0),
    1
  ) AS wau_qoq_pct
FROM main.gtm_gold.account_active_users_quarterly
WHERE account_id IN (<territory_account_ids>)
  AND fiscal_year_quarter = '<current_fiscal_year_quarter>'
ORDER BY wau_t7d DESC
```

Build the `fiscal_year_quarter` string from today's date using the shared fiscal calendar utility (`../../resources/fiscal_calendar.py`). Example: `python3 ../../resources/fiscal_calendar.py | python3 -c "import json,sys; print(json.load(sys.stdin)['fiscal_year_quarter_str'])"` → `"FY'27 Q1"`.

**Trend labels:**
- Rising: `wau_qoq_pct > +10%`
- Flat: `wau_qoq_pct` between -10% and +10%
- Declining: `wau_qoq_pct < -10%`
- Accounts where both `wau_t7d = 0` and `wau_t7d_prior_quarter = 0`: inactive/prospect — note separately, do not label as declining.

---

## Phase 4 — Feature-level signals

> **SQL resource file:** `resources/sql/phase4_feature_metrics.sql`

**Source:** `main.data_product_features.account_metrics`

**Verified schema (2026-02-24):** The filter key is `salesforce_account_id` (not `sfdc_account_id`). The date column is `date` (not `snapshot_date`). Feature column names differ significantly from what you might expect — use only the verified names below.

```sql
SELECT
  salesforce_account_id,
  salesforce_account_name,
  date,
  genie_num_events_t28d,
  lakeview_num_users_t28d,
  databricks_assistant_num_users_t28d,
  databricks_assistant_ghost_text_accepted_num_events_t28d,
  mlflow_num_api_calls_t28d,
  apps_dbus_t28d,
  dlt_dbus_t28d,
  scim_num_api_calls_t28d,
  interactive_num_users_t28d
FROM main.data_product_features.account_metrics
WHERE salesforce_account_id IN (<territory_account_ids>)
  AND date = (
    SELECT MAX(date)
    FROM main.data_product_features.account_metrics
    WHERE salesforce_account_id IN (<territory_account_ids>)
  )
```

**Column name reference (verified 2026-02-24):**

| Intent | Correct column name |
|--------|---------------------|
| Genie events | `genie_num_events_t28d` |
| Lakeview dashboard users | `lakeview_num_users_t28d` |
| Databricks Assistant users | `databricks_assistant_num_users_t28d` |
| Ghost text accepts | `databricks_assistant_ghost_text_accepted_num_events_t28d` |
| MLflow API calls | `mlflow_num_api_calls_t28d` |
| Apps DBUs | `apps_dbus_t28d` |
| DLT DBUs | `dlt_dbus_t28d` |
| SCIM API calls | `scim_num_api_calls_t28d` |
| Total interactive users | `interactive_num_users_t28d` |
| Account name | `salesforce_account_name` |
| Date | `date` |

**Do NOT use these — they do not exist:** `sfdc_account_id`, `snapshot_date`, `assistant_num_users_t28d`, `assistant_num_ghost_text_accepts_t28d`, `ml_flow_num_api_calls_t28d`, `lakeview_num_viewers_t28d`, `lakeview_num_authors_t28d`, `total_num_users_t28d`, `total_num_events_t28d`, `data_lineage_num_users_t28d`, `dlt_num_users_t28d`.

**Note:** This table returns one row per account per date but may return multiple rows per account if date ranges overlap. Always filter to `MAX(date)` as shown. The table can also be large — submit async if territory has >20 accounts.

**Pairing with Phase 2f dollars:** `apps_dbus_t28d` and `dlt_dbus_t28d` in this table are DBU counts only. For dollar values, use `sku_dollars[account_id].feature.apps_dollars` and `sku_dollars[account_id].feature.dlt_dollars` from Phase 2f. Similarly, `genie_num_events_t28d` and `lakeview_num_users_t28d` are event/user counts; pair with `genie_dollars` and `lakeview_dollars` from Phase 2f when writing signal bullets.

---

## Phase 4b — Salesforce campaign and marketing engagement

**Source:** Salesforce `CampaignMember` + `Campaign` objects via `sf data query` CLI.

**Window:** Last 90 days. Marketing event attendance often precedes or correlates with active evaluation — a contact who attended a webinar 6–8 weeks ago may be in active evaluation right now.

**Authentication check (required before running this phase):** Verify Salesforce auth is valid. If not, invoke the `salesforce-authentication` skill before continuing.

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  echo "ERROR: Salesforce auth missing or expired. Run the salesforce-authentication skill, then retry Phase 4b."
  # Skip this phase — set campaign_signals to empty and note omission in output
  exit 0
fi
```

If auth fails, skip Phase 4b entirely and include this note in the output report: *"Campaign signals omitted — Salesforce authentication required. Re-run with valid auth to include marketing engagement data."*

**Query:**

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username')

sf data query --query "
SELECT
  Contact.FirstName,
  Contact.LastName,
  Contact.Title,
  Contact.Account.Name,
  Contact.AccountId,
  Campaign.Name,
  Campaign.Type,
  Campaign.StartDate,
  Status,
  CreatedDate
FROM CampaignMember
WHERE Contact.AccountId IN (<territory_account_ids_single_quoted>)
  AND CreatedDate >= LAST_N_DAYS:90
ORDER BY CreatedDate DESC
LIMIT 500" --target-org "$SF_TARGET_ORG" --json 2>/dev/null | jq '.result.records'
```

**Important:** SOQL IN clauses require single-quoted IDs separated by commas, e.g. `'0018Y00002qRt2hQAC','001Vp00000jOR21IAG'`. Build this string from `territory_account_ids` before running the query.

**Exclude from signals:** Records where `Status = 'Sent'` only (email blast with no engagement action) — these are not strong intent signals.

**Persist per account:**

```
campaign_signals[sfdc_account_id] = [
  {
    "contact_name": "...",
    "contact_title": "...",
    "campaign_name": "...",
    "campaign_type": "Event|Offer|Product|Asset|...",
    "campaign_date": "YYYY-MM-DD",
    "status": "Attended|Responded|Registered|Attended On-demand",
    "created_date": "YYYY-MM-DD"
  }
]
```

**Campaign type signal strength:**

| `Campaign.Type` | Status | Signal strength | Meaning |
|-----------------|--------|-----------------|---------|
| `Event` | `Attended` | **Strong** | Contact proactively attended in-person or live virtual event |
| `Event` | `Attended On-demand` | **Medium** | Async viewing after the event — accessing content at own pace |
| `Event` | `Registered` (not Attended) | **Weak** | Intent to attend but no-show — still worth a follow-up with recording |
| `Offer` | `Responded` | **Medium** | Content download / asset consumption — topic reveals interest area |
| `Product` | `Responded` | **Strong** | Trial or product self-service sign-up — high conversion intent |
| `Asset` | `Responded` | **Medium** | Partner-submitted lead or content response |

**Contact seniority:** Note whether attending contacts are senior (VP, Director, Head of, C-level, CDO, CTO, CISO) vs. practitioner (Analyst, Engineer, Consultant). Senior attendance is a strong executive engagement signal.

**Decode Databricks campaign name convention** (`FY{YY}{MM}{DD}-{TYPE}-{TOPIC}-{LOCATION}`):

| Code | Meaning |
|------|---------|
| `EV` | In-person or live virtual Event |
| `EXEV` | Executive event track |
| `TR` | Training |
| `WB` | Webinar |
| `EB` | eBook / content offer |
| `DAIWT` | Data + AI World Tour |

Decode the campaign name for the user in the output — do not leave raw campaign slugs unexplained.

---

## Phase 5 — External research: job postings and company news

For each account in the territory, run targeted web searches to gather external intelligence. This takes 2–3 searches per account. Prioritise accounts that have either high consumption, active UCOs, or WAU/workspace signals from Phases 1–4 — for large territories (>15 accounts) focus on top accounts by consumption first.

**Tools:** Use `WebSearch` for each search query. Use `WebFetch` if a specific article or careers page URL is needed for detail.

**Time window:** Focus on content published in the last 60 days. Discard results older than 90 days unless they are structural (e.g. a merger still in effect).

---

### 5a. Open job postings (data and AI hiring signals)

For each account, run a search to identify open roles related to data engineering, analytics, ML/AI, and cloud infrastructure. These indicate where the company is investing and what capabilities they are building.

**Search queries to run (pick 1–2 per account):**

```
"[Company Name]" jobs "data engineer" OR "analytics engineer" OR "data platform" OR "machine learning" 2026
"[Company Name]" careers "cloud" OR "AI" OR "data" site:linkedin.com OR site:greenhouse.io OR site:lever.co
"[Company Name]" "[City/Country]" hiring "Databricks" OR "Spark" OR "Lakehouse"
```

**Signal classification for job data:**

| Observation | Classification | Conversation hook |
|-------------|---------------|-------------------|
| Multiple open data engineering / analytics roles | Green | Active platform build-out — expansion conversation ready |
| ML/AI Engineer roles open | Green | AI workloads being built — discuss Model Serving, Mosaic AI |
| "Databricks" or "Spark" in JD tech requirements | Green | Platform is strategic — confirm UCO coverage and expand scope |
| "Snowflake" or "Redshift" in JDs alongside Databricks | Watch | Competitive tooling present — consolidation opportunity |
| No data roles open after recent wave of hires | Green | Team ramped and fully staffed — expect consumption growth |
| Engineering hiring freeze or very few open roles | Orange | Possible budget constraint or restructuring — validate project health |

Capture: count of relevant open roles, representative titles, location, and any technology keywords in JDs.

---

### 5b. Recent company news (corporate events and risk signals)

For each account, run 1–2 searches to surface recent corporate events from news sites and press releases.

**Search queries:**

```
"[Company Name]" news 2026 expansion OR acquisition OR "new product" OR "new service" OR partnership
"[Company Name]" 2026 layoffs OR restructuring OR "cost cutting" OR "budget freeze" OR "leadership change"
"[Company Name]" blog OR press release 2026 technology OR data OR AI OR cloud
```

**Event classification:**

| Event type | Classification | Signal and action |
|-----------|---------------|-------------------|
| New product launch with data/AI component | Green | New Databricks workload likely — discuss platform capacity and UCO |
| Geographic expansion / new market entry | Green | Expansion → new workspaces and data infra needed |
| Acquisition announced | Green/Watch | Data integration workload incoming — potential new Databricks seats |
| Partnership with cloud/data vendor | Green | Validate Databricks alignment within the joint programme |
| IPO or major funding round | Green | Growth-stage scale-up — expand UCO footprint before data scale event |
| Technology modernisation programme announced | Green | Confirm Databricks is part of the programme; get a UCO created |
| Layoffs or headcount reduction | Red | Restructuring risk — validate champion retained and project not cancelled; cross-check WAU trend |
| CEO/CDO/CTO departure | Red | Executive change — re-qualify sponsor immediately |
| Cost-cutting or budget freeze reported | Red | Budget pressure — prioritise renewal; validate expansion is still funded |
| Revenue miss or negative earnings | Orange | Revenue pressure — renewal risk elevated |
| Data breach or security incident | Orange | Strong entry point: security posture review (ESM, private endpoints, SCIM) |
| Regulatory action or compliance news | Orange | Compliance pressure — UC lineage, audit logging, and governance conversation |

Capture: event type, date (approximate), source URL, 1–2 sentence summary.

---

### 5c. Company tech/engineering blog (strategic data signals)

For accounts with high strategic value, fetch the company's engineering or tech blog to scan recent post titles and dates.

1. Search `"[Company Name]" engineering blog OR tech blog` to find the URL.
2. Use `WebFetch` on the blog index page.
3. Scan post titles for mentions of: data platforms, lakehouse, real-time analytics, AI/ML pipelines, Databricks, Spark, or competitive tools.

Posts referencing Databricks directly can be used as conversation starters. Posts about a data-heavy new product are expansion signals.

---

### 5d. Persist external research results

Store per account:

```
external_signals[account_id] = {
  "open_data_roles": [{"title": "...", "location": "...", "tech_keywords": ["Databricks", "Spark", ...]}],
  "news_events": [{"type": "layoff|expansion|...", "date": "...", "summary": "...", "url": "...", "classification": "green|red|orange"}],
  "blog_signals": [{"title": "...", "date": "...", "relevance": "..."}]
}
```

---

## Phase 5b — Upcoming feature recommendations from go/baseline

Match each account's behavioral patterns (collected in Phases 2–4) against upcoming Databricks features from the internal roadmap baseline. This surfaces personalised "what's coming that matters to you" hooks for each account.

### Step 1 — Resolve the current baseline document

Resolve the `go/baseline` shortlink by following HTTP redirects — no browser required:

```bash
# Follow redirects to get the final Google Doc URL
BASELINE_URL=$(curl -sI -L --max-redirs 10 "http://go/baseline" 2>/dev/null | \
  grep -i "^location:" | tail -1 | sed 's/[Ll]ocation: //;s/\r//')

# Extract Google Doc ID (segment between /d/ and next /)
BASELINE_DOC_ID=$(echo "$BASELINE_URL" | python3 -c "
import sys, re
url = sys.stdin.read().strip()
m = re.search(r'/d/([^/]+)', url)
print(m.group(1) if m else '')
")
echo "Resolved baseline doc ID: $BASELINE_DOC_ID"
```

**Fallback chain (in order):**
1. If `curl` redirect resolution returns an empty URL (e.g. corporate DNS doesn't route `go/` from headless context), check `~/.vibe/cache/go_baseline_url.txt` for a previously resolved and cached URL.
2. Use the `google-docs` skill to search Drive for documents with "baseline" in the title owned by Databricks internal: `google_docs.search("baseline roadmap")`.
3. As a last resort, manually navigate to `go/baseline` in a browser, copy the resulting Google Doc URL, and paste it as `BASELINE_URL` in the session.

**Cache the resolved URL** after first successful resolution:
```bash
mkdir -p ~/.vibe/cache
echo "$BASELINE_URL" > ~/.vibe/cache/go_baseline_url.txt
```

Extract the Google Doc ID from the returned URL (the segment between `/d/` and the next `/`).

### Step 2 — Fetch and parse the baseline document

Use the Google Docs API with the standard `google-auth` token to read the document. Extract all HEADING_2 and HEADING_3 paragraphs and their immediately following text (specifically paragraphs containing `GA`, `PuPr`, `PrPr`, `Beta`, or `launching`) as the feature signal corpus. Use Python `urllib.request` rather than `curl` to avoid shell timeouts on large docs:

```python
import subprocess, json, urllib.request

token = subprocess.run(
    ["python3", "~/.claude/plugins/cache/fe-vibe/fe-google-tools/.../google-auth/resources/google_auth.py", "token"],
    capture_output=True, text=True, timeout=15
).stdout.strip()

req = urllib.request.Request(
    f"https://docs.googleapis.com/v1/documents/{DOC_ID}",
    headers={"Authorization": f"Bearer {token}", "x-goog-user-project": "gcp-sandbox-field-eng"}
)
with urllib.request.urlopen(req, timeout=25) as resp:
    doc = json.loads(resp.read())

# Walk body, collect (heading, [bullet lines]) pairs
features = []   # list of {"area": str, "items": [str]}
current_area = None
current_items = []
for elem in doc.get("body", {}).get("content", []):
    para = elem.get("paragraph", {})
    style = para.get("paragraphStyle", {}).get("namedStyleType", "")
    text = "".join(r.get("textRun", {}).get("content", "") for r in para.get("elements", [])).strip()
    if not text:
        continue
    if style in ("HEADING_2", "HEADING_3"):
        if current_area and current_items:
            features.append({"area": current_area, "items": current_items})
        current_area = text
        current_items = []
    elif current_area and any(kw in text for kw in ["GA", "PuPr", "PrPr", "Beta", "launching", "Launch"]):
        if len(text) < 250:
            current_items.append(text)
if current_area and current_items:
    features.append({"area": current_area, "items": current_items})
```

### Step 3 — Match features to account behavioral signals

For each account, use the following mapping table to find relevant upcoming features based on the signals collected in Phases 2–4. Only surface a feature if the account has **non-zero activity** in the matching signal column.

| Behavioral signal (non-zero) | Relevant feature areas to search in baseline |
|------------------------------|----------------------------------------------|
| Classic warehouses detected (`warehouse_type = 'CLASSIC'`, Phase 2b) | "Data Warehousing", "Serverless SQL", "SQL Features", "Lakebridge" |
| `genie_num_events_t28d > 0` (Phase 4) | "Genie", "AI/BI", "Databricks One", "Unity Catalog Business Semantics" |
| `lakeview_num_users_t28d > 0` (Phase 4) | "Dashboards", "Genie", "AI/BI" |
| `mlflow_num_api_calls_t28d > 0` (Phase 4) | "MLflow", "Agent Bricks", "Foundation Model Serving", "Custom Model Serving" |
| `mlflow_num_api_calls_t28d > 0` AND no model serving signals | "Foundation Model Serving", "Agent Bricks", "Custom Model Serving" (strong hook: training but not serving) |
| `dlt_dbus_t28d > 0` (Phase 4) | "Spark Declarative Pipelines", "Lakeflow", "Materialized Views" |
| `apps_dbus_t28d > 0` (Phase 4) | "Databricks Apps", "Lakebase" |
| `apps_dbus_t28d = 0` (no Apps yet) | "Databricks Apps" (greenfield hook) |
| ADF or Airflow in `client_application` (Phase 2c) | "Lakeflow Connect", "Lakeflow Jobs" |
| dbt in query history or warehouse name (Phase 2c/2b) | "Lakeflow Connect", "Lakeflow Designer", "Lakeflow Jobs" |
| `databricks_assistant_num_users_t28d > 0` (Phase 4) | "Databricks Assistant", "Lakebridge" |
| `scim_num_api_calls_t28d > 0` OR identity federation issues (Phase 1) | "IAM", "Unity Catalog", "Security and Compliance" |
| `lakeview_num_users_t28d = 0` AND `genie_num_events_t28d = 0` (Phase 4) | "Unity Catalog", "Managed Tables / Open Lakehouse" (no AI/BI adoption yet) |
| EOL DBR clusters (Phase 2a) | "DBR Stability", "Serverless Compute" |
| `wau_qoq_pct < -10%` (Phase 3c) | "Databricks One", "Genie" (re-engagement hooks) |
| High job error rate > 5% (Phase 2d) | "Lakeflow Jobs", "Serverless Compute" (observability features) |

**Matching algorithm:**
1. For each account, build a set of matching feature areas from the table above.
2. Search the parsed `features` list for entries whose `area` contains any of the matching keywords (case-insensitive).
3. For each matched area, select up to 2 of the most actionable bullet items (prefer items mentioning `GA` or `PuPr` over `PrPr`, and prefer items with a short clear benefit description).
4. **Cap at 3 features per account** — ranked by: (a) GA/PuPr before PrPr, (b) strength of the matching behavioral signal, (c) whether it addresses an active pain point (e.g. high error rate → Lakeflow Jobs observability).
5. Skip features whose bullet text only says "planned" or "TBD" with no milestone marker.

### Step 4 — Persist feature recommendations

```
feature_recommendations[account_id] = [
  {
    "feature_area": "Genie",
    "feature_name": "Genie Research Agent",
    "milestone": "Beta/PuPr",
    "why_relevant": "Account has 1,762 Genie events — power users ready for agentic Genie capabilities",
    "action": "Enrol in Genie Research Agent beta; demo multi-step research queries"
  },
  ...
]
```

---

## Phase 6 — Signal classification and output

**Incomplete-data banner (render at the very top of the output if any phase was skipped):**

If Phase 4b was skipped due to missing Salesforce authentication, prepend this callout before the per-account sections:

> **⚠ Warning: Campaign engagement data omitted.** Salesforce authentication was not active when this report was generated — Phase 4b (marketing campaign signals) was skipped. To include campaign engagement data, run the `salesforce-authentication` skill and re-run `ae-accounts-signals`.

Render this banner even if all other phases completed successfully, so the reader does not assume the report is complete.

---

Aggregate all findings from Phases 1–5 (internal platform data + external research). For each account, classify into two buckets and produce a markdown report section.

### Green signals — positive momentum and conversation hooks

| Condition | Signal and hook |
|-----------|-----------------|
| `is_identity_federation_enabled = true` on all workspaces | SSO/SCIM active — validate user access governance is current |
| `genie_num_events_t28d > 0` (Phase 4) OR Genie confirmed in query_history (Phase 2c) | Genie is active — discuss Genie Agent and AI/BI upgrade path |
| dbt warehouse name detected (Phase 2b) OR `client_application LIKE '%dbt%'` (Phase 2c) | dbt in stack — position DABs CI/CD, Lakeflow Connect for pipeline orchestration |
| New workspace first-consuming in last 28 days (Phase 3b) | Project expansion: "[workspace name]" started consuming — new use case likely in flight, get a UCO created |
| ≥3 SFDC workspaces created in last 28 days with consumption (Phase 3a + 3b) | High provisioning velocity — development pace is strong, multi-project expansion |
| `wau_qoq_pct > +10%` (Phase 3c) | User growth +X% QoQ — strong adoption momentum, discuss team-wide enablement and training |
| `databricks_assistant_ghost_text_accepted_num_events_t28d > 0` (Phase 4) | Databricks Assistant actively used — discuss team licence expansion and usage best practices |
| `mlflow_num_api_calls_t28d > 0` (Phase 4) | MLflow API calls active — ML pipelines confirmed; position Model Serving / Mosaic AI endpoints |
| `dlt_dbus_t28d > 0` (Phase 4) | DLT active — discuss DLT Apply Changes from Snapshot preview if not enrolled |
| ADF in `client_application` (Phase 2c) | ADF orchestrating Databricks — position Lakeflow Connect for consolidation and cost reduction |
| `execution_status = 'FINISHED_FROM_RESULT_CACHE'` high ratio (Phase 2c) | Cache hit rate high — serverless + result caching story for TCO conversation |
| `scim_num_api_calls_t28d > 0` (Phase 4) | SCIM provisioning active — UC governance is in motion |
| `apps_dbus_t28d > 0` (Phase 4) | Databricks Apps consuming DBUs — discuss Apps roadmap and dev platform positioning |

### Red/Orange signals — worst practices and remediation

| Condition | Risk level | Remediation |
|-----------|-----------|-------------|
| `is_public_access_enabled = true` on any workspace (Phase 1) | NEUTRAL | Public internet access is a valid configuration. Do not surface as a risk or remediation item unless account has explicit compliance requirements (FSI, healthcare, government). If relevant, mention as an optional hardening step. |
| `is_no_public_ip_enabled = false` on any workspace (Phase 1) | MEDIUM | Enable "No Public IP" in workspace settings — cluster nodes currently assigned public IPs. |
| `is_identity_federation_enabled = false` on any workspace (Phase 1) | MEDIUM | Configure SSO/SCIM via Account Console → Settings → Identity and Access. Manual user management creates stale access risk. |
| `feature_tier` missing security tier (Phase 1) | MEDIUM | Enroll in Enhanced Security Monitoring tier — audit logs and compliance features not active. |
| DBR version < 14.x on clusters (Phase 2a) | MEDIUM | Upgrade to DBR 15.4 LTS — versions 10.x/11.x/12.x/13.x are EOL, security patches stopped. |
| `data_security_mode IS NULL` or `'NONE'` on job clusters (Phase 2a) | NEUTRAL | Shared isolation mode is a valid and common choice. Do not flag as a risk — single-user or user-isolation mode are optional hardening steps, not requirements. Only mention if account is pursuing strict multi-tenant data isolation. |
| `warehouse_type = 'CLASSIC'` present (Phase 2b) | MEDIUM | Migrate to Serverless SQL — typically 30–50% cost reduction, no cluster warm-up time. |
| `auto_stop_minutes > 30` on any warehouse (Phase 2b) | LOW | Set auto-stop to 5–10 minutes — idle warehouses likely wasting compute budget. |
| Job error rate > 5% (Phase 2d) | MEDIUM | Review Workflows dashboard — X% of job runs failing. Check cluster logs and retry policies. |
| Near-zero CRON jobs despite consumption (Phase 2e) | LOW | Workloads appear ad-hoc — discuss scheduling and DABs for production-grade automation maturity. |
| SFDC workspace created >14 days ago with zero consumption (Phase 3a vs 3b) | MEDIUM | Provisioned but inactive workspace — follow up on blockers to activation: missing access? data not migrated? no use case defined? |
| `wau_qoq_pct < -10%` (Phase 3c) | HIGH | User count falling -X% QoQ — investigate: champion or team change? competing tool adopted? project deprioritized? |
| `wau_t7d = 0`, `wau_t7d_prior_quarter > 0` (Phase 3c) | HIGH | Users dropped to zero this quarter — urgent: validate who the new champion is and whether workload continues. |
| `wau_t7d = 0` AND `wau_t7d_prior_quarter = 0` but consumption > 0 (Phase 3c) | MEDIUM | Automated-only workloads, no human users — confirm UC governance and access model is correct, no human oversight risk. |
| Zero AI feature adoption: `genie_num_events_t28d = 0`, `lakeview_num_users_t28d = 0`, `databricks_assistant_num_users_t28d = 0` (Phase 4) | MEDIUM | No AI features in use — strong entry point for AI/BI + Databricks Assistant enablement conversation. |
| ADF driving high MERGE count (Phase 2c) | MEDIUM | External orchestrator driving CDC pattern — position DLT Apply Changes + Lakeflow Connect migration path. |
| JDBC dominant, no named BI tool (Phase 2c) | LOW | Unverified BI connectivity — validate JDBC driver version and consider certified connector for stability. |

**Campaign engagement signals from Phase 4b:**

| Condition | Classification | Signal and hook |
|-----------|---------------|-----------------|
| ≥1 contact attended an Event in the last 90 days | Green | Active marketing engagement — use the specific event as a conversation entry point ("We saw [Name] at [event] — did they share takeaways with the team?") |
| ≥3 contacts from the same account attended the same event | Green | Team-level buying signal — broad interest, not just one champion; strong moment to propose a multi-stakeholder discovery call |
| Senior contact (VP/Director/Head of/C-level) attended an event | Green | Executive engagement confirmed — flag to AE for executive alignment follow-up |
| Contact responded to an Offer/content asset (ebook, whitepaper) | Green | Topic of the offer indicates active interest area — use content as a conversation hook |
| Contact signed up for a Product trial (campaign type `Product`) | Green | Self-service evaluation intent — follow up immediately to support the trial |
| Contact registered for an event but did not attend | Watch | Intent signal with no follow-through — send event recording or key takeaways |

**External signals from Phase 5 (added to Green or Red/Orange as appropriate):**

| Condition | Classification | Signal and action |
|-----------|---------------|-------------------|
| Multiple open data/ML/AI roles (Phase 5a) | Green | Active data investment — expansion conversation and platform capacity planning |
| "Databricks" or "Spark" in open JDs (Phase 5a) | Green | Platform is confirmed strategic in hiring — align UCO coverage |
| New product / expansion / funding announced (Phase 5, news) | Green | Growth event — new Databricks workload likely, create or update UCO |
| Technology modernisation programme announced (Phase 5, news) | Green | Modernisation in progress — confirm Databricks is part of the programme |
| Acquisition announced (Phase 5, news) | Green/Watch | Data integration workload incoming — discuss platform consolidation |
| Engineering blog post about data/AI platform (Phase 5, blog) | Green | Active platform investment signalled publicly — use as conversation context |
| Layoffs or restructuring announced (Phase 5, news) | Red | Champion retention risk — validate key contacts still in role; cross-check WAU |
| CEO/CDO/CTO departure (Phase 5, news) | Red | Executive sponsor change — re-qualify immediately; do not assume project continues |
| Cost-cutting or budget freeze reported (Phase 5, news) | Red | Budget pressure — validate renewal funding and expansion approvals |
| Revenue miss or negative earnings (Phase 5, news) | Orange | Revenue pressure — renewal risk elevated; escalate to AE and CSM |
| Data breach or security incident (Phase 5, news) | Orange | Security event — open security posture conversation (ESM, private endpoints, SCIM) |
| Hiring freeze or no open data roles (Phase 5a) | Orange | Possible team stall — validate project is still active and resourced |

---

## Output format

Produce the report in two parts: **Territory summary first**, then per-account detail sections. This ensures the reader sees the most important findings immediately without scrolling.

**Part 1 — Territory summary (top of report):**

```markdown
## Territory summary

**Top positive signals — platform data:**
1. [Account] — [signal]
2. [Account] — [signal]

**Recent campaign engagement (last 90 days):**
1. [Account] — [N] contacts engaged: [event/campaign name], [date] (e.g. "5 contacts attended DAIWT Munich Nov 2025 incl. Head of IT")
2. [Account] — [contact name], [title] responded to [content offer], [date]

**Top positive signals — external intelligence:**
1. [Account] — [event/news/hiring signal]
2. [Account] — [event/news/hiring signal]

**Upcoming features with territory-wide relevance:**
1. [Feature name] ([milestone]) — relevant for [Account A], [Account B] because [shared pattern]
2. [Feature name] ([milestone]) — relevant for [Account C] because [pattern]

**Top risks requiring attention:**
1. [Account] — [risk + source: internal/external]
2. [Account] — [risk + source: internal/external]

**Accounts with most signals:** [list top 3]
**Accounts with external risk events:** [list any with Red external signals]
**Accounts with recent campaign activity:** [list accounts that had CampaignMember hits in Phase 4b, or "None" if none found]
**Baseline doc used:** [title and URL from go/baseline, resolved at run time]
```

**Part 1b — High Priority Specific Actions (immediately after territory summary):**

This section synthesises all signals from Phases 1–5b into a ranked, actionable to-do list for the account team. It must appear **after the territory summary and before per-account detail sections** so the reader knows exactly what to do first.

**Scope rules:**
- **Single account analysed:** Include all high-priority actions identified (no cap). Aim for 5–10.
- **Multiple accounts analysed:** Include the top 10 actions across all accounts, ranked by urgency and business impact. Prioritise actions that address HIGH risk signals, strong buying intent (senior contacts at events, webinar registrations for product-specific sessions), and fast expansion opportunities (new workspaces, active feature adoption with upgrade path).

**Structure for each action:**

```markdown
## High Priority Specific Actions

| Priority | Action | Account | Timing | Owner |
|---|---|---|---|---|
| 1 | [one-line action summary] | [Account Name] | [e.g. "Within 48h", "This week", "Before [date]"] | [AE / SA / AE + SA] |
| 2 | ... | ... | ... | ... |
...

### 1. [Action title — specific and concrete]

**Signal:** [The specific data point or event that makes this action urgent. Cite the source: campaign registration, job error rate, spend figure, job posting, news event, etc.]

**Action:** [2–4 sentences of specific guidance — who to contact, what to say, what to offer, and what the desired outcome is. Include dollar context where relevant (e.g. "$248K/month Jobs spend with 14.7% error rate"). Do not be generic — name the contact if known, reference the specific event or data point, and connect it to a concrete next step.]
```

**Prioritisation criteria (apply in this order):**
1. **Imminent buying intent:** Senior contact (Director+) registered for a product-specific webinar or event → follow up within 48h, before the conversation window closes.
2. **High-severity risk with spend at stake:** HIGH-flagged security or stability risk on a workload with >$50K/month spend → remediation offer this week.
3. **Named champion with scheduled event:** Known contact registered for upcoming Databricks roadmap/exec session → pre-brief and post-brief.
4. **Quick cost win:** Classic→Serverless or idle warehouse optimisation where savings > $10K/month → pitch as TCO win in current budget climate.
5. **Feature expansion with active adoption:** Account already consuming a feature (Genie, Apps, DLT) with a clear upgrade path (Research Agent beta, Lakebase, DLT Managed Freshness) → enrol or nominate.
6. **New geography or team signal:** Contact from a new region or team attended an event → discovery call to uncover new use case.
7. **UCO hygiene:** New workspaces without UCO coverage → map before quarter closes.
8. **Strategic competitive angle:** External news (partnership, agentic AI investment) creates a framing opportunity → position Databricks in the architecture conversation.

**What NOT to include:**
- Generic advice without a specific data point to justify it.
- Actions already captured as a "Needs attention" remediation with no proactive hook.
- Actions where the required contact is unknown and no outreach path exists.

---

**Part 2 — Per-account detail (after the actions section):**

Produce one section per account. Output **four** subsections: Positive signals (internal), Positive signals (external), Upcoming features to watch, and Needs attention. Only include signals and features where there is actual data or a found article/posting to support the finding — do not surface phantom signals.

**Dollar formatting rule:** Always express DBU-based signals as `$X spend (Y DBUs)` using Phase 2f data. Never report raw DBU counts alone when dollars are available. For event/user counts (Genie events, WAU, Assistant users) that have no direct dollar equivalent, show the count alongside the associated dollar line (e.g. "13,505 Genie events / $1,525 Genie spend").

```markdown
## Account: [Account Name]

**SFDC ID:** [ID] | **Primary Cloud:** [Azure/AWS/GCP] | **Running Workspaces:** [N] | **Total Spend (28d):** $[X] across [Y] DBUs

**SKU Spend Breakdown (last 28 days):**

| Product Area | Spend (28d) | DBUs (28d) |
|---|---|---|
| SQL / DBSQL | $[X] | [Y] |
| Jobs / Lakeflow | $[X] | [Y] |
| All-Purpose Compute | $[X] | [Y] |
| DLT (Lakeflow Pipelines) | $[X] | [Y] |
| Databricks Apps | $[X] | [Y] |
| [other non-zero rows...] | $[X] | [Y] |
| **TOTAL** | **$[X]** | **[Y]** |

*(Omit rows with $0 spend. Only show rows where spend > $0.)*

### Positive signals — platform data
- **[SIGNAL NAME]:** [What was observed — with $dollars (DBUs) from Phase 2f, or count for non-DBU metrics] → [Conversation hook or next action]

Examples of correct signal formatting:
- **DLT active:** $71,655 spend (229,179 DBUs) in 28 days → ...
- **Apps:** $33,410 spend (52,851 DBUs) in 28 days → ...
- **Genie Active:** 13,505 events / $1,525 Genie-attributed spend in 28 days → ...
- **SQL dominant workload:** $448,691 spend (939K DBUs) — 75% serverless already → ...
- **WAU +16.8% QoQ:** 5,049 WAU vs 4,321 prior quarter → ... *(WAU has no direct $ equivalent — show counts only)*

### Salesforce campaign engagement
- **[CAMPAIGN NAME (decoded)]** ([campaign type], [date]): [Contact Name], [Title] — [Status] → [Conversation hook, e.g. "Use the DAIWT Munich session as an opener — ask what they took away and whether the team saw the AI/BI demos"]

### Positive signals — external intelligence
- **[SIGNAL NAME]:** [What was found — with date/source] → [Conversation hook or next action]

### Upcoming features to watch
- **[FEATURE NAME]** ([milestone: GA/PuPr/PrPr]): [1-sentence why this matters for this specific account based on their usage pattern — include $ spend where relevant] → [Recommended action: enrol in preview / schedule demo / discuss with champion]

### Needs attention
- **[HIGH/MEDIUM/LOW]:** [What was observed — include $ spend context where relevant, e.g. "Jobs error rate 14.7% against $248K/month Jobs spend"] → [Specific remediation step]

*(No issues found for this account across the checked dimensions.)*
```

If no campaign membership records were found for an account in the last 90 days, omit the "Salesforce campaign engagement" section entirely.

If no external data was found for an account, omit the "Positive signals — external intelligence" section rather than showing it empty.

If no feature recommendations matched for an account, omit the "Upcoming features to watch" section rather than showing it empty.

If an account has no signals at all: `*(No notable signals found — data may be limited for this account.)*`

---

## Phase 7 — Google Doc delivery

After Phase 6 signal classification is complete, create a Google Doc using the `google-docs` skill.

**When to create the doc:**
- **Standalone run** (skill invoked directly, not from ae-biweekly-review): always create the doc and print the link.
- **Called from ae-biweekly-review with "include signals"**: return the markdown output to the caller. The biweekly skill will embed it in its own doc (Section 6). Do NOT create a separate doc in this case — avoid duplicate docs.

**Doc title:** `Account Signals: [AE Name] — [YYYY-MM-DD]`

If the AE name is not known (standalone run without AE context), use: `Account Signals: [owner email safe] — [YYYY-MM-DD]`

**Doc structure** (convert markdown to Google Doc using google-docs skill, markdown-first approach):

```markdown
# Account Signals Report
**AE:** [AE Name or "Territory"]
**Run date:** [YYYY-MM-DD]
**Accounts analysed:** [count]
**Data window:** last 28 days (signals), current fiscal quarter (WAU QoQ)
**Roadmap baseline:** [go/baseline title + URL, resolved at run time]

---

[Territory summary from Phase 6 — immediately after the header, includes upcoming features section]

---

[High Priority Specific Actions — summary table + detailed action write-ups; all actions for single account, top 10 cross-account for multi-account runs]

---

[Per-account detail sections from Phase 6 — one H2 per account, each with up to 4 subsections: platform signals, external intelligence, upcoming features, needs attention]
```

**Default save location:** Save the doc in the **root of the user's Google Drive** ("My Drive") unless the user specifies a different folder name or URL. Do not create a subfolder. Use the Drive API `parents` field with the root folder ID `root`:

```python
# In the google-docs creation call, set the parent to Drive root
body = {
    "title": doc_title,
    "parents": ["root"]   # saves to "My Drive" top level
}
```

If the user provides a folder (e.g. "save it in the Vibe Outputs folder"), resolve the folder ID first with a Drive files.list query filtered by `mimeType = 'application/vnd.google-apps.folder'` and `name = '<folder name>'`, then use that ID as `parents`.

**Steps:**
1. Load the `google-docs` skill.
2. Read the google-docs skill to check how it creates documents and whether it exposes a `parent_folder_id` parameter. If it does, pass `"root"` (or the resolved folder ID). If it does not, call the Drive API directly to move the newly created doc to the root: `PATCH /drive/v3/files/<doc_id>?addParents=root&removeParents=<current_parent>`.
3. Print the doc URL to the user.
4. If the doc creation fails, print the full markdown output directly to the console so the user has the content.

---

## Data sources reference

| Data | Source | Key join column |
|------|---------|-----------------|
| Workspace security flags + Databricks UUIDs | `main.certified.workspaces_latest` | `salesforce_account_id` (SFDC) → `account_id` (UUID) |
| Cluster DBR version and isolation mode | `main.centralized_system_tables.compute_clusters` | `account_id` (UUID) |
| SQL warehouse type and idle settings | `main.centralized_system_tables.compute_warehouses` | `account_id` (UUID) |
| Query patterns and client applications | `main.centralized_system_tables.query_history` | `account_id` (UUID) |
| Job success/error rates | `main.centralized_system_tables.lakeflow_job_run_timeline` | `account_id` (UUID) |
| Job automation maturity | `main.centralized_system_tables.lakeflow_jobs` | `account_id` (UUID) |
| New workspaces created | `main.sfdc_bronze.workspace__c` | `Account__c` (SFDC account ID) |
| New workspaces first-consuming | `main.fin_live_gold.paid_usage_metering` | `sfdc_account_id` |
| **SKU dollar + DBU breakdown by product area** | **`main.fin_live_gold.paid_usage_metering`** | **`sfdc_account_id`; filter `is_paying = 'true'`** |
| **Feature-level dollars (Genie, Lakeview, DLT, Apps, SQL, Model Serving, Vector Search, Lakebase)** | **`main.fin_live_gold.paid_usage_metering` — struct fields `sales_comp_metric.*` and `product_lines_metric.ai.*`** | **`sfdc_account_id`; use dot notation (not `get_json_object`)** |
| WAU trends (QoQ) | `main.gtm_gold.account_active_users_quarterly` | `account_id` = SFDC account ID (not UUID) |
| Feature adoption event/user counts (Genie, Assistant, DLT, MLflow, Apps) | `main.data_product_features.account_metrics` | `salesforce_account_id` (not `sfdc_account_id`) |
| Campaign and marketing engagement (last 90 days) | Salesforce `CampaignMember` + `Campaign` via `sf data query` CLI | `Contact.AccountId` (SFDC account ID) |

---

## Checklist

- [ ] Territory account IDs resolved (from caller or standalone AE lookup).
- [ ] Phase 1 complete: `workspaces_latest` queried; `workspace_uuid_map` (SFDC → UUID list) persisted.
- [ ] Phase 2 complete: all five centralized system tables queries run using UUIDs.
- [ ] Phase 2f complete: PUM dollar breakdown queried (product-level + feature struct fields); `sku_dollars` map persisted per account with total dollars, total DBUs, and feature-level dollar splits.
- [ ] Phase 3 complete: SFDC workspace creation query + PUM first-consumption query + WAU QoQ query all run.
- [ ] Phase 4 complete: `account_metrics` queried for latest snapshot per account; DBU/event counts paired with Phase 2f dollar figures.
- [ ] Phase 4b complete: Salesforce CampaignMember queried for all territory account contacts (last 90 days); `campaign_signals` map persisted per account; `Status = 'Sent'`-only records excluded.
- [ ] Phase 5 complete: external research run (job postings + news + blog) for priority accounts; results persisted.
- [ ] Phase 5b complete: go/baseline URL resolved via browser; doc fetched; features matched to each account's behavioral signals; up to 3 recommendations per account persisted.
- [ ] Phase 6 complete: signals classified (internal + external + upcoming features); territory summary written first (including upcoming features section); **"High Priority Specific Actions" section produced immediately after territory summary** (all actions for single account; top 10 cross-account for multi-account runs); per-account markdown sections follow with 4 subsections each. **All DBU signals expressed as "$X spend (Y DBUs)".** Account headers include total spend + SKU table.
- [ ] Phase 7 complete: Google Doc created (standalone run) OR markdown returned to caller (biweekly integration). Doc URL printed.
- [ ] Only signal findings with data support are surfaced — no phantom signals from NULL/zero values.
