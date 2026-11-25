---
name: dsa-assignment-sync
description: Sync and validate DSA project assignments from Logfood against Salesforce UCO coverage. Identifies mismatches, missing assignments, and stale records. Use when someone says assignment sync, DSA sync, assignment validation, assignment audit, mismatch check.
user-invocable: true
---

# DSA Assignment Sync & Validation

Sync and validate DSA project assignments from Logfood against Salesforce UCO coverage. This skill cross-references two data sources to identify mismatches, missing assignments, stale records, and coverage gaps, then generates a sync report and optionally fixes issues in Salesforce.

## When to Use This Skill

Use this skill when you need to:
- Validate that Logfood DSA assignments match Salesforce UCO DSA fields
- Identify UCOs at team accounts that have no DSA assigned in Salesforce
- Find Logfood assignments that do not correspond to any active UCO
- Detect name mismatches between Logfood and Salesforce DSA fields
- Audit expired assignments that are still showing as active
- Fix assignment mismatches in Salesforce (with explicit user consent)

## Prerequisites

Before running this skill, ensure:
1. **Databricks** — Run `/databricks-authentication` (for Logfood queries)
2. **Salesforce** — Run `/salesforce-authentication` (for UCO DSA field queries and optional writes)

## Required Information

The skill needs a **team lead name** or **manager filter**. Provided as: $ARGUMENTS

If not provided, ask the user.

## Reference Files

- **`resources/DSA_LT_QUERIES.md`** (in `dsa-business-overview/resources/`) — SQL query templates
- **`resources/SYNC_REPORT_TEMPLATE.md`** — Sync report output template

---

## Step 0: Team Discovery

Identify the team using `main.field_dsa.dsa_roster_curr`:

```sql
SELECT dsa AS name, email, hire_date, dsa_manager
FROM main.field_dsa.dsa_roster_curr
WHERE LOWER(dsa_manager) LIKE '%{manager_name}%'
ORDER BY dsa
```

Build:
- `dsa_names` — Full names as they appear in Logfood (e.g., "Richa Sethi")
- `dsa_emails` — Emails for Salesforce User ID lookups
- `manager_name` — Manager name pattern

---

## Step 1: Pull Logfood Assignments

Query Logfood for all active DSA assignments using the detailed assignment query from `DSA_LT_QUERIES.md` (Section 3):

```sql
WITH expanded AS (
  SELECT
    account_name, business_unit, sales_subregion_level_1,
    EXPLODE(project_assignments) AS pa
  FROM main.field_dsa.dsa_project_assignment_outcomes
)
SELECT DISTINCT
  account_name,
  pa.project_name,
  pa.project_id,
  pa.assignment_resource_user_name,
  pa.assignment_resource_manager,
  CAST(pa.assignment_start_date AS STRING)  AS assignment_start_date,
  CAST(pa.assignment_end_date   AS STRING)  AS assignment_end_date,
  pa.assignment_status_custom,
  pa.dsa_engagement_type,
  COALESCE(CAST(pa.subscription_hours_weekly AS DOUBLE), 0) AS subscription_hours_weekly,
  COALESCE(CAST(pa.fte_req AS DOUBLE), 0)                   AS fte_req,
  pa.start_fq, pa.end_fq
FROM expanded
WHERE LOWER(pa.assignment_resource_manager) LIKE '%{manager_name}%'
  AND pa.assignment_status_custom IN ('CURRENT ASSIGNED', 'UPCOMING')
ORDER BY assignment_start_date
```

This gives us the **Logfood side** — what the assignment system says.

Also query the UCO pipeline for the same DSAs:

```sql
-- Use the UCO_SQL_TEMPLATE from DSA_LT_QUERIES.md Section 5
-- with dsa_list = team DSA names
```

This gives us the **Logfood UCO side** — what UCOs exist for team DSAs.

---

## Step 2: Pull Salesforce UCO DSA Fields

Use `/salesforce-actions` to query UCO records at team accounts. First, look up Salesforce User IDs for team members:

```bash
sf data query --query "SELECT Id, Name, Email FROM User WHERE Email IN ({emails_list}) AND IsActive = true" --json
```

Then query UCOs with DSA assignments:

```bash
sf data query --query "
  SELECT Id, Name, Stages__c, Account__r.Name, Account__c,
    DSA__c, DSA__r.Name, DSA__r.Email,
    Primary_Solution_Architect__c, Primary_Solution_Architect__r.Name,
    Solution_Architect__c, Solution_Architect__r.Name,
    Active__c, Implementation_Status__c
  FROM UseCase__c
  WHERE Account__r.Name IN ({account_list})
    AND Active__c = true
  ORDER BY Account__r.Name, Name
" --json
```

This gives us the **Salesforce side** — what SFDC says about DSA coverage.

---

## Step 3: Cross-Reference and Categorize

Compare the two data sources and categorize each assignment/UCO into one of these buckets:

### Category 1: Clean Match

Logfood assignment exists AND the Salesforce UCO has the correct DSA assigned.

| Account | UCO | Logfood DSA | SFDC DSA | Status |
|---------|-----|-------------|----------|--------|
| {account} | {uco_name} | {logfood_name} | {sfdc_name} | Match |

### Category 2: Logfood-Only (No SFDC UCO Coverage)

DSA has a Logfood assignment at the account, but no UCO at that account has this DSA in the `DSA__c` field.

| Account | Logfood DSA | Assignment Type | FTE | SFDC UCOs at Account | Issue |
|---------|-------------|-----------------|-----|---------------------|-------|
| {account} | {dsa_name} | {engagement_type} | {fte} | {uco_count} | No DSA field set |

**Possible causes**:
- UCO exists but `DSA__c` field is empty
- UCO exists but a different DSA is assigned
- No UCO exists at this account

### Category 3: SFDC-Only (No Logfood Assignment)

UCO has a DSA assigned in Salesforce, but that DSA has no active Logfood assignment at the account.

| Account | UCO | SFDC DSA | Stage | Issue |
|---------|-----|----------|-------|-------|
| {account} | {uco_name} | {sfdc_dsa_name} | U{stage} | No Logfood assignment |

**Possible causes**:
- Assignment expired but UCO DSA field was not cleared
- DSA was manually assigned in SFDC without a formal subscription
- Assignment is in a different system

### Category 4: Name Mismatch

Both Logfood and SFDC have the DSA assigned, but the names do not match exactly (typos, nicknames, format differences).

| Account | UCO | Logfood Name | SFDC Name | Similarity |
|---------|-----|-------------|-----------|------------|
| {account} | {uco_name} | {logfood_name} | {sfdc_name} | {score}% |

Use fuzzy matching (Levenshtein distance or similar) to detect near-matches.

### Category 5: Expired Assignment

Logfood assignment has `assignment_end_date` in the past, but the UCO still shows this DSA as active.

| Account | UCO | DSA | Assignment End | UCO Stage | Issue |
|---------|-----|-----|---------------|-----------|-------|
| {account} | {uco_name} | {dsa_name} | {end_date} | U{stage} | Assignment expired |

### Category 6: Orphan U5 (No DSA at All)

UCO is in U5 (Onboarding) at a team account, but has no DSA assigned in either Logfood or Salesforce.

| Account | UCO | Stage | Est. Quarterly DBUs | Target Live Date |
|---------|-----|-------|---------------------|------------------|
| {account} | {uco_name} | U5 | ${dbus} | {date} |

---

## Step 4: Generate Sync Report

Compile the cross-reference results into a formatted report.

**Load `resources/SYNC_REPORT_TEMPLATE.md`** for the template.

### Summary Statistics

| Metric | Value |
|--------|-------|
| Total Logfood Assignments | {count} |
| Total SFDC UCOs (Team Accounts) | {count} |
| Clean Matches | {count} ({pct}%) |
| Logfood-Only | {count} |
| SFDC-Only | {count} |
| Name Mismatches | {count} |
| Expired (Stale) | {count} |
| Orphan U5 | {count} |
| **Sync Score** | **{score}%** |

**Sync Score** = (Clean Matches / Total Logfood Assignments) * 100

### Mismatch Details

Present each category with full details (see Step 3 tables).

### Recommended Actions

For each mismatch, recommend a specific fix:

| # | Account | UCO | Current State | Recommended Action | Priority |
|---|---------|-----|---------------|-------------------|----------|
| 1 | {account} | {uco} | No DSA in SFDC | Set DSA__c = {user_id} | High |
| 2 | {account} | {uco} | Wrong DSA | Update DSA__c from {old} to {new} | High |
| 3 | {account} | {uco} | Expired assignment | Clear DSA__c | Medium |
| 4 | {account} | {uco} | No UCO exists | Create UCO or investigate | Low |

---

## Step 5: Optional Fixes (EXPLICIT CONSENT REQUIRED)

**NEVER write to Salesforce without EXPLICIT user approval.**

After presenting the sync report, you MUST:

1. **STOP** and show the full mismatch summary
2. **ASK** explicitly: "Would you like me to fix these mismatches in Salesforce? I will show you the exact changes before applying each one."
3. **WAIT** for the user to respond "yes", "approve", "proceed", or similar
4. **IF APPROVED**: Show a diff table for each change:

```
Change #1: Set DSA on UCO
Account: {account_name}
UCO: {usecase_name} ({usecase_id})
Field: DSA__c
Current: {empty or wrong name}
New: {correct_user_id} ({correct_name})

Apply? [y/n]
```

5. **GET CONFIRMATION** for each change (or batch if user says "apply all")
6. **EXECUTE** using `/salesforce-actions`:

```bash
sf data update record --sobject UseCase__c --record-id {uco_id} --values "DSA__c={user_id}" --json
```

7. **VERIFY** the update succeeded:

```bash
sf data query --query "SELECT Id, Name, DSA__r.Name FROM UseCase__c WHERE Id = '{uco_id}'" --json
```

**DO NOT assume consent. DO NOT write to SFDC unless the user explicitly approves. DO NOT apply changes without showing the diff first.**

---

## Domain Rules

### Name Matching

Logfood uses full names from the HR system (e.g., "Mujahid Ali Mohammed"). Salesforce may have different formats (e.g., "Muju Mohammed"). Common patterns:
- First name nicknames (Mujahid -> Muju)
- Middle names included/excluded
- Suffixes (Jr., III) present/absent

When matching, normalize:
1. Lowercase both names
2. Split into tokens
3. Match if last name matches AND first name starts with same letters
4. Use fuzzy matching for edge cases

### Account Name Matching

Logfood and Salesforce may have slightly different account names:
- Logfood: "ABC Company" vs SFDC: "ABC Company, Inc."
- Logfood: "XYZ Corp" vs SFDC: "XYZ Corporation"

Use `LIKE '%core_name%'` patterns when cross-referencing.

### Assignment Status Values

| Status | Meaning |
|--------|---------|
| CURRENT ASSIGNED | Active engagement |
| UPCOMING | Scheduled, not yet started |

Only `CURRENT ASSIGNED` assignments should have corresponding SFDC DSA fields set.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No roster data | Ask user for team lead name or DSA list |
| Logfood timeout | Retry once after 30s (cold start) |
| SFDC auth expired | Run `/salesforce-authentication` |
| Account name mismatch | Try fuzzy matching, ask user to confirm |
| UCO not found | Skip — may be in a different system |
| Write failed | Report error, continue with next change |
| User declines fixes | Stop. Report is the deliverable |

---

## Common Pitfalls

### Pitfall #1: Applying Fixes Without Consent
**Problem**: Auto-updating SFDC DSA fields without user approval
**Solution**: ALWAYS show diff and get explicit "yes" before any write

### Pitfall #2: Account Name Mismatches
**Problem**: "Acme Inc" in Logfood vs "Acme Inc." in SFDC causes false negatives
**Solution**: Normalize names (strip suffixes, lowercase) before comparing

### Pitfall #3: Matching by Name Instead of ID
**Problem**: Two DSAs with similar names could be confused
**Solution**: When available, match by email or Salesforce User ID, not just name

### Pitfall #4: Ignoring Orphan U5s
**Problem**: Focusing only on mismatches and missing the bigger gap — unassigned UCOs
**Solution**: Always include orphan U5 detection as a separate category

---

## Related Skills

- `/dsa-business-overview` — Monthly overview doc (uses assignment data)
- `/dsa-capacity-planning` — FTE analysis (uses same assignment data)
- `/salesforce-actions` — Salesforce query and update operations
- `/logfood-querier` — Logfood SQL queries
