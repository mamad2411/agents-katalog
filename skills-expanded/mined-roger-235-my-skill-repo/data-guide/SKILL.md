---
name: data-guide
description: "Navigation guide for all data category skills. Trigger when: which data skill should I use, database skill guide, data skill 導覽, 有哪些資料 skill, 資料庫 skill 怎麼用, help me with database design. Do not trigger for actually designing a database — route to the appropriate skill instead."
metadata:
  category: data
  version: "1.0"
---

# Data Skill Guide

Routes the user to the right data skill and explains what it covers.

## Purpose

Match the user's data or database goal to the correct skill and clarify the scope boundary between design and query/ORM work.

## Trigger

Apply when user asks:
- "which data skill", "database skill guide", "有哪些資料 skill", "資料庫 skill 怎麼用"

Do NOT trigger for:
- Actually designing a database — route to `db-schema` directly

## Prerequisites

None.

## Steps

1. **Identify the user's data goal** — match to the Routing Table below; pay attention to the scope boundary

2. **Recommend the skill** — describe what it will produce for the user's specific situation

3. **Clarify scope** — if the request is out of scope for available skills, state what the skill does NOT cover

## Routing Table

| Goal | Skill | Scope boundary |
|------|-------|---------------|
| Design new tables / entities from requirements | `db-schema` | Produces ER diagram + DDL + migrations |
| Add a new table to an existing schema | `db-schema` | Provide existing schema; skill adds the new table |
| Normalize an existing schema | `db-schema` | Paste current DDL; skill identifies NF violations |
| Write a migration file | `db-schema` | Part of db-schema output; includes `up` + `down` |
| Research market size, competitors, SWOT | `market-research` | Produces structured report with TAM/SAM/SOM |
| Build a financial model, P&L, or revenue forecast | `financial-modeling` | Produces P&L projection + unit economics + scenarios |
| Query optimization / EXPLAIN analysis | *(not covered)* | Use `debug` for runtime issues; no dedicated query skill |
| ORM usage (SQLAlchemy, Prisma, ActiveRecord) | *(not covered)* | ORM code is generated via `code-review` after schema |
| Data pipeline / ETL | *(not covered)* | No dedicated skill yet |

## Output Format

File path: none (routing recommendation printed to user)

```
## Data Skill Routing

**Your goal:** <one-line summary>

**Recommended skill:** `db-schema`
**What it will produce:** <ER diagram / DDL / migration tailored to the request>
**How to trigger:** "<trigger phrase>"

**Scope note (if applicable):**
<what the skill does NOT cover for this request>
```

## Rules

### Must
- Be explicit when a request falls outside the scope of available data skills
- For out-of-scope requests, suggest the closest available skill or workaround

### Never
- Perform database design or write SQL directly — route to the skill
- Claim `db-schema` handles ORM generation or query optimization

## Examples

### Good Example

User: "I need to add a `payments` table to my existing e-commerce schema."

```
## Data Skill Routing

**Your goal:** Add a payments table to an existing schema

**Recommended skill:** `db-schema`
**What it will produce:** ER diagram update, `payments` table DDL (with FK to `orders`, PII flags on card fields, `created_at`/`updated_at`), migration file with `up` + `down`
**How to trigger:** "add a payments table — here is my current schema: [paste DDL]"

**Scope note:**
db-schema outputs DDL and migrations; ORM model generation (e.g. Prisma schema or SQLAlchemy model) is a separate step done manually or via code-review after the DDL is confirmed.
```

### Bad Example

```
Sure, just add a payments table with id, amount, and user_id columns.
Here's the SQL: CREATE TABLE payments (...)
```

> Why this is bad: Performs the task directly instead of routing to `db-schema`. Skips the ER diagram, normalization check, PII flagging, migration file, and `ON DELETE RESTRICT` FK defaults that `db-schema` would produce. User gets incomplete output with no migration and no `down` rollback.
