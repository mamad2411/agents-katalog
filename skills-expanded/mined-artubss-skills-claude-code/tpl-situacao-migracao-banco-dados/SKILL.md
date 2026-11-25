---
name: tpl-situacao-migracao-banco-dados
description: Template do pack (situacao/02-migracao-banco-dados.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/02-migracao-banco-dados.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Database Migration

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/02-migracao-banco-dados.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when making schema changes (adding/removing columns, renaming tables, changing data types, adding constraints, migrating data between tables) on a production database. This applies whether using Postgres, MySQL, SQLite, MongoDB or any other database. The primary risk is data loss and downtime — this configuration eliminates both when followed correctly.

## OBJECTIVES
- Achieve schema changes with zero data loss
- Maintain application availability during migration
- Have a verified rollback path before executing forward migration
- Validate data integrity before and after every migration step
- Keep migration scripts idempotent and version-controlled

## APPROACH RULES

1. **Expand-Contract Pattern (required for production).** Never rename a column in one step. Expand first (add the new column), contract later (remove the old one) after all application code has been updated and deployed. Steps: ADD new column → backfill data → deploy app that writes to both → verify → remove old column.

2. **Every migration must have a rollback script.** Write the down migration before running the up migration. If you cannot write a rollback (e.g., irreversible data transformations), document exactly why and get explicit sign-off.

3. **Backfill in batches, never in one statement.** `UPDATE large_table SET ...` with millions of rows will lock the table. Use batch updates of 1,000–10,000 rows with a small sleep between batches.

4. **Test migration on staging with production data snapshot.** Never run a migration for the first time on production. Always confirm timing and row counts on staging first.

5. **Validate before completing.** After migration: check row counts match expected, verify NULL/NOT NULL constraints satisfied, run application smoke tests before announcing done.

6. **Version all migrations.** Use sequential numbering (001, 002...) or timestamps. Never edit an already-applied migration file — create a new one.

7. **Foreign key changes need special handling.** To add a FK constraint: add the column nullable first → backfill → verify all values are valid → add constraint → make NOT NULL if needed. Never add FK constraint and NOT NULL in one step.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Column rename | Use Expand-Contract: add new column, backfill, update app code, verify, drop old column (3 separate deployments) |
| Table rename | Create a view with the old name pointing to new table; update all app references; remove view in final step |
| Adding NOT NULL column | Add as nullable → backfill all rows → add NOT NULL constraint → add DEFAULT if needed |
| Removing a column | Remove from application code first (deploy) → wait one release cycle → drop column from schema |
| Large table (1M+ rows) | Use `pt-online-schema-change` (MySQL) or `pg_repack` (Postgres). Never `ALTER TABLE` directly |
| Data type change (e.g., int → bigint) | Add new column with new type → backfill → switch app → drop old |
| Adding unique constraint | Check for duplicates first with a query. If duplicates exist, resolve them before adding constraint |
| Dropping a table | Rename to `_archived_tablename` first, keep for 30 days, then drop |
| Migration takes > 5 seconds on staging | Reconsider approach — find a batched or online solution |
| Schema diff between environments | Always diff staging vs production before running migration. Use `pg_dump --schema-only` |

## DO NOT

- **DO NOT** run `ALTER TABLE` on large tables during business hours without an online schema change tool
- **DO NOT** write a migration that depends on application code that hasn't been deployed yet
- **DO NOT** deploy new application code that depends on a migration that hasn't run yet
- **DO NOT** truncate or drop tables without confirmed backups
- **DO NOT** mix schema changes and data changes in the same migration script
- **DO NOT** use `CASCADE` on DROP without listing exactly what will be affected
- **DO NOT** edit a migration file that has already been applied to any environment
- **DO NOT** assume rollback is possible after dropping a column — verify backup strategy first

## OUTPUT FORMAT

For each migration, produce:

**Migration Plan Document** covering:
```
Migration: [description]
Ticket: [link]
Author: [name]
Date: [date]

RISK LEVEL: Low / Medium / High / Critical

FORWARD MIGRATION:
1. Step-by-step procedures
2. Expected duration on staging
3. Row counts before/after

ROLLBACK PLAN:
1. Step-by-step rollback
2. Decision point: when to rollback
3. Estimated rollback time

VALIDATION QUERIES:
-- Before migration
SELECT COUNT(*) FROM affected_table;

-- After migration
SELECT COUNT(*) FROM affected_table WHERE new_column IS NOT NULL;

DEPLOYMENT ORDER:
[ ] 1. Run migration script
[ ] 2. Verify validation queries
[ ] 3. Deploy application version X.Y.Z
[ ] 4. Smoke test endpoints
[ ] 5. Monitor error rate for 15 minutes
```

## QUALITY GATES

- [ ] Rollback script written and tested on staging before forward migration runs
- [ ] Migration tested on a snapshot of production data (not just seed data)
- [ ] Batch sizes specified for any UPDATE/INSERT affecting > 10,000 rows
- [ ] All FK constraints validated with a query before being added
- [ ] Zero downtime verified: no exclusive table locks for more than 100ms
- [ ] Migration script is idempotent (can be run twice without error)
- [ ] Validation queries defined and results documented
- [ ] Database backup confirmed before production migration
- [ ] Timing logged: how long did migration take on staging?
- [ ] Application smoke tests pass after migration in staging
