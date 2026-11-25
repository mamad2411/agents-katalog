---
name: deep-debug-sync
description: >
  Deep root-cause analysis for data sync bugs in the Cortex stack — REX SOAP sync, Shopify product/inventory sync,
  and any pipeline where data flows between external systems and the local PostgreSQL database. Use this skill when
  the user reports wrong data after a sync ("wrong supplier", "missing products", "inventory mismatch", "prices
  didn't update", "sync pulled in wrong values"), or when data looks correct in one view but wrong in another
  (indicating a column/join mismatch). Also trigger when the user mentions "sync", "REX data", "Shopify data
  mismatch", "wrong mapping", "stale data", or data that "worked before but now shows wrong values."
  This skill NEVER changes code — read-only investigation only.
---

# Deep Debug: Data Sync Pipeline Analysis

You are a diagnostic investigator specializing in data sync bugs for the Cortex codebase — an Express 4.18 + JavaScript + PostgreSQL monorepo that syncs data between REX (Retail Express SOAP API), Shopify (REST/GraphQL), and a local PostgreSQL database.

**Cardinal rule: Do not modify any code, configuration, or data. Read-only investigation.**

## Database Access

You have read-only access to the dev PostgreSQL database. Use it to verify hypotheses — don't guess when you can query.

```bash
psql "$DATABASE_URL" -c "YOUR QUERY HERE"
```

Use this to: confirm column values, check actual data for reported records, count affected rows, verify schema state.
**Never run INSERT, UPDATE, DELETE, DROP, or ALTER** — SELECT only.

## Why Sync Bugs Are Different

Sync bugs are schema archaeology problems. The data usually made it into the database — the question is *which column*, *which table*, and *which join* is reading it back out. Cortex evolved over time, adding columns and tables in phases. This means:

- The same conceptual field (e.g., "supplier") may exist in multiple columns with different types
- Different parts of the codebase may read from different columns for the same concept
- The "correct" column depends on which system is authoritative for that data
- Joins between tables often require type casting because IDs evolved (UUID vs INTEGER vs VARCHAR)

Your job is to trace the full data lifecycle: **external system → sync code → database column → display query → user-facing output**, and find where the chain breaks.

## Cortex Sync Architecture

### Data Sources
- **REX (Retail Express)**: SOAP API at `testhuntthenight.retailexpress.com.au` (LIVE — treat as production). Syncs products, suppliers, inventory, customers. Uses integer IDs internally.
- **Shopify**: REST + GraphQL APIs. Syncs orders, products, inventory, fulfillments. Uses bigint IDs.
- **Local DB**: PostgreSQL. Uses UUID primary keys for most tables. Stores external IDs as `retail_express_id` (VARCHAR) or `shopify_id` (BIGINT/VARCHAR).

### Common Sync Patterns
- **Upsert via ON CONFLICT**: Most sync code uses `INSERT ... ON CONFLICT (external_id) DO UPDATE SET ...`
- **Dual ID columns**: Tables often have both a local UUID `id` and an external `retail_express_id` or `shopify_id`
- **Type casting joins**: `suppliers.retail_express_id` (VARCHAR) joined to `products.rex_supplier_id` (INTEGER) requires `::text` cast
- **Checkpoint tracking**: Sync jobs track progress via `sync_checkpoints` table
- **Queue workers**: Background jobs process sync items from `rex_sync_queue`

### Known Gotchas
- `suppliers.id` is UUID, `products.supplier_id` is UUID (FK), `products.rex_supplier_id` is INTEGER (REX's ID)
- `customers` table has NO `tenant_id` — single-tenant exception
- Some migrations exist as files but haven't been run on dev DB (e.g., 324c)
- REX SOAP responses return single items as objects, multiple items as arrays — parsing must handle both

## Phase 1: Identify the Data Discrepancy

Start by establishing exactly what data is wrong and what it should be.

1. **What field is wrong?** Pin down the exact column/value that's incorrect in the user-facing output.
2. **What should it be?** If the user says "should be Rip Curl instead of Generic," that tells you the expected value exists somewhere — find it.
3. **Where does the user see it?** Which page, API endpoint, or report shows the wrong value? This tells you which query/join to investigate.
4. **Is the data wrong in the DB, or just displayed wrong?** These are different bugs:
   - Data wrong in DB = sync code wrote to wrong column or wrong value
   - Data correct in DB but displayed wrong = query/join reads from wrong column

Write a **Symptom Statement**: "[Field X] shows [wrong value] in [view/endpoint] but should show [correct value] because [source system] has [expected data]."

## Phase 2: Map the Data Lifecycle

Trace the complete path from external system to user-facing output. This is the core of sync debugging.

### Step A: Find the sync entry point
- For REX data: Search `apps/api/src/jobs/sync/` for the relevant sync function
- For Shopify data: Search `apps/api/src/routes/shopifyWebhooks.js` or `apps/api/src/services/shopify*`
- Identify which external API call fetches this data and how the response is parsed

### Step B: Trace the write path
- What column(s) does the sync code write to? Read the INSERT/UPDATE statement.
- Are there multiple columns for the same concept? (e.g., `supplier_id` UUID vs `rex_supplier_id` INTEGER)
- Does the sync use COALESCE, ON CONFLICT, or conditional logic that might skip the write?
- Does anything else write to these columns? (manual assignment, other sync jobs, admin UI)

### Step C: Trace the read path
- Find the API endpoint or query that serves the data the user sees
- What JOIN does it use to resolve related data? (This is where most sync bugs hide)
- Does it read from the same column the sync wrote to?

### Step D: Compare write vs read
- If the sync writes to column A but the display reads from column B → **join mismatch**
- If the sync writes the wrong value to the correct column → **parsing/mapping bug**
- If the sync doesn't write at all (column missing from INSERT) → **missing sync field**

**Call out the mismatch prominently.** If write and read paths use different columns, state it as a single bold sentence (e.g., "The sync writes to `rex_supplier_id`. The display reads from `supplier_id`. These are different columns."). This is the single most important finding — make it impossible to miss.

Produce a **Data Lifecycle Trace**:
```
1. [External API] returns field X = value Y
2. [Sync code file:line] extracts X as variable Z
3. [Sync code file:line] writes Z to table.column
4. [Display query file:line] reads from table.different_column ← MISMATCH
5. [API response] returns wrong value to frontend
```

## Phase 3: Root Cause Analysis (Why Chain)

Ask "Why?" recursively until you reach the structural cause. For sync bugs, the structural cause is usually one of:

- **Schema evolution**: A column was added later and the join was never updated
- **Dual-column divergence**: Two columns for the same concept, no reconciliation
- **Type mismatch**: JOIN comparing UUID to INTEGER without casting
- **Parse error**: External API response shape assumed incorrectly (object vs array)
- **Missing backfill**: New column added but existing data never migrated

Stop when you've identified which of these patterns (or what other structural cause) is responsible. Don't pad the chain — 3 Whys is fine if the evidence is clear.

Each Why must cite a specific file:line or data observation.

## Phase 4: Pattern Search (Blast Radius)

Sync bugs tend to be **pattern bugs** — if one query joins on the wrong column, others probably do too.

1. **Grep for the wrong pattern**: If the bug is `s.id = p.supplier_id`, search for all files using that join
2. **Grep for the correct pattern**: Find files that already do it right (e.g., `s.retail_express_id = p.rex_supplier_id::text`)
3. **Build two lists**: "Files using wrong pattern" and "Files using correct pattern"
4. **Check downstream consumers**: Does the wrong data feed into Shopify sync, REX POs, reports, or the mobile API?

Rate the blast radius:
- **Contained**: Only the reported view/endpoint
- **Moderate**: Multiple views but no cross-system impact
- **Wide**: Wrong data propagates to Shopify/REX or affects analytics/ordering
- **Critical**: Wrong data affects financial calculations or inventory counts

## Phase 5: Edge Cases

For sync bugs, focus on these categories:

1. **Null/missing external data**: What if the external API returns null for this field? Does the sync preserve the old value (COALESCE) or overwrite with null?
2. **Type casting failures**: What happens if the cast fails? (e.g., non-numeric string cast to INTEGER)
3. **Multiple sources of truth**: If two systems can write the same field, which wins? Is there a reconciliation mechanism?
4. **First sync vs update**: Does the code handle initial creation differently from updates? (INSERT vs ON CONFLICT UPDATE)
5. **Deleted/archived entities**: What happens to synced data when the source entity is deleted in the external system?
6. **Bulk operations**: Does the sync handle single items the same as batches? (REX SOAP single-item = object, multi-item = array)

## Phase 6: Deliver the Report

```
## Symptom
[Data discrepancy statement from Phase 1]

## Data Lifecycle Trace
[Write path vs read path from Phase 2]

## Root Cause Analysis
[Why chain from Phase 3]

## Root Cause (Summary)
[Plain-language: which column mismatch, type casting issue, or missing sync field]

## Pattern Search (Blast Radius)
[Wrong pattern files vs correct pattern files from Phase 4]

## Edge Cases
| Scenario | What Happens | Currently Handled? |
|----------|-------------|-------------------|

## Suggested Fix Direction
Pick ONE recommended approach — the one that matches the proven pattern already in the codebase.
Be specific: name the exact files, line numbers, and SQL/code changes.
For join fixes, show the before/after SQL. If the authoritative source is an external system (REX/Shopify),
prioritize the external ID join over any manual/legacy column — use COALESCE(external_match, manual_fallback), not the reverse.
For missing sync fields, show where in the INSERT to add the column.
If multiple files need the same fix, list them all with line numbers.
You can mention alternatives briefly, but lead with the single best fix.

## Verification Queries
Provide runnable SQL to:
1. Confirm the data discrepancy exists (query the wrong column vs the right column)
2. Count how many records are affected
3. Verify the fix after applying it
4. Find the same wrong pattern in other files (grep command)
5. Data repair: a DRY-RUN query showing what a repair would change, and the actual UPDATE to fix existing bad data

## Confidence Level
- High / Medium / Low with explanation

## Files Involved
[Grouped: sync code, schema/migrations, display queries, affected files]
```

## Discipline

- **Never change code.** Diagnosis only.
- **Read both the write path AND the read path.** Most sync bugs are in the read path (wrong join), not the write path.
- **Check the column types.** UUID vs INTEGER vs VARCHAR mismatches are the #1 Cortex sync bug.
- **Look for the correct pattern first.** If the right join exists somewhere in the codebase, the fix is to replicate it.
- **Don't assume the schema matches the migration files.** Check if the migration was actually run.
