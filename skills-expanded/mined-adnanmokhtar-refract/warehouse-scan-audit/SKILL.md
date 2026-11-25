---
name: warehouse-scan-audit
description: "Pipeline SQL that scans more than it reads: unpruned partitions, unbounded merges, full rebuilds, view chains; offline first."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: warehouse-scan-audit

## Premise

Warehouse spend is bytes scanned or slot-seconds consumed, and both come from specific lines of pipeline SQL: a reader that wraps the partition column in a function (`where date(created_at) = …`) so nothing prunes; a partitioned table with no `require_partition_filter`, so any unfiltered query reads every partition; an incremental `merge` with no bound on the **target** side, so each run scans the whole destination to find matches (dbt BigQuery and Snowflake configs, `incremental_predicates`, accessed 2026-10-19); a `table` materialization rebuilding an append-mostly fact every night; a chain of views re-executed for every reference; `SELECT *` on a wide columnar table. Each is visible in the repository **before** anyone reads a bill — so this skill's static lane always runs, offline, on any checkout. Measured cost needs the platform's own numbers: the free dry-run estimate (BigQuery `--dry_run`, Snowflake `EXPLAIN`) or recorded job history — never a figure reasoned from the SQL.

This skill owns research ids CO-1…CO-5 (`research-data-engineering.md` § 1.9), shipped as `DE-CO-<n>`: **the pipeline SQL that makes a warehouse scan more than it needs.** Budgets, `maximum_bytes_billed` policies, auto-suspend, warehouse sizing and who pays are finops' (`/cost-guardrails`, `/cost-model`); this skill reports the SQL and hands the money total over.

**Every finding cites the model or query `<file:line>` + the table's partitioning and clustering as configured (with the source of each value) + the predicate or materialization that defeats it + bytes before and after when a dry run or history is available (labelled measured), else the static fact labelled `estimated: not measured` + the fix in the project's own SQL or config.** A grep hit is a candidate. "The warehouse is expensive" is never a finding; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) (measurement claims); the oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V568.

## The rule

A candidate is a finding when all four hold:

1. **The SQL runs on a schedule against a billed engine.** A dbt job, a DAG task, a scheduled query, a BI extract on a per-byte or per-slot warehouse. Row-store engines (Postgres, MySQL) are database `query-shape-scan`'s; `SELECT *` there is precedent § 23.
2. **The table's layout is read.** `partition_by`, `cluster_by`, `require_partition_filter`, `partitions`, the table's growth class (append-only events vs a small dimension). A small table is precedent § 35.
3. **No existing control, across files.** A sargable predicate on the partition column, `incremental_predicates` or a target-side `where` in the merge, `insert_overwrite` with `partitions`, an incremental instead of a rebuild, a materialized intermediate in the chain, an explicit column list.
4. **The oracle fired, or the fact is two-ended.** V568 — dry-run bytes before and after the fix (or recorded job bytes for the model) — or the static fact cites the layout and the predicate that defeats it, labelled `estimated`.

## Boundaries

- **Budgets, quotas, `maximum_bytes_billed` as policy, auto-suspend, warehouse size, reservations, chargeback** → finops (when installed); without it the money row prints `→ finops (not installed)` and only bytes are reported. **The SQL of an OLTP query** (indexes, plans) → database. **Whether the result is right** → `grain-probe`, `data-test-scan`.
- **The merge key's correctness** → `incremental-load-scan` §2; **the merge's cost** is §2 here. **A view chain's lineage** → `lineage-trace`; its re-execution cost is §4 here. **`SELECT *` as a contract hazard** → `contract-diff` §3; its bytes are §4 here.

## Adapt to the codebase — the lanes

| Lane | Always runs? | Reads | Needs |
|---|---|---|---|
| **Static** | yes, offline | `model-graph.py` configs (`partition_by`, `cluster_by`, `require_partition_filter`, `incremental_predicates`, materialization) from `graph.json`; reader predicates in model SQL; schedules (`--full-refresh`, cron frequency); view-chain depth from `edges.tsv` | a checkout |
| **Recorded history** | when a file is supplied or committed | an exported `INFORMATION_SCHEMA.JOBS` / `QUERY_HISTORY` CSV: bytes per dbt node (the query comment's `node_id`) or per query hash | the CSV only — never fetched by this skill |
| **Dry run** | only with the user's word and their credentials | `bq query --use_legacy_sql=false --dry_run '<compiled sql>'` (free; prints bytes); Snowflake `EXPLAIN`; Databricks `EXPLAIN COST` | a non-production project or the user's go; telemetry and default profiles off |
| **Live history** | only with the user's word | the same history views queried read-only, bounded by date and `LIMIT` | the user's go, a read-only role |

Per engine: BigQuery (bytes billed; `require_partition_filter`, clustering, `partition_expiration_days`), Snowflake (micro-partition pruning, clustering keys, warehouse-seconds), Databricks/Spark (file pruning, Z-order/liquid clustering), Redshift (sort/dist keys), ClickHouse (primary-key order → database pack). The pricing model decides which fix matters: per-byte rewards pruning; capacity pricing rewards slot time and contention — **halt and ask** when it is unknown.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; G builds the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; path globs may stand together but are never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. **No warehouse is contacted by this block.** Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the dbt project and the DAG/job roots
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-co.XXXXXX")}"; mkdir -p "$OUT/none"; HISTORY="${HISTORY:-}"   # HISTORY=<exported jobs CSV> for §5
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# G  the dbt graph (incremental-load-scan/scripts/model-graph.py): exit 0 built · 4 no dbt project (static dbt lane N/A) · 2 blocked
MG=.claude/skills/incremental-load-scan/scripts/model-graph.py
if command -v python3 >/dev/null 2>&1 && [ -f "$MG" ]; then python3 -I -B "$MG" "${ROOTS[@]}" --out="$OUT/graph" --class=CO > "$OUT/graph.txt" 2> "$OUT/graph.err"; echo "G model-graph exit $? → $OUT/graph"; sed -n '2,4p' "$OUT/graph.txt"; grep '^\[' "$OUT/graph.txt"
else echo 'G NOT-RUN (python3 or model-graph.py absent): §1–§4 are read by hand from 1a–4b and print Live, unreviewed'; fi
# 0 LAYOUT — partitioned / clustered models with their effective require_partition_filter, and view-chain depth, from graph.json (stdlib only)
h 0; [ -s "$OUT/graph/graph.json" ] && python3 -I - "$OUT/graph/graph.json" <<'PY'
import json, sys
g = json.load(open(sys.argv[1], encoding='utf-8')); nodes = g['nodes']
cfg = lambda n, k: ((nodes.get(n) or {}).get('config', {}).get(k) or {}).get('value')
par = {}
for c, p, kind, w in g['edges']:
    par.setdefault(c, []).append(p)
for n in sorted(nodes):
    pb, cb, rpf = cfg(n, 'partition_by'), cfg(n, 'cluster_by'), cfg(n, 'require_partition_filter')
    if pb or cb:
        print('layout %s  partition_by=%s cluster_by=%s require_partition_filter=%s  (%s)' % (n, json.dumps(pb), json.dumps(cb), rpf, nodes[n].get('path')))
def depth(n, seen=()):
    if n in seen or str(cfg(n, 'materialized') or 'view').lower() != 'view' or not n.startswith('model.'):
        return 0
    return 1 + max([depth(p, seen + (n,)) for p in par.get(n, [])] or [0])
for n in sorted(nodes):
    d = depth(n)
    if d >= 3:
        print('view-chain %s depth=%d (%s)' % (n, d, nodes[n].get('path')))
PY
# 1 CO-1 pruning — 1a function-wrapped date/partition columns in model and scheduled SQL · 1b partition_by declared with no require_partition_filter anywhere
h 1a; rg -n --pcre2 '(?i)\b(?:where|and|on)\b[^;\n]*\b(?:date|cast|to_date|date_trunc|timestamp_trunc|datetime_trunc|extract|format_date|format_timestamp|to_char|trunc)\s*\(\s*(?:\w+\.)?\w*(?:_date|_at|_ts|_time|day|event_time|partition\w*)\b' -g '**/models/**/*.sql' -g '**/{dags,etl,jobs,pipelines,queries,scheduled_queries}/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 1a ${PIPESTATUS[0]}
h 1b; rg -l --pcre2 '\bpartition_by\s*[=:]' -g '**/models/**' -g '**/dbt_project.yml' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'require_partition_filter'
# 2 CO-2 unbounded merges — G rows (merge into a partitioned target with no incremental_predicates); 2a hand MERGE statements with no target-side bound
h 2a; rg -n -U --pcre2 '(?i)\bmerge\s+into\s+[\w."`]+(?:\s+(?:as\s+)?(\w+))?\s+using\b[\s\S]{0,600}?\bon\s+(?![^;]{0,400}?\b(?:\1|dbt_internal_dest|target|t|tgt)\.\w*(?:_date|_at|day|partition\w*)\s*(?:>=|>|between|in)\b)[^;\n]*' -g '**/models/**/*.sql' -g '**/{dags,etl,jobs,pipelines,spark}/**' -g '**/macros/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -30; ck 2a ${PIPESTATUS[0]}
# 3 CO-3 full rebuilds — G rows (table-materialized facts); 3a --full-refresh in schedules · 3b schedules tighter than hourly that run dbt (read the freshness need)
h 3a; rg -n --pcre2 '\bdbt\s+(?:run|build)\b[^\n]*--full-refresh' -g '**/.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci.yml' -g '**/dags/**' -g '**/Makefile' -g '**/*.sh' -g '**/crontab*' --hidden "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3a ${PIPESTATUS[0]}
h 3b; rg -n --pcre2 '(?:schedule(?:_interval)?\s*=\s*|cron\s*:\s*|-\s*cron\s*:\s*)["\x27]\*/(?:[1-9]|[1-5]\d)\s' -g '**/dags/**' -g '**/.github/workflows/*.{yml,yaml}' --hidden "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3b ${PIPESTATUS[0]}
# 4 CO-4 amplification — view chains (0) and SELECT * on models of a columnar adapter (G header names the adapter)
h 4; rg -n --pcre2 '(?i)^\s*select\s+(?:distinct\s+)?\*\s*$|\bselect\s+(?:distinct\s+)?\*\s+from\s+(?!final\b|renamed\b)' -g '**/models/marts/**' -g '**/models/intermediate/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4 ${PIPESTATUS[0]}
# 5 CO-5 measured top cost — the recorded-history lane (a supplied or committed CSV); live history and dry runs are never run by this block
h 5; HF=("$HISTORY"); [ -n "$HISTORY" ] || { HF=(); while IFS= read -r f; do HF+=("$f"); done < <(rg --files -g '**/*{jobs,JOBS,query_history,QUERY_HISTORY}*.csv' "${X[@]}" "${ROOTS[@]}"); }
[ ${#HF[@]} -gt 0 ] && python3 -I - "${HF[@]}" <<'PY' || echo '5 N/A (no recorded history; live history and dry runs need the user'"'"'s word)'
import csv, re, sys, collections
tot = collections.Counter(); runs = collections.Counter()
for f in sys.argv[1:]:
    for r in csv.DictReader(open(f, encoding='utf-8', newline='')):
        b = next((r[k] for k in r if k and k.lower() in ('total_bytes_billed', 'total_bytes_processed', 'bytes_scanned')), '0') or '0'
        q = next((r[k] for k in r if k and k.lower() in ('query', 'query_text')), '') or ''
        m = re.search(r'"node_id"\s*:\s*"([^"]+)"', q)
        key = m.group(1) if m else (r.get('query_hash') or q[:60])
        tot[key] += int(float(b)); runs[key] += 1
for k, v in tot.most_common(10):
    print('history %-40s %8.2f GiB over %d runs (measured: recorded file)' % (k, v / 2**30, runs[k]))
PY
```

0 prints every partitioned or clustered model with its effective `require_partition_filter` and every view chain of depth ≥ 3. 1a's lines are candidates only when the wrapped column is the table's partition column (0's `partition_by.field`). 2a lists hand-written `MERGE` statements whose `ON` clause carries no range on a target date or partition column — read the statement; the G row covers dbt merges.

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s; no warehouse contacted): 0 3 partitioned models (one without `require_partition_filter`) and 2 view-chain rows (depth 4 at `rpt_daily_kpis`, 3 at its parent — one chain); 1a 1 (`date(impression_ts)` on the partition column); 1b 1; G 1 CO-2 (the merge with no `incremental_predicates`) and 1 CO-3; 2a 2 hand MERGEs (the impressions merge with no target bound; the orders merge on a small unpartitioned table, refuted); 3a 2 `--full-refresh` lines (the nightly schedule; a Makefile runbook that `incremental-load-scan` §8 owns); 4 3; 5 the recorded `INFORMATION_SCHEMA.JOBS` CSV ranks the impressions merge (4 TiB) and the ad report (1 TiB) — measured: recorded file.
- **Real repo, read-only** (the NestJS monorepo): G exit 4; 0–4 0 — no warehouse (a Postgres row store: database `query-shape-scan` owns its SQL); 5 `N/A (no recorded history)`.
- **Every lane is fixture-measured only** (eval O-2); the dry-run lane was never run (no credentials, by design).

## The 3,000-hit path

1. **Build the layout once** (0): every partitioned and clustered model with its effective filter requirement. Every 1a hit is joined to it — a wrapped column that is not the partition column is not CO-1.
2. **Group by table**: one fact read by forty models with `date(ts)` is one decision — fix the readers, or add `require_partition_filter` and let the build fail the unfiltered ones.
3. **Rank by bytes when any number exists** (5's recorded history, or the user's dry runs); otherwise by the table's growth class.
4. **One dry-run pass at scale, only with the user's word**: compile once (`dbt compile` on a profile pointing at the user's non-production project), dry-run each candidate's compiled SQL before and after the fix; never execute.
5. **Ledger the rest** as `Live, unreviewed (k tables / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | CO-1 partitioned table read without a pruning predicate; function-wrapped partition column; no `require_partition_filter` on a large table | medium | V568 |
| 2 | CO-2 merge with no `incremental_predicates` / target-side bound | medium | V568 |
| 3 | CO-3 full rebuild of an append-mostly fact; schedule tighter than the freshness need | medium | V568 |
| 4 | CO-4 view chains re-executed per reference; `SELECT *` on wide columnar tables | low | V568 |
| 5 | CO-5 measured top-cost entries (history lane only) | — (ranked, never graded alone) | V568 |

### 1. Pruning defeated

```
BAD:   where date(event_ts) = current_date - 1          -- event_ts is the partition column: every partition scanned
       {{ config(partition_by={'field': 'event_ts', 'data_type': 'timestamp'}) }}   -- no require_partition_filter
GOOD:  where event_ts >= timestamp(current_date - 1) and event_ts < timestamp(current_date)
       require_partition_filter=true  (unfiltered readers now fail at plan time)
```
**Read the code:** Is the wrapped column the partition column (0)? Does the engine prune through the function (BigQuery prunes on `DATE(ts)` for a `DATE`-partitioned column in some forms — read the dry run, never assume)? Is the table large and growing (an event fact) or small (precedent § 35)? **Finding when** a scheduled reader of a large partitioned table scans every partition. **Proof:** V568 — dry-run bytes before and after; `require_partition_filter=true` makes the unfiltered reader fail.

### 2. Merge with no target bound

**Read the code:** Is the target partitioned and large? Does the merge carry `incremental_predicates` (dbt) or a target-side range in `ON` (hand `MERGE`), so only recent target partitions are scanned for matches? Would `insert_overwrite` with `partitions` fit the grain? Is the destination small (no finding)? **Finding when** every run scans the whole destination to merge a day of rows. **Proof:** V568 on the compiled merge.

### 3. Full rebuild of an append-mostly fact

**Read the code:** Is the `table` fact append-mostly (events, ledger lines) and rebuilt nightly? Is `--full-refresh` in a schedule rather than a manual runbook? Is the schedule tighter than anyone reads the table (a five-minute dbt run for a daily dashboard)? A documented weekly compaction is not this class. **Finding when** cost grows with history for no freshness gain. **Proof:** V568 — bytes of the rebuild vs the incremental equivalent.

### 4. Amplification

**Read the code:** Is a chain of three or more views read by several consumers (each reference re-executes the chain)? Would materializing the middle link pay for itself? Is `SELECT *` on a wide columnar table feeding a model that uses a few columns (row stores and narrow views are precedent § 23)? **Finding when** the same scan repeats per reference, or unused columns are read every run. **Proof:** V568.

### 5. Measured top cost

Only from a recorded history file (5) or, with the user's word and a read-only role, the live history views (bounded by date, `LIMIT 20`). The top entries rank the §1–§4 rows; a top entry with no §1–§4 cause is reported as `measured, cause not found statically` for the user to read — never as a finding with an invented cause. Money totals go to finops.

## Output

```
warehouse-scan-audit — lanes: static (dbt 1.9.4, adapter bigquery from profiles.yml); history: warehouse/jobs_2026-10.csv (recorded);
                       dry run: NOT-RUN (no credentials — offline mode); pricing: on-demand per byte (profiles.yml comment, asked)
Layout: 2 partitioned models (1 without require_partition_filter) · 1 view chain depth 4

Findings: 1 · Unconfirmed: 2

1. analytics/models/marts/fct_sessions_daily.sql:9                  [report-flagged]    medium
   §1 CO-1 — `where date(event_ts) = …` on fct_pageviews (partition_by event_ts, models/marts/fct_pageviews.sql:2), no
   require_partition_filter. History: fct_sessions_daily 412 GiB over 30 runs (measured: recorded file).
   Settling: V568 dry run before/after (needs the user's project). Fix: a range on event_ts; require_partition_filter=true.
2. analytics/models/marts/fct_pageviews.sql:2                        [report-with-fix]   medium
   §2 CO-2 — merge into the partitioned fct_pageviews with no incremental_predicates (G; effective config from the file).
   Two-ended: the partitioned target and the unbounded merge. Fix: incremental_predicates on event_ts ≥ 3 days back.
3. .github/workflows/nightly-build.yml:14                           [report-flagged]    medium
   §3 CO-3 — `dbt build --full-refresh` nightly on fct_pageviews (append-only). Unproven link: why (a runbook may need it).

Routed: money total and budget → finops /cost-guardrails (not installed: bytes only)
Verification: 9 candidates → 1 finding · 2 unconfirmed · 2 hardening · 4 refuted (self-verified; precedents § 23, § 35)

Class coverage:
  §1 pruning            checked (0 2 · 1a 3 · 1b 1 → 1 unconfirmed; 2 wrapped columns not the partition column)
  §2 merge bound        checked (G 1 + 2a 0 → 1 finding)
  §3 full rebuild       checked (G 1 + 3a 1 + 3b 0 → 1 unconfirmed)
  §4 amplification      checked (0 1 chain · 4 2 → hardening: the chain has one reader)
  §5 measured top cost  checked (recorded file: 10 nodes; dry run and live history NOT-RUN)
```

`[report-with-fix]`: the dry-run oracle showed the bytes drop on the user's non-production project, or the fact is two-ended (the layout and the defeating SQL) and the fix is local to the model, the config or the schedule. `[report-flagged]`: the bytes are unmeasured or the reason for a rebuild is unread; the row names the settling dry run. Every number is labelled **measured** (with its source file or dry run) or omitted. The coverage block lists **all five** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `NOT-RUN (<reason>)`, `blocked (model-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md), [`precedents/performance.md`](../../../../snippets/precedents/performance.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 35 no `require_partition_filter` on a small table; § 23 `SELECT *` on a row store or a narrow view, or as the last CTE statement; a documented weekly compaction; a capacity-priced warehouse where the marginal byte is free (optimise slot time, say so — a "$ saved" figure would be fiction).

## When to run

- On any diff that touches a model's partitioning, clustering or materialization, a reader of a partitioned table, a merge, or a dbt schedule — `/audit-data-quality`'s cost signal; when the bill jumps (with a recorded history file); before materializing something expensive; from `/backfill-plan` for its per-chunk estimate (it returns `UNKNOWN` rather than a guess without history or a dry run).
- On every whole-repo `/audit-data-quality`, reporting all five §s.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the layout, the SQL and any measured bytes with their sources — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@warehouse-modeler` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`.
- **Cost guard: nothing scans a warehouse without a dry run and the user's word.** This skill never executes a query on a billed engine. A dry run (`--dry_run`, `EXPLAIN`) needs the user's project or account named in this session, `CLOUDSDK_CORE_DISABLE_PROMPTS=1`, no default profile assumed; a live history query additionally needs a read-only role and is bounded by date and `LIMIT`. Without credentials the run is **offline** and every byte figure is `NOT-RUN`.
- **Pricing model unknown → ask** before recommending: per-byte, per-slot and flat-rate capacity reward different fixes. **Every number labelled measured or omitted** — never derived from reading the SQL ([`precedents/performance.md`](../../../../snippets/precedents/performance.md) on measurement claims).
- **This skill writes nothing into the audited repo**; `find <root> -newer "$OUT/graph.txt"` is empty at the end; a fix is `/data-fix`'s; a budget or a guardrail is finops'.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the warehouse is expensive"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill; `/backfill-plan` reads it for per-chunk bytes; `@warehouse-modeler` judges CO rows; `/data-fix` closes them with V568 dry runs.
- This pack: `incremental-load-scan` §2 (the merge key), `lineage-trace` (the chain's edges), `contract-diff` §3 (`SELECT *` as a contract hazard).
- finops `/cost-guardrails` and `/cost-model`, database `query-shape-scan` (row-store SQL), when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): dbt BigQuery and Snowflake configs (`partition_by`, `require_partition_filter`, `incremental_predicates`, `partitions`); BigQuery dry run (CC BY 4.0) and partitioned-table pruning; Snowflake warehouse considerations; dbt incremental strategies (DE-B-40…50). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
