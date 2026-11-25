---
name: data-test-scan
description: "dbt, GX and Soda data tests that cannot fail or never run: grain, warn-only, empty slices, freshness."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: data-test-scan

## Premise

A data test is the only thing between a duplicated key and the dashboard, and it fails open in six documented ways (dbt docs, accessed 2026-10-19): a `where:` that narrows the test to a slice that can be empty; `severity: warn` on a key test, so the build exits 0; a loosened `error_if`; `relationships` on a nullable foreign key (NULLs pass by design); `accepted_values` compared as quoted strings on a numeric column; source freshness with only `warn_after`. Soda and SQLMesh column checks pass on an **empty** table unless a row-count check exists; Dagster asset checks do not block by default; and a suite that CI never runs protects nothing. Counting test files measures none of this. **A data test is proved by making it fail**: plant the violating row in a scratch target and watch it go red.

This skill owns research ids DQ-1…DQ-8 (`research-data-engineering.md` § 1.3), shipped as `DE-DQ-<n>`: **whether a data test can fail, and whether it runs.**

**Every finding cites the test or the model `<file:line>` + its effective configuration and where each value came from (the test's own `config:` → the project's `data_tests:` tree → the default) + the violating row that would pass + the oracle or the mutation that would settle it + the fix in the project's own test framework.** "The data is well tested" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V553–V556 and V564.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The model, source or table the test guards is consumed (a mart, an export, an exposure, a contract, a downstream job). A test on a scratch or deprecated model fails here.
2. **The contract is read.** The grain and the mandatory columns come from the model's docs, its contract, its primary key, or the consumer that joins on it. A missing grain is `[report-flagged]` with the grain named as the gap (and `grain-probe` §1's row).
3. **No existing control, across files.** Another test covering the same rule on the full table, an enforced constraint **on an adapter that enforces it** (§ Constraint enforcement), a unit test on the logic, a CI step that runs the tests elsewhere, a reconciliation job.
4. **The oracle fired, or the fact is two-ended.** The mutation ran and the test stayed green; or the static fact cites both ends — the test's effective setting with its source, and the build or CI command that makes that setting harmless (`severity: warn` + a `dbt build` whose exit code gates nothing else).

## Boundaries

- **Application tests** (unit, integration, e2e; assertion strength, mutation of code) → the testing pack, when installed. This skill owns tests on **data**.
- **A reported number reconciled with the books** (ledger, invoices, provider export) → business `report-scan` §6; §6 here owns the mechanical equality of a derived table with its own detail. An in-app rollup's reconciliation is `derived-data-scan` §3 (this pack) — §6 here reads it and does not grade it twice.
- **Whether a failed Dagster check blocks downstream** → `orchestration-scan` §9; **the incremental load the test guards** → `incremental-load-scan`; **a contract's shape and versioning** → `contract-diff`; **the grain itself, probed on data** → `grain-probe`.

## Constraint enforcement — never accept a declared key as proof outside Postgres

| Adapter | Enforced | Metadata only | Source |
|---|---|---|---|
| Postgres | every constraint type | — | dbt constraints (accessed 2026-10-19) |
| Snowflake, BigQuery, Redshift | `not_null` | primary key, unique, foreign key | dbt constraints |
| Databricks | `not_null`, `check` (the table is created first, so a failed constraint leaves the bad rows in place) | primary key, unique, foreign key | dbt constraints |

A uniqueness guarantee outside Postgres is a **data test** (`unique`, `unique_combination_of_columns`), never a declared constraint. `warn_unenforced: false` with a covering data test is precedent § 11.

## Adapt to the codebase — the lanes

| Lane | Detect by | What the scan reads | Run it offline |
|---|---|---|---|
| **dbt** (Core / Fusion) | `dbt_project.yml`, `models/**/*.yml` | `model-graph.py --tests`: every test with its effective `severity` (and source), `where`, `enabled`, `error_if`/`warn_if`, `store_failures`; source freshness after inheritance; unit tests; per-layer counts | `dbt build` / `dbt test` against a duckdb profile written in `$OUT` (dbt-duckdb 1.11.0), `DO_NOT_TRACK=1`, `DBT_SEND_ANONYMOUS_USAGE_STATS=False`, `DBT_ENGINE_SEND_ANONYMOUS_USAGE_STATS=false` |
| **dbt packages** | `dbt_utils.*`, `dbt_expectations.*`, `elementary` in `packages.yml` / tests | the same YAML, by test name | as dbt |
| **Great Expectations** (GX Core 1.x) | `great_expectations/`, `gx/`, `expect_*` suites, `ValidationDefinition`, checkpoints | `mostly` on key columns, `catch_exceptions`, row-count expectations, whether a checkpoint is called from CI or a DAG | a pandas DataFrame batch, `GX_ANALYTICS_ENABLED=False` |
| **Soda** | `checks for <dataset>:` YAML, Soda contract YAML | per dataset: a `row_count` check present, thresholds | **read the YAML only.** Soda Core v4 is Elastic License 2.0 (PyPI lists it as proprietary): never install, vendor or require it; its oracle is the equivalent SQL on a scratch target |
| **SQLMesh audits** | `AUDIT (`, `audits` on `MODEL (` | `blocking false`, `_non_blocking`, `number_of_rows`/`at_least_one` | `sqlmesh test` on the duckdb gateway |
| **CI** | `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, `.circleci/`, Makefile, dbt Cloud job JSON | `dbt run` with no `test`/`build`; selectors that drop tests or sources; `|| true` / `continue-on-error` around a test step | — |

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; G and 0 build the surface. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; a path glob is never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Nothing is written outside `$OUT`. Data-test files are the subject here, so `tests/` directories are **in** scope.

```bash
ROOTS=(.)   # monorepo: name the analytics and pipeline roots
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-dq.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,dbt_packages,logs}/**' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?:#|--|//)')
# G  the dbt graph and its tests (incremental-load-scan/scripts/model-graph.py): exit 0 built · 4 no dbt project (dbt lane N/A) · 2 blocked
MG=.claude/skills/incremental-load-scan/scripts/model-graph.py
if command -v python3 >/dev/null 2>&1 && [ -f "$MG" ]; then python3 -I -B "$MG" "${ROOTS[@]}" --out="$OUT/graph" --class=DQ,SC > "$OUT/graph.txt" 2> "$OUT/graph.err"; echo "G model-graph exit $? → $OUT/graph.txt ($OUT/graph/tests.tsv, sources.tsv)"; sed -n '2,10p' "$OUT/graph.txt"; grep '^\[' "$OUT/graph.txt"
else echo 'G NOT-RUN (python3 or model-graph.py absent): the dbt lane is read by hand from 2a and 4a and prints Live, unreviewed'; fi
# 0 THE SURFACE — 0a CI files that run dbt / GX / SQLMesh · 0b GX suites and runners · 0c Soda check files · 0d SQLMesh audits
h 0a; rg -n --pcre2 '\b(?:dbt\s+(?:run|build|test|seed|snapshot|source\s+freshness)|great_expectations\s+checkpoint|gx\s+checkpoint|\.run_checkpoint\(|sqlmesh\s+(?:run|plan|test|audit))\b[^\n]*' -g '**/.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci.yml' -g '**/Jenkinsfile' -g '**/azure-pipelines*.yml' -g '**/bitbucket-pipelines.yml' -g '**/.circleci/*.yml' -g '**/Makefile' -g '**/*.sh' -g '**/dags/**/*.py' --hidden "${X[@]}" "${ROOTS[@]}" | tee "$OUT/CI.txt"; ck 0a ${PIPESTATUS[0]}
h 0b; rg -l --pcre2 '"expectation_type"|\bexpect_[a-z_]+\b\s*[(:"]|\bgx\.expectations\.|\bValidationDefinition\b|\bExpectationSuite\b' -g '*.{py,json,yml,yaml}' "${X[@]}" "${ROOTS[@]}" | tee "$OUT/GX.txt" | wc -l; ck 0b ${PIPESTATUS[0]}
h 0c; rg -l --pcre2 '^\s*checks\s+for\s+[\w."-]+\s*:|^\s*dataset\s*:\s*\S+[\s\S]{0,400}^\s*checks\s*:' -U -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | tee "$OUT/SODA.txt" | wc -l; ck 0c ${PIPESTATUS[0]}
h 0d; rg -n --pcre2 '(?i)^\s*AUDIT\s*\(|^\s*audits\s*[(\[]' -g '*.sql' "${X[@]}" "${ROOTS[@]}" | wc -l; ck 0d ${PIPESTATUS[0]}
# 1 DQ-1 grain — from G (DQ-1 rows); hand lane: model YAML files with no grain test at all
h 1; rg -l --pcre2 '^\s*models\s*:' -g '**/models/**/*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '^\s*-\s*unique\b|[\[,]\s*unique\s*[\],]|unique_combination_of_columns|dbt_constraints\.primary_key'
# 2 DQ-2 cannot fail — 2a dbt YAML settings (G resolves the effective value); 2b GX tolerance and swallowed errors; 2c Soda datasets with no row_count; 2d SQLMesh non-blocking
h 2a; rg -n --pcre2 '\bseverity\s*:\s*["\x27]?warn\b|\bwhere\s*:\s*["\x27][^\n]*(?i:current_date|current_timestamp|now\(\)|getdate|sysdate|\{\{)|\benabled\s*:\s*false\b|\b(?:error_if|warn_if)\s*:|\bwarn_unenforced\s*:\s*false' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2a ${PIPESTATUS[0]}
GX=(); while IFS= read -r f; do GX+=("$f"); done < "$OUT/GX.txt"; [ ${#GX[@]} -gt 0 ] || GX=("$OUT/none")
h 2b; rg -n --pcre2 '\bmostly["\x27]?\s*[=:]\s*0?\.\d+|\bcatch_exceptions\s*=\s*True|\bresult_format\s*[=:]\s*["\x27]?BOOLEAN_ONLY' "${GX[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
h 2c; [ -s "$OUT/SODA.txt" ] && tr '\n' '\0' < "$OUT/SODA.txt" | xargs -0 -n1 awk 'function out(){ if (ds != "" && !rc) print FILENAME ": " ds " — no row_count check" } /^[[:space:]]*checks[[:space:]]+for[[:space:]]/{ out(); ds=$3; sub(/:$/, "", ds); rc=0; next } /row_count/{ rc=1 } END{ out() }'
h 2d; rg -n --pcre2 '(?i)\bblocking\s*(?::=|=|:)\s*false\b|_non_blocking\b' -g '*.{sql,py,yml,yaml}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 2d ${PIPESTATUS[0]}
# 3 DQ-3 never executed — 3a CI files that run dbt but never test/build; 3b selectors and exclusions; 3c test steps whose failure is swallowed; 3d GX suites never run
h 3a; [ -s "$OUT/CI.txt" ] && cut -d: -f1 "$OUT/CI.txt" | sort -u | tr '\n' '\0' | xargs -0 rg -l --pcre2 '\bdbt\s+run\b' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bdbt\s+(?:build|test)\b'
h 3b; [ -s "$OUT/CI.txt" ] && rg --pcre2 '\bdbt\s+(?:build|test|run)\b[^\n]*(?:--exclude\b|--resource-type\b|--select\s+(?!\S*source:)\S+)' "$OUT/CI.txt"
h 3c; [ -s "$OUT/CI.txt" ] && cut -d: -f1 "$OUT/CI.txt" | sort -u | tr '\n' '\0' | xargs -0 rg -H -n --pcre2 '\b(?:dbt\s+(?:build|test|source\s+freshness)|checkpoint|sqlmesh\s+(?:test|audit))\b[^\n]*(?:\|\|\s*(?:true|:|exit\s+0)|;\s*true\b)|^\s*continue-on-error\s*:\s*true|^\s*allow_failure\s*:\s*true'
h 3d; [ -s "$OUT/GX.txt" ] && { rg -c --pcre2 '\.run\(|run_checkpoint|checkpoint\s+run|ValidationDefinition|great_expectations|\bgx\b' "$OUT/CI.txt" 2>/dev/null || echo 'GX suites exist and no CI line runs a checkpoint — read the DAGs and jobs that should'; }
# 4 DQ-4 freshness — from G (sources.tsv); hand lane: source YAML files with no freshness or no error_after
h 4a; rg -l --pcre2 '^\s*sources\s*:' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\berror_after\b'
# 5 DQ-5 FK and enum gaps — from G (relationships on nullable keys, numeric accepted_values without quote: false, CASE literals vs accepted_values)
# 6 DQ-6 reconciliation — from G (rollup models with no comparing test); 6a package tests comparing two relations; 6b singular tests named for it; in-app rollups → derived-data-scan §3
h 6a; rg -n --pcre2 '\b(?:equal_rowcount|fewer_rows_than|equality|expect_table_aggregation_to_equal_other_table|expect_table_row_count_to_equal_other_table)\b' -g '*.{yml,yaml,sql}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"; ck 6a ${PIPESTATUS[0]}
h 6b; rg --files -g '**/tests/**/*{reconcil,match,equal,tie_out,tieout}*.sql' "${X[@]}" "${ROOTS[@]}"; ck 6b $?
# 7 DQ-7 zero-row success — row-count guards that exist (dbt, GX, Soda, SQLMesh); G lists sources and incrementals with none
h 7; rg -n --pcre2 '\b(?:expect_table_row_count_to_be_between|expect_table_row_count_to_equal|at_least_one|not_empty|number_of_rows|row_count\s*[>=]|ExpectTableRowCountToBeBetween)\b' -g '*.{yml,yaml,sql,py,json}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l; ck 7 ${PIPESTATUS[0]}
# 8 DQ-8 coverage shape — from G (tests per layer; incrementals with window/CASE logic and no unit test); unit-test blocks present
h 8; rg -c --pcre2 '^\s*unit_tests\s*:' -g '*.{yml,yaml}' "${X[@]}" "${ROOTS[@]}"; ck 8 $?
```

2c runs one POSIX `awk` per Soda file (BSD and GNU alike) and prints each dataset whose block has no `row_count` check.

### Measured (2026-10-19)

- **Scratch sample** (a dbt-postgres 1.9 project — 5 models, 3 source tables, 7 YAML tests; a GX suite with `mostly` on two columns and a `catch_exceptions=True` runner; a Soda file with two datasets, one without `row_count`; a GitHub workflow running `dbt run --select marts+` and `dbt source freshness || true`): under 1 s, 0 `rg` errors, `find -newer` empty. G: model-graph exit 0, 16 `DQ` candidates — DQ-1 ×3 (`fct_events`'s only key test is `unique` at `warn` with no `not_null`; a rollup; a staging model), DQ-2 ×3 (two `severity: warn` key tests — one on `relationships`; an `accepted_values` sliced by `where: updated_at >= current_date`), DQ-4 ×2 (`warn_after` inherited from the source with no `error_after`; the table that overrides with `error_after` is quiet), DQ-5 ×1 (relationships on a nullable key), DQ-6 ×1 (a daily rollup), DQ-7 ×5, DQ-8 ×1. 2a 3, 2b 3 (`mostly` 0.95 on the key, 0.9 on a status column — read precedent § 12, `catch_exceptions=True`), 2c 1 (`orders` — no row_count; `customers` has one), 3a 1 (the workflow runs `dbt run` and never `build`/`test`), 3b 1 (`--select marts+`: no source tests), 3c 1 (`dbt source freshness || true`), 3d: GX suites with no CI checkpoint; 6a/6b 0 (no comparing test anywhere; G's DQ-6 row names the daily rollup).
- **Fixtures** (26 trees): 0 `rg` errors; G exits 4 everywhere (no dbt project → the dbt lane prints N/A); 0a–0d 0 — no fixture runs dbt, GX, Soda or SQLMesh, so every § prints `N/A (no data-test framework)`. A first draft of grep 6 matched bare `reconcil*` and listed 10 lines in four fixtures (a migration cutover plan, a ledger column, a bank-statement docstring): books and cutover reconciliation, not data tests — grep 6 now names the comparing test packages (6a) and singular test files (6b) only, and lists 0.
- **Real repo, read-only** (the NestJS monorepo, `ROOTS=(apps/api/src)`; nothing written): G exit 4; 0a–0d 0; 6a/6b 0. Its nightly rollup reconcile job is TypeScript — `derived-data-scan` §3 reads it (a control: it marks disagreeing days stale). **The dbt/GX/Soda lanes are fixture-measured only** (eval O-2).

## The 3,000-hit path

1. **Build the graph once** (G) and read `tests.tsv`: group by **(severity source, test name)** — one `+severity: warn` in `dbt_project.yml` turns every test under that path warn-only, one decision, one line to fix.
2. **Rank** by consumer: exposures, `access: public`, contracted and exported models first; then marts; staging last (DQ-8 records the shape, not each model).
3. **Read the CI once** (0a, 3a–3c): a suite CI never runs makes every §2 row moot until §3 is closed — report §3 first and the §2 rows under it.
4. **Prefer the bulk mutation oracle**: build the project into duckdb from committed seeds, then for each grain test plant one duplicate and one NULL in a scratch copy of the model's output and run `dbt test -s <model>` — every test that stays green is a confirmed §1/§2 row (V553).
5. **Read the top 30 groups fully**; ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them.

## Scans for

Severity assumes the guarded table is consumed. One step lower for staging-only tables; a test that guards money, a payout or a regulatory extract stays at its default.

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | DQ-1 consumed model with no grain test | medium | V553 |
| 2 | DQ-2 a test that passes by construction | medium | V553 |
| 3 | DQ-3 tests never executed | medium | V554 |
| 4 | DQ-4 freshness missing, warn-only, or keyed on warehouse metadata | medium | V555 |
| 5 | DQ-5 relationships on a nullable key; accepted_values missing or mis-quoted | medium | V553 |
| 6 | DQ-6 derived table never reconciled with its detail | medium | V564 |
| 7 | DQ-7 zero-row success | medium (low on optional datasets) | V556 |
| 8 | DQ-8 tests only on staging; complex incremental logic with no unit test | low | V553 |

### 1. Consumed model with no grain test

```
BAD:   - name: fct_events   columns: [{ name: event_id, data_tests: [{ unique: { config: { severity: warn } } }] }]
GOOD:  - name: event_id  data_tests: [unique, not_null]     · or dbt_utils.unique_combination_of_columns on the composite grain
```
**Read the code:** What is the grain (one row per what)? Does one column carry both `unique` and `not_null` (a `unique` alone passes many NULLs), or does a `unique_combination_of_columns` cover the composite key? Is uniqueness enforced by a constraint **on Postgres** with an enforced contract (§ Constraint enforcement)? **Finding when** a consumed model can hold two rows for one grain key and no enabled, error-severity test catches it. **Proof:** V553 — duplicate one key row in a scratch target: the test fails.

### 2. A test that passes by construction

```
BAD:   - unique: { config: { severity: warn } }                 # on the key — build exits 0
       - not_null: { config: { where: "updated_at >= current_date" } }   # empty slice on a quiet day
       - unique: { enabled: false } · error_if: ">1000" · GX mostly: 0.95 on the id · Soda `checks for orders:` with no row_count
GOOD:  error severity on key, FK and contract-critical tests; a where: only as a rolling window beside a full-table test
```
**Read the code:** For each 2a/2b/2c/2d hit and each G `DQ-2` row, what is the **effective** value and its source (`tests.tsv` prints both)? Is the test a key, FK or contract-critical rule (precedent § 3 keeps advisory tests at warn)? Can the `where:` slice be empty, and does another test cover the full table (precedent § 4)? Is the `error_if` threshold below the volume a real defect produces? Is `mostly` < 1 on a key column, or on a sampled noisy column (precedent § 12)? Does a GX runner check only `success` while `catch_exceptions=True` reports a broken expectation as unsuccessful without raising? `store_failures` records rows; it changes no verdict. **Finding when** a violating row on the guarded table leaves the build or the pipeline green. **Proof:** V553 — plant the violating row: the build or the checkpoint exits non-zero after the fix and zero before.

### 3. Tests never executed

```
BAD:   - run: dbt deps && dbt run --select marts+      # no test step; sources never tested
       - run: dbt source freshness || true
GOOD:  dbt build --select +marts+ (models and their tests, sources included) · freshness as its own failing step
```
**Read the code:** Does any CI job, scheduler or DAG run `dbt build` or `dbt test` on the models that matter (3a), including `source:` tests (3b — `--select marts+` selects downstream of marts, not the sources)? Is a test step's failure swallowed (3c)? Is there a GX checkpoint or SQLMesh audit run anywhere outside a notebook (3d)? A separate scheduled job that runs the tests is the control — cite it. **Finding when** a declared test can never fail a run anyone watches. **Proof:** V554 — a deliberately failing test makes the CI command (or the DAG task) exit non-zero.

### 4. Freshness missing, warn-only, or keyed on metadata

**Read the code:** After inheritance (source → table → `config:`), does each consumed source table have `freshness:`? Does it set `error_after` (a `warn_after` alone never fails)? Is `loaded_at_field` set — without it dbt falls back to warehouse metadata where it can, which is unreliable for some tables (BigQuery wildcard tables)? Is `dbt source freshness` run (§3)? An explicit `freshness: null` on a static seed or reference table is not this class. **Finding when** a feed that stops loading leaves every run green. **Proof:** V555 — set `loaded_at` beyond the SLA in a scratch source: freshness exits non-zero only with `error_after`.

### 5. Relationships on a nullable key; enum gaps

```
BAD:   - name: customer_id  data_tests: [{ relationships: { to: ref('dim_customers'), field: customer_id } }]   # NULLs pass
       case when status = 'paid' then … when status = 'refunded' then … else 0 end   # accepted_values: ['paid', 'pending']
GOOD:  not_null beside relationships when the FK is mandatory · accepted_values listing exactly the members the CASE handles
```
**Read the code:** Is the FK business-mandatory (precedent § 10 keeps optional FKs)? Does a model `CASE` branch on literals of a column whose `accepted_values` (in this model or its parent) is missing, or lists a different set — so a new member falls into `ELSE` silently? Are numeric or boolean `values:` compared as quoted strings (`quote: false` absent)? **Finding when** an orphan FK or a new enum member passes every test and changes a figure. **Proof:** V553 — a NULL FK row, an unknown enum value: the test fails.

### 6. Derived table never reconciled with its detail

**Read the code:** For each rollup model (`*_daily`, `*_summary`, `*_agg`, `*_totals`…) G lists, is there a test that compares it with its source — `equal_rowcount`, an aggregate-equality expectation, or a singular test that refs both? A full recompute from source each run needs none (precedent § 22). In-app rollups are `derived-data-scan` §3's row. **Finding when** a derived table can drift from its detail with nothing comparing them. **Proof:** V564 — mutate a detail row behind the rollup: the reconciliation fails.

### 7. Zero-row success

**Read the code:** Does each source and each incremental model have a row-count guard (`dbt_expectations.expect_table_row_count_to_be_between` with `min_value: 1`, `dbt_utils.at_least_one`, Soda `row_count > 0`, SQLMesh `number_of_rows`)? Column tests, Soda checks and SQLMesh audits all pass on an empty table. Is the dataset optional by design? Does a loader check the affected row count before marking success? **Finding when** an empty load passes every check and downstream reads nothing. **Proof:** V556 — run with an empty source batch: the run fails.

### 8. Coverage shape

**Read the code:** Where do the tests sit (`tests per layer` in G's header)? Do marts — where numbers become claims — have their own tests, or only staging? Do incremental models with window or `CASE` logic have a dbt unit test (dbt ≥ 1.8, `overrides.macros.is_incremental`) for the incremental branch? A pass-through model needs none. **Finding when** the logic most likely to be wrong has no test that exercises it. **Proof:** V553 on the mart (mutation), or a unit test that fails before the fix.

## Output

```
data-test-scan — lanes: dbt 1.9.4 + dbt-postgres (requirements.txt); great_expectations 1.5.0; soda yaml (read-only); ci: github actions
Graph: $OUT/graph — 7 tests · tests per layer: marts 5 · staging 2 · 0 unit tests · 16 DQ candidates

Findings: 2 · Unconfirmed: 2 · Enabler: 1

1. .github/workflows/dbt.yml:7                                     [report-with-fix]   medium
   §3 DQ-3 — CI runs `dbt run --select marts+` and never `dbt build`/`test`: all 7 tests and source tests never run.
   V554: a failing unique test leaves the job green. Fix: dbt build --select +marts+ (sources included).
2. analytics/models/marts/_marts.yml:24                            [report-with-fix]   medium
   §2 DQ-2 + §1 DQ-1 — fct_events.event_id: unique at severity warn (the test's own config) and no not_null.
   V553 on duckdb: a duplicated event_id → exit 0. Fix: unique + not_null at error.
3. analytics/models/marts/_marts.yml:16                            [report-flagged]    medium
   §2 DQ-2 — accepted_values on status sliced by `updated_at >= current_date`. Unproven link: whether a full-table test exists
   elsewhere (none in the repo). Settling: V553 with no row updated today.
4. soda/checks_orders.yml:1                                        [report-flagged]    medium
   §7 DQ-7 — `checks for orders` has no row_count. Unproven link: whether Soda runs anywhere (no CI line). Settling: V556.
5. (sources)                                                       Enabler             —
   §4 DQ-4 — shop.orders and shop.events inherit warn_after only; `dbt source freshness || true` in CI.

Verification: 27 candidates → 2 findings · 2 unconfirmed · 1 enabler · 6 hardening · 16 refuted (self-verified; precedents § 3, § 10, § 12, § 22)

Class coverage:
  §1 grain              checked (G 3 + 1 0 → 1 finding with §2; the rollup and stg_events → hardening, not consumed)
  §2 cannot fail        checked (G 3 + 2a 3 + 2b 3 + 2c 1 → 1 finding, 1 unconfirmed; GX mostly on status → precedent § 12)
  §3 never executed     checked (3a 1 + 3b 1 + 3c 1 → 1 finding)
  §4 freshness          checked (G 2 → enabler)
  §5 FK / enum          checked (G 1 → refuted: customer_id optional for guest orders, precedent § 10)
  §6 reconciliation     checked (G 1 → refuted: the daily rollup is a full recompute, precedent § 22)
  §7 zero-row           checked (G 5 + 2c 1 → 1 unconfirmed)
  §8 coverage shape     checked (marts 5 · staging 2 · 0 unit tests → 1 low row folded into §2's fix)
```

`[report-with-fix]`: the mutation or CI oracle failed on a scratch target or a dry CI run, or the fact is two-ended with the effective setting's source quoted, and the fix is local to the YAML, the suite, the check file or the CI step. `[report-flagged]`: one link is unproven (whether another job runs the tests, whether the dataset is optional, the grain); the row names it and the settling oracle. The coverage block lists **all eight** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (model-graph exit 2 | <grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 3 `severity: warn` on advisory or statistical tests; § 4 a `where:` rolling window on a huge table beside a full-table test; § 10 `relationships` passing NULLs on an optional FK; § 11 an unenforced constraint with `warn_unenforced: false` used as an optimizer hint when a data test covers uniqueness; § 12 `mostly` < 1 or `catch_exceptions` on sampled, noisy, non-key columns; § 22 a full recompute needs no reconciliation test.
- `freshness: null` on a static seed or reference table; a separate scheduled job that runs the tests (cite it for §3).

## When to run

- On any diff that touches a properties YAML, a source definition, a GX suite or checkpoint, a Soda check file, a SQLMesh audit, `dbt_project.yml`'s `data_tests:` tree, or a CI step that runs dbt — `/audit-data-quality`'s test signal.
- On every whole-repo `/audit-data-quality`, reporting all eight §s; `/add-data-model` runs it on the new model before it is done.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the test's effective setting with its source, the `file:line` and the violating row — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@data-quality-auditor` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`.
- **This skill is read-only.** It never adds, edits, enables or deletes a test, a suite, a check file or a CI step, and never writes a quality-contract file into the repo — writing the missing assertions is `/data-fix`'s job, after the audit. `git status --porcelain` and `find <root> -newer "$OUT/graph.txt"` are empty at the end.
- **Mutation runs only on a scratch target**: a duckdb profile written in `$OUT` (`--profiles-dir "$OUT"`, `--target-path "$OUT/target"`, `--log-path "$OUT/logs"`, telemetry off as in § Lanes), a throwaway container, or a rolled-back transaction — never a shared warehouse, never production. A mutation that cannot be isolated is `NOT-RUN`. **Soda Core is never installed, vendored or required** (Elastic License 2.0); its checks are proved with the equivalent SQL.
- **Halt before §1–§5 on a dbt project when model-graph is blocked** (exit 2): those §s print `blocked`, never `checked`; exit 4 prints the dbt lane `N/A (no dbt project)`.
- **No `[report-with-fix]` without a red mutation** or a two-ended static fact. A test file count is not coverage; "the tests pass" is not evidence a test can fail.
- **Do not grade a class another skill owns** (§ Boundaries). **Do not print "the data is well tested"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill and folds its coverage block into the class ledger (the four-floor coverage table lives inside its DQ section); `@data-quality-auditor` judges DQ rows; `/data-fix` writes the missing or strengthened tests, failing first.
- This pack: `grain-probe` (the grain proved on data), `incremental-load-scan` (the key the merge relies on), `derived-data-scan` §3 (in-app reconciliation), `contract-diff` (contracts and constraint enforcement), `orchestration-scan` §9 (blocking checks), `incremental-load-scan` (`scripts/model-graph.py`, the shared dbt graph), `lineage-trace`.
- business `report-scan` §6 (books), the testing pack (application tests), when installed.

## Sources

From the data-engineering research (2026-10-19): dbt docs — data tests, `where`, severity and thresholds, freshness, constraints, unit tests (dbt ≥ 1.8), usage stats; dbt-project-evaluator v2.0.0, dbt-checkpoint 2.0.10 and dbt-score 0.19.0 rule names (missing primary-key tests, sources without freshness); GX Core 1.24.0 (Apache-2.0, `GX_ANALYTICS_ENABLED`); soda-core 4.27.0 (Elastic License 2.0 — read-only); SQLMesh 0.236.3 audits; dbt-duckdb 1.11.0 as the offline oracle. Class ids DE-A-36…51 as catalogued there. Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
