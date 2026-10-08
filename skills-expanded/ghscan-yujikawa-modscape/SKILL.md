---
name: modscape-spec-generate
description: Generate specs/<table-id>/spec.md for all tables found in the given implementation artifacts. Use this to bootstrap permanent table specs for an existing project before starting the regular SDD flow.
---

# Spec Generate

Generate `specs/<table-id>/spec.md` for all tables found in the given implementation artifacts.
Use this to bootstrap permanent table specs for an existing project before starting the regular SDD flow.

## Usage

```
@modscape-spec-generate [files...]
```

`[files...]` is optional. Accepts file paths, glob patterns, or a mix of both:

```
@modscape-spec-generate model.yaml
@modscape-spec-generate models/staging/*.sql src/models.py
@modscape-spec-generate model.yaml models/**/*.sql
```

If no arguments are provided, the skill will ask interactively.

## Instructions

**When reading model information from a YAML file, always use modscape CLI commands — do not use `grep` or direct file reads:**
```bash
modscape table list <file>
modscape table get <file> --id <id>
```

### Step 1: Collect input files

- If arguments are provided: use them as the list of input files. Expand globs if needed.
- If no arguments are provided: ask the user:
  > Which files should I read to discover tables? (Enter file paths or glob patterns — e.g., `model.yaml`, `models/**/*.sql`, `src/models.py`)
  Continue collecting until the user signals they are done.

### Step 2: Confirm model.yaml update

Immediately after collecting input files, before reading any file, ask:

> Should I also update (or create) `model.yaml` with the tables I find?
> - **Yes** — generate spec.md AND add/update tables in model.yaml
> - **No** — generate spec.md only (recommended if model.yaml already exists and is up to date)

If the user confirms model.yaml update:
- If model.yaml is among the input files, update it in place.
- If no model.yaml exists yet, ask the user for the target path (default: `model.yaml`).
- If a model.yaml exists but is not among the input files, ask whether to update it.

### Step 3: Read and extract tables

Read each input file and extract table definitions. Apply the following per file type:

**`.yaml` / `.yml` (model.yaml format)**
```bash
modscape table list <file>
# For each table id:
modscape table get <file> --id <id>
```
From each table, extract:
- `id`: `physical.name` if available, otherwise the table `id` field
- `owner`: `metadata.owner`
- `update_frequency`: inferred from `physical.strategy` + `physical.partition.granularity`
- `sla`: `metadata.sla`
- `business_context`: `conceptual.description`
- `business_rules`: from column `description` and `expression` fields

**`.sql` files**
Read the file and parse:
- `CREATE TABLE <name>` — physical table name becomes the ID
- dbt model files: filename (without `.sql`) becomes the ID; `{{ config(materialized=...) }}` informs `update_frequency`
- Column names, types, and inline comments become `business_rules` candidates
- CTE names are not tables — skip them

**`.py` files**
Read the file and parse:
- SQLAlchemy `class <Model>(Base)`: table name from `__tablename__`; `Column()` definitions for columns
- PySpark `StructType` / `StructField`: extract schema field names and types
- pandas `read_sql('SELECT ... FROM <table>')`: extract table names
- Use class/variable docstrings as `business_context` candidates

**Conflict resolution**: If the same physical table name appears in multiple files, use the **first file** that defined it and note the conflict in the final summary.

### Step 4: Generate spec file for each table

Output path per table:
```
.modscape/specs/<table-id>/spec.md
```

**If the file already exists: skip it.** Do not overwrite.

**If the file does not exist**: create the directory and write the file.

Write using this format:

```markdown
# <table-id>

## Overview
- **Owner**: <metadata.owner, or "—">
- **Update Frequency**: <inferred from physical.strategy + partition, or "—">
- **SLA**: <metadata.sla, or "—">

## Business Context
<conceptual.description, or "—">

## Business Rules
- <derived from column descriptions / expressions, or "—">

## Known Issues / Caveats
- —

## Changelog
- <YYYY-MM-DD>: Bootstrapped from existing implementation (`@modscape-spec-generate`)
```

Fill `<YYYY-MM-DD>` with today's date.

### Step 5: Update model.yaml (if confirmed in Step 2)

If the user confirmed model.yaml updates:
- For tables that exist in model.yaml: skip (do not overwrite existing definitions).
- For tables not yet in model.yaml: add a minimal entry using `modscape table add`.
- Run validate after all additions:
  ```bash
  modscape validate <model.yaml-path>
  ```

### Step 6: Display summary

After processing all tables, output the following summary — always, without exception:

---
✅ `spec:generate` complete.

**Input files scanned:** <list of files>

**spec.md results:**
- Generated: <n> tables — `specs/fct_orders/spec.md`, `specs/dim_customers/spec.md`, ...
- Skipped (already exists): <m> tables — `specs/stg_raw_orders/spec.md`, ...
- Conflicts (first-source used): <list, or "none">

**model.yaml:** <updated / not updated>

> ℹ️ Generated specs contain only information available in the source files.
> Sections marked `—` can be enriched later using the regular SDD flow (`@modscape-spec-requirements` → `@modscape-spec-design`).
---
