---
name: eng-blockers
description: Engineering blocker search - find product gaps, escalations, and customer blockers
---

# Engineering Blockers

Search and analyze engineering blockers tracked in `main.eng_blockers.use_case_blockers`. SQL-based operations that surface product gaps, customer escalations, and architecture feasibility issues.

**Pattern**: Fast SQL reads from logfood (no API rate limits)

## Engineering Blockers vs Aha Ideas

**Engineering Blockers** (this skill):
- **What**: Technical issues blocking customer deployments/deals RIGHT NOW
- **Who**: SAs/AEs tracking account-specific issues
- **Purpose**: Escalation tracking and deal risk management
- **Tense**: Present tense - "Customer is BLOCKED today"
- **Financial impact**: Tracked via dollarDBUs and deal size
- **Blocker types**: "Blocked" (hard stop) vs "Friction" (painful workaround)
- **Examples**: "Acme Corp can't go live - HMS Federation doesn't work with Streaming"

**Aha! Ideas** (`aha-ideas` skill):
- **What**: Feature requests and product feedback portal
- **Who**: Anyone (SAs, customers, PMs, engineering)
- **Purpose**: Product roadmap planning and customer voice
- **Tense**: Forward-looking - "We WANT this feature"
- **Status**: Open → Investigating → Planned → In Progress → Shipped
- **Examples**: "Add row-level security to Unity Catalog", "Support Iceberg REST catalog"

**The Relationship**:
- Engineering blockers can link to Aha ideas (via `aha_id`/`merge_aha_id` fields)
- Multiple customer blockers often point to the same Aha idea
- Not all Aha ideas have blockers (feature requests without immediate customer pain)
- Not all blockers have Aha ideas (customer-specific issues)

**Example flow**:
1. SA discovers customer blocked by missing feature
2. Create eng blocker (account, use case, dollarDBUs, blocker_type)
3. Search Aha for existing feature request
4. Link blocker to Aha idea (aha_id field)
5. Add proxy vote to Aha idea
6. PM sees aggregate impact → prioritizes for roadmap

**When to use which**:
- 🔴 **Customer blocked TODAY** → Use this skill (search for existing blockers, check financial impact)
- 🟢 **Customer wants feature for FUTURE** → Use `aha-ideas` skill (search for existing ideas, create or vote)
- 🔗 **Both** → Search blockers for financial impact, search Aha for roadmap status, link them together

## Prerequisites

- Databricks CLI authenticated to the logfood workspace
- Access to `main.eng_blockers` catalog

## Available Operations

### 1. Search Engineering Blockers

**Use when**: User wants to find blockers by keyword, product area, or technology

**Input**:
- Keyword (required) - searches across blocker_comment, aha_name, and Applicable_Products
- Optional filters: severity, blocker_type (Blocked vs Friction)

**Output**:
- blocker_id
- acct_name (affected customer)
- uc_name (use case)
- blocker_comment
- blocker_category
- canonical_aha_id (linked Aha idea, deduplicated)
- canonical_aha_name
- canonical_status (Aha status)
- blocker_type (Blocked vs Friction)
- uc_stage (use case stage)
- dollarDBUs (financial impact)
- Applicable_Products
- SA/AE names
- aha_url

**Implementation**: Query `main.eng_blockers.use_case_blockers` with LIKE search

**Example queries**:
```
User: "search for blockers related to HMS Federation"
User: "find engineering blockers for Spark Structured Streaming"
User: "what are the blockers for Unity Catalog row-level security"
```

### 2. Get Blockers by Account

**Use when**: User wants to see all known blockers affecting a specific customer

**Input**:
- account_name (supports partial match)

**Output**:
- All blockers for that account
- Sorted by blocker_type (Blocked first) then dollarDBUs DESC
- Includes linked Aha ideas and their status
- SA/AE assignments

**Implementation**: Query `main.eng_blockers.use_case_blockers` filtered by acct_name

**Example queries**:
```
User: "show me all blockers for Acme Corp"
User: "what blockers affect the Hinge Health account"
User: "find blockers for SF account 001DE00002KHqRk"
```

## Phase 1: Search Engineering Blockers

When the user asks to search for engineering blockers:

1. **Parse the search intent**
   - Extract the keyword(s) from the user's query
   - Identify product areas, features, or technologies mentioned
   - Determine if user wants to filter by blocker_type or severity

2. **Execute the SQL query**
   - Use `search_blockers.sql` template
   - Replace `<keyword>` with the extracted search term
   - Execute via Databricks SQL CLI or SDK

3. **Format the results**
   - Present results sorted by financial impact (dollarDBUs DESC)
   - Show top 50 results
   - Highlight canonical Aha ID (deduplicated reference)
   - Include Aha URL for each linked idea

**SQL Template** (`resources/search_blockers.sql`):
```sql
SELECT
  blocker_id,
  acct_name,
  uc_name,
  blocker_comment,
  blocker_category,
  COALESCE(merge_aha_id, aha_id) as canonical_aha_id,
  COALESCE(merge_aha_name, aha_name) as canonical_aha_name,
  COALESCE(merge_aha_status, aha_status) as canonical_status,
  blocker_type,
  uc_stage,
  dollarDBUs,
  Applicable_Products,
  blocker_created_date,
  sa_name,
  ae_name,
  databricks_vertical
FROM main.eng_blockers.use_case_blockers
WHERE LOWER(blocker_comment) LIKE LOWER('%<keyword>%')
   OR LOWER(aha_name) LIKE LOWER('%<keyword>%')
   OR LOWER(Applicable_Products) LIKE LOWER('%<keyword>%')
ORDER BY dollarDBUs DESC NULLS LAST
LIMIT 50;
```

**Interpretation Guide**:
- **blocker_type = "Blocked"**: Hard blocker, customer cannot proceed
- **blocker_type = "Friction"**: Workaround exists but suboptimal
- **canonical_aha_id**: Use this instead of aha_id (handles merged ideas)
- **dollarDBUs**: Financial impact estimate (higher = more critical)
- **uc_stage**: Use case maturity (POC, Dev, Production)

## Phase 2: Get Blockers by Account

When the user asks for blockers affecting a specific account:

1. **Normalize the account name**
   - Support partial matches (e.g., "Acme" matches "Acme Corp")
   - Handle Salesforce IDs (e.g., 001DE00002KHqRk)

2. **Execute the SQL query**
   - Use `blocker_by_account.sql` template
   - Replace `<account_name>` with the normalized name
   - Execute via Databricks SQL CLI or SDK

3. **Present the comprehensive view**
   - Group by blocker_type (Blocked first, then Friction)
   - Sort by financial impact within each group
   - Show linked Aha ideas with status
   - Include SA/AE contact information

**SQL Template** (`resources/blocker_by_account.sql`):
```sql
SELECT
  blocker_id,
  acct_name,
  uc_name,
  blocker_comment,
  blocker_category,
  blocker_type,
  canonical_aha_id,
  canonical_aha_name,
  canonical_status,
  uc_stage,
  dollarDBUs,
  Applicable_Products,
  blocker_created_date,
  sa_name,
  ae_name,
  aha_url
FROM main.eng_blockers.use_case_blockers
WHERE LOWER(acct_name) LIKE LOWER('%<account_name>%')
ORDER BY
  CASE blocker_type WHEN 'Blocked' THEN 0 ELSE 1 END,
  dollarDBUs DESC NULLS LAST;
```

**Account-Level Insights**:
- Total blocker count (Blocked vs Friction breakdown)
- Total financial impact (sum of dollarDBUs)
- Most critical blocker (highest dollarDBUs)
- Linked Aha ideas with status (which are In Progress, Planned, Shipped)
- SA/AE owners for follow-up

## Understanding Canonical Aha IDs

**Problem**: Aha ideas can be merged/deduplicated, creating stale references

**Solution**: Use `COALESCE(merge_aha_id, aha_id)` for the canonical reference
- If an idea was merged into another, `merge_aha_id` points to the canonical one
- If not merged, `merge_aha_id` is NULL and `aha_id` is canonical
- Always prefer `canonical_aha_id` in output

**Example**:
```
blocker_id: BL-12345
aha_id: DB-I-10001 (original idea)
merge_aha_id: DB-I-10500 (merged into this one)
canonical_aha_id: DB-I-10500 ✓ (use this)
```

## Use Cases

### Architecture Feasibility Questions
```
User: "My customer wants to use Spark Structured Streaming with HMS Federation - are there known blockers for that architecture?"
Action: Search for "HMS Federation" + "Streaming" → surface known issues
```

### Pre-Filing Aha Ideas
```
User: "Before I file an Aha for Unity Catalog row-level security, check if it already exists as a blocker"
Action: Search for "Unity Catalog" + "row-level" → find existing blockers + linked Aha ideas
```

### Account Health Check
```
User: "Show me all blockers for Acme Corp so I can prep for the QBR"
Action: Get blockers by account → prioritize by financial impact → group by Aha status
```

### Escalation Triage
```
User: "Find all blockers with dollarDBUs > 1M that have no Aha linked"
Action: Custom filter on dollarDBUs + canonical_aha_id IS NULL → identify escalation gaps
```

## Error Handling

**SQL Errors**:
- Connection failures → verify Databricks CLI profile for logfood workspace
- Table not found → verify access to `main.eng_blockers` catalog (may require ACL grant)
- Empty results → suggest broader search terms or check spelling

**Data Quality Issues**:
- NULL dollarDBUs → financial impact unknown, deprioritize in sort
- Missing canonical_aha_id → blocker not yet linked to an Aha idea
- Stale blocker_created_date → may be resolved but not marked as such

## Related Resources

- `resources/search_blockers.sql` - Keyword search across blocker comments, Aha names, and products
- `resources/blocker_by_account.sql` - Account-specific blocker lookup

## Related Skills

This is a generic skill - other skills build on these operations:
- `fe-internal-tools:aha-ideas` - Complementary Aha! Ideas operations (search, detail)
- `fe-workflows:performance-tuning` - May reference blockers during architecture analysis

## Notes

- **Logfood data freshness**: Tables updated daily (may lag by ~24 hours)
- **Financial impact**: `dollarDBUs` is an estimate based on use case stage and customer size
- **Blocker types**: "Blocked" = hard blocker, "Friction" = workaround exists
- **Canonical IDs**: Always use `canonical_aha_id` instead of raw `aha_id` to handle merged ideas
- **Account matching**: Partial match supported (e.g., "Acme" finds "Acme Corp, Inc.")
