---
name: angora-data
description: Quick operations on `src/data/data.sqlite` — inspect the current schema, add a single column to an existing table via Drizzle migration, seed 2-5 test rows, or run a read-only SELECT/COUNT query. Trigger whenever the user wants a small, single-step database operation. Phrases like 'add a company column to testimonials', 'seed 5 rows into pricing_tiers', 'show me the schema', 'count draft vs published posts grouped by author', 'what's in the media table', 'add a phone column to team_members' all trigger this. For designing new tables or rethinking relationships use angora-schema; for bulk imports from inbox files use angora-import.
argument-hint: [command]
---

# Data: $ARGUMENTS

Quick operations on the SQLite content layer (`src/data/data.sqlite`).

## Commands

| Command | Action |
|---------|--------|
| `schema` (or no arguments) | Show full database schema (glob `src/data/schema/tables/*.ts`) |
| `add column <table> <column>` | Add a column to the Drizzle schema, generate and apply migration (confirm first) |
| `seed <table>` | Generate 2-5 realistic sample rows |
| `query <description>` | Run a read-only query and display results |

## Schema inspection

Glob `src/data/schema/tables/*.ts` to discover tables, then read individual files for column details. No need to query the database for structure.

## Read-only queries

```bash
node -e "
  import db from './src/data/db.ts';
  import { media } from './src/data/schema/tables/media.ts';
  const rows = db.select().from(media).all();
  console.table(rows);
"
```

Use Drizzle's typed API. Import the relevant table from `schema/tables/<table>.ts` and use `db.select()`, `.where()`, etc.

## Schema changes (ALTER TABLE, etc.)

All DDL goes through the Drizzle workflow:

1. **Edit the table's file in `src/data/schema/tables/`** — add the column to the table definition
2. **Generate migration** — `pnpm db:generate`
3. **Apply migration** — `pnpm db:migrate`

Each step requires user approval.

## Seeding data

```bash
node -e "
  import db from './src/data/db.ts';
  import { <table> } from './src/data/schema/tables/<table>.ts';
  db.insert(<table>).values([
    { /* row 1 */ },
    { /* row 2 */ },
  ]).run();
  console.log('Seeded.');
"
```

## Rules

- **All schema changes require user approval** before executing.
- **Foreign keys are ON** — respect referential integrity.
- Use `text()` for dates (ISO 8601 format).
- Use `integer()` for booleans (0/1).
- `query` runs read-only — refuse writes via this command.

## For heavier work

This skill is for quick operations. For more involved work, use `/angora`:

- **Schema design** (new tables, relational modeling, SEO fields) → `/angora-schema`
- **Data import** (CSV, JSON from inbox) → `/angora-import`
- **Media processing** (images from inbox) → `/angora-media`