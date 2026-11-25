---
name: lineage-trace
description: "Model graph without dbt: hard-coded relations, layer breaks, undeclared readers, orphans; up/downstream trace of a node."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: lineage-trace

## Premise

Nobody changes a warehouse model without knowing its readers on purpose; they do it because finding the readers is tedious, and the graph they would ask is wrong in three predictable ways. A model that reads `analytics_raw.payments` instead of `{{ source('raw', 'payments') }}` is an edge the framework never sees: the build order can run it before its parent, and a trace from `payments` misses it. A mart that reads a raw source directly, or a staging model that joins two sources, ties consumers to raw shapes and duplicates logic. And the readers that matter most — a dashboard, a scheduled export, an application query, a reverse-ETL sync — are outside the project unless an `exposures:` entry names them. A lineage report that silently omits them converts an unknown into false confidence.

This skill owns research ids LN-1…LN-4 (`research-data-engineering.md` § 1.5), shipped as `DE-LN-<n>`: **whether the model graph is complete and layered, and who reads each node.** It also answers the trace question the other skills ask — *who is downstream of this column, model or table* — with real paths, never "some dashboards".

**Every finding cites the model `<file:line>` + the relation as written + the edge the graph has (or lacks) + the layer of each end + the readers found inside and outside the project + the oracle that would settle it + the fix (`ref()`/`source()`, a staging model, an `exposures:` entry, a retirement).** A grep hit is a candidate. "The lineage is complete" is never printed; a trace with an unread consumption layer is printed `PARTIAL — <what was not traced>`. Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V559.

## The rule

A candidate is a finding when all four hold:

1. **The node is built and scheduled.** The model is enabled and selected by a job (CI, cron, dbt Cloud, a DAG). An `analyses/` file or a disabled model fails here.
2. **The relation is read as written.** The raw `schema.table`, the `source()`/`ref()` call, the layer from the path; for readers outside the project, the file that names the physical table.
3. **No existing control, across files.** A macro that resolves the relation through `source()`/`ref()`, a CTE name, `{{ this }}`, `information_schema` (precedent § 24); a declared exposure; a source read by a non-dbt job cited by file.
4. **The oracle fired, or the fact is two-ended.** V559 — the graph's edges per model equal the relation mentions in its SQL (a `sqlglot` table walk, or `dbt ls --select +<model>` on a duckdb profile) — or the static fact cites the raw relation and the missing edge.

## Boundaries

- **Whether a change breaks the readers found here** → `contract-diff` (this pack); **whether the data in a node is right** → `grain-probe`, `data-test-scan`; **cost of a view chain** → `warehouse-scan-audit` §4. This skill names *who*, not *whether*.
- **A metric defined twice** across models or in the BI layer → business `report-scan` §2 (when installed); this skill supplies the paths of both definitions.
- **Application-to-application data flow** (services calling each other, message topics) → distributed-systems; **the module dependency graph of application code** → code-quality `architecture-scan`. The in-app lane here maps only which application files name a derived or analytical table.

## Adapt to the codebase — the lanes

| Lane | Detect by | Graph source | Readers outside the graph |
|---|---|---|---|
| **dbt** (Core / Fusion, any adapter) | `dbt_project.yml` | `model-graph.py`: `ref()` (one- and two-argument), `source()`, raw `from/join schema.table`, Python models, snapshots, exposures; a committed `target/manifest.json` is a cross-check (`manifest-diff.tsv`) | `exposures:`; physical names searched in app code, BI definitions (LookML `sql_table_name`, Metabase/Superset exports), export jobs, reverse-ETL configs |
| **SQLMesh** | `MODEL (` in `*.sql` | model names in `FROM`; `sqlmesh dag` when installed | the same search |
| **Plain SQL / Python ETL** | `INSERT INTO … SELECT`, `to_sql(`, `read_sql(` in jobs | the table each job reads and writes (sqlglot when installed) | — |
| **In-app** (any ORM + raw SQL) | rollups, views and analytical tables in migrations | raw SQL `from/join/into/update` mentions per table | the files that name each derived table |
| **Runtime lineage** | `openlineage`, `dbt-ol`, `OPENLINEAGE_URL` | emitted events (never read here; noted as present) | — |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; G builds the graph. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; path globs may stand together but are never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the dbt project root(s) and the app roots whose code may read the warehouse
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-ln.XXXXXX")}"; mkdir -p "$OUT/none"; NODE="${NODE:-}"   # NODE=model.fct_orders for a trace
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**' -g '!**/*.{spec,test}.*' -g '!**/{docs,ai,.claude}/**' -g '!**/*.{md,mdx,lock}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#|--)')
# G  the dbt graph without dbt (incremental-load-scan/scripts/model-graph.py): exit 0 built · 4 no dbt project (dbt lane N/A) · 2 blocked
MG=.claude/skills/incremental-load-scan/scripts/model-graph.py
if command -v python3 >/dev/null 2>&1 && [ -f "$MG" ]; then python3 -I -B "$MG" "${ROOTS[@]}" --out="$OUT/graph" --class=LN > "$OUT/graph.txt" 2> "$OUT/graph.err"; echo "G model-graph exit $? → $OUT/graph/edges.tsv"; sed -n '2,10p' "$OUT/graph.txt"; grep '^\[' "$OUT/graph.txt"
else echo 'G NOT-RUN (python3 or model-graph.py absent): §1 and §4 are read by hand from 1 and 4 and print Live, unreviewed'; fi
# 1 LN-1 hard-coded relations — the hand lane over model SQL (G's LN-1 rows are the same class with CTEs removed)
h 1; rg -n --pcre2 '(?i)\b(?:from|join)\s+(?!\{\{|information_schema\b|lateral\b|unnest\b)["`]?[a-z_]\w*["`]?\.["`]?[a-z_]\w*["`]?(?:\.["`]?[a-z_]\w*["`]?)?(?!\s*\()' -g '**/models/**/*.sql' -g '**/snapshots/**/*.sql' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 1 ${PIPESTATUS[0]}
# 2 LN-2 layer direction — G rows (marts/intermediate reading source(); staging joining sources); 2a source() calls outside staging by path
h 2a; rg -n --pcre2 '\{\{\s*source\s*\(' -g '**/models/marts/**' -g '**/models/intermediate/**' -g '**/models/mart/**' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2a ${PIPESTATUS[0]}
# 3 LN-3 readers outside the graph — 3a exposures declared · 3b marts' physical names named outside the dbt project · 3c runtime lineage present
h 3a; rg -c --pcre2 '^\s*exposures\s*:' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}"; ck 3a $?
[ -s "$OUT/graph/models.tsv" ] && awk -F'\t' 'NR>1 && $5=="marts" {sub(/^model\./,"",$2); print $2}' "$OUT/graph/models.tsv" | sort -u > "$OUT/MARTS.txt"
h 3b; [ -s "$OUT/MARTS.txt" ] && while IFS= read -r m; do r=$(rg -l -w "$m" -g '!**/models/**' -g '!**/snapshots/**' -g '!**/target/**' -g '!**/dbt_project.yml' "${X[@]}" "${ROOTS[@]}" | tr '\n' ' '); echo "$m → ${r:-no reader outside dbt}"; done < "$OUT/MARTS.txt"
h 3c; rg -l --pcre2 '\bopenlineage\b|\bdbt-ol\b|OPENLINEAGE_URL' -i "${X[@]}" "${ROOTS[@]}"; ck 3c $?
# 4 LN-4 orphans — G rows (unread non-mart models; declared sources never read); 4a schedules that select by name (read whether a 'dead' model is selected)
h 4a; rg -n --pcre2 '\bdbt\s+(?:run|build)\b[^\n]*(?:--select|-s)\s+[^\n]+' -g '**/.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci.yml' -g '**/dags/**' -g '**/Makefile' -g '**/*.sh' --hidden "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 4a ${PIPESTATUS[0]}
# IN-APP lane — which application files name each derived/analytical table in raw SQL (the reader list for rollups and views)
h app; rg -o -I --no-filename --pcre2 -r '$1' '(?i)\b(?:from|join)\s+"?((?:\w+_)?\w+_(?:daily|hourly|weekly|monthly|summary|stats|rollups?|agg|totals|facts|snapshots?|mv)|(?:mv|analytics|reporting|rpt)_\w+)"?\b' -g '*.{ts,js,py,rb,php,java,kt,go,sql}' -g '!**/{migrations,migration}/**' "${X[@]}" "${ROOTS[@]}" | sort | uniq -c | sort -rn | head -30
# TRACE (on demand): NODE's downstream and upstream closure from edges.tsv
[ -n "$NODE" ] && [ -s "$OUT/graph/edges.tsv" ] && python3 -I - "$OUT/graph/edges.tsv" "$NODE" <<'PY'
import sys, collections
down, up = collections.defaultdict(set), collections.defaultdict(set)
for line in open(sys.argv[1], encoding='utf-8').read().splitlines()[1:]:
    c, p, k, w = (line.split('\t') + ['', '', '', ''])[:4]
    down[p].add(c); up[c].add(p)
def walk(g, n):
    seen, st = set(), [n]
    while st:
        for x in g[st.pop()] - seen:
            seen.add(x); st.append(x)
    return sorted(seen)
print('downstream of', sys.argv[2], ':', ' '.join(walk(down, sys.argv[2])) or 'none in the graph')
print('upstream of', sys.argv[2], ':', ' '.join(walk(up, sys.argv[2])) or 'none')
PY
```

3b prints, per mart, the files outside the dbt project that name its physical table: `no reader outside dbt` on a mart with no exposure is an LN-3/LN-4 question for the read (a BI tool may read it through a connection the repo cannot see — `PARTIAL`, never "unused"). The model name stands for its physical name unless `alias:` or a custom schema changes it; read `models.tsv` for the alias column before trusting a miss.

### Measured (2026-10-19)

- **Fixture** (`benchmarks/fixtures/data-pipelines`, `ROOTS=(.)`; under 1 s): G 6 LN rows — two hard-coded `analytics_raw.*` relations, a mart reading `source()` directly, a staging model joining two sources, an unread staging model, a source nobody reads; 1 2 (the same raw relations); 2a 1; 3a 1 exposure; 3b 31 marts, of which the bank-feed mart and the CRM-sync dimension have undeclared outside readers, and three names collide with a DAG or table name — read; 4a 5 dbt selections. The project-level "no exposures" row does not fire because one exposure exists.
- **Real repo, read-only** (the NestJS monorepo, `ROOTS=(apps/api/src)`; 0.3 s): G exit 4 — §1, §2, §4 print `N/A (no dbt project)`. The in-app lane lists the order-day and quarter rollups (4 reading files each) and four `*_agg` CTE names inside report queries (CTEs, not tables — read); §3 prints `PARTIAL — no exposures; readers are application queries listed by the in-app lane`.
- **The dbt, SQLMesh and runtime-lineage lanes are fixture-measured only** (eval O-2).

## The 3,000-hit path

1. **Build the graph once** (G) and read `edges.tsv`: group LN-1 by the raw schema (`analytics_raw.*` in forty models is one decision — declare the source once, replace the relation everywhere).
2. **Run the oracle at scale** (V559): one `sqlglot` table walk over every compiled model (or `dbt ls --select +<model>` on a duckdb profile in `$OUT`), compared with `edges.tsv` per model; the difference is the LN-1 list.
3. **Rank** by consumption: marts with outside readers (3b) and exposures first; staging last.
4. **Read the top 30 groups fully**; ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | LN-1 hard-coded relation instead of `ref()`/`source()` | medium | V559 |
| 2 | LN-2 layer direction violated | low | V559 |
| 3 | LN-3 readers undeclared (no exposures; outside readers invisible) | info (medium when a money or partner reader is found undeclared) | — (two-ended: the reader file and the missing exposure) |
| 4 | LN-4 orphans: scheduled models nobody reads; sources declared and unused | low | — (two-ended: the schedule and the absent reader) |

### 1. Hard-coded relation

```
BAD:   select … from analytics_raw.payments p join {{ ref('stg_orders') }} o on …
GOOD:  from {{ source('raw', 'payments') }} p   -- declared in _sources.yml; the graph and the build order see it
```
**Read the code:** Is the relation a CTE defined above, `{{ this }}`, `information_schema`, or resolved by a project macro (precedent § 24)? Is it a table another dbt project builds (then a cross-project `ref` or a declared source)? **Finding when** a real upstream relation is invisible to the graph, so the build order or a trace is wrong. **Proof:** V559 — the table walk of the compiled SQL lists a relation that `edges.tsv` lacks.

### 2. Layer direction

**Read the code:** Does a mart or intermediate model read `source()` directly (a staging model would own the renames and casts once)? Does a staging model join two sources? Is the project small enough that two layers are the convention (not a finding)? **Finding when** the same raw-shape logic is duplicated in two marts, or a mart breaks on a raw rename that staging should have absorbed. **Proof:** V559 with the layer of each edge's ends.

### 3. Readers undeclared

**Read the code:** For each mart, which files outside the project name it (3b) — an export job, an app query, a LookML view, a reverse-ETL config? Is each declared as an exposure? Does runtime lineage (OpenLineage) cover what the repo cannot? **Finding when** a reader that acts on money or sends data to a partner is found and undeclared — a breaking change would not list it. Otherwise print the trace `PARTIAL` with the gap named.

### 4. Orphans

**Read the code:** Is the "orphan" selected by a schedule (4a) and read by nothing (no model, no exposure, no outside file)? Is a declared source read by a non-dbt job (cite it)? **Finding when** a scheduled model or source has no reader anywhere the repo can show — spend and freshness alerts for nothing. Retirement is the owner's call; the row names the schedule and asks.

## Output

```
lineage-trace — lanes: dbt 1.9.4 (static graph; no manifest); in-app: postgres raw SQL; runtime lineage: none
Graph: $OUT/graph — 14 models · 3 snapshots · 6 sources · 29 edges (ref 17, source 9, raw 3) · 0 exposures

Findings: 1 · Unconfirmed: 1 · PARTIAL: consumption layer (no exposures; BI not in repo)

1. analytics/models/staging/stg_invoices.sql:4                     [report-with-fix]   medium
   §1 LN-1 — `from analytics_raw.invoices` (raw edge, no source()); fct_invoices and invoices_daily sit downstream and
   build before it on a fresh target. V559: sqlglot lists analytics_raw.invoices; edges.tsv has no parent.
   Fix: declare raw.invoices in _src.yml and use {{ source('raw','invoices') }}.
2. analytics/models/marts/fct_invoices.sql:1                       [report-flagged]    medium
   §3 LN-3 — read by apps/reporting/src/exports/finance-feed.ts:22 (partner file) with no exposure. Unproven link:
   whether finance-feed is scheduled. Settling: the scheduler file.

Trace (NODE=model.stg_invoices): downstream fct_invoices invoices_daily · upstream raw:analytics_raw.invoices
Verification: 9 candidates → 1 finding · 1 unconfirmed · 3 hardening · 4 refuted (self-verified; precedent § 24)

Class coverage:
  §1 hard-coded relation   checked (G 2 + 1 3 → 1 finding; 1 CTE refuted, precedent § 24)
  §2 layer direction       checked (G 2 + 2a 1 → hardening: small project, two layers)
  §3 undeclared readers    checked (3a 0 · 3b 4 marts → 1 unconfirmed) — PARTIAL: BI tool outside the repo
  §4 orphans               checked (G 2 · 4a 1 → hardening: the unused source feeds a reverse-ETL job, cited)
```

`[report-with-fix]`: V559 shows the missing edge, or the fact is two-ended (the raw relation and the absent edge; the reader file and the missing exposure), and the fix is local to the model or the YAML. `[report-flagged]`: one link is unproven (the reader's schedule, an alias, a cross-project build); the row names it. The coverage block lists **all four** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (model-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`; a trace prints `PARTIAL — <gap>` whenever a consumption layer was not read.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 24 `information_schema`, `{{ this }}`, a macro-resolved relation or a CTE name.
- A small project with two layers (not LN-2); a source read by a non-dbt job, cited (not LN-4); an alias that changes the physical name (read before calling a mart unread).

## When to run

- Before changing or deleting a model, column or source (the trace); on any diff that adds a model, a `source()`, a raw relation or an exposure — `/audit-data-quality`'s lineage signal; when sizing a defect's blast radius under `/audit-data-model`.
- On every whole-repo `/audit-data-quality`, reporting all four §s.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the relation, the edge list and the readers with their `file:line` — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@warehouse-modeler` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`.
- **Never present a partial trace as complete.** Hard-coded relations make the graph `PARTIAL — hard-coded edges`; an unread BI layer, export or reverse-ETL destination makes it `PARTIAL — consumption layer not traced`, with what access would settle it. Never imply zero readers because none were visible.
- **Halt before §1, §2 and §4 when model-graph is blocked** (exit 2): they print `blocked`, never `checked`. Exit 4 prints the dbt lane `N/A (no dbt project)`.
- **Never run `dbt` against a shared target and never emit lineage events** (`OPENLINEAGE_URL` stays unset). This skill writes nothing into the audited repo; `find <root> -newer "$OUT/graph.txt"` is empty at the end; a fix is `/data-fix`'s.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the lineage is complete"** without the coverage block.

## Related

- `/audit-data-quality` and `/audit-data-model` dispatch this skill; `contract-diff` §2/§4 and `/backfill-plan` call its trace for the reader list; `@warehouse-modeler` judges LN rows; `/data-fix` closes them.
- This pack: `incremental-load-scan/scripts/model-graph.py` (the graph), `warehouse-scan-audit` §4 (view-chain depth from the same edges), `pii-copy-scan` (where a PII column flows).
- business `report-scan` §2, code-quality `architecture-scan`, when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): dbt-project-evaluator rules (`fct_hard_coded_references`, `fct_marts_or_intermediate_dependent_on_source`, `fct_source_fanout`, `fct_unused_sources`; v2.0.0, 2026-10-16); dbt `parse` / `ls` docs; sqlglot 30.23.0 table and column lineage (MIT); sqllineage 1.5.9; OpenLineage 1.54.0 (DE-A-63…67). Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
