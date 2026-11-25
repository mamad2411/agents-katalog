---
name: migration
description: "Database migration workflow. Activated when the user says \"migration\", \"schema change\", \"add column\", \"alter table\", \"database change\", \"migrate\", \"create table\", or wants to make database schema changes safely."
allowed tools: Read, Write, Edit, Grep, Glob, Bash
---

# Migration

Guide safe database schema changes: assess impact, generate up+down migration,
verify reversibility, and create ADR for destructive changes.

## Rules

1. **Every schema change is a migration** — never alter the DB manually
2. **Up AND down** — every migration must be reversible (unless explicitly documented why not)
3. **Zero-downtime by default** — no changes that lock tables or break running queries
4. **ADR for destructive changes** — DROP, column type change, or data loss requires an ADR
5. **Test the migration** — run up, verify, run down, verify, run up again
6. **One concern per migration** — don't mix schema changes with data migrations
7. **Follow naming convention** — `[SPEC]` (e.g., `YYYYMMDDHHMMSS_description.sql`)

## Risk Assessment

Before creating any migration, classify the risk:

| Risk | Examples | Required |
|---|---|---|
| 🟢 **Low** | Add nullable column, add index, create table | Migration + tests |
| 🟡 **Medium** | Add NOT NULL column with default, rename column, add constraint | Migration + tests + team review |
| 🔴 **High** | Drop column/table, change column type, data migration | Migration + tests + ADR + rollback plan |

## Workflow

### Phase 1: Assess
1. Read the PRD/requirement that drives the schema change
2. Check `docs/specs/versioning/` for migration naming and strategy
3. Check `docs/specs/data-architecture/` for modeling conventions
4. List ALL changes needed (don't discover them mid-migration)
5. Classify risk level (🟢/🟡/🔴) for each change

### Phase 2: Design
For each change, document:

```
Change: [what is changing]
Risk: [🟢/🟡/🔴]
Up: [SQL or ORM operation]
Down: [reverse operation]
Zero-downtime: [yes/no — if no, explain why and what the plan is]
Data impact: [rows affected estimate, if relevant]
```

### Phase 3: Generate
1. Create migration file following naming convention: `[SPEC]`
2. Write the **up** migration
3. Write the **down** migration (rollback)
4. If data migration is needed, separate it from schema migration

### Phase 4: Verify
Run the migration cycle:
```bash
# [SPEC] Adapt these commands to your migration tool
1. Run up migration
2. Verify: check schema matches expected state
3. Run down migration (rollback)
4. Verify: check schema is back to original state
5. Run up migration again
6. Run application tests against the new schema
```

### Phase 5: Document
- 🟢 Low risk: migration file + tests are sufficient
- 🟡 Medium risk: add note to PR description with impact assessment
- 🔴 High risk: create ADR in `docs/architecture/` with:
  - Why the destructive change is necessary
  - Data backup strategy
  - Rollback plan with time estimate
  - Communication plan (who needs to know)

## Zero-Downtime Patterns

| Dangerous | Safe alternative |
|---|---|
| Add NOT NULL column | Add nullable → backfill → add constraint |
| Rename column | Add new column → dual-write → migrate reads → drop old |
| Change column type | Add new column with new type → migrate data → drop old |
| Drop column | Stop writing → deploy → stop reading → drop |
| Add unique constraint | Add index CONCURRENTLY first, then add constraint |

## [SPEC] Migration Tool Config
- Tool: [SPEC] (Prisma, Knex, Alembic, Flyway, TypeORM, Django, etc.)
- Naming: [SPEC] (timestamp_description, sequential_number, etc.)
- Directory: [SPEC] (migrations/, db/migrations/, prisma/migrations/)
- Run command: [SPEC]
- Rollback command: [SPEC]

## References
- `docs/specs/versioning/` — migration naming, reversibility rules
- `docs/specs/data-architecture/` — modeling conventions
- `docs/architecture/` — ADRs for past schema decisions
