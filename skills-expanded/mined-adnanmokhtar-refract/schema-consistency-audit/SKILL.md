---
name: schema-consistency-audit
description: Schema + migration consistency audit. Detects drift in nullability, type choice, timezone handling, charset/collation, timestamp and audit-field coverage, soft-delete coverage, migration patterns, and object naming. Findings are ranked by data-integrity risk, not by detector order. Emits closure verbs that ship as reversible migrations. Used by /polish on data-* stacks and /db-audit.
kind: skill
pack: database
allowed-tools: [Read, Write, Edit, Grep, Glob, Bash]
---

# Skill: schema-consistency-audit

## Purpose

Detect drift across the project's database schema + migration history so /polish can unify it. The skill operates on the live schema (introspection) or the static schema map + migration history + the project's conventions (`_extracted-idioms.md § Schema conventions`, `ai/schema-conventions.md`, or the schema section of `ai/conventions.md` — `## Persistence`, `## Schema`, `## Database`, `## Data model`).

## When to use

- Dispatched by `/polish` on `data-*` stacks (or `backend-*` stacks with significant schema scope).
- Dispatched by `/db-audit` for read-only audit.
- Standalone: `/polish --diagnose-only --stack=data` writes the artifact, no fixes.
- NOT for adding new tables (use `/add-migration`) or query optimisation (use `/optimize-query`).

## Inputs (precise contract)

| Input | Source | Required |
|---|---|---|
| Codebase root | Orchestrator | YES |
| `PROJECT_KIND` | `_extracted-codebase.md § Gold standards`, else `.claude/codebase-profile.md` (its stack line names the ORM and engine) | YES under `/polish` (`data-*` or `backend-*` with schema scope); under `/db-audit` a backend with migrations is enough |
| Schema conventions | `_extracted-idioms.md § Schema conventions`, `ai/schema-conventions.md`, or the schema section of `ai/conventions.md` (S1 prints which) | YES (without one, drift is undefined: under `/polish` halt; under `/db-audit` print `blocked (no conventions file)` and still print S2's profile as context) |
| Schema introspection access | DB connection, OR the schema map (S2, `index-coverage-scan/scripts/schema-map.py`), OR the migration history | YES (one of the three) |
| Scope filter (optional) | Caller flag (e.g., `--scope=analytics`) | NO (default: all tables) |

## Outputs (precise contract)

```yaml
class: schema-consistency
subclass: <one of: nullable-drift | type-drift | timezone-drift | charset-drift |
                   collation-drift | soft-delete-drift | audit-field-drift |
                   timestamp-column-drift | column-naming-drift |
                   migration-pattern-drift | object-naming-drift>
table: <table-name>
column: <column-name OR null for table-level findings>
file: <migration-path:line OR schema-file:line>
canonical: <what the project's convention says>
divergence: <what this column/table does differently>
closure_verb: <one of the verbs below>
migration_strategy: rename-in-place | expand-contract | rename-with-dual-read | meta
risk: low | medium | high
integrity_class: <one of: corrupts-data | loses-precision | breaks-queries | cosmetic>
```

## Pre-flight (runnable, read-only)

Run from the repo root. S1 finds the conventions and the project kind; S2 profiles the schema the migrations leave behind, one line per detector family. Every number is a candidate list for a detector below, never a finding: a drift is a finding only against what the conventions say.

```bash
# S1. Where the conventions live (first that exists wins) and PROJECT_KIND (the extract, else the codebase profile).
for f in _extracted-idioms.md .claude/_extracted-idioms.md ai/schema-conventions.md ai/conventions.md; do [ -f "$f" ] && rg -n -i --pcre2 '^#{1,4}\s*(schema|persistence|database|data\s*model|migrations?)\b' "$f"; done
for f in _extracted-codebase.md .claude/codebase-profile.md; do [ -f "$f" ] && rg -n -i --pcre2 '\bPROJECT_KIND\b|\b(MikroORM|Prisma|TypeORM|Sequelize|Drizzle|Django|SQLAlchemy|ActiveRecord|Eloquent|Hibernate|GORM|EF Core)\b[^\n]{0,40}\b(Postgres|MySQL|MariaDB|SQLite|SQL Server)' "$f" | head -3; done
# S2. The schema (index-coverage-scan H0's map) profiled per detector, and object-name patterns by the date of the migration that made them.
SM=.claude/skills/index-coverage-scan/scripts/schema-map.py; RUN=$(mktemp -d "${TMPDIR:-/tmp}/schema-consistency.XXXXXX")
if command -v python3 >/dev/null 2>&1 && [ -f "$SM" ] && python3 -I -B "$SM" . > "$RUN/schema.sql"; then grep '^-- schema-map l' "$RUN/schema.sql"; python3 - "$RUN/schema.sql" . <<'PY'
import os, re, sys
from collections import Counter, defaultdict
sql, root = open(sys.argv[1], encoding='utf-8').read(), sys.argv[2]
cols = defaultdict(dict)                                   # cols[table][column] = (type, nullable)
for m in re.finditer(r'(?im)^alter table "(\w+)" add column "(\w+)" ([^;\n]+?)(?: default [^;\n]*)?;', sql):
    t = m.group(3).lower(); cols[m.group(1)][m.group(2)] = (re.sub(r'\s*not null$', '', t), not t.endswith('not null'))
case = Counter('camel' if re.search(r'[a-z][A-Z]', c) else 'Pascal' if c[:1].isupper() else 'snake' for T in cols.values() for c in T)
print('column case styles: %s' % dict(case))
ts = [(t, c, ty) for t, T in cols.items() for c, (ty, n) in T.items() if ty.startswith('timestamp') or ty.startswith('datetime')]
naive = [x for x in ts if not re.match(r'timestamptz|timestamp\S* with time zone', x[2])]
print('timezone: %d timestamp columns, %d without a zone%s' % (len(ts), len(naive), ': ' + ', '.join('%s.%s' % x[:2] for x in naive[:10]) if naive else ''))
by = defaultdict(list)
for t, T in cols.items():
    for c, (ty, n) in T.items(): by[c].append((t, re.sub(r'\(.*', '', ty), n))
drift = sorted(((c, Counter(x[1] for x in v)) for c, v in by.items() if len(v) >= 3 and len({x[1] for x in v}) > 1), key=lambda x: -sum(x[1].values()))
print('type drift (same name, several base types; %d names): %s' % (len(drift), '; '.join('%s %s' % (c, dict(k)) for c, k in drift[:12])))
nul = sorted(((c, sum(x[2] for x in v), len(v)) for c, v in by.items() if len(v) >= 3 and 0 < sum(x[2] for x in v) < len(v) and c not in ('id',)), key=lambda x: -x[2])
print('nullable drift (same name; %d names): %s' % (len(nul), '; '.join('%s %d/%d nullable' % x for x in nul[:12])))
stamp = Counter(c for T in cols.values() for c in T if re.match(r'(created|updated|modified|inserted|deleted)(_?at|_?on|_time|_date)?$|^(creation|modification)_\w+$|^last_modified$', c))
print('timestamp names: %s' % dict(stamp))
miss = [t for t, T in cols.items() if not {'created_at', 'updated_at'} <= set(T) and not {'createdAt', 'updatedAt'} <= set(T)]
print('audit fields: %d of %d tables lack created_at + updated_at%s' % (len(miss), len(cols), ': ' + ', '.join(sorted(miss)[:12]) if miss else ''))
print('collation: %d explicit COLLATE clauses (Postgres has no per-table charset: charset-drift is N/A there)' % len(re.findall(r'(?i)\bcollate\b', sql)))
pat = lambda n: next((p for p, r in (('idx_*', r'^idx_'), ('ix_*', r'^ix_'), ('*_idx', r'_idx$'), ('*_index', r'_index$'), ('*_unique', r'_unique$'), ('*_uniq', r'_uniq$'),
        ('*_key', r'_key$'), ('*_pkey', r'_pkey$'), ('*_fkey', r'_fkey$'), ('*_foreign', r'_foreign$'), ('*_fk', r'_fk$'), ('*_check', r'_check$')) if re.search(r, n)), 'other')
first, last, count = {}, {}, Counter()
for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if d not in ('node_modules', '.git', 'dist', 'build', 'vendor', '.venv')]
    if not re.search(r'(^|/)(migrations?|migrate|alembic|versions)(/|$)', os.path.relpath(dp, root)): continue
    for f in sorted(fns):
        d = re.search(r'(\d{8})', f)
        if not d or not re.search(r'\.(sql|ts|js|py|rb|php)$', f): continue
        t = open(os.path.join(dp, f), encoding='utf-8', errors='replace').read()
        for m in re.finditer(r'(?i)(?:create\s+(?:unique\s+)?index\s+(?:concurrently\s+)?(?:if\s+not\s+exists\s+)?|add\s+constraint\s+)["`]?(\w+)', t):
            p = pat(m.group(1)); count[p] += 1; first[p] = min(first.get(p, d.group(1)), d.group(1)); last[p] = max(last.get(p, d.group(1)), d.group(1))
print('object-name patterns by migration date (pattern count first..last): %s' % '; '.join('%s %d %s..%s' % (p, n, first[p], last[p]) for p, n in count.most_common()))
PY
else echo 'S2 NOT-RUN (python3 or schema-map.py absent): profile the schema by reading the migrations'; fi
```

**Measured** (2026-10-15) on a real NestJS + React monorepo (MikroORM 6.6, Postgres 16, 291 tables): S1 found `ai/conventions.md` `## Persistence` (there is no `ai/schema-conventions.md`, so the earlier halt read every such repo as unconfigured) and the stack line in `.claude/codebase-profile.md`; S2 ran in about 2 s and printed snake case only, 737 timestamps all with a zone, 37 names with several base types (`order_id` `uuid` ×50 and `varchar` ×3), 80 names with mixed nullability (`currency` nullable in 7 of 44 tables, the tables whose amounts sit beside it), 4 tables without both audit fields, 0 `COLLATE` clauses, and the index suffixes by date (`*_idx` last used 2027-01-17, `*_index` still in use) — the input to grandfathering below.

## The 11 detectors

### 1. column-naming-drift

**Fingerprint**: column names mix case styles within the same database (e.g., `created_at` and `createdAt` and `CreatedAt` for the same conceptual field across tables).

**Detection**: introspect every column; classify case style; flag tables/columns deviating from the project's canonical (declared in conventions).

**Closure verb**: `unify-column-naming`.

**Migration strategy**: `rename-with-dual-read` — add new column, backfill, dual-read in code, drop old column in next migration. NEVER blind rename in production.

### 2. type-drift

**Fingerprint**: same conceptual field uses different types across tables.

Common drifts:
- `email` is `VARCHAR(255)` in some tables, `TEXT` in others.
- `description` is `TEXT` in some, `VARCHAR(2000)` in others.
- Money: `DECIMAL(10,2)` in some, `BIGINT` (storing cents) in others.
- IDs: `BIGINT` in some, `UUID` in others, `VARCHAR(36)` in others.

**Closure verb**: `unify-type-choice`.

**Migration strategy**: `expand-contract` (add new column with right type; backfill; switch reads; switch writes; drop old column).

### 3. object-naming-drift (indexes and foreign-key constraints)

**Fingerprint**: index or FK-constraint names follow different patterns across the schema — `idx_orders_status` / `ix_orders_status` / `orders_status_idx` / `orders_idx_status`, and the equivalent spread on constraint names.

**Grandfathering**: a naming rule binds the objects created after the rule was adopted (the conventions file's date, its ADR, or the first migration that follows it). S2 prints each name pattern with the first and last migration date that used it; a pattern whose last use predates the rule is grandfathered (one summary line with its count), and only a pattern still used after the rule is drift.

**Closure verb**: `unify-object-naming`.

**Migration strategy**: `rename-in-place` — **use the engine's rename, never drop + recreate.** Postgres: `ALTER INDEX <old> RENAME TO <new>` / `ALTER TABLE <t> RENAME CONSTRAINT <old> TO <new>`. MySQL 5.7+: `ALTER TABLE <t> RENAME INDEX <old> TO <new>, ALGORITHM=INPLACE` — the operation is In Place, permits concurrent DML, and only modifies metadata ([MySQL Table 17.16](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html)). Dropping and recreating an index on a populated table is a full index build for a **cosmetic** gain — exactly the trade the rest of this pack forbids. If the engine cannot rename the object, the finding's risk becomes `medium` and it is deferred, not forced through.

**Risk**: `low` — and its rank reflects that. A naming inconsistency costs a reader five seconds; it never corrupts data. It is ordered after every integrity finding, and a run that reports only naming drift is a clean run with a note, not a finding list.

### 4. migration-pattern-drift

**Fingerprint**: migration files don't follow the project's pattern. Common drifts:
- Some have `down()` / rollback, others don't.
- Some are reversible, others irreversible without comment explaining why.
- Some run as transactions, others don't (where the project's convention says they should).
- Some include data migrations inline, others separate.

**Detection**: walk migrations directory; check each against the project's template (in `_extracted-idioms.md § Migration template`).

**Closure verb**: `unify-migration-pattern` — for forward-only fixes, refactor the migration before merge. For already-merged migrations, document the deviation in a follow-up migration's header.

**Migration strategy**: meta — fixes the structure of future migrations, not data.

### 5. timestamp-column-drift

**Fingerprint**: timestamp columns named inconsistently.

Common drifts:
- `created_at` vs `createdAt` vs `created` vs `creation_time` vs `inserted_at`
- `updated_at` vs `last_modified` vs `modified_at`

**Closure verb**: `unify-timestamp-cols`.

**Migration strategy**: `rename-with-dual-read`.

### 6. soft-delete-drift

**Fingerprint**: some tables have `deleted_at` (soft delete), others don't, where the project's convention requires soft delete.

**Detection**: cross-check tables-without-`deleted_at` against `_extracted-idioms.md § Soft-delete tables`.

**Closure verb**: `add-soft-delete` — adds `deleted_at TIMESTAMPTZ NULL`, updates queries to filter `deleted_at IS NULL` by default, updates ORM models.

**Migration strategy**: `expand-contract` (column add → query updates → enforcement).

### 7. audit-field-drift

**Fingerprint**: some tables have `created_by` / `updated_by` / `created_at` / `updated_at`, others don't, where the project's convention requires them.

**Closure verb**: `add-audit-fields`.

**Migration strategy**: `expand-contract`.

### 8. timezone-drift

**Fingerprint**: timestamp columns mix `TIMESTAMP` (timezone-naive) and `TIMESTAMPTZ` (timezone-aware) within the same conceptual schema.

**Closure verb**: `unify-timezone` — typically converges to `TIMESTAMPTZ` per modern best practice.

**Migration strategy**: `expand-contract` for prod tables (the conversion can change reads if the timezone differs).

### 9. charset-drift

**Fingerprint**: tables use different charsets (e.g., MySQL `utf8` vs `utf8mb4` for the same concept). **Postgres has no per-table or per-column charset** — the encoding is the database's — so on Postgres this detector is `N/A (engine)` and the text-comparison drift lives in detector 10 (`COLLATE` clauses, ICU or nondeterministic collations).

**Closure verb**: `unify-charset`.

**Migration strategy**: depends on the DB — some support online conversion, others require expand-contract.

### 10. collation-drift

**Fingerprint**: tables use different collations affecting ordering / comparison. On Postgres read the column-level `COLLATE` clauses (S2 counts them) and `CREATE COLLATION`; on MySQL, the table and column `COLLATE` options.

**Closure verb**: `unify-collation`.

**Migration strategy**: same as charset.

### 11. nullable-drift

**Fingerprint**: same conceptual field is nullable in some tables, NOT NULL in others, without documented reason.

**Closure verb**: `unify-nullable` — converges to whichever the project's convention requires (usually NOT NULL with default for stable fields).

**Migration strategy**: `expand-contract` (add default → backfill nulls → set NOT NULL).

## Procedure

1. **Pre-flight**:
   - Run the block in § "Pre-flight (runnable, read-only)".
   - `PROJECT_KIND` is `data-*` OR `backend-*` with schema scope (the extract, else the codebase profile). Under `/polish`, halt otherwise.
   - A conventions source exists (S1). Under `/polish`, halt if none; under `/db-audit`, print `blocked (no conventions file)`.
   - DB introspection access, the schema map, OR migration history readable. Halt if none.
2. **Introspect schema** — get tables, columns, types, indexes, FKs, constraints. Emit `_schema-snapshot.md`.
3. **Walk migration history** — emit `_migration-summary.md` listing files + patterns + reversibility.
4. **Run the 11 detectors**; emit findings. Detector order is not report order — see step 6.
5. **For each finding**:
   - Cite `<file:line>` evidence.
   - Pick `migration_strategy` per the verb's table above.
   - Estimate `risk` — the cost of *making the change*:
     - `low`: in-place object renames, audit-field additions, metadata-only changes.
     - `medium`: column renames (require a dual-read window), nullable tightening (requires a backfill).
     - `high`: type conversion (data-loss potential), charset/collation change on a populated table.
   - Assign `integrity_class` — the cost of *leaving it alone*, which is a different axis and the one that ranks the report:
     - `corrupts-data`: the drift can silently produce wrong stored values — mixed timezone-naive/aware timestamps, a money column stored as float in one table and decimal in another, `utf8` vs `utf8mb4` truncating on 4-byte characters.
     - `loses-precision`: values survive but detail does not — a narrower type, a lower-precision timestamp.
     - `breaks-queries`: comparisons or ordering behave differently across tables — collation drift, nullability that makes a `NOT IN` silently return nothing.
     - `cosmetic`: a reader is inconvenienced. Naming drift is always this.
6. **Write the decisions file** — under `/polish`, `ai/polish/_schema-decisions.md`; under `/db-audit` or a standalone read-only run, `$RUN/_schema-decisions.md` (the run folder S2 made; the audit writes nothing in the repo but its report). The file holds findings **ranked by `integrity_class` first** (`corrupts-data` → `loses-precision` → `breaks-queries` → `cosmetic`), then grouped by table, then ordered foundation-first within a table (audit fields before nullability tightening; column rename before type change on the same column). Detector index carries no weight: a charset drift that truncates emoji outranks every naming finding in the report, and a report that lists them at the same level has mis-sorted the reader's afternoon.

## Hard rules

- **Reversible migrations only** — every closure verb produces a migration with a documented `down()` / rollback. Irreversible changes require ADR.
- **No blind renames in production** — column / table renames go through a dual-read window: add new, dual-write, dual-read, drop old. Multi-PR.
- **Never drop-and-recreate an object that the engine can rename.** Indexes and constraints have in-place rename syntax on both major engines; a rebuild for a naming fix is unjustifiable cost.
- **Cosmetic findings never outrank integrity findings**, whatever order the detectors ran in.
- **Type changes via expand-contract** — add new column, backfill, switch reads, switch writes, drop old. NEVER `ALTER COLUMN TYPE` directly on prod tables with significant data.
- **One conceptual change per migration** — bundling rename + type change + nullable change in one migration makes rollback ambiguous.
- **Migration tested in staging** — every closure verb's migration runs in staging before prod; staging dataset must reflect prod scale (≥ 10% sample).
- **No detector invents conventions** — canonical comes from the conventions source S1 names (`_extracted-idioms.md § Schema conventions`, `ai/schema-conventions.md`, or the schema section of `ai/conventions.md`).

## Verify (postconditions)

Contract: [`templates/snippets/postcondition-check.md`](../../../../snippets/postcondition-check.md). **Preconditions are not verification** — this skill guards its entry and must also check its exit. Every entry under `## Failure modes` that this skill's own write could cause becomes a check here, observed rather than assumed, reported when it passes as well as when it fails, and `NOT RUN` with a reason where no signal is available. A failure mode the skill documented and never checked is a risk it accepted on the caller's behalf without saying so.

## Failure modes

- **Conventions missing** → under `/polish` halt; surface "/setup-project --refine to declare schema conventions first". Under `/db-audit`, the Conventions ledger row prints `blocked (no conventions file)` with S2's profile as context.
- **Cannot introspect** → halt; user provides DB access OR migration-history dump.
- **High-risk closure** (type conversion with data-loss potential) → flag, halt that finding, surface ADR template; rest continue.
- **Engine cannot rename the object in place** → the naming finding is deferred, not converted into a drop + recreate.
- **Migration framework not detected** → halt; tool-specific (Prisma / Knex / Flyway / Alembic / Django / etc.) format must be discoverable.

## References

- `_extracted-idioms.md § Schema conventions`, `ai/schema-conventions.md`, `ai/conventions.md` (its schema section).
- `index-coverage-scan/scripts/schema-map.py` (this pack) — the schema map S2 profiles; `index-coverage-scan` § "Pre-flight (static lane)" H0 says what its lanes and horizons mean.
- `migration-rehearsal.md` (this pack) — every `expand-contract` or high-risk closure verb's migration goes through rehearsal. In-place renames do not need one.
- `align-discipline.md` — closed-vocabulary discipline.
- `polish` command — dispatches this skill on data stacks.
