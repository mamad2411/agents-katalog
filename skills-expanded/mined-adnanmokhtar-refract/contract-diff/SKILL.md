---
name: contract-diff
description: "Tables others read: unenforced contracts, unversioned breaks, SELECT *, migrations under readers, timestamp mixing."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: contract-diff

## Premise

A table someone else reads is an interface. It breaks loudly when a column is dropped, renamed, narrowed or made non-null under a reader, and silently when its **meaning** moves: `amount` goes from cents to units, `status` gains a member a downstream `CASE` sends to `ELSE`, a column starts arriving NULL, a naive timestamp starts holding local time. Most "constraints" in a warehouse are documentation (dbt constraints docs, accessed 2026-10-19): only Postgres enforces every constraint type; Snowflake, BigQuery, Redshift and Databricks enforce `not_null` (Databricks also `check`) and keep primary key, unique and foreign key as metadata — so a contract is a **shape** gate, never a uniqueness proof. The most common break is not in the warehouse at all: an application migration drops a column that a dbt source, a CDC include list or an export mapper still reads, and the nightly fails — or loads NULL.

This skill owns research ids SC-1…SC-6 (`research-data-engineering.md` § 1.4), shipped as `DE-SC-<n>`: **whether a table other people read changes shape or meaning under them without a contract, a version or a notice.** It classifies *whether* a change breaks; `lineage-trace` names *who* it breaks; `grain-probe` proves the key after the fact.

**Every finding cites the published model or table `<file:line>` + its readers (exposure, `access: public`, another project's `source()`, an export, a CDC sink) + the change (the removed or narrowed column, the migration statement, the cast) with both sides read + the effective contract config and where it came from + the oracle that would settle it + the fix (a contract, a version with `deprecation_date`, an explicit column list, an expand/contract migration).** A grep hit is a candidate. "The contracts look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V552, V553, V557 and V558.

## The rule

A candidate is a finding when all four hold:

1. **The table has readers outside its author.** An exposure, `access: public`, a model in another dbt project reading it through `source()`, a BI tool, an export or reverse-ETL sync, a CDC sink. A pre-release model with no reader fails here.
2. **Both sides are read.** For a diff: the old and the new YAML/SQL (`git diff` against the base). For a migration: the DDL statement and each reader naming the table.column. For a semantic break: two data snapshots. A single observation is an inventory, not a diff.
3. **No existing control, across files.** `contract: {enforced: true}` on the adapter that enforces what it declares, a new `versions:` entry with `latest_version` and a `deprecation_date` on the old one, an explicit select list, an expand/contract migration sequence with the reader moved first, a `datacontract` or `dbt build --select state:modified+` gate in CI.
4. **The oracle fired, or the fact is two-ended.** V557 (drop or rename a contracted column → `dbt build` or `datacontract breaking` fails) or V558 (the migration applied to a scratch DB → every reader fails) ran; or the static fact cites the change and the reader that consumes it.

## Boundaries

- **Message and event schemas** (Avro, Protobuf, JSON Schema, registry compatibility, `buf breaking`) → distributed-systems `event-contract-scan` §1–§5 (when installed); this skill cites them when a warehouse landing table is the consumer. Precedent § 36 is listed for corroboration only.
- **The application's own N-1 compatibility** (an API process reading a column a migration drops in the same deploy) → database `migration-safety` §4; §4 here owns the **analytical readers** of that column (dbt sources, CDC, exports, raw SQL in jobs). **API response shapes** → backend `http-contract-scan`. **OLTP timestamp storage** → database `schema-integrity-scan` §5; §6 here owns type mixing on **load** into the warehouse.
- **Who reads a table** → `lineage-trace` (this pack; §2 and §4 here call it for the reader list). **Whether a data test catches a semantic break** → `data-test-scan` §5 (`accepted_values` vs a `CASE`). **A metric whose definition moved** → business `report-scan` §2.

## Adapt to the codebase — the lanes

| Lane | Detect by | Read | Tool (offline, telemetry off) |
|---|---|---|---|
| **dbt contracts** | `contract:`, `access:`, `versions:`, `latest_version`, `deprecation_date`, `constraints:` in model YAML | `model-graph.py` `--class=SC` (effective contract, access, materialization, adapter enforcement) | `dbt parse` / `dbt build --select state:modified+ --state <base artifacts>` on a duckdb profile in `$OUT` |
| **Data contracts** (ODCS, `datacontract.yaml`) | `apiVersion: v3`, `dataContractSpecification`, `datacontract.yaml` | declared fields, types, quality rules | `datacontract lint`, `datacontract breaking old.yaml new.yaml` (exit 1 on a breaking change); `DO_NOT_TRACK=1` |
| **Git diff** | a base branch or SHA (`BASE`) | removed/renamed columns, changed `data_type`, dropped `versions:` entries | `git diff` read-only (`GIT_OPTIONAL_LOCKS=0`) |
| **App migrations as producers** | SQL, Knex/MikroORM/TypeORM, Prisma SQL, Rails, Django, Laravel migrations | `drop column`, `rename column`, `alter column … type`, `set not null`, ORM equivalents | a scratch DB with the migration applied (V558); sqlglot to resolve raw SQL readers |
| **Warehouse types** | casts and DDL in models and loaders; the profile's session zone | `TIMESTAMP_NTZ`/`LTZ`/`TZ`, BigQuery `DATETIME` vs `TIMESTAMP`, `::timestamp` on `timestamptz` | V552 on the real cast |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; G and 0 build the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; path globs may stand together (they OR by intent) but are never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Migrations are **in** scope for §4. `git` runs read-only. Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the analytics, app and migration roots
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-sc.XXXXXX")}"; mkdir -p "$OUT/none"; BASE="${BASE:-}"   # BASE=origin/main for a diff run
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**' -g '!**/*.{spec,test}.*' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# G  the dbt graph without dbt (incremental-load-scan/scripts/model-graph.py): exit 0 built · 4 no dbt project (dbt lane N/A) · 2 blocked
MG=.claude/skills/incremental-load-scan/scripts/model-graph.py
if command -v python3 >/dev/null 2>&1 && [ -f "$MG" ]; then python3 -I -B "$MG" "${ROOTS[@]}" --out="$OUT/graph" --class=SC > "$OUT/graph.txt" 2> "$OUT/graph.err"; echo "G model-graph exit $? → $OUT/graph.txt"; sed -n '2,4p' "$OUT/graph.txt"; grep '^\[' "$OUT/graph.txt"
else echo 'G NOT-RUN (python3 or model-graph.py absent): §1 and §3 are read by hand from 1a and 3 and print Live, unreviewed'; fi
# 0 THE PUBLISHED SURFACE — 0a published or contracted models · 0b data-contract files
h 0a; rg -n --pcre2 '^\s*(?:\+?access\s*:\s*["\x27]?public|\+?contract\s*:|enforced\s*:\s*true|latest_version\s*:|deprecation_date\s*:|-\s*v\s*:\s*\d+)' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 0a ${PIPESTATUS[0]}
h 0b; rg -l --pcre2 '^\s*(?:dataContractSpecification|apiVersion\s*:\s*["\x27]?v3|kind\s*:\s*DataContract)\b' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}"; ck 0b $?
# 1 SC-1 unenforced or unenforceable contracts — G rows (published with no contract; PK/unique/FK metadata-only on the adapter; contract + incremental on_schema_change; unsupported materializations) + 1a warn_unenforced off
h 1a; rg -n --pcre2 '\bwarn_unenforced\s*:\s*false\b|^\s*-?\s*type\s*:\s*(?:primary_key|unique|foreign_key)\b' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 1a ${PIPESTATUS[0]}
# 2 SC-2 breaking change with no version — the git lane (removed columns, changed data_type, dropped versions) against BASE
h 2; if [ -n "$BASE" ] && GIT_OPTIONAL_LOCKS=0 git rev-parse --verify -q "$BASE" >/dev/null 2>&1; then GIT_OPTIONAL_LOCKS=0 git diff --no-color -U0 "$BASE"...HEAD -- '*.yml' '*.yaml' '*.sql' | rg --pcre2 '^(?:\+\+\+ b/|-\s*-\s*name\s*:|[-+]\s*data_type\s*:|[-+]\s*(?:latest_version|deprecation_date|versions)\s*:|-\s*-\s*v\s*:)'; else echo "2 NOT-RUN (no BASE, or BASE not in this clone): whole-repo runs read §2 from versions:/deprecation_date in 0a only"; fi
# 3 SC-3 SELECT * past staging — G rows (final select *) + the hand lane over marts and intermediate SQL
h 3; rg -n --pcre2 '(?i)\bselect\s+(?:distinct\s+)?\*\s+from\s+(?!final\b|renamed\b|joined\b)|\bselect\s+(?:distinct\s+)?\w+\.\*\s' -g '**/models/marts/**' -g '**/models/intermediate/**' -g '**/models/mart/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 3 ${PIPESTATUS[0]}
# 4 SC-4 an app migration drops/renames/narrows a column an analytical reader still names — 4a the DDL · 4b each column's readers (dbt YAML, CDC configs, export/sync files, raw SQL)
h 4a; rg -n --pcre2 '(?i)\b(?:drop\s+column\s+(?:if\s+exists\s+)?|rename\s+column\s+)"?\w+"?|\balter\s+column\s+"?\w+"?\s+(?:type|set\s+data\s+type|set\s+not\s+null)\b|\.(?:dropColumn|renameColumn|dropColumns)\(\s*["\x27]\w+|\b(?:remove_column|rename_column|change_column)\s+:\w+\s*,\s*:\w+|\b(?:RemoveField|RenameField|AlterField)\(|->(?:dropColumn|renameColumn)\(\s*["\x27]\w+' -g '**/{migrations,migration,db/migrate,alembic/versions,Migrations}/**' -g '**/prisma/migrations/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | tee "$OUT/DDL.txt" | head -60; ck 4a ${PIPESTATUS[0]}
rg -o -I --no-filename --pcre2 -r '$1$2$3$4$5' '(?i)\b(?:drop\s+column\s+(?:if\s+exists\s+)?|rename\s+column\s+)"?(\w{4,})"?|\balter\s+column\s+"?(\w{4,})"?\s+(?:type|set)|\.(?:dropColumn|renameColumn)\(\s*["\x27](\w{4,})|\b(?:remove_column|rename_column|change_column)\s+:\w+\s*,\s*:(\w{4,})|\bname\s*=\s*["\x27](\w{4,})["\x27]' "$OUT/DDL.txt" 2>/dev/null | sort -u > "$OUT/COLS.txt"
rg -l --pcre2 '"connector\.class"|^\s*connector\.class\s*[=:]|io\.debezium' -g '*.{json,properties,yml,yaml}' "${X[@]}" "${ROOTS[@]}" > "$OUT/CDC.txt"; RD=(); while IFS= read -r f; do RD+=("$f"); done < "$OUT/CDC.txt"
h 4b; while IFS= read -r c; do r=$(rg -l -w "$c" -g '**/models/**/*.{yml,yaml,sql}' -g '**/snapshots/**' -g '**/{dags,etl,jobs,pipelines,loaders,spark}/**' "${X[@]}" "${ROOTS[@]}" "${RD[@]}" | sort -u | tr '\n' ' '); [ -n "$r" ] && echo "$c → $r"; done < "$OUT/COLS.txt"
# 5 SC-5 semantic break — the data lane only: two snapshots of the same table (SNAP_A, SNAP_B: CSV or parquet paths) compared by distribution
h 5; SN=(); if [ -n "${SNAP_A:-}" ] && [ -n "${SNAP_B:-}" ]; then SN=("$SNAP_A" "$SNAP_B"); else while IFS= read -r f; do SN+=("$f"); done < <(rg --files -g '**/snapshots/**/*.csv' -g '**/data_snapshots/**/*.csv' "${X[@]}" "${ROOTS[@]}" | sort); fi
[ ${#SN[@]} -ge 2 ] && python3 -I - "${SN[@]}" <<'PY' || echo '5 N/A (data lane only: no two snapshots of one table in the repo, and none supplied as SNAP_A/SNAP_B)'
import csv, re, statistics, sys, collections
groups = collections.defaultdict(list)          # <table>_<YYYY-MM[-DD]>.csv → one group per table, ordered by date
for p in sys.argv[1:]:
    m = re.match(r'(.*/)?([A-Za-z]\w*?)_(\d{4}-\d{2}(?:-\d{2})?)\.csv$', p)
    if m:
        groups[m.group(2)].append((m.group(3), p))
pairs = [(t, sorted(v)[-2], sorted(v)[-1]) for t, v in groups.items() if len(v) >= 2]
if not pairs:
    sys.exit(1)
def load(p):
    return list(csv.DictReader(open(p, encoding='utf-8', newline='')))
for t, (da, pa), (db, pb) in pairs:
    a, b = load(pa), load(pb)
    for col in (a[0].keys() if a else []):
        va, vb = [r.get(col) for r in a], [r.get(col) for r in b]
        na = sum(1 for v in va if v in ('', None)) / max(len(va), 1); nb = sum(1 for v in vb if v in ('', None)) / max(len(vb), 1)
        if abs(nb - na) >= 0.05:
            print('%s.%s null rate %.0f%% -> %.0f%% (%s vs %s)' % (t, col, na * 100, nb * 100, pa, pb))
        try:
            fa = [float(v) for v in va if v not in ('', None)]; fb = [float(v) for v in vb if v not in ('', None)]
            ma, mb = statistics.median(fa), statistics.median(fb)
            if ma and mb and (mb / ma >= 8 or ma / mb >= 8):
                print('%s.%s median %g -> %g (x%.0f; row counts %d/%d) — unit or magnitude shift? (%s vs %s)' % (t, col, ma, mb, max(mb / ma, ma / mb), len(a), len(b), pa, pb))
        except (ValueError, statistics.StatisticsError):
            new = sorted(set(vb) - set(va))
            if new and len(set(va)) <= 20 and not re.search(r'(^|_)id$', col):
                print('%s.%s new members %s (%s vs %s) — read every CASE on this column' % (t, col, new, pa, pb))
PY
# 6 SC-6 timestamp type mixing on load — casts and DDL in models and loaders; the dbt profile's session zone
h 6a; rg -n --pcre2 '(?i)\btimestamp_(?:ntz|ltz|tz)\b|::timestamp\b(?!tz|_)|\bcast\s*\([^)]*\bas\s+(?:timestamp|datetime)\s*\)|\b(?:safe_)?cast\s*\([^)]*\bas\s+datetime\b|\bto_timestamp_(?:ntz|ltz)\s*\(|(?-i:\bDATETIME\b)' -g '**/models/**' -g '**/snapshots/**' -g '**/{etl,loaders,pipelines,jobs,dags,spark}/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -40; ck 6a ${PIPESTATUS[0]}
h 6b; rg -n --pcre2 '(?i)^\s*(?:timezone|time_zone|session_parameters|query_tag)\s*:' -g '**/profiles.yml' -g '**/dbt_project.yml' --hidden "${X[@]}" "${ROOTS[@]}"; ck 6b $?
```

4b prints `column → readers` for every column a migration drops, renames or narrows: each pair is a candidate until the read shows the reader moved first (an expand/contract sequence) or names another table's column of the same name. Column names under four characters are skipped (`id`, `day`) — read those statements by hand from 4a. Export and sync files are not searched here: an export that reads through the ORM entity is the app's own N-1 reader (database `migration-safety` §4); one that names the column in raw SQL is found from `extract-scan`'s surface by the read.

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s, 0 `rg` errors): G 4 SC rows (the public `fct_payments` with no contract; a BigQuery foreign key no test covers; two `select *` past staging) · 0a 10 published/contract/version lines · 2 `NOT-RUN` (a staged copy has no base) · 3 3 (the two `select *` models and a `select *` CTE that `warehouse-scan-audit` §4 owns) · 4a 3 statements → 4b 2 pairs (`legacy_status` → the dbt source, `stg_orders`, the Debezium include list; `phone_number` → staging, the snapshot, the CRM sync DAG) · 5 the two committed snapshot pairs: `refunds.refund_amount` median ×100 at the same row count, `payments.method` gains `bnpl` · 6a 2 (a local wall-clock string cast to an instant; `paid_at::timestamp` on landing). The `select * from final` tail is refuted (precedent § 23).
- **Real repo, read-only** (the NestJS monorepo, `ROOTS=(apps/api/src)`; 1.8 s; nothing written): G exit 4 — §1, §3 print `N/A (no dbt project)`; 4a 60 (the head of the migrations' drops, renames and type changes, `down()` reversals included) → 4b 0 pairs: no dbt source, CDC include list or DAG reads a column it changes; its exports read through ORM entities, which the app's own N-1 rule covers (database `migration-safety` §4). **A first draft of 4b** searched export and sheet files by path and paired common words (`phone`, `city`, `status`) with forty unrelated files; it now searches analytical readers only (dbt models and snapshots, pipeline folders, connector configs).
- **The dbt-contract, ODCS and warehouse-type lanes are fixture-measured only** (eval O-2).

## The 3,000-hit path

1. **Build the published set once** (G + 0a): only models with readers outside the project are §1/§2 subjects; a model nobody publishes is Hardening at most.
2. **Group by root**: one missing `+contract` default on `models/marts/` in `dbt_project.yml` is one decision; one migration file dropping six columns is one §4 row with its readers listed.
3. **Run the gate tools once** on a duckdb profile (`dbt build --select state:modified+ --state <base>` or `dbt parse`), and `datacontract breaking` once per contract pair; a tool exit is the V557 proof for every model it covers.
4. **Read the top 30 published tables fully** (readers, versions, the adapter's enforcement).
5. **Ledger the rest** as `Live, unreviewed (k tables / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | SC-1 published model with no enforced contract, or a contract relying on a constraint the adapter does not enforce | medium | V557 |
| 2 | SC-2 breaking change to a published model with no version or `deprecation_date` | high | V557 |
| 3 | SC-3 `SELECT *` past staging | low | V557 |
| 4 | SC-4 an OLTP migration drops/renames/narrows a column an analytical reader names | high | V558 |
| 5 | SC-5 semantic break (unit, zone, enum member, null rate) | high | V553 |
| 6 | SC-6 timestamp type mixing on load | medium | V552 |

### 1. Unenforced or unenforceable contract on a published model

```
BAD:   models: - name: fct_orders  access: public   (no contract)
       contract: {enforced: true}  columns: - name: order_id  constraints: [{type: primary_key}]   -- Snowflake: metadata only, no data test
GOOD:  contract: {enforced: true} + data_type per column; uniqueness by a `unique` + `not_null` data test, not the constraint
```
**Read the code:** Who reads the model (exposure, `access: public`, another project)? Is the contract enforced, and on this adapter which declared constraints are real (Postgres: all; Snowflake/BigQuery/Redshift/Databricks: `not_null`, Databricks also `check`)? Does a data test cover what the constraint only documents (precedent § 11)? Is the contract on a materialization that supports it (not `ephemeral`, Python, or a materialized view), and on an incremental with `on_schema_change` `append_new_columns` or `fail`? **Finding when** a published table can change shape without failing a build, or a declared uniqueness is believed and never checked. **Proof:** V557 — drop a contracted column in a scratch branch: `dbt build` fails at the contract preflight.

### 2. Breaking change with no version

**Read the code (the diff):** For each removed `- name:` or changed `data_type:` under a published model, is there a new `versions:` entry, `latest_version` still pointing at the old shape for readers, and a `deprecation_date` on the old version? Does CI compare against production artifacts (`--state` pointing at a real base, not `--target-path` itself)? Pre-release models are not this class. **Finding when** a reader's column disappears or narrows in a merge with no version and no notice. **Proof:** V557 — `dbt build --select state:modified+ --state <base>` or `datacontract breaking` exits non-zero.

### 3. `SELECT *` past staging

**Read the code:** Is the `select *` the model's final select over an upstream relation, or the tail of a CTE chain (`select * from final`, precedent § 23)? Is the model published or read by an export? On a columnar warehouse the same line is also a cost row (`warehouse-scan-audit` §4). **Finding when** an additive upstream change flows into a published shape. **Proof:** V557 — add an upstream column: the contracted model's build fails (or, uncontracted, the shape changes).

### 4. A migration under an analytical reader

```
BAD:   migrations/0042_orders.sql:  alter table orders drop column legacy_status;
       analytics/models/staging/_src.yml:  - name: legacy_status   ·   cdc/orders-source.json: "column.include.list": "…legacy_status"
GOOD:  expand → move every reader (dbt source, connector, export) → contract in a later release
```
**Read the code:** For each 4b pair, is the reader on the same table (not a same-named column elsewhere)? Was the reader moved before this migration ships (expand/contract), or does the migration ship first? Does the CDC connector fail on the missing column or silently stop carrying it? **Finding when** the migration breaks or silently empties a column an analytical reader still consumes. **Proof:** V558 — apply the migration to a scratch DB and run each reader: it fails before the fix and passes after.

### 5. Semantic break

The data lane, kept from this skill's first version: with two snapshots of the same table — committed exports named `<table>_<date>.csv` under a `snapshots/` folder (5 pairs them), or two files the user supplies as `SNAP_A`/`SNAP_B`, never fetched from production — compare per column — the mean/median moving by a power of ten or a currency-shaped factor with the row count stable (unit); a new distinct member that a downstream `CASE` sends to `ELSE` (enum — corroborate with `data-test-scan` §5); a null rate jumping (null); the hour histogram shifting by whole hours (zone); trailing-digit collapse (precision). A real business change looks like a unit change: cross-check row counts and a correlated column before calling it. **Finding when** a reader's numbers move with no shape change. **Proof:** V553 — an `accepted_values` or a distribution bound planted at the old shape goes red on the new snapshot. Without two snapshots §5 prints `N/A (data lane only)`.

### 6. Timestamp type mixing on load

**Read the code:** What does the source column hold (an instant, or local wall time)? What type does the landing cast produce — Snowflake `TIMESTAMP` defaults to `NTZ`, `TIMESTAMP_TZ` stores an offset not a zone; BigQuery `DATETIME` is naive, `TIMESTAMP` is an instant; Postgres `::timestamp` on a `timestamptz` drops the zone at the session's offset? Is the session `TIMEZONE` pinned in the profile (6b)? **Finding when** an instant is stored naive or converted at a session offset, so downstream buckets shift. **Proof:** V552 — the DST corpus through the real cast.

## Output

```
contract-diff — lanes: dbt 1.9.4 (dbt-snowflake in the prod profile; duckdb for proofs); git BASE=origin/main; migrations: knex
Graph: $OUT/graph — 4 published models · 6 SC candidates · 0b 0 data contracts

Findings: 2 · Unconfirmed: 1

1. apps/reporting/migrations/20261012_drop_legacy_status.ts:9        [report-with-fix]   high
   §4 SC-4 — dropColumn('legacy_status') on orders; readers: analytics/models/staging/_src.yml:14 (source column),
   cdc/orders-source.json:6 (column.include.list). V558 on a scratch PG: stg_orders fails (column does not exist).
   Fix: expand/contract — move stg_orders and the connector first, drop in the next release.
2. analytics/models/marts/_marts.yml:31                                [report-with-fix]   medium
   §1 SC-1 — fct_payments access: public, exposure finance_dashboard; contract: none (effective, dbt_project.yml:22 has no
   +contract for marts). Two-ended. Fix: contract: {enforced: true} with data_type per column.
3. analytics/models/marts/_marts.yml:12                                [report-flagged]    medium
   §1 SC-1 — primary_key constraint on fct_orders.order_id on dbt-snowflake (metadata only); the unique test is at
   severity warn. Unproven link: whether a reader relies on uniqueness. Settling: V553 (data-test-scan §2 corroborates).

Routed: 1 → distributed-systems event-contract-scan (orders.avsc landing) · 1 → database migration-safety §4 (same drop, app reader)
Verification: 12 candidates → 2 findings · 1 unconfirmed · 3 hardening · 6 refuted (self-verified; precedents § 11, § 23)

Class coverage:
  §1 contracts           checked (G 4 + 1a 2 → 1 finding, 1 unconfirmed)
  §2 unversioned break   NOT-RUN → N/A on a whole-repo run (no BASE); versions: present on 1 model, read
  §3 SELECT *            checked (G 1 + 3 2 → hardening: final CTE tail, precedent § 23)
  §4 migration readers   checked (4a 7 statements · 4b 1 pair → 1 finding)
  §5 semantic break      N/A (data lane only — no two snapshots supplied)
  §6 timestamp mixing    checked (6a 3 + 6b 0 → 0; both casts are TIMESTAMP_TZ on an offset-carrying source)
```

`[report-with-fix]`: the build/contract tool or the migration oracle failed on a scratch target, or the fact is two-ended (the change and its reader; the published model and its effective contract), and the fix is local to the YAML, the migration sequence or the cast. `[report-flagged]`: one link is unproven (a reader's reliance, the production adapter, the deploy order); the row names it and the settling oracle. The coverage block lists **all six** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `NOT-RUN (<reason>)`, `blocked (model-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 11 an unenforced constraint used as an optimizer hint when a data test covers uniqueness; § 23 `SELECT *` in a staging passthrough or as the last CTE statement; § 36 BACKWARD registry compatibility (routed).
- A pre-release model with no reader; column order changes (diff by name); type aliases (`text`/`varchar`, `int8`/`bigint`); identifier case folding.

## When to run

- On any diff that touches a published model's YAML or SQL, `dbt_project.yml` contract defaults, a data-contract file, an application migration that drops, renames or narrows a column, or a landing cast — `/audit-data-quality`'s contract signal.
- On every whole-repo `/audit-data-quality`, reporting all six §s; when an upstream team announces a change; when a load starts failing after "nothing changed".

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the change, the reader and the effective contract with their `file:line` — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@warehouse-modeler` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`.
- **§2 needs both sides; §5 needs two snapshots.** Without them the § prints `NOT-RUN` / `N/A (data lane only)` — never a verdict diffed against "the last successful load".
- **Never run `dbt build`, a migration or `datacontract test` against a shared or production target.** Proofs use a duckdb profile in `$OUT` (`DO_NOT_TRACK=1`, `DBT_SEND_ANONYMOUS_USAGE_STATS=False`, `DBT_ENGINE_SEND_ANONYMOUS_USAGE_STATS=false`) or a throwaway container. `git` runs read-only; this skill writes nothing into the audited repo, and `find <root> -newer "$OUT/graph.txt"` is empty at the end. A contract or version proposal is `/data-fix`'s and the version bump is the user's call.
- **No `[report-with-fix]` without the V-oracle failing** or a two-ended fact. **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the contracts look fine"** without the coverage block.

## Related

- `/audit-data-quality` and `/audit-data-model` dispatch this skill; `@warehouse-modeler` judges SC rows; `/data-fix` closes them with V552/V553/V557/V558 failing first.
- This pack: `lineage-trace` (the reader list §2/§4 attach), `data-test-scan` §5 (enum gaps), `warehouse-scan-audit` §4 (the cost side of `SELECT *`), `incremental-load-scan` §6 (`on_schema_change` on incrementals).
- distributed-systems `event-contract-scan`, database `migration-safety` §4 and `schema-integrity-scan` §5, backend `http-contract-scan`, business `report-scan` §2, when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): dbt docs — model contracts, constraints (per-adapter enforcement), model versions and `deprecation_date`, state comparison caveats; datacontract-cli 1.2.7 (`lint`, `breaking`; MIT) and ODCS v3.x; Snowflake and BigQuery datetime type docs; sqlfluff `AM04` (DE-A-52…62, DE-A-66, DE-B-41). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
