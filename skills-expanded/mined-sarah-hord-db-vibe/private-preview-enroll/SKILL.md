---
name: private-preview-enroll
description: Enroll a customer workspace or account into a Databricks feature preview. Guides SAs/DSAs through the nomination process by collecting the required information (customer, preview, cloud, workspace IDs, use case) and creating the SFDC enrollment records. Use when asked to enroll, nominate, sign up, or request a preview for a customer. Do NOT use for checking or looking up what previews a customer is already enrolled in — use feature-preview-lookup instead.
user-invocable: true
---

# Preview Enrollment

Enrolls a customer workspace or account into a Databricks feature preview by creating the necessary SFDC records (FP_Approval__c and FP_Enrollment__c).

## Prerequisites

- Authenticated with Salesforce (`/salesforce-authentication`)
- Authenticated with Logfood for lookups (`databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`)

## Instructions

### Step 1: Gather Required Information

Collect the following from the user. Ask for anything not provided:

| Field | Required | Description |
|-------|----------|-------------|
| **Preview name** | Yes | The feature preview to enroll in (e.g., "Serverless GPU Compute", "AI Runtime") |
| **Customer/Account name** | Yes | The Salesforce account name |
| **Cloud** | Yes | AWS, Azure, or GCP — must match the preview's cloud |
| **Workspace ID(s)** | Depends | Required for workspace-level previews. Space-separated if multiple. Not needed for account-level previews. |
| **Use case** | Recommended | Brief description of why the customer needs this preview |
| **Region** | Optional | AMER, EMEA, APAC, or JAPAC |

### Step 2: Look Up the Preview

Use the `feature-preview-lookup` skill or query Logfood to find the preview and confirm it exists for the specified cloud:

```sql
SELECT Id, Name, FP_Cloud_Type__c AS cloud, FP_Preview_Phase__c AS phase,
       FP_Preview_Key__c AS preview_key, FP_Deployment_Level__c AS deployment_level
FROM main.sfdc_bronze.fp_preview__c
WHERE IsDeleted = FALSE
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_preview__c)
  AND FP_Preview_Key__c IS NOT NULL
  AND FP_Preview_Key__c NOT LIKE 'legacy_%'
  AND Name LIKE '%<PREVIEW_NAME>%'
  AND FP_Cloud_Type__c = '<CLOUD>'
```

Execute with:
```bash
databricks api post /api/2.0/sql/statements/ --profile=logfood --json='{"statement": "<SQL>", "warehouse_id": "<WAREHOUSE_ID>", "format":"JSON_ARRAY", "wait_timeout":"50s"}'
```

**Important checks before proceeding:**

1. **Enrollment eligibility:** Enrollments can only be created when a preview is in **Private Preview** or **Gated Public Preview**. If the preview is in Beta, Public Preview, or GA, enrollment is not needed — features in those phases are auto-enabled based on ring (see the rollout matrix in the `feature-preview-lookup` skill).

2. **Deployment level:** Note the `FP_Deployment_Level__c` value:
   - `Workspace Id` → workspace IDs are required
   - `Account Id` → enrollment is account-wide, no workspace IDs needed

Present the preview details to the user and confirm before proceeding.

### Step 3: Look Up the Customer Account

Find the Salesforce Account ID:

```sql
SELECT Id, Name FROM main.sfdc_bronze.account
WHERE processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
  AND Name LIKE '%<CUSTOMER_NAME>%'
  AND IsDeleted = FALSE
```

If multiple accounts match, present them and ask the user to confirm which one.

### Step 4: Check for Existing Enrollment

Before creating a new enrollment, check if one already exists:

```sql
SELECT approval.Id AS approval_id, approval.FP_Status__c AS approval_status,
       approval.FP_Workspace_Id__c AS workspace_ids,
       enrollment.FP_Workspace_Id__c AS enrolled_workspace,
       enrollment.FP_Status__c AS enrollment_status
FROM main.sfdc_bronze.fp_approval__c AS approval
LEFT JOIN main.sfdc_bronze.fp_enrollment__c AS enrollment
  ON approval.Id = enrollment.FP_Approval__c
  AND enrollment.IsDeleted = FALSE
  AND enrollment.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_enrollment__c)
WHERE approval.IsDeleted = FALSE
  AND approval.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.fp_approval__c)
  AND approval.FP_Feature_Preview__c = '<PREVIEW_SFDC_ID>'
  AND approval.FP_Account__c = '<ACCOUNT_SFDC_ID>'
```

If an enrollment already exists, inform the user and ask how to proceed (e.g., add additional workspaces, or skip).

### Step 5: Create the FP_Approval Record

Ensure authenticated with Salesforce first (`/salesforce-authentication`).

Resolve the SF target org:
```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
```

Create the approval record:

```bash
sf data create record --sobject FP_Approval__c \
  --values "FP_Feature_Preview__c='<PREVIEW_SFDC_ID>' \
  FP_Account__c='<ACCOUNT_SFDC_ID>' \
  FP_Status__c='Nominated' \
  FP_Nomination_Type__c='Standard Nomination' \
  FP_Cloud_Type__c='<CLOUD>' \
  FP_Deployment_Level__c='<DEPLOYMENT_LEVEL>' \
  FP_Workspace_Id__c='<WORKSPACE_IDS>' \
  FP_Use_Case_for_customer__c='<USE_CASE>'" \
  --target-org "$SF_TARGET_ORG" \
  --json
```

**Field mapping:**
| Field | Value |
|-------|-------|
| `FP_Feature_Preview__c` | The `Id` from `fp_preview__c` (e.g., `aOWVp0000002PqLOAU`) |
| `FP_Account__c` | The `Id` from `account` (e.g., `0016100001ZW6nKAAT`) |
| `FP_Status__c` | `Nominated` (initial status — approval happens downstream) |
| `FP_Nomination_Type__c` | `Standard Nomination` (or `Quick Nomination`) |
| `FP_Cloud_Type__c` | `AWS`, `Azure`, or `GCP` |
| `FP_Deployment_Level__c` | `Workspace Id` or `Account Id` (from the preview definition) |
| `FP_Workspace_Id__c` | Space-separated workspace IDs (for workspace-level previews) |
| `FP_Region__c` | `AMER`, `EMEA`, `APAC`, or `JAPAC` (optional) |
| `FP_Use_Case_for_customer__c` | Customer use case description (optional but recommended) |

Save the returned approval record ID for the next step.

### Step 6: Create FP_Enrollment Records (Workspace-Level Previews)

For workspace-level previews, create an enrollment record for each workspace:

```bash
sf data create record --sobject FP_Enrollment__c \
  --values "FP_Approval__c='<APPROVAL_RECORD_ID>' \
  FP_Workspace_Id__c='<WORKSPACE_ID>' \
  FP_Status__c='Nominated'" \
  --target-org "$SF_TARGET_ORG" \
  --json
```

Repeat for each workspace ID. For account-level previews, this step is not needed.

### Step 7: Confirm and Summarize

Present a summary to the user:

1. **Preview** — Name, cloud, current phase
2. **Customer** — Account name
3. **Deployment level** — Account or workspace
4. **Workspace(s)** — List of enrolled workspace IDs (if applicable)
5. **Status** — Nominated (pending approval by the preview team)
6. **Workspace ring** — Invoke `/workspace-ring-lookup` to show the ring for each workspace and explain what the ring means for this preview's availability based on its current phase
7. **Next steps** — The nomination will be reviewed by the preview team. The user can track status in the SFDC Preview Portal or by re-running `/feature-preview-lookup`.

## Nomination Types

| Type | When to Use |
|------|-------------|
| `Standard Nomination` | Default. Goes through normal approval flow. |
| `Quick Nomination` | For time-sensitive requests. Still requires approval but flagged as urgent. |

## Important Notes

- Nominations start in `Nominated` status. Approval is handled by the preview team, not by this skill.
- Enrollments can only be created for previews in **Private Preview** or **Gated Public Preview** with enrollment status **Open**. For Beta/PuPr/GA features, enrollment is unnecessary — they auto-enable by ring.
- For workspace-level previews, you must provide the Databricks workspace ID(s) — not the workspace name.
- Some previews may require Terms of Service (ToS) acceptance. The preview team may send ToS to the customer contact after nomination. The customer must accept before the preview is enabled.
- Once approved, the settings platform syncs enrollment hourly — the preview toggle will appear in the customer's workspace/account console within ~1 hour.
- All lookups (preview, account, existing enrollments, workspace validation) use Logfood for speed. Only the final record creation uses the Salesforce API since Logfood is read-only.
- Always confirm the details with the user before creating records in Salesforce.
- For questions or issues, reach out on Slack: **#feature-preview-discuss**

## Reference

- SFDC Preview Portal Guide: https://databricks.atlassian.net/wiki/spaces/UN/pages/3639869547/Full+SFDC+Preview+Portal+Guide+go+preview-portal
- Previews + Rings Overview: https://databricks.atlassian.net/wiki/spaces/UN/pages/5575245850/Previews+Rings+Overview+go+launch-previews+intro
- Feature Previews Dashboard: https://adb-2548836972759138.18.azuredatabricks.net/dashboardsv3/01ee9ae78b921f82bb6e7272aa84fde2/published
