---
name: financialforce-ip-project-create
description: Create productive utilization projects and budgets in FinancialForce/Certinia (pse__Proj__c, pse__Budget__c). Use when the user asks to create a presales project, partner oversight project, productive util project, budgeted util project, or process a request from #ps-budgeted-util-request. Covers DPP oversight, presales RSA support, and similar internal-funded project types.
---

# FinancialForce Productive Utilization Projects

Create productive utilization projects (`pse__Proj__c`) and associated budgets (`pse__Budget__c`) in Salesforce/FinancialForce for presales support, partner oversight (DPP), and similar internal-funded work.

## Prerequisites

1. **Salesforce CLI authenticated** — run `sf org display` to verify. If not connected, follow the `salesforce-authentication` skill.
2. **Target org alias** — identify which org to use via `sf org list`. Pass `--target-org <alias>` on every command.
3. **Slack MCP** — required if processing requests from the `#ps-budgeted-util-request` channel.

## Project Types

| Type | Name Pattern | Time Credited |
|------|-------------|---------------|
| Partner Oversight (DPP) | `FY25-26 Partner Oversight (DPP) - <Account Name>` | true |
| Presales RSA Support | `<Account Name> - Presales RSA Support` | true |

## Workflow

### Step 1 — Gather Request Details

Requests come from Slack channel `#ps-budgeted-util-request` (channel ID: `C08LT7HPE4T`) or directly from the user.

**Required inputs:**
- Account name
- Hours requested
- Start date and end date
- Justification / description
- Project type (Partner Oversight, Presales RSA, etc.)

**Check the thread for approval** — look for a reply from a manager/director confirming approval before proceeding.

To search for requests:
```
slack_read_api_call("search.messages", {"query": "<account> in:#ps-budgeted-util-request"})
```

To read a thread:
```
slack_read_api_call("conversations.replies", {"channel": "C08LT7HPE4T", "ts": "<thread_ts>"})
```

### Step 2 — Resolve All Reference IDs

Every lookup field must be resolved dynamically by name. **Never hardcode IDs.**

#### Account (`pse__Account__c`)
```bash
sf data query \
  --query "SELECT Id, Name FROM Account WHERE Name LIKE '%<account_name>%'" \
  --target-org <alias>
```

#### Parent Project (`pse__Parent_Project__c`)
Search for the active master project matching the project type:
```bash
sf data query \
  --query "SELECT Id, Name FROM pse__Proj__c WHERE Name LIKE '%Partner Oversight (DPP) MASTER%' AND pse__Is_Active__c = true ORDER BY CreatedDate DESC LIMIT 5" \
  --target-org <alias>
```
For presales: search `'%Presales%MASTER%'` or `'%Presales%Master%'` instead.

#### Project Manager (`pse__Project_Manager__c`)
This is a **Contact** lookup (not User). Look up by name:
```bash
sf data query \
  --query "SELECT Id, Name FROM Contact WHERE Name LIKE '%<pm_name>%' LIMIT 5" \
  --target-org <alias>
```
If PM is not specified, ask the user.

#### Region (`pse__Region__c`)
This is a custom object lookup. Common values:
```bash
sf data query \
  --query "SELECT Id, Name FROM pse__Region__c WHERE Name = '<region>'" \
  --target-org <alias>
```
Determine region from the account's geography (AMER for US/Canada, APJ for Asia-Pacific, EMEA for Europe/Middle East/Africa).

#### Practice (`pse__Practice__c`)
Always "Professional Services" for budgeted util projects:
```bash
sf data query \
  --query "SELECT Id, Name FROM pse__Practice__c WHERE Name = 'Professional Services'" \
  --target-org <alias>
```

#### Group (`pse__Group__c`)
Determined by the account's geography. Examples: CAN, ANZ, US East, US West, etc.
```bash
sf data query \
  --query "SELECT Id, Name FROM pse__Grp__c WHERE Name = '<group>'" \
  --target-org <alias>
```
If unsure which group to use, ask the user or look at other projects for the same account.

### Step 3 — Confirm with User

Before creating anything, present a summary table:

```
Project: FY25-26 Partner Oversight (DPP) - <Account Name>
Account: <Account Name> (<account_id>)
Parent:  <Parent Project Name> (<parent_id>)
PM:      <PM Name> (<pm_id>)
Region:  <Region Name>
Group:   <Group Name>
Dates:   <start> – <end>
Hours:   <N>
```

### Step 4 — Create the Project

```bash
sf data create record \
  --sobject pse__Proj__c \
  --values "Name='<project_name>' \
    pse__Account__c='<account_id>' \
    pse__Parent_Project__c='<parent_id>' \
    pse__Project_Manager__c='<pm_contact_id>' \
    pse__Stage__c='In Progress' \
    pse__Is_Active__c=true \
    pse__Billing_Type__c='BIF T&M' \
    pse__Project_Type__c='Customer Project' \
    pse__Region__c='<region_id>' \
    pse__Practice__c='<practice_id>' \
    pse__Group__c='<group_id>' \
    pse__Project_Status__c='Green' \
    pse__Time_Credited__c=true \
    Project_Funding__c='Internal' \
    SOW_Start_Date__c='<YYYY-MM-DD>' \
    SOW_End_Date__c='<YYYY-MM-DD>' \
    pse__Start_Date__c='<YYYY-MM-DD>' \
    pse__End_Date__c='<YYYY-MM-DD>' \
    Operations_Notes__c='<initials> <YYYY-MM-DD>: <project_type> - <justification_summary>' \
    CurrencyIsoCode='USD'" \
  --target-org <alias>
```

Capture the returned record ID from the response.

### Step 5 — Create the Budget

```bash
sf data create record \
  --sobject pse__Budget__c \
  --values "Name='<hours> Hours' \
    pse__Project__c='<new_project_id>' \
    pse__Amount__c=<hours> \
    pse__Type__c='Customer Purchase Order' \
    pse__Status__c='Approved' \
    pse__Approved__c=true \
    pse__Billable__c=false \
    pse__Include_In_Financials__c=true" \
  --target-org <alias>
```

### Step 6 — Verify

Re-query the project and budget to confirm they were created correctly:
```bash
sf data query \
  --query "SELECT Id, Name, pse__Stage__c, pse__Project_Status__c, pse__Practice__c, pse__Group__c, pse__Time_Credited__c, SOW_Start_Date__c, SOW_End_Date__c FROM pse__Proj__c WHERE Id = '<new_project_id>'" \
  --target-org <alias>
```

### Step 7 — Post Back to Slack

If the request came from Slack, post the project link back in the thread:
```
slack_write_api_call("chat.postMessage", {
  "channel": "C08LT7HPE4T",
  "thread_ts": "<original_thread_ts>",
  "text": "Project created:\n\n*<project_name>*\nhttps://databricks.lightning.force.com/lightning/r/pse__Proj__c/<new_project_id>/view\n\n• <hours> hours budgeted\n• Dates: <start> – <end>\n• PM: <pm_name>\n• Region: <region>\n• Status: Green / In Progress"
})
```

## Field Reference

### Project Fields (`pse__Proj__c`)

| Field | API Name | Source | Notes |
|-------|----------|--------|-------|
| Name | `Name` | Constructed | See naming patterns above |
| Account | `pse__Account__c` | Lookup | Search by account name |
| Parent Project | `pse__Parent_Project__c` | Lookup | Search for active MASTER project |
| Project Manager | `pse__Project_Manager__c` | Lookup | Contact object, search by name |
| Stage | `pse__Stage__c` | Default | "In Progress" |
| Active | `pse__Is_Active__c` | Default | true |
| Billing Type | `pse__Billing_Type__c` | Default | "BIF T&M" |
| Project Type | `pse__Project_Type__c` | Default | "Customer Project" |
| Region | `pse__Region__c` | Lookup | Search by name (AMER, APJ, EMEA) |
| Practice | `pse__Practice__c` | Lookup | Always "Professional Services" |
| Group | `pse__Group__c` | Lookup | By account geography (CAN, ANZ, etc.) |
| Project Status | `pse__Project_Status__c` | Default | "Green" |
| Time Credited | `pse__Time_Credited__c` | Default | true for DPP oversight and presales |
| Funding | `Project_Funding__c` | Default | "Internal" |
| SOW Start | `SOW_Start_Date__c` | Request | YYYY-MM-DD format |
| SOW End | `SOW_End_Date__c` | Request | YYYY-MM-DD format |
| Start Date | `pse__Start_Date__c` | Request | Same as SOW start |
| End Date | `pse__End_Date__c` | Request | Same as SOW end |
| Notes | `Operations_Notes__c` | Constructed | `<initials> <date>: <type> - <summary>` |
| Currency | `CurrencyIsoCode` | Default | "USD" (adjust for non-US accounts) |

### Budget Fields (`pse__Budget__c`)

| Field | API Name | Source | Notes |
|-------|----------|--------|-------|
| Name | `Name` | Constructed | e.g. "96 Hours" |
| Project | `pse__Project__c` | Created project ID | Link to parent project |
| Amount | `pse__Amount__c` | Request | Total hours |
| Type | `pse__Type__c` | Default | "Customer Purchase Order" |
| Status | `pse__Status__c` | Default | "Approved" |
| Approved | `pse__Approved__c` | Default | true |
| Billable | `pse__Billable__c` | Default | false |
| Include In Financials | `pse__Include_In_Financials__c` | Default | true |

## Important Notes

- **Do not** use `--use-tooling-api` flag.
- **Never hardcode IDs** — always resolve by name lookup.
- **Always confirm** the full project details with the user before creating.
- SOW dates and project dates should match unless the user specifies otherwise.
- The Salesforce link format is: `https://databricks.lightning.force.com/lightning/r/pse__Proj__c/<id>/view`
- Logfood data syncs daily — use the Salesforce API for verification after creating records.
- If a similar project exists for the same account, use it as a template for field values (especially Group and Region).
