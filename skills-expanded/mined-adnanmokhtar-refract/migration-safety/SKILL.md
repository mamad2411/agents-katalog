---
name: migration-safety
description: Migration safety detector — blocking index builds, table rewrites, NOT NULL and constraints validated under the table lock, same-deploy drops and renames the running release still reads, missing lock timeouts, data inside DDL, irreversible steps, edited applied migrations. Linter lanes plus a safe / safe-with-pattern / unsafe op-class per engine and version.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: migration-safety

## Premise

A migration runs once, on deploy, against a populated database under live traffic. Two questions decide every statement in it: **what lock it takes, and for how long, on this engine at this version** (its operation class), and **whether the release still serving traffic when it lands can live with the result** (N-1 compatibility). A linter answers the first question one statement at a time. It cannot see the table's row count, the runner's transaction wrapping, the code that still reads a dropped column, or the deploy order. Those are what this skill reads.

**Every finding cites the migration at `<file:line>` + the statement + its op class with the engine and version that assign it + the table-size rung + the safe rewrite.** A grep or linter hit is never a finding by itself. "The migrations are safe" is never printed without the class coverage block (§ Output). This is the static detector. The execution proof is [`migration-rehearsal`](../migration-rehearsal/SKILL.md) (a restored copy, a lock observer, a timed run). The builder is `/add-migration`. `/migration-review` dispatches this skill and prints its class lines.

## The operation-class rule

Each statement gets one class, read from the engine and version (refute-before-report gate 3), **never from a row count**. Row count decides only whether the table is populated and how long a scan or rewrite runs.

| Class | Meaning on this engine + version | Finding when |
|---|---|---|
| **safe** | No rewrite, no long scan under a write-blocking lock; writes continue | Never by its class. §4 and §6 still apply |
| **safe-with-pattern** | Blocks or fails as one statement on a populated table; a named pattern makes it online | Written without the pattern on a populated or unresolved-size table |
| **unsafe** | No online form here: a rewrite or copy that blocks writes | Shipped on a populated table without an expand-contract, an online-schema-change tool, or an ADR'd window with a measured hold |
| **unknown** | Engine or version unresolved, or no row below (MariaDB, SQL Server, CockroachDB, SQLite rebuilds) | Always `[report-flagged]`; never cleared |

They map onto `/add-migration`'s numbered classes: class 1 is safe; class 2 is safe or safe-with-pattern; class 3 is unsafe when it blocks writes and safe when the engine permits writes through it (an InnoDB INPLACE rebuild).

| Statement | Postgres ≥ 11 | MySQL InnoDB ≥ 8.0 |
|---|---|---|
| `ADD COLUMN` nullable, or a **non-volatile** default (a constant, `now()` / `current_timestamp`, which are STABLE) | safe — default kept in the catalog, no rewrite | safe — INSTANT (last position from 8.0.12, any position from 8.0.29; 8.0.29 was withdrawn, use 8.0.30+). Falls back to an INPLACE rebuild (writes continue) on `ROW_FORMAT=COMPRESSED`, a FULLTEXT index, or the row-version cap (64 on 8.x, 255 from 9.1) |
| `ADD COLUMN` with a volatile default (`clock_timestamp()`, `random()`, `gen_random_uuid()`), a STORED generated column, an identity / serial column | unsafe as written → safe-with-pattern: add with no default, `SET DEFAULT`, batched backfill. A PG 18 virtual generated column never rewrites | STORED generated: COPY only → unsafe. Auto-increment column: no concurrent DML → unsafe |
| `ADD COLUMN … NOT NULL` with no default, populated table | fails on existing rows → safe-with-pattern: nullable → backfill → §3 | same |
| `SET NOT NULL` | safe-with-pattern: `CHECK (c IS NOT NULL) NOT VALID` → `VALIDATE` → `SET NOT NULL` (a valid CHECK skips the scan, PG ≥ 12). PG 18: `ADD CONSTRAINT … NOT NULL c NOT VALID` → `VALIDATE` | safe — INPLACE rebuild, concurrent DML permitted; needs strict mode, fails on NULLs, so backfill first |
| B-tree `CREATE INDEX` / `ADD INDEX` | safe-with-pattern: `CONCURRENTLY`, outside any transaction, alone in its file; a failed build leaves an `INVALID` index (`IF NOT EXISTS` does not repair it) | **safe** — INPLACE, no rebuild, concurrent DML permitted. Write `ALGORITHM=INPLACE, LOCK=NONE` |
| FULLTEXT / SPATIAL index | GIN / GiST: as the row above | unsafe — no concurrent DML; the first FULLTEXT index rebuilds the table unless `FTS_DOC_ID` exists |
| `UNIQUE` / `PRIMARY KEY` as a constraint | safe-with-pattern: `CREATE UNIQUE INDEX CONCURRENTLY` → `ADD CONSTRAINT … USING INDEX` (a PK on nullable columns first scans for NULLs) | `ADD PRIMARY KEY`: INPLACE rebuild with DML (strict mode). `DROP PRIMARY KEY` alone: COPY → unsafe |
| `DROP INDEX` / `REINDEX` | safe-with-pattern: `DROP INDEX CONCURRENTLY`, `REINDEX … CONCURRENTLY` | safe |
| `ADD FOREIGN KEY` / `ADD CHECK` | safe-with-pattern: `NOT VALID`, then `VALIDATE CONSTRAINT` in a separate transaction (`SHARE UPDATE EXCLUSIVE`, plus `ROW SHARE` on the referenced table) | FK: COPY while `foreign_key_checks` is on → unsafe; INPLACE only with checks off, which verifies no existing row — the anti-join recipe in `/add-migration` § Add FK on a populated table. CHECK: scans every row, no `NOT VALID` |
| `ALTER COLUMN TYPE` | unsafe, except binary-coercible changes (widen or drop a `varchar` limit, `varchar ↔ text`, numeric precision up at the same scale, `timestamp ↔ timestamptz` with a UTC session). `int → bigint` always rewrites. A collation change still rebuilds indexes | unsafe (COPY only), except extending a `VARCHAR` within its length-byte class (INPLACE) |
| `RENAME COLUMN` / `RENAME TABLE`, `DROP COLUMN` / `DROP TABLE` | safe for the lock; §4 decides | rename INSTANT from 8.0.28, drop INSTANT from 8.0.29; §4 decides |
| Backfill `UPDATE` / `INSERT … SELECT` | safe-with-pattern: batched, outside the DDL transaction, throttled, resumable (§7) | same; an INPLACE DDL replicates as one statement, so replicas lag by its whole duration |
| `VACUUM FULL`, `CLUSTER`, `SET LOGGED/UNLOGGED`, `CONVERT TO CHARACTER SET` | unsafe — `pg_repack` / `pg_squeeze`; PG 19 `REPACK (CONCURRENTLY)` is in beta | `CONVERT TO CHARACTER SET` blocks DML → unsafe |

Every class, safe included, takes a short exclusive lock to swap the definition (Postgres `ACCESS EXCLUSIVE` for most `ALTER TABLE` forms; MySQL an exclusive metadata lock at the start and end). Behind one long transaction, that request queues every later query on the table. That is §6, whatever the class. Sources: PostgreSQL 18 `ALTER TABLE` § Notes and *Function Volatility Categories*; MySQL 8.4 online-DDL operations table (§17.12.1; the 8.0, 9.7 and 26.7 manuals match), all fetched 2026-10-02. A MySQL version below 8.0 or any MariaDB is `unknown` until that version's own DDL table is read.

**MySQL secondary indexes — settled.** An earlier backend copy of this skill required `pt-online-schema-change` / `gh-ost` for every MySQL index build, which contradicted `/add-migration` and [`precedents/data.md`](../../../../snippets/precedents/data.md) precedent 14. The engine documentation decides: on InnoDB, MySQL ≥ 8.0, a B-tree secondary index is INPLACE with concurrent DML. It is not a finding when written with `ALGORITHM=INPLACE, LOCK=NONE` (so an unsupported case errors instead of silently copying) and `lock_wait_timeout` set. An online-schema-change tool (gh-ost, pt-osc, Spirit) earns its place for a COPY-only change, for throttling or pausing a long build, or for replica lag. "Native ALTER locks" is not a reason; flag a migration comment that gives it.

## Resolving table size

A migration file holds no row count. Resolve it, record the rung, and never assume "probably small":

| Rung | How | Confidence |
|---|---|---|
| Reachable non-prod or prod-shaped DB | PG `SELECT reltuples::bigint FROM pg_class WHERE relname = '<t>';` · MySQL `SELECT table_rows FROM information_schema.tables WHERE table_name = '<t>';` (an InnoDB estimate, order of magnitude) | Good |
| A dated profile in `ai/` naming the large tables | Cite `<path:line>` | Good if dated |
| Migration history | The table is created in this migration or this unreleased diff | Conclusive for empty only |
| Nothing | — | **Unknown → treat as populated, `[report-flagged]`** |

A threshold of 100,000 rows separates "milliseconds" from "a queue of writers" as a **starting point** only. Replace it with the crossover from one timed `migration-rehearsal` build on this system.

## Boundaries

- ORM auto-sync reachable in production (`synchronize: true`, `prisma db push`, `ddl-auto=update`, MikroORM `updateSchema()` at boot) → `schema-integrity-scan` §8. Entity-vs-database drift → `schema-diff`. Convention drift across tables → `schema-consistency-audit`. A missing natural-key unique constraint → `schema-integrity-scan` §3.
- Whether a new index pays for its writes → `ai/patterns/indexing-strategy.md` and `@query-optimizer`. Which access path lacks an index → `index-coverage-scan`.
- A migration runner callable from a request path → `injection-scan` grep 2c, when the security pack is installed; without it, list the call site under §9's history and say the class went unread.
- Timing, the lock observer and the rollback diff → `migration-rehearsal`. This skill never prints a duration.

## Adapt to the codebase

Read the engine and version, the ORM and migration runner, and the deploy controls with [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2's context block, once per run. Then read the runner's transaction wrapping, which decides whether `CONCURRENTLY` (and every other non-transactional statement) can run at all:

| Runner | Wraps by default | Opt-out for a non-transactional statement | Read from (2026-10-02) |
|---|---|---|---|
| **MikroORM** (NestJS / Fastify / Express) | each migration (`transactional: true`) **and** the whole run in one master transaction (`allOrNothing: true`) | `isTransactional() { return false; }` **plus** `allOrNothing: false`. With the default, the build runs on another pooled connection while the master transaction stays open: it waits on the migrator's own session, or cannot see tables the batch created | docs 7.2; source v7.2.3 (`MigrationRunner.ts`, `AbstractMigrator.ts`); both failures recorded in a real 6.6 monorepo's migrator config |
| **TypeORM** 1.x | the whole run (`migrationsTransactionMode: "all"`) | mode `"each"` or `"none"` plus `transaction = false` on the class | source 1.1.1 `MigrationInterface.ts` |
| **Knex** | each migration | `exports.config = { transaction: false }`, or `disableTransactions` | knexjs.org migrations guide |
| **Sequelize** | not verified | `addIndex(t, cols, { concurrently: true })`; read any `sequelize.transaction(` around it | source `query-generator.js` |
| **Prisma** 7 / **Drizzle** | not verified | run the file through the real runner on a scratch DB, then `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;`. Prisma 8 (RC) runs a whole `db migrate` in one transaction: no `CONCURRENTLY` | research 2026-10-02 |
| **Django** | `atomic = True` on Postgres and SQLite | `atomic = False` + `AddIndexConcurrently` | docs 6.1 |
| **Alembic** (SQLAlchemy) | per `env.py` | `with op.get_context().autocommit_block():` + `postgresql_concurrently=True` (commits the work before it unconditionally); `transaction_per_migration = True` | docs |
| **Rails** (ActiveRecord) | each migration | `disable_ddl_transaction!` + `algorithm: :concurrently` | strong_migrations README |
| **Laravel** (Eloquent) | `$withinTransaction = true` where the grammar supports schema transactions | `public $withinTransaction = false;` | framework 13.x source |
| **Ecto** | each migration, under a migration lock | `@disable_ddl_transaction true` + `@disable_migration_lock true` + `concurrently: true` | excellent_migrations danger types |
| **goose** / **golang-migrate** (Go, GORM) | goose: each file; golang-migrate (PG): a multi-statement file runs as one implicit transaction | goose `-- +goose NO TRANSACTION`; golang-migrate: the statement alone in its file | goose README v3.28.0; postgres driver README v4.20.1 |
| **Flyway** (Spring, Hibernate/JPA) | per script, with a parser that runs a non-transactional statement outside one | `executeInTransaction=false` in `<script>.sql.conf`; mixing both kinds in one file needs `mixed` | flyway-core source 13.9.0 |
| **Atlas** | per file | `-- atlas:txmode none` | research |

Linter lanes — run the one that matches the runner; a linter decides the statement, the read layer decides the rest:

| Lane | Files | Linter + command | Blind to |
|---|---|---|---|
| Postgres SQL (Flyway, goose, golang-migrate, dbmate, Prisma, Drizzle, Supabase, Atlas) | `*.sql` | `squawk --pg-version=<major> <files>` (installed only: `node_modules/.bin`, then PATH; to enable: `npm i -D squawk-cli@2.66.0`) | size, wrapping it is not told about, goose `Down` sections, N-1 |
| TS / JS (MikroORM, TypeORM, Knex, Sequelize) | `migrations/*.ts` | lift the SQL (§ Linter lane), then squawk | SQL assembled at runtime → `syntax-error`; those files go to the read lane |
| Django | `<app>/migrations/*.py` | `python manage.py lintmigrations --git-commit-id <base> --warnings-as-errors` (django-migration-linter 6.0.0); `python manage.py sqlmigrate <app> <n> \| squawk --stdin-filepath <app>/<n>.sql` (no `--assume-in-transaction`: sqlmigrate prints BEGIN/COMMIT) | `ALTER_COLUMN` on compatible alters; a correct drop still needs an ignore |
| Alembic | `versions/*.py` | `alembic upgrade <from>:<to> --sql \| squawk` | renames autogenerated as drop + add |
| Rails | `db/migrate/*.rb` | strong_migrations 2.8.0 / online_migrations 0.36.1 raise at `bin/rails db:migrate` on a scratch DB | backfills (not detected); `execute` always needs `safety_assured` |
| Ecto | `priv/repo/migrations/*.exs` | `mix excellent_migrations.check_safety` | raw SQL |
| Laravel | `database/migrations/*.php` | none found → the grep and read lanes | — |
| MySQL, any runner | — | no free statement-level online-DDL linter: `atlas migrate lint` is Atlas Pro since v0.38; `spirit lint --source-dsn …` needs a live MySQL 8.0+ → the op-class table and grep 2a's `ALGORITHM=` read | everything the class table names |

Measured on squawk 2.66.0 (2026-10-02): the `gcc` reporter counts lines **from 0** (add 1); `ban-concurrent-index-creation-in-transaction` fires on an explicit `BEGIN … COMMIT` but **not** under `--assume-in-transaction` (so grep 1c, not the linter, owns runner wrapping); `require-lock-timeout` and `require-statement-timeout` fired without `--include`; `--pg-version` defaults to 15. The type-hygiene rules (`prefer-text-field`, `prefer-bigint-over-int`, `prefer-identity`) are excluded: they are style here (precedent 20), and `schema-integrity-scan` §7 owns int keys.

## Pre-flight greps

Run as **one** script from the repo root (`X`, `NC`, `UP`, `NEW` and `MIG_PATHS` must live in the same invocation). `DIFF=1 BASE=origin/main` scopes it to the migrations this branch adds or edits, `FILES="<path> <path>"` to named files; with neither, every migration. Every `rg` names its paths — `"${MIG_PATHS[@]}"` or `.`; given no path, rg reads stdin under a pipe and reports a false zero. Lane absence comes from the lane count the block prints first, never from a quiet grep. `UP` drops hits inside reversal bodies (`down`, `downgrade`, goose `Down`, `*.down.sql`); `NEW` drops statements on tables created in the same file (in the same diff under `DIFF=1`) and prints how many, which the coverage line counts as precedent 12.

```bash
BASE="${BASE:-origin/main}"; T="$(mktemp -d "${TMPDIR:-/tmp}/migsafe.XXXXXX")"
MIGRE='(^|/)(migrations?|db/migrate|alembic/versions|db/changelog|supabase/migrations|drizzle)/'
SKIP='(^|/)(node_modules|vendor|dist|build|target|\.venv|__pycache__|tests?|specs?|__tests__|__mocks__|testdata)/|\.(md|mdx|json|snap|lock|pyc)$|\.d\.ts$|[._](test|spec)\.'
if [ -n "${FILES:-}" ]; then printf '%s\n' "$FILES" | tr ' ' '\n' > "$T/files"; else
{ if [ "${DIFF:-0}" = 1 ]; then git diff --name-only --diff-filter=AMR "$BASE"...HEAD; git ls-files --others --modified --exclude-standard
  else git ls-files --cached --others --exclude-standard; fi; } | sort -u | rg -i "$MIGRE" | rg -v -i "$SKIP" > "$T/files"; fi
MIG_PATHS=(); while IFS= read -r f; do [ -f "$f" ] && MIG_PATHS+=("$f"); done < "$T/files"
[ ${#MIG_PATHS[@]} -gt 0 ] || { echo "no migration files in scope — every class N/A (no migration in this scope)"; exit 0; }
for e in sql ts js py rb php exs cs xml yaml; do printf '%-5s %s\n' "$e" "$(rg -c -i "\.$e\$" "$T/files" || echo 0)"; done   # 0 = lane absent
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!*.{md,mdx,json,snap,lock}'
   -g '!**/{test,tests,spec,e2e,__tests__,__mocks__,__fixtures__,testdata}/**' -g '!**/*{.,_}{test,spec}.*' -g '!**/{migrations,migration,migrate,versions}/**' -g '!**/docs/**' -g '!/ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#(?!\{)|<!--|--(?!\s*\+goose|\s*migrate:|\s*atlas:))')   # drops comment-only lines
awk 'FNR==1{d=(FILENAME ~ /\.down\.sql$/)} /(^|[^[:alnum:]_.])down[ \t]*\(|def[ \t]+(down|downgrade)[ \t(:]|exports\.down|-- \+goose Down|-- migrate:down/{d=1}
     /(^|[^[:alnum:]_.])up[ \t]*\(|def[ \t]+(up|upgrade|change)[ \t(:]|exports\.up|-- \+goose Up|-- migrate:up/{d=0} d{print FILENAME":"FNR}' "${MIG_PATHS[@]}" > "$T/down"
UP=(awk -F: 'FILENAME==ARGV[1]{d[$1":"$2];next} !(($1":"$2) in d)' "$T/down" -)
cat > "$T/new.py" <<'PY'
import os, re, sys
diff, files = os.environ.get("DIFF") == "1", sys.argv[1:]
CT = re.compile(r'(?i)\bcreate\s+table\s+(?:if\s+not\s+exists\s+)?([\w."`]+)|\bcreate_table\s+[:"\x27]([\w.]+)|'
                r'Schema::create\(\s*["\x27]([\w.]+)|\bcreateTable\(\s*["\x27`]([\w.]+)|\bop\.create_table\(\s*["\x27]([\w.]+)')
TB = re.compile(r'(?i)(?:\balter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?|\bon\s+(?!delete\b|update\b)(?:only\s+)?|\badd_index\s+:|'
                r'Schema::table\(\s*["\x27]|\balterTable\(\s*["\x27`])([\w."`]+)')
norm = lambda t: t.split(".")[-1].strip("\"`'").lower()
src, made = {}, {}
for f in files:
    try: src[f] = open(f, encoding="utf-8", errors="replace").read().split("\n")
    except OSError: continue
    made[f] = {norm(next(g for g in m.groups() if g)) for m in CT.finditer("\n".join(src[f]))}
every, dropped = set().union(*made.values()) if made else set(), 0
for hit in sys.stdin:
    f, n = (hit.split(":", 2) + ["", ""])[:2]
    k = int(n) if f in src and n.isdigit() else 0
    stmt = "\n".join(src[f][k - 1:k + 4]).split(";")[0] if k else ""          # this statement, forward
    tabs = TB.findall(stmt) or (TB.findall("\n".join(src[f][max(0, k - 4):k])) if k else [])
    if tabs and norm(tabs[0] if TB.search(stmt) else tabs[-1]) in (every if diff else made.get(f, set())):
        dropped += 1; continue
    sys.stdout.write(hit)
if dropped: sys.stderr.write(f"  ({dropped} hit(s) on tables created in the same {'diff' if diff else 'file'}: precedent 12)\n")
PY
NEW=(python3 "$T/new.py" "${MIG_PATHS[@]}")

# 1. Index builds: non-concurrent build / drop / reindex (1a); ORM helpers without the concurrent option (1b); CONCURRENTLY
#    in a file with no transaction opt-out (1c) and the runner settings that decide it (1d); FULLTEXT / SPATIAL (1e);
#    UNIQUE / PRIMARY KEY added as a constraint, which builds its index under the table lock (1f).
rg -n -H -i --pcre2 '\b(create\s+(unique\s+)?index|drop\s+index|reindex\s+(index|table|schema|database))\b(?![^;\n]*\bconcurrently\b)' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | "${NEW[@]}"
rg -n -H --pcre2 '\badd_(index|reference)\b(?!.*algorithm:\s*:concurrently)|\bmigrations\.AddIndex\(|\bop\.create_index\((?!.*postgresql_concurrently\s*=\s*True)|\bcreate\s+unique_index\((?!.*concurrently:\s*true)|\baddIndex\((?!.*concurrently:\s*true)|->(index|unique|fullText|spatialIndex)\(|\b\w+\.(index|unique)\(\s*[\["\x27]|\bnew\s+TableIndex\(|\bdb_index\s*=\s*True' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"
rg -n -H -i '\bconcurrently\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | cut -d: -f1 | sort -u > "$T/conc"
rg -l -H -U --pcre2 'isTransactional\(\)[^{]*\{\s*return\s+false|^\s*(public\s+)?transaction\s*=\s*false|\bconfig\s*=\s*\{\s*transaction:\s*false|disable_ddl_transaction!|^\s*atomic\s*=\s*False|autocommit_block\(|@disable_ddl_transaction\s+true|\$withinTransaction\s*=\s*false|\+goose\s+NO\s+TRANSACTION|atlas:txmode\s+none' "${MIG_PATHS[@]}" | sort -u > "$T/optout"
comm -23 "$T/conc" "$T/optout"
rg -n -H --pcre2 '\b(allOrNothing|migrationsTransactionMode|disableTransactions|transaction_per_migration|executeInTransaction)\b|\bflyway\.mixed\b|django_zero_downtime_migrations|\b(strong|online)_migrations\b|\bsafe[-_]pg[-_]migrations\b' "${X[@]}" . | "${NC[@]}"
rg -n -H -i --pcre2 '\b(add|create)\s+(fulltext|spatial)\s+(index|key)\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"
rg -n -H -i --pcre2 '\badd\s+(constraint\s+["\x60\w]+\s+)?(unique|primary\s+key)\b(?![^;\n]*\busing\s+index\b)' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | "${NEW[@]}"

# 2. Rewrites and copies: type change, volatile / stored / identity default, MySQL COPY-only forms, VACUUM FULL / CLUSTER (2a);
#    the same through ORM helpers (2b). On MySQL also read every ALTER TABLE for an explicit ALGORITHM= clause.
rg -n -H -i --pcre2 '\balter\s+column\s+["\x60\w]+\s+(set\s+data\s+)?type\b|\bmodify\s+(column\s+)?["\x60\w]+\s+\w+|\balgorithm\s*=\s*copy\b|\bconvert\s+to\s+character\s+set\b|\bdrop\s+primary\s+key\b|\bset\s+(logged|unlogged)\b|\bvacuum\s+(\([^)]*\)\s*)?full\b|^\s*["\x60\x27]?\s*cluster\s+["\w]+|\badd\s+(column\s+)?[^;\n]*\b(default\s+\(?\s*(clock_timestamp|random|gen_random_uuid|uuid_generate_v[14]|uuidv7|timeofday|nextval)\s*\(|generated\s+always\s+as\s*\(.*\)\s*stored|generated\s+(always|by\s+default)\s+as\s+identity|(big|small)?serial\b)' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | "${NEW[@]}"
rg -n -H --pcre2 '\bchange_column\b(?!_(null|default|comment))|\bmigrations\.AlterField\(|\bop\.alter_column\([^)]*\btype_\s*=|->change\(\)|\.alter\(\)|^\s*modify\s+:' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"

# 3. NOT NULL: SET NOT NULL, ADD COLUMN … NOT NULL with no default (3a); the same through ORM helpers (3b).
rg -n -H -U -i --pcre2 '\bset\s+not\s+null\b|\badd\s+(column\s+)?(if\s+not\s+exists\s+)?["\x60\w]+\s+[^,;\n]*\bnot\s+null\b(?![^,;]*\bdefault\b)' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | "${NEW[@]}"
rg -n -H --pcre2 '\bchange_column_null\b[^\n]*\bfalse\b|\badd_column\b[^\n]*\bnull:\s*false\b(?![^\n]*\bdefault:)|\bop\.(add_column|alter_column)\([^\n]*\bnullable\s*=\s*False|->nullable\(false\)|\.notNullable\(\)|^\s*(add|modify)\s+:\w+[^\n]*\bnull:\s*false' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"

# 4. Breaking the running (N-1) release: rename / drop / enum-value rename (4a); a Django field whose default lives only in
#    Python (4b); Rails default changes, and the ignore step a drop needs first (4c); a column dropped and added = a lost rename (4d).
rg -n -H -i --pcre2 '\brename\s+(column\s+)?["\x60\w]+\s+to\b|\brename\s+to\b|\bdrop\s+(column|table)\b|\brename\s+value\b|\b(rename_column|rename_table|remove_column|remove_columns|remove_reference|drop_table)\b|\bmigrations\.(RenameField|RemoveField|RenameModel|DeleteModel)\(|\bop\.(drop_column|drop_table|rename_table)\(|\bnew_column_name\s*=|->(renameColumn|dropColumn|dropColumns)\(|Schema::(drop|dropIfExists|rename)\(|\.(dropColumn|renameColumn|dropTable|renameTable)\(' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"
rg -n -H -U --pcre2 'migrations\.AddField\((?=(?:(?!migrations\.)[\s\S])*?\bdefault\s*=)(?!(?:(?!migrations\.)[\s\S])*?\b(db_default\s*=|null\s*=\s*True))' "${MIG_PATHS[@]}"
rg -n -H --pcre2 '\bchange_column_default\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"; rg -n --pcre2 '\b(ignored_columns|ignore_column)\b' -g '*.rb' "${X[@]}" .
rg -n -H -i '\bdrop\s+column\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | cut -d: -f1 | sort -u > "$T/dropc"
rg -n -H -i '\badd\s+column\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | cut -d: -f1 | sort -u | comm -12 "$T/dropc" -

# 5. Constraints validated in the statement that adds them: FK / CHECK with no NOT VALID (multi-line aware), inline REFERENCES on
#    an added column (5a); ORM helpers without deferred validation (5b).
rg -n -H -U -i --pcre2 '\badd\s+(?=(constraint\s+["\x60\w]+\s+)?(foreign\s+key|check)\b)(?![^;]*\bnot\s+valid\b)|\badd[ \t]+(column[ \t]+)?(?!constraint\b|foreign\b)["\x60\w]+[ \t]+[^;\n]*\breferences\b(?![^;]*\bnot\s+valid\b)' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | "${NEW[@]}"
#    5c. NOT VALID and VALIDATE in one file the runner wraps in a transaction: the ADD's lock is held through the validation
#    (precedent 43). Read each: a new or empty table is precedent 12.
rg -l -i --pcre2 '\bnot\s+valid\b' "${MIG_PATHS[@]}" | sort > "$T/notvalid"; rg -l -i --pcre2 '\bvalidate\s+constraint\b' "${MIG_PATHS[@]}" | sort | comm -12 - "$T/notvalid" | comm -23 - "$T/optout"
rg -n -H --pcre2 '\badd_(foreign_key|check_constraint)\b(?!.*validate:\s*false)|\badd_reference\b.*\bforeign_key:\s*true|\bop\.create_(foreign_key|check_constraint)\(|\bmigrations\.AddConstraint\(|->(foreign|constrained)\(|\.foreign\(|\bforeign_key_checks\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"

# 6. Files that change an existing table with no lock timeout in the file (6a); the timeout set anywhere else (6b).
DDL='\b(alter\s+table|create\s+(unique\s+)?index|drop\s+index|add\s+constraint|alter\s+type|drop\s+table|rename\s+to)\b|\b(add_column|add_index|change_column|remove_column|add_foreign_key|rename_column)\b|migrations\.(AddField|AlterField|RemoveField|AddIndex|AddConstraint|RenameField)\(|\bop\.(add_column|alter_column|create_index|drop_column|create_foreign_key)\(|Schema::table\(|\.alterTable\('
rg -n -H -i --pcre2 "$DDL" "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | "${NEW[@]}" 2>/dev/null | cut -d: -f1 | sort -u > "$T/ddl"
rg -n -H -i --pcre2 '\b(lock_timeout|lock_wait_timeout)\b' "${MIG_PATHS[@]}" | "${NC[@]}" | cut -d: -f1 | sort -u | comm -23 "$T/ddl" -
rg -n -H -i --pcre2 '\b(lock_timeout|lock_wait_timeout)\b|StrongMigrations\.lock_timeout|ZERO_DOWNTIME_MIGRATIONS_LOCK_TIMEOUT|SafePgMigrations' "${X[@]}" . | "${NC[@]}"
#    6c. Files that opt out of the runner's transaction: `SET LOCAL lock_timeout` is a no-op there (precedent 42), and a runner
#    may set 0 for them (read 6b). ALTER/ADD CONSTRAINT/DROP/LOCK with no session `SET lock_timeout` or `set_config('lock_timeout',
#    …)` (a CONCURRENTLY-only file is not listed); and files that rely on SET LOCAL.
comm -12 "$T/optout" "$T/ddl" | while IFS= read -r f; do rg -q -i --pcre2 '\b(alter\s+table|add\s+constraint|drop\s+table|lock\s+table|alter\s+type)\b' "$f" && ! rg -q -i --pcre2 "\bset\s+(session\s+)?lock_timeout\b|set_config\(\s*'lock_timeout'" "$f" && echo "6c no session lock_timeout: $f"; rg -q -i --pcre2 '\bset\s+local\s+lock_timeout\b' "$f" && echo "6c SET LOCAL in a non-transactional file: $f"; done

# 7. Data inside a schema migration: files with both DML and DDL (7a); how many DML lines carry a batch key (7b).
rg -n -H -i --pcre2 '\b(update\s+(only\s+)?["\x60\w.${}]+(\s+(as\s+)?(?!set\b)\w+)?\s+set|insert\s+into|delete\s+from)\b|\bupdate_all\b|\bmigrations\.RunPython\(|\bDB::(update|insert|delete)\(' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}" | tee "$T/dml" | cut -d: -f1 | sort -u | comm -12 "$T/ddl" -
rg -c -H -i --pcre2 '\b(limit|between|batch|chunk|in_batches|find_each|iterator)\b' "$T/dml"
#    7b′. Files whose DML runs batched inside a `DO $$ … LOOP … LIMIT … $$` block (the key is lines away from the DML line).
rg -l -U -i --pcre2 'do\s+\$\$(?:(?!\$\$)[\s\S])*?\bloop\b(?:(?!\$\$)[\s\S])*?\blimit\b' "${MIG_PATHS[@]}"

# 8. Reversal: empty or raising down, RunPython / RunSQL with no reverse (8a); empty downs that carry a note — read the reason (8b);
#    destructive steps, to check for a recovery point (8c).
rg -n -H -U --pcre2 '\bdown\s*(?=\([^)]*\)\s*(:\s*Promise<void>\s*)?\{\s*\})|\bdef\s+(down|downgrade)\b(?=\s*\([^)]*\)\s*(->\s*None\s*)?:\s*pass\b)|raise\s+ActiveRecord::IrreversibleMigration|\bexports\.down\b(?=\s*=\s*(async\s*)?(function\s*)?\([^)]*\)\s*(=>\s*)?\{\s*\})|\bfunction\s+down\b(?=\s*\(\)\s*(:\s*void\s*)?\{\s*\})|\bmigrations\.RunPython\(\s*[\w.]+\s*\)|\bmigrations\.RunSQL\((?!(?:(?!migrations\.)[\s\S])*?\breverse_sql\b)' "${MIG_PATHS[@]}"
rg -c -H -U --pcre2 '\bdown\s*(?=\([^)]*\)\s*(:\s*Promise<void>\s*)?\{\s*(//|/\*))|\bdef\s+(down|downgrade)\b(?=\s*\([^)]*\)\s*(->\s*None\s*)?:\s*#)' "${MIG_PATHS[@]}" | wc -l
rg -n -H -i --pcre2 '\b(drop\s+table|drop\s+column|truncate)\b' "${MIG_PATHS[@]}" | "${NC[@]}" | "${UP[@]}"

# 9. Migrations edited after they were added: in this diff (9a); across history, most-edited first (9b).
git diff --name-only --diff-filter=M "$BASE"...HEAD 2>/dev/null | rg -i "$MIGRE"
git log --diff-filter=M --format= --name-only -- "${MIG_PATHS[@]}" | sort | uniq -c | sort -rn | head -20
# 9c. A squashed or re-rooted history hides 9b's edits. Compare each deployed ref's migrations with HEAD's, comments stripped.
#     Refs: $DEPLOYED_REFS, else git tags plus every commit-hash image tag the deploy files ever pinned (kustomize newTag, Helm
#     tag:, image: x:<sha>). Read-only: commits only, never the worktree. `history starts` near the first deploy = squashed.
git log --reverse --format='9c history starts %h %cs' | head -1
PINF=$(rg -l --pcre2 '\b(?:newTag|tag|image)\s*:\s*["\x27]?(?:\S+:)?[0-9a-f]{7,40}\b' -g '*.{yml,yaml}' "${X[@]}" . | tr '\n' ' ')
REFS="${DEPLOYED_REFS:-}"; [ -n "$REFS" ] || REFS=$( { git tag; [ -n "$PINF" ] && git log -p --format= -- $PINF | tr -d "\"'" | grep -oE '^\+\s*(newTag|tag|image)\s*:\s*([^ ]*:)?[0-9a-f]{7,40}' | grep -oE '[0-9a-f]{7,40}$'; } | sort -u)
for r in $REFS; do git cat-file -e "$r^{commit}" 2>/dev/null || continue; git diff --name-only --diff-filter=M "$r" HEAD -- "${MIG_PATHS[@]}" | while IFS= read -r f; do
  cmp -s <(git show "$r:$f" | sed -E '/^[[:space:]]*(\*|\/\/|--|\/\*)/d; s#[[:space:]]//.*$##') <(git show "HEAD:$f" | sed -E '/^[[:space:]]*(\*|\/\/|--|\/\*)/d; s#[[:space:]]//.*$##') || echo "9c code differs from deployed $r: $f"; done; done | sort -u
echo "9c refs: $(printf '%s\n' $REFS | grep -c .)"
```

A finding is a grep hit **plus** a read of the statement, the file's wrapping, the table's size rung and, for §4, the code that touches the column. Three blind spots are structural: SQL assembled at runtime (`create table "${name}"` defeats `NEW`, so its index hits survive and are read), helper methods that wrap DDL (`this.createIndexConcurrently(t, cols)` — grep the helper's name once found), and statements split across files (a `NOT VALID` here, its `VALIDATE` in the next migration — read both before reporting §5).

## Linter lane

Run after the block above, in the same shell. Pass `PGV` from the server major the context block read. MySQL and SQLite lanes skip it.

```bash
PGV="${PGV:-16}"; mkdir -p "$T/tx" "$T/notx"
python3 - "$T" "${MIG_PATHS[@]}" <<'PY'
import re, sys, pathlib
T, files = pathlib.Path(sys.argv[1]), sys.argv[2:]
CALL = re.compile(r'\b(?:addSql|query|raw|execute|runSql)\s*\(\s*(`(?:[^`\\]|\\.)*`|\'(?:[^\'\\]|\\.)*\'|"(?:[^"\\]|\\.)*")', re.S)
OPT = re.compile(r'isTransactional\(\)[^{]*\{\s*return\s+false|^\s*(?:public\s+)?transaction\s*=\s*false|transaction:\s*false', re.M)
DOWN = re.compile(r'(?:^|[^\w.])(?:async\s+)?down\s*\(|exports\.down\b')
for p in files:
    if not p.endswith((".ts", ".js", ".mjs", ".cjs")): continue
    src = open(p, encoding="utf-8", errors="replace").read()
    m = DOWN.search(src); up = src[:m.start()] if m else src          # the reversal does not ship forward
    out = [f"-- {p}:{src.count(chr(10), 0, c.start()) + 1}\n" + re.sub(r"\$\{[^}]*\}", "x", c.group(1)[1:-1]).strip().rstrip(";") + ";"
           for c in CALL.finditer(up) if c.group(1)[1:-1].strip()]
    if out: (T / ("notx" if OPT.search(src) else "tx") / (re.sub(r"[^\w.-]", "_", p) + ".sql")).write_text("\n".join(out) + "\n")
PY
SQLF=(); for f in "${MIG_PATHS[@]}"; do case "$f" in *.sql) SQLF+=("$f");; esac; done
SQB=""; for b in node_modules/.bin/squawk "$(command -v squawk)"; do [ -x "$b" ] && { SQB="$b"; break; }; done   # installed only — an audit never downloads
[ -n "$SQB" ] || { echo "linter NOT-RUN (squawk not installed — to enable: npm i -D squawk-cli@2.66.0); the grep half still runs"; SQB=false; }
SQ=("$SQB" --pg-version="$PGV" --reporter=gcc --exclude=prefer-text-field,prefer-bigint-over-int,prefer-bigint-over-smallint,prefer-identity,prefer-robust-stmts)
[ ${#SQLF[@]} -gt 0 ] && "${SQ[@]}" "${SQLF[@]}"          # add --assume-in-transaction when this runner wraps each SQL file
ls "$T/tx"/*.sql >/dev/null 2>&1 && "${SQ[@]}" --assume-in-transaction "$T/tx"/*.sql
ls "$T/notx"/*.sql >/dev/null 2>&1 && "${SQ[@]}" "$T/notx"/*.sql
```

Each lifted statement carries `-- <file>:<line>` above it; report the finding at that source line, not the lifted file's. A rule id is the linter's claim about one statement; the class (§ The operation-class rule), the size rung and the read decide the finding. squawk not installed → `NOT-RUN (squawk not installed — to enable: npm i -D squawk-cli@2.66.0)` for the linter half, and the grep half still runs; the audit never downloads it.

## Bulk triage — the 3,000-hit path

Migration history accumulates; a whole-repo run over years of files returns thousands of hits that already ran.

1. **Split applied from pending.** Read the runner's table on a reachable non-prod database (`mikro_orm_migrations`, TypeORM `migrations`, `knex_migrations`, `_prisma_migrations`, `django_migrations`, `alembic_version`, `schema_migrations`, `flyway_schema_history`, goose `goose_db_version`) or list the files at the deployed ref (`git ls-tree -r --name-only <deployed-ref> -- <migrations dir>`). Applied files close with one cited reason — `applied: the lock was taken already; a fresh environment replays them on empty tables (precedent 12)` — except for §9 and for repeatable migrations (Flyway `R__`), which rerun.
2. **Count, never re-read, the new-table hits** `NEW` drops.
3. **Read every pending file in full**, grouped by `(file, class)`: one decision covers a file's repeated statement on one table.
4. **Whatever is left unread** goes to the ledger as `Live, unreviewed (k files / n hits)` with the command that continues it. Never `checked`.

Measured (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, 376 TS migrations, history squashed on 2026-10-12): 3a 6 → 4 (two `DEFAULT`s on the next line were read as missing); 7a 21 → 24 files (aliased `update public.order_items i set` and `update "${this.table}" set`); the `NEW` filter no longer reads `ON DELETE` as a table named `delete`; new 5c 17 transactional files with `NOT VALID` and `VALIDATE` together (the four files a full read found, plus first-deploy sites); new 6c 6 non-transactional files with lock DDL and no session timeout plus 4 relying on `SET LOCAL` (a full read found the runner sets 0 for those files); new 7b′ 3 files batching inside a `DO` loop; 9c resolved 11 deployed refs from the kustomize `newTag` history and found 0 code edits, the same answer a by-hand comparison of every deployed sha gave. No fixture line was lost.

Measured on a real NestJS-on-Fastify + MikroORM 6.6 + Postgres monorepo (293 TS migrations, 2026-10-02): grep 1a returned 448 hits, of which `NEW` closed 347; 5a returned 330, of which it closed 265; 6a listed 183 files with no in-file lock timeout (65 files set one). 1c returned 0, as it should — all 23 `CONCURRENTLY` files opt out and the config sets `allOrNothing: false`, after both failures in the MikroORM row had been hit there. squawk on the lifted SQL (280 files) returned `require-concurrent-index-creation` ×76 and `constraint-missing-not-valid` ×62, close to greps 1a and 5a; 19 files with runtime-assembled SQL returned `syntax-error` and went to the read lane. On a synthetic corpus (Rails, Django, Alembic, Laravel, Knex, TypeORM, Prisma, Ecto, MySQL Flyway, goose), all 26 seeded defects stay in the candidate set and the 12 decoys stay out (a concurrent build with the right opt-out, `now()` as a default, a `NOT VALID` FK, a goose `Down` section).

## Scans for

Default severity assumes a populated table on a live path. A new or proven-empty table closes the class (precedent 12). An unresolved size keeps the severity and adds `[report-flagged]`. `/migration-review` prints critical and high as BLOCKER, medium as REQUEST and low as NIT.

| § | Class | Linter ids | Default |
|---|---|---|---|
| 1 | Blocking index build, drop or reindex; `CONCURRENTLY` inside a wrapped transaction; MySQL FULLTEXT / SPATIAL | squawk `require-concurrent-index-creation`, `require-concurrent-index-deletion`, `disallowed-unique-constraint`; strong_migrations `add_index`; django-migration-linter `CREATE_INDEX` | high |
| 2 | Rewrite or copy of a populated table | squawk `changing-column-type`, `adding-field-with-default`; strong_migrations `change_column`; Atlas PG301 / MY130 | critical |
| 3 | NOT NULL enforced without a backfill or the validated-CHECK path | squawk `adding-not-nullable-field`, `adding-required-field`; django-migration-linter `NOT_NULL` | high |
| 4 | A rename, drop or default change the running (N-1) release still depends on | squawk `renaming-column`, `ban-drop-column`; strong_migrations `remove_column`; django-migration-linter `RENAME_COLUMN`, `DROP_COLUMN`; Atlas BC10x | high; critical when data is lost |
| 5 | FK or CHECK validated in the statement that adds it | squawk `constraint-missing-not-valid`, `adding-foreign-key-constraint`; strong_migrations `add_foreign_key` | high |
| 6 | No lock timeout around DDL on an existing table | squawk `require-lock-timeout`; Eugene E9 | medium |
| 7 | Data inside the DDL transaction; unbatched backfill; schema and data in one file | django-migration-linter `RUNPYTHON_*`; excellent_migrations `operation_update` | medium; high on a large table |
| 8 | Irreversible or lossy step with no reverse and no recovery point | django-migration-linter `RUNPYTHON_REVERSIBLE`, `RUNSQL_REVERSIBLE`; Atlas DS10x | high on data loss; medium otherwise |
| 9 | An applied migration edited after it ran | Atlas non-linear | high |

### 1. Blocking index build

```
BAD:   CREATE INDEX orders_customer_idx ON orders (customer_id);                  -- PG: blocks writes for the whole build
       this.addSql('create index concurrently …');   // MikroORM default: inside the run's transaction → error, or a hang
       add_index :orders, :user_id                    # Rails: non-concurrent, inside the DDL transaction
GOOD:  CREATE INDEX CONCURRENTLY IF NOT EXISTS orders_customer_idx ON orders (customer_id);   -- own file, no transaction
       override isTransactional() { return false; }   // + allOrNothing: false in the migrator config
       ALTER TABLE orders ADD INDEX ix (customer_id), ALGORITHM=INPLACE, LOCK=NONE;      -- MySQL InnoDB ≥ 8.0: safe
```
Greps 1a, 1b, 1e and 1f list the builds; grep 1c lists `CONCURRENTLY` files with no opt-out, and grep 1d shows the runner settings that decide whether the opt-out works. **Read:** Is the table created in this file or this unreleased diff? Which engine — a MySQL B-tree build is safe, and SQLite and MySQL have no `CONCURRENTLY` at all? Does the runner wrap this file, and is the opt-out the right one for this runner and version (MikroORM needs both settings; TypeORM needs the mode)? Is the build alone in its file (goose, golang-migrate)? For a Django `ForeignKey` or `db_index=True` added to an existing model, the index is built non-concurrently. **Finding when** a populated or unresolved-size table gets a non-concurrent build, or a concurrent build runs where the runner wraps it. **Severity:** high; a wrapped concurrent build is high too (the deploy fails or, under MikroORM's master transaction, waits on itself while holding locks on the table). **Proof:** the lock-budget oracle in [`proof-oracles.md`](../../../../snippets/proof-oracles.md), run by `migration-rehearsal` (a reader holding `ACCESS SHARE` while the build runs; writes must not queue); for wrapping, run the migration through the real runner on a scratch DB and check `pg_index.indisvalid`.

### 2. Rewrite or copy of a populated table

```
BAD:   ALTER TABLE orders ALTER COLUMN id TYPE bigint;            -- PG: full rewrite under ACCESS EXCLUSIVE
       ALTER TABLE orders ADD COLUMN token uuid DEFAULT gen_random_uuid();      -- volatile → rewrite
       ALTER TABLE orders MODIFY COLUMN amount DECIMAL(12,2);      -- MySQL: COPY, DML blocked
GOOD:  ADD COLUMN created_at timestamptz DEFAULT now()            -- now() is STABLE: metadata-only on PG ≥ 11
       new column → dual write → batched backfill → swap → drop   -- expand-contract (ai/patterns/migrations.md)
```
Grep 2a lists the SQL forms; grep 2b lists the ORM helpers whose SQL must be read (`AlterField`, `change_column`, `->change()`). On MySQL, read every `ALTER TABLE` for an explicit `ALGORITHM=` clause: without one, MySQL silently falls back INSTANT → INPLACE → COPY. **Read:** Is the type change binary-coercible (class table)? Is the default volatile — `now()` is not? Is the MySQL table INSTANT-eligible (`SHOW CREATE TABLE` and `INNODB_TABLES.TOTAL_ROW_VERSIONS`)? **Finding when** the class is unsafe on a populated table with no expand-contract, online-schema-change tool or ADR'd window. **Severity:** critical (writes block for the whole rewrite); high when the size is unresolved. **Proof:** `migration-rehearsal`'s rewrite probe (`pg_relation_filenode` changes; MySQL reports the algorithm it took), plus the lock-budget oracle.

### 3. NOT NULL enforced without the safe path

```
BAD:   ALTER TABLE users ALTER COLUMN email SET NOT NULL;         -- scans the table under ACCESS EXCLUSIVE
       ALTER TABLE users ADD COLUMN status text NOT NULL;         -- fails on a populated table
GOOD:  ADD CONSTRAINT users_email_nn CHECK (email IS NOT NULL) NOT VALID;  VALIDATE CONSTRAINT users_email_nn;
       ALTER COLUMN email SET NOT NULL;  DROP CONSTRAINT users_email_nn;    -- PG ≥ 12 skips the scan
       PG 18: ADD CONSTRAINT users_email_nn NOT NULL email NOT VALID;  VALIDATE CONSTRAINT users_email_nn;
```
Greps 3a and 3b. **Read:** Was the column backfilled in an earlier migration, and is a validated CHECK already in place (squawk lints one file, so it flags a `SET NOT NULL` whose `VALIDATE` ran last week)? On MySQL, `SET NOT NULL` is an INPLACE rebuild that permits writes: there the risk is NULLs left in the column and the disk the rebuild needs, not a lock. **Finding when** a populated Postgres table gets `SET NOT NULL` with no validated CHECK, or any table gets `ADD COLUMN … NOT NULL` with neither a default nor a backfill. **Severity:** high. **Proof:** the lock-budget oracle; for the failing add, the migration run against a copy holding rows.

### 4. Breaking the release that is still running (N-1)

```
BAD:   ALTER TABLE orders RENAME COLUMN amt TO amount;            -- pods on the old release still SELECT amt
       remove_column :users, :legacy                              # Active Record caches columns: inserts fail until restart
       migrations.AddField("order", "status", models.CharField(default="new"))   # NOT NULL; Django drops the DB default
       DROP COLUMN "name"; ADD COLUMN "full_name"                  -- an autogenerated rename: the data is gone
GOOD:  expand (add) → dual-write → backfill → switch reads → contract (drop) in a later deploy
       self.ignored_columns += ["legacy"]  ships first; remove_column in the next deploy
       models.CharField(db_default="new")                         # Django ≥ 5.0: the default stays in the database
```
Grep 4a lists renames and drops; 4b lists Django `AddField` with a Python-only `default`; 4c lists Rails default changes and the ignore steps; 4d lists files that drop and add a column (a rename that Prisma or Alembic autogenerated as drop + add). For every dropped or renamed column, search the code that still runs:
`rg -n -w --pcre2 '<column>' "${X[@]}" .` — entities, serializers, raw SQL, column lists, reports, other services reading the same database.
**Read:** Does the deploy run migrations before or after the code, and does the old release survive the new schema (and, for a code-first deploy, the new code the old schema)? **Django:** `add_field` adds the column with its default to fill existing rows, then drops the database default unless the field has `db_default` (`django/db/backends/base/schema.py`, main, read 2026-10-02). An old release that inserts without the column then fails with `23502`. **Rails:** Active Record caches columns, so a drop needs `ignored_columns` shipped one deploy earlier (strong_migrations). With `partial_inserts`, Rails omits a column whose value equals the cached default, so changing a default ships as two steps (GitLab's `SafelyChangeColumnDefault`). Enum values: renaming or removing one breaks old readers; `ADD VALUE` does not. **Finding when** running code (or the previous release) reads or writes what this migration renames, drops or makes stricter, with no expand-contract or ignore step shipped first. **Severity:** high; critical when data is lost (4d). **Proof:** the compatibility (N-1) oracle in `proof-oracles.md`: the previous release's suite against the migrated schema.

### 5. Constraint validated in the statement that adds it

```
BAD:   ALTER TABLE orders ADD CONSTRAINT orders_user_fk FOREIGN KEY (user_id) REFERENCES users (id);
GOOD:  … REFERENCES users (id) NOT VALID;      -- migration N
       ALTER TABLE orders VALIDATE CONSTRAINT orders_user_fk;   -- migration N+1: SHARE UPDATE EXCLUSIVE, writes continue
```
Greps 5a, 5b and 5c (files the runner wraps in a transaction that hold both `NOT VALID` and `VALIDATE`, precedent 43). **Read:** Is the `VALIDATE` in this file (then it holds this file's transaction lock: split it) or in a later migration? On MySQL, there is no `NOT VALID`: an FK with checks on is COPY. With checks off, the anti-join recipe in `/add-migration` applies, and a `LOCK=NONE` choice needs the anti-join re-run after commit. An FK with `ON DELETE CASCADE` / `SET NULL` refuses `LOCK=NONE` on that table afterwards. **Finding when** a populated table gets a validated-on-add FK or CHECK. **Severity:** high. **Proof:** the lock-budget oracle; after the fix, constraint rejection (a violating insert fails with `23503` / `23514`).

### 6. No lock timeout

```
BAD:   ALTER TABLE orders ADD COLUMN note text;                   -- cheap, but queues behind one long transaction
GOOD:  SET lock_timeout = '3s';  ALTER TABLE …                    -- PG: fail fast, retry
       SET SESSION lock_wait_timeout = 5;  ALTER TABLE …          -- MySQL: the default is one year
```
Grep 6a lists files that change an existing table with no timeout in the file. Grep 6c lists the non-transactional files with lock-taking DDL and no session `SET lock_timeout` / `set_config('lock_timeout', …, true)`, and those that rely on `SET LOCAL` there (a no-op outside a transaction, precedent 42); in a file of `DO` blocks, read that each block sets its own. Grep 6b finds a timeout set elsewhere: the runner config, a wrapper (strong_migrations, safe-pg-migrations, django-pg-zero-downtime-migrations), or a role (`ALTER ROLE … SET lock_timeout`). Under a PgBouncer transaction pooler, a session `SET` does not stick, so only the role setting counts. **Finding when** neither the file nor the runner, wrapper or role bounds the wait. A control set elsewhere clears it (precedent 15). **Severity:** medium, whatever the op class. **Proof:** the lock-budget oracle's lock-queue variant: one session holds `ACCESS SHARE`, the migration must fail within the timeout, and a third session must not queue.

### 7. Data inside the schema migration

```
BAD:   ALTER TABLE orders ADD COLUMN status text;  UPDATE orders SET status = 'new';   -- one transaction: the lock lasts the whole UPDATE
GOOD:  schema migration → separate, batched backfill (UPDATE … WHERE id IN (SELECT id … LIMIT 1000 FOR UPDATE SKIP LOCKED)), throttled
```
Grep 7a lists files with both DDL and DML; grep 7b counts how many DML lines carry a batch key. **Read:** How many rows does the DML touch (size rung)? Is it inside the DDL's transaction? Is it idempotent and resumable? On MySQL, DDL commits implicitly, so a multi-step file half-applies on failure. Django `RunPython` beside `AddField` on Postgres can fail with "pending trigger events". **Finding when** an unbatched backfill touches a populated table, or DML shares the DDL's transaction on one. **Severity:** medium; high when the table is large. **Proof:** the backfill variant in `proof-oracles.md`, run on a production-shaped copy: each batch under budget, resumable after a kill, replica lag within budget.

### 8. Irreversible or lossy without a recovery point

```
BAD:   async down(): Promise<void> {}           // reversible step, empty down, no note
       migrations.RunPython(forwards)            # no reverse_code
       DROP TABLE legacy_invoices;               -- no archive copy, no backup point named
GOOD:  down() reverses the step, or the header says why it cannot and names the backup or archive step
```
Grep 8a lists empty or raising reversals; grep 8b counts empty ones with a note (read the reason); grep 8c lists destructive steps. **Read:** Is the project forward-only by policy (precedent 16)? Does the destructive step have an archive copy or a named backup point? **Finding when** a step destroys data with neither a reverse nor a recovery point, or a reversible step has an empty reversal where the convention is reversible. **Severity:** high on data loss; medium otherwise; a documented, deliberate one-way step is Hardening. **Proof:** the round-trip oracle (`up → down → up`, schema diff = 0) via `migration-rehearsal`'s Rollback block.

### 9. An applied migration edited after it ran

Grep 9a lists migrations this diff modifies; grep 9b lists files modified after they were added. 9b is blind on a squashed or re-rooted history (the first commit prints as `9c history starts`): grep 9c compares every deployed ref it can resolve (`DEPLOYED_REFS`, git tags, the image tags the deploy files ever pinned) with HEAD, comments stripped, and prints each migration whose code differs. Zero resolvable refs is `blocked (no deployed ref)`, not `checked`. **Read:** `git log -p --follow -- <file>`: did the SQL change, or only a comment? Is the original on the deployed ref, or in the runner's table? Flyway's `validate` stops on the edit (`Migration checksum mismatch`, flyway-nc source 13.9.0); a runner whose table records only names (MikroORM keeps `name` and `executed_at`) skips the edited file silently, so production never gets the change. **Finding when** executable content of an applied migration changed. **Severity:** high: fix forward with a new migration. **Proof:** the deployed ref or runner table shows it applied, and the diff shows changed SQL.

## Output

```
migration-safety — scope: diff vs origin/main (3 migrations) · engine: postgres 16 (docker-compose.yml:4)
runner: MikroORM 6.6 (transactional, allOrNothing: false) · lanes: ts 3 · linter: squawk 2.66.0 on lifted SQL

Findings: 3

1. src/migrations/Migration20261012000000.ts:21                          [report-with-fix]  high
   §1 create index "orders_customer_idx" on "orders" — blocking build; class safe-with-pattern
   (PG 16). orders ~2.4M rows (pg_class.reltuples, staging). Fix: CONCURRENTLY in its own
   migration with isTransactional() → false; the config already sets allOrNothing: false.

2. src/migrations/Migration20261012000100.ts:14                          [report-flagged]  high
   §4 drop column "legacy_ref" — still selected by src/orders/order.entity.ts:88 and
   src/reports/export.sql.ts:31. Unproven link: whether pods on the previous release still
   run during migrate. Fix: remove the entity property, ship, then drop in a later deploy.

3. src/migrations/Migration20261012000100.ts:9                           [report-with-fix]  medium
   §6 no lock timeout; none in orm-options.ts, none on the role. Fix: set local lock_timeout = '3s';

Verification: 5 candidates → 3 findings · 0 unconfirmed · 2 hardening · 0 pre-existing · 0 refuted

Class coverage:
  §1 index builds          checked (4 hits: 3 on a table created in the diff — precedent 12 → 1 finding)
  §2 rewrites / copies     checked (0 hits)
  §3 NOT NULL              checked (1 hit → 0 findings: validated CHECK in Migration20261005)
  §4 N-1 compatibility     checked (1 hit → 1 finding)
  §5 constraint validation checked (2 hits → 0 findings: both NOT VALID, VALIDATE in the next file)
  §6 lock timeout          checked (1 file → 1 finding)
  §7 data in DDL           checked (0 files)
  §8 reversal              checked (1 empty down with a note → 0 findings: one-way by design, header names the backup)
  §9 edited applied        checked (0 files)
```

`[report-with-fix]`: the class, the size rung and the safe rewrite are all resolved. `[report-flagged]`: the unsafe shape is real, but one link is unproven (size, engine version, runner wrapping, deploy order, code reachability), and the row names it. The coverage block lists **all nine** classes on every run: `checked (k hits → m findings)` only when its grep ran on a present lane, `N/A (<reason>)` only when nothing in scope can carry the class (no migration in scope; `engine sqlite: no CONCURRENTLY / NOT VALID / lock_timeout` for §1, §5 and §6), and `blocked (<reason>)` when a grep or the linter could not run, or SQL is assembled at runtime and went unread.

## False positives / precedents

Read [`precedents/data.md`](../../../../snippets/precedents/data.md) § Migrations (12–17) before reporting; they settle a new or empty table, PG ≥ 11 metadata-only DDL, the InnoDB index build, runner-level timeouts, forward-only projects and drop-versus-N-1. Also:
- `now()` / `current_timestamp` defaults are STABLE: metadata-only on PG ≥ 11. Only volatile functions rewrite.
- A `varchar → text` or widening change is not a rewrite. squawk's `changing-column-type` flags it anyway.
- Linters lint one file. A `SET NOT NULL` after last week's `VALIDATE`, or a `VALIDATE` split into the next file, is the safe pattern spread across two files.
- A `squawk-ignore`, `safety_assured` or `linter.IgnoreMigration()` with a checkable reason is evidence, not a bypass. Without a reason it is part of what is audited.
- Seeds, fixtures and test migrations are out of scope, unless the runner applies them in production.

## When to run

- On any diff that adds or edits a migration — the `/migration-review` dispatch, and the `/db-audit` signal.
- After `/add-migration` generates one, and when the backend pack is installed, after `add-endpoint` / `add-module` emit one.
- Before a deploy that ships schema changes, and after switching migration runner, ORM major or engine version.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (seven gates; gate 3 is engine and version). Under `/migration-review` or `/db-audit` that happens in their verification step. Run standalone, apply it as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening or Refuted — never drop them.
- Halt on any finding without the `<file:line>`, the statement, the op class with its engine and version, the size rung, and the safe rewrite.
- Do not report a grep or linter hit as a finding without reading the statement, the file's wrapping and the table's size.
- Do not decide a class from a row count, carry a class across engines, or clear an `unknown` class.
- Do not treat an unresolved size as small: it is `[report-flagged]`, treated as populated.
- Do not print a duration, lock hold or rewrite time. Numbers come from `migration-rehearsal` only.
- Do not print "migrations are safe" without the nine-class coverage block. A class whose grep did not run is `blocked`, never `checked`.

## Related

- `/migration-review` — dispatches this skill on every migration and prints its class lines in the review. `/add-migration` — builds the safe form, with its D1–D5 gate. `/db-audit` — dispatches it on whole-repo runs.
- [`migration-rehearsal`](../migration-rehearsal/SKILL.md) — the execution proof: the timed run, the lock observer, the rollback diff. `schema-diff`, `schema-integrity-scan`, `index-coverage-scan` — the neighbouring classes (§ Boundaries).
- `ai/patterns/migrations.md` — § Expand-contract for breaking changes and § Batched updates are the fix recipes. `ai/patterns/indexing-strategy.md` — whether the index is worth it.
- [`refute-before-report.md`](../../../../snippets/refute-before-report.md), [`precedents/data.md`](../../../../snippets/precedents/data.md) and [`proof-oracles.md`](../../../../snippets/proof-oracles.md) — verification, settled questions, oracles.
- `.claude/rules/database-principles.md` — the migration MUSTs this skill enforces.
