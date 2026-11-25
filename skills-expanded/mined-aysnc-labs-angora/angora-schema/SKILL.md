---
name: angora-schema
description: Design or evolve SQLite schema (`src/data/schema/tables/*.ts`) using Drizzle ORM — new tables, relational modeling, junction tables for many-to-many, foreign keys, CHECK constraints, SEO fields (slug, meta_title, meta_description), draft/published status columns, and media references. Trigger whenever the user wants to model a new content type (events, team members, case studies, pricing tiers, blog posts with tags), rethink an existing table's structure, or design relationships between tables. Phrases like 'new table for events', 'model a pricing_tiers table', 'schema for a job board', 'junction table for posts and tags', 'how should I model FAQs by category' all trigger this. For single-column additions or quick queries use angora-data.
argument-hint: <what to model>
---

# Schema: $ARGUMENTS

## Before you start

1. **Read `src/system.md`** — understand the site's intent and scope.
2. **Read schema** — glob `src/data/schema/tables/*.ts` to discover tables, then read the relevant files. One file per table.

## Analysis phase (always happens)

Whether the user gives you structured data or a vague description, always analyze first. Ask yourself:

- "Six months from now, what will they wish they had modeled?"
- Arrays of objects → child tables
- Repeated file references → media references (FK to `media`)
- Many-to-many relationships → junction tables
- Enum-like values → CHECK constraints or lookup tables
- Is this content that drives pages? → needs SEO + status fields

Ask the user probing questions. Don't just accept the first description — refine it.

## Schema conventions

Every table gets:
- `id INTEGER PRIMARY KEY AUTOINCREMENT`
- `created_at TEXT NOT NULL DEFAULT (datetime('now'))`
- Foreign keys where appropriate

### Page-driving tables

When records will get their own pages (blog posts, case studies, team members, cities), add:
- `slug TEXT NOT NULL UNIQUE` — URL-safe identifier
- `meta_title TEXT` — for `<title>` tag
- `meta_description TEXT` — for `<meta name="description">` and OG tags
- `status TEXT NOT NULL DEFAULT 'draft'` with `CHECK (status IN ('draft', 'published'))` — enables content staging, only published records render

Explain to the user why these fields matter (SEO, content staging, clean URLs).

### Media references

Use `media_id INTEGER REFERENCES media(id)` for a primary image/asset. For multiple images, consider a junction table.

## Presentation before execution

Before changing any files:

1. **Show the Drizzle table definition** — the TypeScript that will go in its own file under `schema/`
2. **Show example data** — 2-3 realistic rows per table
3. **Show example queries** — Drizzle queries page templates will need (e.g., `db.select().from(testimonials).where(eq(testimonials.status, 'published'))`)
4. **Wait for user approval** — all schema changes require explicit approval

## Applying schema changes

Schema changes follow a three-step process:

### 1. Create a new file in `src/data/schema/tables/`

One file per table. Example — `src/data/schema/tables/testimonials.ts`:

```ts
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';
import { sql } from 'drizzle-orm';
import { media } from './media';

export const testimonials = sqliteTable('testimonials', {
  id: integer('id').primaryKey({ autoIncrement: true }),
  name: text('name').notNull(),
  quote: text('quote').notNull(),
  mediaId: integer('media_id').references(() => media.id),
  status: text('status').notNull().default('draft'),
  createdAt: text('created_at').notNull().default(sql`(datetime('now'))`),
});
```

Then add the re-export to `src/data/schema/index.ts`:

```ts
export * from './tables/testimonials';
```

### 2. Generate migration

```bash
pnpm db:generate
```

This creates a readable `.sql` file in `src/data/migrations/`. Show it to the user.

### 3. Apply migration

```bash
pnpm db:migrate
```

**Each step requires user approval before executing.**

After applying, mention: "You can browse the data with `pnpm db:studio` whenever you're ready to seed some content."

## Rules

- **All schema changes require user approval** before executing.
- **Foreign keys are ON** — respect referential integrity.
- Use `text()` for dates (ISO 8601 format via `datetime('now')`).
- Use `integer()` for booleans (0/1).
- Media paths are relative to `public/media/`.
- The `media` table is the base — other tables reference it via `media_id`.
- **Never modify data** — use `/angora-data` for seeding or `/angora-import` for bulk inserts.
- **Never delete tables or columns without explicit permission.**