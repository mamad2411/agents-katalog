---
name: byaan:learn
description: Analyze the codebase database schema, query patterns, and business domain to build a data-agent skill. Use when setting up a new project, after schema changes, or when the data-agent skill needs updating.
disable-model-invocation: true
---

You are a codebase analyst. Your job is to deeply analyze this project's data layer and build (or update) a skill that teaches AI how to write accurate queries against the databases in this codebase.

This skill can be run at any time to learn or re-learn the codebase. It is also invoked automatically during `/byaan:start` onboarding.

## Step 1: Deep Codebase Analysis

Analyze the following in order. Be exhaustive. Read every relevant file.

### Database Models & Schema
- Find ALL model/schema definition files (SQLAlchemy, Mongoose, Prisma, Sequelize, TypeORM, Django models, Drizzle, etc.)
- For each model/collection, document:
  - Table/collection name (actual DB name, not class name)
  - Every field: name, type, nullable, defaults, constraints
  - Primary keys, foreign keys, unique constraints
  - Indexes (single, compound, unique, partial, text)
  - Relationships (one-to-one, one-to-many, many-to-many) with join tables/foreign keys
  - Enums and their possible values
  - Soft deletes, timestamps, versioning patterns

### Data Access Patterns
- Find ALL places models are queried: repositories, DAOs, services, controllers, scripts, migrations, seeders, jobs, workers
- For each, document:
  - What queries are commonly run (CRUD, aggregations, joins, subqueries)
  - Filtering patterns (common WHERE clauses, date ranges, status filters)
  - Pagination approaches (offset, cursor, keyset)
  - Sorting conventions
  - Aggregation pipelines (MongoDB) or GROUP BY patterns (SQL)
  - Raw queries vs ORM usage
  - Transaction patterns
  - Bulk operations

### Business Domain Context
- What do the entities represent in business terms?
- What are the core domain relationships? (e.g., "A User has many Notebooks, each Notebook has many Queries")
- What are the most important entities and why?
- What status flows exist?
- What are the tenant/org/workspace scoping rules?

### Query Performance & Conventions
- What indexes exist and what queries do they optimize?
- Are there materialized views, CTEs, or complex SQL patterns?
- MongoDB: aggregation pipelines? Change streams? Atlas Search?
- Naming conventions (snake_case, camelCase, plural table names, etc.)

## Step 2: Build the Skill File

Create the directory `.claude/skills/data-agent/` if it does not exist, then create or overwrite `.claude/skills/data-agent/SKILL.md` with this structure:

```markdown
---
name: data-agent
description: "Query the database. Write SQL/MongoDB queries for data analysis, debugging, reporting, and exploration. Use when asked to query data, analyze records, build reports, debug data issues, or explore the database schema."
---

# Data Agent Skill

## When to Use
- User asks to query, analyze, or explore data
- User asks to debug a data issue or find specific records
- User asks to build a report or aggregate data
- User asks "how many", "which", "find all", "show me" type questions about data
- User asks to write a migration or seed script that needs schema knowledge

## Database Overview
[One paragraph: what database(s) this app uses, the ORM/driver, connection details pattern]

## Complete Schema Reference

### [Table/Collection Name]
**Description:** [What this entity represents in business terms]
**Actual DB name:** `table_name`

| Column | Type | Nullable | Default | Notes |
|--------|------|----------|---------|-------|
| id | uuid/int | no | gen | Primary key |
| ... | ... | ... | ... | FK -> other_table.id |

**Indexes:**
- `idx_name` on (col1, col2) — used for [what query pattern]
- unique on (tenant_id, email)

**Key relationships:**
- Has many `orders` via `orders.user_id`
- Belongs to `organization` via `org_id`

**Common filters:** status IN ('active', 'pending'), created_at ranges, tenant scoping

[Repeat for EVERY table/collection]

## Enum & Status Values
[List every enum with all possible values and what they mean]

## Relationship Map
[Describe the full entity relationship graph in text — how everything connects]

## Query Patterns & Examples

### Filtering & Scoping Rules
- [e.g., "Always filter by tenant_id when querying user-scoped data"]
- [e.g., "Soft-deleted records have deleted_at IS NOT NULL — exclude by default"]

### Common Query Templates
[Include: joins, aggregations, date ranges, pagination, full-text search patterns from the actual codebase]

### Performance Rules
[Index usage, large table warnings, select-only-what-you-need rules]

### Anti-Patterns to Avoid
[N+1, unscoped queries, unindexed filters, etc.]

## Database-Specific Notes
[DB-specific syntax, functions, or features relied on — JSONB operators, $facet, GROUP_CONCAT, etc.]
```

## Rules

1. Read every single model file. Do not skip any. Do not summarize.
2. Read how models are actually used in repositories, services, and controllers.
3. Use actual table/collection names as they appear in the database.
4. Include real examples from the codebase adapted into standalone query form.
5. The skill teaches querying, not coding. No ORM syntax, no API endpoints. Raw SQL / MongoDB shell queries.
6. Keep the skill file under 1000 lines. Be dense and precise. Use tables for schemas.
7. If the codebase uses multiple databases, document each separately.

## Step 3: Verify

After building the skill, cross-reference at least 3 complex queries from the codebase to verify your schema documentation would enable someone to write them correctly.

Print a summary:
> Codebase analysis complete.
> - [N] tables/collections documented
> - [N] relationships mapped
> - [N] query patterns captured
> - Skill file: .claude/skills/data-agent/SKILL.md
>
> Run `/byaan:learn` again after schema changes to keep the skill current.
