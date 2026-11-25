---
name: incremental-load-scan
description: "Batch and incremental loads: lookback, merge key, deletes, dedup, schema drift, overwrite scope, backfill, CDC."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: incremental-load-scan

## Premise

An incremental load is a promise that every source row lands in the target **exactly once and stays current**: a row committed with the same timestamp as the last run's maximum, a row that arrives two days late, a row updated after it was loaded, a row deleted at the source, a run retried after a crash, a backfill over a range already loaded. Each is a different mechanism, and none fails a test that loads ten rows once. **The defaults are the defect** (dbt docs, accessed 2026-10-19): `on_schema_change` is `ignore`, so new upstream columns never arrive; `append` never deduplicates and ignores `unique_key`; a NULL in any `unique_key` column never matches, so the merge inserts a duplicate; snapshot `hard_deletes` is `ignore`, so a deleted entity stays current forever. Spark's `partitionOverwriteMode` is `STATIC` (Spark 4.2 configuration), so `mode("overwrite")` deletes every partition, not only the ones the run wrote.

This skill owns research ids IN-1…IN-10 (`research-data-engineering.md` § 1.1), shipped as `DE-IN-<n>`: **whether a batch or incremental load writes each source row exactly once and keeps late, updated and deleted rows.**

**Every finding cites the load `<file:line>` + the effective config it runs under and where each value came from (model `config()` → properties YAML → `dbt_project.yml` `+key` → default) + the source row that is lost or doubled (a tie, a late row, a NULL key, a delete, a retry) + the oracle or the test that would settle it + the fix in the project's own tool.** A grep hit is a candidate. "The loads look idempotent" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V540–V546, V549 and V550.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The load runs on a schedule or a trigger that production uses: a dbt job in CI/cron/dbt Cloud, an Airflow/Dagster/Prefect task, a Spark job, a scheduled application writer, a CDC connector. A one-off backfill script that already ran fails here unless it is the documented re-run path.
2. **The contract is read.** The grain (what one target row is), the source's mutation pattern (append-only, updated in place, hard-deleted), and the latest a row can arrive — from the model's docs, the source system, or the loader. Without the grain the row is `[report-flagged]` with the grain named as the gap.
3. **No existing control, across files.** A merge on the grain key, a lookback window, a `delete … where <partition>` before the insert, a `qualify` with a total order, a `not_null` test on the key, a soft-delete flag the staging model filters, an explicit `on_schema_change`, `partitionOverwriteMode=dynamic` or Delta `replaceWhere`, a CDC sink that merges by key and source position.
4. **The oracle fired, or the fact is two-ended.** The replay/late-row/delete oracle ran on a scratch target and the target is wrong; or the static fact cites both ends — the effective config value and its source, plus the source system's behaviour that makes the default wrong (a source with `updated_at`, a source that hard-deletes).

## Boundaries

- **Message consumers and CDC *consumers* in application code** (dedup, ack order, poison messages, outbox, gap-blind event cursors) → distributed-systems `messaging-scan` §1–§3 and `dual-write-scan` §5/§6, when that pack is installed; without it the row is `[report-flagged]` here with the route named. This skill owns a CDC stream **landing into a warehouse or lake table** (§10).
- **A report's filter, definition or zone** → business `report-scan`; **an application scheduler's overlap, misfire or zone** → backend `job-lifecycle-scan` §4–§6; **a data orchestrator's run semantics** (wall-clock windows, catchup, trigger rules, retries) → `orchestration-scan` (this pack). OR-5 (retries) and §2 here meet on the same write: the non-idempotent write is §2's; the retry that replays it is `orchestration-scan` §5's.
- **Whether a data test can fail** → `data-test-scan`; **an in-app rollup or materialized view** (counter increments, recompute windows) → `derived-data-scan` (this pack); **the cost of a merge with no target bound** → `warehouse-scan-audit` §2.
- **The backfill *plan*** stays `/backfill-plan`; §8 here reports the load shape that makes a backfill double-count.

## Effective config — defaults the verdict reads

| Setting | Default when unset | Source (accessed 2026-10-19) | The class it feeds |
|---|---|---|---|
| dbt `materialized` | `view` | dbt docs | — |
| dbt `incremental_strategy` | adapter default — printed `adapter-default`, read from the installed adapter's docs, never guessed | dbt Incremental strategy | §2 |
| dbt `unique_key` | none: every returned row is inserted | dbt Incremental models | §2 |
| dbt `on_schema_change` | `ignore`: added columns silently not added, removed columns fail the run | dbt Incremental models | §6 |
| dbt snapshot `hard_deletes` (≥ 1.9) | `ignore`; `invalidate_hard_deletes` is the ≤ 1.8 flag | dbt Snapshots | §4 |
| dbt microbatch | `event_time`, `begin`, `batch_size` required; `lookback` 1; Postgres merges (needs `unique_key`), BigQuery/Spark insert-overwrite (need `partition_by`); all times UTC | dbt Microbatch | §9 |
| constraints | enforced in full only on Postgres; Snowflake, BigQuery, Redshift, Databricks enforce `not_null` (Databricks also `check`) and keep PK/unique/FK as metadata | dbt constraints | §2 (a declared PK is no dedup proof) |
| Spark `spark.sql.sources.partitionOverwriteMode` | `STATIC`: overwrite deletes every matching partition; Hive serde tables are always dynamic | Spark 4.2.0 configuration | §7 |
| Spark `mergeSchema` | `false` | Spark 4.2.0 configuration | §6 |
| Debezium (Postgres) | a delete is an event plus a tombstone; a table with no PK under `REPLICA IDENTITY DEFAULT` emits no update/delete; unchanged TOAST columns arrive as `unavailable.value.placeholder`; 3.2 replaced `drop.tombstones` / `delete.handling.mode` | Debezium 3.7 Postgres connector docs; 3.2.0.Final notes (2025-07-09) | §10 |

`scripts/model-graph.py` (this skill's folder; stdlib Python 3.8+, `--self-test`) is the pack's shared dbt reader: it parses the project **without dbt** — models, `ref`/`source`, effective configs with their source, `is_incremental()` branches, snapshots, tests, sources, exposures, unit tests — and writes `models.tsv`, `edges.tsv`, `tests.tsv`, `sources.tsv`, `snapshots.tsv`, `incremental.tsv`, `candidates.tsv` and `graph.json` under `--out` (refused inside the scanned root). Exit 0 built · 2 blocked · 4 no dbt project. `data-test-scan`, `lineage-trace`, `contract-diff`, `warehouse-scan-audit` and `grain-probe` read the same tables; quote the printed source of every effective value in a finding.

## Adapt to the codebase — the lanes

Read the tool **and its version** from the files (`dbt_project.yml` `require-dbt-version`, a `dbt-core` / `dbt-<adapter>` pin, `pyspark` / `delta-spark` pins, the Debezium image tag, `package.json`), never from memory, and print the lanes you ran in the output header.

| Lane | Detect by | Per-class read | Fix primitive |
|---|---|---|---|
| **dbt** (Core / Fusion, any adapter) | `dbt_project.yml` | `model-graph.py` candidates `IN-*` (configs, `is_incremental()` branches, snapshots, tests on key columns) — no dbt run needed | `unique_key` + merge / delete+insert; `>=` + lookback; `qualify row_number() over (… order by ts, id)`; `on_schema_change: append_new_columns` or `fail`; `hard_deletes: invalidate` / `new_record`; microbatch keys |
| **SQLMesh** | `MODEL (` in `*.sql`, `config.yaml` | `kind INCREMENTAL_BY_TIME_RANGE` (needs `time_column`), `INCREMENTAL_BY_UNIQUE_KEY` (`unique_key`), `lookback` | the kind's own keys |
| **Spark / Databricks** | `pyspark`, `SparkSession`, `.write.mode(`, `MERGE INTO`, notebooks (`.py`, `.ipynb`) | overwrite mode, `dropDuplicates`, window order, `mergeSchema` | `partitionOverwriteMode=dynamic`, Delta `replaceWhere`, `MERGE` on the key with a `whenMatchedDelete` branch |
| **Plain SQL / Python ETL** | `INSERT INTO … SELECT`, `COPY`, `MERGE`, `to_sql(`, `executemany(`, `read_sql(` in a scheduled file | watermark read, advance and compare; dedup on write | `ON CONFLICT … DO UPDATE` / `MERGE`; advance the watermark after the commit, in the same transaction |
| **In-app scheduled writers** (Nest `@Cron`/`@Interval`/`@Processor`, BullMQ, Celery beat, Sidekiq, Laravel `schedule`, Spring `@Scheduled`) | a schedule marker ∩ a write in one file (grep 0e) | the same as plain SQL; the rollup/MV classes are `derived-data-scan`'s | the same |
| **CDC landing** (Debezium, Kafka Connect sinks, Fivetran/Airbyte soft-delete columns) | connector JSON/YAML/properties, `_fivetran_deleted`, `_ab_cdc_deleted_at` | tombstones, delete handling, sink insert mode, PK-less tables | upsert/merge sink keyed by PK + source LSN; staging filters the delete flag |

Version gates: dbt ≤ 1.8 vs ≥ 1.9 (snapshot flags, microbatch), dbt ≥ 1.11 telemetry variable prefix `DBT_ENGINE_`; Spark 3 vs 4 (ANSI on by default in 4); Debezium < 3.2 vs ≥ 3.2 (delete options renamed).

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; G and 0 build the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; a path glob is never combined with an extension glob (ripgrep ORs two positive `-g` globs). Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the pipeline and app roots, e.g. ROOTS=(analytics dags apps/api/src)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-inc.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories,d}.*' -g '!**/test_*.py' -g '!**/*_test.{py,go}' -g '!**/conftest.py'
   -g '!**/{locales,locale,i18n,translations}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock,min.js}')
XM=(-g '!**/{migrations,migration,db/migrate}/**')
CODE=(-g '*.{py,ipynb,scala,sql,ts,mts,js,mjs,rb,php,java,kt,go,cs}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# G  the dbt graph without dbt (incremental-load-scan/scripts/model-graph.py): exit 0 built · 4 no dbt project (dbt lane N/A) · 2 blocked
MG=.claude/skills/incremental-load-scan/scripts/model-graph.py
if command -v python3 >/dev/null 2>&1 && [ -f "$MG" ]; then python3 -I -B "$MG" "${ROOTS[@]}" --out="$OUT/graph" --class=IN,CO > "$OUT/graph.txt" 2> "$OUT/graph.err"; echo "G model-graph exit $? → $OUT/graph.txt"; sed -n '2,8p' "$OUT/graph.txt"; grep '^\[' "$OUT/graph.txt"
else echo 'G NOT-RUN (python3 or model-graph.py absent): the dbt lane is read by hand from 1a, 2a, 4a, 6a, 9a and prints Live, unreviewed'; fi
# 0 THE LOAD SURFACE — 0a dbt/SQLMesh projects · 0b Spark/Python/SQL loaders · 0c CDC configs · 0d backfill entry points · 0e scheduled writers
h 0a; rg --files -g '**/dbt_project.yml' -g '**/sqlmesh.yaml' "${X[@]}" "${ROOTS[@]}"; ck 0a $?
h 0b; rg -l -U --pcre2 '\b(?:pyspark|SparkSession|spark\.read|\.write\.mode\(|to_sql\(|read_sql\w*\(|executemany\(|copy_expert\(|(?i:merge\s+into\s+[\w."`]+(?:\s+(?:as\s+)?\w+)?\s+using\b|copy\s+[\w."]+\s*(?:\([^)]*\)\s*)?from\s+(?:stdin|\x27|\$|:)))' "${CODE[@]}" "${X[@]}" "${XM[@]}" "${ROOTS[@]}" | tee "$OUT/ETL.txt" | wc -l; ck 0b ${PIPESTATUS[0]}
h 0c; rg -l --pcre2 'io\.debezium|\bdebezium\b|"connector\.class"|^\s*connector\.class\s*[=:]|_fivetran_deleted|_ab_cdc_deleted_at' -g '*.{json,yml,yaml,properties,tf,py,sql}' "${X[@]}" "${ROOTS[@]}" | tee "$OUT/CDC.txt"; ck 0c ${PIPESTATUS[0]}
h 0d; rg -n --pcre2 '(?:dbt\s+(?:run|build)\b[^\n]*--full-refresh|airflow\s+dags\s+backfill|\bdagster\s+\w*\s*backfill|--event-time-(?:start|end)|\bbackfill\w*\s*[:=(])' -g '*.{yml,yaml,sh,py,toml,json,cfg}' -g '**/Makefile' -g '**/Dockerfile*' -g '**/crontab*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 0d ${PIPESTATUS[0]}
SCH='@(?:Cron|Interval|Timeout|Processor|Scheduled)\b|\bcron\.schedule\(|\bnew\s+CronJob\(|\bschedule\.(?:every|scheduleJob)\b|@(?:shared_task|periodic_task)\b|\bbeat_schedule\b|\bsidekiq_options\b|\bShouldQueue\b|->(?:daily|hourly|everyMinute|cron)\(|\bfrom\s+airflow\b|@(?:dag|asset|flow)\b|\bDAG\('
h 0e; rg -l --pcre2 "$SCH" "${CODE[@]}" "${X[@]}" "${XM[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -l -i --pcre2 '\b(?:insert\s+into|upsert\w*|on\s+conflict|merge\s+into|to_sql\(|bulk_create|insert_all|upsert_all|createMany|native(?:Insert|Update|Delete)|persist(?:AndFlush)?\(|executemany|update\s+"?\w+"?\s+set)\b|\.save\(' | sort -u > "$OUT/SW.txt"; wc -l < "$OUT/SW.txt"
cat "$OUT/SW.txt" "$OUT/ETL.txt" | sort -u > "$OUT/LOAD.txt"; F=(); while IFS= read -r f; do F+=("$f"); done < "$OUT/LOAD.txt"; [ ${#F[@]} -gt 0 ] || F=("$OUT/none")
# 1 IN-1 watermark — 1a dbt hand lane (strict > on max()); 1b loaders: a timestamp compared with > to a bound parameter or a max() (read the lookback)
h 1a; rg -n --pcre2 '(?i)(?<![<=>-])>\s*\(\s*select\s+(?:coalesce\s*\(\s*)?max\s*\(' -g '*.sql' "${X[@]}" "${ROOTS[@]}"; ck 1a $?
h 1b; rg -n -U --pcre2 '(?i)\b\w*(?:updated|modified|changed|synced|loaded|created|event|ingested)_?at\b["`\]]?\s*>\s*(?:\$\d+|\?|%s|%\(\w+\)s|:\w+|\$\{|\{\w*\}|\(\s*select\s+(?:coalesce\s*\(\s*)?max\()|\b(?:updatedAt|modifiedAt|syncedAt|createdAt)\s*:\s*\{\s*\$?gt\s*:|\b\w+_at__gt\s*=' "${F[@]}" | "${NC[@]}"; ck 1b ${PIPESTATUS[0]}
# 2 IN-2 no merge key — 2a dbt hand lane: incremental models with no unique_key; 2b INSERT…SELECT with no ON CONFLICT / MERGE; 2c append writers
#   (2c spans lines: pandas `to_sql(` is usually multi-line and nests `get_engine()` — the old one-line `[^)\n]*` form found 0 of 2 such calls in a sample, 2026-10-19; data-pipelines 1 → 1)
h 2a; rg -l --pcre2 'materialized\s*=\s*["\x27]incremental' -g '*.sql' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bunique_key\b|insert_overwrite|microbatch'
h 2b; rg -n -U --pcre2 '(?i)\binsert\s+into\s+[\w."`]+(?:\s*\([^)]{0,400}\))?\s*select\b(?![^;]{0,1200}?\bon\s+(?:conflict|duplicate\s+key)\b)' "${F[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
h 2c; rg -n -U --pcre2 '\bto_sql\((?:[^()]|\([^()]*\))*?\bif_exists\s*=\s*["\x27]append|\.write\.mode\(\s*["\x27]append|\binsertInto\(|"?insert\.mode"?\s*[:=]\s*"?insert\b' "${CODE[@]}" -g '*.{json,properties,yml,yaml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2c ${PIPESTATUS[0]}
# 3 IN-3 load-time clock — 3a filters on load/processing columns; 3b watermark state written (read whether before the sink commits); 3c naive watermark types
LC='(?:_?loaded_at|_etl_\w+|ingested_at|inserted_at|_fivetran_synced|_airbyte_extracted_at|_sdc_batched_at|_load_ts)'
h 3a; rg -n --pcre2 "(?i)\\b$LC\\b[\"\`]?\\s*>=?\\s*" -g '*.sql' "${X[@]}" "${F[@]}" "${ROOTS[@]}" | "${NC[@]}" | sort -u; ck 3a ${PIPESTATUS[0]}
h 3b; rg -n --pcre2 '(?i)\bset_?watermark\w*\(|\bVariable\.set\(|\b(?:state|watermarks?|cursors?|checkpoints?|sync\w*)\.set\(|\.set\(\s*["\x27][\w:-]*(?:sync|watermark|cursor|last|checkpoint)|\b(?:last_?(?:run|sync|synced|loaded)\w*|watermark|high_?water\w*)\s*=\s*(?!=|(?:await\s+)?[\w.]*\.get\w*\()|\bupdate\s+"?\w*(?:state|watermark|cursor|checkpoint|sync)\w*"?\s+set\b' "${F[@]}" | "${NC[@]}"; ck 3b ${PIPESTATUS[0]}
h 3c; rg -n --pcre2 '(?i)\btimestamp_ntz\b|\btimestamp\s+without\s+time\s+zone\b|::timestamp\b(?!tz)|\bDATETIME\b' -g '*.sql' "${X[@]}" "${XM[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -50; ck 3c ${PIPESTATUS[0]}
# 4 IN-4 deletes — 4a snapshots with no hard-delete handling (hand lane); 4b MERGE files with no delete branch (read each)
h 4a; rg -l --pcre2 '\{%-?\s*snapshot\s+\w+|^\s*relation:\s' -g '**/snapshots/**' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bhard_deletes\b|\binvalidate_hard_deletes\b'
h 4b; rg -l -U --pcre2 '(?i)\bmerge\s+into\s+[\w."`]+(?:\s+(?:as\s+)?\w+)?\s+using\b' "${CODE[@]}" "${X[@]}" "${XM[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '(?i)\bwhen\s+matched\s+and\b[^\n]{0,160}\b(?:op|_op|__op|_change_type|is_deleted|__deleted|_fivetran_deleted|deleted_at|_deleted)\b|whenMatchedDelete|\bthen\s+delete\b'
# 5 IN-5 non-deterministic dedup — one order key in row_number(), dropDuplicates/drop_duplicates, distinct on
h 5; rg -n -U --pcre2 '(?i)\brow_number\s*\(\s*\)\s*over\s*\(\s*partition\s+by\s+[^)]*?\border\s+by\s+[^,()]+(?:\([^()]*\))?\s*(?:asc|desc)?\s*(?:nulls\s+(?:first|last)\s*)?\)|\.(?:dropDuplicates|drop_duplicates)\(|\bdistinct\s+on\s*\(' "${CODE[@]}" "${X[@]}" "${XM[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 5 ${PIPESTATUS[0]}
# 6 IN-6 schema drift — 6a dbt hand lane (incremental, no on_schema_change); 6b Spark landing reads with no mergeSchema
h 6a; rg -l --pcre2 'materialized\s*=\s*["\x27]incremental' -g '*.sql' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match 'on_schema_change'
h 6b; rg -l --pcre2 'spark\.read\.(?:parquet|format\(\s*["\x27](?:parquet|json|avro))' "${F[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match 'mergeSchema'
# 7 IN-7 overwrite scope — overwrite writers with no dynamic mode / replaceWhere; truncate-and-reload in loaders
h 7a; rg -l --pcre2 '\.mode\(\s*["\x27]overwrite["\x27]\s*\)|\bINSERT\s+OVERWRITE\b' "${F[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'partitionOverwriteMode["\x27,\s]+(?:["\x27])?dynamic|replaceWhere'
h 7b; rg -n --pcre2 '(?i)\btruncate\s+(?:table\s+)?[\w."`]+|\bif_exists\s*=\s*["\x27]replace' "${F[@]}" | "${NC[@]}"; ck 7b ${PIPESTATUS[0]}
# 8 IN-8 backfill — 0d entry points above; read each against the target's strategy (append target + range re-run = double count)
# 9 IN-9 microbatch — hand lane: microbatch models (read event_time, begin, batch_size, unique_key / partition_by per adapter)
h 9a; rg -n --pcre2 'incremental_strategy\s*[=:]\s*["\x27]?microbatch' -g '*.{sql,yml,yaml}' "${X[@]}" "${ROOTS[@]}"; ck 9a $?
# 10 IN-10 CDC landing — delete/tombstone handling, TOAST placeholder, sink insert mode, include lists; PK-less tables (migrations IN scope)
h 10a; [ -s "$OUT/CDC.txt" ] && tr '\n' '\0' < "$OUT/CDC.txt" | xargs -0 rg -H -n --pcre2 'ExtractNewRecordState|delete\.handling\.mode|drop\.tombstones|delete\.tombstone\.handling\.mode|tombstones\.on\.delete["\x27]?\s*[:=]\s*["\x27]?false|unavailable\.value\.placeholder|insert\.mode|table\.include\.list|snapshot\.mode'
h 10b; rg -n --pcre2 '(?i)\breplica\s+identity\b' -g '*.{sql,ts,js,py,rb,php}' "${ROOTS[@]}"; ck 10b $?
```

### Measured (2026-10-19)

- **Scratch sample** (a dbt-postgres 1.9 project — 5 models, 1 SQL snapshot, 3 source tables; three Airflow DAG files, a Dagster and a Prefect file, two Spark jobs, a pandas loader, a Debezium source + JDBC sink, a Nest `@Cron` sync job): under 1 s, 0 `rg` errors, `find -newer` empty. G: model-graph exit 0, 6 `IN` candidates — strict `>` on `_loaded_at` with no lookback (§1 + §3), no `unique_key` (§2), a one-key `row_number()` (§5), `on_schema_change` default `ignore` (§6), the snapshot with no hard-delete handling (§4); the `>=` + `interval '3 days'` model with a key stays quiet (precedent § 2). 0e 3 scheduled writers. 1b 2 (the pandas `> %s`, the Nest `> $1`). 2b 4 statements (two `DELETE … ; INSERT … SELECT` pairs — the delete is the control, read it — and two bare inserts). 2c 2 (`to_sql(if_exists="append")`, the sink's `insert.mode`). 3b 3 lines (both watermarks advanced before the read). 5 2 (`row_number()`, `dropDuplicates(["order_id"])`). 7a 1 (the job with `partitionOverwriteMode=dynamic` is excluded). 10a 4 lines.
- **Fixtures** (26 trees under `benchmarks/fixtures/`): 0 `rg` errors; G exits 4 on every tree (no dbt project → the dbt lane prints N/A); 0a 0. Only `ds-defects` has a load surface: 0c 4 (three Debezium connectors), 1b 1 (an event-store projector cursor `created_at > $1` → distributed-systems `dual-write-scan` §6), 2b 3 statements (a statement-close and a daily-volume rollup → `derived-data-scan`; a reconciliation adjustment → read), 3b 1 (an outbox feed cursor → distributed-systems), 10a 8 lines (two outbox connectors with `tombstones.on.delete` false → precedent § 18 and distributed-systems; one table-CDC connector with `snapshot.mode` initial — the §10 read). 0e lists 15 / 4 / 1 scheduled writers in `ds-defects` / `backend-defects` / `slow-marketplace`.
- **Real repo, read-only** (a NestJS 11 + Fastify + MikroORM 6 + Postgres monorepo, `ROOTS=(apps/api/src)`; 0.6 s; nothing written): G exit 4; 0a–0d 0 (no dbt, Spark, CDC or backfill entry point). 0e 5 — four queue consumers (→ distributed-systems `messaging-scan`) and a usage processor whose find-then-insert sits behind a unique `(tenant, day)` constraint (precedent § 20). 1b 0, 3b 0. 5: 4 `distinct on` in report queries (latest row per order — the order-by is the read). A first draft of 0b and 4b matched the phrase "merge into" in a comment; both now require `MERGE INTO … USING`. A first draft of 0e found 0 scheduled writers: the jobs write through MikroORM (`persist`, `nativeUpdate`, `.save(`), now in the write set.
- **The warehouse lanes are fixture-measured only**: no real dbt, Spark or Debezium repo is in the program's allowed set (eval O-2). Every dbt/Spark/CDC count above comes from the scratch sample until one is granted.

## The 3,000-hit path

1. **Build the graph once** (G). On a dbt project every `IN-*` row arrives with its effective config and source; group by **(config source, class)** — one `+on_schema_change` missing in `dbt_project.yml` is one decision for every model under that path, and the fix is one line there.
2. **Intersect** the loader greps with `$OUT/LOAD.txt` (scheduled writers + ETL files); a watermark word outside a scheduled writer is noise (eval § 3.4: 81 watermark lines → the rollup files on a real repo).
3. **Rank** by consumption: models with exposures or `access: public` and tables an export or a BI tool reads first; staging last.
4. **Read the top 30 groups fully** (the grain, the source mutation pattern, the latest arrival).
5. **Prefer the replay oracle at scale**: build the project into duckdb from committed seeds (`dbt build --target` a duckdb profile in `$OUT`) and run V540 over every incremental at once — two runs, identical counts and checksums.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

Severity assumes the target feeds a consumer (a mart, an export, a dashboard, a model contract). One step lower for a staging-only or internal-scratch table; a row loss in a table feeding money or a regulatory report stays high.

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | IN-1 strict `>` watermark or no lookback | high (`>` without lookback) / medium (`>=` without lookback) | V541, V542 |
| 2 | IN-2 no merge key, a key that is not the grain, or a nullable key | high | V540 |
| 3 | IN-3 load-time clock, wrong-zone watermark, watermark advanced before the write commits | medium | V541 |
| 4 | IN-4 source deletes never reach the target | high | V543 |
| 5 | IN-5 non-deterministic dedup | medium | V544 |
| 6 | IN-6 schema drift silently dropped or fatal late | medium | V545 |
| 7 | IN-7 overwrite wipes more than the run's partitions | high | V546 |
| 8 | IN-8 backfill re-appends history or runs in place beside the schedule | high | V549, V550 |
| 9 | IN-9 microbatch misconfiguration | high | V541 |
| 10 | IN-10 CDC landing loses, keeps or corrupts rows | high | V543, V540 |

### 1. Strict `>` watermark, or no lookback

```
BAD:   {% if is_incremental() %} where updated_at > (select max(updated_at) from {{ this }}) {% endif %}
       rows = db.query('select * from orders where updated_at > $1', [lastSyncedAt])
GOOD:  where updated_at >= (select max(updated_at) from {{ this }}) - interval '3 days'   -- with a merge on the key
```
**Read the code:** Which column is the watermark — event time, an update stamp the source sets, or a monotonic sequence? Can two rows share its value and commit at different times (a batch insert, a clock at second precision)? What is the latest a row can arrive (replication lag, a mobile client, a partner file)? Is there a lookback, and is the load a merge (so the lookback re-reads without duplicating — precedent § 2)? **Finding when** a tie or a late row inside the documented arrival window is never loaded. A strictly monotonic sequence id (an LSN, a bigserial the loader reads after commit) is not this class. **Severity:** high for `>` with no lookback, medium for `>=` with no lookback on an event-time column. **Proof:** V542 (a row with the watermark's timestamp inserted after the run is present after the next) and V541 (a row older than the watermark, inside the lookback, is present).

### 2. No merge key, a key that is not the grain, or a nullable key

```
BAD:   {{ config(materialized='incremental') }}                          -- adapter default, no unique_key
       {{ config(materialized='incremental', incremental_strategy='append', unique_key='id') }}   -- append ignores the key
       INSERT INTO mart.orders SELECT * FROM raw.orders WHERE day = %s    -- a retry inserts the day again
       df.to_sql('orders_copy', conn, if_exists='append')
GOOD:  unique_key='order_id' + a not_null and a unique test on order_id · ON CONFLICT (order_id) DO UPDATE
       DELETE FROM mart.orders WHERE day = %s; INSERT … (one transaction) · insert_overwrite on the partition
```
**Read the code:** What is the grain, and is the key exactly it (a composite key for a line-level table)? Does the source update rows in place (`updated_at`, a CDC op column) — then `append` duplicates (precedent § 1 holds only for immutable events deduplicated downstream)? Can any key column be NULL (no `not_null` test, an outer join upstream)? A NULL never matches in a merge. Is a declared primary key relied on outside Postgres (metadata only)? **Finding when** re-processing the same batch, a retry, or the lookback window inserts a row twice. **Proof:** V540 — run the same batch twice on a scratch target: `count(*)` and a row checksum unchanged; a NULL-key row yields no duplicate.

### 3. Load-time clock, wrong-zone watermark, or a watermark advanced too early

```
BAD:   where _loaded_at > (select max(_loaded_at) from {{ this }})        -- the warehouse's clock, not the event's
       state.set('last_synced_at', now()); rows = read('… where updated_at > %s', last)   -- advanced before the write
GOOD:  filter on the event/update time with a lookback; advance the watermark to max(read rows) after the commit
```
**Read the code:** Which clock wrote the filter column — the source system, the loader, or the warehouse? A load-time column (`_loaded_at`, `_fivetran_synced`, `_airbyte_extracted_at`) skips rows the extractor delivers out of order. Is the watermark read from the target and compared with a source stamp written by another clock (skew)? Is one side `timestamp_ntz` / `without time zone` and the other UTC? Is the watermark advanced before the sink statement commits, so a crash between the two loses the window? Does a wall-clock function (`now()`, `current_date`) bound the window, so a replay selects a different set? **Finding when** a row the source committed is skipped because of the clock, the zone or the ordering. **Proof:** V541 with the row's two stamps skewed; and a fault injected between the state write and the sink — the rerun loads the window.

### 4. Source deletes never reach the target

```
BAD:   {% snapshot customers_snapshot %} {{ config(unique_key='id', strategy='timestamp', updated_at='updated_at') }}
       MERGE INTO t USING s ON t.id = s.id WHEN MATCHED THEN UPDATE … WHEN NOT MATCHED THEN INSERT …   -- no delete
GOOD:  hard_deletes='invalidate' (or 'new_record'); staging filters _fivetran_deleted;
       WHEN MATCHED AND s.op = 'd' THEN DELETE
```
**Read the code:** Does the source hard-delete (an erasure job, an admin delete, a retention purge)? Does the extractor deliver deletes (a CDC op, a soft-delete column, a full snapshot compare)? Does every downstream model filter or apply them? On dbt ≥ 1.9 is `hard_deletes` set; on ≤ 1.8, `invalidate_hard_deletes`? A source that never deletes is precedent § 16. **Finding when** a row deleted at the source stays current in a consumed table. Personal data kept after erasure is also `pii-copy-scan` §2's row — cite it there. **Proof:** V543 — delete a source row, run: absent or flagged (`dbt_valid_to` set) in the target.

### 5. Non-deterministic dedup

```
BAD:   row_number() over (partition by event_id order by occurred_at)          -- ties: a different winner per run
       df.dropDuplicates(["order_id"])                                         -- keeps an arbitrary row
GOOD:  row_number() over (partition by event_id order by occurred_at desc, _ingested_seq desc, payload_hash)
```
**Read the code:** Can two rows tie on the order keys? Do tied rows differ in any other column? `dropDuplicates` on full-row duplicates is deterministic in effect (precedent § 15). **Finding when** a tie on the order columns between rows that differ elsewhere is possible. **Proof:** V544 — shuffle the input order (seeded) ×10: the output checksum is identical.

### 6. Schema drift silently dropped, or fatal late

**Read the code:** Is the effective `on_schema_change` `ignore` (default) on an incremental whose source gains columns (a SaaS extractor, an event payload)? Is it `sync_all_columns` on a large or partitioned table (columns dropped, types changed without a failure)? Does an enforced contract require `append_new_columns` or `fail`? On Spark, does a landing path hold several schema versions read without `mergeSchema`? `view` and `table` models rebuild each run (precedent § 5). **Finding when** an added source column never reaches a consumed table and nothing fails, or a removed column fails the nightly with no migration path. **Proof:** V545 — add a source column, run incrementally: the run fails or carries it per the declared policy.

### 7. An overwrite wipes more than the run's partitions

```
BAD:   df.write.mode("overwrite").partitionBy("day").parquet(path)          -- STATIC: every partition deleted
       TRUNCATE TABLE mart.orders; INSERT INTO mart.orders SELECT …         -- readers see an empty table between
GOOD:  spark.sql.sources.partitionOverwriteMode=dynamic · Delta .option("replaceWhere", "day = '…'") · swap a staged table
```
**Read the code:** Is `partitionOverwriteMode` set to `dynamic` in the session, the job conf or the write options? Is the table Delta with `replaceWhere`, or Hive serde (always dynamic — precedent § 28)? For dbt `insert_overwrite`, which scope does the adapter replace with and without `partition_by` / `partitions`? Do readers query during a truncate-and-reload? **Finding when** one run's write deletes partitions it did not produce, or exposes an empty table to readers. **Proof:** V546 — write two partitions, overwrite one: the other's checksum is unchanged.

### 8. Backfill re-appends history, or runs in place beside the schedule

**Read the code:** For each 0d entry point, what is the target's strategy? A range re-run into an `append` target double-counts; `--full-refresh` on an incremental over a retention-limited source rebuilds without the history (is `full_refresh: false` pinned — precedent § 9)? Does the backfill write the live table while the schedule runs (`max_active_runs`, no pause)? **Finding when** re-running a loaded range changes counts or loses history. **Proof:** V550 — backfill the same range twice: identical aggregates; V549 — the run's output depends only on its interval.

### 9. Microbatch misconfiguration

**Read the code:** Are `event_time`, `begin` and `batch_size` set? Does every `ref()` parent declare `event_time` (else it is read in full for every batch)? On Postgres (merge) is there a `unique_key`; on BigQuery/Spark/Databricks (insert-overwrite) a `partition_by`? Is `lookback` enough for the source's late arrival? Microbatch models need no `is_incremental()` filter (precedent § 7). **Finding when** a missing key or parent `event_time` breaks the backfill, re-scans the parent, or duplicates rows. **Proof:** V541 over two batches with a late row; `dbt run --event-time-start/--event-time-end` twice → identical counts.

### 10. CDC landing loses, keeps or corrupts rows

```
BAD:   "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState", "transforms.unwrap.drop.tombstones": "true",
       "transforms.unwrap.delete.handling.mode": "drop"          -- deletes never reach the sink
       JDBC sink "insert.mode": "insert" over a change topic       -- updates and snapshot restarts append duplicates
GOOD:  rewrite deletes to a flag (or keep tombstones for a compacted topic) + an upsert sink keyed by PK + source LSN
```
**Read the code:** Which Debezium version (the image tag — 3.2 renamed the delete options)? Are deletes dropped, rewritten to a flag, or delivered as tombstones the sink applies? Does every table in `table.include.list` have a primary key or `REPLICA IDENTITY FULL` (grep 10b and the migrations)? Are TOASTed columns handled (`unavailable.value.placeholder` would overwrite the real value)? Does the sink upsert by key with source ordering, so a restarted snapshot does not append the table again? `tombstones.on.delete=false` with a non-compacted topic whose sink consumes `op=d` is precedent § 18. **Finding when** a source delete, update or snapshot restart leaves the landing table wrong. **Proof:** V543 (delete → absent or flagged; connector restart mid-snapshot → no duplicate key) and V540.

## Output

```
incremental-load-scan — lanes: dbt 1.9.4 (requirements.txt) + dbt-postgres; airflow 3.0.2; pyspark 3.5.1; debezium (cdc/*.json); nest @Cron
Graph: $OUT/graph — model-graph exit 0 · 5 models · 2 incremental · 1 snapshot · 6 IN candidates

Findings: 2 · Unconfirmed: 2

1. analytics/models/marts/fct_pageviews.sql:7                    [report-with-fix]   high
   §1 IN-1 + §3 IN-3 — `_loaded_at > (select max(_loaded_at) from {{ this }})`: a load-time column, strict, no lookback;
   effective unique_key none, strategy adapter-default (fct_pageviews.sql:1 config()). V542 on duckdb: the tie row is missing.
   Fix: filter on occurred_at >= max(occurred_at) - interval '2 days', unique_key='event_id'.
2. analytics/snapshots/orders_snapshot.sql:1                      [report-with-fix]   high
   §4 IN-4 — hard_deletes `ignore` (default, dbt 1.9.4); orders are hard-deleted by the erasure job (apps/…/erase.ts:40).
   V543: deleted order still has dbt_valid_to null. Fix: hard_deletes='invalidate'.
3. etl/loader.py:4                                                [report-flagged]    medium
   §3 IN-3 — last_synced_at advanced before the read and the append. Unproven link: the scheduler's retry on failure.
   Settling: V541 with a fault after line 4.
4. cdc/orders-source.json:4                                       [report-flagged]    high
   §10 IN-10 — delete.handling.mode drop + drop.tombstones true: deletes never reach the lake. Unproven link: the
   Debezium version (no image tag in the repo). Settling: V543 on a scratch connector.

Routed: 1 → distributed-systems dual-write-scan §6 (outbox relay cursor) · 1 → derived-data-scan §1 (rollup counter)
Verification: 14 candidates → 2 findings · 2 unconfirmed · 3 hardening · 7 refuted (self-verified; precedents § 2, § 5, § 15)

Class coverage:
  §1 watermark          checked (G 1 + 1b 3 → 1 finding; 2 refuted: >= with lookback and a merge)
  §2 merge key          checked (G 2 + 2b 2 + 2c 3 → 0 findings; the DAG deletes the day first)
  §3 load clock         checked (G 1 + 3b 2 → 1 finding, 1 unconfirmed)
  §4 deletes            checked (G 1 + 4b 0 → 1 finding)
  §5 dedup              checked (2 → 0 findings; event_id ties carry identical payloads, read)
  §6 schema drift       checked (G 1 → hardening: the source is a frozen export)
  §7 overwrite scope    checked (7a 1 → 0: the path is written once per day by one job — hardening)
  §8 backfill           checked (0d 1 → 0)
  §9 microbatch         N/A (no microbatch model)
  §10 CDC landing       checked (10a 4 lines → 1 unconfirmed)
```

`[report-with-fix]`: the oracle failed on a scratch target (duckdb, a container, a rolled-back transaction) or the fact is two-ended with the effective value's source quoted, and the fix is local to the model config, the loader or the connector. `[report-flagged]`: one link is unproven (the source's delete behaviour, the arrival window, the connector version, the scheduler's retry); the row names it and the settling oracle. The coverage block lists **all ten** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (model-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 1 an append-only immutable event table with no key (flips back when the source has `updated_at` or a CDC op); § 2 strict `>` + lookback + merge; § 5 `on_schema_change` on `view`/`table`; § 7 microbatch with no `is_incremental()`; § 8 `insert_overwrite` with no `unique_key`; § 9 `full_refresh: false` on huge incrementals.
- § 15 `dropDuplicates` on full-row duplicates; § 16 `hard_deletes: ignore` on a source that never deletes; § 18 `tombstones.on.delete=false` on a non-compacted topic whose sink applies `op=d`; § 28 Delta `replaceWhere` / Hive serde overwrite.

## When to run

- On any diff that touches a dbt model config or `is_incremental()` block, `dbt_project.yml`, a snapshot, a loader or sync job, a Spark write, a connector config, a backfill script — `/audit-data-quality`'s load signal.
- On every whole-repo `/audit-data-quality`, reporting all ten §s; before `/backfill-plan` (its loader gate reads §2, §7 and §8).

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the effective config with sources, the `file:line` and the source row — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@warehouse-modeler` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Never run a load, a `dbt run/build`, a backfill or a connector against a shared or production target.** Oracles run on duckdb (a profile written in `$OUT`, `DO_NOT_TRACK=1`, `DBT_SEND_ANONYMOUS_USAGE_STATS=False`, `DBT_ENGINE_SEND_ANONYMOUS_USAGE_STATS=false`, `--profiles-dir "$OUT"`), a throwaway container, or a rolled-back transaction; a probe that cannot be isolated is `NOT-RUN`.
- **This skill writes nothing into the audited repo**: no model, test, config or fixture. `git status --porcelain` and `find <root> -newer "$OUT/graph.txt"` are empty at the end; a fix is `/data-fix`'s.
- **Halt before §1–§10 on a dbt project when model-graph is blocked** (exit 2): every dbt row prints `blocked`, never `checked`. Exit 4 prints the dbt lane `N/A (no dbt project)`.
- **No `[report-with-fix]` without the V-oracle failing on a scratch target**, or a two-ended static fact whose effective value and source are quoted. "Incremental without a key" is a candidate until the source's mutation pattern is read.
- **No fix may hide the class:** never add `distinct` to mask duplicates, never widen a lookback without a merge, never switch to a full refresh of an unrecoverable history.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the loads look idempotent"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill and folds its coverage block into the class ledger; `@warehouse-modeler` judges IN rows; `/data-fix` closes them with the failing-first oracle; `/backfill-plan` reads §2/§7/§8 for its loader gate.
- This pack: `orchestration-scan` (the retry and the schedule around a load), `data-test-scan` (the key's `not_null`/`unique` tests), `derived-data-scan` (in-app rollups), `pii-copy-scan` §2 (erasure in snapshots), `warehouse-scan-audit` §2 (merge cost), `lineage-trace` (it reads the edges `scripts/model-graph.py` here writes).
- distributed-systems `messaging-scan` / `dual-write-scan`, backend `job-lifecycle-scan`, database `migration-safety` (PK-less tables), when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): dbt docs — incremental models and strategies (updated 2026-09-16), microbatch, snapshots, constraints, full_refresh, usage stats and the `DBT_ENGINE_` prefix; Spark 4.2.0 configuration (`partitionOverwriteMode`, `mergeSchema`); Debezium Postgres connector 3.7 docs and the 3.2.0.Final release notes (2025-07-09); dbt-duckdb 1.11.0 / DuckDB 1.5.6 (MERGE INTO since 1.4.0) as the offline oracle. Class ids DE-A-1…35 and DE-B-60…64 as catalogued there. Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
