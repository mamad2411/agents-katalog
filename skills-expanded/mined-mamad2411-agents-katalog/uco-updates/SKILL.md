---
name: uco-updates
description: Update Use Case Objects (UCOs) with status updates
user-invocable: true
---

# UCO Updates Skill

Update Use Case Objects (UCOs) with status updates. UCOs should be reviewed regularly and updated with any changes for UCOs in U1+.

**Reference Doc**: [UCO Management Guidelines](https://docs.google.com/document/d/1cLx2xjQ8YqdxvJeFRIi3Z20xPgnaD-Mu_RNEKdzT8oM)

## Optional Setup (Recommended)

For best results, the following are recommended but not required:

1. **MCP Authentication** (Optional for automated workflow): Set up authentication for:
   - Gmail (for searching customer emails)
   - Salesforce (for querying and updating UCOs)
   - Google Drive (for accessing meeting transcripts)

   Use `/validate-mcp-access` to verify all connections are working.

2. **Salesforce Account Alignment**: Your accounts must be correctly aligned in Salesforce:
   - Set as **Account Owner** (`Account.OwnerId`), OR
   - Set as **Last SA Engaged** (`Account.Last_SA_Engaged__c`)

   If UCOs are not appearing, verify these fields are set correctly for your accounts.

3. **Meeting Transcript Folder** (Optional, but highly recommended):
   - Configure `ae_transcript_folder_id` in `~/.vibe/profile` with your AE's Gemini recordings folder ID
   - Enables automatic UCO update generation from meeting transcripts
   - To get folder ID: Ask your AE for their folder → Extract from URL: `https://drive.google.com/drive/folders/{FOLDER_ID}`
   - Add to profile:
     ```yaml
     salesforce:
       ae_transcript_folder_id: <FOLDER_ID>
     ```

## Instructions

**IMPORTANT**: Use the field-data-analyst subagent to execute commands and summarize results

**IMPORTANT: Always use `--target-org` on every `sf` CLI command** to avoid `NoDefaultEnvError`. Resolve the org username once at the start of the session and reuse it:
```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
```
Then append `--target-org "$SF_TARGET_ORG"` to every `sf data query`, `sf data update record`, `sf data create record`, and `sf data get record` command. The examples below may omit this flag for brevity, but you **MUST** always include it.

1. **Note**: If Salesforce queries fail due to authentication, use `/salesforce-authentication` to set up access
2. **Check user preferences** for Next Steps format (see below)
3. **Automatically discover your UCOs** using Step 0 (filters by your assignments and accounts)
4. Identify specific UCO to update from the discovered list
5. Review current UCO state
6. Update required fields per the guidelines below
7. Verify updates were applied

---

## User Preferences

Check `~/.vibe/profile` for the `next_steps_format` preference:

```bash
if [ -f ~/.vibe/profile ]; then
  grep -A2 "salesforce:" ~/.vibe/profile | grep "next_steps_format" | awk '{print $2}'
fi
```

### Next Steps Format

**short** (default) - Concise, single-line updates:
```
Jan-05 - BK - Meeting with customer Monday to review architecture
```

**verbose** - Structured, multi-line updates:
```
YYYY-MM-DD - [Initials]:
Status: [green|yellow|red] - [brief status summary, is it on track?]
Last step: [description of completed action with date]
Next step: [description of upcoming action with date] - Owner: [Name/Role]
Risk: [risk description and mitigation actions]

[... existing entries below ...]
```

If no preference is set, default to `short` format.

## Required Update Fields (U1+ UCOs)

| Field | API Field | Owner | Description |
|-------|-----------|-------|-------------|
| **Next Steps** | `Demand_Plan_Next_Steps__c` | AE | Progress updates |
| **Target Onboarding Date** | `Implementation_Start_Date__c` | AE | Date dev work begins & $DBU usage starts |
| **Target Live Date** | `Full_Production_Date__c` | AE | Date dev work completes & $DBU at steady state |
| **Use Case Health** | `Implementation_Status__c` | SA | Red/Yellow/Green confidence indicator |
| **Stage** | `Stages__c` | AE/SA | UCO lifecycle stage (U1-U6) |

## MEDDPIC Fields (Optional - Fill When Evidence Exists)

MEDDPIC qualification fields on `UseCase__c` help track deal qualification signals. These fields are **not required** for weekly updates, but the skill should **opportunistically extract MEDDPIC signals** from meeting transcripts and emails and recommend updates when clear evidence is found. **Do not guess or speculate** - only fill these in when you have concrete evidence from transcripts, emails, or conversations.

### Updateable MEDDPIC Fields

| MEDDPIC | Field | API Field | Type | Values / Notes |
|---------|-------|-----------|------|----------------|
| **M** - Metrics | Metrics | `Metrics__c` | multipicklist | Cost Reduction, Customer Experience, Data Pipeline Efficiency, Data Quality, Innovation Enablement, Other, Productivity Improvement, Revenue Growth, Scalability, Security & Compliance, Time to Market |
| **M** - Metrics Notes | Metrics Notes | `MetricsNotes__c` | textarea (32K) | Free text for specific KPIs, quantified business outcomes, and success criteria |
| **E** - Economic Buyer | Exec Sponsor | `Business_Exec_Sponsor__c` | reference (Contact) | Contact ID of the executive sponsor. Query Contacts to find the right ID. |
| **E** - Authority | AE Authority | `AEAuthority__c` | picklist | Influencer, Technical Decision Maker, Economic Decision Maker, Executive Sponsor, Practitioner, Unknown |
| **C** - Compelling Event | Compelling Event | `Compelling_event_Urgency__c` | textarea (255) | Free text describing the compelling event or urgency driving the deal (e.g., "Contract renewal in Q3", "Legacy system EOL in June") |

### Read-Only MEDDPIC Fields (Show for Context)

These fields are owned by SDR/BDR and should NOT be updated by the SA/AE. Display them for context when reviewing UCOs.

| MEDDPIC | API Field | Notes |
|---------|-----------|-------|
| **D** - Decision Process | `XDRDecisionProcess__c` | SDR/BDR owned - shows how decisions are made |
| **I** - Identified Pain | `XDRIdentifiedPainGain__c` | SDR/BDR owned - shows initial pain/gain identified |

### MEDDPIC Signal Sources

MEDDPIC signals can come from **multiple sources**, not just meeting transcripts. When reviewing a UCO, cross-reference these Salesforce data sources:

| Source | What to Look For | Query |
|--------|-----------------|-------|
| **Contacts on Account** | Exec/VP titles → Exec Sponsor, Authority | `SELECT Id, Name, Title FROM Contact WHERE AccountId = '<ACCOUNT_ID>' AND Title != null ORDER BY Title` |
| **Open Opportunities** | Close dates, amounts → Compelling Event | `SELECT Name, CloseDate, Amount, StageName FROM Opportunity WHERE AccountId = '<ACCOUNT_ID>' AND IsClosed = false` |
| **UCO Description** | Use case goals → Metrics | `Use_Case_Description__c` field on the UCO itself |
| **Implementation Notes** | Champions, process notes → Decision Process | `Implementation_Notes__c` field on the UCO |
| **Next Steps History** | Named contacts, timelines → Champion, Compelling Event | `Demand_Plan_Next_Steps__c` field (scan for names and dates) |
| **Other UCOs on Account** | Patterns (self-impl preference, team structure) | Query sibling UCOs for `Implementation_Notes__c` patterns |
| **XDR Fields (read-only)** | SDR/BDR context → informs Metrics, Pain | `XDRDecisionProcess__c`, `XDRIdentifiedPainGain__c` |
| **Meeting Transcripts** | Direct quotes → all MEDDPIC fields | Google Drive transcript folder |
| **Customer Emails** | Timelines, blockers, stakeholders | Gmail search by account domain |

### When to Update MEDDPIC Fields

- **Metrics**: When UCO description, transcripts, or emails reference specific KPIs, cost savings targets, or success criteria
- **Metrics Notes**: When you find quantified outcomes (e.g., "reduce ETL runtime by 50%", "save $2M annually") in any source
- **Exec Sponsor**: When Contacts show a VP/C-level with a relevant title, or transcripts/notes name a sponsor. Query: `SELECT Id, Name, Title FROM Contact WHERE AccountId = '<ACCOUNT_ID>' AND (Title LIKE '%VP%' OR Title LIKE '%Director%' OR Title LIKE '%Chief%' OR Title LIKE '%CTO%' OR Title LIKE '%CEO%' OR Title LIKE '%CFO%')`
- **Authority**: When Contact titles, transcript mentions, or Implementation Notes reveal someone's role in the buying process
- **Compelling Event**: When Opportunities show close/renewal dates, or UCO notes mention deadlines, contract expirations, or migration timelines

---

## Step 0: Discover Your UCOs (Default Behavior)

**This step should run automatically when the skill is invoked without a specific UCO target.**

### 0A: Get Current User Information

```bash
# Get current authenticated user email
sf org display --json | jq -r '.result.username'
```

### 0B: Find UCOs Assigned to You

Query for UCOs where you are assigned as Primary SA, Solution Architect, RSA, or DSA:

```bash
# Store user email
USER_EMAIL=$(sf org display --json | jq -r '.result.username')

# Find all UCOs assigned to you (Primary SA, SA, RSA, or DSA) in U1-U5 stages
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, \
  Account__r.Name, Solution_Architect__r.Name, Primary_Solution_Architect__r.Name, \
  rsa__r.Name, DSA__r.Name, \
  Implementation_Start_Date__c, Full_Production_Date__c, \
  Metrics__c, MetricsNotes__c, AEAuthority__c, \
  Business_Exec_Sponsor__c, Compelling_event_Urgency__c, \
  XDRDecisionProcess__c, XDRIdentifiedPainGain__c, \
  LastModifiedDate \
  FROM UseCase__c \
  WHERE (Primary_Solution_Architect__r.Email = '${USER_EMAIL}' \
    OR Solution_Architect__r.Email = '${USER_EMAIL}' \
    OR rsa__r.Email = '${USER_EMAIL}' \
    OR DSA__r.Email = '${USER_EMAIL}') \
  AND Active__c = true \
  AND Stages__c IN ('1-Validating','2-Scoping','3-Evaluating','4-Confirming','5-Onboarding') \
  ORDER BY Implementation_Status__c DESC, Stages__c, LastModifiedDate DESC" --json
```

### 0C: Find UCOs for Your Accounts (from vibe profile)

If the user has accounts configured in `~/.vibe/profile`, query UCOs for those accounts:

```bash
# Check if vibe profile exists and has accounts
if [ -f ~/.vibe/profile ]; then
  # Parse account SFDC IDs from profile (if configured)
  # This step requires the profile to have sfdc_account_id fields

  # Example query for a specific account
  sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, \
    Account__r.Name, Solution_Architect__r.Name, \
    Implementation_Start_Date__c, Full_Production_Date__c, \
    Metrics__c, MetricsNotes__c, AEAuthority__c, \
    Business_Exec_Sponsor__c, Compelling_event_Urgency__c, \
    XDRDecisionProcess__c, XDRIdentifiedPainGain__c \
    FROM UseCase__c \
    WHERE Account__c IN ('<ACCOUNT_ID_1>', '<ACCOUNT_ID_2>') \
    AND Active__c = true \
    AND Stages__c IN ('1-Validating','2-Scoping','3-Evaluating','4-Confirming','5-Onboarding') \
    ORDER BY Account__r.Name, Stages__c" --json
fi
```

### 0D: Present Summary

Use the field-data-analyst subagent to:
1. Execute the queries above
2. Summarize results in a clear table format showing:
   - UCO Name
   - Account
   - Stage
   - Health Status
   - Your Role (Primary SA/SA/RSA/DSA)
   - Target Dates
   - In Plan status
3. Group by:
   - **Priority 1**: Red/Yellow health status UCOs
   - **Priority 2**: By stage (U2, U3, U4, U5, U6)
4. Highlight:
   - UCOs with no health status set
   - UCOs with approaching target dates
   - UCOs not modified recently

**If no UCOs found**: Inform user they have no UCO assignments and offer to search by account name or UCO name instead.

---

## Step 1: Find a Specific UCO (Manual Search)

**Use these queries when you need to find a UCO not automatically discovered in Step 0.**

```bash
# Search by UCO name
sf data query --query "SELECT Id, Name, Stages__c, Account__r.Name \
  FROM UseCase__c WHERE Name LIKE '%<SEARCH_TERM>%' AND Active__c = true"

# List all active UCOs for an account
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c \
  FROM UseCase__c \
  WHERE Account__r.Name LIKE '%<ACCOUNT_NAME>%' \
  AND Active__c = true"

# List UCOs needing updates (U1-U5) for an account
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, \
  Demand_Plan_Next_Steps__c, Full_Production_Date__c \
  FROM UseCase__c \
  WHERE Account__c = '<ACCOUNT_ID>' \
  AND Stages__c IN ('1-Validating','2-Scoping','3-Evaluating','4-Confirming','5-Onboarding') \
  AND Active__c = true"
```

---

## Step 2: Review Current UCO State

```bash
# Get all update fields for a UCO (including MEDDPIC)
sf data query --query "SELECT Id, Name, Stages__c, Implementation_Status__c, \
  Demand_Plan_Next_Steps__c, Implementation_Start_Date__c, Full_Production_Date__c, \
  Metrics__c, MetricsNotes__c, AEAuthority__c, \
  Business_Exec_Sponsor__c, Business_Exec_Sponsor__r.Name, \
  Compelling_event_Urgency__c, \
  XDRDecisionProcess__c, XDRIdentifiedPainGain__c, \
  Account__r.Name FROM UseCase__c WHERE Id = '<UCO_ID>'"
```

---

## Step 3: Update Fields

### Next Steps (Demand_Plan_Next_Steps__c)

**Format**: `Mon-DD - INITIALS - Update text`

Updates are prepended to the top (newest first). Include links to relevant docs where applicable.

**Example entries**:
```
Jan-05 - BK - Meeting with customer on Monday to review architecture
Dec-11 - RZ - Block is still finalizing design. Doc: https://docs.google.com/document/d/xxx
Dec-04 - RZ - Beth working with Catalyst team on test plan
```

**To update**: First read the current value, then prepend your new entry:

```bash
# 1. Get current Next Steps
sf data query --query "SELECT Demand_Plan_Next_Steps__c FROM UseCase__c WHERE Id = '<UCO_ID>'" --json

# 2. Update with new entry prepended (replace <EXISTING> with current content)
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Demand_Plan_Next_Steps__c='Jan-05 - BK - <YOUR_UPDATE>\n<EXISTING_CONTENT>'"
```

---

### Target Onboarding Date (Implementation_Start_Date__c)

Date development work is expected to begin and $DBU usage starts driving from the UCO.

- Do NOT include usage from a Pilot or POC for this date
- Date should align with U5 Stage criteria

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Start_Date__c=2026-02-01"
```

---

### Target Live Date (Full_Production_Date__c)

Date development work is completed and $DBU usage has hit a steady state.

- Date should align with U6 Stage criteria
- If pushed out 30+ days, must include reasoning in Next Steps field

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Full_Production_Date__c=2026-03-15"
```

---

### Use Case Health (Implementation_Status__c)

Red, Yellow, or Green based on confidence the UCO will go live by Target Live Date.

| Status | Meaning |
|--------|---------|
| **Green** | On track to hit Target Live Date |
| **Yellow** | Some risk, but still achievable |
| **Red** | Significant risk or product blockers preventing progression |

**Note**: If product blockers exist, Health should be Red and AHAs must be linked for each unique blocker.

```bash
# Set to Green
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Status__c=Green"

# Set to Yellow
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Status__c=Yellow"

# Set to Red
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Status__c=Red"
```

---

### Stage (Stages__c)

Update the UCO lifecycle stage when criteria are met.

| Stage | Name | Definition | Clear Indicator |
|-------|------|------------|-----------------|
| **U2** | Scoping | Pain identified, willingness to address | Customer willing to engage with SA |
| **U3** | Evaluating | Customer agrees DB could be solution. Requires: (1) Success criteria, (2) Workspace deployed, (3) Hands-on | Pilot/POC started |
| **U4** | Confirming | Customer agrees DB is best solution | Tech Win from customer |
| **U5** | Onboarding | Starting to use DBUs for this UCO | UCO driving $DBUs outside Pilot/POC |
| **U6** | Live | Dev work completed, hitting MRR target | $DBU at steady state |

**Note**: If UCO has product blocker preventing progression, stage must remain in U2.

```bash
# Valid values: 1-Validating, 2-Scoping, 3-Evaluating, 4-Confirming, 5-Onboarding, 6-Live, Lost, Disqualified
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Stages__c=3-Evaluating"
```

---

### Metrics (Metrics__c) - MEDDPIC

Multipicklist of business metrics the customer is targeting. Select one or more values.

```bash
# Set single metric
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Metrics__c='Cost Reduction'"

# Set multiple metrics (semicolon-separated for multipicklist)
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Metrics__c='Cost Reduction;Data Pipeline Efficiency;Productivity Improvement'"
```

---

### Metrics Notes (MetricsNotes__c) - MEDDPIC

Free-text field for specific KPIs and quantified business outcomes.

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "MetricsNotes__c='Target: reduce ETL runtime by 50% and save \$2M annually in infrastructure costs. Success criteria: <500ms query latency for real-time dashboards.'"
```

---

### AE Authority (AEAuthority__c) - MEDDPIC

Categorizes the authority level of the primary contact.

| Value | Meaning |
|-------|---------|
| **Influencer** | Can influence but not approve budget |
| **Technical Decision Maker** | Makes technical decisions for the project |
| **Economic Decision Maker** | Controls budget allocation |
| **Executive Sponsor** | C-level or VP sponsoring the initiative |
| **Practitioner** | Hands-on user, no decision authority |
| **Unknown** | Authority not yet determined |

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "AEAuthority__c='Economic Decision Maker'"
```

---

### Executive Sponsor (Business_Exec_Sponsor__c) - MEDDPIC

Reference to a Contact record for the executive sponsor. You need the Contact ID.

```bash
# First, find the contact ID
sf data query --query "SELECT Id, Name, Title FROM Contact \
  WHERE AccountId = '<ACCOUNT_ID>' AND Name LIKE '%<EXEC_NAME>%'"

# Then set the exec sponsor
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Business_Exec_Sponsor__c=003XXXXXXXXXXXX"
```

---

### Compelling Event (Compelling_event_Urgency__c) - MEDDPIC

Short description (max 255 chars) of the compelling event or urgency driving the deal.

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Compelling_event_Urgency__c='Legacy Hadoop cluster EOL in June 2026. Must migrate all workloads before contract expires.'"
```

---

## Combined Update Example

Update multiple fields in a single command:

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Demand_Plan_Next_Steps__c='Jan-05 - BK - POC progressing well\n<EXISTING>' \
  Implementation_Status__c=Green \
  Implementation_Start_Date__c=2026-02-01 \
  Full_Production_Date__c=2026-03-15 \
  Stages__c=3-Evaluating"
```

### Combined Update with MEDDPIC Fields

```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Demand_Plan_Next_Steps__c='Jan-05 - BK - POC progressing well\n<EXISTING>' \
  Implementation_Status__c=Green \
  Metrics__c='Cost Reduction;Data Pipeline Efficiency' \
  MetricsNotes__c='Target: 50% reduction in ETL runtime' \
  AEAuthority__c='Economic Decision Maker' \
  Compelling_event_Urgency__c='Legacy system EOL June 2026'"
```

---

## Step 4: Verify Updates

```bash
# Confirm the updates were applied (including MEDDPIC fields)
sf data query --query "SELECT Name, Stages__c, Implementation_Status__c, \
  Implementation_Start_Date__c, Full_Production_Date__c, \
  Metrics__c, MetricsNotes__c, AEAuthority__c, \
  Business_Exec_Sponsor__r.Name, Compelling_event_Urgency__c \
  FROM UseCase__c WHERE Id = '<UCO_ID>'"
```

---

## Step 5: Hygiene Validation (Automatic)

After updating UCOs, automatically run these 6 validation checks on all active UCOs (U1-U5) for the account. Flag any issues found.

### Hygiene Rules

| # | Rule | Severity | Description |
|---|------|----------|-------------|
| 1 | **Missing dates at U1** | Info | Stage U1 with no onboarding or go-live dates set. Early stage — dates should be estimated soon. |
| 2 | **Past go-live on early stage** | Warning | Stage U1-U3 but go-live date is in the past. Either the stage needs advancing or the date needs updating. |
| 3 | **Future onboarding on late stage** | Warning | Stage U5 but onboarding date is in the future. If already onboarding, the date should be current or past. |
| 4 | **Date ordering** | Error | Go-live date is before onboarding date. Go-live should always be after onboarding. |
| 5 | **Missing products** | Warning | No products (Use_Case_Type__c) set. Products should be identified by U2. |
| 6 | **U5 missing onboarding date** | Error | Stage U5 (Onboarding) but no Implementation_Start_Date__c set. Cannot be onboarding without a start date. |

### Validation Query

Run this SOQL query to get all active UCOs for validation:

```bash
sf data query --query "SELECT Id, Name, Stages__c, Use_Case_Type__c, Implementation_Start_Date__c, Full_Production_Date__c FROM UseCase__c WHERE Account__r.Name = '{ACCOUNT_NAME}' AND Stages__c IN ('U1','U2','U3','U4','U5')" --target-org $SF_TARGET_ORG --json
```

### Validation Logic

For each UCO returned, check:

```
Rule 1: IF Stages__c = 'U1' AND (Implementation_Start_Date__c IS NULL AND Full_Production_Date__c IS NULL) → INFO
Rule 2: IF Stages__c IN ('U1','U2','U3') AND Full_Production_Date__c < TODAY → WARNING
Rule 3: IF Stages__c = 'U5' AND Implementation_Start_Date__c > TODAY → WARNING
Rule 4: IF Full_Production_Date__c IS NOT NULL AND Implementation_Start_Date__c IS NOT NULL AND Full_Production_Date__c < Implementation_Start_Date__c → ERROR
Rule 5: IF Use_Case_Type__c IS NULL OR Use_Case_Type__c = '' → WARNING
Rule 6: IF Stages__c = 'U5' AND Implementation_Start_Date__c IS NULL → ERROR
```

### Output Format

Present hygiene results as a table:

| UCO Name | Stage | Issue | Severity |
|----------|-------|-------|----------|
| Example UCO | U3 | Go-live date (2025-06-01) is in the past | Warning |
| Another UCO | U5 | No onboarding date set | Error |

If no issues found, report: "✓ All UCOs pass hygiene validation."

**Tip:** These checks can also be run standalone without updating UCOs — just run the validation query and apply the rules.

---

## Production Pilot vs POC

Both available when UCO moves to U3, but Production Pilot has benefits:

| Type | Environment | Data | Adoption |
|------|-------------|------|----------|
| **Production Pilot** | Production | Live customer data | Easier (already in prod) - shorter U5 |
| **POC** | Development | Dev data/architecture | Requires rebuild in prod - longer U5 |

---

## Quick Reference

| What to Update | API Field | Example Value |
|----------------|-----------|---------------|
| Next Steps | `Demand_Plan_Next_Steps__c` | `'Jan-05 - BK - Update text\n...'` |
| Target Onboarding | `Implementation_Start_Date__c` | `2026-02-01` |
| Target Live | `Full_Production_Date__c` | `2026-03-15` |
| Health | `Implementation_Status__c` | `Green`, `Yellow`, `Red` |
| Stage | `Stages__c` | `3-Evaluating` |
| **MEDDPIC** | | |
| Metrics | `Metrics__c` | `'Cost Reduction;Productivity Improvement'` |
| Metrics Notes | `MetricsNotes__c` | `'Reduce ETL runtime by 50%'` |
| Exec Sponsor | `Business_Exec_Sponsor__c` | `003XXXXXXXXXXXX` (Contact ID) |
| Authority | `AEAuthority__c` | `'Economic Decision Maker'` |
| Compelling Event | `Compelling_event_Urgency__c` | `'Legacy system EOL June 2026'` |
| Decision Process (read-only) | `XDRDecisionProcess__c` | SDR/BDR owned |
| Identified Pain (read-only) | `XDRIdentifiedPainGain__c` | SDR/BDR owned |
