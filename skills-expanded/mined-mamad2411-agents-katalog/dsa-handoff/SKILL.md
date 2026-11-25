---
name: dsa-handoff
description: Generate a comprehensive DSA account handoff document when transitioning an account to a new DSA. Gathers complete account context, UCO pipeline, consumption analysis, stakeholder map, and engagement history. Use when a DSA says DSA handoff, account handoff, DSA transition, DSA reassignment, hand off account.
user-invocable: true
---

# DSA Account Handoff

Generate a comprehensive DSA account handoff document when transitioning an account to a new DSA. This skill gathers complete account context, UCO pipeline, consumption analysis, stakeholder map, and engagement history into a structured document that ensures a smooth transition.

**This skill is read-only. It queries Salesforce and Logfood but never writes or updates any records.**

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** -- Run `/salesforce-authentication`
2. **Logfood** -- Run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`
3. **Google** -- Run `/google-auth` (required for Google Doc output)

## Required Information

Ask the user for:
1. **Account Name** -- The customer account being transitioned
2. **Incoming DSA** -- Name and/or email of the new DSA taking over

Optional:
- **Handoff date** -- When the transition takes effect (default: today)
- **Additional context** -- Any notes the outgoing DSA wants to include

## Query Reference

All SQL and SOQL templates used by this skill are documented in:
- `fe-dsa:dsa-account-prep` skill -> `resources/DSA_QUERIES.md`

The output template is documented in:
- `resources/HANDOFF_DOC_TEMPLATE.md`

---

## Step 0: Discover Outgoing DSA Identity

**IMPORTANT: Always use `--target-org` on every `sf` CLI command.**

### 0A: Resolve Salesforce Org and User

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
USER_EMAIL="$SF_TARGET_ORG"
```

### 0B: Get Outgoing DSA Info

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Email FROM User WHERE Email = '${USER_EMAIL}'" --json
```

### 0C: Resolve Account ID

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name FROM Account WHERE Name LIKE '%<ACCOUNT_NAME>%' LIMIT 5" --json
```

Confirm the correct account with the user if multiple matches. Store `Account.Id` as `ACCOUNT_ID`.

### 0D: Resolve Incoming DSA

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Email FROM User WHERE Name LIKE '%<INCOMING_DSA_NAME>%' \
   OR Email LIKE '%<INCOMING_DSA_EMAIL>%' LIMIT 5" --json
```

---

## Step 1: Parallel Data Gathering (3 Agent Streams)

Use the `field-data-analyst` subagent or `account-researcher` agent to execute queries in parallel across three data streams.

### Stream A: Salesforce Data

**A1: Account Overview**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Industry, BillingCity, BillingState, BillingCountry, \
    NumberOfEmployees, Type, AccountTier__c, Website, Description \
   FROM Account WHERE Id = '<ACCOUNT_ID>'" --json
```

**A2: Full UCO Pipeline (All Stages)**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Stages__c, Implementation_Status__c, \
    Account__r.Name, DSA__r.Name, DSA__r.Email, \
    Primary_Solution_Architect__r.Name, Primary_Solution_Architect__r.Email, \
    Solution_Architect__r.Name, Solution_Architect__r.Email, \
    Implementation_Start_Date__c, Full_Production_Date__c, \
    Demand_Plan_Next_Steps__c, Use_Case_Description__c, \
    Use_Case_Product__c, \
    Metrics__c, MetricsNotes__c, \
    AEAuthority__c, Compelling_event_Urgency__c, \
    Business_Exec_Sponsor__r.Name, \
    XDRDecisionProcess__c, XDRIdentifiedPainGain__c, \
    Implementation_Notes__c, \
    CreatedDate, LastModifiedDate \
  FROM UseCase__c \
  WHERE Account__c = '<ACCOUNT_ID>' \
  ORDER BY Stages__c DESC, LastModifiedDate DESC" --json
```

**A3: Account Team (Internal)**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT User.Name, User.Email, TeamMemberRole \
   FROM AccountTeamMember \
   WHERE AccountId = '<ACCOUNT_ID>' \
   ORDER BY TeamMemberRole" --json
```

**A4: Customer Contacts**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Name, Title, Email, Phone, Department \
   FROM Contact \
   WHERE AccountId = '<ACCOUNT_ID>' AND Title != null \
   ORDER BY Title" --json
```

**A5: Active Blockers**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Status__c, Priority__c, Jira_Ticket_Number__c, \
    UseCase__r.Name, Description__c, CreatedDate \
   FROM Blocker__c \
   WHERE UseCase__r.Account__c = '<ACCOUNT_ID>' \
   ORDER BY Status__c, Priority__c, CreatedDate DESC" --json
```

**A6: Open Opportunities**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Name, StageName, Amount, CloseDate, Type \
   FROM Opportunity \
   WHERE AccountId = '<ACCOUNT_ID>' \
   AND IsClosed = false \
   ORDER BY CloseDate" --json
```

### Stream B: Logfood Data

**B1: DSA Assignment History**

Query ALL assignments (current, upcoming, and past) to show full engagement history:

```sql
WITH expanded AS (
  SELECT
    account_name,
    business_unit,
    sales_subregion_level_1,
    EXPLODE(project_assignments) AS pa
  FROM main.field_dsa.dsa_project_assignment_outcomes
)
SELECT DISTINCT
  account_name,
  pa.project_name,
  pa.assignment_resource_user_name,
  pa.assignment_resource_manager,
  CAST(pa.assignment_start_date AS STRING) AS assignment_start_date,
  CAST(pa.assignment_end_date   AS STRING) AS assignment_end_date,
  pa.assignment_status_custom,
  pa.dsa_engagement_type,
  COALESCE(CAST(pa.subscription_hours_weekly AS DOUBLE), 0) AS subscription_hours_weekly,
  COALESCE(CAST(pa.fte_req AS DOUBLE), 0) AS fte_req,
  pa.start_fq,
  pa.end_fq,
  pa.cost_center,
  business_unit,
  sales_subregion_level_1
FROM expanded
WHERE LOWER(account_name) LIKE '%<ACCOUNT_NAME>%'
ORDER BY assignment_start_date DESC
```

**B2: Monthly Consumption (Last 12 Months)**

```sql
SELECT
  DATE_TRUNC('month', date) AS usage_month,
  sku,
  SUM(usage_dollars_at_list) AS list_dollars,
  SUM(usage_dollars) AS net_dollars
FROM main.fin_live_gold.paid_usage_metering
WHERE LOWER(sfdc_account_name) LIKE '%<ACCOUNT_NAME>%'
  AND date >= DATE_ADD(CURRENT_DATE(), -365)
GROUP BY usage_month, sku
ORDER BY usage_month DESC, list_dollars DESC
```

**B3: Consumption Summary (Current MRR)**

```sql
SELECT
  SUM(usage_dollars_at_list) / 3 AS avg_monthly_list_dollars,
  SUM(usage_dollars) / 3 AS avg_monthly_net_dollars
FROM main.fin_live_gold.paid_usage_metering
WHERE LOWER(sfdc_account_name) LIKE '%<ACCOUNT_NAME>%'
  AND date >= DATE_ADD(CURRENT_DATE(), -90)
```

**B4: Top SKUs**

```sql
SELECT
  sku,
  SUM(usage_dollars_at_list) AS total_list_dollars,
  ROUND(SUM(usage_dollars_at_list) * 100.0 / SUM(SUM(usage_dollars_at_list)) OVER (), 1) AS pct_of_total
FROM main.fin_live_gold.paid_usage_metering
WHERE LOWER(sfdc_account_name) LIKE '%<ACCOUNT_NAME>%'
  AND date >= DATE_ADD(CURRENT_DATE(), -90)
GROUP BY sku
ORDER BY total_list_dollars DESC
LIMIT 10
```

**B5: DSA Bandwidth for Incoming DSA**

```sql
SELECT
  dsa,
  capacity_flag,
  CAST(
    regexp_extract(bandwidth_bar_html, '(\\d+\\.\\d+)', 1)
    AS DECIMAL(10,3)
  ) AS assigned_bandwidth
FROM main.field_dsa.dsa_bandwidth_table
WHERE LOWER(dsa) LIKE '%<INCOMING_DSA_NAME>%'
```

**B6: UCO Pipeline from Logfood (with ARR)**

Query `main.gtm_gold.rpt_use_case_pipeline_monthly` for the account (see DSA_QUERIES.md Section 4). This provides estimated_quarterly_dbus for ARR calculations.

### Stream C: Contextual Data (Optional)

If Glean and Slack MCP tools are available:

**C1: Glean Document Search**
Search for account-related documents (architecture docs, strategy decks, meeting notes).

**C2: Slack Channel Discovery**
Search for relevant Slack channels:
- `#ext-<account-name>` (external/customer-facing)
- `#acct-<account-name>` (internal)

---

## Step 2: DSA Engagement History

Using the assignment data from Step 1 (Stream B1), build a chronological engagement history:

### Timeline

| Period | DSA | Engagement Type | Hours/wk | FTE | Status |
|--------|-----|-----------------|----------|-----|--------|
| <START_FQ> - <END_FQ> | <DSA_NAME> | <TYPE> | <HOURS> | <FTE> | <STATUS> |

### Engagement Summary

For the outgoing DSA's tenure, calculate:
- **Total engagement duration** -- weeks from first assignment_start_date to today
- **Average weekly hours** -- mean of subscription_hours_weekly across assignments
- **Total FTE invested** -- sum of fte_req * duration
- **Engagement type history** -- list of engagement types (Implementation, Advisory, etc.)
- **FTE changes** -- any changes in allocated hours over time

### Cost Center and Business Unit

Document the cost center and business unit for proper resource tracking in the transition.

---

## Step 3: Build Handoff Document

Assemble the comprehensive handoff document using the template in `resources/HANDOFF_DOC_TEMPLATE.md`.

### Section-by-Section Assembly

**3A: Executive Summary**
- 2-3 paragraph overview of the account relationship
- Current state (MRR, UCO pipeline health, consumption trajectory)
- Key priorities for the incoming DSA
- Critical context the incoming DSA must know immediately

**3B: Account Overview**
- Company profile (industry, size, location)
- Account tier and strategic importance
- Key metrics (MRR, growth rate, UCO counts)

**3C: Databricks Team Contacts**
- AE, SA, CSM, outgoing DSA, incoming DSA
- Use @mentions for person chip formatting in Google Docs

**3D: Customer Stakeholders**
- Key customer contacts with roles and relationship context
- Technical champions, executive sponsors, decision makers
- Relationship quality notes (who to build rapport with first)

**3E: DSA Engagement Context**
- Full assignment history timeline
- Current engagement type and hours
- What worked well and what to watch out for
- Customer communication preferences and meeting cadence

**3F: UCO Portfolio**
Group by status:
- **Production (U6)** -- Stable use cases, any ongoing support needs
- **Active Pipeline (U1-U5)** -- Grouped by stage with health, target dates, next steps
- **Lost/Disqualified** -- Why they failed, lessons learned, re-engagement potential

For each UCO include:
- Name with Salesforce link
- Stage and health
- Product area
- Estimated quarterly DBUs (ARR = quarterly DBUs * 4)
- Target dates
- Last Next Steps entry
- Blocker count

**3G: Consumption Analysis**
- 12-month trend with monthly totals
- Top SKUs by spend
- Growth trajectory and key drivers
- Notable consumption events (spikes, drops, new SKU adoption)

**3H: In-Flight Deliverables**
- Architecture docs in progress
- POCs or pilots underway
- Pending customer deliverables
- Scheduled meetings or workshops

**3I: Known Issues and Blockers**
- Active blockers with JIRA links
- Engineering escalations (open and recently resolved)
- Product feature requests
- Technical debt or workarounds in place

**3J: 30/60/90 Day Priorities**

| Timeframe | Priority | Details |
|-----------|----------|---------|
| **30 Days** | Build relationships | Meet key stakeholders, establish meeting cadence |
| **30 Days** | Review all active UCOs | Understand current state, update Next Steps |
| **30 Days** | Address Red/Yellow UCOs | Prioritize health improvement |
| **60 Days** | Consumption optimization | Identify growth opportunities |
| **60 Days** | Blocker resolution | Drive open blockers to completion |
| **90 Days** | Strategic planning | Develop expansion strategy with AE |

**3K: Resources**
- Relevant Slack channels (external and internal)
- Key documents (architecture docs, strategy decks, meeting notes)
- Support instructions
- Workspace URLs and access details

---

## Step 4: Create Google Doc

### 4A: Save Markdown to Temp File

```bash
cat > /tmp/dsa_handoff_doc.md << 'CONTENT'
[Complete handoff document markdown]
CONTENT
```

### 4B: Convert to Google Doc

```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/dsa_handoff_doc.md \
  --title "<ACCOUNT_NAME> - DSA Handoff Document"
```

### 4C: Post-Process for Person Chips and Status Colors

Create a post-processing script to:

1. **Replace @mentions with person chips** -- Map Databricks team member names to email addresses and convert to interactive Google Docs person chips.

2. **Apply status colors** -- Color-code health indicators:
   - **Green** -> green text (rgb: 0, 0.5, 0)
   - **Yellow** -> amber text (rgb: 0.8, 0.6, 0)
   - **Red** -> red text (rgb: 0.8, 0, 0)

Use the post-processing pattern from the `fe-account-transition` skill:

```python
#!/usr/bin/env python3
"""Post-process handoff doc for person chips and status colors."""

import json
import subprocess
import urllib.request
import time

DOC_ID = "YOUR_DOC_ID"
QUOTA_PROJECT = "gcp-sandbox-field-eng"

MENTION_TO_EMAIL = {
    "@Outgoing DSA Name": "outgoing.dsa@databricks.com",
    "@Incoming DSA Name": "incoming.dsa@databricks.com",
    # Add AE, SA, CSM as discovered
}

STATUS_COLORS = {
    "**Green**": {"red": 0.0, "green": 0.5, "blue": 0.0},
    "**Yellow**": {"red": 0.8, "green": 0.6, "blue": 0.0},
    "**Red**": {"red": 0.8, "green": 0.0, "blue": 0.0},
}

# ... (use full implementation from fe-account-transition skill)
```

Save as `/tmp/fix_handoff_doc.py`, update DOC_ID and MENTION_TO_EMAIL, then run:

```bash
python3 /tmp/fix_handoff_doc.py
```

### 4D: Return Document URL

Present the Google Doc URL to the user:
```
Handoff document created: https://docs.google.com/document/d/<DOC_ID>/edit

Share this with @Incoming DSA Name and schedule a handoff meeting to walk through it.
```

---

## Example Invocations

| Prompt | What Happens |
|--------|-------------|
| "DSA handoff for Acme Corp to Jane Smith" | Full handoff doc for Acme Corp |
| "Hand off Block account to john.doe@databricks.com" | Handoff doc for Block |
| "Account transition for Netflix" | Asks for incoming DSA, then generates doc |
| "DSA reassignment handoff for Capital One to Pat Lee" | Full handoff doc |
| "Prepare handoff document for my Stripe account" | Asks for incoming DSA |

---

## Related Skills

| Skill | When to Use |
|-------|------------|
| `/dsa-account-prep` | Quick account brief (lighter than full handoff) |
| `/dsa-status-update` | Current status across all accounts |
| `/dsa-weekly-report` | Detailed weekly activity report |
| `/uco-updates` | Update UCO fields after handoff review |
| `/fe-account-transition` | Full account transition doc (AE/SA transitions, not DSA-specific) |

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Incoming DSA not found in Salesforce | Try searching by email or partial name; they may need a Salesforce user record |
| Assignment history incomplete | Logfood only tracks CURRENT ASSIGNED and UPCOMING by default; past assignments may be filtered out |
| Google Doc creation fails | Ensure `/google-auth` is complete; check quota project is `gcp-sandbox-field-eng` |
| Person chips not working | Verify email addresses are valid Databricks corporate emails |
| Consumption data gaps | Some accounts may use different name variations in Logfood vs Salesforce |
| No Slack channels found | Try alternate patterns: `ext-<short-name>`, `acct-<name>`, `#databricks<number>` |
