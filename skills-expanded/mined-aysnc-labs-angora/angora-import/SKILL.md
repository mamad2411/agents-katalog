---
name: angora-import
description: Bulk-import structured data (CSV or JSON) from `inbox/` into existing database tables — maps fields to columns, validates against the Drizzle schema, inserts within a transaction. Trigger whenever the user wants to load, import, pull, or ingest a data file from inbox into an existing table. Phrases like 'import speakers.json from inbox', 'pull team.csv into team_members', 'load testimonials.csv', 'ingest the events in inbox', 'bulk load faqs.csv' all trigger this. Do NOT use for seeding a handful of test rows (→ angora-data), designing new tables (→ angora-schema), or processing images (→ angora-media).
argument-hint: <filename>
---

# Import: $ARGUMENTS

Import structured data from `inbox/` into the SQLite database.

## Before you start

1. **Check inbox** — verify the target file exists in `inbox/`.
2. **Read schema** — glob `src/data/schema/tables/*.ts` to discover tables, read relevant files for column details.

## Workflow

### 1. Read and detect format

Read the inbox file. Detect format:
- **JSON array** — `[{...}, {...}]`
- **Nested JSON** — `{ "testimonials": [...], "authors": [...] }`
- **CSV** — comma-separated with header row

### 2. Analysis phase

Map data fields to schema columns. Flag:
- Fields in data without matching columns
- Required columns (NOT NULL, no default) without data
- Type mismatches (string in INTEGER column, etc.)
- Missing foreign key targets (e.g., `media_id` referencing non-existent media)
- Duplicate slugs
- Which table(s) the data maps to

### 3. Flag schema gaps

If the data has fields that don't match the schema, **do NOT modify the schema**. Report clearly:

> "The data has a `company` field but the testimonials table doesn't have a `company` column. This needs schema work first. Run `/angora-schema` to update the schema."

### 4. Present mapping for approval

Show the user:
- Source field → Target column mapping
- Sample of first 2-3 rows as they would be inserted
- Any transformations needed (date format, slug generation, etc.)
- Row count

**Wait for user approval before inserting.**

### 5. Import with transactions

```bash
node -e "
  import db from './src/data/db.ts';
  import { <table> } from './src/data/schema/tables/<table>.ts';
  const rows = <data>;
  db.insert(<table>).values(rows).run();
  console.log('Inserted ' + rows.length + ' rows.');
"
```

Drizzle wraps multi-row inserts in a transaction by default.

### 6. Verify

Query and show a sample of inserted data:

```bash
node -e "
  import db from './src/data/db.ts';
  import { <table> } from './src/data/schema/tables/<table>.ts';
  import { desc } from 'drizzle-orm';
  const rows = db.select().from(<table>).orderBy(desc(<table>.id)).limit(5).all();
  console.table(rows);
"
```

## Rules

- **Never delete inbox files without explicit permission** — ask after processing
- **Never modify schema** — that's the schema specialist's job. Report gaps and recommend `/angora-schema`.
- **All imports require user approval** before executing
- Report validation errors with row numbers and field names
- Supports JSON and CSV (more formats can be added)