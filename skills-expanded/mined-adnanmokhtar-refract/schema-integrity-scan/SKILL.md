---
name: schema-integrity-scan
description: Schema-integrity detector — relations with no database FK, FKs with no explicit ON DELETE, natural keys with no unique constraint, money as float, instants without a time zone, missing NOT NULL or CHECK, int32 keys, auto schema sync in production, soft-delete bypasses, PII storage, gapless numbers from a sequence.
kind: skill
pack: database
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: schema-integrity-scan

## Premise

An application rule that the database does not enforce is a rule every write path must remember: the bulk import, the admin script, the second service, and the Rails `update_all` or Django `QuerySet.update()` that skips validation. Each such gap leaves wrong data behind: orphan rows, two accounts on one email, a ledger off by a cent, an expiry that moves with the server's time zone, an id column that stops at 2³¹−1, a deleted row that comes back in an export. The data is wrong long before anyone notices, and fixing it later means a data migration, not a patch. Across 12 Rails apps, 24 % of application-level constraints had no database counterpart (Yang et al., ICSE 2020, via the research catalog). This skill finds where **the guarantee the code relies on is missing from the schema**.

**Every finding cites the column or constraint at `<migration-or-schema:line>` + the code that relies on the guarantee (`<file:line>`) or the class rule it breaks + the engine and version + the fix.** A grep hit is never a finding. Nothing is reported as clean without the class-coverage block (§ Output).

Most classes here are **static facts**: a constraint, type or setting that is absent. Under [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2 (gate 6), a static fact passes on the full trace, with both ends cited: where the guarantee should live, and the code that depends on it. A failing-first test from [`proof-oracles.md`](../../../../snippets/proof-oracles.md) is still the fix's first step.

## Boundaries

- **Tenant predicates, RLS and cross-tenant constraints** belong to security's `@tenant-isolation-reviewer` when the security pack is installed. Without it, `/db-audit` prints `owner: security (not installed)` in the ledger. A global unique key on a tenant table is reported here (§3) for its integrity half, and cross-linked.
- **Races on natural keys and money values** belong to security's `logic-race-scan` when installed: §7 (find-or-create without a unique index) and §2 (money stored in a binary float). This skill anchors the **schema** half (the missing constraint, the float column); that skill anchors the code path. One root cause is one finding, deduped by `<file:line>` with both cited. Without the security pack, this skill reports the schema half only, and says so.
- **The PII data flow** (who reads and exports it, logs, consent) belongs to security's `@data-privacy-reviewer` when installed. §10 here owns the storage mechanics: classification, retention mechanism, erasure path.
- **Convention drift** across tables (naming, mixed time-zone handling, charset, collation) belongs to `schema-consistency-audit`. **Entity-vs-database drift** belongs to `schema-diff`; §8 here owns only auto-sync reachable in production. **Adding** a constraint to a populated table without locking it (`NOT VALID` then `VALIDATE`) belongs to `migration-safety` and `/add-migration`. **The index** on an FK belongs to `index-coverage-scan` §1.

## Adapt to the codebase

Read the engine, its version and the ORM version first: run the context block in [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2 (G1–G3). The ORM query logger, for proof tests, is in `n-plus-one-scan` § "Adapt to the codebase — the shared ORM lane table". This table holds what changes an integrity verdict.

| Lane | DB FK switched off by | Default type of a timestamp (Postgres) | Soft-delete scope · its escapes | Auto-sync switch (§8) |
|---|---|---|---|---|
| **MikroORM** | `createForeignKeyConstraint: false` on the relation; `schemaGenerator.createForeignKeyConstraints: false` (both read in 6.6.16 source) | `Date` → `timestamptz` (6.6.16 source). 7.x defaults `forceUtcTimezone: true`, which shifts data written as local time on v6 | `@Filter` · `filters: false`, raw `em.execute` / `qb.raw` (raw carries no ORM filter) | `getSchemaGenerator().updateSchema()`, `schema:update --run` |
| **TypeORM** | `createForeignKeyConstraints: false` | `@CreateDateColumn()` → `timestamp` without tz (research catalog DB-07) | `@DeleteDateColumn` · `withDeleted`, raw `query()` | `synchronize: true`, `dropSchema: true` |
| **Prisma** | `relationMode = "prisma"`: "Prisma ORM will not use foreign keys" (docs, read 2026-10-02) | `DateTime` → `timestamp(3)` unless `@db.Timestamptz` (docs, read 2026-10-02) | none built in (extensions; `$use` is gone in v7) · `$queryRaw` | `prisma db push`, `--accept-data-loss`, `migrate reset` |
| **Sequelize / Knex / Drizzle** | `constraints: false` (v6; v7 `@sequelize/core`: `foreignKeyConstraints: false`) / no `.references()` / no `.references(() => …)` | Sequelize `DATE` → `TIMESTAMP WITH TIME ZONE` (v6 docs, read 2026-10-02); Knex and Drizzle: read the migration SQL | `paranoid: true` · `paranoid: false`, raw | `sync({ alter \| force })` / — / `drizzle-kit push` |
| **Django** | `db_constraint=False` | read `sqlmigrate`; with `USE_TZ = False` values are naive and the connection `timezone` follows `TIME_ZONE` (databases docs, read 2026-10-02) | custom manager · `all_objects`, `_base_manager`, `raw()` | — (`migrate` only); `--run-syncdb` |
| **SQLAlchemy / Alembic** | relationship with no `ForeignKey()` | `DateTime(timezone=True)` needed for `timestamptz` | none built in | `metadata.create_all()` |
| **Rails** | `belongs_to` with no `foreign_key: true` / `add_foreign_key` | `t.datetime` → `timestamp without time zone` unless `PostgreSQLAdapter.datetime_type = :timestamptz` (Rails API docs, read 2026-10-02) | `default_scope` / discard · `unscoped` | `db:schema:load` in a deploy step |
| **Laravel** | `foreignId()` with no `->constrained()` | `->timestamp()` makes a `TIMESTAMP` (on MySQL it ends in 2038); `->timestampTz()` adds the zone (Laravel 12.x docs, read 2026-10-02) | `SoftDeletes` · `withTrashed()`, `DB::table` | `migrate:fresh`, `db:wipe` |
| **Hibernate / JPA** | `@ForeignKey(ConstraintMode.NO_CONSTRAINT)` | read the generated DDL; `hibernate.jdbc.time_zone` | `@SQLRestriction` (`@Where` is gone in 7.x) · native queries | `ddl-auto` / `hbm2ddl.auto` `update \| create` |
| **GORM / EF Core** | `DisableForeignKeyConstraintWhenMigrating: true` / a scalar `…Id` with no navigation and no `HasForeignKey` | read the generated DDL | `gorm.DeletedAt` · `Unscoped()`, `Raw` / `HasQueryFilter` · `IgnoreQueryFilters()` | `AutoMigrate` at boot (additive) / `EnsureCreated()` |
| **Engines** | MySQL `foreign_key_checks = 0` (re-enabling does not validate existing rows), MyISAM ignores FKs; SQLite enforces FKs only on connections that ran `PRAGMA foreign_keys = ON`; Postgres 18 `NOT ENFORCED` (`precedents/data.md` § 27) | MySQL `TIMESTAMP` ends 2038-01-19 and converts by session `time_zone`; `DATETIME` does not | — | — |

A row the table marks "read the generated DDL" is settled by the dump command in `index-coverage-scan` § "Adapt to the codebase", never by memory.

## Pre-flight

Run as **one** script from the repo root. **H** is the schema map, which feeds §1–§7, §9 (soft-delete reads), §10 and §11. Grep **N** feeds detector **§N**. Every `rg` names its path (`.`): given none, `rg` reads stdin whenever stdin is a pipe, which is a silent zero-hit run. A lane that prints `No files were searched` is an `N/A` reason. `rg` exit code 2 is a failed grep.

```bash
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/target/**' -g '!**/.venv/**' -g '!**/*.min.*' -g '!*.md' -g '!ai/**' -g '!docs/**'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,testdata,seeds,seeders,generated,__generated__,temp,locales}/**'
   -g '!**/*.{spec,test,e2e-spec,mock,stories,test-data,doc}.*' -g '!**/{*_test,test_*}.*' -g '!**/*.{snap,lock,map,po,json}')
C='^(?!\s*(?://|\*|/\*|#|--))[^\n]*?'      # the hit is not on a comment line
M='price|amount|total|sub_?total|balance|cost|fee|tax|discount|credit|debit|payout|refund|salary|commission'

# H0. The schema map (index-coverage-scan/scripts/schema-map.py; index-coverage-scan § Pre-flight H0 says what it holds): a MikroORM
#     snapshot plus the migrations after its horizon, else every migration's up() with `${…}` names resolved.
SM=.claude/skills/index-coverage-scan/scripts/schema-map.py; RUN=$(mktemp -d "${TMPDIR:-/tmp}/db-scan.XXXXXX")
if command -v python3 >/dev/null 2>&1 && [ -f "$SM" ] && python3 -I -B "$SM" . > "$RUN/schema.sql"; then export SCHEMA_SQL="$RUN/schema.sql"; grep '^-- schema-map [lhr]' "$SCHEMA_SQL"; else unset SCHEMA_SQL; echo 'schema-map NOT-RUN (python3 or schema-map.py absent): H parses the migrations; ${...} names stay invisible'; fi

# H. Schema map: CREATE/ALTER/DROP TABLE and CREATE UNIQUE INDEX (SQL, and SQL inside addSql(), queryRunner.query(),
#    knex.raw()), Prisma models, Django models, Rails db/schema.rb, in path order, skipping down()/downgrade bodies, then
#    H0's map instead of the files it covers. It applies ALTER COLUMN TYPE / SET NOT NULL / DROP COLUMN / DROP TABLE.
python3 - . <<'PY'
import os, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else '.'
SKIP = {'node_modules','vendor','dist','build','target','.git','.venv','coverage','test','tests','__tests__','spec','e2e','__mocks__','mocks','fixtures','__fixtures__','testdata','.next','tmp'}
SQ = os.environ.get('SCHEMA_SQL') or ''; COV = re.findall(r'(?m)^-- schema-map covers (.+)$', open(SQ, encoding='utf-8').read()) if SQ else []
I = r'[\\"`\[]*(?:\w+[\\"`\]]*\.[\\"`\[]*)?(\w+)[\\"`\]]*'
RF = r'\s*(?:\([^)]*\))?(?:[^,;]*?(\bon\s+delete\s+(\w+(?:\s+(?:null|default|action))?)))?'   # past the referenced columns to ON DELETE
def bal(s, i):
    d = 0
    for j in range(i, len(s)):
        d += (s[j] == '(') - (s[j] == ')')
        if not d: return j
    return len(s) - 1
def ecols(q): return [x.lower() for x in re.findall(r'[a-z_]\w*', re.sub(r'\b\w+\s*\(', '(', re.sub(r'::\s*\w+(?:\s+(?:varying|precision))?', '', re.sub(r"'[^']*'", '', q))), re.I) if x.lower() not in ('null', 'true', 'false', 'and', 'or', 'not', 'is', 'nulls', 'distinct')]
def split(s):
    out, d, cur = [], 0, ''
    for ch in s:
        d += (ch == '(') - (ch == ')')
        if ch == ',' and d == 0: out.append(cur); cur = ''
        else: cur += ch
    return out + [cur]
def names(s): return [re.match(r'[\\"`\[]*(\w*)', q.strip()).group(1).lower() for q in split(s) if q.strip()]
col, fks, uq, chk, raws, softuq = {}, {}, {}, {}, [], set()      # col[(t,c)] = [type, notnull, default, at]; fks[name] = (t, cols, parent, on delete, at)
def setcol(t, c, spec, at):
    m = re.match(r'(?is)\s*((?:double\s+precision\b|character\s+varying\b|timestamp(?:\s*\(\d\))?(?:\s+with(?:out)?\s+time\s+zone)?\b|[\w.]+)(?:\s*\([^)]*\))?(?:\s*\[\])?)(.*)', spec)
    if m: col[(t.lower(), c.lower())] = [m.group(1).lower(), bool(re.search(r'(?i)\bnot\s+null\b|\bprimary\s+key\b', m.group(2))), (re.search(r'(?i)\bdefault\s+(\S+)|\b(generated\b[^,]*identity|auto_?increment)\b', m.group(2)) or [None])[0], at]
    if re.search(r'(?i)\bunique\b|\bprimary\s+key\b', spec): uq.setdefault(t.lower(), []).append([c.lower()])
    if re.search(r'(?i)\bcheck\s*\(', spec): chk.setdefault(t.lower(), set()).add(c.lower())
    r = re.search(r'(?is)\breferences\s+' + I + RF, spec)
    if r: fks['%s_%s_fkey' % (t.lower(), c.lower())] = (t.lower(), [c.lower()], r.group(1).lower(), (r.group(3) or '').lower(), at)
files = sorted(os.path.join(dp, f) for dp, dns, fns in os.walk(R) for f in fns if not dns.__setitem__(slice(None), [d for d in dns if d not in SKIP])
               and re.search(r'\.(sql|prisma|ts|js|mjs|py|rb|php|java|kt|go|cs)$', f) and not re.search(r'\.(spec|test|e2e-spec|mock|stories)\.', f)) + [SQ][:bool(SQ)]
for p in files:
    t = open(p, encoding='utf-8', errors='replace').read().replace('\\"', '"'); rel = SQ if p == SQ else os.path.relpath(p, R)
    def ln(pos):                                                                  # H0's `-- @src file:line` markers name the origin
        k = t.rfind('-- @src ', 0, pos) if p == SQ else -1
        if k < 0: return '%s:%d' % (rel, t.count('\n', 0, pos) + 1)
        e = t.find('\n', k); f, _, l = t[k + 8:e].rpartition(':'); return '%s:%d' % (f, int(l) + t.count('\n', e + 1, pos))
    if any(rel == c or c.endswith('/') and rel.startswith(c) for c in COV): continue        # H0's map holds this file's DDL
    if p != SQ and not re.search(r'(?i)migrat|(^|/)(scripts?|seeds?|seeders?|ai|docs?)/', rel):        # raw SQL in code: §9 needs it
        for m in re.finditer(r'(?is)\b(?:from|join)\s+' + I + r'\b(?!\s*\()', t):
            if re.match(r'\s*(\*|//|#|--)', t[t.rfind('\n', 0, m.start()) + 1:m.start()]): continue
            w = re.split(r';|["\'`]\s*[+),;]', t[m.start():m.start() + 700])[0]
            if re.search(r'(?i)\b(select|update|delete|where)\b', t[max(0, m.start() - 400):m.start() + 200]): raws.append((m.group(1).lower(), w, ln(m.start())))
    if p.endswith('.prisma'):
        pg = re.search(r'provider\s*=\s*"postgresql"', t)
        for mm in re.finditer(r'(?ms)^model\s+(\w+)\s*\{(.*?)^\}', t):
            b = mm.group(2); tb = (re.search(r'@@map\("(\w+)"\)', b) or mm).group(1).lower()
            fm = {f.group(1): (re.search(r'@map\("(\w+)"\)', f.group(2)) or [None, f.group(1)])[1].lower() for f in re.finditer(r'(?m)^\s*(\w+)\s+\w+\??([^\n]*)', b)}
            for f in re.finditer(r'(?m)^\s*(\w+)\s+(\w+)(\??)([^\n]*)', b):
                n, ty, opt, rest = f.group(1), f.group(2), f.group(3), f.group(4)
                if n.startswith('@@') or re.match(r'[A-Z]', ty) and ty not in ('String','Int','BigInt','Float','Decimal','DateTime','Boolean','Json','Bytes'): continue
                if ty == 'DateTime' and pg and 'Timestamptz' not in rest: ty = 'timestamp(3)'
                col[(tb, fm[n])] = [ty.lower(), not opt, (re.search(r'@default\(([^)]*\)?)\)', rest) or [None, None])[1], ln(mm.start(2) + f.start())]
                if re.search(r'@(unique|id)\b', rest): uq.setdefault(tb, []).append([fm[n]])
            for f in re.finditer(r'(?m)^\s*\w+\s+(\w+)\??\s+@relation\(([^)]*fields:\s*\[([^\]]*)\][^)]*)\)', b):
                fks['%s#%d' % (tb, len(fks))] = (tb, [fm.get(x, x.lower()) for x in re.findall(r'\w+', f.group(3))], f.group(1).lower(), (re.search(r'onDelete:\s*(\w+)', f.group(2)) or [None, ''])[1].lower(), ln(mm.start(2) + f.start()))
            for f in re.finditer(r'@@(unique|id)\(\s*(?:fields:\s*)?\[([^\]]*)\]', b): uq.setdefault(tb, []).append([fm.get(x, x.lower()) for x in re.findall(r'\w+', f.group(2))])
        continue
    if p.endswith('schema.rb'):                                                                       # Rails db/schema.rb (Prisma above, Django below)
        for m in re.finditer(r'(?s)create_table "(\w+)"([^\n]*)\n(.*?)\n  end\b', t):
            tb = m.group(1).lower(); idt = re.search(r'id: :(\w+)', m.group(2))
            col[(tb, 'id')] = [idt.group(1) if idt else 'bigint', True, None, ln(m.start())]
            for f in re.finditer(r't\.(\w+)\s+"(\w+)"([^\n]*)', m.group(3)):
                if f.group(1) != 'index': col[(tb, f.group(2).lower())] = [f.group(1).replace('datetime', 'datetime(rails)'), 'null: false' in f.group(3), (re.search(r'default: ([^,\n]+)', f.group(3)) or [None, None])[1], ln(m.start(3) + f.start())]
            for f in re.finditer(r't\.index \[([^\]]*)\][^\n]*unique: true', m.group(3)): uq.setdefault(tb, []).append(re.findall(r'"(\w+)"', f.group(1)))
        for m in re.finditer(r'add_foreign_key "(\w+)", "(\w+)"([^\n]*)', t):
            c = re.search(r'column: "(\w+)"', m.group(3)); od = re.search(r'on_delete: :(\w+)', m.group(3))
            fks['%s#%d' % (m.group(1), len(fks))] = (m.group(1), [c.group(1) if c else re.sub(r'ies$', 'y', m.group(2)).rstrip('s') + '_id'], m.group(2), od.group(1) if od else '', ln(m.start()))
        continue
    if re.search(r'(?m)^class\s+\w+\(.*\bmodels\.Model\b', t):                                       # Django models (Rails above, SQL DDL below)
        for cm in re.finditer(r'(?ms)^class\s+(\w+)\([^)]*\):(.*?)(?=^class\s|\Z)', t):
            dbt = re.search(r'db_table\s*=\s*[\'"](\w+)', cm.group(2)); tb = (dbt.group(1) if dbt else cm.group(1)).lower()
            for f in re.finditer(r'(?m)^\s+(\w+)\s*=\s*models\.(\w+)\(([^)\n]*)', cm.group(2)):
                ty = f.group(2).lower(); a = f.group(3)
                col[(tb, f.group(1).lower())] = [ty, 'null=True' not in a.replace(' ', ''), None, ln(cm.start(2) + f.start())]
                if 'unique=True' in a.replace(' ', ''): uq.setdefault(tb, []).append([f.group(1).lower()])
                if ty in ('foreignkey', 'onetoonefield'): fks['%s#%d' % (tb, len(fks))] = (tb, [f.group(1).lower() + '_id'], 'model', ('db_constraint=False ' if 'db_constraint=False' in a.replace(' ', '') else '') + (re.search(r'on_delete\s*=\s*models\.(\w+)', a) or [None, ''])[1].lower(), ln(cm.start(2) + f.start()))
            for f in re.finditer(r'UniqueConstraint\([^)]*fields\s*=\s*[\[(]([^\])]*)', cm.group(2)): uq.setdefault(tb, []).append(names(f.group(1).replace("'", '').replace('"', '')))
        continue
    if not re.search(r'(?i)\b(create\s+table|alter\s+table|create\s+unique\s+index|drop\s+table)\b', t): continue
    dn = re.search(r'(?m)^\s*(?:public\s+|override\s+)*(?:async\s+)?(?:def\s+|function\s+)?(?:down|downgrade)\s*(?:[(:]|$)|\bexports\.down\b|^--\s*\+(?:goose|migrate)\s+Down', t); t = t[:dn.start()] if dn else t
    for m in re.finditer(r'(?is)create\s+(?:unlogged\s+)?table\s+(?:if\s+not\s+exists\s+)?' + I + r'\s*\(', t):
        for q in split(t[m.end():bal(t, m.end() - 1)]):
            s = q.strip(); at = ln(m.end() + t[m.end():].find(s))
            k = re.match(r'(?is)(?:constraint\s+\S+\s+)?(primary\s+key|unique(?:\s+nulls\s+not\s+distinct)?)\s*\(([^)]*)\)', s)
            if k: uq.setdefault(m.group(1).lower(), []).append(names(k.group(2))); continue
            k = re.match(r'(?is)(?:constraint\s+(\S+)\s+)?foreign\s+key\s*\(([^)]*)\)\s*references\s+' + I + RF + r'.*$', s)
            if k: fks[(k.group(1) or '').strip('"`').lower() or '%s_%s_fkey' % (m.group(1).lower(), '_'.join(names(k.group(2))))] = (m.group(1).lower(), names(k.group(2)), k.group(3).lower(), (k.group(5) or '').lower(), at); continue
            k = re.match(r'(?is)(?:constraint\s+\S+\s+)?check\s*\((.*)\)', s)
            if k: chk.setdefault(m.group(1).lower(), set()).update(x.lower() for x in re.findall(r'\b([a-z_]\w*)\b', k.group(1))); continue
            k = re.match(r'(?is)[\\"`\[]*(\w+)[\\"`\]]*\s+(.*)', s)
            if k and k.group(1).lower() not in ('key', 'index', 'unique', 'primary', 'constraint', 'like', 'exclude'): setcol(m.group(1), k.group(1), k.group(2), at)
    for m in re.finditer(r'(?is)alter\s+table\s+(?:only\s+)?(?:if\s+exists\s+)?' + I + r'\s+([^;`]*)', t):
        tb, body = m.group(1).lower(), m.group(2)
        for a in re.finditer(r'(?is)\badd\s+(?:column\s+)?(?:if\s+not\s+exists\s+)?(?!constraint\b|primary\b|unique\b|foreign\b|check\b|index\b)[\\"`]*(\w+)[\\"`]*\s+((?:[^,(]|\([^)]*\))*)', body): setcol(tb, a.group(1), a.group(2), ln(m.start()))
        for a in re.finditer(r'(?is)\balter\s+column\s+[\\"`]*(\w+)[\\"`]*\s+(?:set\s+data\s+)?type\s+([\w ]+(?:\([^)]*\))?)', body):
            if (tb, a.group(1).lower()) in col: col[(tb, a.group(1).lower())][0] = a.group(2).strip().lower()
        for a in re.finditer(r'(?is)\balter\s+column\s+[\\"`]*(\w+)[\\"`]*\s+(set|drop)\s+not\s+null', body):
            if (tb, a.group(1).lower()) in col: col[(tb, a.group(1).lower())][1] = a.group(2).lower() == 'set'
        for a in re.finditer(r'(?is)\bdrop\s+column\s+(?:if\s+exists\s+)?[\\"`]*(\w+)', body): col.pop((tb, a.group(1).lower()), None)
        for a in re.finditer(r'(?is)\badd\s+(?:constraint\s+(\S+)\s+)?foreign\s+key\s*\(([^)]*)\)\s*references\s+' + I + RF, body): fks[(a.group(1) or '').strip('"`').lower() or '%s_%s_fkey' % (tb, '_'.join(names(a.group(2))))] = (tb, names(a.group(2)), a.group(3).lower(), (a.group(5) or '').lower(), ln(m.start()))
        for a in re.finditer(r'(?is)\bdrop\s+constraint\s+(?:if\s+exists\s+)?' + I, body): fks.pop(a.group(1).lower(), None)
        for a in re.finditer(r'(?is)\badd\s+(?:constraint\s+\S+\s+)?(?:primary\s+key|unique(?:\s+nulls\s+not\s+distinct)?)\s*\(([^)]*)\)', body): uq.setdefault(tb, []).append(names(a.group(1)))
        for a in re.finditer(r'(?is)\badd\s+(?:constraint\s+\S+\s+)?check\s*\((.*?)\)\s*(?:not\s+valid)?\s*(?:,|$)', body): chk.setdefault(tb, set()).update(x.lower() for x in re.findall(r'\b([a-z_]\w*)\b', a.group(1)))
    for m in re.finditer(r'(?is)create\s+unique\s+index\s+(?:concurrently\s+)?(?:if\s+not\s+exists\s+)?(?:\S+\s+)?on\s+(?:only\s+)?' + I + r'\s*(?:using\s+\w+\s*)?\(', t):
        e = bal(t, m.end() - 1)                                                       # nested expressions: lower(btrim(email)) keys on email
        if re.search(r'(?i)where[^;]*deleted', re.split(r'[;`]', t[e + 1:e + 300])[0]): softuq.add(m.group(1).lower())
        uq.setdefault(m.group(1).lower(), []).append([x for q in split(t[m.end():e]) for x in ecols(q)])
    for m in re.finditer(r'(?is)\bdrop\s+table\s+(?:if\s+exists\s+)?' + I, t):
        tb = m.group(1).lower(); uq.pop(tb, None); chk.pop(tb, None); softuq.discard(tb)
        for k in [k for k in col if k[0] == tb]: col.pop(k)
        for k in [k for k, v in fks.items() if v[0] == tb]: fks.pop(k)
tables = {t for t, _ in col}
NAT = r'^(email|email_?address|username|login|handle|phone|phone_?number|mobile|slug|sku|idempotency_?key|external_?id)$'
SKIPT = r'(^|_)(logs?|events?|messages?|notifications?|audits?|history|histories|snapshots?|items|lines|attempts?|sessions?|tokens?|outbox|jobs?|webhooks?|deliveries|imports?|exports?)($|_)'
MONEY = r'^(\w*_)?(price|amount|total|balance|cost|fee|fees|salary|revenue|commission|discount|tax|subtotal|credit|debit|payout|wage|refund|charge)s?(_\w*)?$|^[a-z]+(Price|Amount|Total|Balance|Cost|Fee|Discount|Tax|Refund)s?$'
FKC = {(t, x) for t, c, *_ in fks.values() for x in c}                                    # every column of a composite FK
PKT = max(set(v[0] for (t, c), v in col.items() if c == 'id') or {''}, key=lambda y: sum(1 for (t, c), v in col.items() if c == 'id' and v[0] == y)).split('(')[0]
LOGT = r'(^|_)(logs?|events?|audits?|history|histories|snapshots?|messages?|notifications?|attempts?|outbox|webhooks?|deliveries)($|_)'   # rows that outlive the parent (§ 25)
STR = r'(text|varchar|character\s+varying|string|charfield)'                     # a string *_id beside non-string primary keys
EXT = r'^(external|provider|stripe|remote|payment_intent|customer_ext|vendor|gateway|psp)\w*_id$|^(request|session|trace|correlation|idempotency|message|span)_id$'
out = lambda tag, s: print('  %-4s %s' % (tag, s))
print('schema-integrity map — %d tables, %d columns, %d FKs, %d unique keys' % (len(tables), len(col), len(fks), sum(map(len, uq.values()))))
ten, logs = [], []
for (t, c), (ty, nn, df, at) in sorted(col.items(), key=lambda x: (x[1][3].rpartition(':')[0], int('0' + x[1][3].rpartition(':')[2]))):
    if re.search(r'_id$', c) and (t, c) not in FKC and ty not in ('foreignkey', 'onetoonefield'):
        if c == 'tenant_id': ten.append(t)
        elif re.search(LOGT, t): logs.append(t)
        else: out('§1', '%s.%s %s no FK%s  %s' % (t, c, ty, '  [external-looking]' if re.match(EXT, c) or re.match(STR, ty) and not re.match(STR, PKT) else '', at))
    if re.match(NAT, c) and not re.search(SKIPT, t) and not any(c in x for k in uq.get(t, []) for x in k):
        out('§3', '%s.%s no unique key covers it%s  %s' % (t, c, '' if (t, 'tenant_id') not in col else '  [tenant table]', at))
    elif re.match(NAT, c) and (t, 'tenant_id') in col and [c] in uq.get(t, []): out('§3', '%s.%s unique WITHOUT tenant_id on a tenant table  %s' % (t, c, at))
    if re.match(MONEY, c) and re.match(r'(float|double|real|money|floatfield)', ty): out('§4', '%s.%s %s  %s' % (t, c, ty, at))
    if re.search(r'(_at|^created|^updated|^expires?|^deleted)$', c) and (re.match(r'timestamp(\(\d\))?(\s+without\s+time\s+zone)?$', ty) or ty in ('timestamp(3)', 'datetime(rails)')): out('§5', '%s.%s %s (no time zone)  %s' % (t, c, ty, at))
    if re.search(r'(^|_)(status|state|type|kind|role|stage|tier|plan|level)$', c) and re.match(r'(text|varchar|character varying|string|charfield)', ty) and c not in chk.get(t, set()):
        out('§6', '%s.%s %s, no CHECK/enum%s  %s' % (t, c, ty, '' if nn else ', nullable', at))
    if c == 'id' and re.match(r'(serial|integer|int|int4|smallint|mediumint|autofield)$', ty) and (df or '').lower() != 'autoincrement': out('§7', '%s.id %s  %s' % (t, ty, at))
    if re.search(r'(invoice|receipt|credit_?note|bill|voucher|fiscal)\w*_?(number|no|num|seq)$', c) and re.search(r'(?i)nextval|serial|identity|auto_increment|autoincrement', '%s %s' % (ty, df)): out('§11', '%s.%s from a sequence (%s)  %s' % (t, c, df or ty, at))
if ten: out('§1', 'tenant_id has no FK on %d tables: one decision (the tenancy policy), not %d rows' % (len(set(ten)), len(ten)))
if logs: out('§1', '%d *_id columns without an FK in %d log/event/history tables (precedents/data.md § 21, § 25): read the table list only if no policy names them' % (len(logs), len(set(logs))))
for t, c, par, od, at in fks.values():
    if not od or 'db_constraint' in od: out('§2', '%s.%s -> %s  ON DELETE %s  %s' % (t, ','.join(c), par, od or 'not stated (the engine or ORM default applies)', at))
    elif 'cascade' in od and re.search(r'^(users?|tenants?|accounts?|organi[sz]ations?|merchants?|customers?|companies|workspaces?)$', par) and re.search(r'invoice|payment|ledger|transaction|journal|audit|receipt|payout|refund|order', t): out('§2', '%s.%s -> %s  ON DELETE CASCADE into a record of fact  %s' % (t, ','.join(c), par, at))
soft = sorted({t for t, c in col if re.match(r'(deleted_?at|is_?deleted|deleted|archived_?at)$', c)})
print('§9 soft-delete tables: %s' % (', '.join(soft) or 'none'))
for t in soft:
    if t not in softuq and any(re.match(NAT, x) for k in uq.get(t, []) for x in k): out('§3', '%s: unique key on a natural column ignores soft delete (no WHERE deleted_at IS NULL)' % t)
for t, w, at in raws:
    if t in soft and not re.search(r'(?i)deleted|archived', w): out('§9', '%s read with no deleted predicate in the statement  %s' % (t, at))
PII = r'^(?!\w*_(?:id|prefix|type)$|(?:require|is|has|show|allow)_)(\w+_)?(e?mail\w*|phone\w*|mobile\w*|(first|last|full|middle|display)_?name|address\w*|street\w*|postal_?code|zip\w*|dob|date_of_birth|birth_?date|national_?id\w*|ssn|passport\w*|tax_?id|iban|card_\w+|ip_?address|ip|lat|lng|latitude|longitude|device_?id)$'
pii = {}
for t, c in col:
    if re.match(PII, c) and not re.search(SKIPT, t): pii.setdefault(t, []).append(c)
print('§10 PII columns in %d tables:' % len(pii))
for t in sorted(pii, key=lambda x: -len(pii[x]))[:25]: out('§10', '%s(%s)' % (t, ', '.join(sorted(pii[t]))))
if len(pii) > 25: print('  …  %d more tables' % (len(pii) - 25))
PY

# 1. ORM and engine switches that drop the DB-level FK, plus integrity-free modelling (polymorphic, generic FK).
rg -n --pcre2 "$C"'(?:relationMode\s*=\s*"prisma"|(?:createF|f)oreignKeyConstraints?\s*:\s*false|db_constraint\s*=\s*False|\bconstraints\s*:\s*false|DisableForeignKeyConstraintWhenMigrating\s*:\s*true|ConstraintMode\.NO_CONSTRAINT|(?i:foreign_key_checks)\s*=\s*0|(?i:engine\s*=\s*MyISAM)|(?i:\bNOT\s+ENFORCED\b)|\bpolymorphic:\s*true|\bmorphTo\(|\bGenericForeignKey\(|(?i:PRAGMA\s+foreign_keys))' "${X[@]}" .
# 3. Code that assumes uniqueness: model validations and find-or-create (the race itself is logic-race-scan §7's).
rg -n --pcre2 "$C"'(?:\buniqueness:\s*(?:true|\{)|\bvalidates_uniqueness_of\b|\bRule::unique\(|\bunique:[a-z_]+|\b(?:findOrCreate|find_or_create_by|get_or_create|update_or_create|firstOrCreate|updateOrCreate|FirstOrCreate)\b|\bupsert(?:Many)?\()' "${X[@]}" .
# 4. Money typed as binary float in ORM declarations H does not parse (decorators, SQLAlchemy, JPA, Go, Laravel, Rails).
rg -n -i --pcre2 "$C"'(?:\b\w*(?:'"$M"')\w*\b["\x27\x60]?\s*[:=\s]\s*(?:[\w.]*\(\s*)?(?:\w+\.)?(?:double precision|float[48]?|float32|float64|real|double|FloatField|Float)\b|\b(?:double|float|float32|float64)\s+\w*(?:'"$M"')|\b(?:type|columnType)\s*:\s*["\x27](?:double(?: precision)?|float[48]?|real|money)["\x27]|\bColumn\(\s*["\x27](?:double(?: precision)?|float[48]?|real)["\x27]|->(?:float|double)\(\s*["\x27]\w*(?:'"$M"')|\bt\.float\s+[:"\x27]\w*(?:'"$M"'))' "${X[@]}" .
# 5. Time semantics set in code or config: naive-time switches, wall-clock column types, inclusive BETWEEN on instants.
rg -n --pcre2 "$C"'(?:\bUSE_TZ\s*=\s*False|\bforceUtcTimezone\s*:\s*false|@(?:CreateDateColumn|UpdateDateColumn|DeleteDateColumn)\(\s*\)|\btype\s*:\s*["\x27]timestamp["\x27]|->timestamp\(|\bdatetime_type\b|\bparseTime=|\bjdbc\.time_zone\b|(?i:\bBETWEEN\b)[^\n]{0,60}\b\w+_at\b)' "${X[@]}" .
# 6. Domain constraints the engine or ORM silently drops: ordinal enums, non-strict MySQL, IGNORE writes.
rg -n --pcre2 "$C"'(?:@Enumerated(?!\(\s*EnumType\.STRING)|(?i:sql_mode)\s*[=:]|(?i:\b(?:INSERT|UPDATE)\s+IGNORE\b))' "${X[@]}" .
# 7. 32-bit primary keys declared in the ORM (H covers SQL, Prisma, Django and schema.rb).
rg -n --pcre2 "$C"'(?:@PrimaryGeneratedColumn\(\s*(?:["\x27]increment["\x27])?\s*\)|\.increments\(|->increments\(|\bmodels\.AutoField\b|DEFAULT_AUTO_FIELD\s*=\s*["\x27]django\.db\.models\.AutoField|\b(?:Integer|int)\s+id\s*;)' "${X[@]}" .
# 8. Auto-sync and schema-destroying commands. Deploy surfaces are included on purpose: package.json scripts,
#    Dockerfiles, CI and k8s manifests are where these reach production.
rg -n --pcre2 "$C"'(?:\bsynchronize\s*:\s*true|\bdropSchema\s*:\s*true|\bdb\s+push\b|--accept-data-loss|\bmigrate\s+reset\b|--force-reset|hbm2ddl\.auto\s*[=:]\s*["\x27]?(?:update|create|create-drop)|ddl-auto\s*[=:]\s*["\x27]?(?:update|create|create-drop)|\.sync\(\s*\{[^}]*\b(?:alter|force)\s*:\s*true|\bcreate_all\(|getSchemaGenerator\(\)\s*\.\s*(?:updateSchema|createSchema|refreshDatabase|dropSchema)|\bschema:(?:update|fresh|drop)\b[^\n]*(?:--run|-r\b)|\bmigrate:(?:fresh|reset)\b|\bdb:(?:wipe|schema:load)\b|\bdrizzle-kit\s+push\b|\.AutoMigrate\(|\bEnsureCreated(?:Async)?\()' -g '!**/node_modules/**' -g '!**/{test,tests,__tests__,spec,e2e}/**' -g '!**/*.{spec,test,e2e-spec}.*' -g '!*.md' -g '!ai/**' -g '!docs/**' .
# 9. Soft-delete escapes and raw paths that carry no ORM filter (H lists raw reads of soft-delete tables).
rg -n --pcre2 "$C"'(?:\bwithDeleted\(|\bunscoped\b|\bwithTrashed\(|\bonlyTrashed\(|\bUnscoped\(\)|\bfilters\s*:\s*(?:false|\{[^}]*:\s*false)|\ball_objects\b|\b_base_manager\b|\bparanoid\s*:\s*false|\bIgnoreQueryFilters\(\)|\bcreateNativeQuery\(|\$queryRaw(?:Unsafe)?\b|\bknex\.raw\(|\bem\.execute\(|\bDB::(?:select|table)\()' "${X[@]}" .
# 9b. Hand-rolled soft delete (an entity with a deletedAt / isDeleted property and no @Filter, @DeleteDateColumn, paranoid or
#     SoftDeletes): its ORM reads that never name the column. Each must carry the predicate or be an admin/restore path.
SD=$(rg -l --pcre2 '^\s*(?:deletedAt|isDeleted|deleted_at|is_deleted)[!?]?\s*[:=]' -t ts -t js -t py "${X[@]}" . | xargs -r rg --files-without-match --pcre2 '@Filter\(|@DeleteDateColumn|paranoid\s*:\s*true|SoftDeletes|@SQLRestriction' | xargs -r rg -o --no-filename --pcre2 '\bclass\s+\K\w+' | sort -u | head -40 | paste -sd'|' -)
[ -n "$SD" ] && rg -n -U --pcre2 "$C"'\b(?:find\w*|count\w*|exists\w*|getReference)\s*\(\s*(?:'"$SD"')\b\s*,(?:(?!deleted|isDeleted|isActive)[^;])*?\)\s*[;,)]' "${X[@]}" . || echo '9b: no hand-rolled soft-delete entity'
# 10. Files that implement retention or erasure. Zero files means no mechanism: every PII table is a candidate.
rg -l --pcre2 -i "$C"'\b(?:retention|purge\w*|anonymi[sz]e\w*|pseudonymi[sz]e\w*|erasure|right_to_(?:be_forgotten|erasure)|gdpr|expireAfterSeconds|drop\s+partition|detach\s+partition)\b' "${X[@]}" .
# 11. Document numbers taken from a sequence in code (H covers column defaults).
#     A number source must be on the line: nextval(, max(…) + 1, a serial / identity / auto-increment column, @GeneratedValue.
rg -n --pcre2 -i "$C"'(?:(?:invoice|receipt|credit_?note|fiscal|bill)\w*[^\n]{0,80}(?:\bnextval\s*\(|\bmax\s*\([^)\n]*\)\s*\+\s*1\b|\b(?:serial|bigserial|auto_?increment)\b|\bgenerated\b[^\n]{0,30}\bidentity\b|@GeneratedValue\b)|\bnextval\s*\([^\n]{0,80}(?:invoice|receipt|credit_?note|fiscal))' "${X[@]}" .
```

**H0** is the same map `index-coverage-scan` reads (its § "Pre-flight (static lane)" H0 paragraph says what the lanes, horizons and counts mean). A MikroORM snapshot stores a `col IN (…)` CHECK as the column's `enumItems`; H0 gives it back as a CHECK, so §6 does not report it. **Entity-first repos** (no SQL migrations, so H maps 0 tables): write the DDL dump (`index-coverage-scan` § "Adapt to the codebase", last column) to a file in `$RUN` (never in the repo), point `SCHEMA_SQL` at it and re-run H.

**Live lane** (only when a database is reachable). It follows the rules in `index-coverage-scan` § "Live lane — read-only by construction": read-only catalog and stat queries, never DDL, never `EXPLAIN ANALYZE`, unless the user has confirmed a non-production target in this session. Its queries:
- §1 existing orphans: `SELECT c.id FROM <child> c LEFT JOIN <parent> p ON p.id = c.<fk> WHERE c.<fk> IS NOT NULL AND p.id IS NULL LIMIT 20` (SQLite: `PRAGMA foreign_key_check`).
- §2 delete rules: `SELECT conrelid::regclass, confrelid::regclass, confdeltype FROM pg_constraint WHERE contype = 'f'` (`a` no action, `r` restrict, `c` cascade, `n` set null).
- §4, §5, §7: `information_schema.columns` filtered to `real`, `double precision`, `money`, `timestamp without time zone` and integer `id` columns.
- §7 headroom: `SELECT sequencename, last_value, max_value FROM pg_sequences`.
- §6: `SELECT @@sql_mode` on MySQL. SQLite: `PRAGMA foreign_keys` on an **app** connection.

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, Postgres 16, 376 migrations, 125 of them building DDL with `${…}`), before → after H0 and the H fixes: map 261 tables / 3,182 columns / 86 FKs → 291 / 3,523 / 124 (snapshot + 5 replayed files); §1 546 rows → 279 + 2 summary lines (`tenant_id` on 171 tables is one line; 58 `*_id` columns in 31 log, event and audit tables are one line; every column of a composite FK now counts as covered, so a `(tenant_id, order_id)` FK no longer prints `order_id`), and `requester_id` is no longer tagged external (exact `request_id` only, or a string `*_id` beside uuid keys); §2 4 → 0 (all four were an `ON DELETE` after `("tenant_id", "id")` the regex stopped at); §3 17 → 8 (9 were covered by `lower(btrim(email))`-style expression uniques H could not parse); §4 2 → 0 (both converted to `numeric(14,4)` by a migration that loops over a list); §10 21 → 25 tables (prefixed columns such as `customer_phone`; `*_id`, `*_prefix`, `*_type`, `require_*` dropped); grep 3 0 → 25 (`upsert(` / `upsertMany(`); grep 9b 13 hand-rolled soft-delete reads (`Membership` has `deletedAt`, no filter); grep 11 2 → 0 (both were the word "receipt" beside "sequence" in PII-label strings). Fixture rows are unchanged except node-api's `audit_log.actor_id` and `tenant_id` rows, now in the two summary lines (`NAPI-ARCH-02`'s `order_items.order_id` still prints).

Earlier measurement (2026-10-02) on the same repo with 294 migrations. H mapped 238 tables, 2,851 columns, 72 FKs and 437 unique keys. Per class:
- §1: 483 `*_id` columns with no FK, over 108 column names; `tenant_id` alone is 194, so grouping by name makes it one decision.
- §2: 1 FK with no stated `ON DELETE`. Before the ON-DELETE capture was fixed, it reported all 72.
- §3: 17 natural keys with no unique key. Counting a unique key on a normalised sibling (`phone_key`) as cover dropped one.
- §4: 2 money columns in `double precision`. Grep 4 printed 5 lines: the same two, two entity decorators, and a rating (not money).
- §6: 42 enum-like text columns with no CHECK.
- §9: 1 soft-delete table and 0 raw reads of it. §10: 21 tables with PII columns, and grep 10 found 72 files with retention or erasure vocabulary. §5, §7 and §11: 0 rows.
- Grep 8: 2 `package.json` scripts that run `schema:update` / `schema:fresh` with `--run`, one guarded by a dev-database check. Grep 9: 6 lines, including the project's own lint rule that bans the raw escape (a control under gate 4).

On the fixtures:
- `node-api`: §1 lists `orders.tenant_id`, `orders.customer_id` and `order_items.order_id` (the anchor of `NAPI-ARCH-02`).
- `vuln-fullstack`: 12 scalar `_id` fields with no `@relation`, and 10 `DateTime` fields that are `timestamp(3)` on its Postgres provider.
- `half-built-crm`: SQLite, so §7 stays quiet on `INTEGER PRIMARY KEY` (a 64-bit rowid). It reports 3 FKs with no `ON DELETE` and 2 enum-like text columns.

## From candidate to finding

1. **Name the invariant** in one business sentence: "every order item belongs to an existing order", "one account per email per tenant", "an invoice total is exact to the minor unit". No invariant means the hit is not this skill's.
2. **Find where it is enforced.** The order is: database constraint or type, then a trigger, view or RLS policy, then the ORM, then application code. Only the first two hold on every write path. A model validation, an `if` before the insert, or a DTO decorator is a message, not a guarantee. Read the paths that skip it: bulk inserts, `update_all`, `QuerySet.update()`, raw SQL, imports, a second service.
3. **Read the code with these questions.** Which entry points write this table, and does any of them bypass the ORM? Is the table append-only, growing or bounded? Is the column an instant or a wall-clock value? Is the value money, a measurement or a score? Is there a documented trade-off (a cross-database reference, polymorphism, a forward-only policy) with a compensating job?
4. **Restate the claim** in the sentence of [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 1 and run its seven gates. Then read [`precedents/data.md`](../../../../snippets/precedents/data.md) for the class: § 18–§ 28 cover types and constraints, § 30–§ 32 soft delete and uniqueness, § 38–§ 40 retention.
5. **Grade** by what breaks:
   - **critical**: money wrong in a ledger or payment path; `CASCADE` from a root aggregate into records of fact; auto-sync reachable in production.
   - **high**: orphans or duplicates in ownership, identity or financial rows; deleted data on a user-facing path; an int4 key on an append-heavy table; consecutive numbering a law requires.
   - **medium**: the same gaps on other tables; instants without a zone that drive expiry or billing.
   - **low**: an unstated `ON DELETE` whose default is safe; an enum-like column whose writers are all validated.

**3,000 hits.** §1 printed 483 rows on the measured repo. When a list runs long:
- (a) Group H's rows by **column name** (§1, §3, §6) or by **table** (§5, §10). One decision covers a group with the same parent, type and writers.
- (b) Rank the groups by table role: ownership, identity and financial tables first, then growing tables, then lookups.
- (c) Read the top 30 groups fully.
- (d) Prefer the bulk oracle. On a reachable database, the live orphan, delete-rule and type queries decide whole groups at once. Without one, a single constraint-rejection test per group decides it.
- (e) List the rest in the ledger as `Live, unreviewed (k groups / n rows)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | DB id · standard | Default |
|---|---|---|---|
| 1 | Relation with no database-level FK | DB-01, DB-04, DB-48 · DATA-3 | high on ownership/financial rows, else medium |
| 2 | FK with no explicit `ON DELETE`; `CASCADE` into records of fact | DB-05 · DATA-3 | critical (cascade into records of fact) · low (unstated) |
| 3 | Natural key with no unique constraint, or one scoped wrong (tenant, case, soft delete) | DB-02, DB-39, DB-44 · DATA-1 · CWE-362 | high (identity, money), else medium |
| 4 | Money in binary floating point (`float`, `double`, `real`, PG `money`) | DB-06 · DATA-9 · CWE-1339 | critical (ledger, payments), else high |
| 5 | Instant stored as wall time (`timestamp` without zone; MySQL `TIMESTAMP` past 2038) | DB-07 | high when it drives billing or expiry, else medium |
| 6 | Missing NOT NULL / CHECK on an enum-like or invariant column; constraints the engine drops | DB-03, DB-10, DB-49 · DATA-4 | high (balance, quantity, state), else medium |
| 7 | 32-bit key on a growing table; FK width below its PK | DB-08 · CWE-190 | high (event, order tables), else low |
| 8 | Auto schema sync or schema-destroying command reachable in production | DB-36, DB-54 · DATA-8 | critical |
| 9 | Soft-delete filter bypassed on a user-facing path | DB-43, DB-44 · DATA-11 | high |
| 10 | PII stored with no classification, retention mechanism or erasure path | DB-53 · DATA-13 | medium (high under regulation) |
| 11 | Gapless document numbers taken from a sequence | DB-11 | high where the law requires consecutive numbers, else N/A |

### 1. Relation with no database-level FK

```
BAD:   order_id uuid NOT NULL,                                      -- order_items: an FK by name, not by constraint
       @relation(fields: [buyerId]) missing; relationMode = "prisma"; ForeignKey(…, db_constraint=False)
GOOD:  ALTER TABLE order_items ADD CONSTRAINT order_items_order_fk FOREIGN KEY (order_id) REFERENCES orders (id) NOT VALID;
       ALTER TABLE order_items VALIDATE CONSTRAINT order_items_order_fk;   -- after the orphan clean-up
```
Candidates: H's `§1` rows and grep 1. Two summary lines replace row lists: `tenant_id` (one decision: the tenancy policy) and the `*_id` columns of log, event, audit, history and outbox tables (rows meant to outlive the parent, § 25 — read that list only when no written policy covers it). `[external-looking]` marks a provider, request or trace id, or a string `*_id` beside non-string primary keys; read it, never drop it. It is a finding when the column references another table's rows (its name, the code that joins on it, or an ORM relation), the parent is in the same database, and no precedent applies: cross-database or sharded references, audit rows meant to outlive the parent, or a documented polymorphic association with an orphan sweep (`precedents/data.md` § 25). On SQLite, every FK on a connection without `PRAGMA foreign_keys = ON` is in this class; so is a Postgres 18 `NOT ENFORCED` constraint (§ 27). **Proof — constraint rejection** (`proof-oracles.md` § "Constraint rejection", V20): a raw orphan insert as the app role must fail with `23503`. It succeeds before the fix. Live, the orphan query counts what already leaked.

### 2. FK with no explicit `ON DELETE`; `CASCADE` into records of fact

```
BAD:   invoices.user_id REFERENCES users (id) ON DELETE CASCADE     -- deleting a user erases invoices
GOOD:  ON DELETE RESTRICT on records of fact (invoices, ledger, audit); CASCADE only into owned children
```
Candidates: H's `§2` rows (unstated, or `CASCADE` from a root table into a records-of-fact table) and live `confdeltype`. **Cascade into records of fact is critical** (§ 26). An unstated rule is low: Postgres and InnoDB default to `NO ACTION`, which refuses the delete. DATA-3 still wants the choice written. Soft-deleted parents never fire a cascade (`UPDATE deleted_at`), so the children stay live: read that with §9. MySQL cascades do not fire triggers. **Proof:** delete a seeded parent inside a transaction on a non-production copy, count the rows removed per table, then roll back. The test asserts that records of fact survive.

### 3. Natural key with no unique constraint, or scoped wrong

```
BAD:   customers.email text NOT NULL                                -- checked by SELECT before INSERT; no constraint
       UNIQUE (email) on a tenant table · UNIQUE (email) on a soft-delete table · UNIQUE (email) on case-sensitive text
GOOD:  CREATE UNIQUE INDEX … ON customers (tenant_id, lower(email)) WHERE deleted_at IS NULL;
```
Candidates: H's `§3` rows (no key, a global key on a tenant table, a key that ignores soft delete) and grep 3 (code that assumes uniqueness, `upsert` included). An expression unique (`(tenant_id, lower(btrim(email)))`) covers every column it reads. It is a finding when the domain says "only one" (identity, slug, SKU, external or provider id, idempotency key) and no unique key covers the column. A key on a normalised sibling (`phone_key`, `email_normalized`, `lower(email)`) counts. The skip list is log, event and line-item tables (`precedents/data.md` § 21); NULLs being distinct is intended (§ 22). A global key on a tenant table is a finding twice (§ 32): cross-link `@tenant-isolation-reviewer` (security pack) for the existence leak. **Proof — invariant under concurrency** (`proof-oracles.md` § "Invariant under concurrency", V6): N concurrent creates with one key leave exactly one row, and the others get a clean conflict (`23505` / MySQL `1062`). Add V6's case, trailing-space, other-tenant and re-create-after-soft-delete variants.

### 4. Money in binary floating point

```
BAD:   unit_price double precision · price Float (Prisma) · amount = models.FloatField() · @Property({ type: 'double' }) price
GOOD:  numeric(19,4) / DECIMAL(19,4), or bigint minor units plus a currency column; Decimal end to end (DB → ORM → JSON as a string)
```
Candidates: H's `§4` rows and grep 4 (read the property under a bare `type: 'double'` decorator: a rating is not money). Measurements, scores, coordinates and ratios are legitimately float (`precedents/data.md` § 18). Also in the class: the Postgres `money` type, whose output depends on `lc_monetary`; JS `number` past 2⁵³ minor units; Drizzle `bigint({ mode: 'number' })`. **Proof — value vectors** (`proof-oracles.md` § "Value vectors", V18): `SELECT 0.1::float8 + 0.2::float8 = 0.3::float8` is false. A three-way split of 100.00 sums back exactly, and so do the 3-decimal currencies (KWD, BHD, OMR, JOD, TND). Both fail before the fix.

### 5. Instant stored as wall time

```
BAD:   created_at timestamp NOT NULL DEFAULT now() · Prisma DateTime (→ timestamp(3)) · Rails t.datetime on Postgres · MySQL TIMESTAMP for an expiry in 2040
GOOD:  timestamptz for instants; a wall-clock column plus an IANA zone for future local events; half-open ranges (>= a AND < b), not BETWEEN
```
Candidates: H's `§5` rows and grep 5. It is a finding for **instants** (`created_at`, `paid_at`, `expires_at`) that are compared, bucketed by day, or written by more than one clock: a DB `DEFAULT now()` evaluated in the session zone beside an app that writes UTC, a second service, a BI tool. It is not one for wall-clock values (`opens_at` plus a zone) or for `date` facts (`precedents/data.md` § 19). When every writer is one ORM that always writes UTC, the row is `[report-flagged]`, and the unproven link is that no other writer exists. **Proof — value vectors** (V19): run the suite with `TZ=Asia/Kolkata` and a DB session zone that differs, and read one instant under both. Add the DST gap and overlap, day bucketing at local midnight, and a MySQL `TIMESTAMP` insert past 2038-01-19.

### 6. Missing NOT NULL / CHECK; constraints the engine drops

```
BAD:   status varchar(20)                                   -- any string, NULL included; validated only in a DTO
       @Enumerated private Status status;                    // ORDINAL by default: reordering the enum remaps stored rows
       sql_mode='' · INSERT IGNORE …                         -- invalid values silently adjusted
GOOD:  status text NOT NULL CHECK (status IN ('pending','paid','void'))  (or a lookup table with an FK); @Enumerated(EnumType.STRING)
```
Candidates: H's `§6` rows (enum-like text with no CHECK, nullable flagged) and grep 6. It is a finding when code depends on the domain (a `switch` with no default, a state machine, a non-negative balance) and a path writes past the validation. An intentionally nullable column with a stated reason is not one (`precedents/data.md` § 28); a `NOT ENFORCED` constraint does not count as a control (§ 27). A non-negative balance or stock CHECK also closes a race: cross-link `logic-race-scan` §5 (security pack). **Proof — constraint rejection** (V20): a raw insert of an invalid value as the app role must fail with `23514` / `23502`. For JPA, reorder the enum in a test and read an old row back.

### 7. 32-bit key on a growing table

```
BAD:   id serial PRIMARY KEY on events · TypeORM @PrimaryGeneratedColumn() (int) · Django AutoField · Laravel $table->increments('id') · user_id int → users.id bigint
GOOD:  bigint identity (GENERATED ALWAYS AS IDENTITY) / bigserial / BigAutoField / $table->id(); every FK column as wide as its PK
```
Candidates: H's `§7` rows, grep 7, live `pg_sequences` headroom. It is a finding on append-heavy tables (events, logs, messages, orders), with the growth rate cited (`precedents/data.md` § 24; Basecamp was read-only for about 5 h on 2018-11-09 when an `integer` id overflowed). Bounded lookups are fine. A SQLite `INTEGER PRIMARY KEY` is a 64-bit rowid, so gate 3 refutes it. **Proof — identifier exhaustion** (V21): `ALTER SEQUENCE … RESTART WITH 2147483640` on a non-production copy, then insert ten rows. It fails before the fix. Live, headroom is `last_value / max_value`.

### 8. Auto schema sync or schema-destroying command reachable in production

```
BAD:   synchronize: true in the prod TypeORM config · CMD … mikro-orm schema:update --run · prisma db push --accept-data-loss in CI deploy
GOOD:  migrations only (reviewed, versioned); sync and push confined to dev/test configs that production cannot load
```
Candidates: grep 8, which includes `package.json` scripts, Dockerfiles, CI and k8s manifests. It is a finding when the setting or command is reachable from a production profile: the config that `NODE_ENV=production` loads, the image's `CMD` / entrypoint, a deploy job. A dev-only script behind a guard that refuses a non-local database is Hardening once the guard is read. **Proof — config test per environment** (V15): load the production profile in a test and assert sync is off. The drift check exits 0 (`prisma migrate diff … --exit-code`, `manage.py makemigrations --check`, `alembic check`, `typeorm migration:generate --check`, `mikro-orm migration:check`, `drizzle-kit check`).

### 9. Soft-delete filter bypassed on a user-facing path

```
BAD:   SELECT * FROM products WHERE store_id = $1             -- raw report; products is soft-deleted
       em.find(Product, { slug }, { filters: false })          // storefront path
GOOD:  … AND deleted_at IS NULL; or read through a view that applies it; the escape only on admin/restore/erasure paths, named in a comment
```
Candidates: H's `§9` rows (raw SQL on a soft-delete table with no `deleted` predicate in the statement), grep 9 (escapes and raw paths) and grep 9b (a hand-rolled soft delete — a `deletedAt` property with no global filter — read through the ORM without naming the column: every such read must carry it, or be an admin, restore or erasure path). It is a finding when the path is user-facing or feeds an export, aggregate or authorization check. Audit, admin, restore and erasure paths that use the explicit escape are correct (`precedents/data.md` § 30). A view or RLS policy that applies the filter is the control (§ 31), and so is a lint rule that bans the escape outside allow-listed files: read it. Deactivated accounts still able to act is `logic-race-scan` §11's (security pack). **Proof** (V17): soft-delete a seeded row, then hit the endpoint, export and count. None may return it, and each does before the fix.

### 10. PII stored with no classification, retention mechanism or erasure path

Candidates: H's `§10` inventory (email, phone, name, address, birth date, national id, IP, location and card columns per table) against grep 10's list of retention and erasure files. It is a finding when a PII table has no retention mechanism that really runs (a TTL or purge job, a partition drop), or when its erasure path is missing or blocked: an FK with `RESTRICT` to a table nobody purges, copies in JSON or denormalised columns, an "erasure" that only sets `deleted_at` (`precedents/data.md` § 40). A legal hold or an undo window with a TTL purge is not a finding. Who reads and exports the data is `@data-privacy-reviewer`'s (security pack); without it, the row says `flow: not assessed (owner pack security not installed)`. **Proof — seeded aged rows** (V23): run the retention job and assert in-policy rows remain and aged ones are gone. For erasure, erase a seeded subject, then scan every PII column (and JSON copies) for its values.

### 11. Gapless document numbers taken from a sequence

```
BAD:   invoice_number bigint DEFAULT nextval('invoice_seq')      -- a rolled-back issue leaves a gap; tax rules may forbid gaps
GOOD:  UPDATE invoice_counters SET next = next + 1 WHERE series = $1 RETURNING next   -- in the issuing transaction, row-locked
```
Candidates: H's `§11` rows and grep 11. Sequence gaps are normal (`precedents/data.md` § 23). It is a finding only where consecutive numbering is required: name the rule or jurisdiction the project serves, or mark the row `[report-flagged]` with that as the unproven link. When the business pack is installed, the jurisdiction fact comes from `tax-invoice-scan`'s tax policy (`tax-policy.md`: jurisdictions and the document rules each sets) — cite its row; a policy with no jurisdiction or no source keeps the row `[report-flagged]`. The issued-document lifecycle itself (immutability, credit notes, chain fields) is `tax-invoice-scan` §7–§11's. **Proof:** on a non-production copy, issue a number inside a transaction, roll it back, then issue the next one. The gap appears before the fix. Then run two concurrent issues: no duplicate, no gap.

## Output

```
schema-integrity-scan — lanes: postgres 17 (docker-compose.yml:12), prisma 6 (package.json:21); live lane: not run (no reachable DB)

Findings: 3   (Verification: 11 candidates → 3 findings · 2 unconfirmed · 5 hardening · 0 pre-existing · 1 refuted)

1. prisma/schema.prisma:58 · orders.coupon_id                       [report-with-fix]  high
   §1 coupon_id is a scalar with no @relation, so no FK exists. Coupons are hard-deleted by
   DELETE /admin/coupons/:id (src/admin/coupons.controller.ts:40), which leaves orders pointing nowhere.
   Fix: @relation(fields: [couponId], references: [id], onDelete: SetNull) + a migration adding the FK
   NOT VALID, an orphan clean-up, then VALIDATE (route via /add-migration). DB-01 · DATA-3

2. migrations/0031_pricing.sql:12 · price_rules.line_price          [report-with-fix]  critical
   §4 double precision on a price that feeds invoice totals (src/billing/invoice.ts:88). Fix: numeric(19,4)
   via expand/contract, and Decimal in the entity and the JSON contract. DB-06 · DATA-9 · CWE-1339

3. prisma/schema.prisma:91 · coupons.expires_at                     [report-flagged]  medium
   §5 DateTime → timestamp(3), no zone, compared with now() in raw SQL (src/coupons/coupons.repo.ts:61).
   Unproven link: whether any writer besides Prisma Client stores it. Probe: TZ=Asia/Kolkata + a DB
   session zone of America/St_Johns; read one coupon's expiry under both.

Class coverage:
  §1  relation without FK        checked (9 hits in 5 groups → 1 finding, 3 hardening: external ids)
  §2  ON DELETE                  checked (3 hits → 0 findings; defaults are NO ACTION)
  §3  natural key unique         checked (0 hits)
  §4  money as float             checked (2 hits → 1 finding, 1 hardening: rating)
  §5  instant without zone       checked (7 hits in 1 group → 1 report-flagged)
  §6  NOT NULL / CHECK           checked (1 hit → 0 findings, 1 unconfirmed)
  §7  int32 keys                 checked (0 hits)
  §8  auto-sync in production    checked (0 hits)
  §9  soft-delete bypass         N/A (no soft-delete column in the schema map)
  §10 PII storage                checked (2 tables → 0 findings; retention: src/jobs/purge.ts)
  §11 gapless numbering          checked (0 hits)
```

Row tags:
- `[report-with-fix]`: the missing guarantee and the code that depends on it are both cited.
- `[report-flagged]`: one link is unproven (another writer, the legal rule, the production profile, a path not read), and the row names it and its probe.

The block lists **all eleven** classes on every run:
- `checked (k hits → m findings)` only when the class's grep or H ran on a lane that is present;
- `N/A (<reason>)` when the repo cannot have the class;
- `blocked (<reason>)` when the lane could not run;
- groups never read appear as `Live, unreviewed`.

## False positives / gotchas

- **H is a map, not a verdict.** A constraint added by a trigger, a view, an ORM declaration H does not parse, or a later migration in an unusual folder decides the row. Grep the constraint name, and query the live catalog when it is reachable. Without H0 (`schema-map NOT-RUN`), DDL whose names are built with `${…}` is invisible and every row on those tables is suspect.
- **Statement order within one file:** H applies statements in path order and skips `down()` bodies. A file that adds and drops the same column in its `up` can mislead it: read it.
- **Validation is not a constraint**, and a constraint the engine does not enforce is not one either (`precedents/data.md` § 27). A model validation, a DTO decorator or a `SELECT` before `INSERT` never clears §1, §3 or §6.
- **The engine decides:** SQLite `INTEGER PRIMARY KEY` is 64-bit; InnoDB creates FK indexes (not this skill's, but often confused with §1); MySQL `DATETIME` does not convert zones while `TIMESTAMP` does.
- **Test files, seeds and fixtures** are out of scope unless they are the migration or backfill that runs in production (`refute-before-report.md` § 4).

## When to run

- On every diff that adds or changes an entity, a model, a table, a column, a relation or a migration, and on diffs that add a create or update path to a table with a natural key, money or soft delete.
- On every whole-repo `/db-audit`, reporting all eleven classes; the live lane runs when a database is reachable.
- On a V1 → V2 port, against the V1 schema's constraints: a port that drops a constraint ships the bug DATA-1 was written for.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§ 8 says who verifies). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening or Refuted. Never drop them.
- Halt on any finding without the column or constraint `<file:line>`, the code or rule that depends on it, the engine and version, and the fix.
- Do not run anything in the live lane but the read-only set unless the user has confirmed a non-production target in this session. The orphan, delete and exhaustion probes run on a copy.
- Do not propose a constraint on a populated table as a one-step migration. Route it through `/add-migration` (`NOT VALID` then `VALIDATE`, and the clean-up of rows that already break it).
- Do not print "schema is sound" without the class-coverage block. A class whose lane did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries): cross-link it.

## Related

- [`refute-before-report.md`](../../../../snippets/refute-before-report.md), [`precedents/data.md`](../../../../snippets/precedents/data.md) (§ 18–§ 32 and § 38–§ 40 here) and [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Data" (constraint rejection, invariant under concurrency, value vectors) with its class variants V6, V15, V17–V21 and V23.
- `index-coverage-scan` (the index on an FK, and the live-lane rules this skill follows), `schema-diff` (entity-vs-database drift), `schema-consistency-audit` (convention drift for `/polish`), `migration-safety` and `/add-migration` (adding a constraint without blocking writes), `migration-rehearsal` (timing the validation on a restored copy).
- `/db-audit` dispatches this skill and folds its class block into the ledger. `/db-fix` closes the findings, failing first on the class oracle.
- Security pack, when installed: `@tenant-isolation-reviewer` (tenancy, RLS), `logic-race-scan` (§7 find-or-create, §2 money values, §5 balances, §11 deactivated accounts), `@data-privacy-reviewer` (the PII flow).
- `rules/database-principles.md` § "Must" (`.claude/rules/` when installed) — the invariants these classes enforce.
