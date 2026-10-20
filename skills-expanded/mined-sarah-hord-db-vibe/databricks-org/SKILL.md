---
name: databricks-org
description: Look up organizational information for Databricks employees including BU, BU+1, segment, vertical, manager hierarchy, direct/indirect reports, and territory accounts. Do NOT use if the user explicitly asks to search Glean or look up someone in Glean — use glean-search instead.
capabilities:
  - Business Unit (BU) via FEL2Team__c (FE roles) or User_Sub_Region__c (AEs/Sales)
  - Parent Business Unit (BU+1) via FEL1Team__c
  - Segment via Role_Segment__c
  - Vertical (industry focus) for accounts
  - Manager hierarchy and reporting structure
  - Direct and indirect reports (distinguishing ICs vs managers)
  - Territory account associations for individuals and managers
  - Region-aware filtering for cross-regional data safety
  - Support for both Field Engineering and Sales/AE role types
---

# Databricks Organization Lookup

Look up organizational structure and hierarchy information for Databricks employees using Logfood data.

## What This Skill Does

Given a person's name or email, this skill can identify:
1. **BU (Business Unit)**: The person's business unit (FEL2Team__c for FE, or parsed from User_Sub_Region__c for AEs)
2. **BU+1**: The parent business unit (FEL1Team__c)
3. **Manager**: Who they report to
4. **Segment**: What segment they're in (Role_Segment__c)
5. **Region**: What region they're in (FEPhysicalRegion__c for FE, or parsed from User_Region__c for AEs)
6. **Direct Reports**: People who report directly to them (with IC vs manager distinction)
7. **Full Organization**: Complete hierarchy of all reports (direct and indirect)
8. **Territory Accounts**: Customer accounts associated with individuals or a manager's org

## Role Type Detection

**IMPORTANT:** Different Databricks roles use different fields for organizational data.

### Field Engineering (FE) Roles
FE roles (SAs, SA Managers, FE Leaders) have populated:
- `FEL1Team__c` - BU+1 (Parent Business Unit)
- `FEL2Team__c` - BU (Business Unit)
- `FEL2Role__c` - FE Role (SA, SA Manager 1st Line, etc.)
- `FEPhysicalRegion__c` - Region (AMER, EMEA, APJ)

### Sales Roles (AEs, AE Managers, Sales Leaders)
Sales roles like Account Executives have **NULL values** for all FE-specific fields. Instead, use:

| Field | Value Example | What It Tells You |
|-------|---------------|-------------------|
| `User_Sub_Region__c` | "DNB Strat Core 1" | Contains BU prefix (DNB, FSI, PubSec, HLS, etc.) |
| `User_Region__c` | "AMER Enterprise & Emerging" | Contains region (AMER, EMEA, APJ) |
| `Role_Segment__c` | "Enterprise" | Segment (same as FE) |

**How to determine BU for AEs:** Parse the BU prefix from `User_Sub_Region__c`:
- "DNB Strat Core 1" → BU is **DNB**
- "FSI Banking West" → BU is **FSI**
- "PubSec Fed Civilian" → BU is **PubSec**
- "HLS Pharma East" → BU is **HLS**
- "Retail CPG Central" → BU is **Retail**
- "Manufacturing Auto" → BU is **Manufacturing**

**How to determine Region for AEs:** Parse from `User_Region__c`:
- "AMER Enterprise & Emerging" → Region is **AMER**
- "EMEA Enterprise" → Region is **EMEA**
- "APJ Enterprise" → Region is **APJ**

### Detection Logic

When querying a user, check if FE fields are populated:

```sql
CASE
  WHEN FEL2Team__c IS NOT NULL THEN 'FE'
  ELSE 'Sales/Other'
END as role_type
```

For Sales roles, extract BU from `User_Sub_Region__c` using the first word/acronym:

```sql
-- Extract BU prefix from User_Sub_Region__c for Sales roles
CASE
  WHEN FEL2Team__c IS NOT NULL THEN FEL2Team__c
  WHEN User_Sub_Region__c LIKE 'DNB%' THEN 'DNB'
  WHEN User_Sub_Region__c LIKE 'FSI%' THEN 'FSI'
  WHEN User_Sub_Region__c LIKE 'PubSec%' THEN 'PubSec'
  WHEN User_Sub_Region__c LIKE 'HLS%' THEN 'HLS'
  WHEN User_Sub_Region__c LIKE 'Retail%' THEN 'Retail'
  WHEN User_Sub_Region__c LIKE 'Manufacturing%' THEN 'Manufacturing'
  WHEN User_Sub_Region__c LIKE 'Tech%' THEN 'Tech'
  ELSE SPLIT(User_Sub_Region__c, ' ')[0]
END as derived_bu
```

## CRITICAL: Regional Scoping

**BU names are NOT globally unique!** The same BU name can exist across multiple regions:

| BU Name | Regions Where It Exists |
|---------|-------------------------|
| DNB | AMER, APJ (Japan) |
| FSI | AMER, EMEA, APJ |
| PubSec | AMER, EMEA |
| HLS | AMER, EMEA |

**⚠️ WARNING:** When filtering data by BU (e.g., finding use cases, accounts, or opportunities for a BU), you MUST ALSO filter by region to avoid cross-regional data leakage.

**WRONG - will capture data from ALL regions with this BU:**
```sql
-- BAD: Captures AMER DNB AND Japan DNB data!
WHERE ur.Name LIKE '%DNB%'
```

**CORRECT - scoped to specific region:**
```sql
-- GOOD: Only captures AMER DNB data
WHERE ur.Name LIKE '%DNB%'
  AND u.FEPhysicalRegion__c = 'AMER'
```

**Best practice:** When looking up a user's org info, ALWAYS capture both their BU AND region. Then use both values when filtering other data (use cases, accounts, opportunities, etc.).

## Instructions

**Step 1: Load Related Skills**

Before starting, proactively load the `salesforce-actions` skill into context:
```
/salesforce-actions
```
This is important because org lookups often lead to Salesforce data queries (use cases, accounts, opportunities). Having the Salesforce schemas and query patterns in context prevents incorrect queries.

**Step 2: Execute Queries**

**Use the `logfood-querier` skill** to execute all queries below. This skill queries Logfood (Databricks internal data warehouse) which is more efficient than direct Salesforce queries.

**CRITICAL: Always use `--profile=logfood`** for all queries. Do NOT use any other profile name (not `fe-logfood`, not `fe-dogfood`, not `fe-central-sa`). The profile is simply `logfood`.

### Key Logfood Tables

| Table | Purpose |
|-------|---------|
| `main.sfdc_bronze.user` | Primary user info, BU/BU+1, manager IDs, FE role data |
| `main.sfdc_bronze.accountteammember` | Account-to-user relationships, team roles |
| `main.metric_store.dim_workday_attributes_latest` | Manager chain, estaff, job profiles - **best for hierarchy** |
| `main.fin_live_gold.sfdc_users_mapping` | Clean BU/Sub BU mapping, role names |

### 1. Look Up the User

Find a user by name or email. **See `resources/user-lookup.sql` for the full query with derived fields for both FE and Sales roles.**

**⚠️ Use the derived fields for consistent BU + Region:**
- **derived_bu** - Works for both FE (from FEL2Team__c) and Sales (parsed from User_Sub_Region__c)
- **derived_region** - Works for both FE (from FEPhysicalRegion__c) and Sales (parsed from User_Region__c)

**Key fields:**
| Field | FE Roles | Sales Roles | Notes |
|-------|----------|-------------|-------|
| `FEL2Team__c` | BU (e.g., "DNB") | NULL | Use derived_bu instead |
| `FEPhysicalRegion__c` | Region (e.g., "AMER") | NULL | Use derived_region instead |
| `FEL2Role__c` | Role (e.g., "SA") | NULL | FE-specific |
| `User_Sub_Region__c` | Sub-region + hierarchy | Territory with BU prefix | Parse BU from first word |
| `User_Region__c` | Territory | Region prefix (e.g., "AMER...") | Parse region from first word |
| `Role_Segment__c` | Segment | Segment | Works for both |

### 2. Get Full Management Chain (Upward)

Use the Workday table for clean manager hierarchy. This gets the person and all managers up to estaff:

```sql
-- Get management chain from a person up to estaff
SELECT
  workday_id,
  dim_employee_name_latest as name,
  dim_business_title_latest as title,
  dim_employee_email_latest as email,
  dim_manager_name_latest as manager,
  dim_manager_email_latest as manager_email,
  dim_estaff_latest as estaff,
  dim_sup_org_name_latest as sup_org
FROM main.metric_store.dim_workday_attributes_latest
WHERE dim_employee_email_latest IN (
  '<person_email>',
  '<manager_email>',
  '<manager2_email>',
  -- Add more manager emails as you discover them
)
ORDER BY dim_employee_name_latest
```

**Tip**: Query the person first to get their manager_email, then iteratively query up the chain.

### 3. Get Direct Reports (with IC vs Manager distinction)

Get all direct reports for a manager, distinguishing ICs from managers:

```sql
-- From SFDC Bronze (has FEL2Role__c for IC/Manager distinction)
SELECT
  Id,
  Name,
  Email,
  Title,
  FEL2Role__c,
  CASE
    WHEN FEL2Role__c LIKE '%Manager%' THEN 'Manager'
    ELSE 'IC'
  END as employee_type,
  User_Sub_Region__c
FROM main.sfdc_bronze.user
WHERE ManagerId = '<manager_sfdc_id>'
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
  AND IsActive = true
ORDER BY
  CASE WHEN FEL2Role__c LIKE '%Manager%' THEN 0 ELSE 1 END,  -- Managers first
  Name
```

**Alternative using Workday (simpler, by email):**
```sql
SELECT
  dim_employee_name_latest as name,
  dim_business_title_latest as title,
  dim_employee_email_latest as email,
  dim_job_profile_latest as job_profile,
  CASE
    WHEN dim_business_title_latest LIKE '%Manager%'
      OR dim_business_title_latest LIKE '%Director%'
      OR dim_business_title_latest LIKE '%VP%'
    THEN 'Manager'
    ELSE 'IC'
  END as employee_type
FROM main.metric_store.dim_workday_attributes_latest
WHERE dim_manager_email_latest = '<manager_email>'
ORDER BY employee_type, name
```

### 4. Get Full Organization Hierarchy (All Reports - Recursive)

Get the entire org under a manager using a recursive CTE. **See `resources/org-hierarchy.sql` for the full query.**

Key points:
- Uses `main.metric_store.dim_workday_attributes_latest` for clean hierarchy
- Recursive CTE with `level < 10` to prevent infinite recursion
- Distinguishes managers vs ICs using title patterns (`Manager`, `Director`, `VP`)

### 5. Get Accounts for an Individual

Find accounts where a person is on the account team:

```sql
SELECT DISTINCT
  a.Name as AccountName,
  atm.TeamMemberRole,
  a.Owner_Territory__c as Territory
FROM main.sfdc_bronze.accountteammember atm
JOIN main.sfdc_bronze.account a
  ON atm.AccountId = a.Id
  AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
WHERE atm.UserId = '<user_sfdc_id>'
  AND atm.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.accountteammember)
  AND atm.IsDeleted = false
ORDER BY
  CASE WHEN atm.TeamMemberRole LIKE 'Primary%' THEN 0 ELSE 1 END,
  a.Name
```

### 6. Get Accounts for a Manager's Org

Get all accounts covered by a manager's entire organization. **See `resources/accounts-for-org.sql` for the full query.**

Key points:
- Combines recursive org CTE with accountteammember join
- Filters by `TeamMemberRole LIKE '%Solution Architect%'` for SA accounts
- Returns account name, team member, and role

### 7. Region-Aware Queries for Related Data

When querying use cases, accounts, or other data for a BU, ALWAYS include region filtering. Here are region-safe query patterns:

**UCOs by BU (region-safe):**
```sql
-- Get UCOs for a BU, properly scoped to region
SELECT uc.Id, uc.Name, uc.Stages__c, uc.Implementation_Status__c
FROM main.sfdc_bronze.usecase__c uc
JOIN main.sfdc_bronze.account a ON uc.Account__c = a.Id
JOIN main.sfdc_bronze.user u ON a.OwnerId = u.Id
JOIN main.sfdc_bronze.userrole ur ON u.UserRoleId = ur.Id
WHERE uc.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.usecase__c)
AND a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
AND ur.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.userrole)
AND u.FEL2Team__c = '<BU>'              -- e.g., 'DNB'
AND u.FEPhysicalRegion__c = '<REGION>'  -- e.g., 'AMER'
AND uc.Stages__c IN ('U2', 'U3', 'U4', 'U5')
```

**Accounts by BU (region-safe):**
```sql
-- Get accounts for a BU, properly scoped to region
SELECT DISTINCT a.Id, a.Name, a.Owner_Territory__c
FROM main.sfdc_bronze.account a
JOIN main.sfdc_bronze.user u ON a.OwnerId = u.Id
WHERE a.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.account)
AND u.processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user)
AND u.FEL2Team__c = '<BU>'              -- e.g., 'DNB'
AND u.FEPhysicalRegion__c = '<REGION>'  -- e.g., 'AMER'
AND u.IsActive = true
```

**Alternative: Use FEL1Team__c (already contains region):**
```sql
-- FEL1Team__c includes region prefix, so LIKE '%AMER%DNB%' is region-safe
WHERE u.FEL1Team__c LIKE '%AMER%' AND u.FEL2Team__c = 'DNB'
```

### 8. Format the Results

Present information in a clear, hierarchical format. **Always prominently display both BU AND Region.** Adapt the format based on role type.

**For FE Roles (SAs, SA Managers):**
```
=== ORGANIZATIONAL INFORMATION ===

Person: <Name> (<Email>)
Title: <Title>
Department: <Department>
Role Type: Field Engineering

⚠️ REGIONAL SCOPE (use both for filtering):
  BU (Business Unit): <FEL2Team__c>
  Region: <FEPhysicalRegion__c>

BU+1 (Parent BU): <FEL1Team__c>
Segment: <Role_Segment__c>
FE Role: <FEL2Role__c>
Sub-Region: <User_Sub_Region__c>
Cost Center: <Cost_Center__c>
EStaff: <estaff>
```

**For Sales Roles (AEs, AE Managers):**
```
=== ORGANIZATIONAL INFORMATION ===

Person: <Name> (<Email>)
Title: <Title>
Department: <Department>
Role Type: Sales/AE

⚠️ REGIONAL SCOPE (use both for filtering):
  BU (Business Unit): <derived_bu> (parsed from User_Sub_Region__c: "<User_Sub_Region__c>")
  Region: <derived_region> (parsed from User_Region__c: "<User_Region__c>")

Segment: <Role_Segment__c>
Territory: <User_Sub_Region__c>
Cost Center: <Cost_Center__c>
EStaff: <estaff>

=== MANAGEMENT CHAIN ===
1. <Person> - <Title>
   ↳ 2. <Manager> - <Title>
      ↳ 3. <Manager's Manager> - <Title>
         ↳ ... (up to estaff)

=== DIRECT REPORTS ===
Total: <count> (Managers: <X>, ICs: <Y>)

Managers:
  1. <Name> - <Title>
  2. <Name> - <Title>

Individual Contributors:
  1. <Name> - <Title>
  2. <Name> - <Title>
...

=== FULL ORGANIZATION ===
Total: <count> people

Level 1 (Direct Reports): <count>
  Managers: <X>, ICs: <Y>

Level 2: <count>
  Managers: <X>, ICs: <Y>

Level 3: <count>
  ...

=== ACCOUNTS ===
Total: <count> accounts

Primary SA:
  1. <Account Name>
  2. <Account Name>

Solution Architect:
  1. <Account Name>
  2. <Account Name>
```

## Example Usage

**User asks:** "Who reports to Maneesh Bhide?"

**Response:**
1. Query Logfood for Maneesh Bhide's user info
2. Use recursive CTE to get his full org (132 people)
3. Distinguish managers from ICs
4. Present hierarchy by level with counts

**User asks:** "What is Brandon Kvarda's BU and segment?"

**Response:**
1. Query `main.sfdc_bronze.user` for Brandon Kvarda
2. Check role_type: FE (FEL2Team__c is populated)
3. Extract: BU = DNB, BU+1 = AMER Enterprise & Emerging, Segment = Enterprise, Region = AMER

**User asks:** "What is Natalie Smith's BU?" (where Natalie is an AE)

**Response:**
1. Query `main.sfdc_bronze.user` for Natalie Smith
2. Check role_type: Sales/Other (FEL2Team__c is NULL)
3. Use alternative fields:
   - `User_Sub_Region__c` = "DNB Strat Core 1" → **BU = DNB**
   - `User_Region__c` = "AMER Enterprise & Emerging" → **Region = AMER**
   - `Role_Segment__c` = "Enterprise" → **Segment = Enterprise**

**User asks:** "What accounts does Kyle Pistor's team cover?"

**Response:**
1. Get all members of Kyle's org using recursive CTE
2. Join to accountteammember to find all accounts
3. Group by account and show which team member covers each

## Quick Reference Queries

**Find someone's BU, segment, AND REGION:** See `resources/user-lookup.sql` - handles both FE and Sales roles with derived fields.

**Find all users in a specific BU + Region (FE only):**
```sql
SELECT Name, Email, Title, FEL2Role__c, User_Sub_Region__c
FROM main.sfdc_bronze.user
WHERE FEL2Team__c = '<BU>' AND FEPhysicalRegion__c = '<REGION>'
  AND processDate = (SELECT MAX(processDate) FROM main.sfdc_bronze.user) AND IsActive = true
```

**Count an org / List managers:** See `resources/org-hierarchy.sql` - use with GROUP BY for counts or WHERE for filtering.

## Important Notes

- **⚠️ REGIONAL SCOPING**: BU names (FEL2Team__c) are NOT globally unique. Always capture and filter by BOTH BU + Region (FEPhysicalRegion__c) when querying related data.
- **⚠️ ROLE TYPE AWARENESS**: FE-specific fields (FEL2Team__c, FEPhysicalRegion__c, FEL2Role__c) are NULL for Sales roles like AEs. Always check role_type and use derived fields (derived_bu, derived_region) for consistent results across all roles.
- **AE/Sales BU detection**: For AEs, parse BU from `User_Sub_Region__c` (e.g., "DNB Strat Core 1" → "DNB"). The first word/acronym typically indicates the BU.
- **AE/Sales Region detection**: For AEs, parse region from `User_Region__c` (e.g., "AMER Enterprise & Emerging" → "AMER"). The first word indicates the region.
- **Data freshness**: Logfood data is synced daily (24-48 hour lag). For real-time data, fall back to Salesforce queries.
- **processDate filter**: Always filter `sfdc_bronze` tables by `processDate = (SELECT MAX(processDate) FROM <table>)` to get latest data.
- **Recursive CTE limit**: Use `WHERE o.level < 10` to prevent infinite recursion.
- **IC vs Manager detection**: Use title patterns (`Manager`, `Director`, `VP`) or `FEL2Role__c` field.
- **Account coverage**: Use `accountteammember` table with `TeamMemberRole LIKE '%Solution Architect%'` for SA accounts.
- **Alternative region scoping**: FEL1Team__c contains region prefix (e.g., "AMER Enterprise & Emerging"), so filtering by FEL1Team__c LIKE '%AMER%' can also provide regional scoping.

## Troubleshooting

**"No results found":**
- Try using LIKE with wildcards: `Name LIKE '%firstname%'`
- Check email format: use full email `<name>@databricks.com`
- Verify user is active

**FE fields (FEL2Team__c, FEPhysicalRegion__c) are NULL:**
- This is expected for non-FE roles (AEs, AE Managers, Sales Leaders, etc.)
- Use `User_Sub_Region__c` to derive BU (e.g., "DNB Strat Core 1" → DNB)
- Use `User_Region__c` to derive region (e.g., "AMER Enterprise & Emerging" → AMER)
- See "Role Type Detection" section for full details

**Query timeout:**
- Add LIMIT clause
- Reduce recursive depth
- Query specific levels instead of full recursion

**Missing manager in chain:**
- Some managers may not be in Workday yet
- Fall back to `sfdc_bronze.user` with `ManagerId` field
