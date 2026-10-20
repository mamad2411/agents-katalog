---
description: Phase 5 helper for w-task — write database/<NN>-<module>.md + sub-ERD .puml when DB changes occur. MANDATORY syncs the master ERD on every sub-ERD change — a stale master ERD is considered worse than none.
argument-hint: <task-slug>
allowed-tools: Bash, Read, Write, Edit
---

# w-db-doc

Persist database schema documentation per module with PlantUML ERD pipeline.
Updates module schema doc + sub-ERD + master ERD atomically — never leaves the
master ERD lagging behind sub-ERDs.

Reads `.claude/workflow.yaml`:
- `workflow.db_docs_root`
- `workflow.diagrams_root`
- `workflow.master_erd_path`
- `project.schema_paths.prisma`

Input: `<state_root>/<task-slug>/impact.md` § Database Changes.

---

## Step 1 — Preconditions

Abort silently if:
- `db_docs_root` is null, OR
- impact.md has no § Database Changes section / it is empty.

Required: `master_erd_path` MUST be set if `diagrams_root` is set — otherwise
abort with error: "Diagrams root configured without master_erd_path. Run /w-setup
to fix — master ERD sync is mandatory."

---

## Step 2 — Parse DB changes

From impact.md § Database Changes, extract:
- New models / tables (entity + columns + indexes + FKs)
- Modified columns (rename, type change, nullable change)
- Dropped columns
- New indexes / unique constraints
- Migration name (if specified)

Cross-reference with `project.schema_paths.prisma` if set — read current
schema.prisma to ground the column types.

---

## Step 3 — Update module schema doc

Path: `<db_docs_root>/<NN>-<module>.md`

If absent, create with template:
```markdown
# Database — <module>

## Tables

## Invariants

## Migration history
```

For each new/changed table, write/replace its subsection:
```markdown
### <table_name>
**Purpose:** <one line>

| Column | Type | Constraints | Purpose |
|--------|------|-------------|---------|
| id | uuid | PK | |
| ... | ... | ... | ... |

**Indexes:**
- <name>: <columns> (<unique?>)

**FKs:**
- <column> → <ref_table>.<ref_column>

**Invariants:**
- <e.g. soft-delete only, append-only ledger>
```

Append to § Migration history:
```
| <YYYY-MM-DD> | <task-slug> | <migration name or "schema change"> |
```

---

## Step 4 — Update sub-ERD

Path: `<diagrams_root>/<NN>-<module>-erd.puml`

If absent, create:
```plantuml
@startuml <NN>-<module>
!define table(x) entity x as "x"
hide circle
skinparam linetype ortho

' Entities for module: <module>

@enduml
```

For each new/changed table, add or replace its entity block:
```plantuml
table(<name>) {
  + id : uuid <<PK>>
  + <col> : <type> [<constraints>]
  ...
}
```

For each FK, add relationship:
```plantuml
<table> }|--|| <ref_table>
```

---

## Step 5 — MANDATORY master ERD sync

Path: `<master_erd_path>` (e.g. `00-database-overview-erd.puml`).

For EACH entity touched in Step 4:
- If entity NOT already in master ERD: add an entity stub (PK + FKs only — not
  full column list).
- If entity exists: update only PKs/FKs, leave the stub line otherwise.

For EACH cross-module FK introduced: add the relationship arrow at master level.

Do not skip this step. A sub-ERD update without master-ERD update is considered
broken state and w-doc-gate will block PR creation.

---

## Step 6 — Update database README index (if exists)

If `<db_docs_root>/README.md` exists and contains an index table of module docs,
add a row for the new `<NN>-<module>.md` file (skip if already listed).

---

## Step 7 — Confirm

Print:
```
DB docs updated:
  Module doc:  <db_docs_root>/<NN>-<module>.md
  Sub-ERD:     <diagrams_root>/<NN>-<module>-erd.puml
  Master ERD:  <master_erd_path>  (REQUIRED — synced)

Run `make diagrams` (or your project's PlantUML pipeline) to regenerate PNGs.
Review files before /w-task advances Phase 5.
```
