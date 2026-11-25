---
name: account-plan-populator
description: Auto-research and populate all content fields and child records on a Salesforce AccountPlan record. Pulls context from Salesforce UCOs/Opps/Contacts/Blockers, Logfood consumption, Gmail, Calendar, Slack, Drive, Web Search, and Glean. Populates text fields, Strategic Priorities, Partner Landscape, TAP Map (EB Champions), and Whitespace records with all picklist dropdowns configured. Writes approved values back to Salesforce via REST API.
user-invocable: true
---

# Account Plan Populator

This skill automatically researches a customer account across 8 data sources and populates the full Salesforce AccountPlan — text fields (Company Overview, SWOT, KPIs, etc.), Strategic Priority child records, Partner Landscape records, TAP Map / EB Champion records, and Whitespace By LOB records, including all picklist dropdown fields.

## Routing — When to Use This Skill

This skill should be triggered when the user says any of:
- "populate account plan", "fill out account plan", "complete account plan"
- "account plan for [account name]"
- "fill in the account plan"
- "prepare account plan for QBR/EBC"
- "research and populate [account] plan"
- "update account plan fields"
- `/account-plan-populator`

Do NOT trigger for:
- UCO next steps updates (use `/uco-next-steps` instead)
- TAP Map only (unless in context of full account plan)
- Whitespace analysis only

## Prerequisites

Before running, ensure the following are authenticated:
1. **Salesforce** - Run `/salesforce-authentication` if needed
2. **Google** - Run `/google-auth` if needed (for Gmail, Calendar, Drive)
3. **Slack** - MCP connection should be active (check with `/validate-mcp-access`)
4. **Databricks** - Logfood profile configured (`databricks auth profiles` should show `logfood`)

## How to Invoke

```
/account-plan-populator <Account Name or AccountPlan ID>
```

**Examples:**
- `/account-plan-populator Brookfield Renewable` — resolve by account name
- `/account-plan-populator 252Vp00000aXqcUIAS` — use a specific AccountPlan record ID

**Optional flags:**
- `--refresh` — overwrite all fields, even those with existing content
- `--sections swot,competitors,overview` — only populate specific sections

## What This Skill Does

1. **Resolves** the account and finds (or offers to create) the AccountPlan record
2. **Discovers** all active UCOs, Opportunities, Contacts, and Blockers from Salesforce
3. **Gathers signals** from 8 sources: Salesforce, Logfood, Gmail, Calendar, Slack, Drive, Web Search, Glean
4. **Synthesizes** research into all AccountPlan content fields and child records
5. **Presents** a review with confidence ratings (HIGH/MEDIUM/LOW) and source citations
6. **Writes** approved values to Salesforce via REST API after your confirmation

## What Gets Populated

### Text Fields on the AccountPlan (14 fields)

| # | API Name | Label | Format |
|---|----------|-------|--------|
| 1 | `CompanyIndustryOverview__c` | Company/Industry Overview | 2-3 paragraphs (uses all account context) |
| 2 | `AccountVision` | Account Vision | 2-4 bullet points |
| 3 | `AccountPrfmIndicators` | Performance Indicators (KPIs) | Quantitative bullet list |
| 4 | `AccountChallenges` | Account Challenges | Numbered list 3-5 items |
| 5 | `AccountCompetitiveStrengths` | Competitive Strengths | 3-5 bullets: why we win |
| 6 | `AccountCmptvWeaknesses` | Competitive Weaknesses | 3-5 bullets: honest gaps |
| 7 | `RelationshipStrengths` | Relationship Strengths | 3-5 bullets |
| 8 | `RelationshipWeaknesses` | Relationship Weaknesses | 3-5 bullets |
| 9 | `RelationshipOpportunities` | Relationship Opportunities | 3-5 bullets |
| 10 | `RelationshipThreats` | Relationship Threats | 3-5 bullets |
| 11 | `Current_State_Pains_Challenges_The_W__c` | Current State / Pains / Why | Narrative paragraph |
| 12 | `Data_AI_Strategy_Value_Roadmap_Exec__c` | Data & AI Strategy / Roadmap | Structured roadmap |
| 13 | `Strategic_Priorities_Long_Term_Data__c` | Long-Term Strategic Priorities | 3-5 bullets |
| 14 | `Notes` | Notes | Auto-generated source summary |

### Child Record Sections (on `AccountPlanRelated__c` and `StrategicPriority__c`)

| Section | SF Object / RecordType | What Gets Created | Key Rules |
|---------|----------------------|-------------------|-----------|
| **Strategic Priorities** | `StrategicPriority__c` | At least 3 priority records, linked to UCOs | Derived from UCOs, Drive docs, Slack/Gmail |
| **Industry Imperatives** | Text field + Glean research | Imperatives from Databricks industry outcomes | Search Glean for published outcomes by vertical |
| **Partner Landscape** | `AccountPlanRelated__c` (Partner Landscape) | All relevant partners with full field population | Review every partner, update `Account_Partner__c` engagement stages |
| **TAP Map / EB Champions** | `AccountPlanRelated__c` (EB Champion) | 8 records (one per category) with champions, TAM, DBx% | Use primary account champion(s) — same person on most tabs |
| **Whitespace By LOB** | `AccountPlanRelated__c` (Whitespace By LOB) | 9 records with ALL picklist dropdowns set | Must set `AIBI__c`, `DataEngineering__c`, etc. on every record |
| **Whitespace By BU+1** | `AccountPlanRelated__c` (Whitespace By BU+1) | 1 aggregate record | All dropdowns + aggregate TAM |

### Workload Category Dropdowns (MUST be set on every child record)

These picklist fields exist on all `AccountPlanRelated__c` records and must be configured:
`AIBI__c`, `AgentBricks__c`, `Collaboration__c`, `DataEngineering__c`, `DataFormatsAndLakehouseStorage__c`, `DataGovernance__c`, `DataWarehousing__c`, `Lakebase__c`

Values: `Live`, `Actively Pursuing`, `Potential` (always verify via describe)

## Section Completion Booleans

| Boolean Field | Set When |
|--------------|----------|
| `IsBusinessOverviewFilled__c` | `CompanyIndustryOverview__c` is populated |
| `IsStrategicPriorityCompleted__c` | `StrategicPriority__c` records created (at least 3) |
| `IsPartnerLandscapeFilled__c` | Partner Landscape records created |
| `IsTAPMAPFilled__c` | EB Champion records populated |
| `IsWhitespaceLobFilled__c` | Whitespace By LOB records populated |
| `IsWhitespaceBuPlusOne__c` | Whitespace By BU+1 record populated |

Not set by this skill: `IsMigrationPlanFilled__c`, `IsOrgChartLinkAdded__c`

## Quick Start

**Invoke the `account-plan-populator` agent** to handle the full workflow:

```
Task tool with subagent_type='fins-canada-tools:account-plan-populator' and model='opus'
```

Pass the user's full request (including account name/ID and any flags) directly to the agent. The agent handles all data gathering, synthesis, review, and Salesforce writes.

## Key Design Principles

1. **SWOT is Databricks-relationship-centric** — analyzes our position with this customer, NOT generic company SWOT
2. **Primary champions on TAP Map** — use the account's 1-2 primary champions across most tabs, not scattered contacts
3. **All picklist dropdowns must be set** — every `AccountPlanRelated__c` record needs the workload category fields configured
4. **Incumbent tools must be SFDC-recognized** — only use picklist values that exist in the system
5. **REST API v62.0** — use v62.0 (not v59.0) as the `Account_Plan__c` parent link is not visible in older versions

## Eval Tests

These tests verify the skill produces correct output. Run after populating an account plan.

### Test 1: Text Fields Written
```
sf data query --query "SELECT CompanyIndustryOverview__c, AccountVision, AccountPrfmIndicators,
  AccountChallenges, RelationshipStrengths, Notes FROM AccountPlan
  WHERE Id = '{PLAN_ID}'" --json --target-org "$SF_TARGET_ORG"
```
**Pass criteria:** All queried fields are non-null and contain substantive content (>50 chars each).

### Test 2: Strategic Priorities Created
```
sf data query --query "SELECT Id, Name, Strategic_Objective__c FROM StrategicPriority__c
  WHERE Account_Plan__c = '{PLAN_ID}'" --json --target-org "$SF_TARGET_ORG"
```
**Pass criteria:** At least 3 records returned, each with a non-null Name and Strategic_Objective__c.

### Test 3: Whitespace LOB Dropdowns Configured
```bash
curl -s "${SF_INSTANCE_URL}/services/data/v62.0/query?q=SELECT+Id,Category__c,AIBI__c,DataEngineering__c,DataWarehousing__c,DataGovernance__c,Lakebase__c,AgentBricks__c+FROM+AccountPlanRelated__c+WHERE+Account_Plan__c='{PLAN_ID}'+AND+RecordType.Name='Whitespace+By+LOB'" \
  -H "Authorization: Bearer ${SF_ACCESS_TOKEN}"
```
**Pass criteria:** 9 records returned. ALL picklist fields are non-null on every record. Values are one of: `Live`, `Actively Pursuing`, `Potential`.

### Test 4: EB Champions Have Primary Champion
```bash
curl -s "${SF_INSTANCE_URL}/services/data/v62.0/query?q=SELECT+Id,Category__c,RelatedContact__c,EstimatedTAM__c,EstimatedDatabricks__c+FROM+AccountPlanRelated__c+WHERE+Account_Plan__c='{PLAN_ID}'+AND+RecordType.Name='EB+Champion'" \
  -H "Authorization: Bearer ${SF_ACCESS_TOKEN}"
```
**Pass criteria:** 8 records returned. At least 6 of 8 have the SAME `RelatedContact__c` (primary champion). All have non-null `EstimatedTAM__c` and `EstimatedDatabricks__c`.

### Test 5: Partner Landscape Complete
```bash
curl -s "${SF_INSTANCE_URL}/services/data/v62.0/query?q=SELECT+Id,AccountPartner__c,Details__c,NextStepsActions__c+FROM+AccountPlanRelated__c+WHERE+Account_Plan__c='{PLAN_ID}'+AND+RecordType.Name='Partner+Landscape'" \
  -H "Authorization: Bearer ${SF_ACCESS_TOKEN}"
```
**Pass criteria:** At least 1 partner record. Each has non-null `AccountPartner__c`, `Details__c`.

### Test 6: Booleans Set
```
sf data query --query "SELECT IsBusinessOverviewFilled__c, IsStrategicPriorityCompleted__c,
  IsPartnerLandscapeFilled__c, IsTAPMAPFilled__c, IsWhitespaceLobFilled__c,
  IsWhitespaceBuPlusOne__c, Status FROM AccountPlan
  WHERE Id = '{PLAN_ID}'" --json --target-org "$SF_TARGET_ORG"
```
**Pass criteria:** All 6 booleans are `true`. Status is `Active`.

### Test 7: SWOT is Relationship-Centric
Read `RelationshipStrengths`, `RelationshipWeaknesses`, `RelationshipOpportunities`, `RelationshipThreats` from the AccountPlan.
**Pass criteria:** Content references Databricks engagement (champion names, meeting cadence, UCO progress, competitive position) — NOT generic company strengths/weaknesses.

## Output

The skill presents a confirmation review before writing anything:

```
## AccountPlan Review — [Account Name]

14 text fields + 5 child record sections. Sources: SF ✓ Logfood ✓ Gmail ✓ Calendar ✓ Slack ✓ Drive ✓ Web ✓ Glean ✓

| # | Field | Confidence | Sources | Preview |
|---|-------|-----------|---------|---------|
| 1 | Company Overview | HIGH | Web, Glean | Brookfield Renewable Partners... |
| 2 | Account Vision | MEDIUM | Web, Drive | - Expand global renewable... |
| ... | ... | ... | ... | ... |

Child Records:
- Strategic Priorities: 5 proposed
- Partners: 7 proposed
- EB Champions: 8 tabs (primary champion: Emily Cox)
- Whitespace LOB: 9 categories
- Whitespace BU+1: 1 aggregate

Reply with:
- `yes` — write all to Salesforce
- `no` — cancel
- `edit <field>` — revise a specific field
- `skip <field>` — exclude a field from the write
- `show <field>` — see the full proposed value
```

After approval, values are written to Salesforce via REST API in batches, with verification queries and a final summary.
