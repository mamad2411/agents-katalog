---
name: feature-preview-lookup
description: Look up what phase a Databricks feature preview is in (Private Preview, Beta, Public Preview, GA) and check if a customer workspace is enrolled/enabled. Cross-references with workspace ring to explain feature availability. Use when asked about preview status, feature rollout stage, whether a customer has access to a preview feature, or what previews a customer is enrolled for.
user-invocable: true
---

# Feature Preview Lookup

Looks up the phase of a Databricks feature preview and checks whether a customer workspace is enrolled or enabled for it. Cross-references the workspace ring to explain when the feature should be available.

## Ring & Phase Rollout Matrix

Features auto-enable based on ring and release phase:

| Target Ring | PrPr | Beta | PuPr | GA | GA + 30d | GA + 6mo |
|-------------|------|------|------|----|----------|----------|
| **Ring 3** (Premium AWS/GCP) | INVITE ONLY | ON | ON | ON | ON | ON |
| **Ring 2** (Enterprise AWS/GCP + Premium Azure) | INVITE ONLY | OFF | ON | ON | ON | ON |
| **Ring 1** (ESC/CSP workspaces) | INVITE ONLY | OFF | OFF | OFF | ON | ON |
| **Ring 0** (Whitelisted - WIP) | INVITE ONLY | OFF | OFF | OFF | OFF | ON |

## Instructions

### Step 1: Authenticate with Logfood

```bash
databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood
```

### Step 2: Select a Warehouse

Use the `databricks-warehouse-selector` skill with `--profile=logfood`.

### Step 3: Look Up Preview Phase

Search for the preview by name in the SFDC preview definitions table. Use fuzzy matching with LIKE:

```sql
SELECT
  Name,
  FP_Cloud_Type__c AS cloud,
  FP_Preview_Phase__c AS phase,
  FP_Preview_Key__c AS preview_key,
  FP_Deployment_Level__c AS deployment_level,
  FP_Description__c AS description,
  Id AS preview_sfdc_id
FROM main.sfdc_bronze.fp_preview__c
WHERE IsDeleted = FALSE
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_preview__c)
  AND FP_Preview_Key__c IS NOT NULL
  AND FP_Preview_Key__c NOT LIKE 'legacy_%'
  AND Name LIKE '%<FEATURE_NAME>%'
ORDER BY Name, cloud
```

Execute with:
```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{"statement": "<SQL>", "warehouse_id": "<WAREHOUSE_ID>", "format":"JSON_ARRAY", "wait_timeout":"50s"}'
```

### Step 4: Check Customer Enrollment (Optional)

If a workspace ID or customer account is provided, check whether they are enrolled for the preview via the SFDC approval/enrollment chain:

```sql
SELECT
  preview.Name AS preview_name,
  preview.FP_Cloud_Type__c AS cloud,
  preview.FP_Preview_Phase__c AS phase,
  account.Name AS account_name,
  approval.FP_Status__c AS approval_status,
  enrollment.FP_Status__c AS enrollment_status,
  enrollment.FP_Workspace_Id__c AS workspace_id,
  enrollment.FP_Enablement_Status__c AS enablement_status
FROM main.sfdc_bronze.fp_preview__c AS preview
JOIN main.sfdc_bronze.fp_approval__c AS approval
  ON preview.Id = approval.FP_Feature_Preview__c
  AND approval.IsDeleted = FALSE
  AND approval.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_approval__c)
JOIN main.sfdc_bronze.fp_enrollment__c AS enrollment
  ON approval.Id = enrollment.FP_Approval__c
  AND enrollment.IsDeleted = FALSE
  AND enrollment.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_enrollment__c)
JOIN main.sfdc_bronze.account AS account
  ON approval.FP_Account__c = account.Id
  AND account.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE preview.IsDeleted = FALSE
  AND preview.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_preview__c)
  AND preview.FP_Preview_Key__c IS NOT NULL
  AND preview.FP_Preview_Key__c NOT LIKE 'legacy_%'
  AND (
    enrollment.FP_Workspace_Id__c = '<WORKSPACE_ID>'
    OR account.Name LIKE '%<CUSTOMER_NAME>%'
  )
  AND preview.Name LIKE '%<FEATURE_NAME>%'
ORDER BY preview.Name
```

### Step 5: Check Settings DB for Actual State (Optional)

The Settings DB (`prod_settings_log`) is the source of truth for actual enablement. If you know the preview key, check actual enrollment/enablement state:

```sql
SELECT
  setting_type_name,
  key_name.workspace_id,
  setting_value.preview_enrollment_log_message.enrolled AS enrolled,
  setting_value.preview_enablement_log_message.enabled AS enabled
FROM main.eng_lumberjack.prod_settings_log
WHERE `_partition_date` = CURRENT_DATE() - 1
  AND setting_type_name IN ('<preview_key>', '<preview_key>_enrollment')
  AND key_name.workspace_id = <WORKSPACE_ID>
```

The `setting_type_name` for previews follows the pattern: `<preview_key_without_cloud_suffix>` for enablement and `<preview_key_without_cloud_suffix>_enrollment` for enrollment.

### Step 6: Cross-Reference with Workspace Ring

If a workspace ID is provided, invoke the `workspace-ring-lookup` skill (`/workspace-ring-lookup`) to determine the workspace's ring. Use the ring result to explain whether the feature *should* be available based on the ring + phase matrix above.

Do NOT duplicate the ring-determination SQL here — the `workspace-ring-lookup` skill is the single source of truth for ring logic.

### Step 7: Present Results

Summarize findings clearly:

1. **Preview Phase** — What phase the feature is in per cloud (Private Preview, Beta, Public Preview, GA, Gated Public Preview)
2. **Workspace Ring** — What ring the customer workspace is in
3. **Availability Assessment** — Cross-reference the phase × ring matrix to determine:
   - Is the feature currently available to this workspace?
   - If not, what needs to happen? (phase advancement, GA+30d wait, compliance certification, etc.)
4. **Enrollment/Enablement Status** — If enrolled via SFDC, show approval and enablement status
5. **Settings DB State** — If checked, show actual enabled/enrolled state from source of truth

### List All Previews

To list all current previews and their phases:

```sql
SELECT
  Name,
  FP_Cloud_Type__c AS cloud,
  FP_Preview_Phase__c AS phase,
  FP_Preview_Key__c AS preview_key
FROM main.sfdc_bronze.fp_preview__c
WHERE IsDeleted = FALSE
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_preview__c)
  AND FP_Preview_Key__c IS NOT NULL
  AND FP_Preview_Key__c NOT LIKE 'legacy_%'
ORDER BY Name, cloud
```

## Data Model Reference

| Table | Access | Description |
|-------|--------|-------------|
| `main.sfdc_bronze.fp_preview__c` | YES | Preview definitions — name, cloud, phase, key, description |
| `main.sfdc_bronze.fp_approval__c` | YES | Customer enrollment approvals (links preview → account) |
| `main.sfdc_bronze.fp_enrollment__c` | YES | Workspace-level enrollments (links approval → workspace) |
| `main.sfdc_bronze.account` | YES | Account names and metadata |
| `main.eng_lumberjack.prod_settings_log` | YES | Source of truth for actual enablement/enrollment state |
| `main.certified.workspaces_latest` | YES | Workspace metadata for ring determination |
| `main.it_sfdc_bronze_hourly.fp_preview__c` | NO | Hourly SFDC snapshot (use sfdc_bronze instead) |
| `main.eng_voice_of_the_customer.fp_silver_enroll_enable` | NO | Combined view (no access, use individual tables) |

## When SFDC Data Is Insufficient

If the preview is not found in the SFDC tables, or the user wants a broader view of the feature roadmap (upcoming features, planned timelines, feature status beyond what's in the Previews Platform), direct them to the **Asana Roadmap Board**:

https://app.asana.com/1/8808412813448/project/1207294417666725/list/1207294501101678

This board tracks all features and their preview status across the product. It is especially useful for:
- Features not yet launched through the Previews Platform
- Planned timelines and roadmap visibility
- Features in early planning stages before they have a preview key

Note: Asana requires manual browser access — there is no API integration available.

## Reference

- Wiki: https://databricks.atlassian.net/wiki/spaces/UN/pages/5575245850/Previews+Rings+Overview+go+launch-previews+intro
- Feature Previews Dashboard: https://adb-2548836972759138.18.azuredatabricks.net/dashboardsv3/01ee9ae78b921f82bb6e7272aa84fde2/published
- Asana Roadmap Board: https://app.asana.com/1/8808412813448/project/1207294417666725/list/1207294501101678
