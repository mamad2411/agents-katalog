---
name: schema-diff
description: Diff the ORM entities against the actual DB schema — catch drift between code and reality. Run before generating a new migration (drift corrupts autogenerate output), after an out-of-band hotfix, and weekly in CI against a restored backup. Detects drift only — `migration-rehearsal` is what proves the corrective migration is safe to apply.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# schema-diff

When migrations are skipped, hand-edited on prod, or entities change without a generated migration, the ORM and DB drift. This skill catches it.

## Premise

Find real drift, cite `<table>.<column>` and the file/line in the entity definition. Every finding maps to a concrete artifact: a column visible in `pg_dump` output, an entity field in `prisma/schema.prisma:NN`, an index declared in `*.entity.ts:NN`. No "looks like drift" — either the diff tool emits it or it's not reported. Verdicts (blocker / warning / info) come from the captured diff, not from intuition about the ORM.

## Halt conditions

- Refuse to report drift without both sides captured (`$RUN/db.sql` or the static mode's schema map, AND the ORM expected schema). `RUN=$(mktemp -d "${TMPDIR:-/tmp}/schema-diff.XXXXXX")`: never a fixed temp-dir path (two runs overwrite each other) and never a file inside the repo.
- Refuse to flag a "ghost column" without confirming via `\d <table>` that it actually exists.
- Halt if the target DB is prod — re-run against a restored snapshot.
- Don't propose `db push` / destructive sync as the fix; propose a generated migration with the exact name.

## When to use

- Before generating a new migration — drift corrupts autogenerate output.
- After a prod incident where queries returned unexpected null/missing columns.
- Weekly in CI against a restored backup.
- After a hotfix that touched the DB out-of-band.

## Prerequisites

- Read access to the target DB (DEV or STAGING — never prod directly).
- The ORM CLI for your stack: `prisma`, `typeorm`, `alembic`, `drizzle-kit`, `sea-orm-cli`.
- `psql` / `mysql` client for raw introspection.

## Procedure

1. Snapshot the live schema:
   ```bash
   RUN=$(mktemp -d "${TMPDIR:-/tmp}/schema-diff.XXXXXX")
   # Postgres
   pg_dump --schema-only --no-owner --no-privileges "$DATABASE_URL" > "$RUN/db.sql"
   # MySQL
   mysqldump --no-data --skip-comments -h $H -u $U -p $DB > "$RUN/db.sql"
   ```
2. Generate the ORM's expected schema:
   ```bash
   # Prisma — the project's own CLI; absent → NOT-RUN (prisma not installed — to enable: npm i -D prisma)
   npx --no prisma migrate diff --from-schema-datamodel prisma/schema.prisma --to-schema-datasource "$DATABASE_URL" --script
   # TypeORM — absent → NOT-RUN (typeorm not installed — to enable: npm i typeorm)
   npx --no typeorm schema:log -d ./database/data-source.ts
   # Alembic / SQLAlchemy
   alembic revision --autogenerate -m "drift-check" --sql > /tmp/diff.sql && rm -f migrations/versions/*drift-check*
   ```
3. Diff per table — categorize each finding:
   - Column in entity, missing in DB → **migration needed** (deploy will fail).
   - Column in DB, missing in entity → **ghost column** (ORM ignores it; data may rot).
   - Type mismatch (`DECIMAL(10,2)` vs `NUMERIC`) → check semantic equivalence.
   - Missing index declared in entity → query performance regression.
   - Missing FK / CHECK / NOT NULL → integrity hole.
4. Categorize each finding as blocker (deploy will fail), warning (perf/integrity), or info (cosmetic).

## Static mode (no database reachable)

`/db-audit` runs this skill on repos with no database in reach. Two lines run first, from the repo root:

```bash
# S1. The project's own drift gate: a test that compares the migrated schema with the entities, and its accepted-drift list.
rg -l --pcre2 'SchemaComparator|getUpdateSchemaSQL|migration:check|migrate\s+diff[^\n]*--exit-code|makemigrations\s+--check|alembic\s+check|KNOWN_DRIFT|schema:log' -g '!**/node_modules/**' -g '!**/dist/**' -g '!*.md' .
# S2. MikroORM: the entity decorators against the snapshot plus the migrations after its horizon (schema-map.py --entities).
SM=.claude/skills/index-coverage-scan/scripts/schema-map.py; if command -v python3 >/dev/null 2>&1 && [ -f "$SM" ]; then python3 -I -B "$SM" . --entities; else echo 'S2 NOT-RUN (python3 or schema-map.py absent)'; fi
```

- **S1 hit:** the project already gates drift. Read the test and its accepted list (`KNOWN_DRIFT` or the like). Its pass or fail needs a database, so the live row stays `not run`, but every static row below that the list names is `accepted (<file:line>)`, not drift. A test that exists but is excluded from CI is the finding.
- **S2** prints the snapshot's horizon (see `index-coverage-scan` § "Pre-flight (static lane)" H0), then one row per difference: `MISSING-TABLE` / `MISSING-COLUMN` (the entity maps what the schema lacks: a deploy-time failure), `NULLABLE`, `GHOST-COLUMN` / `GHOST-TABLE` (only the schema has it), `MISSING-INDEX` (a named `@Index` / `@Unique` the schema lacks). Without the replay, every column added by a hand-written migration after the snapshot reads as `MISSING-*`: the horizon line is the first thing to check. Other ORMs: diff the schema map (`schema-map.py .`, the `ddl` lane) against the model files by reading; the live procedure below stays the oracle.
- **Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, 376 migrations, snapshot 5 files behind HEAD): the snapshot alone gave 19 rows, 8 of them `MISSING-*` for columns and tables the 5 later migrations add; with the replay, 6 rows (5 ghost columns, 1 ghost table), and S1 found the project's own comparator test whose `KNOWN_DRIFT` names all 6 → 0 drift findings. A property under a `// prettier-ignore` comment and a `tableName:` given as a constant were the two parser misses fixed on that run.

## Output

```
Schema drift — orders table  (<target-db> vs <schema-source>)

  + order_ref_id  TEXT NOT NULL     entity has it, DB missing — migration needed
  - legacy_notes  TEXT               DB has it, entity doesn't — ghost, either use or drop
  ~ price         DECIMAL(10,2) vs NUMERIC   semantically equivalent — OK
  ! index (tenant_id, created_at)    declared in entity, missing in DB

Verdict: 1 blocker (missing column), 1 ghost, 1 missing index.
Run: <the project's own generate command, from the detected tool — see below>
```

**Emit the fix command in the project's tool, never a default one.** The prerequisites name several; pick the one this repo actually uses (from `.claude/codebase-profile.md` / the migration folder) and print its command:

| Tool | Generate |
|---|---|
| Prisma | `npx --no prisma migrate dev --name <slug>` |
| TypeORM | `pnpm migration:generate -- src/migrations/<Name>` |
| Alembic | `alembic revision --autogenerate -m "<slug>"` |
| Django | `python manage.py makemigrations` |
| Rails | `rails generate migration <Name>` |
| Laravel | `php artisan make:migration <slug>` |
| Raw (Flyway / goose / sqlx) | write the `up`/`down` pair by hand |

If the tool cannot be determined, print the DDL the drift implies and say the tool was not detected — do not guess a command the reader will paste.

## False positives / gotchas

- Postgres `serial` vs `integer GENERATED BY DEFAULT AS IDENTITY` — same behavior, different DDL — not real drift.
- TypeORM emits `varchar(255)` even when the entity didn't specify length — may match `text` columns semantically.
- Generated columns and partial indexes are often missed by autogenerate — verify by hand.
- Ghost columns may be intentional (kept for backfill or audit) — confirm with the team before proposing DROP.
- NEVER "fix" drift on prod with a schema-push command (`prisma db push`, `synchronize: true`, `db.create_all()`) — they are destructive and skip migration history. Drift is closed by a reviewed migration, always.
- A generated migration is a **draft**: autogenerate reads a shape difference, not an intent. A rename looks identical to a drop plus an add, and it will emit the destructive pair. Read the SQL and route it through `/migration-review`.

## Baseline registration

The procedure above compares the ORM with a **live** database. A behavioural baseline compares the schema with a **stored** snapshot instead, never with the live DB (proposal §7, kind `schema`), so the comparison needs no database in reach and P5 can capture it at the base sha:

```bash
bash .claude/scripts/baseline-capture.sh register --id=schema-main --kind=schema \
  --engine=database/schema-diff --scope='prisma/**,src/**/*.entity.*,migrations/**' \
  --command='npx --no prisma migrate diff --from-empty --to-schema-datamodel prisma/schema.prisma --script > "$REFRACT_BASELINE_OUT/schema.sql"' \
  --artifact=db/schema.snapshot.sql --compare=file --cadence=pr
```

- The command emits the schema the code declares with no database in reach: Prisma as above, or Alembic's offline `alembic upgrade head --sql`. A repo that already commits a dump its migrations maintain (`db/structure.sql`, `db/schema.rb`) points `--artifact` at that file and adds `--no-capture`, with a command that copies it into `$REFRACT_BASELINE_OUT`. Otherwise the registration's capture writes `db/schema.snapshot.sql` once, and you commit it.
- **Gate G14**: a quick kind. It re-runs at Stop when an entity or migration is touched and in full in CI, and P5 captures it. An unplanned difference is drift the run did not declare.
- A migration that changes the schema on purpose is declared by an acceptance criterion, `changes_baseline: ["schema-main"]`. Re-writing the snapshot with no criterion naming it fails `test-integrity.py` (`undeclared-baseline-rewrite`).
