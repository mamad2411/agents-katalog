---
name: uco-sheet-sync
description: "Sync Use Case Object (UCO) tracking data from a Google Sheet to Salesforce. Reads UCO data from a structured spreadsheet, matches to existing SFDC records, updates fields (stage, dates, products, notes), runs hygiene validation, and emails a summary report with before/after diffs. Use when the user says 'sync UCOs from sheet', 'update UCOs from spreadsheet', 'sheet to salesforce sync', 'bulk UCO update from sheet', or wants to push UCO tracking data from Google Sheets to Salesforce."
user-invocable: true
---

# UCO Sheet Sync

Sync UCO tracking data from a Google Sheet to Salesforce with hygiene validation and email summary.

## Quick Start

```
Sync my UCO tracking sheet to Salesforce for Acme Corp
```
```
Update Salesforce UCOs from sheet 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms tab "Q1 Tracking" and email me a summary
```
```
Dry run: preview what would change if I synced sheet 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms to SFDC for Contoso
```

## Prerequisites

1. **Google Auth** — invoke the `google-auth` skill first
2. **Salesforce Auth** — invoke the `salesforce-authentication` skill first

## Input Parameters

| Parameter | Required | Description |
|---|---|---|
| `account_name` | Yes | SFDC account name (used in SOQL WHERE clause) |
| `sheet_id` | Yes | Google Sheet ID (from the URL) |
| `tab_name` | Yes | Sheet tab/worksheet name |
| `recipients` | Yes | Comma-separated email addresses for the summary report |
| `column_mapping` | No | JSON mapping of sheet columns to SFDC fields (see defaults below) |
| `dry_run` | No | If `true`, preview changes without writing to SFDC (default: `false`) |

## Default Column Mapping

| Sheet Column | SFDC Field | Notes |
|---|---|---|
| E | Name (match key) | Used to match sheet rows to SFDC records |
| F | Use_Case_Description__c | Skip if empty |
| I | Use_Case_Type__c | Convert commas to semicolons for multipicklist |
| S | Stages__c | Map stage labels to U1-U6 codes (see Stage Mapping) |
| T | CustomMonthlyTotalDollarDBUs__c | Numeric — strip non-numeric characters |
| V | Implementation_Start_Date__c | Convert to YYYY-MM-DD |
| W | Full_Production_Date__c | Convert to YYYY-MM-DD |
| Y | Demand_Plan_Next_Steps__c | Full history — replaces SFDC value |

## Stage Mapping

| Sheet Value | SFDC Value |
|---|---|
| 1 - New/ Validating | U1 |
| 2 - In Scoping | U2 |
| 3 - Evaluating | U3 |
| 4 - Confirming | U4 |
| 5 - Onboarding | U5 |
| 6 - Live | U6 |

Match by prefix number (e.g. any value starting with "1" → U1, "2" → U2, etc.).

## Workflow

### Step 1: Authenticate

1. **Google**: invoke the `google-auth` skill to get an access token
2. **Salesforce**: run `sf org display --target-org {ORG}` to resolve the org username and confirm auth

### Step 2: Read Google Sheet

Use the Google Sheets API via gcloud CLI + curl:

```bash
ACCESS_TOKEN=$(gcloud auth print-access-token)
SHEET_ID="{sheet_id}"
TAB="{tab_name}"
RANGE="${TAB}!A3:Z"

curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "x-goog-user-project: gcp-sandbox-field-eng" \
  "https://sheets.googleapis.com/v4/spreadsheets/${SHEET_ID}/values/${RANGE}"
```

- Read from row 3 onwards (rows 1-2 are headers)
- Parse each row using the column mapping
- Skip rows where the Name column (E) is empty
- Trim whitespace from all values

### Step 3: Query Salesforce UCOs

Query existing UCOs for the account:

```sql
SELECT Id, Name, Stages__c, Use_Case_Description__c, Use_Case_Type__c,
       Implementation_Start_Date__c, Full_Production_Date__c,
       Demand_Plan_Next_Steps__c, CustomMonthlyTotalDollarDBUs__c
FROM UseCase__c
WHERE Account__r.Name = '{ACCOUNT_NAME}'
  AND Stages__c IN ('U1','U2','U3','U4','U5')
```

Run via `sf data query --query "..." --target-org {ORG} --json`.

For each returned UCO:
- Save all current field values as BEFORE snapshot for change tracking
- Build the Salesforce URL: `https://databricks.lightning.force.com/lightning/r/UseCase__c/{Id}/view`
- Match to sheet rows by Name (column E) — case-insensitive, trimmed

### Step 4: Update SFDC

For each matched UCO where the sheet has different values:

1. Build the update payload with only changed fields
2. Apply field transformations:
   - **Use_Case_Type__c**: replace commas with semicolons (SFDC multipicklist delimiter)
   - **Stages__c**: map sheet label to U-code using the Stage Mapping table
   - **Dates**: convert to YYYY-MM-DD format
   - **CustomMonthlyTotalDollarDBUs__c**: parse as number, strip `$` and `,`
3. Run the update:

```bash
sf data update record --sobject UseCase__c --record-id {Id} \
  --values "{field1}='{value1}' {field2}='{value2}'" \
  --target-org {ORG} --json
```

**Rules:**
- Do NOT update a field if the sheet value is empty/blank
- Do NOT create new UCOs — only update existing matches
- Track every change: record the field name, BEFORE value, and AFTER value
- If `dry_run` is true, log what would change but skip the actual update

### Step 5: Hygiene Check

Run these 6 validation rules against ALL U1-U5 UCOs for the account (not just those matched from the sheet):

| # | Rule | Severity |
|---|---|---|
| 1 | Stage U1 with no onboarding or go-live dates | Info (U1 is early stage) |
| 2 | Stage ≤ U3 but go-live date is in the past | Warning |
| 3 | Stage ≥ U5 but onboarding date is in the future | Warning |
| 4 | Go-live date before onboarding date | Error |
| 5 | No products set (Use_Case_Type__c is empty) | Warning |
| 6 | Stage U5 but no onboarding date | Warning |

For each flagged UCO, record the rule number, UCO Name, and Salesforce URL.

### Step 6: Send Summary Email

Use `gmail_builder.py` from the gmail skill resources to send an HTML email to the specified recipients.

The email should contain these 5 sections:

**TL;DR box** (styled callout at the top):
- Number of UCOs updated
- Number of hygiene issues found
- Number of unmatched sheet entries
- Total pipeline $DBU/mo across U1-U5

**Section 1: Updates Made**
- Table with columns: UCO Name (hyperlinked to SFDC), Field, Before, After
- Group rows by UCO
- If dry run, title this "Proposed Updates (Dry Run)" instead

**Section 2: Full UCO Pipeline**
- Table grouped by stage (U1 through U5), sorted by Name within each group
- Columns: Stage, UCO Name (hyperlinked), Products, $DBU/mo, Onboarding Date, Go-Live Date
- Include stage subtotals for $DBU/mo

**Section 3: Hygiene Issues**
- Bullet list with severity icon, UCO Name (hyperlinked), and rule description
- If no issues: "No hygiene issues found"

**Section 4: Unmatched Sheet Entries**
- List of sheet row names that did not match any SFDC UCO
- These may be new use cases that need to be created manually

**Section 5: Stage Distribution**
- Summary table: Stage, Count, Total $DBU/mo

**Footer:**
- Link to the source Google Sheet
- Link to the SFDC account page
- Timestamp of the sync

## Scheduling

You can use the `fe-macos-scheduler` skill to run this sync on a recurring basis. For example, to sync every Saturday morning:

```
Schedule uco-sheet-sync to run every Saturday at 9am: sync UCO sheet {sheet_id} tab "Tracking" for Acme Corp and email me at user@databricks.com
```

## Safety Rules

- **Never creates new UCOs** — only updates existing matches by Name
- **Never deletes UCO data** — only overwrites fields where the sheet has a non-empty value
- **Dry run mode** — set `dry_run: true` to preview all changes without writing to SFDC
- **All changes are logged** — every update records the field, before value, and after value in the summary email
- **No destructive actions on unmatched entries** — sheet rows without SFDC matches are reported but not acted on
