---
name: workspace-ring-lookup
description: Look up what deployment ring a customer workspace is in. Rings determine feature rollout order and preview availability. Use when asked about workspace ring, stage, deployment tier, or feature rollout eligibility.
user-invocable: true
---

# Workspace Ring Lookup

Determines which deployment ring a Databricks workspace belongs to, which controls how features are rolled out via the Previews Platform.

## Ring Definitions

Rings segment customers by security & compliance sensitivity. Features roll out to less sensitive rings first.

| Ring | Sensitivity | Workspace Tier |
|------|-------------|----------------|
| **Ring 3** | Low | Premium Tier on AWS & GCP |
| **Ring 2** | Medium | Enterprise Tier on AWS & GCP + Premium Tier on Azure |
| **Ring 1** | High | Workspaces with Enhanced Security & Compliance (ESC/CSP) add-on |
| **Ring 0** | Max | Specific whitelisted customers (WIP - not yet implemented) |

## Feature Rollout by Ring and Release Stage

| Target Ring | PrPr | Beta | PuPr | GA | GA + 30d | GA + 6mo |
|-------------|------|------|------|----|----------|----------|
| **Ring 3** | INVITE ONLY | ON | ON | ON | ON | ON |
| **Ring 2** | INVITE ONLY | OFF | ON | ON | ON | ON |
| **Ring 1** | INVITE ONLY | OFF | OFF | OFF | ON | ON |
| **Ring 0** | INVITE ONLY | OFF | OFF | OFF | OFF | ON |

Key implications:
- **Ring 3** workspaces get features earliest — auto-enabled at Beta
- **Ring 2** workspaces get features at Public Preview
- **Ring 1** workspaces only get features 30 days after GA (with compliance certification required)
- **Ring 0** workspaces only get features 6 months after GA

## Instructions

### Step 1: Authenticate with Logfood

```bash
databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood
```

### Step 2: Select a Warehouse

Use the `databricks-warehouse-selector` skill with `--profile=logfood`.

### Step 3: Query the Workspace Ring

The ring is determined by the workspace's feature tier, cloud type, and CSP status. Run this query substituting the workspace ID:

```sql
WITH csp_workspaces AS (
  SELECT DISTINCT CAST(key_name.workspace_id AS STRING) AS workspace_id
  FROM main.eng_lumberjack.prod_settings_log
  WHERE `_partition_date` = CURRENT_DATE() - 1
    AND setting_type_name = 'shield_csp_enablement_ws_db'
    AND setting_value.csp_enablement_log_message.is_enabled = TRUE
)
SELECT
  workspace_id, cloud_type, workspace_name,
  salesforce_account_name AS account,
  feature_tier,
  CASE
    WHEN workspace_id IN (SELECT workspace_id FROM csp_workspaces) THEN 'Ring 1'
    WHEN feature_tier IN ('ENTERPRISE_TIER', 'ENTERPRISE_TIER_V2') AND cloud_type = 'aws' THEN 'Ring 2'
    WHEN feature_tier = 'STANDARD_W_SEC_TIER' AND cloud_type = 'aws' THEN 'Ring 3'
    WHEN cloud_type = 'azure' THEN 'Ring 2'
    WHEN feature_tier IN ('ENTERPRISE_TIER', 'ENTERPRISE_TIER_V2') AND cloud_type = 'gcp' THEN 'Ring 2'
    WHEN feature_tier = 'STANDARD_W_SEC_TIER' AND cloud_type = 'gcp' THEN 'Ring 3'
    ELSE CONCAT('Unknown: ', feature_tier)
  END AS workspace_ring
FROM main.certified.workspaces_latest
WHERE workspace_id = '<WORKSPACE_ID>'
```

Execute with:
```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{"statement": "<SQL>", "warehouse_id": "<WAREHOUSE_ID>", "format":"JSON_ARRAY", "wait_timeout":"50s"}'
```

### Step 4: Present Results

Present the workspace details and ring assignment clearly. Include:
- Workspace name, ID, cloud, and account
- Feature tier
- **Ring assignment** with what it means for feature rollout
- When this workspace gets features relative to other rings (reference the rollout table above)

### Multiple Workspaces

If the user provides multiple workspace IDs, modify the WHERE clause:
```sql
WHERE workspace_id IN ('<ID1>', '<ID2>', '<ID3>')
```

### Account-Wide Lookup

To look up all workspaces for a customer account, filter by account name:
```sql
WHERE salesforce_account_name LIKE '%<CUSTOMER_NAME>%'
```

## Reference

- Wiki: https://databricks.atlassian.net/wiki/spaces/UN/pages/5575245850/Previews+Rings+Overview+go+launch-previews+intro
- Feature Previews Dashboard: https://adb-2548836972759138.18.azuredatabricks.net/dashboardsv3/01ee9ae78b921f82bb6e7272aa84fde2/published
