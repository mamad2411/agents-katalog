---
name: aha-ideas
description: Aha! Ideas operations - search, detail lookup, create ideas, and add proxy votes
---

# Aha! Ideas

Search, view, create, and vote on Aha! Ideas in the Databricks internal portal (databrickinternal.ideas.aha.io). Generic operations that workflows can build upon.

**Pattern**: "Read from logfood, write with API"
- Fast SQL-based reads from `main.eng_blockers` tables (no rate limits)
- Targeted API writes only when mutating state (create ideas, add votes)

## Aha Ideas vs Engineering Blockers

**Aha! Ideas** (this skill):
- **What**: Feature requests and product feedback portal
- **Who**: Anyone (SAs, customers, PMs, engineering)
- **Purpose**: Product roadmap planning and customer voice
- **Tense**: Forward-looking - "We WANT this feature"
- **Status**: Open → Investigating → Planned → In Progress → Shipped
- **Examples**: "Add row-level security to Unity Catalog", "Support Iceberg REST catalog"

**Engineering Blockers** (`eng-blockers` skill):
- **What**: Technical issues blocking customer deployments/deals RIGHT NOW
- **Who**: SAs/AEs tracking account-specific issues
- **Purpose**: Escalation tracking and deal risk management
- **Tense**: Present tense - "Customer is BLOCKED today"
- **Financial impact**: Tracked via dollarDBUs and deal size
- **Examples**: "Acme Corp can't go live - HMS Federation doesn't work with Streaming"

**The Relationship**:
- Engineering blockers can link to Aha ideas (via `aha_id` field)
- Multiple customer blockers often point to the same Aha idea
- Not all Aha ideas have blockers (feature requests without immediate customer pain)
- Not all blockers have Aha ideas (customer-specific issues)

**When to use which**:
- 🔴 **Customer blocked TODAY** → Use `eng-blockers` skill (search for existing blockers, check financial impact)
- 🟢 **Customer wants feature for FUTURE** → Use this skill (search for existing ideas, create or vote)
- 🔗 **Both** → Search blockers for financial impact, search Aha for roadmap status, link them together

## Prerequisites

- Databricks CLI authenticated to the logfood workspace
- For write operations: Aha! OAuth2 credentials at `~/.vibe/aha/config.json`

## Available Operations

### 1. Search Aha Ideas

**Use when**: User wants to find existing Aha ideas by keyword, product area, or feature name

**Input**:
- Keyword (required)
- Search scope: "name" (faster, default) or "body" (thorough)
- Filter out closed statuses (default: true)

**Output**:
- reference_num (e.g., DB-I-18242)
- idea_name
- status (In progress, Planned, Investigating, Open, Shipped, etc.)
- votes (proxy vote count)
- categories (product area)
- assigned_to_name
- aha_url

**Implementation**: Query `main.eng_blockers.aha_ideas` or `aha_ideas_body` tables

**Example queries**:
```
User: "search aha for unity catalog lineage"
User: "find aha ideas about serverless real-time tables"
User: "check if there's an existing aha for HMS federation"
```

### 2. Get Aha Idea Detail

**Use when**: User wants full details on a specific Aha idea including proxy votes and linked blockers

**Input**:
- reference_num (e.g., DB-I-18242)

**Output**:
- Full metadata (name, body preview, status, votes, categories, assigned_to)
- List of proxy votes (voter names)
- Linked blockers from use_case_blockers (financial impact, affected accounts)
- Aggregate impact summary (total blockers, affected accounts, DBU impact)

**Implementation**: 4 SQL queries against `main.eng_blockers` tables

**Example queries**:
```
User: "show me details for DB-I-18242"
User: "what's the status of aha idea DB-I-15903"
User: "who voted for DB-I-18242"
```

### 3. Create Aha Idea (API)

**Use when**: User wants to file a new feature request

**Input**:
- title (required)
- description (required)
- product_id (required - e.g., "DB" for Databricks)
- created_by (optional - email of creator)
- categories (optional - comma-separated)
- tags (optional - comma-separated)

**Output**:
- reference_num (e.g., DB-I-12345)
- aha_url
- id (numeric ID)

**Implementation**: Uses `aha_api.create_idea()` which POSTs to Aha! REST API

**Prerequisites**:
- OAuth2 authentication via `python3 aha_auth.py login`
- Or API key stored in `~/.vibe/aha/credentials.json`

**Example queries**:
```
User: "create an aha idea for row-level security in Unity Catalog"
User: "file a feature request for serverless real-time tables"
```

### 4. Add Proxy Vote (API)

**Use when**: User wants to add a customer endorsement to an existing idea

**Input**:
- idea_id (required - e.g., "DB-I-12345")
- customer_email (required)
- description (optional - why customer needs this)
- value (optional - dollar value / ARR)
- link (optional - Salesforce opportunity URL)
- created_by (optional - email of SA creating the vote)

**Output**:
- confirmation message
- vote details (email, value, description)

**Implementation**: Uses `aha_api.add_proxy_vote()` which POSTs to Aha! REST API

**Prerequisites**: Same as Create Aha Idea (OAuth2 or API key)

**Example queries**:
```
User: "add a proxy vote for Acme Corp on DB-I-18242"
User: "vote for aha DB-I-15903 on behalf of customer@company.com with $250k ARR"
```

### 5. List Aha Product Areas

**Use when**: User wants to filter searches by product area or see valid categories

**Input**: None

**Output**: List of valid Aha! product area names

**Implementation**: Query distinct categories from `main.eng_blockers.aha_ideas`

**Example queries**:
```
User: "what aha product areas exist"
User: "show me aha categories"
```

## Phase 1: Search Aha Ideas

When the user asks to search for Aha ideas:

1. **Parse the search intent**
   - Extract the keyword(s) from the user's query
   - Determine search scope: name-only (faster) or body text (thorough)
   - Default to name-only unless user specifically wants deep search

2. **Execute the SQL query**
   - Use `aha_search.sql` template (Option 1 for name search, Option 2 for body search)
   - Replace `<keyword>` with the extracted search term
   - Execute via Databricks SQL CLI or SDK

3. **Format the results**
   - Present results in a table with: reference_num, idea_name, status, votes, aha_url
   - Sort by actionability (In progress → Planned → Open) then by votes
   - Limit to top 20 results

**SQL Template** (`resources/aha_search.sql`):
```sql
-- Option 1: Search idea names (faster)
SELECT reference_num, idea_name, status, votes, categories, aha_url
FROM main.eng_blockers.aha_ideas
WHERE LOWER(idea_name) LIKE LOWER('%<keyword>%')
  AND status NOT IN ('Will not implement', 'Duplicate')
ORDER BY status_priority, votes DESC
LIMIT 20;
```

## Phase 2: Get Aha Idea Detail

When the user asks for details on a specific Aha idea:

1. **Validate the reference number**
   - Format should be DB-I-##### (e.g., DB-I-18242)
   - If user provides just the number, prepend "DB-I-"

2. **Execute the 4 detail queries**
   - Query 1: Full idea metadata with body text preview
   - Query 2: Proxy votes list (voter names)
   - Query 3: Linked blockers with financial impact
   - Query 4: Aggregate impact summary

3. **Present the comprehensive view**
   - Main idea details (title, status, assignee, categories)
   - Proxy vote count and voter list
   - Linked blocker summary (affected accounts, DBU impact)
   - Aha URL for full details

**SQL Template** (`resources/aha_detail.sql`):
```sql
-- Query 1: Full metadata
SELECT reference_num, idea_name, body, status, votes, ...
FROM main.eng_blockers.aha_ideas_body
WHERE reference_num = '<reference_num>';

-- Query 2: Proxy votes
SELECT voter_name FROM main.eng_blockers.aha_proxy_votes
WHERE reference_num = '<reference_num>';

-- Query 3: Linked blockers
SELECT blocker_id, acct_name, dollarDBUs, ...
FROM main.eng_blockers.use_case_blockers
WHERE aha_id = '<reference_num>' OR merge_aha_id = '<reference_num>';

-- Query 4: Impact summary
SELECT COUNT(*) as total_blockers, SUM(dollarDBUs) as total_impact, ...
FROM main.eng_blockers.use_case_blockers
WHERE aha_id = '<reference_num>' OR merge_aha_id = '<reference_num>';
```

## Phase 3: List Product Areas

When the user asks for Aha! product areas:

1. **Query distinct categories**
   - Get unique values from `categories` column
   - Filter out nulls and generic values
   - Sort alphabetically

2. **Present the list**
   - Show all available product areas
   - Optionally show idea count per category

**Example SQL**:
```sql
SELECT
  categories as product_area,
  COUNT(*) as idea_count
FROM main.eng_blockers.aha_ideas
WHERE categories IS NOT NULL
GROUP BY categories
ORDER BY categories;
```

## Phase 4: Create Aha Idea

When the user wants to create a new Aha! idea:

### Prerequisites (One-time Setup)

**Authentication required** before first use. Choose one method:

**Method 1: API Key (Simplest)**
```bash
# User generates API key at https://databrickinternal.aha.io/settings/api_keys
mkdir -p ~/.vibe/aha
echo '{"access_token":"PASTE_KEY_HERE","aha_domain":"databrickinternal"}' > ~/.vibe/aha/credentials.json
chmod 600 ~/.vibe/aha/credentials.json

# Test
python3 ~/.claude/plugins/cache/fe-vibe/fe-internal-tools/*/skills/aha-ideas/resources/aha_api.py me
```

**Method 2: OAuth2 Flow**
```bash
# Run auth helper
python3 ~/.claude/plugins/cache/fe-vibe/fe-internal-tools/*/skills/aha-ideas/resources/aha_auth.py login

# This opens browser for Okta SSO → redirects to Aha! → stores tokens at ~/.vibe/aha/credentials.json
```

### Implementation Steps

1. **Check for duplicates**
   - First run search-aha-ideas with the proposed title keywords
   - Surface any existing ideas to the user
   - Ask: "Found similar ideas. Do you still want to create a new one?"

2. **Gather required fields**
   - **title**: Help user write a concise, descriptive title (< 80 chars)
   - **description**: Help draft clear description covering what, why, and business context
   - **product_id**: Usually "DB" for Databricks (or ask user to list products)
   - **created_by**: Use user's Databricks email (optional)
   - **categories**: Suggest based on search results or let user specify (optional)

3. **Create the idea**
   ```python
   from aha_api import create_idea

   idea = create_idea(
       title="Add Row-Level Security to Unity Catalog",
       description="Customers need RLS for regulatory compliance (GDPR, HIPAA)",
       product_id="DB",
       created_by="sa@databricks.com",
       categories="Unity Catalog,Security"
   )

   print(f"Created: {idea['reference_num']}")
   print(f"URL: {idea['url']}")
   ```

4. **Confirm and offer next steps**
   - Show the new reference_num and URL
   - Ask: "Would you like to add a proxy vote to this idea now?"

**CLI Example**:
```bash
python3 aha_api.py create \
  --title "Add Row-Level Security to Unity Catalog" \
  --description "Customers need RLS for GDPR/HIPAA compliance" \
  --product DB \
  --created-by sa@databricks.com
```

## Phase 5: Add Proxy Vote

When the user wants to add a customer endorsement to an idea:

### Prerequisites

Same authentication as Phase 4 (API key or OAuth2)

### Implementation Steps

1. **Validate the idea**
   - If user provides just keywords, search first (Phase 1)
   - If user provides reference_num, verify it exists with get-aha-idea-detail (Phase 2)
   - Show current vote count and status

2. **Gather vote details**
   - **customer_email**: Email of the customer (required)
   - **description**: Why does this customer need this feature? (optional but recommended)
   - **value**: Dollar value - ARR, deal size, or opportunity value (optional)
   - **link**: Salesforce opportunity or account URL for context (optional)
   - **created_by**: SA/AE email creating the vote (optional)

3. **Add the vote**
   ```python
   from aha_api import add_proxy_vote

   vote = add_proxy_vote(
       idea_id="DB-I-12345",
       customer_email="eng-lead@acmecorp.com",
       description="Critical for Q1 production deployment - they have 500+ TB data",
       value=250000,
       link="https://databricks.lightning.force.com/lightning/r/Opportunity/006.../view",
       created_by="sa@databricks.com"
   )

   print(f"Added vote from {vote['email']}")
   if vote.get('value'):
       print(f"Value: ${vote['value']:,}")
   ```

4. **Confirm**
   - Show updated vote count
   - Provide Aha! idea URL for user to view in browser

**CLI Example**:
```bash
python3 aha_api.py vote DB-I-12345 \
  --email eng-lead@acmecorp.com \
  --description "Critical for Q1 production deployment" \
  --value 250000 \
  --created-by sa@databricks.com
```

## Error Handling

**SQL Errors**:
- Connection failures → verify Databricks CLI profile
- Table not found → verify access to `main.eng_blockers` catalog
- Empty results → suggest broader search or check spelling

**API Errors**:
- Auth failures → run `python3 aha_auth.py login --force` to re-authenticate
- Token expired → `aha_auth.py` auto-refreshes tokens (should be transparent)
- Rate limits (300 req/min) → retry with exponential backoff
- Duplicate ideas → surface existing idea via search and ask if user still wants to create
- Invalid product_id → run `python3 aha_api.py products` to list valid products
- 404 idea not found → verify reference_num format (e.g., DB-I-12345)

## Related Resources

- `resources/aha_search.sql` - Search query templates (name + body search)
- `resources/aha_detail.sql` - Detail query templates (4 queries: metadata, votes, blockers, impact)
- `resources/aha_auth.py` - OAuth2 authentication manager with token refresh
- `resources/aha_api.py` - REST API wrapper (create, search, vote operations)

## Related Skills

This is a generic skill - other skills build on these operations:
- `fe-workflows:aha-workflow` - Opinionated multi-step workflow (smart search from meeting notes, guided creation)

## Notes

- **Logfood data freshness**: Tables updated daily (may lag by ~24 hours)
- **Canonical Aha IDs**: Use `merge_aha_id` when present (handles deduplicated ideas)
- **Status filtering**: Default excludes "Will not implement" and "Duplicate" to focus on actionable ideas
- **DBU impact**: Prioritize blockers by `dollarDBUs` DESC to surface financial impact
