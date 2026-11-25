---
name: data-source-research
description: Investigate a data source (database, API, file system, message queue) ONCE and produce a permanent reference document. Use this skill BEFORE writing any code that reads from or writes to a data source. Triggers when the user mentions a database, API, table, schema, or any external data they want to use. ALWAYS persist findings so the source is never re-investigated. Solves the "Claude keeps re-asking about the database" problem.
---

# Data Source Research Skill

## The Problem This Solves

When Claude touches an unfamiliar database or API, it tends to re-investigate the same thing every session. This wastes tokens and time. This skill investigates ONCE, writes a permanent reference, and from then on every agent reads the reference instead of re-investigating.

## When to Trigger

ALWAYS run this skill before writing code that:
- Queries a database (SQL, NoSQL, time-series, graph)
- Calls a REST/GraphQL/gRPC API
- Reads from a message queue or stream
- Parses files of an unfamiliar format
- Connects to a legacy system

If the data source has been investigated before, READ the reference first. Re-investigate only if reference is stale (>30 days) or user explicitly asks.

## Workflow

### Step 1: Check for existing reference

Look in `docs/data-sources/` for an existing reference file matching the source. The naming convention is:

- `docs/data-sources/<source-name>.md` for any source
- For databases: `docs/data-sources/<db-type>-<db-name>.md` (e.g., `postgres-orders.md`, `clickhouse-analytics.md`)
- For APIs: `docs/data-sources/api-<service-name>.md`

If exists and not stale, use it directly. Skip the rest.

### Step 2: Plan the investigation

Tell the user: "I'm going to investigate <source>. This will take a few minutes. After this, I'll save findings so we never need to research the same source again."

List what you'll investigate:
- Connection details (host, port, auth method)
- Schema (tables/collections/endpoints)
- Volume (row counts, document counts, request rates)
- Indexes / partition keys / cursor strategies
- Sample data
- Quirks and gotchas

### Step 3: Investigate systematically

#### For SQL databases (PostgreSQL, MySQL, ClickHouse, etc.)

```sql
-- 1. Database identity
SELECT version();
SELECT current_database(), current_user;

-- 2. List of tables (PostgreSQL example)
SELECT table_schema, table_name, 
       pg_size_pretty(pg_total_relation_size(quote_ident(table_schema)||'.'||quote_ident(table_name))) AS size
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
ORDER BY pg_total_relation_size(quote_ident(table_schema)||'.'||quote_ident(table_name)) DESC;

-- 3. For each significant table, schema:
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = '<TABLE>'
ORDER BY ordinal_position;

-- 4. Indexes:
SELECT indexname, indexdef FROM pg_indexes WHERE tablename = '<TABLE>';

-- 5. Foreign keys:
SELECT
  tc.table_name, kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage ccu
  ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY';

-- 6. Row counts (sample for big tables):
SELECT '<TABLE>' AS t, count(*) FROM <TABLE>;

-- 7. Sample rows (5-10 representative):
SELECT * FROM <TABLE> LIMIT 10;

-- 8. Distinct values for likely-categorical columns:
SELECT <col>, count(*) FROM <TABLE> GROUP BY <col> ORDER BY count(*) DESC LIMIT 20;

-- 9. Null patterns:
SELECT 
  count(*) AS total,
  count(<col1>) AS non_null_col1,
  count(<col2>) AS non_null_col2
FROM <TABLE>;
```

For ClickHouse, also collect:
```sql
-- Engine + partitioning
SELECT name, engine, partition_key, sorting_key, primary_key
FROM system.tables WHERE database = '<DB>';

-- Partition stats
SELECT partition, count(), sum(rows), formatReadableSize(sum(bytes_on_disk))
FROM system.parts WHERE table = '<TABLE>' AND active
GROUP BY partition ORDER BY partition DESC LIMIT 10;
```

#### For REST/GraphQL APIs

- Fetch OpenAPI/Swagger spec if available
- Hit `/health`, `/version`, `/info` endpoints
- Make ONE example request per main endpoint and capture response shape
- Note rate limits from headers
- Note authentication mechanism

#### For message queues (Kafka, RabbitMQ, NATS)

- List topics/queues
- For each significant topic: partition count, retention, sample message
- Note schema registry if used
- Note consumer groups already in use

### Step 4: Write the reference

Save to `docs/data-sources/<source>.md`:

```markdown
# Data Source: <Source Name>

**Type:** PostgreSQL | ClickHouse | REST API | Kafka | ...
**Investigated:** <date>
**Investigated by:** Claude (run 'data-source-research' to refresh)
**Stale after:** <date + 30 days>

## Connection

```
host: <host>
port: <port>
database: <db>
auth: <method, where credentials live>
```

For local dev: <how to connect from a dev machine>
For prod: <how to connect from prod env>

## Schema Overview

<short narrative: what's in here>

## Tables / Collections / Endpoints

### Table: `<n>`

**Purpose:** <what it represents in domain terms>
**Volume:** ~<X> rows, growing ~<Y>/day
**Partitioning:** <if applicable>

| Column | Type | Nullable | Notes |
|---|---|---|---|
| id | uuid | NO | Primary key |
| created_at | timestamptz | NO | Indexed |
| status | text | NO | Enum: 'draft', 'submitted', 'confirmed', 'cancelled' |
| ... | ... | ... | ... |

**Indexes:**
- `idx_<n>_status` on (status) - used by dashboard queries
- `idx_<n>_created_at` on (created_at DESC) - used for recent items

**Foreign keys:**
- `customer_id` → `customers.id`

**Common queries seen in app code:**
```sql
-- Find pending orders for a customer
SELECT * FROM orders WHERE customer_id = $1 AND status = 'submitted'
ORDER BY created_at DESC LIMIT 50;
```

**Sample row:**
```json
{ "id": "...", "customer_id": "...", "status": "confirmed", ... }
```

**Quirks:**
- `metadata` column is JSONB but historically held mixed shapes; always check before parsing
- `legacy_id` is nullable but often present for rows imported from old system
- `status = 'draft'` rows older than 30 days are auto-cleaned by a cron job

### Table: `<next>`

...

## Cross-Table Relationships (ER summary)

```
customers (1) ─── (many) orders (1) ─── (many) order_lines
orders (1) ─── (many) shipments
```

## Performance Notes

- Total DB size: <X GB>
- Heaviest tables: <list>
- Slow queries observed: <if any>
- Connection pool size used in app: <N>

## Known Issues / Gotchas

- <thing that bit someone before>
- <historical anomaly>

## How to Refresh This File

Run the `data-source-research` skill again. It will overwrite this file with fresh data.
```

### Step 5: Verify and confirm

Show the user the reference file. Ask: "This look right? Anything to add?"

### Step 6: Hand off

Tell the user: "Reference saved to `docs/data-sources/<n>.md`. From now on, every agent will read this file instead of re-querying the database."

## Critical Rules

- **NEVER skip Step 1.** Always check for existing reference first.
- **NEVER write code that touches the source before the reference exists.** If the user asks to skip this, push back gently with cost argument: "Investigating once saves us about 30k tokens per future task."
- **Keep the reference up to date.** If you discover during implementation that something in the reference is wrong, update the reference immediately.
- **Don't dump 1000 columns.** For wide tables, document the columns the app actually uses, list the rest at the bottom.

## Recommendations

After investigation, output:
- Indexes that should exist but don't
- Tables that look like they need partitioning
- Schema patterns that suggest the data model could be cleaner
- Queries that should be cached
- Risks (data quality, missing FKs, etc.)
