---
name: index-coverage-scan
description: Index-coverage detector — FK columns with no usable index (engine- and ORM-aware), filter and sort paths no index serves, wrong composite order, duplicate prefixes, unused indexes, missing expression or partial indexes, write-amplifying indexes. Static lane always; live lane read-only.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: index-coverage-scan

## Premise

An index is the cheapest performance fix there is, which is why it is also the most over-advised one. A query whose predicate no index serves reads the whole table on every call, and the cost grows with the table. An FK the engine never indexed makes every parent delete scan the child. An index nothing reads, or one that disables Postgres HOT updates on a write-hot table, taxes every write. This skill finds all three shapes: **the access paths the code really runs, against the indexes the schema really has, on the engine and version the project really uses.**

**Every finding cites the query or FK at `<file:line>` + the index list it was checked against (`<migration:line>` or the live catalog) + the engine and version + the fix.** A grep hit is never a finding. "Missing index" with no access path named, or "unused index" with no statistics window, is not one either. Nothing is reported as clean without the class-coverage block (§ Output).

Two lanes:
- The **static lane** always runs. It reads the DDL in migrations, schema files and ORM declarations, and the predicates in code and in captured query logs.
- The **live lane** runs only when a database is reachable. It is read-only by construction (§ "Live lane — read-only by construction").

The static lane cannot see row counts, so it proves **shape**. Cost claims need a plan on production-shaped data and are **Unconfirmed** until they have one ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## Boundaries

- **Non-sargable predicates** (`lower(col) =`, leading `%`, implicit casts, `OR` across columns) are detected by `query-shape-scan` §4 when the fix is a rewrite. They come here (§6) only when the predicate is intended and the fix is an expression or partial index. Dedupe by `<file:line>`.
- **Whether** an index is worth its write cost is decided by `ai/patterns/indexing-strategy.md` § "Is this index worth adding? — the verdict, in three measured inputs", and by `@query-optimizer` / `/optimize-query`. **Building** it on a populated table (`CONCURRENTLY`, `ALGORITHM=INPLACE, LOCK=NONE`, a transactional migration runner) belongs to `migration-safety` and `/add-migration`. This skill detects; those decide and ship.
- **N+1 and unbounded reads** belong to `n-plus-one-scan` and `query-shape-scan`. A missing FK constraint, as opposed to a missing FK index, belongs to `schema-integrity-scan` §1. Text search (`LIKE '%x%'` that should be FTS) belongs to `ai/patterns/full-text-search.md`.
- **Bloat, autovacuum and engine memory** belong to `@database-optimizer`.

## Adapt to the codebase

Read the engine, its version and the ORM version from the files (grep 0 in § "Pre-flight (static lane)"), never from memory. Then pick the rows below. The query logger and counter for each ORM are in `n-plus-one-scan` § "Adapt to the codebase — the shared ORM lane table"; this table holds only what changes an index verdict.

| Lane | Indexes declared in | FK index created for you? | Dump the DDL the ORM really emits |
|---|---|---|---|
| **Postgres** (raw `REFERENCES`) | migrations / `*.sql` | **No.** The docs call one "often a good idea"; nothing creates it | `pg_dump --schema-only` of a migrated scratch DB |
| **MySQL / MariaDB (InnoDB)** | migrations | **Yes.** It creates one leading with the FK columns, and may drop it later when a composite leading with them appears (`ai/patterns/indexing-strategy.md` § "Foreign keys — the engines differ, and the advice inverts"). §1 is `N/A` | `mysqldump --no-data` |
| **SQLite** | migrations | No. FKs are enforced only where `PRAGMA foreign_keys=ON` | `sqlite3 db .schema` |
| **MikroORM** (NestJS, Fastify, Express) | `@Index()` / `@Unique()` on the entity, `addSql()` in TS migrations | **Postgres: no.** Read in `@mikro-orm/postgresql` 6.6.16 source on 2026-10-02: `indexForeignKeys()` returns `false`, so `@ManyToOne` gets no index. Other SQL drivers inherit `true`. 7.x is current: dump to confirm | `npx --no mikro-orm schema:create --dump` |
| **TypeORM** | `@Index()`, `queryRunner.query()` | Postgres: no (`@ManyToOne` / `@JoinColumn`) | `typeorm schema:log -d <data-source>` against an empty scratch DB (it prints the diff against the live database, so only an empty one yields the full DDL) |
| **Prisma** | `@@index`, `@@unique`, `@id`, `@unique` | Postgres: no. With `relationMode = "prisma"`, "no indexes are created" (Prisma docs, read 2026-10-02) | `prisma migrate diff --from-empty --to-schema <schema.prisma> --script` with the project's pinned `prisma` binary, not an unpinned `npx prisma` (6.x: `--to-schema-datamodel`) |
| **Drizzle / Knex / Sequelize** | `index()` in the table builder / `.index()` / `indexes:` | Postgres: no | `drizzle-kit generate`; read the migration SQL |
| **Django** | `Meta.indexes`, `db_index=True` | **Yes**: "A database index is automatically created on the `ForeignKey`" unless `db_index=False` (Django docs, read 2026-10-02) | `manage.py sqlmigrate <app> <n>` |
| **SQLAlchemy / Alembic** | `Index()`, `index=True` | No | `alembic upgrade head --sql` |
| **Rails** | `add_index`, `t.index`, `db/schema.rb` | **Yes** for `t.references` / `add_reference` ("It also creates an index", Rails guide, read 2026-10-02) unless `index: false`. No for a bare `t.bigint :x_id` plus `add_foreign_key` | `db/schema.rb` / `structure.sql` |
| **Laravel** | `->index()`, `$table->index([...])` | Postgres: no. `foreignId()->constrained()` names no index (Laravel 12.x migrations docs, read 2026-10-02) | `php artisan schema:dump` |
| **Hibernate / JPA / Spring Data** | `@Table(indexes = …)`, `@Index` | Postgres: no (`@JoinColumn`) | `hbm2ddl` script output / Flyway SQL |
| **GORM** | `gorm:"index"` tags | Postgres: no | `AutoMigrate` against a scratch DB, then `pg_dump` |
| **EF Core** | `HasIndex`, `[Index]` | **Yes**: "By convention, an index is created in each property … used as a foreign key" (EF Core docs, read 2026-10-02) | `dotnet ef migrations script` |
| **MongoDB** | `createIndex`, schema `index: true` | No FKs. §1 is `N/A` | `db.c.getIndexes()` |

**Laravel without a booted app.** `schema-map.py` (H0) has a `laravel` lane: with no `.snapshot-*.json` and `.php` migrations that call `Schema::`, it replays every Blueprint `up()` in filename order (onto `database/schema/*-schema.sql` when `schema:dump` left one) and prints the same DDL the other lanes print, so §1–§4 read a Laravel schema with no PHP installed. `--lane=laravel` forces it on a checkout that also holds a snapshot (the V1 side of a port). The migration pack's `paired-inventory` reads V1's I-SCHEMA lane through it, when the migration pack is installed; without that pack the lane serves this skill alone.

An auto-created index is still checked against §3 and §4. A dump settles any "does this ORM add one?" question for the installed version in one command. Run it before reporting a §1 row that rests on an ORM default.

**Engine-version facts that change a verdict:**
- **Postgres ≥ 18 B-tree skip scan** can use `(a, b)` for `WHERE b = ?` when `a` has few distinct values (PG 18 release notes and the "Multicolumn Indexes" docs chapter, read 2026-10-02). Before 18, and for a range on `b`, the leading-column rule holds.
- **MySQL skip scan** needs all of these (the MySQL 8.4 manual's "Skip Scan Range Access Method" section, read 2026-10-02): one table, no `GROUP BY` or `DISTINCT`, the query reads only index columns, equality constants on the leading parts, and a range condition on the column after the skipped part. Prove it with `EXPLAIN`.
- **HOT updates** (Postgres) happen only when the `UPDATE` modifies no column any index references (`ai/patterns/indexing-strategy.md` § "Input 3 — the write cost, on the specific write path").

## Live lane — read-only by construction

Run it only when a database is reachable. Before the first statement, name the target (host and database, from the environment the app reads) and classify it:
- **production or unknown** — read-only mode;
- **non-production** — this mode only after the user confirms *in this session* that `<host>/<db>` is not production.

| Mode | Allowed | Never |
|---|---|---|
| **Read-only** (default) | `SELECT` on `pg_catalog`, `information_schema`, `pg_stat_*`, `sys`, `performance_schema`; plain `EXPLAIN` (no `ANALYZE`); every session opened as `BEGIN READ ONLY; SET LOCAL statement_timeout = '5s'; SET LOCAL lock_timeout = '1s';` (MySQL: `SET SESSION TRANSACTION READ ONLY; SET SESSION max_execution_time = 5000;`) | `EXPLAIN ANALYZE` (it **executes** the statement: triggers fire and sequences advance even on rollback), `ANALYZE` (it writes statistics), `CREATE EXTENSION`, `hypopg_*`, any DDL, `pg_stat_reset`, `SET` on a server parameter |
| **Confirmed non-production** | The above, plus `EXPLAIN (ANALYZE, BUFFERS)` (DML inside `BEGIN; … ROLLBACK;`), `ANALYZE`, `hypopg_create_index` / `hypopg_hide_index`, `generate_series` seeding | DDL on a shared database without saying what it changes |

**Parameter values are sampled, never invented.** Take them from `pg_stats.most_common_vals` / `histogram_bounds` or from a captured query log. Plan with one common and one rare value: selectivity flips the right plan. A prepared statement's generic plan needs `EXPLAIN (GENERIC_PLAN)` (Postgres ≥ 16).

```sql
-- L1. Statistics window (§5, and gate 3 for everything below). Under 30 days → §5 is blocked.
SELECT stats_reset, now() - coalesce(stats_reset, pg_postmaster_start_time()) AS window FROM pg_stat_database WHERE datname = current_database();
-- L2 (§1). FKs with no valid, non-partial index leading with their columns, and the child's row estimate.
SELECT c.conrelid::regclass AS child, c.conname, pg_get_constraintdef(c.oid) AS def, cl.reltuples::bigint AS est_rows
  FROM pg_constraint c JOIN pg_class cl ON cl.oid = c.conrelid
 WHERE c.contype = 'f' AND NOT EXISTS (
       SELECT 1 FROM pg_index i WHERE i.indrelid = c.conrelid AND i.indisvalid AND i.indpred IS NULL
          AND (string_to_array(i.indkey::text, ' ')::int2[])[1:cardinality(c.conkey)] @> c.conkey
          AND (string_to_array(i.indkey::text, ' ')::int2[])[1:cardinality(c.conkey)] <@ c.conkey)
 ORDER BY est_rows DESC;
-- L3 (§4). Left-prefix duplicates: same access method, no predicate, no expression, the shorter not constraint-backing.
SELECT a.indrelid::regclass AS tbl, a.indexrelid::regclass AS redundant, b.indexrelid::regclass AS covered_by
  FROM pg_index a JOIN pg_index b ON b.indrelid = a.indrelid AND b.indexrelid <> a.indexrelid
  JOIN pg_class ca ON ca.oid = a.indexrelid JOIN pg_class cb ON cb.oid = b.indexrelid
 WHERE ca.relam = cb.relam AND a.indpred IS NULL AND b.indpred IS NULL AND a.indexprs IS NULL AND b.indexprs IS NULL
   AND NOT a.indisunique AND a.indnatts = a.indnkeyatts AND a.indnkeyatts <= b.indnkeyatts   -- a shorter index with INCLUDE columns is not redundant
   AND (string_to_array(a.indkey::text, ' ')::int2[])[1:a.indnkeyatts] = (string_to_array(b.indkey::text, ' ')::int2[])[1:a.indnkeyatts]
   AND NOT EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conindid = a.indexrelid);
-- L4 (§4, §5). Invalid indexes (a failed CREATE INDEX CONCURRENTLY still costs writes), then never-scanned ones.
SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;
SELECT s.relname, s.indexrelname, s.idx_scan, pg_relation_size(s.indexrelid) AS bytes, i.indisunique,
       EXISTS (SELECT 1 FROM pg_constraint k WHERE k.conindid = s.indexrelid) AS backs_constraint
  FROM pg_stat_user_indexes s JOIN pg_index i USING (indexrelid) WHERE s.idx_scan = 0 ORDER BY bytes DESC;
-- L5 (§7). Write-hot tables: HOT share of updates and index count.
SELECT relname, n_tup_upd, n_tup_hot_upd, round(100.0 * n_tup_hot_upd / nullif(n_tup_upd, 0), 1) AS hot_pct,
       (SELECT count(*) FROM pg_index WHERE indrelid = s.relid) AS indexes
  FROM pg_stat_user_tables s ORDER BY n_tup_upd DESC LIMIT 20;
-- L6 (§8). Partitions × indexes per parent; slow-path locks per backend; LockManager waits (sample during load).
SELECT inhparent::regclass, count(*) AS partitions, (SELECT count(*) FROM pg_index WHERE indrelid = inhparent) AS parent_indexes
  FROM pg_inherits GROUP BY inhparent ORDER BY 2 DESC;
SELECT pid, count(*) FILTER (WHERE NOT fastpath) AS slow_path_locks, count(*) AS locks FROM pg_locks GROUP BY pid ORDER BY 2 DESC LIMIT 10;
SELECT count(*) FROM pg_stat_activity WHERE wait_event_type = 'LWLock' AND wait_event = 'LockManager';
```
MySQL: `SELECT * FROM sys.schema_unused_indexes;` and `sys.schema_redundant_indexes` (§4, §5 — representative only after enough uptime; read `Uptime` from `performance_schema.global_status`), `information_schema.STATISTICS` for the index map, `EXPLAIN FORMAT=TREE <query>` (never `ANALYZE`). Supabase-hosted repos can add `supabase db advisors` / MCP `get_advisors` (splinter lints `0001_unindexed_foreign_keys`, `0005_unused_index`, `0009_duplicate_index`): each hit is a candidate for the same detector, judged the same way.

## Pre-flight (static lane)

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**; **H** is the schema-and-predicate map, which feeds §1–§4 and §7. Every `rg` names its path (`.`): given none, `rg` reads stdin whenever stdin is a pipe, and an agent's shell turns that into a silent zero-hit run. A lane that prints `No files were searched` is absent: record it as an `N/A` reason. Any `rg` exit code 2 is a failed grep, not zero hits.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*' -g '!*.md' -g '!ai/**' -g '!docs/**'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,scripts,generated,__generated__,temp,locales}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,doc}.*' -g '!**/{*_test,test_*}.*' -g '!**/*.{snap,lock,map,po,json}')
N=(-g '!**/{migrations,migration,migrate,alembic}/**')   # query greps skip migrations; DDL greps keep them
C='^(?!\s*(?://|\*|/\*|#|--))[^\n]*?'                     # the hit is not on a comment line

# 0. Engine, version and ORM (gate 3) — the lane table's rows, read from files.
rg -n --pcre2 -i 'image:\s*["\x27]?\S*(postgres|postgis|mysql|mariadb|mongo)\S*:\S+|engine_version\s*=|\b(postgres|mysql)_?version\s*[:=]' -g '*.{yml,yaml,tf,tfvars,env}' -g '!**/node_modules/**' .
rg -n --pcre2 '"(@mikro-orm/\w+|typeorm|@prisma/client|sequelize|drizzle-orm|knex|mongoose)"\s*:|^\s*(django|sqlalchemy|alembic)\b|gem\s+["\x27](rails|activerecord)["\x27]|"laravel/framework"|hibernate-core|spring-boot-starter-data-jpa|gorm\.io/gorm|Microsoft\.EntityFrameworkCore|provider\s*=\s*"(postgresql|mysql|sqlite|mongodb)"' -g '{package.json,pyproject.toml,requirements*.txt,Gemfile,composer.json,pom.xml,build.gradle*,go.mod,*.csproj,*.prisma}' -g '!**/node_modules/**' .

# H0. The schema map (database pack script index-coverage-scan/scripts/schema-map.py): a MikroORM `.snapshot-*.json` plus a
#     replay of the migrations written after its horizon, else every migration's up() with `${…}` names resolved and
#     template loops unrolled. H reads it instead of the files it covers. NOT-RUN = interpolated DDL is invisible to H.
SM=.claude/skills/index-coverage-scan/scripts/schema-map.py; RUN=$(mktemp -d "${TMPDIR:-/tmp}/db-scan.XXXXXX")
if command -v python3 >/dev/null 2>&1 && [ -f "$SM" ] && python3 -I -B "$SM" . > "$RUN/schema.sql"; then export SCHEMA_SQL="$RUN/schema.sql"; grep '^-- schema-map [lhr]' "$SCHEMA_SQL"; else unset SCHEMA_SQL; echo 'schema-map NOT-RUN (python3 or schema-map.py absent): H parses the migrations; ${...} names stay invisible'; fi

# H. Schema-and-predicate map. Parses CREATE TABLE / ALTER TABLE / CREATE INDEX / DROP (SQL, and SQL inside addSql(),
#    queryRunner.query(), knex.raw()), Prisma models and Rails schema.rb, in path order, skipping down()/downgrade
#    bodies, then H0's map. Then raw-SQL `FROM t WHERE … ORDER BY …` in code. Extra arguments are captured query logs (R2).
python3 - . ${QLOG:+"$QLOG"} <<'PY'
import os, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
SKIP = {'node_modules','vendor','dist','build','target','.git','.venv','coverage','test','tests','__tests__','spec','e2e','__mocks__','mocks','fixtures','__fixtures__','testdata','.next','tmp'}
SQ = os.environ.get('SCHEMA_SQL') or ''; COV = re.findall(r'(?m)^-- schema-map covers (.+)$', open(SQ, encoding='utf-8').read()) if SQ else []
I = r'[\\"`\[]*(?:\w+[\\"`\]]*\.[\\"`\[]*)?(\w+)[\\"`\]]*'                      # [schema.]name, quotes stripped
def split(s):
    out, d, cur = [], 0, ''
    for ch in s:
        d += (ch == '(') - (ch == ')')
        if ch == ',' and d == 0: out.append(cur); cur = ''
        else: cur += ch
    return out + [cur]
def bal(s, i):                                                                    # the ')' closing s[i], at any depth
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '(') - (s[j] == ')')
        if not d: return j
    return len(s) - 1
def cols(s): return [('(' + ' '.join(q.split()) + ')') if '(' in q else re.match(r'[\\"`\[]*(\w*)', q).group(1).lower() for q in (x.strip() for x in split(s)) if q]
fks, idx, preds = {}, {}, []                                                      # fks[name] = (table, cols, parent, at)
def add(n, t, c, k, w=''): idx[(n or '').strip('"`[]\\').lower() or '%s(%s)#%d' % (t, ','.join(c), len(idx))] = (t.lower(), c, k, w)
def fk(n, t, c, par, at): fks[(n or '').strip('"`[]\\').lower() or '%s_%s_fkey' % (t.lower(), '_'.join(c))] = (t.lower(), c, par.lower(), at)
files = sorted(os.path.join(dp, f) for dp, dns, fns in os.walk(R) for f in fns if not dns.__setitem__(slice(None), [d for d in dns if d not in SKIP])
               and re.search(r'\.(sql|prisma|ts|js|mjs|py|rb|php|java|kt|go|cs|exs)$', f) and not re.search(r'\.(spec|test|e2e-spec|mock|stories)\.', f)) + sys.argv[2:] + [SQ][:bool(SQ)]
for p in files:
    t = open(p, encoding='utf-8', errors='replace').read().replace('\\"', '"'); rel = p if p in sys.argv[2:] + [SQ] else os.path.relpath(p, R)
    def ln(pos):                                                                  # H0's `-- @src file:line` markers name the origin
        k = t.rfind('-- @src ', 0, pos) if p == SQ else -1
        if k < 0: return '%s:%d' % (rel, t.count('\n', 0, pos) + 1)
        e = t.find('\n', k); f, _, l = t[k + 8:e].rpartition(':'); return '%s:%d' % (f, int(l) + t.count('\n', e + 1, pos))
    if p != SQ and not re.search(r'(?i)migrat|(^|/)(scripts?|seeds?|seeders?|ai|docs?)/', rel):              # raw-SQL access paths (§2/§3)
        for m in re.finditer(r'(?is)\bfrom\s+' + I + r'(?:\s+(?:as\s+)?(?!where\b)["`]?\w+["`]?)?\s+where\s+(.{1,300}?)(?:\border\s+by\s+(?:["`]?\w+["`]?\.)?["`]?(\w+)\b(?!\s*\()|\b(?:limit|offset|returning|group\s+by)\b|;|["\'`]\s*[+),;]|$)', t):
            pc = [c.lower() for c in re.findall(r'(?i)(?:["`]?\w+["`]?\.)?["`]?([a-z_]\w*)["`]?\s*(?:=|<|>|!=|\bin\b|\bis\b|\bi?like\b|\bbetween\b)', m.group(2))]
            ob = '' if re.search(r'(?i)\bunion\b', t[max(0, m.start() - 600):m.start()]) else (m.group(3) or '').lower()   # a later UNION branch: the ORDER BY is the outer one
            if (pc or '${' in m.group(2)) and not re.match(r'\s*(\*|//|#|--)', t[t.rfind('\n', 0, m.start()) + 1:m.start()]): preds.append((m.group(1).lower(), pc, ob, ln(m.start()), '${' in m.group(2)))
    if any(rel == c or c.endswith('/') and rel.startswith(c) for c in COV): continue        # H0's map already holds this file's DDL
    if p.endswith('.prisma'):
        for mm in re.finditer(r'(?ms)^model\s+(\w+)\s*\{(.*?)^\}', t):
            b = mm.group(2); tb = (re.search(r'@@map\("(\w+)"\)', b) or mm).group(1)
            for f in re.finditer(r'(?m)^\s*(\w+)\s+\w+[?\[\]]*\s+[^\n]*?@(id|unique)\b', b): add(None, tb, [f.group(1).lower()], 'unique')
            for f in re.finditer(r'(?m)^\s*\w+\s+(\w+)\??\s+@relation\([^)]*fields:\s*\[([^\]]*)\]', b): fk(None, tb, cols(f.group(2)), f.group(1), ln(mm.start(2) + f.start()))
            for f in re.finditer(r'@@(index|unique|id)\(\s*(?:fields:\s*)?\[([^\]]*)\]', b): add(None, tb, cols(f.group(2)), 'index' if f.group(1) == 'index' else 'unique')
        continue
    if not re.search(r'(?i)\b(create\s+(unique\s+)?index|foreign\s+key|references|create\s+table|primary\s+key|add_index|t\.index|drop\s+(table|index|constraint))\b', t): continue
    dn = re.search(r'(?m)^\s*(?:public\s+|override\s+)*(?:async\s+)?(?:def\s+|function\s+)?(?:down|downgrade)\s*(?:[(:]|$)|\bexports\.down\b|^--\s*\+(?:goose|migrate)\s+Down', t); t = t[:dn.start()] if dn else t   # skip down()/downgrade
    for m in re.finditer(r'(?is)create\s+(?:unlogged\s+)?table\s+(?:if\s+not\s+exists\s+)?' + I + r'\s*\(', t):     # CREATE TABLE body
        for q in (x.strip() for x in split(t[m.end():bal(t, m.end() - 1)])):
            k = re.match(r'(?is)(?:constraint\s+\S+\s+)?(primary\s+key|unique|(?:unique\s+)?(?:key|index)\s+\S+)\s*\(([^)]*)\)', q)
            if k: add(None, m.group(1), cols(k.group(2)), 'index' if re.match(r'(?i)(key|index)', k.group(1)) else 'unique'); continue
            k = re.match(r'(?is)(?:constraint\s+(\S+)\s+)?foreign\s+key\s*\(([^)]*)\)\s*references\s+' + I, q)
            if k: fk(k.group(1), m.group(1), cols(k.group(2)), k.group(3), ln(m.end() + t[m.end():].find(q))); continue
            k = re.match(r'(?is)[\\"`\[]*(\w+)[\\"`\]]*\s+\w[^,]*?\breferences\s+' + I, q)
            if k: fk(None, m.group(1), [k.group(1).lower()], k.group(2), ln(m.end() + t[m.end():].find(q))); continue
            k = re.match(r'(?is)[\\"`\[]*(\w+)[\\"`\]]*\s+\w[^,]*?\b(primary\s+key|unique)\b', q)
            if k and k.group(1).lower() not in ('constraint', 'check'): add(None, m.group(1), [k.group(1).lower()], 'unique')
    A = r'(?is)alter\s+table\s+(?:only\s+)?(?:if\s+exists\s+)?' + I
    for m in re.finditer(A + r'\s+add\s+(?:constraint\s+(\S+)\s+)?foreign\s+key\s*\(([^)]*)\)\s*references\s+' + I, t): fk(m.group(2), m.group(1), cols(m.group(3)), m.group(4), ln(m.start()))
    for m in re.finditer(A + r'\s+add\s+(?:column\s+)?(?:if\s+not\s+exists\s+)?[\\"`]*(\w+)[\\"`]*\s+\w[\w ()]*?\breferences\s+' + I, t): fk(None, m.group(1), [m.group(2).lower()], m.group(3), ln(m.start()))
    for m in re.finditer(A + r'\s+add\s+(?:constraint\s+(\S+)\s+)?(?:primary\s+key|unique)\s*\(([^)]*)\)', t): add(m.group(2), m.group(1), cols(m.group(3)), 'unique')
    for m in re.finditer(r'(?is)create\s+(unique\s+)?index\s+(?:concurrently\s+)?(?:if\s+not\s+exists\s+)?(?:' + I + r'\s+)?on\s+(?:only\s+)?' + I + r'\s*(?:using\s+(\w+)\s*)?\(', t):
        e = bal(t, m.end() - 1); tail = re.split(r'[;`]', t[e + 1:e + 300])[0]; wh = re.search(r'(?is)\bwhere\b\s*(.*)', tail)
        add(m.group(2), m.group(3), cols(t[m.end():e]), ('unique' if m.group(1) else 'index') + ('/' + m.group(4).lower() if m.group(4) and m.group(4).lower() != 'btree' else '') + ('/partial' if wh else '') + ('/include' if re.match(r'(?is)\s*include\s*\(', tail) else ''), ' '.join(wh.group(1).split()) if wh else '')
    for m in re.finditer(r'(?s)create_table "(\w+)".*?\n  end\b', t):                                  # Rails db/schema.rb (Prisma and SQL DDL above)
        add(None, m.group(1), ['id'], 'unique')
        for f in re.finditer(r't\.index \[([^\]]*)\](.*)', m.group(0)): add(f.group(2) and (re.search(r'name: "(\w+)"', f.group(2)) or [None, None])[1], m.group(1), re.findall(r'"(\w+)"', f.group(1)), 'unique' if 'unique: true' in f.group(2) else 'index')
    for m in re.finditer(r'add_foreign_key "(\w+)", "(\w+)"(?:, column: "(\w+)")?', t): fk(None, m.group(1), [m.group(3) or re.sub(r'ies$', 'y', m.group(2)).rstrip('s') + '_id'], m.group(2), ln(m.start()))
    for m in re.finditer(r'(?is)\bdrop\s+(?:constraint|index)\s+(?:concurrently\s+)?(?:if\s+exists\s+)?' + I, t): idx.pop(m.group(1).lower(), None); fks.pop(m.group(1).lower(), None)
    for m in re.finditer(r'(?is)\bdrop\s+table\s+(?:if\s+exists\s+)?' + I, t):
        for d in (idx, fks): [d.pop(n) for n in [n for n, v in d.items() if v[0] == m.group(1).lower()]]
lead = {}
for n, (tb, c, k, w) in idx.items(): lead.setdefault(tb, []).append((n, c, k, w))
HOT = r'^(updated_at|last_\w+|\w+_count|\w+_seen_at|heartbeat\w*|accessed_at|locked_\w+|attempts?)$'
TEN = r'^(tenant|org|organi[sz]ation|account|workspace|company|team)_id$'
print('§1 FK with no index/key leading with its columns, compared as a set (Postgres/SQLite; InnoDB creates one):'); led = 0
for n, (tb, c, par, at) in sorted(fks.items(), key=lambda x: x[1][3]):
    L = [(ic, k) for _, ic, k, w in lead.get(tb, []) if 'partial' not in k or all(re.fullmatch(r'(\w+) is not null', x) and x.split()[0] in c for x in ' '.join(re.sub(r'[()"]', ' ', w.lower()).split()).split(' and '))]   # `WHERE fk IS NOT NULL` serves the check
    if any(set(ic[:len(c)]) == set(c) for ic, k in L): continue
    if len(c) > 1 and any(ic[0] in c and not re.match(TEN, ic[0]) for ic, k in L): led += 1; continue        # (tenant_id, x) served by an index led by x
    sec = [n2 for n2, ic, k, w in lead.get(tb, []) if ic[1:1 + len(c)] == c]
    print('  %s.%s -> %s  %s%s' % (tb, ','.join(c), par, at, '  [2nd column of %s]' % sec[0] if sec else ''))
if led: print('  (%d composite FKs served by an index led by their non-tenant column: not listed)' % led)
print('§2/§3 raw-SQL filter (| sort) with no index leading with a filter column, or the sort not inside one:'); blind = []
for tb, pc, ob, at, var in preds:
    hit = [(n, c) for n, c, k, w in lead.get(tb, []) if c[0] in pc and 'partial' not in k]
    part = [('%s(%s)' % (n, ','.join(c)), w) for n, c, k, w in lead.get(tb, []) if 'partial' in k and (c[0] in pc or any(re.search(r'\b%s\b' % x, w) for x in pc))]
    if tb in lead and not hit and not pc: blind.append(at)
    elif tb in lead and not hit and var: print('  UNKNOWN  %s: %s + ${…} | %s  %s (the WHERE is partly interpolated: read its builder)' % (tb, ','.join(pc), ob or '-', at))
    elif tb in lead and not hit and part: print('  PARTIAL-CANDIDATE %s: %s | %s  %s (%s where %s: serves it only if the query implies that predicate)' % (tb, ','.join(pc), ob or '-', at, part[0][0], part[0][1][:80]))
    elif tb in lead and not hit: print('  NO-INDEX %s: %s | %s  %s' % (tb, ','.join(pc), ob or '-', at))
    elif hit and ob and ob not in pc and not any(ob in c for _, c in hit): print('  SORT     %s: %s | %s  %s (best %s)' % (tb, ','.join(pc), ob, at, hit[0][0]))
if blind: print('  UNKNOWN  %d statement(s) whose whole WHERE is interpolated (`${where}`): read each builder — %s' % (len(blind), ' '.join(blind[:4]) + (' …' if len(blind) > 4 else '')))
print('§3 composite led by a time/range-looking column · §4 left-prefix duplicate · §7 hot-update column indexed:')
for tb, L in sorted(lead.items()):
    for n, c, k, w in L:
        if len(c) > 1 and re.search(r'(_at|_on|date|time|ts)$', c[0]): print('  §3 %s: %s(%s)' % (tb, n, ','.join(c)))
        for n2, c2, k2, w2 in L:
            if n != n2 and k == 'index' and '/' not in k2 and c2[:len(c)] == c and (len(c2) > len(c) or n < n2): print('  §4 %s: %s(%s) inside %s(%s) [%s]' % (tb, n, ','.join(c), n2, ','.join(c2), k2))
        if any(re.match(HOT, x) for x in c): print('  §7 %s: %s(%s)  [%d indexes on table]' % (tb, n, ','.join(c), len(L)))
print('parsed: %d FKs, %d live indexes/keys in %d tables%s' % (len(fks), len(idx), len(lead), ' (H0 map: %s)' % SQ if SQ else ''))
PY

# 1. ORM relation declarations (entity-first repos have no SQL for H to read) and the switches that turn an index off.
rg -n --pcre2 '@(ManyToOne|OneToOne|JoinColumn)\(|\bmodels\.(ForeignKey|OneToOneField)\(|^\s*(belongs_to|t\.references|add_reference)\b|\bforeignId(For)?\(|->foreign\(|\.references\(\s*(\(\)\s*=>|["\x27])|\bHasForeignKey\(|\bgorm:"[^"]*foreignKey|\bbelongsTo\(\s*\w+' "${X[@]}" .
rg -n --pcre2 'ForeignKey\([^)]*db_index\s*=\s*False|\b(add_reference|t\.references)\b[^\n]*index:\s*false|relationMode\s*=\s*"prisma"' "${X[@]}" .
#    1c. References kept as scalar uuid properties (`@Property({ type: 'uuid' }) orderId`): one count line, then the top files.
rg -c -U --pcre2 '@Property\(\s*\{[^}]*\btype:\s*["\x27]uuid["\x27][^}]*\}\s*\)\s*(?:readonly\s+)?(?!tenantId\b)\w+Id[!?]?\s*:' "${X[@]}" . | sort -t: -k2 -nr | awk -F: '{s+=$2; if (NR<=5) top=top" "$0} END {print s+0" scalar uuid *Id properties in "NR" files (relation candidates on entity-first repos):"top}'

# 2. Access paths in ORM code. 2a: sorted queries (the filter + sort pair is the composite question; read each
#    query's filter). 2b: Spring Data derived finders spell their columns. 2c: worker polls and claims run every tick
#    (a status literal only inside a query call or a `where: {` object, SQL `WHERE status =`, or SKIP LOCKED).
rg -n --pcre2 "$C"'(?:\border(?:By)?\s*:\s*[\[{]|\.(?:orderBy|addOrderBy|order_by|OrderBy|Order)\(\s*[\[{"\x27`:]|\bORDER\s+BY\b)' "${N[@]}" "${X[@]}" .
rg -n --pcre2 '\b(find|read|get|query|search|stream|count|exists|delete)(First|Top)?\d*(Distinct)?(All)?By[A-Z]\w*\s*\(' -t java -t kotlin "${X[@]}" .
rg -n -U --pcre2 "$C"'(?:\b(?:(?:find\w*|count\w*|native(?:Update|Delete)|(?:update|delete)Many|where|andWhere|orWhere|exists\w*)\s*\(|where\s*:\s*\{)(?:[^;()]|\([^;()]*\)){0,240}?\K\b(?i:status|state)\b["\x27`]?\s*(?::|=>)\s*["\x27](?i:pending|queued|new|ready|scheduled|retrying|waiting)["\x27]|\b(?i:where)\b[^\n]{0,80}\b(?i:status|state)\b["`]?\s*(?:=|in\b)[^\n]{0,40}\b(?i:pending|queued|ready|scheduled)\b|(?i:for\s+update\s+skip\s+locked))' "${N[@]}" "${X[@]}" -g '!**/*.{yml,yaml}' .

# 4. ORM-declared indexes, for the lanes H does not parse (decorators, Meta.indexes, fluent builders, tags).
rg -n --pcre2 '@Index\(|@Unique\(|\bmodels\.(Index|UniqueConstraint)\(|\bindex_together\b|^\s*(add_index|t\.index)\b|->(index|unique)\(|@Table\([^)]*indexes\s*=|\bHasIndex\(|\bgorm:"[^"]*index|\b(uniqueIndex|index)\(\s*["\x27]\w+["\x27]\s*\)\.on\(' "${X[@]}" .

# 6. Predicates that need an expression or partial index: functions on a column, case-insensitive match, and the
#    soft-delete or status filter every query repeats (a partial-index candidate).
rg -n --pcre2 "$C"'(?:\b(?i:lower|upper|date_trunc|coalesce|cast|btrim|trim|unaccent)\s*\(\s*["\x60]?[\w.]+["\x60]?\s*(?:\)|::\w+\)?|,[^)]{0,30}\))\s*(?i:=|<|>|\bin\b|\bi?like\b)|(?-i:DATE)\(\s*[\w."]+\s*\)\s*=|\bmode\s*:\s*["\x27]insensitive["\x27]|__(?:iexact|istartswith|date|year|month)\b|\$ilike\b)' "${N[@]}" "${X[@]}" .
rg -n --pcre2 '\bdeleted_?[aA]t\b["`]?\s*(?:(?i:IS\s+NULL)|:\s*null|===?\s*null)|@Filter\(|@SQLRestriction|@Where\(|\bdefault_scope\b|\bSoftDeletes\b|\bparanoid\s*:\s*true' "${N[@]}" "${X[@]}" .

# 8. Partitioned tables (the live lane's lock-manager row needs them; window functions do not match).
rg -n --pcre2 -i '\)\s*partition\s+by\s+(range|list|hash)\s*\(|\bpartition\s+of\s+["\x60]?[\w.]+["\x60]?\s+(for\s+values|default)\b|\bpg_partman\b|\bcreate_parent\s*\(' "${X[@]}" .
```

**H0 decides what H reads.** `lane=mikro-orm-snapshot` prints both horizons (`git`: the files added after the snapshot's last commit; `content`: the last migration creating an object the snapshot holds) and replays the files after the earlier one; every object keeps a `-- @src` origin, so H's rows cite the snapshot line or the replayed migration line. `lane=ddl` is a reconstruction (on the measured repo it recovered 52 of the 124 FKs the snapshot holds, because helper functions still build some DDL): its §1 rows are candidates to read. A non-zero `not understood` or `unresolved ${...}` count names files to read by hand. **Entity-first repos** (no SQL migrations, so H prints 0 tables): write the DDL dump from the lane table's last column to a file in `$RUN` (never in the repo), point `SCHEMA_SQL` at it and re-run H; grep 1c counts the scalar `uuid` references such repos use.

**§7 follow-up.** For each `§7` row H prints, list the column's writers. Use `rg -n -w '<column>|<camelCaseColumn>' "${N[@]}" "${X[@]}" .` and read which update paths set it and how often.

**R2 — the SQL the ORM really emits** settles more §2 candidates than any amount of reading. Turn on the ORM's query logger from the `n-plus-one-scan` lane table, run the e2e or integration suite, save the log, and re-run H with `QLOG=<log>`. H then reads every logged `FROM … WHERE … ORDER BY` against the index map.

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, Postgres 16, 376 TS migrations, 125 of them building DDL with `${…}`). Before H0, H parsed 105 FKs and 813 indexes from the migration text and printed §1 86 rows (all stale: FKs later rewritten as tenant composites, dropped by name), §2 10 (4 false: a partial index that serves, an index created through `${this.x}`, an interpolated `${where}`), §4 21 (19 stale: one migration drops them in a loop over a module-level list). With H0 (snapshot horizon `content` = 5 files before HEAD, `git` = 2; 5 replayed, 14 statements, 0 not understood) H reads 124 FKs and 976 indexes in 291 tables in 3.7 s: §1 **0** rows (29 composite FKs served by an index led by their non-tenant column, plus partial `WHERE fk IS NOT NULL` indexes, which serve the check), §2 9 rows + 1 UNKNOWN line (16 statements whose whole WHERE is `${where}`), §4 2. Grep 2c went from 109 lines (type declarations, writes, YAML alert rules) to 18, every one a poll or claim filter; grep 1c counts 397 scalar `uuid` references in 127 files. On the fixtures every seeded row stays (`slow-marketplace` SM-IDX-01/02; `node-api`'s three NAPI-PERF-04 paths; `half-built-crm` 3 FKs; `vuln-fullstack` 4 `@relation` fields), and `slow-marketplace`'s two outbox/webhook polls now print `PARTIAL-CANDIDATE` (their partial index serves them) instead of `NO-INDEX`.

Earlier measurement (2026-10-02) on the same repo, 294 TS migrations, H ran in 1.5 s. It parsed 72 FKs and 711 live indexes in 245 tables. The output: §1 61 FK columns with no leading index, 42 of them second in a `(tenant_id, fk, …)` composite; §2 5 raw-SQL paths; §3 2; §4 18 left-prefix duplicates; §7 6. Two parser fixes came from that run. Skipping `down()` bodies raised the live-index count from 646 to 711 and removed false §1 rows. Dropping comment lines removed V1-reference SQL quoted in doc comments. Grep 6 went from 148 to 95 lines once `new Date(` and comment lines were excluded, 2a from 518 to 464, and grep 8 from 2 (prose saying "partition of") to 0 once it matched only DDL. 2c printed 79 and 4 printed 415 entity-declared indexes. On the fixtures, H's §2 rows on `node-api` are the three paths `NAPI-PERF-04` names (`orders.customer_id` + sort, the `tenant_id` sort, `order_items.order_id`). `half-built-crm` gives 3 unindexed FKs (SQLite) and `vuln-fullstack` 4 Prisma `@relation` fields with no `@@index`.

## From candidate to finding

1. **Context first** (whole-repo runs, once). Build the table list with a **growth class** for each table: append-only or event, per-tenant growing, or bounded lookup. Use `reltuples` when live; otherwise the entity's role. Build the entry points that reach each repository, with a call rate where APM or access logs give one. Otherwise rank list, search, export and worker-poll paths first.
2. **Read the code with these questions.** Is the path reachable from a route, job or consumer, and how often does it run? Which predicate set does the query really send (R2), including filters a base repository or global filter adds (`tenant_id`, `deleted_at IS NULL`)? For each column, is it equality or range? Which columns does it sort by? Does it `LIMIT`? What is the table's growth class? Is the table write-hot? On the FK side, is the parent ever hard-deleted, or its key updated (cascade paths included)?
3. **Restate the claim** in the sentence of [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 1. Then run its seven gates. Gate 3 (engine and version) clears more candidates here than any other: InnoDB's FK index, PG 18 skip scan, an ORM that indexes FKs.
4. **Grade.** **high**: a Seq Scan (or an FK check scan) proven by plan on a production-sized, growing table on a request or worker path. **medium**: the same shape proven statically on a growing table with no plan yet (Unconfirmed until it has one), or a §3 sort that a `LIMIT` cannot stop early. **low**: hygiene (§4, §5, §7) and bounded tables. Index findings are never BLOCKERs: the fix waits for the worth-it verdict.

**3,000 hits.** Grep 2a alone printed 464 lines on the measured repo. When a list runs past what can be read:
- (a) Intersect it with the files that import the data layer (`rg -l` on grep 0's ORM names).
- (b) Group the rows by **(table, leading predicate column)**. H already prints raw SQL that way. For ORM code, group by entity plus filter keys, using `rg -o` on the call line.
- (c) Rank the groups by entry-point reachability (route, worker and cron first) and by the table's growth class.
- (d) Read the top 30 groups fully. One decision covers every member of a group that shares the table and predicate set.
- (e) Prefer the bulk oracle: capture the e2e suite's query log once and feed it to H (R2). That decides every logged query mechanically.
- (f) List the rest in the ledger as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | DB id · standard | Default |
|---|---|---|---|
| 1 | FK column with no index leading with it (Postgres, SQLite; ORM-conditional) | DB-12 · DATA-5 · CWE-1067 | medium (high when a parent delete or join path is hot) |
| 2 | Filter or join path with no index whose leading columns match | DB-12 · DATA-5 · CWE-1067 | medium (high on a hot path, proven) |
| 3 | Composite in the wrong order: range before equality; sort not served | DB-12 · CWE-1067 | medium |
| 4 | Duplicate, left-prefix-redundant or invalid index | DB-14 · CWE-1089 | low |
| 5 | Unused index (live only, ≥ 30 days, every node) | DB-14 · CWE-1089 | low |
| 6 | Intended non-sargable predicate with no expression or partial index | DB-13 · DATA-5 · CWE-1067 | medium |
| 7 | Write amplification: an index on a column the hot update path writes (HOT disabled), or index count on a write-hot table | DB-14 · CWE-1089 | medium (live HOT share decides) |
| 8 | Lock-manager pressure from partitions × indexes (live only) | DB-14 | medium · always `[report-flagged]` |

### 1. FK column with no index leading with it

```
BAD:   ALTER TABLE order_items ADD CONSTRAINT … FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE;
       CREATE INDEX order_items_tenant_order_idx ON order_items (tenant_id, order_id);   -- order_id is second: the RI check cannot seek
GOOD:  CREATE INDEX CONCURRENTLY order_items_order_id_idx ON order_items (order_id);    -- or lead the composite with order_id
```
Candidates: H's §1 rows on Postgres or SQLite; on entity-first repos, grep 1 checked against grep 4 and the lane table. H compares the FK's columns with an index's leading columns **as a set**, accepts a partial index whose only predicate is `<fk column> IS NOT NULL` (the check's `=` implies it), and counts a composite `(tenant_id, x)` served by an index led by `x` instead of listing it. A row is a finding when the child grows **and** a production path deletes the parent or updates its key (each such statement makes the FK trigger look up the child rows by that column), or the column is a join or filter key on a hot path. `[2nd column of …]` rows are the multi-tenant shape. On PG ≥ 18 with few tenants, skip scan may already serve the check: prove it with a plan, do not assume either way. Never a BLOCKER; the fix is a worth-it verdict, then `/add-migration`. **Proof — plan shape:** `EXPLAIN SELECT 1 FROM <child> WHERE <fk> = <sampled id>` shows a Seq Scan before and an Index (Only) Scan after. On a confirmed non-production copy, `BEGIN; EXPLAIN (ANALYZE) DELETE FROM <parent> WHERE id = <id>; ROLLBACK;` prints the FK trigger's own time (the PG "Using EXPLAIN" docs: each trigger's total time is shown separately; a deferred constraint trigger is not measured), which drops after the fix. Precedents: `precedents/performance.md` § 8, § 9.

### 2. Filter or join path with no matching index

```
BAD:   SELECT * FROM orders WHERE customer_id = $1 ORDER BY created_at DESC   -- only orders(tenant_id) exists
       em.find(Payout, { status: 'pending' }, { orderBy: { createdAt: 'asc' } })  // worker poll, every 5 s
GOOD:  CREATE INDEX … ON orders (customer_id, created_at DESC);
       CREATE INDEX … ON payouts (created_at) WHERE status = 'pending';            -- partial: the poll reads one slice
```
Candidates: H's `NO-INDEX` rows (raw SQL and logged queries), its `PARTIAL-CANDIDATE` rows (only a partial index leads with the column: it serves the query when the query's predicate implies the index's `WHERE` — read both), its `UNKNOWN` rows (a WHERE built from `${…}`: read the builder, which often carries `tenant_id`), grep 2a–2c, and Spring Data finders (`findByCustomerIdAndStatusOrderByCreatedAtDesc` spells `customer_id`, `status`, `created_at`). It is a finding when the table grows with users, orders, events or tenants, the predicate is selective, and the path is hot. Include the filters a base repository adds: a `tenant_id` the global filter prepends changes which composite serves the query. **Proof — plan shape** on production-shaped data (seed with `generate_series` to the row estimate, then `ANALYZE`). Before: `Seq Scan` with `Rows Removed by Filter` ≫ rows returned. After: `Index Scan using <new index>`. The test shape per stack is `proof-oracles.md` § "Plan shape"; the fix must survive V2's variants there (every filter combination and sort, first and deep page, case-insensitive match, parameter type, generic plan). `hypopg` makes the before and after a pure plan test without a build. Its plans are estimates, and `EXPLAIN ANALYZE` ignores hypothetical indexes. Precedents: `precedents/performance.md` § 4, § 7, § 12.

### 3. Composite in the wrong order; sort not served

```
BAD:   CREATE INDEX … ON orders (created_at, tenant_id);   -- WHERE tenant_id = $1 AND created_at > $2: range first, equality second
       CREATE INDEX … ON orders (tenant_id);               -- WHERE tenant_id = $1 ORDER BY created_at DESC LIMIT 20: sorts every tenant row
GOOD:  CREATE INDEX … ON orders (tenant_id, created_at DESC);   -- equality, then the range or sort column
```
Candidates: H's `§3` rows (a composite led by a time-like column) and `SORT` rows (filter served, sort not). It is a finding when the query mixes equality and range in the wrong order, or sorts and limits a large per-key set the index does not order. **Proof — plan shape:** before, a `Sort` or `Incremental Sort` node over many rows, or an index scan with a `Filter` doing the range. After, no `Sort`, and the `Limit` stops early. Read `precedents/performance.md` § 11 (skip scan) before calling a leading column useless.

### 4. Duplicate, left-prefix-redundant or invalid index

```
BAD:   CREATE INDEX memberships_tenant_idx ON memberships (tenant_id);
       ALTER TABLE memberships ADD CONSTRAINT memberships_tenant_user_unique UNIQUE (tenant_id, user_id);   -- serves tenant_id alone too
GOOD:  keep the unique constraint; drop the plain index after the checks below
```
Candidates: H's `§4` rows, live L3, and L4's invalid indexes. It is a finding when the shorter index has the same method, no predicate and no expression, backs no constraint, and the wider one leads with all its columns. On InnoDB, also check that the shorter one is not the only index able to enforce an FK (`indexing-strategy.md` § "Foreign keys — the engines differ, and the advice inverts"). Every row is `report-with-proposal`: the drop is proposed and never applied here, and it routes through `/migration-review`. **Proof — catalog:** both `pg_get_indexdef` lines, the prefix relation, and `backs_constraint = false`. On a confirmed non-production copy, `hypopg_hide_index(<oid>)` (or MySQL `ALTER INDEX … INVISIBLE`) and the plans of the queries that used it pick the wider index.

### 5. Unused index (live only)

Candidates: L4's second query. It is a finding only when all of these hold: `idx_scan = 0` over a window of at least 30 days that spans month-end jobs (L1), on **every** node including replicas (the counters are per node), and the index backs no PK, unique, exclusion or FK constraint. **Proof — catalog:** the L1 window plus the zero counts per node. Without a reachable database, or with a window under 30 days, the class is `blocked`, never `checked`. Precedents: `precedents/performance.md` § 5, § 10.

### 6. Intended non-sargable predicate with no expression or partial index

```
BAD:   WHERE lower(email) = lower($1)                 -- only a plain (email) index exists
       { email: { $ilike: escapeLike(email) } }       // case-insensitive exact match; no lower(email) index or citext
GOOD:  CREATE UNIQUE INDEX … ON users (lower(email));   -- and query with lower(email) = lower($1)
       CREATE INDEX … ON orders (tenant_id, created_at) WHERE deleted_at IS NULL;   -- the soft-delete filter every query repeats
```
Candidates: grep 6. It is a finding when the predicate is intended (the product wants case-insensitive email login, or the global filter adds `deleted_at IS NULL` everywhere), no expression, partial or `citext` alternative exists, and the path is hot on a growing table. When the right fix is to rewrite the predicate, the row belongs to `query-shape-scan` §4 instead. A partial index serves only queries that repeat its predicate exactly. **Proof — plan shape** with the real predicate: before, `Seq Scan … Filter: (lower(email) = …)`; after, `Index Scan using <expression index>`. Precedent: `precedents/performance.md` § 13.

### 7. Write amplification on a write-hot table

```
BAD:   CREATE INDEX customers_last_order_idx ON customers (tenant_id, last_order_at);   -- set on every order: no HOT update on customers
GOOD:  drop it if no hot read needs it; serve the read from orders; or keep it and record the HOT and write-p95 cost in the verdict
```
Candidates: H's `§7` rows (an index containing `updated_at`, `last_*`, `*_count`, `*_seen_at`, heartbeat-style columns), the §7 follow-up's writer list, and live L5. It is a finding when an update path that runs per request or per event writes an indexed column of a table whose HOT share is low (L5), and no read the index serves outweighs the cost (`indexing-strategy.md` § "Input 3 — the write cost, on the specific write path"). Without live statistics the row is `[report-flagged]`: the unproven link is the write rate. **Proof:** the L5 HOT share before and after on a confirmed non-production copy under a `pgbench` script that replays the update (`-f update.sql`), plus write p95 inside the noise band. Precedent: `precedents/performance.md` § 12.

### 8. Lock-manager pressure from partitions × indexes (live only)

A query that cannot prune partitions locks every partition and every index on each one. Past the per-backend fast-path slots, those locks go through the shared lock manager, and concurrency shows as `LWLock:LockManager` waits. (The research catalog's R18 cites postgres.ai, 2025, for the slot sizing; it is not settled here, so measure it.) Candidates: grep 8 and L6. **Always `[report-flagged]`**: the effect exists only under concurrency. The row names the parent, its partition and index counts, the hot query, and whether its predicate carries the partition key. **Proof:** L6 sampled during load. Many `slow_path_locks` on the hot query's backends, plus non-zero `LockManager` waits, before. After pruning (the partition key in the predicate) or fewer indexes, both fall. `N/A (no partitioned table)` is the usual ledger line.

## Output

```
index-coverage-scan — lanes: postgres 16 (docker-compose.yml:9), mikro-orm 6.6 (apps/api/package.json:37); live lane: not run (no reachable DB)

Findings: 3   (Verification: 9 candidates → 3 findings · 3 unconfirmed · 2 hardening · 0 pre-existing · 1 refuted)

1. src/data/order-reads.js:19 · orders                              [report-with-fix]  high
   §2 SELECT * FROM orders WHERE customer_id = $1 ORDER BY created_at DESC — only orders_tenant_idx (tenant_id)
   exists (migrations/0004_orders.sql:31). GET /admin/customers/:id/orders (src/http/customers.js:26); orders grows per
   tenant. Measured: EXPLAIN (ANALYZE) on a generate_series seed at the row estimate → Seq Scan, Rows Removed
   by Filter ≫ rows. Fix: (customer_id, created_at DESC) after the worth-it verdict → /add-migration
   (CONCURRENTLY). DB-12 · DATA-5 · CWE-1067

2. migrations/0042_items.ts:54 · order_items.order_id               [report-flagged]  medium
   §1 FK to orders with only (tenant_id, order_id) — second column. Orders are hard-deleted by
   the purge job (src/jobs/purge.ts:31), so each delete scans order_items. Unproven link: PG 16, so no skip
   scan; table size unknown (no DB). Probe: EXPLAIN SELECT 1 FROM order_items WHERE order_id = <id>.

3. migrations/0007_team.sql:12 · team_members_tenant_idx           [report-with-proposal]  low
   §4 (tenant_id) is a left prefix of team_members_tenant_user_key (tenant_id, user_id); backs no
   constraint. PROPOSED drop → /migration-review. CWE-1089

Class coverage:
  §1 FK without index        checked (14 hits → 1 finding, 9 hardening: parent never hard-deleted, 4 unconfirmed)
  §2 access path             checked (4 raw-SQL + 160 ORM sorted queries in 48 groups → 1 finding; 18 groups live, unreviewed)
  §3 composite order         checked (1 + 2 SORT rows → 0 findings)
  §4 duplicate / invalid     checked (5 hits → 1 finding; invalid indexes: blocked (no DB))
  §5 unused                  blocked (no reachable database; statistics window unknown)
  §6 expression / partial    checked (22 hits in 9 groups → 0 findings, 2 unconfirmed)
  §7 write amplification     checked (3 hits → 0 findings, 1 report-flagged)
  §8 lock manager            N/A (no partitioned table: grep 8 printed 0 lines)
```

`[report-with-fix]`: the access path, the missing index and the plan are all cited. `[report-flagged]`: one link is unproven (a row count, the write rate, the version-dependent plan, a hop through code not read), and the row names that link and its probe. `[report-with-proposal]`: hygiene whose fix is a proposed drop, never applied. The block lists **all eight** classes on every run:
- `checked (k hits → m findings)` only when the class's grep or query ran on a lane that is present;
- `N/A (<reason>)` only when the repo cannot have the class;
- `blocked (<reason>)` when the lane could not run — §5 and the live half of §4 and §7 without a database;
- groups that were never read appear as `Live, unreviewed`.

## False positives / gotchas

- **The index exists under another name**, or in a later migration, or in an ORM declaration H does not parse. Grep 4 and the live catalog decide. H is a map, not a verdict.
- **H reads statements per file, `create` before `drop`.** A file that drops and recreates the same index name can show a false gap: read it. H0's snapshot lane has no such order problem for the files before its horizon.
- **A rewritten FK.** `drop constraint <name>` removes the FK and index of that name, and an inline `references` FK carries Postgres's default name (`<table>_<cols>_fkey`). An FK added under another default (an ORM's `_foreign`) and dropped by that name is matched only when the DDL spells the name: H0's snapshot lane settles it.
- **Generated queries add predicates.** A global filter (tenant, soft delete) changes the leading column a query needs. Read the base repository before judging a composite.
- **Small and bounded tables** (countries, statuses, settings) are right to scan (`precedents/performance.md` § 7). Growth class first.
- **InnoDB, Django, Rails `t.references` and EF Core already index FKs** (`precedents/performance.md` § 9). PG 18 skip scan changes §1 and §3 verdicts (§ 11 there).
- **Advisor output is a candidate** (dexter, PgHero, splinter, an LLM): verify it with a plan (`precedents/performance.md` § 12).

## When to run

- On every diff that adds a query, a filter or sort option, a relation or FK, an index, or a migration. Run it on the changed files and on the tables they touch.
- On every whole-repo `/db-audit`, reporting all eight classes; the live lane runs when a database is reachable.
- Before `/optimize-query` or `@query-optimizer` on a slow path: this skill names the candidate, and they decide.

## Halt conditions

- Do not report a high or medium row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 8 says who verifies). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening or Refuted. Never drop them.
- Halt on any finding without the access path or FK `<file:line>`, the index list it was checked against, the engine and version, and the fix.
- Do not run anything in the live lane but the read-only set (§ "Live lane — read-only by construction") unless the user has confirmed a non-production target in this session. Never `EXPLAIN ANALYZE` a production statement.
- Do not state a cost (rows scanned, ms, speed-up) that no tool produced. Label every number `measured` or `estimated` ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 1).
- Do not propose a new index without routing it through the worth-it verdict, and never apply a drop: propose it, then `/migration-review`.
- Do not print "no index issues" without the class-coverage block. A class whose lane did not run is `blocked`, never `checked`.

## Related

- [`refute-before-report.md`](../../../../snippets/refute-before-report.md), [`precedents/performance.md`](../../../../snippets/precedents/performance.md) (§ 4–§ 14 cover plans and indexes) and [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Plan shape" (the failing-first test per stack) and § "Class variants (data)" V2 (what an index fix must survive).
- `ai/patterns/indexing-strategy.md` — the worth-it verdict, index shapes, the InnoDB FK-index inversion.
- `@query-optimizer`, `/optimize-query` — decide a single query's plan and index; `/add-migration` and `migration-safety` — build it without blocking writes; `migration-rehearsal` — time it on a restored copy.
- `query-shape-scan` (non-sargable rewrites, unbounded reads), `n-plus-one-scan` (the ORM query-log lanes), `schema-integrity-scan` (§1 there: a relation with no FK constraint at all).
- `/db-audit` dispatches this skill and folds its class block into the ledger. `/db-fix` closes the findings, failing first on the plan-shape oracle.
- `@database-optimizer` — bloat, autovacuum and memory, which this skill does not judge.
