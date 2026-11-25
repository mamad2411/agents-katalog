---
name: schema-documentation-generator
description: "Generate human-readable data dictionary from DDL with LLM-written business descriptions. Reads DDL or ORM models, extracts structural metadata, and writes plain-English descriptions for every table, column, and relationship. Trigger: /schema-docs"
trigger: /schema-docs
---

# /schema-docs

Most production databases have zero documentation - cryptic column names (cst_id, flg_sts, mod_dt), no descriptions, no relationship context. This skill reads DDL or ORM models, extracts structural metadata, and writes plain-English descriptions for every table, column, and relationship.

## What this is for

- Parse DDL/ORM files (.sql, .prisma, TypeORM entities, SQLAlchemy models)
- Extract per-table structural metadata: columns, types, nullability, defaults, indexes, foreign keys, unique constraints
- Detect and expand naming abbreviations (cst -> customer, ord -> order, prd -> product, etc.)
- Generate a human-readable `schema-dictionary.md` with LLM-written business descriptions


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/schema-docs -help` or `/schema-docs -h` (without further arguments) is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Confirm project directory

Confirm `-ProjectDir` exists and contains DDL/ORM files (.sql, .prisma, TypeORM entities, SQLAlchemy models). If not provided, ask the user.

### Step 3 - Run collector

```powershell
& "<SKILL_DIR>/scripts/schema-extract.ps1" -ProjectDir "<ProjectDir>"
```

If exit code != 0: forward the error, stop.

### Step 4 - LLM analysis: tables

For each table in the extracted JSON, write a business name and purpose (1-2 sentences). Use the table name, column names, and inferred meanings to determine the business context.

### Step 5 - LLM analysis: columns

For each column in each table, write a meaningful plain-English description. Use the column name, type, nullability, default, and inferred meaning to determine what the column represents.

### Step 6 - LLM analysis: relationships

For each foreign key relationship, write the business meaning of the relationship (e.g., "An order belongs to a customer").

### Step 7 - Write schema-dictionary.md

Write `schema-dictionary.md` to the project directory with:
- Title and metadata (table count, column count, FK count, unnamed ratio)
- Per-table section: business name, purpose, columns table (name, type, nullable, default, description)
- Relationships section: each FK with business meaning
- Abbreviation legend: mapping of detected abbreviations to expansions

## Usage

```
/schema-docs                              # interactive (asks for ProjectDir)
/schema-docs -ProjectDir ./path/to/schemas # extract + generate dictionary
/schema-docs -help
```

## Report Format

The output `schema-dictionary.md` contains:

```markdown
# Data Dictionary: <project-name>

**Generated:** <date>
**Tables:** <n> | **Columns:** <n> | **Foreign Keys:** <n> | **Unnamed ratio:** <n>%

## <TableName> - <Business Name>

**Purpose:** <1-2 sentence business description>

| Column | Type | Nullable | Default | Description |
|--------|------|----------|---------|-------------|
| ...    | ...  | ...      | ...     | ...         |

## Relationships

| From | To | Business Meaning |
|------|----|------------------|
| ...  | ... | ...              |

## Abbreviation Legend

| Abbreviation | Expansion |
|-------------|-----------|
| cst         | customer  |
| ...         | ...       |
```


