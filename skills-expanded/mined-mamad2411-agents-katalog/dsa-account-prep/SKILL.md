---
name: dsa-account-prep
description: Prepare a comprehensive account brief before a DSA customer engagement. Gathers UCO pipeline, consumption data, blockers, recent activity, and team context from Salesforce and Logfood. Use when a DSA says account prep, customer prep, engagement prep, meeting prep, account brief, DSA prep.
user-invocable: true
---

# DSA Account Prep

Prepare a comprehensive account brief before a DSA customer engagement. Gathers UCO pipeline, consumption data, blockers, recent activity, and team context from Salesforce and Logfood.

## Prerequisites

Before running this skill, ensure the following are authenticated:
1. **Salesforce** -- Run `/salesforce-authentication`
2. **Logfood** -- Run `databricks auth login https://adb-2548836972759138.18.azuredatabricks.net/ --profile=logfood`

## Required Information

The user must provide (or the skill will ask for):
1. **Account Name** -- The customer account to prepare for (e.g., "Acme Corp")

Optional:
- **Meeting context** -- What type of engagement (kickoff, weekly sync, executive review, technical deep-dive)
- **Output format** -- Console (default) or Google Doc

## Query Reference

All SQL and SOQL templates used by this skill are documented in:
- `resources/DSA_QUERIES.md` -- Shared query library for all fe-dsa skills

The output template is documented in:
- `resources/ACCOUNT_PREP_TEMPLATE.md` -- Markdown template for the account brief

---

## Step 0: Discover DSA Identity

**This step runs automatically at the start of every invocation.**

**IMPORTANT: Always use `--target-org` on every `sf` CLI command.**

### 0A: Resolve Salesforce Org and User

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
USER_EMAIL="$SF_TARGET_ORG"
```

### 0B: Get Salesforce User ID

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Email FROM User WHERE Email = '${USER_EMAIL}'" --json
```

Store the `User.Id` as `DSA_USER_ID` and `User.Name` as `DSA_NAME`.

### 0C: Verify DSA Assignment on Target Account

```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Account.Name, Account.Id, TeamMemberRole \
   FROM AccountTeamMember \
   WHERE UserId = '<DSA_USER_ID>' \
   AND TeamMemberRole = 'DSA' \
   AND Account.Name LIKE '%<ACCOUNT_NAME>%'" --json
```

If no result, fall back to querying UCOs where `DSA__r.Email = '${USER_EMAIL}'` and filter by account name. Store the `Account.Id` as `ACCOUNT_ID`.

---

## Step 1: Parallel Data Gathering

**Use the `field-data-analyst` subagent or `account-researcher` agent to execute queries in parallel.** Load skills first:

```
/salesforce-actions
/logfood-querier
```

### Salesforce Queries (all require --target-org "$SF_TARGET_ORG")

Execute these in parallel:

**1A: Account Overview**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Industry, BillingCity, BillingState, \
    NumberOfEmployees, Type, AccountTier__c \
   FROM Account WHERE Id = '<ACCOUNT_ID>'" --json
```

**1B: UCO Pipeline**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Stages__c, Implementation_Status__c, \
    Account__r.Name, DSA__r.Name, \
    Primary_Solution_Architect__r.Name, Solution_Architect__r.Name, \
    Implementation_Start_Date__c, Full_Production_Date__c, \
    Demand_Plan_Next_Steps__c, Use_Case_Description__c, \
    Metrics__c, MetricsNotes__c, \
    AEAuthority__c, Compelling_event_Urgency__c, \
    Business_Exec_Sponsor__r.Name, \
    LastModifiedDate \
  FROM UseCase__c \
  WHERE Account__c = '<ACCOUNT_ID>' \
  AND Active__c = true \
  ORDER BY Implementation_Status__c DESC, Stages__c" --json
```

**1C: Account Team**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT User.Name, User.Email, TeamMemberRole \
   FROM AccountTeamMember \
   WHERE AccountId = '<ACCOUNT_ID>' \
   ORDER BY TeamMemberRole" --json
```

**1D: Key Contacts**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Name, Title, Email, Phone \
   FROM Contact \
   WHERE AccountId = '<ACCOUNT_ID>' AND Title != null \
   ORDER BY Title" --json
```

**1E: Active Blockers**
```bash
sf data query --target-org "$SF_TARGET_ORG" --query \
  "SELECT Id, Name, Status__c, Priority__c, Jira_Ticket_Number__c, \
    UseCase__r.Name, CreatedDate \
   FROM Blocker__c \
   WHERE UseCase__r.Account__c = '<ACCOUNT_ID>' \
   AND Status__c != 'Resolved' \
   ORDER BY Priority__c, CreatedDate DESC" --json
```

### Logfood Queries (all require --profile=logfood)

Execute these in parallel (see `resources/DSA_QUERIES.md` for full SQL):

**1F: DSA Assignment Details**
- Query `main.field_dsa.dsa_project_assignment_outcomes` with EXPLODE pattern
- Filter by DSA name AND account name
- Returns: subscription_hours_weekly, fte_req, assignment_status_custom, dsa_engagement_type, start_fq, end_fq, cost_center

**1G: Monthly Consumption (Last 6 Months)**
- Query `main.fin_live_gold.paid_usage_metering`
- Filter by `sfdc_account_name` and `date >= DATE_ADD(CURRENT_DATE(), -180)` (no processDate column — this table is not snapshot-based)
- Group by month and `sku` (see DSA_QUERIES.md Section 6)

**1H: DSA Bandwidth**
- Query `main.field_dsa.dsa_bandwidth_table`
- Returns: assigned_bandwidth (FTE), capacity_flag

---

## Step 2: DSA Context Enrichment

Using the assignment data from Step 1F, calculate:

### Assignment Classification

| Field | How to Derive |
|-------|--------------|
| DSA Tier | Platinum (>=32h/wk, 1.0 FTE), Gold (>=16h/wk, 0.5 FTE), Silver (<16h/wk, 0.25 FTE) |
| Engagement Type | From `dsa_engagement_type` field (e.g., Implementation, Advisory, Optimization) |
| Assignment Duration | `assignment_start_date` to `assignment_end_date` |
| Fiscal Quarter Range | `start_fq` to `end_fq` |
| Remaining Weeks | Calculate from today to `assignment_end_date` |

### UCO Summary Metrics

| Metric | How to Calculate |
|--------|-----------------|
| Total Active UCOs | Count of UCOs in U1-U5 |
| Pipeline ARR | SUM(estimated_quarterly_dbus) * 4 for U1-U4 UCOs |
| Production ARR | SUM(estimated_quarterly_dbus) * 4 for U5-U6 UCOs |
| Avg Days in Stage | AVG(days_in_stage) across active UCOs |
| Stale UCOs | UCOs with days_in_stage > 30 |

---

## Step 3: Synthesize Account Brief

Build the account brief using the template in `resources/ACCOUNT_PREP_TEMPLATE.md`.

### Synthesis Rules

1. **Account Snapshot** -- Combine SF account data with Logfood consumption to show MRR
2. **UCO Portfolio** -- Group UCOs by stage, highlight Red/Yellow health, flag approaching target dates
3. **Consumption Highlights** -- Show 6-month trend, MoM growth rate, top SKUs
4. **Active Blockers** -- List by priority, include JIRA ticket links where available
5. **Key Contacts** -- Merge internal team (AccountTeamMember) with customer contacts (Contact)
6. **Recommended Talking Points** -- Generate 3-5 talking points based on:
   - Any Red/Yellow health UCOs (ask about blockers)
   - Consumption trend (celebrate growth or investigate decline)
   - Upcoming target dates (check readiness)
   - New UCOs in early stages (understand requirements)
   - Bandwidth alignment (ensure hours match workload)

### Priority Flags

Flag these items prominently:
- **RED UCO HEALTH** -- Any UCO with `Implementation_Status__c = 'Red'`
- **PAST DUE** -- Any UCO where `Full_Production_Date__c < TODAY`
- **STALE** -- Any UCO not modified in 14+ days with no recent Next Steps entry
- **DECLINING CONSUMPTION** -- MoM consumption drop > 10%
- **ENDING SOON** -- Assignment end date within 30 days

---

## Step 4: Output

### Console Output (Default)

Render the account brief directly in the terminal using the template format. Use markdown tables and clear section headers.

### Google Doc Output (Optional)

If the user requests a Google Doc:

1. Save the markdown brief to a temp file:
```bash
cat > /tmp/dsa_account_prep.md << 'CONTENT'
[Account brief markdown content]
CONTENT
```

2. Convert to Google Doc using the markdown converter:
```bash
python3 ~/.claude/plugins/cache/fe-vibe/fe-google-tools/*/skills/google-docs/resources/markdown_to_gdocs.py \
  --input /tmp/dsa_account_prep.md \
  --title "<ACCOUNT_NAME> - DSA Account Prep Brief"
```

3. Post-process for status colors (Green/Yellow/Red) using the Google Docs API pattern from the `fe-account-transition` skill.

Return the Google Doc URL to the user.

---

## Example Invocations

| Prompt | What Happens |
|--------|-------------|
| "Prep me for my Acme Corp meeting" | Full account brief for Acme Corp |
| "Account prep for Block" | Full account brief for Block |
| "DSA prep for Netflix, output as Google Doc" | Account brief saved to Google Doc |
| "Quick prep for my engagement with Stripe" | Account brief with focus on recent activity |
| "Meeting prep for Capital One executive review" | Account brief with executive-level framing |

---

## Related Skills

| Skill | When to Use |
|-------|------------|
| `/uco-updates` | After the meeting -- update UCO Next Steps and health |
| `/dsa-status-update` | Generate your weekly DSA status covering all accounts |
| `/dsa-weekly-report` | Comprehensive weekly activity report |
| `/dsa-handoff` | Transitioning the account to a new DSA |
| `/logfood-querier` | Ad-hoc Logfood queries for deeper analysis |
| `/salesforce-actions` | Direct Salesforce reads and writes |

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| "NoDefaultEnvError" on sf commands | Always use `--target-org "$SF_TARGET_ORG"` |
| No UCOs found for your email | Verify you are set as DSA on the UCO (`DSA__c` field) or on the AccountTeamMember |
| Logfood query returns empty | Check `--profile=logfood` is authenticated; run `databricks auth login` |
| Account name mismatch | Try partial match with `LIKE '%name%'`; Logfood and SF may use different casing |
| Consumption data missing | Use `date` range filter (e.g., `date >= DATE_ADD(CURRENT_DATE(), -180)`); this table has no `processDate` column |
