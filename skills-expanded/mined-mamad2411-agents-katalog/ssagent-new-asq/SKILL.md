---
name: ssagent-new-asq
description: Starts a new ASQ engagement. Fetches the ASQ from Salesforce, scaffolds a Databricks Asset Bundle with notebooks, research, and docs folders, and suggests running the researcher next.
user-invocable: true
model: sonnet
---

# SSA — New ASQ Setup

Bootstrap a local development environment for a new ASQ engagement.

**Usage:** `/ssagent-new-asq AR-000098660` or `/ssagent-new-asq santander`

---

## Prerequisites

Load the profile using `load_profile.py` from `ssagent-sfdc` (returns all keys with defaults applied). Extract `sf_org`. If `None`, fall back to `fe-salesforce-tools:salesforce-authentication`.

Substitute the resolved `sf_org` value as a **literal** into every `<SF_ORG_USERNAME>` placeholder below.

Get today's date:
```bash
python3 -c "from datetime import date; print(date.today())"
```

---

## Step 1 — Resolve ASQ

Parse `$0` using the **Fuzzy ASQ Lookup** pattern from `ssagent-sfdc`:
- If it starts with `AR-` → direct fetch by AR number
- Otherwise → fuzzy match against open ASQs by customer name fragment, confirm with the user

Once confirmed, fetch the full record:
```bash
sf data query --query "SELECT Id, Name, Account_Name__c, Status__c, Request_Description__c, Support_Type__c, AssignmentDate__c, End_Date__c FROM ApprovalRequest__c WHERE Name = '<AR-XXXXXXXXX>'" --target-org <SF_ORG_USERNAME> --json
```

Extract:
- `SFDC_ID` = `Id`
- `AR_NUMBER` = `Name`
- `CUSTOMER_RAW` = `Account_Name__c`
- `DESCRIPTION` = `Request_Description__c`
- `SUPPORT_TYPE` = `Support_Type__c`

---

## Step 2 — Propose Folder Name

Derive the folder name components:

1. **customer** — lowercase, spaces and special chars removed or replaced with underscores, max 20 chars
   - "Munich Re" → `munichre`
   - "Telefónica Germany" → `telefonica_germany`
2. **date** — today in `yyyymmdd` format
3. **topic** — derived from `Request_Description__c` or `Support_Type__c`, lowercase with underscores, max 30 chars
   - Keep it short and meaningful: `ml_platform`, `data_migration`, `uc_upgrade`
   - If the description is too vague to derive a topic, ask the user

Compose: `<customer>_<yyyymmdd>_<topic>`

Example: `munichre_20260219_ml_platform`

Present to the user for confirmation:
```
New ASQ engagement setup:

  ASQ:       AR-000098660
  Customer:  Munich Re
  Topic:     ML platform assessment
  Folder:    <ASQ_ROOT>/munichre_20260219_ml_platform/

[A] Accept  [E] Edit folder name
```

Wait for confirmation. If **E**: let the user provide the full folder name.

---

## Step 3 — Select Databricks Workspace

### 3a — Detect Target Cloud

Scan `DESCRIPTION` for cloud hints to determine the likely target platform:

| Hint in description | Cloud |
|---|---|
| `Azure`, `ADB`, `azuredatabricks`, `ADLS`, `ABFSS` | Azure |
| `AWS`, `S3`, `EMR`, `Redshift` | AWS |
| `GCP`, `BigQuery`, `GCS` | GCP |

If no hint is found, default to `AWS`.

### 3b — List Available Profiles

```bash
databricks auth profiles 2>/dev/null
```

Parse each profile's host and validity (`YES`/`NO`). Classify by cloud:
- `*.azuredatabricks.net` → Azure
- `*.cloud.databricks.com` → AWS
- `*.gcp.databricks.com` → GCP

### 3c — Present Workspace Options

Sort profiles: valid + matching cloud first, valid + other cloud second, invalid last. Present to the user:

```
Target cloud (from ASQ description): Azure

Available workspaces:
  ★ 1. logfood (Azure) — https://adb-2548836972759138.18.azuredatabricks.net — ✓ valid
    2. e2-demo-west (AWS) — https://e2-demo-field-eng.cloud.databricks.com — ✓ valid
    3. fevm-timo-test (AWS) — https://fevm-timo-test-workspace.cloud.databricks.com — ✗ expired

  [N] New workspace — authenticate to a different host

★ = recommended (matches target cloud)
```

Wait for the user to pick a workspace.

- If they choose an existing valid profile → use it
- If they choose an expired profile → re-authenticate: `databricks auth login --host <HOST> --profile <PROFILE>`
- If they choose **N** → ask for the workspace URL, then: `databricks auth login --host <URL> --profile <new-profile-name>`

Note the final `<PROFILE>` and `<WORKSPACE_HOST>` for the bundle init.

---

## Step 4 — Scaffold the Bundle

Use profile `asq_root` (default `~/ASQ`) as the base directory:
```bash
ASQ_ROOT="<asq_root from profile or ~/ASQ>"
mkdir -p "$ASQ_ROOT"
```

**Check `auto_create_dab`** (profile, default `true`). If `false`, create only the folder structure without a DAB:
```bash
mkdir -p "$ASQ_ROOT/<FOLDER_NAME>"/{src/notebooks,research,docs,resources}
```
Then skip to Step 5.

If `auto_create_dab` is `true`, resolve the DAB template path (from the plugin cache):
```bash
DAB_TEMPLATE=$(ls -d ~/.claude/plugins/cache/fe-vibe/fe-ssagent/*/resources/dab-template 2>/dev/null | sort -V | tail -1)
```

If that path doesn't exist, fall back to the worktree copy or report an error.

Write a config file using profile `default_catalog` (default `users`) and run `databricks bundle init`:
```bash
cat > /tmp/ssagent-dab-config.json << 'DABEOF'
{
  "project_name": "<FOLDER_NAME>",
  "customer_name": "<CUSTOMER_RAW>",
  "asq_number": "<AR_NUMBER>",
  "engagement_topic": "<TOPIC>",
  "sfdc_id": "<SFDC_ID>",
  "default_catalog": "<default_catalog from profile or users>"
}
DABEOF

databricks bundle init "$DAB_TEMPLATE" \
  --output-dir "$ASQ_ROOT/" \
  --config-file /tmp/ssagent-dab-config.json \
  --profile <PROFILE>

rm -f /tmp/ssagent-dab-config.json
```

---

## Step 5 — Initialize Git and Change Directory

```bash
cd "$ASQ_ROOT/<FOLDER_NAME>" && git init && git add -A && git commit -m "Initial scaffold for <AR_NUMBER> — <CUSTOMER_RAW>"
```

**IMPORTANT:** After scaffolding, `cd` into the new folder so it becomes the working directory for the rest of the session:
```bash
cd "$ASQ_ROOT/<FOLDER_NAME>"
```

This means subsequent skills (like `/ssagent-researcher`) will run in the engagement context and can write to `research/` using relative paths.

---

## Step 6 — Summary and Next Steps

```
Engagement bundle created:

  <ASQ_ROOT>/<FOLDER_NAME>/
  ASQ: <AR_NUMBER> — <CUSTOMER_RAW>
  Workspace: <WORKSPACE_HOST>
  Bundle: <FOLDER_NAME>

  databricks.yml    — ready for `databricks bundle deploy`
  src/notebooks/    — add notebooks here
  research/         — will be populated by /ssagent-researcher
  docs/             — customer artifacts
  resources/        — DAB job/pipeline definitions

Working directory changed to <ASQ_ROOT>/<FOLDER_NAME>/

Next: run `/ssagent-researcher <AR_NUMBER>` to research this engagement.
```
