---
name: lakebase-usage
description: Analyze Lakebase usage for a specific customer account. Use ONLY when a Field Engineering employee (SA/DSA) asks about Lakebase adoption, consumption, instances, databases, data sync pipelines, or trends for a named customer. Do NOT use for general Lakebase questions, creating Lakebase instances, Lakebase documentation, or non-customer-specific analysis.
user-invocable: true
invocation-hints:
  - "lakebase usage for <customer>"
  - "how is <customer> using lakebase"
  - "lakebase adoption at <customer>"
  - "lakebase consumption for <customer>"
  - "is <customer> using lakebase"
  - "lakebase analysis for <customer>"
  - "lakebase trends for <customer>"
  - "lakebase instances for <customer>"
anti-hints:
  - "create a lakebase instance"
  - "how does lakebase work"
  - "lakebase documentation"
  - "deploy lakebase"
  - "set up lakebase"
  - "troubleshoot lakebase"
  - "lakebase pricing"
  - "lakebase vs aurora"
  - "lakebase discovery questions"
---

# Lakebase Usage Analysis

Analyze Lakebase adoption, consumption, and operational health for a specific customer account. Produces a comprehensive summary covering active instances, provisioned vs autoscaling breakdown, managed Postgres catalogs/tables, data sync pipeline health, DBU/dollar consumption with trailing window trends, and actionable recommendations for growing Lakebase usage.

**Audience:** SAs and DSAs from Field Engineering who need to understand how a customer is using Lakebase — for account reviews, expansion conversations, adoption tracking, or preparing for customer meetings.

## Prerequisites

1. **Databricks CLI authenticated with logfood profile**: Run `/databricks-authentication` if needed, then verify:
   ```bash
   databricks auth profiles | grep logfood
   ```
   If not valid: `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`

2. **Warehouse selected**: Use `/databricks-warehouse-selector` with `--profile=logfood` to select a SQL warehouse.

## Workflow

### Step 1: Get Customer Name

Ask the user for the customer name (Salesforce account name). This is used to filter all queries.

**Important:** Customer names vary across tables:
- `customer` in `main.eng_brickstore.brickstore_latest_daily_customer_instances_snapshot`
- `customer_name` in `main.eng_brickstore.brickstore_managed_postgres_catalogs` and related tables
- `sfdc_account_name` in `main.fin_live_gold.paid_usage_metering`
- `salesforce_account_name` in `main.certified.workspaces_latest` (joined to `main.eng_dlt` tables)

If unsure of exact name, run a fuzzy lookup first:
```sql
SELECT DISTINCT customer
FROM main.eng_brickstore.brickstore_latest_daily_customer_instances_snapshot
WHERE customer ILIKE '%<partial_name>%'
```

### Step 2: Run Queries

Execute queries against the Logfood workspace using:
```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{"statement": "<SQL>", "warehouse_id": "<WAREHOUSE_ID>", "format":"JSON_ARRAY", "wait_timeout":"50s"}'
```

For queries that may take >10 seconds, use async polling:
```bash
# If status is PENDING, poll:
databricks api get /api/2.0/sql/statements/<STATEMENT_ID> --profile=logfood
```

**For complex queries with nested quotes, use a Python script** (write to /tmp/ and execute) with `json.dumps()` for payload serialization to avoid shell escaping issues.

Run these queries in order (some may be run in parallel):

#### 2a. Active Instances Overview

Get all active Lakebase instances for the customer — instance IDs, workspace, cloud, region, instance type (provisioned vs autoscaling), HA status, instance size, data size. See `resources/QUERIES.md` Section 1.

#### 2b. Usage Summary (Instances, Catalogs, Tables)

Get per-workspace summary with instance count, managed Postgres catalog count, Postgres table count, and online table count. See `resources/QUERIES.md` Section 2.

#### 2c. Daily Revenue & Consumption (Last 35 Days)

Get daily DBU/dollar consumption broken down by usage type (COMPUTE_TIME, STORAGE_SPACE, DLT/sync). See `resources/QUERIES.md` Section 3.

#### 2d. Consumption Trends (Trailing Windows)

Get 7d/14d/28d/60d/90d consumption with period-over-period % change for Lakebase products. See `resources/QUERIES.md` Section 4.

#### 2e. Data Sync Pipelines — Daily Activity (Last 30 Days)

Get daily pipeline counts by mode (continuous vs triggered/snapshot) to understand data sync adoption. See `resources/QUERIES.md` Section 5.

#### 2f. Data Sync Pipelines — Triggered Pipeline Health

Get success/failure status for triggered (non-continuous) data sync pipelines over last 30 days. See `resources/QUERIES.md` Section 6.

#### 2g. Data Sync Pipelines — Continuous Pipeline Failures

Get recent failures for continuous data sync pipelines (last 3 days). See `resources/QUERIES.md` Section 7.

#### 2h. Instance Details — Performance Metrics (Optional)

Get detailed bi-minutely performance metrics (data size, instance size CUs) for deep-dive analysis. See `resources/QUERIES.md` Section 8.

#### 2i. Lakebase Use Cases (UCOs)

Get Salesforce Use Case Objects related to Lakebase — stages, estimated DBUs, competitors, implementation status. See `resources/QUERIES.md` Section 9.

### Step 3: Compile the Summary

Present a structured summary with the following sections. Use tables, bullet points, and clear formatting.

#### Summary Template

```markdown
# Lakebase Usage Report: {Customer Name}
**Generated:** {date}

## Executive Summary
- {1-2 sentence overview: active/inactive, growing/declining, provisioned/autoscaling, key use case patterns}

## Account Info
| Field | Value |
|-------|-------|
| Account Name | ... |
| Workspaces with Lakebase | ... |
| Total Active Instances | ... |
| Instance Types | Provisioned / Autoscaling / Both |
| Cloud(s) | AWS / Azure / GCP |
| Region(s) | ... |

## Instance Breakdown
| Workspace | Instance ID | Type | HA | Region | Data Size (GB) | Instance Size (CU) |
|-----------|-------------|------|-----|--------|---------------|-------------------|
| ... | ... | Provisioned/Autoscaling | Yes/No | ... | ... | ... |

**Observations:**
- Number and type of instances (provisioned vs autoscaling)
- High-availability configuration
- Data sizes — are they growing?
- Instance sizing — over/under-provisioned?

## Managed Postgres Assets
| Workspace | Catalogs | Postgres Tables | Online Tables |
|-----------|----------|-----------------|---------------|
| ... | ... | ... | ... |

**Observations:**
- Are they using managed catalogs (indicates deeper adoption)?
- Online tables indicate serving use cases
- Table count indicates breadth of workloads

## Consumption Overview
| Metric | Last 7D | Last 28D | Last 90D | Trend |
|--------|---------|----------|----------|-------|
| Lakebase $ (Compute) | ... | ... | ... | {+/-}% |
| Lakebase $ (Storage) | ... | ... | ... | {+/-}% |
| Lakebase $ (Sync/DLT) | ... | ... | ... | {+/-}% |
| Total Lakebase $ | ... | ... | ... | {+/-}% |

**Daily Revenue Breakdown (Last 35D):**
- {Commentary on daily revenue chart — spikes, trends, compute vs storage vs sync split}
- {Usage type breakdown: COMPUTE_TIME = instance compute, STORAGE_SPACE = data storage, DLT = data sync pipelines}

## Data Sync Pipeline Health
| Metric | Value |
|--------|-------|
| Active Triggered Pipelines | ... |
| Active Continuous Pipelines | ... |
| Triggered Success Rate (L30D) | ...% |
| Continuous Pipeline Failures (L3D) | ... |

**Pipeline Observations:**
- Are they using data sync (Lakehouse ↔ Lakebase sync)?
- Triggered vs continuous split
- Any failure patterns or reliability issues?

## Use Case Assessment

Based on the data patterns observed, classify the customer's Lakebase usage into these use case categories:

| Use Case Pattern | Evidence | Status |
|-----------------|----------|--------|
| **Application Backend** | {e.g., Provisioned instances, online tables, steady compute} | Active / Likely / Not detected |
| **Reverse ETL / Data Serving** | {e.g., Sync pipelines, online tables, read-heavy patterns} | Active / Likely / Not detected |
| **Agentic State** | {e.g., Small instances, JSONB patterns, agent-related workloads} | Active / Likely / Not detected |
| **Offline Analytics (Sync to Lakehouse)** | {e.g., Continuous sync pipelines, DLT usage} | Active / Likely / Not detected |

## Lakebase UCOs
| Use Case | Stage | Est Monthly DBUs | Est Monthly $ | Competitors | Status |
|----------|-------|------------------|---------------|-------------|--------|
| ... | U3-Evaluating | ... | ... | ... | ... |

## Recommendations
- {Based on the data, suggest actionable next steps}
- {E.g., "Customer is on Provisioned only — introduce Autoscaling for dev/test to reduce costs (Scale-to-Zero)"}
- {E.g., "No data sync pipelines detected — explore Lakehouse Sync for analytics on operational data"}
- {E.g., "Customer has online tables — they're serving data to apps, explore expanding app backend use cases"}
- {E.g., "Consumption is growing steadily — discuss production readiness and HA configuration"}
- {E.g., "Customer uses only 1 instance — explore Database Branching for dev/test environments"}
- {E.g., "High storage but low compute — investigate if they could benefit from Autoscaling"}
- {E.g., "Customer has Lakebase UCOs at U3/U4 — follow up on evaluation progress"}
- {E.g., "No online tables or sync — customer may be early stage, offer Lakebase workshop"}

### Growth Playbook Reference

Use these discovery questions based on the customer's current usage pattern:

**If customer has App Backend usage:**
- "What app(s) are we powering (users, peak concurrency, read/write mix)?"
- "What's your current operational DB and what's painful (ops, scaling, releases)?"
- "How do you move operational data into the lakehouse today?"
- "How long does it take to spin up a dev/test environment? Have you tried Database Branching?"

**If customer has no Sync/Reverse ETL:**
- "Which Unity Catalog tables need to be served to an app? What freshness SLA?"
- "Are you using Census, Hightouch, or custom scripts for reverse ETL?"
- "What's the app's access pattern (keys, filters, joins)?"

**If customer uses Provisioned only:**
- "Do you have databases that only see traffic during business hours? (pitch Scale-to-Zero)"
- "How many staging environments are running that could benefit from instant branching?"

**If customer has low adoption:**
- "Are you building GenAI apps or chatbots? Lakebase is ideal for agent state management."
- "What operational databases are costing you time and money? (pitch consolidation)"
- "We're consolidating our data stack — have you considered Lakebase as a unified OLTP+OLAP platform?"

### Competitive Context

When recommending next steps, keep these competitive differentiators in mind:
- **vs Aurora/RDS:** Lakebase has <1s cold start (Aurora ~25-45s), true scale-to-zero, instant branching
- **vs Azure Database for PostgreSQL:** Lakebase has true scale-to-zero (Azure doesn't), no monolithic storage constraints
- **vs Snowflake Postgres:** Lakebase is GA today with separated compute/storage, instant autoscaling, $0 when idle
- **All competitors:** Lakebase is the only solution that unifies OLTP and OLAP data with Unity Catalog governance
```

### Step 4: Offer Follow-ups

After presenting the summary, offer the user:
1. **Drill down** into a specific workspace or instance's performance metrics
2. **Compare** consumption trends over a longer window
3. **Export** the summary as a Google Doc (use `/google-docs` skill)
4. **Check UCO blockers** for Lakebase at this customer
5. **Run competitive analysis** if the customer uses Aurora/RDS/AlloyDB/CosmosDB

## Key Tables Reference

| Table | Description |
|-------|-------------|
| `main.eng_brickstore.brickstore_latest_daily_customer_instances_snapshot` | Active Lakebase instances — customer, workspace, endpoint, cloud, region, HA, instance size |
| `main.eng_brickstore.brickstore_managed_postgres_catalogs` | Managed Postgres catalogs per workspace |
| `main.eng_brickstore.brickstore_managed_postgres_tables` | Managed Postgres tables per workspace |
| `main.eng_brickstore.brickstore_postgres_online_tables` | Online tables (data serving) per workspace |
| `main.eng_brickstore.pg_product_metrics_biminutely` | Bi-minutely performance metrics — data size, instance size CUs |
| `main.fin_live_gold.paid_usage_metering` | Financial consumption — DBUs, dollars, SKU breakdowns by account/workspace/day |
| `main.eng_dlt.pipelines` | DLT pipeline metadata (filter `pipeline_type = 'DATABASE_TABLE_SYNC'` for Lakebase sync) |
| `main.eng_dlt.updates` | DLT pipeline run events — start/end time, state (COMPLETED/FAILED) |
| `main.certified.workspaces_latest` | Workspace metadata with Salesforce account names |
| `main.gtm_silver.use_case_detail` | Salesforce UCO details with stages, competitors, estimated DBUs |

## Related Skills

- `/logfood-querier` — For ad-hoc Logfood queries beyond Lakebase analysis
- `/genie-spaces-usage` — Analyze Genie Spaces usage for the same customer
- `/lakeflow-connect-usage` — Analyze Lakeflow Connect usage for the same customer
- `/databricks-authentication` — CLI authentication setup
- `/databricks-warehouse-selector` — Select warehouse for query execution
- `/google-docs` — Export the summary as a Google Doc
- `/competitive-analysis` — Compare Lakebase vs Aurora/RDS/AlloyDB/CosmosDB
