---
name: grain-probe
description: "Prove a model's grain by probe: offline duckdb build first; dry-run cost guard before any warehouse count(distinct)."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: grain-probe

## Premise

A grain is a claim about data, so it is settled by data: reading the SQL forms the hypothesis, only the probe tells what is in the table. Every aggregate over a model inherits its grain; a duplicated key fans out every `SUM` downstream, a join on a non-key column multiplies rows inside the model, a Type 2 dimension with overlapping ranges doubles every fact that joins as-of a date in the overlap, and a composite key concatenated without a separator manufactures collisions (`'ab'||'1'` = `'a'||'b1'`). Two things make the probe dangerous in its own right: it is a full-table `count(distinct)`, which on a per-byte warehouse is an unbounded spend nobody estimated, and its offender sample can print personal data. So the probe runs **offline first** — the model built into duckdb from committed seeds or fixtures (dbt-duckdb 1.11 / DuckDB 1.5.6, MERGE since 1.4.0, research accessed 2026-10-19) — and touches a warehouse only after a dry-run byte estimate under a bound the user stated.

This skill owns research ids GR-1…GR-4 (`research-data-engineering.md` § 1.10), shipped as `DE-GR-<n>`: **whether a model's declared grain holds — key unique and non-null, joins of proven cardinality, Type 2 ranges intact, composite keys collision-free.**

**Every finding cites the model `<file:line>` + the declared grain sentence (or `UNDECLARED`) + the key expression probed + the scope (full table or the named partitions) + rows, distinct keys, duplicate rows and NULL keys with where they were measured (duckdb offline, or the warehouse after a dry run of N bytes) + the cause read from one offending group + the fix (a dedup with a total order, a join on the right side's key, a composite test, a separator).** "The grain looks fine" is never printed; the output is the probe report and the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V569 and V544.

## The rule

A candidate is a finding when all four hold:

1. **The model is consumed.** An exposure, `access: public`, a mart, an export or a downstream aggregate reads it. A staging model nobody aggregates is Hardening.
2. **The grain is declared.** One sentence ("one row per order line"), in the model's description or `meta`, or from `@warehouse-modeler`. With no declared grain the probe is refused and §1 reports `UNDECLARED` — a key that happens to be unique today is not a grain.
3. **No existing control, across files.** A `unique` + `not_null` test (or `unique_combination_of_columns`) at `error` that CI runs (`data-test-scan` §1–§3), an enforced primary key on Postgres, a dedup with a total order upstream, a join on the right side's declared key.
4. **The probe fired.** V569 on the duckdb build (or on the warehouse after the cost guard) returned duplicates, NULL keys, a fan-out or a range defect; V544 produced a collision for a separator-less composite key. A static reading alone is `[report-flagged]`.

## Boundaries

- **Whether a test exists that would catch the duplicate** → `data-test-scan` §1/§2 (this pack); this skill proves the data. **A report's `SUM` over a fan-out** → business `report-scan` §1 (when installed); a join that multiplies rows *inside a model* is §2 here. **Upstream shape changes behind a broken grain** → `contract-diff`. **Who reads the duplicated model** → `lineage-trace`.
- **Incremental merge keys that admit duplicates** → `incremental-load-scan` §2/§5; this skill proves the result in the table. **Warehouse cost policy** → finops; the cost guard here only bounds this skill's own probes.

## Adapt to the codebase — the lanes

| Lane | When | How | Never |
|---|---|---|---|
| **Offline (default)** | a dbt project with seeds, fixtures or a sample the user supplies | `dbt seed && dbt build -s +<model>` with a duckdb profile written to `$OUT` (`type: duckdb`, `path: "$OUT/scratch.duckdb"`), `DO_NOT_TRACK=1`, `DBT_SEND_ANONYMOUS_USAGE_STATS=False`, `DBT_ENGINE_SEND_ANONYMOUS_USAGE_STATS=false`, `--profiles-dir "$OUT"`; without dbt, the compiled SQL (or the model SQL with `ref()` replaced by seed tables, transpiled by sqlglot when the dialect differs) in `python3 -c 'import duckdb'` with `SET autoinstall_known_extensions=false` | a production profile |
| **Warehouse (opt-in)** | the user names a non-production target, or production with their word, and a byte bound | **dry run first** (`bq query --dry_run`, Snowflake `EXPLAIN`, Databricks `EXPLAIN COST`); run only below the bound; add `maximum_bytes_billed` / a statement timeout to the probe itself; scope to stated partitions when the bound requires it | a probe with no estimate; printing offender values from an unclassified table |
| **In-app tables** | a rollup or snapshot table in Postgres/MySQL | the same probes on a throwaway container with the migrations and a seeded history | the production database |

Exact distinct counts: several columnar engines approximate `count(distinct)` unless the exact form is requested (`APPROX_COUNT_DISTINCT` is opt-in on BigQuery; read the engine's docs in the run) — confirm exactness before trusting a small non-zero delta.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). It finds what to probe; it never connects to a warehouse. Grep **N** feeds §N; G builds the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; path globs may stand together but are never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # the dbt project root(s)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-gr.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,dbt_packages,logs}/**' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# G  the dbt graph (incremental-load-scan/scripts/model-graph.py): DQ-1 rows are the models with no grain test · exit 4 no dbt project · 2 blocked
MG=.claude/skills/incremental-load-scan/scripts/model-graph.py
if command -v python3 >/dev/null 2>&1 && [ -f "$MG" ]; then python3 -I -B "$MG" "${ROOTS[@]}" --out="$OUT/graph" --class=DQ-1,GR > "$OUT/graph.txt" 2> "$OUT/graph.err"; echo "G model-graph exit $? → $OUT/graph"; sed -n '2,6p' "$OUT/graph.txt"; grep '^\[' "$OUT/graph.txt"
else echo 'G NOT-RUN (python3 or model-graph.py absent): §1 reads model YAML by hand'; fi
# 0 THE OFFLINE LANE — seeds, a duckdb profile or adapter pin, dbt and duckdb availability (nothing is installed by this block)
h 0; rg --files -g '**/seeds/**/*.csv' -g '**/data/**/*.csv' "${X[@]}" "${ROOTS[@]}" | wc -l; rg -n --pcre2 '\bdbt-duckdb\b|\btype\s*:\s*duckdb\b' -g '**/requirements*.txt' -g '**/pyproject.toml' -g '**/profiles.yml' --hidden "${X[@]}" "${ROOTS[@]}"; command -v dbt >/dev/null 2>&1 && echo 'dbt on PATH' || echo 'dbt absent (compiled-SQL lane only)'; python3 -I -c 'import duckdb' 2>/dev/null && echo 'duckdb importable' || echo 'duckdb absent: offline probes NOT-RUN'
# 1 GR-1 grain declared? — per model entry in properties YAML: no description sentence naming the grain and no meta.grain (stdlib, no YAML library)
h 1; rg -l --pcre2 '^\s*models\s*:' -g '**/models/**/*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" > "$OUT/MODELYML.txt"; [ -s "$OUT/MODELYML.txt" ] && python3 -I - "$OUT/MODELYML.txt" <<'PY'
import re, sys
GRAIN = re.compile(r'(?i)\bone\s+row\s+per\b|\bgrain\s*[:=]|\bat\s+the\s+grain\s+of\b|\bunique\s+per\b')
for path in open(sys.argv[1]).read().split('\n'):
    if not path:
        continue
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    name, start, ind = None, 0, -1
    def close(end):
        if name and not any(GRAIN.search(l) for l in lines[start:end]):
            print('%s:%d: %s — no grain sentence' % (path, start + 1, name))
    for i, l in enumerate(lines):
        m = re.match(r'^(\s*)-\s+name:\s*["\x27]?([\w.]+)', l)
        if m and (ind < 0 or len(m.group(1)) <= ind):
            close(i); name, start, ind = m.group(2), i, len(m.group(1))
        elif re.match(r'^\S', l) and not l.startswith('  '):
            close(i); name, ind = None, -1
    close(len(lines))
PY
# 2 GR-2 join cardinality — every join to a ref()/source() with its ON predicate (read: is the right side's column its key?) · implicit and cross joins
h 2a; rg -n --pcre2 '(?i)\b(?:left\s+|inner\s+|right\s+|full\s+)?(?:outer\s+)?join\s+\{\{\s*(?:ref|source)\s*\([^)]*\)\s*\}\}\s*(?:as\s+)?\w*\s*(?:on\s+[^\n]+)?$' -g '**/models/**/*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | head -60; ck 2a ${PIPESTATUS[0]}
h 2b; rg -n --pcre2 '(?i)\bcross\s+join\b|\bfrom\s+\{\{[^}]+\}\}\s*(?:as\s+)?\w*\s*,\s*\{\{' -g '**/models/**/*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
# 3 GR-3 Type 2 range integrity — snapshots and dimensions with validity columns (the three probes run on each)
h 3; rg -l --pcre2 '(?i)\bdbt_valid_(?:from|to)\b|\bvalid_(?:from|to)\b|\beffective_(?:from|to|date)\b|\bis_current\b|\{%-?\s*snapshot\b' -g '**/models/**' -g '**/snapshots/**' "${X[@]}" "${ROOTS[@]}"; ck 3 $?
# 4 GR-4 composite keys — identifier||identifier and concat(a, b) with no literal separator; unique_key expressions built by concatenation
h 4; rg -n --pcre2 '(?i)\b[a-z_]\w*(?:\.\w+)?\s*\|\|\s*(?:cast\s*\(\s*)?[a-z_]\w*\b(?!\s*\|\|\s*["\x27])|\bconcat\s*\(\s*(?:[a-z_][\w.]*\s*,\s*)+[a-z_][\w.]*\s*\)|\bunique_key\s*=\s*["\x27][^"\x27]*\|\|' -g '**/models/**/*.sql' -g '**/snapshots/**/*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4 ${PIPESTATUS[0]}
```

The probes themselves (below) run only after the pre-flight, on the offline build or — with the cost guard satisfied — on the warehouse.

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s): 0 3 seed files, the duckdb profile and pin found, `duckdb absent: offline probes NOT-RUN` (the build environment has neither dbt nor duckdb, and nothing was installed — every V569 row in the key is `NOT-RUN` until `verify.sh` runs where `dbt-duckdb` is available); 1 2 models with no grain sentence (`refunds_ledger`, `int_customer_ltv`); 2a 4 joins (one on `email`, not the dimension's key); 2b 2 (an implicit cross join; the calendar spine, refuted); 3 5 Type 2 files; 4 2 separator-less keys (`order_id || line_no`, `concat(customer_id, campaign_id)`).
- **Real repo, read-only** (the NestJS monorepo): G exit 4, no dbt — §1–§4 print `N/A (no dbt project)`; the in-app lane applies to its rollup tables (the unique `(tenant, day)` constraint is the grain control). **A first draft of §1** was file-level (a YAML file with one grain sentence hid every model in it); it now reads each model entry.
- **The warehouse lane is never run without the user's bound**; it was not run in this build.

## The 3,000-hit path

1. **Probe in bulk offline**: build the whole project into duckdb once, then one SQL file computes the three numbers for every model whose grain is declared — one query per model, all on the scratch file.
2. **Group failures by cause** (a shared upstream join, a shared dedup macro), not by model: one fan-out in an intermediate model duplicates every mart above it.
3. **Rank** by consumer: exposures and money marts first.
4. **The warehouse only for what the offline build cannot represent**, one model at a time, each with its dry run and the user's bound.
5. **Ledger the rest** as `Live, unreviewed (k models)` with the command that continues them. Never `checked`.

## Scans for

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | GR-1 grain undeclared or unprobed on a consumed model | medium | V569 |
| 2 | GR-2 a join with no proven cardinality; an implicit cross join | high | V569 |
| 3 | GR-3 Type 2 overlaps, gaps, or more than one current row | high | V569 |
| 4 | GR-4 composite key probed column-wise or concatenated without a separator | low | V544 |

### 1. The three-number probe

State the grain sentence and the key expression first. Composite grains are probed as a composite, never column by column (a column-wise probe on a legitimate composite key always fails, gets disabled, and the real check disappears).

```sql
select count(*)                                    as rows_total,
       count(distinct <key_expression>)            as keys_distinct,
       count(*) - count(distinct <key_expression>) as duplicate_rows,
       count(*) filter (where <each key column> is null) as null_keys      -- engines without FILTER: sum(case … end)
from <model> [ where <stated partition filter> ]
```

`duplicate_rows = 0` and `null_keys = 0` is the only pass (a NULL key can never be joined to or merged on; `count(distinct)` hides it, and a NULL in any composite column drops the whole row from it). Then name the offenders — counts only when the table's PII classification is unknown:

```sql
select <key_expression> as k, count(*) as n from <model> [ where … ] group by 1 having count(*) > 1 order by n desc limit 20
```

Read one offending group's full rows and name the cause: a duplicate load, a join that fanned out (§2), a grain finer than declared, a legitimate repeat at the source, a Type 2 "current" that is not unique (§3). **Finding when** a consumed model's declared key is duplicated or NULL. **Proof:** V569 on the duckdb build.

### 2. Join cardinality

```
BAD:   from {{ ref('fct_order_lines') }} l join {{ ref('dim_customers') }} c on c.email = l.customer_email   -- email is not dim_customers' key
GOOD:  join on c.customer_id = l.customer_id (dim_customers' grain); or aggregate the right side to the join key first
```
**Read the code:** Is the right side's join column its declared key (and tested unique)? Is it a Type 2 dimension joined without an as-of predicate (`l.ordered_at >= c.valid_from and l.ordered_at < c.valid_to`)? Is a cross join a deliberate calendar spine (not a finding)? **Probe:** count the model's rows before and after the join, and on the right side `select <join key>, count(*) from <right> group by 1 having count(*) > 1` — an increase is fan-out, a decrease silent row loss; both are findings with both counts. **Proof:** V569.

### 3. Type 2 range integrity

For a dimension or snapshot with `valid_from`/`valid_to` (or `dbt_valid_from`/`dbt_valid_to`) and a current flag:
- **one current row per natural key** — the three-number probe on the natural key filtered to current rows;
- **no overlaps** — self-join on the natural key, count pairs whose intervals intersect;
- **no gaps** — per natural key ordered by `valid_from`, count rows whose next `valid_from` is later than this `valid_to`.

**Finding when** any count is non-zero: overlaps duplicate every as-of fact, gaps drop them. **Proof:** V569.

### 4. Composite keys

**Read the code:** Is the key concatenated with no separator (`order_id || line_no`), or with one that can occur in the values? Is a surrogate built from a column-wise list (`generate_surrogate_key([...])` is the control)? Is uniqueness tested per column instead of on the combination? **Finding when** two distinct tuples produce the same key, or the test cannot see the composite. **Proof:** V544 — a crafted pair (`'ab','1'` vs `'a','b1'`) collides in the model's own expression.

### Cost guard (before any warehouse probe)

1. **Offline first.** If the duckdb build can represent the model, the warehouse is not touched.
2. **Dry run.** Compile the probe; run the engine's dry run (`bq query --use_legacy_sql=false --dry_run`, `EXPLAIN`); record the bytes.
3. **The user's bound.** Run only when the dry-run bytes are under the bound the user stated in this session, on the target they named; production needs their explicit word. Add `maximum_bytes_billed` (BigQuery) or a statement timeout to the probe. Above the bound: scope to named partitions (and say so in the report — a clean last week does not clear the table) or report `NOT-RUN (bound)`.
4. **Never print offender values** from a table whose PII classification is unknown: counts only, and say the sample was withheld.

## Output

```
## grain-probe — fct_order_lines — 2026-10-19      lane: offline (dbt-duckdb, seeds/ + fixtures/; $OUT/scratch.duckdb)
Declared grain:  one row per order line (models/marts/_marts.yml:41)
Key expression:  order_id || '-' || line_no          Scope: full table

rows_total 4,812 · keys_distinct 4,790 · duplicate_rows 22 · null_keys 0          Verdict: DUPLICATED
Top offenders: withheld (PII classification unknown) — 22 keys with 2 rows each
Cause (one group read): join to dim_customers on email (fct_order_lines.sql:18); two customers share an email.

Findings: 1 · Unconfirmed: 1
1. analytics/models/marts/fct_order_lines.sql:18                   [report-with-fix]   high
   §2 GR-2 — join on dim_customers.email, not its key; rows 4,790 → 4,812 across the join (measured, duckdb). V569.
   Fix: join on customer_id; add relationships + a unique test on dim_customers.customer_id.
2. analytics/snapshots/accounts_snapshot.sql:1                     [report-flagged]    high
   §3 GR-3 — NOT-RUN on the warehouse: dry run 1.8 TiB > the stated bound 50 GiB. Offline: 0 overlaps on the seed.

Class coverage:
  §1 grain              checked (G 3 models with no grain test · 1 2 undeclared → 1 probed, 2 UNDECLARED → enablers)
  §2 join cardinality   checked (2a 9 joins · 2b 1 → 1 finding; calendar spine refuted)
  §3 Type 2 ranges      checked (3 3 → offline 0 defects; warehouse NOT-RUN (bound))
  §4 composite keys     checked (4 2 → 0; both use a separator)
```

`[report-with-fix]`: the probe ran (offline, or on the warehouse under the bound) and returned the defect, and the fix is local to the model. `[report-flagged]`: the probe could not run (no duckdb, bound exceeded, grain undeclared); the row names what would settle it. The coverage block lists **all four** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `NOT-RUN (<reason>)`, `blocked (model-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. Common traps:
- Probing the source instead of the model (the model may deduplicate); probing a subset and reporting it as the table.
- An approximate `count(distinct)` inventing a small delta; a calendar spine cross join (not GR-2); a composite key with a separator that cannot occur in the values (not GR-4).
- Declaring the grain from the probe result — backwards: the grain is a business statement, the probe tests it.

## When to run

- Before any aggregation claim is trusted; before approving a fact-to-dimension join (on the dimension's key); after a change to a grain, key expression, dedup rule or merge key; on a backfill's shadow target before cutover (`/backfill-plan`); on a new model (`/add-data-model`).
- On every whole-repo `/audit-data-quality` and `/audit-data-model`, reporting all four §s.

## Halt conditions

- **No declared grain → no probe.** §1 reports `UNDECLARED` (an enabler for `@warehouse-modeler`), never a guessed key.
- **Do not report a high row as confirmed until a separate verifier has refuted it.** Under `/audit-data-quality` or `/audit-data-model` that is `@warehouse-modeler` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; the verifier gets the grain, the key, the scope and the numbers with where they were measured — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md).
- **The cost guard is not optional** (§ Cost guard): no warehouse probe without a dry run under the user's bound; production only on their word; never a full-table `count(distinct)` on a per-byte engine "to be sure".
- **Probe the materialized output** (a view whose upstream has not run is not evidence). **State the scope** of every partition-filtered probe.
- **This skill writes nothing into the audited repo**: the duckdb file, the profile and the compiled SQL live in `$OUT`; `find <root> -newer "$OUT/graph.txt"` is empty at the end. A standing uniqueness test is `/data-fix`'s (or `/add-data-model`'s), proposed here, never written.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the grain looks fine"** without the probe numbers and the coverage block.

## Related

- `/audit-data-quality`, `/audit-data-model`, `/add-data-model` and `/backfill-plan` dispatch this skill; `@warehouse-modeler` declares the grain and judges GR rows; `/data-fix` turns a failed probe into a failing-first test.
- This pack: `data-test-scan` §1/§2 (the standing test), `contract-diff` (what changed upstream), `lineage-trace` (who reads the duplicated model), `incremental-load-scan` §2/§5 (merge keys and dedup order).
- business `report-scan` §1 (fan-out in a report's sum), finops (warehouse budgets), when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): dbt-duckdb 1.11.0 (2026-08-07, Apache-2.0) and DuckDB 1.5.6 (2026-09-28; MERGE since 1.4.0) as the offline engine; dbt usage-stats variables (`DBT_ENGINE_` prefix in 1.11+); BigQuery dry run (CC BY 4.0); sqlglot 30.23.0 for transpiling compiled SQL; sqlfluff `AM08`/`CV12` for join shapes (DE-B-48; pack grain-probe rows). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
