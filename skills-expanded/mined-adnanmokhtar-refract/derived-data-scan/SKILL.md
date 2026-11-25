---
name: derived-data-scan
description: "Rollups, materialized views and trigger-kept tables vs their sources; bucket SQL zones and DST."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: derived-data-scan

## Premise

Most applications carry a small warehouse without calling it one: a daily order rollup a cron recomputes, a counter a job bumps, a table a trigger keeps in step, a materialized view a dashboard reads, a closed-period snapshot, a tenant-usage table. Each is a **copy that must equal a function of its source**, and each drifts by a different mechanism: an increment replayed by a retried job, a refund that lands after the recompute window, a trigger whose column list misses the column the rollup sums, a `TRUNCATE` that bypasses row triggers, a refresh that blocks readers or never runs, a UTC-day bucket read as a tenant's local day. The bucket SQL drifts too, and it is engine-specific (PostgreSQL 18 docs, MySQL 8.4 docs, accessed 2026-10-19): `AT TIME ZONE` on a naive `timestamp` **assumes** the zone and on a `timestamptz` **converts to** it, so one conversion on a naive UTC column shifts the wrong way; Prisma `DateTime` maps to a naive `timestamp(3)` unless `@db.Timestamptz`; MySQL `CONVERT_TZ` with a named zone returns NULL when the zone tables are not loaded; `REFRESH … CONCURRENTLY` needs a unique index on plain columns covering every row, and without `CONCURRENTLY` the refresh blocks readers; `now()` in a view definition is frozen at the refresh.

This skill owns research ids MV-1…MV-6 and TB-1…TB-4 (`research-data-engineering.md` § 1.6), shipped as `DE-MV-<n>` / `DE-TB-<n>`: **whether a rollup, view, snapshot or trigger-kept table equals its source, and whether the bucket SQL implements the declared zone.**

**Every finding cites the writer `<file:line>` + the derived table and the source columns it depends on + the source change that breaks it (a replay, a change after the window, an uncovered column, a bulk path, a tenant-zone read, a DST or midnight row) + the declared zone or `UNDECLARED` + the oracle that would settle it + the fix in the project's own primitive.** A grep hit is a candidate. "The rollups look consistent" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V547, V548, V552, V563 and V564.

## The rule

A candidate is a finding when all four hold:

1. **Reachable and read.** A scheduler, consumer, trigger or request path writes the derived table, and a screen, export, API or report reads it. A table nothing reads is LN-4's orphan, not a drift finding.
2. **The source contract is read.** Which source rows and columns the derived row is a function of; whether the source changes after the window (refunds, status changes, edits, deletes); the zone the consumer expects (business `report-scan` §8 owns *which* zone — this skill reads the declared one, or prints `UNDECLARED`).
3. **No existing control, across files.** A whole-period replacement, a guarded increment (processed-events key or a unique `(tenant, day)` constraint), a dirty-period marker written by insert/update/delete triggers, a reconciliation that marks stale and fails, a spec holding the trigger list equal to the fact columns, sub-day buckets beside UTC days, a concurrent refresh with its unique index.
4. **The oracle fired, or the fact is two-ended.** V547/V548/V563/V564 ran red on a scratch DB with the project's migrations; or the static fact cites both ends — the trigger's column list and the source column the rollup sums that is missing from it; the naive column type in the migration and the query with one `AT TIME ZONE`.

## Boundaries

- **Which zone, week start or business day a report should use** → business `report-scan` §8/§9; **a reported number's definition, exclusions, currency, fan-out** → `report-scan` §1–§7. This skill owns whether the rollup and its bucket SQL implement the declared zone. Each when installed; without them the row is `[report-flagged]` here with the route named.
- **A message consumer's dedup and ack order** (a rollup bumped by a Kafka/Rabbit/SQS consumer) → distributed-systems `messaging-scan` §2; this skill corroborates by `file:line`. **An application scheduler's overlap and misfire** → backend `job-lifecycle-scan` §4–§6. **Calendar arithmetic in code** (`addDays`, month ends) → code-quality `correctness-smell-scan` §6. **OLTP timestamp storage** as a schema choice → database `schema-integrity-scan` §5; here a naive column matters only through the bucket SQL that reads it.
- **dbt rollup models** and their reconciliation tests → `data-test-scan` §6; **warehouse incrementals** → `incremental-load-scan`. This skill is the in-app lane: ORM entities, raw SQL in application code, migrations, triggers, views.
- **Erasure reaching a rollup with identifiers** → `pii-copy-scan` §2 (this pack). **An export copied from a rollup** → `extract-scan`.

## Adapt to the codebase — the lanes

Read the engine and its version from the files (compose image tag, `DATABASE_URL` scheme, ORM config, lockfile), never from memory, and print the lanes you ran.

| Lane | Detect by | Bucket and refresh idioms read | Fix primitive |
|---|---|---|---|
| **Postgres** (raw SQL, MikroORM `execute`/`qb`, Prisma `$queryRaw`, TypeORM `query`, Knex `raw`, Drizzle `sql`) | `postgres` image, `pg` / `postgres` driver | `AT TIME ZONE`, 2-arg `date_trunc` (session `TimeZone`), 3-arg `date_trunc(…, tz)` (PG ≥ 12), `date_bin`, `generate_series`, `REFRESH MATERIALIZED VIEW`, triggers | `ts AT TIME ZONE tz` on `timestamptz`; `(ts AT TIME ZONE 'UTC') AT TIME ZONE tz` on naive UTC; half-open `>= start and < end`; `CONCURRENTLY` + unique index |
| **MySQL / MariaDB** | `mysql` image, `mysql2`, `PyMySQL`, Laravel `mysql` | `CONVERT_TZ`, `DATE()`, session `time_zone` | load zone tables (`mysql_tzinfo_to_sql`) or convert in the app; numeric offsets only for no-DST zones |
| **BigQuery / Snowflake / ClickHouse** SQL in app code | client libraries, SQL strings | `DATE(ts, tz)`, `TIMESTAMP_TRUNC(ts, DAY, tz)`; `CONVERT_TIMEZONE`; `toStartOfDay(ts, tz)`, `toStartOfWeek` mode | the zone argument; the engine's aware type |
| **ORM aggregation** | Django `Trunc*`/`TruncDate`, Rails groupdate, Laravel `whereBetween`, SQLAlchemy `func.date_trunc` | Django `tzinfo=`, groupdate `time_zone:`, `__range=` | the ORM's zone argument; `__gte`/`__lt` |
| **Schedulers and consumers** (Nest `@Cron`/`@Interval`/`@Processor`/`@OnEvent`, BullMQ, Celery beat, Sidekiq, Laravel `schedule`, Spring `@Scheduled`, Go cron) | a schedule marker ∩ a write (0a) | increments, recompute windows, replacement vs delta | recompute-and-replace a whole period; a guarded increment in the source transaction |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; 0 builds the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; a path glob is never combined with an extension glob (ripgrep ORs two positive `-g` globs). Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. **Migrations are in scope** (triggers, views, column types live there); tests are in scope only for §3 (a spec that reconciles is a control). Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the server roots and the migrations folder, e.g. ROOTS=(apps/api/src)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-mv.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock,min.js,snap}')
XM=(-g '!**/{migrations,migration,db/migrate}/**')
XT=(-g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**' -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/test_*.py' -g '!**/*_test.{py,go}')
CODE=(-g '*.{ts,mts,js,mjs,cjs,py,rb,php,java,kt,go,cs,sql,prisma,ex,exs}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# 0 THE DERIVED SURFACE — 0a scheduled/event writers · 0b insert…select…group by · 0c materialized views · 0d derived table names
SCH='@(?:Cron|Interval|Timeout|Processor|OnEvent|EventPattern|Scheduled)\b|\bcron\.schedule\(|\bnew\s+CronJob\(|\bschedule\.(?:every|scheduleJob)\b|@(?:shared_task|periodic_task)\b|\bbeat_schedule\b|\bsidekiq_options\b|\bShouldQueue\b|->(?:daily|hourly|everyMinute|cron)\(|\bnew\s+Worker\(|\.process\(\s*["\x27]'
h 0a; rg -l --pcre2 "$SCH" "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -l -i --pcre2 '\b(?:insert\s+into|upsert\w*|on\s+conflict|on\s+duplicate\s+key|update\s+"?\w+"?\s+set|createMany|bulk_create|insert_all|upsert_all|native(?:Insert|Update|Delete)|persist(?:AndFlush)?\(|increment\(|\$inc\b|update_counters|refresh\s+materialized)\b|\.save\(' | sort -u > "$OUT/SW.txt"; wc -l < "$OUT/SW.txt"
h 0b; rg -l -U --pcre2 '(?i)\binsert\s+into\s+"?[\w.]+"?[^;]{0,600}?\bselect\b[^;]{0,2000}?\bgroup\s+by\b' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | sort -u | tee "$OUT/ROLL.txt" | wc -l; ck 0b ${PIPESTATUS[0]}
h 0c; rg -n --pcre2 '(?i)\b(?:create|refresh|drop)\s+materialized\s+view\b' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}" | tee "$OUT/MV.txt" | wc -l; ck 0c ${PIPESTATUS[0]}
DS='(?i)(?:create\s+table\s+(?:if\s+not\s+exists\s+)?|tableName\s*:\s*|@@map\(\s*|db_table\s*=\s*|__tablename__\s*=\s*|table_name\s*=\s*|\$table\s*=\s*)["\x27`]?((?:\w+_)?\w+_(?:daily|hourly|weekly|monthly|summary|summaries|stats|rollups?|agg|aggregates?|totals|facts|snapshots?|usage|counters?|counts)|(?:daily|hourly|weekly|monthly)_\w+)(?!\w)["\x27`]?'
h 0d; rg -o -I --no-filename --pcre2 -r '$1' "$DS" "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | sort -u | tee "$OUT/DERIVED.txt" | tr '\n' ' '; echo
# the ORM classes mapped onto those tables (entity files only — migrations excluded — whose mapping line names the table), then every non-migration file naming a table or its class
rg -l --pcre2 "$DS" "${CODE[@]}" "${X[@]}" "${XT[@]}" "${XM[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -o -I --no-filename --pcre2 -r '$1' '\bclass\s+(\w+)' | sort -u > "$OUT/ENT.txt"
cat "$OUT/DERIVED.txt" "$OUT/ENT.txt" | while IFS= read -r t; do rg -l -w "$t" "${CODE[@]}" "${X[@]}" "${XT[@]}" "${XM[@]}" "${ROOTS[@]}"; done | sort -u > "$OUT/DREF.txt"
cat "$OUT/SW.txt" "$OUT/ROLL.txt" "$OUT/DREF.txt" | sort -u > "$OUT/F.txt"; echo "derived writers+readers: $(wc -l < "$OUT/DREF.txt" | tr -d ' ') · F: $(wc -l < "$OUT/F.txt" | tr -d ' ')"
F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/F.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
# 1 MV-1 non-idempotent rollup writes — SQL self-increments, ORM increments, upsert deltas — in scheduled/event writers only
h 1; rg -n --pcre2 '(?i)\bset\s+"?(\w+)"?\s*=\s*(?:"?\w+"?\.)?"?\1"?\s*[+-]|\bon\s+conflict\b[^;]{0,200}?\bdo\s+update\s+set\s+"?(\w+)"?\s*=\s*(?:"?\w+"?\.)?"?\2"?\s*\+|\.increment\(|->increment\(|\$inc\b|\bF\(\s*["\x27]\w+["\x27]\s*\)\s*\+|\bupdate_counters\b|\bincrement!\(' "${F[@]}" | "${NC[@]}"; ck 1 ${PIPESTATUS[0]}
# 2 MV-2 recompute windows and point-in-time snapshots — the window, and what changes after it (read)
h 2a; rg -n --pcre2 '(?i)\bsub(?:Days|Hours)\(|\b(?:window|lookback|recompute)_?days\s*[:=]\s*[1-9]\d*|\binterval\s+["\x27]\d+\s+days?["\x27]|\bnow\(\)\s*-\s*interval\b|\btimedelta\(\s*days\s*=|\bDuration\.ofDays\(|\.subtract\(\s*\d+\s*,\s*["\x27]days?' "${F[@]}" | "${NC[@]}"; ck 2a ${PIPESTATUS[0]}
h 2b; rg -l --pcre2 "$SCH" -g '**/*{snapshot,Snapshot,snapshots,history,History,closing,period,Period}*' "${X[@]}" "${XT[@]}" "${ROOTS[@]}"; ck 2b $?
# 3 MV-3 reconciliation — every derived table, and the files (tests included) that name it AND reconcile/recompute/compare
h 3; while IFS= read -r t; do r=$(rg -l -w "$t" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -l -i --pcre2 '\breconcil\w*|\brecompute\w*|\bmark\w*stale\b|\bdrift\b|\bverify\w*(?:Rollup|Total|Sum)' | tr '\n' ' '); def=$(rg -n -m1 -i --pcre2 "create\\s+table\\s+(?:if\\s+not\\s+exists\\s+)?[\"\x27\`]?${t}[\"\x27\`]?\\s*\\(" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | head -1 | cut -d: -f1,2); echo "$t defined-at=${def:-?} reconcile-files: ${r:-none}"; done < "$OUT/DERIVED.txt"
# 4 MV-4 invalidation — trigger events and column lists (read against the derived row's source columns); bulk paths that bypass row triggers
h 4a; rg -n -U --pcre2 '(?i)\b(?:after|before)\s+(?:insert|update|delete|truncate)(?:\s+or\s+(?:insert|update|delete|truncate))*(?:\s+of\s+[^\n]*(?:\n[^\n]*){0,3}?)?\s+on\s+"?[\w.]+"?' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4a ${PIPESTATUS[0]}
h 4b; rg -n --pcre2 '(?i)\btruncate\s+(?:table\s+)?"?\w+|\bnativeDelete\(\s*\w+\s*,\s*\{\s*\}\s*\)|\bdeleteMany\(\s*\)|\.delete\(\)\s*$|\bcopy\s+"?\w+"?\s*(?:\([^)]*\)\s*)?from\b' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -40; ck 4b ${PIPESTATUS[0]}
# 5 MV-5 materialized views — 5a refresh without CONCURRENTLY · 5b unique indexes on the views · 5c now()/current_date in a definition · 5d views never refreshed in the repo
h 5a; rg -n --pcre2 '(?i)\brefresh\s+materialized\s+view\s+(?!concurrently\b)"?[\w.]+' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5a ${PIPESTATUS[0]}
rg -o -I --no-filename --pcre2 -r '$1' '(?i)\bcreate\s+materialized\s+view\s+(?:if\s+not\s+exists\s+)?"?([\w.]+)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u > "$OUT/MVN.txt"
h 5b; while IFS= read -r v; do u=$(rg -c -i --pcre2 "create\\s+unique\\s+index\\b[^;]*\\bon\\s+\"?${v}\"?\\s*\\(" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l); r=$(rg -c -i --pcre2 "refresh\\s+materialized\\s+view\\s+(?:concurrently\\s+)?\"?${v}\\b" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l); echo "$v unique-index-files=$(echo $u) refresh-files=$(echo $r)"; done < "$OUT/MVN.txt"
h 5c; rg -n -U --pcre2 '(?i)\bcreate\s+materialized\s+view\b[^;]{0,3000}?\b(?:now\(\)|current_date|current_timestamp|localtimestamp)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg -i --pcre2 'now\(\)|current_(?:date|timestamp)|localtimestamp'; ck 5c $?
# 6 MV-6 grain vs zone — UTC-day buckets in derived writers, and tenant-zone readers of the derived tables (read both)
h 6a; rg -n --pcre2 '(?i)at\s+time\s+zone\s+["\x27]UTC["\x27]\s*\)?\s*::\s*date|\bdate_trunc\(\s*["\x27]day["\x27]\s*,\s*[^,)]+\)|\bDATE\(\s*\w+\s*\)|\bTruncDate\(' "${F[@]}" | "${NC[@]}"; ck 6a ${PIPESTATUS[0]}
DR=(); while IFS= read -r f; do DR+=("$f"); done < "$OUT/DREF.txt"; [ ${#DR[@]} -gt 0 ] || DR=("$OUT/none")
h 6b; rg -n --pcre2 '(?i)\b(?:time_?zone|tz|zone|iana|tenant_?zone|process_?zone|zone_?name)\b' "${DR[@]}" | "${NC[@]}" | rg -v --pcre2 '^[^:]+:\d+:\s*(?:import|from)\b' | head -30; ck 6b ${PIPESTATUS[0]}
# 7 TB-1 naive columns (7a) × queries with exactly one AT TIME ZONE on a line (7b); ORM truncation with no zone (7c) — the join is the read
h 7a; rg -n --pcre2 '(?i)\btimestamp(?:\(\d\))?\s+without\s+time\s+zone\b|"?\w+_at"?\s+timestamp(?:\(\d\))?\s*(?:not\s+null|null|default|,|$)|\btype\s*:\s*["\x27]timestamp["\x27]|\bcolumnType\s*:\s*["\x27]timestamp(?:\(\d\))?["\x27]|(?-i:^\s*\w+\s+DateTime\b(?![^\n]*@db\.Timestamptz))|(?-i:\bDATETIME\b)' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -60; ck 7a ${PIPESTATUS[0]}
h 7b; rg -n --pcre2 '(?i)^(?!.*\bat\s+time\s+zone\b.*\bat\s+time\s+zone\b).*\bat\s+time\s+zone\b' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 7b ${PIPESTATUS[0]}
h 7c; rg -n --pcre2 '\bTrunc(?:Date|Day|Hour|Week|Month)\((?![^)\n]*tzinfo)|\bgroup_by_(?:day|week|month|hour_of_day)\b(?![^\n]*time_zone)|\bdate_trunc\(\s*["\x27](?:day|week|month)["\x27]\s*,\s*"?\w+"?\s*\)' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -40; ck 7c ${PIPESTATUS[0]}
# 8 TB-2 BETWEEN on instants — SQL, Laravel, Django, Rails inclusive ranges, TypeORM
h 8; rg -n --pcre2 '(?i)\b\w*(?:_at|_time|timestamp|_ts)"?\s+between\b|\bwhereBetween\(\s*["\x27]\w*(?:_at|_time)["\x27]|\b\w+_at__range\s*=|\b\w+_at:\s*[\w.()]+\s*\.\.(?!\.)\s*[\w.()]+|\b\w+(?:At|Time)\s*:\s*Between\(' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 8 ${PIPESTATUS[0]}
# 9 TB-3 CONVERT_TZ with a named zone, and whether zone tables are loaded anywhere (Dockerfile, CI, infra, scripts)
h 9a; rg -n --pcre2 '(?i)\bconvert_tz\s*\([^)]*["\x27][A-Za-z]+/[A-Za-z_]+' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 9a ${PIPESTATUS[0]}
h 9b; rg -l 'mysql_tzinfo_to_sql|time_zone_name' --hidden "${X[@]}" "${ROOTS[@]}"; ck 9b $?
# 10 TB-4 DST-unsafe shifts — numeric offsets as zones, hour intervals as zone shifts, UTC day series for local days
h 10; rg -n --pcre2 '(?i)\bat\s+time\s+zone\s+["\x27][+-]?\d{1,2}(?::\d\d)?["\x27]|\bconvert_tz\s*\([^)]*["\x27][+-]\d\d:\d\d["\x27]\s*\)|^(?=[^\n]*(?:date_trunc|::date|\bdate\s*\(|to_char|at\s+time\s+zone))[^\n]*[+-]\s*interval\s+["\x27]\d+\s+hours?["\x27]|\bgenerate_series\([^)]*["\x27]1\s+day["\x27]' "${CODE[@]}" "${X[@]}" "${XT[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 10 ${PIPESTATUS[0]}
```

5b prints, per view, how many files hold a unique index on it and how many refresh it: `refresh-files=0` is a §5 candidate (precedent § 40 — ask whether pg_cron or a runbook refreshes it); `CONCURRENTLY` with `unique-index-files=0` fails at run time. §3 prints, per derived table, where it is defined and the files that name it and reconcile or recompute it: `reconcile-files: none` is a candidate unless the writer is a whole-period replacement (precedent § 22); a listed file is read for what it does on a mismatch (marks stale and fails, or only logs).

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s, 0 `rg` errors, nothing written): 0a 10 scheduled/event writers · 0b 5 rollup statements · 0c 8 materialized-view statements · DERIVED 10 tables. §1 2 (the cron counter, the BullMQ `increment`) · 2a 2 (the 2-day revenue window; the counter's 5-minute cursor, read and refuted) · 2b 2 (the merchant snapshot read as current; the labelled performance snapshot, precedent § 38) · §3 per-table definition and reconcile files (the usage table with none; the inventory reconcile that only logs; the order-day reconcile that marks stale, the control) · 4a 6 trigger lines (the revenue trigger that misses `total_cents`; the order-day triggers held equal by a spec, the control) · 4b 2 (the `truncate` reload) · 5a 2 · 5b 4 views (one `CONCURRENTLY` with no unique index; the one with its index) · 5c 1 (`now()` in a weekly view) · 6a 6 / 6b 7 (two tenant-zone readers of UTC-day tables; the quarter buckets beside them) · 7a 2 naive columns × 7b 12 single-conversion lines (two on the naive columns; the double conversion is not listed) · 8 2 · 9a 2, 9b 0 (no zone tables) · 10 2. Every MV and TB seed is listed; the fixture key records which decoys surface.
- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + Postgres monorepo, `ROOTS=(apps/api/src)`; 2.9 s; `find -newer` on the repo empty): 0a 5 · 0b 3 · 0c 0 · DERIVED 8 tables (the order-day and quarter facts, usage, counters, snapshots) · derived writers and readers 38 files. §1 1 — the order-code sequence counter, incremented in the order insert's own transaction (precedent § 19) · 2b 1 (the closed-period performance snapshot, labelled — precedent § 38) · §3 every table but an external-account snapshot has a recompute or reconcile file · 4a 19 lines: the three order-day triggers (insert, `update of` eleven columns over four lines, delete) — held equal to the fact columns by a spec, the MV-4 control · 4b 3 (`nativeDelete` of configuration tables in a reseed, not a source) · 5 0 views · 7a 0 naive instants (every column is `timestamptz`), so 7b's 13 single conversions print `checked (13 → 0)` · 8–10 0. **First drafts that this measurement corrected:** 4a read only one-line trigger headers (the real `update of` list spans four lines); 0d matched the prefix `order_rollup` of `order_rollup_builds` (now `(?!\w)`); 7a's Prisma lane matched Python's `from datetime import` (now case-sensitive); deriving entity classes from every file that names a table pulled 1,061 files into the surface (now only mapping files outside migrations: 38).
- **The MySQL, BigQuery, Snowflake and ClickHouse lanes are fixture-measured only.**

## The 3,000-hit path

1. **Build the derived inventory first** (0a–0d): one row per derived table with its writer, its trigger list and its readers. Every later grep is restricted to it; a `+ 1` outside a scheduled or event writer is not this class.
2. **Group by mechanism**, not by line: one shared bucket helper (`UTC_DAY(...)`) used by 40 queries is one §7 decision; one export base class is one row.
3. **Rank** by consumer: money and customer-facing screens first, admin counters last.
4. **Read the top 30 derived tables fully** (writer, window, trigger list, reconcile, readers' zone).
5. **Prefer the recompute oracle at scale**: on a scratch DB with the migrations applied and a seeded golden history (late refunds, deletes, a DST day), run every rollup job once and compare each derived table with a recompute from source (V564) — one query per table.
6. **Ledger the rest** as `Live, unreviewed (k tables / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes the derived table feeds a consumer (a dashboard, an export, an invoice, a payout). One step lower for an internal counter; money or a regulatory figure stays high.

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | MV-1 non-idempotent rollup write | high | V547 |
| 2 | MV-2 recompute window misses late changes; a point-in-time snapshot read as current | high | V548 |
| 3 | MV-3 derived table never reconciled, or reconciliation that only logs | medium | V564 |
| 4 | MV-4 invalidation drift: trigger/event list misses a source column; bulk paths bypass row triggers | medium | V564 |
| 5 | MV-5 materialized view never refreshed, blocking refresh, `CONCURRENTLY` without its unique index, `now()` in the definition | medium | V563 |
| 6 | MV-6 rollup grain cannot serve the consumer's zone | medium | V564 |
| 7 | TB-1 `AT TIME ZONE` direction on a naive column, or one conversion where two are needed | high | V552 |
| 8 | TB-2 `BETWEEN` end-inclusive on instants | medium | V552 |
| 9 | TB-3 `CONVERT_TZ` with a named zone and no zone tables (NULL bucket) | high | V552 |
| 10 | TB-4 DST-unsafe offsets in bucket SQL | medium | V552 |

### 1. Non-idempotent rollup write

```
BAD:   @Cron('*/5 * * * *') … update daily_sales set orders = orders + 1, revenue = revenue + $2 where day = $1
       on conflict (tenant_id, day) do update set total = daily_totals.total + excluded.total   -- a retried job adds twice
GOOD:  delete from order_day_facts where day = any($1); insert into order_day_facts … select … group by …   -- one transaction
       increment guarded by insert into processed_events (event_id) in the same transaction (unique key)
```
**Read the code:** Is the writer at-least-once — a cron that can overlap or rerun, a queue job with retries, an `@OnEvent` handler re-emitted, a consumer redelivered? Is the increment in the **same transaction** as the source write (precedent § 19 — a retry replays both or neither), or guarded by a processed-events key or a unique `(tenant, day)` constraint that makes the loser fail (§ 20)? Is there a rebuild path (a recompute job) if the counter drifts? **Finding when** a replay or a partial failure adds a source row's contribution twice to a consumed table. A message-consumer increment is also distributed-systems `messaging-scan` §2's — cite it. **Proof:** V547 — run the job twice, and kill it mid-batch and rerun: the rollup equals a recompute.

### 2. Recompute window misses late changes; a snapshot read as current

```
BAD:   recompute where created_at >= now() - interval '2 days'      -- a refund on day 5 never restates day 1
       performance_snapshots written once at 03:20 for yesterday, then shown on the "current" dashboard
GOOD:  dirty-period markers from insert/update/delete triggers (or updated_at) drive the recompute; the snapshot screen says "as of"
```
**Read the code:** What can change in the source after the window — a refund, a status, an amount edit, a delete, a late import? Does the window key on the **change** (`updated_at`, a dirty marker) or on the **creation** date? For a closed-period snapshot, who reads it and how is it labelled (precedent § 38 — point-in-time by design)? **Finding when** a source change after the window leaves a consumed derived row wrong forever, or a point-in-time row is presented as current. **Proof:** V548 — a refund dated D+3 for a day-D order: rollup(D) restated, or the reader labels it.

### 3. Never reconciled, or reconciliation that only logs

**Read the code:** For each `reconcile-files=0` table, is the writer a whole-period replacement from source (precedent § 22 — no separate check needed)? For each reconcile that exists, what happens on a mismatch — does it mark the period stale and recompute, fail a unit, alert; or only `logger.warn`? Does it compare the same grain and zone? **Finding when** an incremental or trigger-maintained derived table has no check that can catch drift, or the check cannot act. Books reconciliation (does the dashboard equal the ledger) is business `report-scan` §6. **Proof:** V564 — mutate the source behind the rollup on a scratch DB: the reconcile flags and fixes or fails.

### 4. Invalidation drift

```
BAD:   create trigger … after update of status, created_at on orders …   -- the rollup also sums total_amount and store_id
       truncate table order_items; copy order_items from …                   -- bypasses row triggers; no marker written
GOOD:  after update of <every column the rollup reads> + insert + delete triggers; a spec asserts the list equals the fact columns
```
**Read the code:** List the columns the derived row is computed from (the `select … group by` in the writer, joins included). Does every one appear in the trigger's `update of` list, and are insert **and** delete covered? Is the counter insert-only on a source that can update or delete (precedent § 17 flips back when any path deletes)? Do `TRUNCATE`, `COPY`, bulk `nativeDelete`/`deleteMany` or a retention purge touch the source without writing the marker? Is there a spec that holds the lists equal (the control)? **Finding when** a source change on an uncovered column or path leaves the derived row stale. The read of both lists is the two-ended fact. **Proof:** V564 — update the uncovered column on a scratch DB: the derived row is stale and the reconcile does not flag it.

### 5. Materialized view refresh

```
BAD:   create materialized view merchant_balances as select … where created_at > now() - interval '30 days'   -- frozen at refresh
       @Cron('0 * * * *') refresh materialized view merchant_balances      -- blocks every reader for the refresh
       refresh materialized view concurrently sales_mv                      -- no unique index on sales_mv: fails
GOOD:  create unique index on sales_mv (tenant_id, day); refresh materialized view concurrently sales_mv on a schedule
```
**Read the code:** Is every view refreshed somewhere in the repo (5b `refresh-files`) — or by pg_cron or a runbook outside it (precedent § 40: ask, never report as fact)? Does the refresh run while request paths read the view (precedent § 25 for small off-hours refreshes)? For `CONCURRENTLY`, is there a unique index **on plain columns, no `WHERE`, covering every row**, and is the view populated (the first refresh after `WITH NO DATA` cannot be concurrent)? Does the definition hold `now()`/`current_date` (precedent § 26 when the cadence is finer than the window and documented)? Engine: Postgres only — MySQL has no materialized views; never report this class there. **Finding when** readers block, the refresh fails, the view never refreshes, or a frozen `now()` is read as live. **Proof:** V563 — refresh under concurrent reads on a scratch DB.

### 6. Rollup grain cannot serve the consumer's zone

**Read the code:** What zone does the rollup bucket in (6a: `(created_at at time zone 'UTC')::date`)? Who reads it (6b), and with which zone — a tenant's `timeZone` setting, the user's browser zone? Are sub-day buckets kept beside the days (precedent § 21: 15-minute quarters re-bucket any zone)? Is the product single-zone with the zone documented? Which zone is *right* is business `report-scan` §8's; this skill reports that the stored grain cannot produce the zone the reader asks for. **Finding when** a tenant-zone reader sums UTC-day rows, so the edge hours land in the wrong local day. **Proof:** V564 with a 22:30Z row for a UTC+3 tenant: the local day's total equals a recompute in that zone.

### 7. `AT TIME ZONE` direction on a naive column

```
BAD:   created_at timestamp(3) (Prisma DateTime) holding UTC; select date_trunc('day', created_at at time zone $tz)
       -- on a naive column this ASSUMES the value is local in $tz and converts to UTC: shifted the wrong way
GOOD:  date_trunc('day', (created_at at time zone 'UTC') at time zone $tz)   -- or store timestamptz
```
**Read the code:** Is the column naive (7a: `timestamp without time zone`, Prisma `DateTime` without `@db.Timestamptz`, TypeORM `type: 'timestamp'`, MikroORM `columnType: 'timestamp'`) or aware? What does it hold — UTC written by the app, or local wall time? How many conversions does the query apply (7b lists lines with exactly one)? On an aware column one conversion is right; on a naive UTC column two are needed (precedent § 27). Is 2-arg `date_trunc` on a `timestamptz` depending on the session `TimeZone` (7c)? Django `Trunc*` without `tzinfo=` uses the current time zone; groupdate without `time_zone:` uses `Time.zone`. **Finding when** a bucket query shifts rows across a day boundary for a declared zone. **Proof:** V552 — the DST and midnight corpus through the real query on a scratch DB.

### 8. `BETWEEN` end-inclusive on instants

```
BAD:   where created_at between $1 and $2            -- a row at exactly 00:00:00 of the next day counts in both windows
       Order.where(created_at: from..to)             -- inclusive range on a timestamp
GOOD:  where created_at >= $1 and created_at < $2    -- half-open
```
**Read the code:** Is the column a timestamp (precedent § 29: a `date` column is discrete and fine)? Is the upper bound the next period's start, or a `23:59:59` end that drops sub-second rows? Do adjacent windows share a bound? **Finding when** a row on the boundary is counted in two windows or in none. **Proof:** V552 — a row at exactly local midnight, counted once across two adjacent windows.

### 9. `CONVERT_TZ` with a named zone and no zone tables

**Read the code:** Does the query pass a named zone (`'Asia/Riyadh'`)? Are the zone tables loaded anywhere — a `mysql_tzinfo_to_sql` step in the Dockerfile, an init script, the managed service's docs (RDS and Cloud SQL load them; say which)? Numeric offsets need no tables (and are §10's question). **Finding when** the engine the deployment runs has no zone tables, so every row falls into a NULL bucket. **Proof:** V552 — on a scratch MySQL, `select convert_tz(now(), '+00:00', 'Asia/Riyadh')` is NULL before `mysql_tzinfo_to_sql` and not after.

### 10. DST-unsafe offsets in bucket SQL

```
BAD:   at time zone '+01'  (Berlin)  ·  created_at + interval '3 hours'  ·  generate_series(start, end, '1 day') in UTC for local days
GOOD:  at time zone 'Europe/Berlin'  ·  a day series built in the local zone and converted per day
```
**Read the code:** Is the offset for a zone with DST? A fixed offset for a no-DST zone, documented, is not this class. Is an hour interval used to move between zones? Is a day series generated in UTC and labelled as local days? **Finding when** the 23- and 25-hour days are bucketed wrong for a declared zone. **Proof:** V552 on the Berlin and New York DST dates.

## Output

```
derived-data-scan — lanes: postgres 17 (compose) via mikro-orm 6.4; @nestjs/schedule; 3 derived tables · 1 materialized view
Surface: 0a 6 scheduled writers · 0b 2 rollups · 0c 3 MV statements · DERIVED: daily_sales order_day_facts tenant_usage_daily

Findings: 3 · Unconfirmed: 2

1. apps/reporting/src/reports/day-tally.job.ts:19                    [report-with-fix]   high
   §1 MV-1 — `update daily_sales set orders = orders + 1` in a BullMQ job with attempts: 5 and no processed-events guard.
   V547 on a scratch PG: a retried job → orders 2 for 1 order. Fix: recompute-and-replace the day (the module's existing whole-day rollup shape).
2. apps/reporting/migrations/Migration20260301.ts:44                  [report-with-fix]   medium
   §4 MV-4 — trigger `after update of status, created_at on orders`; the rollup sums total_amount (order-rollup.sql:12).
   Two-ended: the trigger list and the writer's select. Fix: add total_amount + a spec holding the lists equal.
3. apps/reporting/src/reports/hourly.query.ts:9                       [report-with-fix]   high
   §7 TB-1 — created_at is `timestamp(3)` (schema.prisma:41, no @db.Timestamptz) holding UTC; one `at time zone $tz`.
   V552: 2026-06-01T22:30Z → Riyadh 2026-06-01 (expected 2026-06-02). Fix: (created_at at time zone 'UTC') at time zone $tz.
4. apps/reporting/src/reports/merchant-balances.job.ts:12             [report-flagged]    medium
   §5 MV-5 — hourly `refresh materialized view merchant_balances` without CONCURRENTLY. Unproven link: whether a request
   path reads the view during the refresh (two readers found, both admin). Settling: V563.
5. apps/reporting/src/reports/payout.query.ts:27                       [report-flagged]    high
   §9 TB-3 — CONVERT_TZ(paid_at, '+00:00', 'Asia/Riyadh'). Unproven link: zone tables on the managed MySQL. Settling: V552.

Routed: 1 → business report-scan §8 (which zone the payout report uses) · 1 → distributed-systems messaging-scan §2
Verification: 19 candidates → 3 findings · 2 unconfirmed · 4 hardening · 10 refuted (self-verified; precedents § 20, § 21, § 22, § 27, § 29)

Class coverage:
  §1 increments            checked (1 3 → 1 finding; 2 refuted: guarded by a unique (tenant, day) — precedent § 20)
  §2 recompute window      checked (2a 2 + 2b 1 → 0; the snapshot screen says "as of", precedent § 38)
  §3 reconciliation        checked (3 tables, 1 reconcile-files=0 → hardening: whole-day replacement, precedent § 22)
  §4 invalidation          checked (4a 4 + 4b 1 → 1 finding)
  §5 materialized views    checked (5a 1 · 5b 1 view · 5c 0 → 1 unconfirmed)
  §6 grain vs zone         checked (6a 2 + 6b 3 → 0; quarter buckets beside days, precedent § 21)
  §7 naive AT TIME ZONE    checked (7a 2 + 7b 9 → 1 finding; 6 on timestamptz, 2 double conversions — precedent § 27)
  §8 BETWEEN on instants   checked (8 2 → 0; both on date columns, precedent § 29)
  §9 CONVERT_TZ            checked (9a 1, 9b 0 → 1 unconfirmed)
  §10 DST offsets          checked (10 0)
```

`[report-with-fix]`: the oracle failed on a scratch DB with the project's migrations, or the fact is two-ended (both lists, or the column type and the query), and the fix is local to the writer, the trigger, the view or the query. `[report-flagged]`: one link is unproven (the reader's timing, the managed engine's zone tables, the declared zone, whether a request path reads the view); the row names it and the settling oracle. The coverage block lists **all ten** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 17 an insert-only counter on an append-only source; § 19 the increment in the source's own transaction; § 20 a guarded increment or a find-then-insert behind a unique `(tenant, day)`; § 21 sub-day buckets beside UTC days; § 22 a whole-period replacement; § 38 a closed-period snapshot labelled as such.
- § 25 an off-hours refresh of a small view; § 26 `now()` in a view refreshed finer than its window; § 40 a refresh managed outside the repo; § 27 the double `AT TIME ZONE`; § 29 `BETWEEN` on `date`.

## When to run

- On any diff that touches a rollup writer, a trigger, a materialized view, a bucket query, a scheduled or event writer that updates a summary table, or a column type an aggregate reads — `/audit-data-quality`'s derived-data signal.
- On every whole-repo `/audit-data-quality`, reporting all ten §s; before a new dashboard reads an existing rollup.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the derived table, its source columns, the `file:line` and the source change — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@data-quality-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Never run a rollup job, a refresh or a bucket query against a shared or production database.** Oracles run on a throwaway Postgres/MySQL container with the project's migrations, or inside `BEGIN … ROLLBACK` on a database the user confirmed is not production; a probe that cannot be isolated is `NOT-RUN`.
- **This skill writes nothing into the audited repo.** `find <root> -newer "$OUT/SW.txt"` is empty at the end; a fix is `/data-fix`'s.
- **No `[report-with-fix]` without the V-oracle failing** or a two-ended fact (both column lists; the column type and the query). **Never report MV-5 on MySQL** (no materialized views) or a zone defect without reading the column type.
- **Do not decide the zone.** A missing zone policy is `UNDECLARED` and the row routes to business `report-scan` §8; never pick "the tenant's zone" for the user.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the rollups look consistent"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill; `@data-quality-auditor` judges MV and TB rows; `/data-fix` closes them with V547/V548/V552/V563/V564 failing first.
- This pack: `data-test-scan` §6 (dbt rollup reconciliation), `extract-scan` (exports built from rollups), `pii-copy-scan` §2 (identifiers kept in rollups), `incremental-load-scan` (warehouse loads).
- business `report-scan` §8/§9, distributed-systems `messaging-scan` §2, backend `job-lifecycle-scan`, database `schema-integrity-scan` §5, code-quality `correctness-smell-scan` §6, when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): PostgreSQL 18 docs — `REFRESH MATERIALIZED VIEW` (unique-index and blocking rules) and date/time functions (`AT TIME ZONE` on `timestamp` vs `timestamptz`, `date_trunc` session zone, `now()` at transaction start); MySQL 8.4 date/time functions (`CONVERT_TZ` NULL without zone tables); PostgreSQL wiki "Don't Do This" (`BETWEEN` on timestamps); Prisma type mapping (`DateTime` → `timestamp(3)`, UNVERIFIED in the research); Django 5.2 database functions (`Trunc*` `tzinfo`); groupdate README; Snowflake, BigQuery and ClickHouse datetime docs as catalogued there (DE-B-1…19). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
