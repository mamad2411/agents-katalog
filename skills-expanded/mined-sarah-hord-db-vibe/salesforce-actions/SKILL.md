---
name: salesforce-actions
description: Read and update salesforce, including Use Cases (UCOs), Accounts, Opportunities, Blockers, ASQs/Specialist Requests, Preview Feature Requests. Manage UCO stages U1, U2 (Scoping), U3 (Evaluating), U4 (Confirming), U5 (Onboarding), U6 (Live).
---


# Salesforce Actions Skill

> **IMPORTANT:** For looking up or creating JIRA tickets (including ES tickets), use the `/jira-actions` skill instead if it is available. This skill is for Salesforce CRM operations only.
>
> **IMPORTANT:** For looking up Databricks employee organizational information (manager hierarchy, direct reports, business unit), use the `/databricks-org` skill instead if it is available. This skill is for Salesforce CRM data.

Read and update salesforce, including Use Cases, Accounts, Opportunities, Blockers, Escalation Requests, ASQs/Specialist Requests.

## Data Source Decision

**Choose the right data source based on your task:**

| Task Type | Use | Why |
|-----------|-----|-----|
| **Read/lookup** (single account, cases, UCOs) | **Logfood** | 2-10x faster with SQL |
| **Write/update** (modify records) | **Salesforce API** | Logfood is read-only |
| **Multi-table analysis** (territory queries, aggregations) | **Logfood** | SQL joins outperform SOQL |
| **Historical/lifecycle tracking** | **Logfood** | Daily snapshots track changes over time |
| **Just-updated records** (real-time) | **Salesforce API** | Logfood syncs daily |

**For Logfood queries:** See `resources/LOGFOOD_QUERIES.md` for table mappings, examples, and the **critical processDate filter**.

## Instructions
**IMPORTANT** Do not use the flag -use-tooling-api on any calls! **IMPORTANT**
**IMPORTANT** When using the field-data-analyst subagent, provide context about what data you need - it will determine the best approach (Logfood vs Salesforce API). **IMPORTANT**
**IMPORTANT: Always use `--target-org` on every `sf` CLI command** to avoid `NoDefaultEnvError`. Resolve the org username once at the start of the session and reuse it:
```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
```
Then append `--target-org "$SF_TARGET_ORG"` to every `sf data query`, `sf data update record`, `sf data create record`, and `sf data get record` command. The examples below may omit this flag for brevity, but you **MUST** always include it.
1) Ensure authenticated with salesforce (for API calls) or databricks (for Logfood queries)
2) To identify an account association, refer to resources/ACCOUNT_LOOKUP.md
3) For Logfood SQL queries, refer to resources/LOGFOOD_QUERIES.md
4) For object-specific operations, refer to the appropriate documentation:
   - **Use Cases**: resources/UseCase.md (for weekly UCO updates, use `/uco-updates` skill)
   - **Accounts**: resources/Account.md
   - **Opportunities**: resources/Opportunity.md
   - **Cases/Support Cases**: resources/Case.md
   - **Workspaces**: resources/Workspace.md
   - **Blockers**: resources/Blocker.md
   - **Aha Ideas**: resources/ahaapp__AhaIdea.md
   - **Escalation Requests/Support Escalations**: resources/Escalation_Request.md
   - **FP Approvals/Preview Feature Requests**: resources/FP_Approval.md
   - **ASQ/Specialist Requests/STS/Shared Technical Services**: resources/ApprovalRequest.md
   - **Users**: resources/User.md
   - **Logfood SQL Queries**: resources/LOGFOOD_QUERIES.md (for fast reads & historical analysis)
5) If you encounter unfamiliar acronyms or industry terminology in Salesforce records (e.g., DNB, FSI, PubSec), use the `internal-jargon` skill to look them up

## Efficient Segment-Based Query Pattern

When users ask questions about internal segments (e.g., "how many UCOs does DNB have?"), follow this streamlined workflow:

### Step 1: Resolve the Acronym (if needed)
If the segment is an acronym you don't recognize:
- Use `/internal-jargon` skill to look it up ONCE
- Example: "DNB" → "Digital Native Businesses"

### Step 2: Determine the Correct Field
Internal segments like DNB, FSI, PubSec can appear in different fields depending on context:

**Owner Role** (most common for sales segments):
- Field: `Owner.UserRole.Name`
- Used for: Sales territory/segment assignments
- Examples: "DNB Strat Core", "FSI Named", "PubSec Federal"
- Query pattern: Use `LIKE '%DNB%'` to match partial role names

**Vertical Fields** (for industry classification):
- Field: `Vertical_New__c` or `Databricks_Vertical_Map_New__c`
- Used for: Industry/market verticals
- Examples: "Enterprise Technology", "FinServ", "Public Sector"
- Query pattern: Use exact match with `= 'value'`

**Discovery approach**: If unsure which field to use, first query all unique values:
```bash
# See all Owner Roles and their account counts
sf data query --query "SELECT Owner.UserRole.Name, COUNT(Id) FROM Account WHERE Owner.UserRole.Name != null GROUP BY Owner.UserRole.Name ORDER BY COUNT(Id) DESC"

# Or check if a specific segment exists in Owner Role
sf data query --query "SELECT Owner.UserRole.Name, COUNT(Id) FROM Account WHERE Owner.UserRole.Name LIKE '%DNB%' GROUP BY Owner.UserRole.Name"
```

### Step 3: Query Accounts by the Appropriate Field
Once you know which field contains the segment:

**For Owner Role (sales segments like DNB, FSI):**
```bash
sf data query --query "SELECT Id, Name, Owner.UserRole.Name FROM Account WHERE Owner.UserRole.Name LIKE '%DNB%'"
```

**For Vertical (industry classification):**
```bash
sf data query --query "SELECT Id, Name, Vertical_New__c FROM Account WHERE Vertical_New__c = 'Enterprise Technology'"
```

### Step 4: Count UCOs Using Subquery
Use a single query with a subquery to count UCOs efficiently:
```bash
sf data query --query "SELECT COUNT(Id) FROM UseCase__c WHERE Account__c IN (SELECT Id FROM Account WHERE Owner.UserRole.Name LIKE '%DNB%') AND Stages__c IN ('U2', 'U3', 'U4', 'U5')"
```

### Complete Example: "How many UCOs does DNB have?"

```bash
# 1. Look up DNB if unknown
/internal-jargon DNB
# Result: DNB = Digital Native Businesses

# 2. Discover where DNB appears (Owner Role vs Vertical)
sf data query --query "SELECT Owner.UserRole.Name, COUNT(Id) FROM Account WHERE Owner.UserRole.Name LIKE '%DNB%' GROUP BY Owner.UserRole.Name"
# Result: DNB appears in Owner Role names like "AE - AMER Enterprise & Emerging - DNB Strat Core 2"

# 3. Count UCOs across all DNB accounts (active stages only) using subquery
sf data query --query "SELECT COUNT(Id) FROM UseCase__c WHERE Account__c IN (SELECT Id FROM Account WHERE Owner.UserRole.Name LIKE '%DNB%') AND Stages__c IN ('U2', 'U3', 'U4', 'U5')"
# Result: 245 active UCOs across 246 DNB accounts
```

### Common Segment Mappings

**Sales Segments (Owner Role field):**
- `DNB` → Owner.UserRole.Name LIKE '%DNB%' (Digital Native Businesses)
- `FSI` → Owner.UserRole.Name LIKE '%FSI%' (Financial Services Industry)
- `PubSec` → Owner.UserRole.Name LIKE '%PubSec%' (Public Sector)
- `Emerging` → Owner.UserRole.Name LIKE '%Emerging%'

**Industry Verticals (Vertical_New__c field):**
- `Enterprise Technology`
- `Financial Services` / `FinServ`
- `Public Sector`
- `CME` (Communications, Media & Entertainment)
- `Healthcare & Life Sciences`
- `Retail` / `CPG`

### Key Efficiency Rules:
- **ALWAYS** use subqueries or IN clauses for bulk operations - never loop over individual accounts
- **DO NOT** re-lookup jargon you've already resolved in the conversation
- **ALWAYS** filter UCOs to active SA tracking stages (`U2, U3, U4, U5`) unless explicitly asked otherwise
- **DISCOVER** which field contains the segment before querying (Owner Role vs Vertical)
- **USE** `LIKE '%segment%'` for Owner Role queries to match partial role names
- **COMBINE** related queries when possible to minimize API calls

### Segment-Based vs Territory-Based Queries

**Important distinction:** The query approach differs based on whether the user is asking about:

1. **A person's territory** (e.g., "What UCOs does Kyle Pistor have?")
   - Use `FEL2Team__c` field on the User object
   - **ALWAYS add region filter** `u.FEPhysicalRegion__c = 'AMER'` to avoid cross-regional data

2. **A segment directly** (e.g., "What DNB Strat UCOs haven't been updated?")
   - Use `ur.Name LIKE '%DNB Strat%'` on UserRole
   - Region filter may **not be needed** if the role name already contains the region (e.g., "AMER Enterprise & Emerging")

**Role Name Patterns for Common Segments:**

| Segment | Role Pattern | Example Role Names |
|---------|-------------|-------------------|
| DNB Strategic | `LIKE '%DNB Strat%'` | "AE - AMER Enterprise & Emerging - DNB Strat Core 1" |
| DNB Named | `LIKE '%DNB Named%'` | "AE - AMER Enterprise & Emerging - DNB Named B2B Core 1" |
| DNB Geo | `LIKE '%DNB Geo%'` | "AE - AMER Enterprise & Emerging - DNB Geo Tech Hunter" |
| FSI Named | `LIKE '%FSI Named%'` | "AE - AMER Enterprise & Emerging - FSI Named Core" |
| PubSec Federal | `LIKE '%PubSec Fed%'` | "AE - AMER Enterprise & Emerging - PubSec Federal" |

**Discovery query** to find exact role patterns:
```sql
SELECT DISTINCT Name FROM main.sfdc_bronze.userrole
WHERE processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.userrole)
AND Name LIKE '%DNB Strat%'
ORDER BY Name
```

## Logfood SQL Alternative (Recommended for Read Queries)

For segment-based analytics, Logfood SQL queries are often **faster and more powerful** than SOQL. See `resources/LOGFOOD_QUERIES.md` for details.

**Example: Count UCOs by segment using Logfood:**

```sql
-- Much faster than SOQL subqueries! Always use MAX(processDate) for current data.
SELECT ur.Name as segment, COUNT(*) as uco_count
FROM main.sfdc_bronze.usecase__c uc
JOIN main.sfdc_bronze.account a ON uc.Account__c = a.Id
JOIN main.sfdc_bronze.user u ON a.OwnerId = u.Id
JOIN main.sfdc_bronze.userrole ur ON u.UserRoleId = ur.Id
WHERE uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
AND ur.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.userrole)
AND ur.Name LIKE '%DNB%'
AND uc.Stages__c IN ('U2', 'U3', 'U4', 'U5')
GROUP BY ur.Name
ORDER BY uco_count DESC
```

**Historical Analysis (Logfood-only capability):**

Track how records changed over time - see when UCO stages changed, go-live dates were pushed, or escalations progressed:

```sql
-- Track a UCO's stage changes over the last 30 days
SELECT processDate, Stages__c, Implementation_Status__c, Full_Production_Date__c
FROM main.sfdc_bronze.usecase__c
WHERE Id = 'aAvXXXXXXXXXXXXXXX'
ORDER BY processDate DESC
LIMIT 30
```

This historical capability is **unique to Logfood** - the Salesforce API only returns current state.