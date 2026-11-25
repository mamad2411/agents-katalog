---
name: uco-blockers
description: Create, query, update, and close Blocker__c records on Use Case Objects (UCOs). Manage blocker lifecycle. For guided workflows involving Aha ideas (search, link Aha idea to UCO, vote on ideas), use aha-workflow instead.
---

# UCO Blockers

Manage `Blocker__c` records on Use Case Objects (UCOs) in Salesforce. Use this skill to log product blockers, track friction items, link Aha ideas, and close resolved blockers.

**Reference**: See `salesforce-actions` resource file `resources/Blocker.md` for the full `Blocker__c` schema and field reference.

## Prerequisites

Ensure authenticated with Salesforce. If commands fail, use `/salesforce-authentication` to set up access.

**IMPORTANT: Always use `--target-org` on every `sf` CLI command.** Resolve the org username once at session start and reuse:

```bash
SF_TARGET_ORG=$(sf org display --json 2>/dev/null | jq -r '.result.username // empty')
if [ -z "$SF_TARGET_ORG" ]; then
  SF_TARGET_ORG=$(sf org list --json 2>/dev/null | jq -r '.result.nonScratchOrgs[0].username // empty')
fi
```

Append `--target-org "$SF_TARGET_ORG"` to every `sf` command.

## Operations

### 1. Create a Blocker

Create a `Blocker__c` record linked to a UCO.

**Required**: `Use_Case__c` (the UCO ID)

**Recommended fields**:
- `Type__c`: `Blocked` (can't move forward) or `Friction` (slowing down)
- `Category__c`: See picklist values below
- `Comment__c`: Description of the issue
- `Account__c`: Account ID (auto-populated from UCO in some orgs, but set explicitly to be safe)
- `Aha_Idea__c`: SF ID of a linked `ahaapp__AhaIdea__c` record (if known)

**Category picklist values**: `C&SI Partner`, `Cloud Partner`, `Customer Blocker (unrelated to Databricks)`, `Customer Buy-In`, `Implementation`, `Legal`, `Migration not planned anytime soon`, `Operating Cost`, `Other`, `Product (Aha features, bugs, etc.)`, `Security / Compliance`

```bash
# Create a product blocker on a UCO
sf data create record --sobject Blocker__c \
  --values "Use_Case__c='<UCO_ID>' Type__c='Blocked' Blocker_Status__c='Open' Category__c='Product (Aha features, bugs, etc.)' Comment__c='Description of the product blocker' Account__c='<ACCOUNT_ID>'" \
  --target-org "$SF_TARGET_ORG" --json

# Create a friction item (not fully blocked, but slowed)
sf data create record --sobject Blocker__c \
  --values "Use_Case__c='<UCO_ID>' Type__c='Friction' Blocker_Status__c='Open' Category__c='Implementation' Comment__c='Migration tooling gaps slowing adoption' Account__c='<ACCOUNT_ID>'" \
  --target-org "$SF_TARGET_ORG" --json

# Create a blocker with an Aha idea already linked
sf data create record --sobject Blocker__c \
  --values "Use_Case__c='<UCO_ID>' Type__c='Blocked' Blocker_Status__c='Open' Category__c='Product (Aha features, bugs, etc.)' Comment__c='HMS Federation not supported with Structured Streaming' Account__c='<ACCOUNT_ID>' Aha_Idea__c='<AHA_IDEA_SF_ID>'" \
  --target-org "$SF_TARGET_ORG" --json
```

**After creating a blocker**: Consider updating the UCO health to Red if this is a true blocker:
```bash
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Status__c=Red" \
  --target-org "$SF_TARGET_ORG"
```

### 2. Query Blockers

#### By UCO
```bash
sf data query --query "SELECT Id, Name, Type__c, Blocker_Status__c, Category__c, Comment__c, Aha_Idea__c, Aha_Status__c, CreatedDate FROM Blocker__c WHERE Use_Case__c = '<UCO_ID>' ORDER BY CreatedDate DESC" \
  --target-org "$SF_TARGET_ORG" --json
```

#### By Account (all UCOs)
```bash
sf data query --query "SELECT Id, Name, Type__c, Blocker_Status__c, Category__c, Comment__c, Use_Case__r.Name, Aha_Idea__c, CreatedDate FROM Blocker__c WHERE Account__c = '<ACCOUNT_ID>' AND Blocker_Status__c IN ('Open', 'In Progress') ORDER BY CreatedDate DESC" \
  --target-org "$SF_TARGET_ORG" --json
```

#### Open blockers with Use Case and Aha context
```bash
sf data query --query "SELECT Id, Name, Type__c, Blocker_Status__c, Category__c, Comment__c, Use_Case__r.Name, Use_Case__r.Account__r.Name, Aha_Idea__c, Aha_Status__c FROM Blocker__c WHERE Blocker_Status__c IN ('Open', 'In Progress') AND Use_Case__r.Account__r.Name LIKE '%<ACCOUNT_NAME>%'" \
  --target-org "$SF_TARGET_ORG" --json
```

#### Using Logfood (recommended for reads)
For bulk queries, Logfood SQL is faster. See `salesforce-actions` resource `resources/Blocker.md` for Logfood query examples.

### 3. Update a Blocker

```bash
# Update status to In Progress
sf data update record --sobject Blocker__c --record-id <BLOCKER_ID> \
  --values "Blocker_Status__c='In Progress'" \
  --target-org "$SF_TARGET_ORG"

# Update comment
sf data update record --sobject Blocker__c --record-id <BLOCKER_ID> \
  --values "Comment__c='Updated: Engineering has a fix targeted for Q2'" \
  --target-org "$SF_TARGET_ORG"

# Change type from Blocked to Friction
sf data update record --sobject Blocker__c --record-id <BLOCKER_ID> \
  --values "Type__c='Friction'" \
  --target-org "$SF_TARGET_ORG"

# Add DBU impact
sf data update record --sobject Blocker__c --record-id <BLOCKER_ID> \
  --values "DBU_Blocked__c=50000" \
  --target-org "$SF_TARGET_ORG"
```

### 4. Close a Blocker

```bash
sf data update record --sobject Blocker__c --record-id <BLOCKER_ID> \
  --values "Blocker_Status__c='Closed' Blocker_Close_Date__c='$(date -u +%Y-%m-%dT%H:%M:%SZ)'" \
  --target-org "$SF_TARGET_ORG"
```

After closing the last open blocker on a UCO, consider updating UCO health:
```bash
# Check if any open blockers remain
sf data query --query "SELECT COUNT(Id) FROM Blocker__c WHERE Use_Case__c = '<UCO_ID>' AND Blocker_Status__c IN ('Open', 'In Progress')" \
  --target-org "$SF_TARGET_ORG" --json

# If count is 0, consider updating health to Green or Yellow
sf data update record --sobject UseCase__c --record-id <UCO_ID> \
  --values "Implementation_Status__c=Green" \
  --target-org "$SF_TARGET_ORG"
```

### 5. Link an Aha Idea to an Existing Blocker

To link an Aha idea, you need the **Salesforce record ID** of the `ahaapp__AhaIdea__c` object (not the Aha reference number).

#### Step 1: Find the Aha idea SF ID by reference number
```bash
sf data query --query "SELECT Id, Name, ahaapp__ReferenceNum__c, ahaapp__Status__c FROM ahaapp__AhaIdea__c WHERE ahaapp__ReferenceNum__c = 'DB-I-XXXXX'" \
  --target-org "$SF_TARGET_ORG" --json
```

#### Step 2: Update the blocker with the Aha idea SF ID
```bash
sf data update record --sobject Blocker__c --record-id <BLOCKER_ID> \
  --values "Aha_Idea__c='<AHA_IDEA_SF_ID>' Category__c='Product (Aha features, bugs, etc.)'" \
  --target-org "$SF_TARGET_ORG"
```

## Presenting Results

When displaying blockers, format as a clear summary:

```
## Blockers for [UCO Name] ([Account])

| # | Type | Status | Category | Aha Idea | Comment |
|---|------|--------|----------|----------|---------|
| 1 | Blocked | Open | Product | DB-I-18242 | HMS Federation not supported with Streaming |
| 2 | Friction | Open | Implementation | - | Migration tooling gaps |
```

To get the Aha reference number for display, query the linked `ahaapp__AhaIdea__c`:
```bash
sf data query --query "SELECT ahaapp__ReferenceNum__c FROM ahaapp__AhaIdea__c WHERE Id = '<AHA_IDEA_SF_ID>'" \
  --target-org "$SF_TARGET_ORG" --json
```

Construct the Aha URL as: `https://databrickinternal.ideas.aha.io/ideas/<REFERENCE_NUM>`

## Error Handling

- **Authentication errors**: Use `/salesforce-authentication` to set up access
- **Invalid UCO ID**: Search for the UCO by name: `sf data query --query "SELECT Id, Name FROM UseCase__c WHERE Name LIKE '%<TERM>%' AND Active__c = true"`
- **Invalid Account ID**: Use `salesforce-actions` to look up the account
- **Aha idea not found in SF**: The idea may not be synced yet. Search by partial reference: `WHERE ahaapp__ReferenceNum__c LIKE '%18242%'`

## Related Skills

- `salesforce-actions` - General Salesforce CRUD (schema reference in `resources/Blocker.md`)
- `uco-updates` - Update UCO health, stage, and next steps
- `aha-ideas` - Search and manage Aha ideas via the Aha API
- `aha-workflow` - Guided workflows for Aha ideas including linking to UCO blockers
- `eng-blockers` - Search engineering blockers in the eng-blockers database
