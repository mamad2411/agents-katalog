---
name: orchestration-scan
description: "Airflow, Dagster, Prefect DAGs: wall-clock windows, parse-time I/O, overlap, trigger rules, retries, Airflow 3."
kind: skill
pack: data-engineering
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: orchestration-scan

## Premise

A data orchestrator promises that a run for an interval reads that interval and only that interval, can be replayed for a past interval with the same result, and does not publish when its inputs failed. A task that computes its window from `datetime.now()` reads "today" during a backfill of last March; a DAG file that calls an API at import time runs that call on every parse; a publish task with `trigger_rule="all_done"` republishes yesterday over a failed load; three overlapping runs interleave writes into one partition. **Airflow 3 changed defaults under existing code** (Airflow "Upgrading to Airflow 3", 3.3.2 docs, accessed 2026-10-19): `catchup_by_default` and `create_cron_data_intervals` are now `False`, so a cron string maps to `CronTriggerTimetable` and `data_interval_start == data_interval_end` — a task that filters on the interval reads **zero rows and succeeds**; `execution_date`, `prev_execution_date`, `next_execution_date` and the yesterday/tomorrow `ds` variables are gone; tasks can no longer open metadata-database sessions.

This skill owns research ids OR-1…OR-9 (`research-data-engineering.md` § 1.2), shipped as `DE-OR-<n>`: **whether a data-orchestrator run is bounded by its interval, replayable, ordered and gated on its upstream.**

**Every finding cites the DAG/asset/flow `<file:line>` + the orchestrator and its version read from a pin + the run it breaks (a backfill of a past interval, a retry, two overlapping runs, a failed upstream, the first run after the Airflow 3 upgrade) + the oracle or the test that would settle it + the fix in the orchestrator's own API.** A grep hit is a candidate. "The DAGs look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md); the oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Data engineering, V540, V549–V551 and V553.

## The rule

A candidate is a finding when all four hold:

1. **Reachable.** The DAG, asset or flow is deployed: it sits in the DAGs folder the deployment mounts, a Dagster `Definitions` that the code location loads, or a Prefect deployment. An example DAG behind `load_examples` or a paused-forever prototype fails here.
2. **The version is read.** Airflow 2 vs 3, Dagster and Prefect majors come from a pin (`requirements*.txt`, `pyproject.toml`, the `apache/airflow:<tag>` image, a constraints URL). Several classes are a different verdict on each major; with no pin the row is `[report-flagged]` with the version named as the gap.
3. **No existing control, across files.** An explicit timetable, `catchup` set to what the team needs, `max_active_runs=1` or a pool of 1 on a shared partition, a short-circuit before the publish, a delete-then-insert keyed on the interval, a sensor `timeout`, an `airflow.cfg` / `AIRFLOW__…` setting that restores the old default.
4. **The oracle fired, or the fact is two-ended.** The task run for a past interval produced output that depends on the wall clock, the rendered interval is zero-width, the upstream failure did not stop the publish; or the static fact cites the version pin and the construct the version removed or redefined.

## Boundaries

- **Application schedulers** — Nest `@Cron`/`@Interval`, BullMQ repeatables, Celery beat, Sidekiq-cron, Laravel `schedule`, Spring `@Scheduled`, Kubernetes CronJobs: overlap, misfire and schedule zone → backend `job-lifecycle-scan` §4–§6; locks and leases → distributed-systems `coordination-scan`. Each when installed; without them the row is `[report-flagged]` here with the route named. **This skill reads data-orchestrator definitions only.**
- **The load the task runs** — merge key, watermark, overwrite scope → `incremental-load-scan`. §5 here is the retry that replays a non-idempotent write; whether the write itself is idempotent is `incremental-load-scan` §2's verdict, and the two rows cite each other.
- **A data test or asset check that cannot fail** → `data-test-scan`; §9 here only owns whether a failed Dagster check **blocks** downstream materialization.
- **Secrets fetched at parse time** are §2's cost and correctness row; the secret's exposure is security's.

## Adapt to the codebase — the lanes

| Lane | Detect by | Version source | What changes across versions |
|---|---|---|---|
| **Airflow** 2.x / 3.x | `from airflow`, `DAG(`, `@dag` | `apache-airflow` pin, `apache/airflow:<tag>`, `constraints-<v>` URL | AF3: `catchup` default False; cron → `CronTriggerTimetable` (zero-width interval) unless `create_cron_data_intervals` or an explicit `CronDataIntervalTimetable`; removed `execution_date` and friends, `schedule_interval`, SubDAGs, `DummyOperator`, `days_ago`; `airflow.datasets` → assets; no metadata-DB sessions in tasks; Task SDK imports (`airflow.sdk`) |
| **Dagster** 1.x | `from dagster`, `@asset`, `Definitions(` | `dagster` pin | asset checks non-blocking unless `blocking=True`; `BackfillPolicy.single_run` hands a partition **range** to one run |
| **Prefect** 2.x / 3.x | `from prefect`, `@flow`, `@task` | `prefect` pin | 3.x caching needs result persistence (off by default), so a "cached" task re-executes |
| **dbt Cloud / cron-run dbt** | job JSON, `dbt build` in a scheduler | — | the schedule's own overlap; `--full-refresh` in a schedule is `incremental-load-scan` §8 |

`ruff check --select AIR` (ruff 0.17.1, MIT, no telemetry) catches the Airflow 3 removals and moves (`AIR301`–`AIR303`); `--preview` adds `AIR304` (dynamic values in DAG arguments, which on Airflow 3 write a new DAG version per parse) and `AIR003`. Run it when installed, with `--no-cache` so nothing is written into the repo.

## Pre-flight

Run as **one** script from the repo root (bash 3.2-safe). Grep **N** feeds §N; 0 builds the orchestrator surface and reads the versions. Every `rg` names its path; include globs first, exclusions last, every exclusion `**/`-rooted; a path glob is never combined with an extension glob. Every grep ends in `ck`: rg exit 2 is a **blocked** class, never zero hits. Nothing is written outside `$OUT`.

```bash
ROOTS=(.)   # monorepo: name the orchestrator roots, e.g. ROOTS=(dags orchestration)
OUT="${OUT:-$(mktemp -d "${TMPDIR:-/tmp}/de-orch.XXXXXX")}"; mkdir -p "$OUT/none"
h() { printf '## %s\n' "$1"; }; ck() { [ "$2" -lt 2 ] || echo "$1 BLOCKED (rg exit $2) — the class is blocked, never 0 hits"; }
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.venv,venv,dbt_packages,logs}/**'
   -g '!**/{test,tests,__tests__,spec,e2e,fixtures,__fixtures__,mocks,testdata,example_dags,examples}/**'
   -g '!**/test_*.py' -g '!**/*_test.py' -g '!**/conftest.py' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*#')
LOGL=(rg -v --pcre2 '\b(?:log(?:ger|ging)?|LOG|print)\b\s*[.(]|\.(?:info|debug|warning|error|exception)\(')
# 0 THE SURFACE — 0a Airflow, 0b Dagster, 0c Prefect files; 0d versions; 0e Airflow config that restores old defaults
h 0a; rg -l --pcre2 '^\s*(?:from|import)\s+airflow\b|\bDAG\s*\(|@dag\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | tee "$OUT/AF.txt" | wc -l; ck 0a ${PIPESTATUS[0]}
h 0b; rg -l --pcre2 '^\s*(?:from|import)\s+dagster\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | tee "$OUT/DG.txt" | wc -l; ck 0b ${PIPESTATUS[0]}
h 0c; rg -l --pcre2 '^\s*(?:from|import)\s+prefect\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | tee "$OUT/PF.txt" | wc -l; ck 0c ${PIPESTATUS[0]}
cat "$OUT/AF.txt" "$OUT/DG.txt" "$OUT/PF.txt" | sort -u > "$OUT/ORCH.txt"
O=(); while IFS= read -r f; do O+=("$f"); done < "$OUT/ORCH.txt"; [ ${#O[@]} -gt 0 ] || O=("$OUT/none")
A=(); while IFS= read -r f; do A+=("$f"); done < "$OUT/AF.txt"; [ ${#A[@]} -gt 0 ] || A=("$OUT/none")
h 0d; rg -n --pcre2 '(?i)\b(?:apache-airflow|dagster|prefect)(?:\[[^\]]*\])?["\x27]?\s*(?:==|>=|~=|<=|=|\^|:)\s*["\x27]?\d+[\d.]*|apache/airflow:\d[\w.-]*|constraints-\d+\.\d+\.\d+' -g '*.{txt,in,toml,cfg,lock,yaml,yml}' -g '**/Dockerfile*' -g '!**/node_modules/**' "${ROOTS[@]}"; ck 0d $?
h 0e; rg -n --pcre2 '(?i)\bcreate_cron_data_intervals\b|\bcatchup_by_default\b|AIRFLOW__SCHEDULER__(?:CREATE_CRON_DATA_INTERVALS|CATCHUP_BY_DEFAULT)' -g '*.{cfg,ini,env,yaml,yml,toml,py,sh}' -g '**/Dockerfile*' -g '!**/node_modules/**' "${ROOTS[@]}"; ck 0e $?
# 1 OR-1 wall-clock windows — clock reads in orchestrator code and operator SQL, logging lines dropped (read: does it select data or name a partition?)
h 1; rg -n --pcre2 '\b(?:datetime\.(?:now|utcnow|today)|pendulum\.(?:now|today)|date\.today|timezone\.utcnow|time\.time)\s*\(|(?i:\bcurrent_date\b|\bcurrent_timestamp\b|\bnow\(\)|\bgetdate\(\)|\bsysdate\b)' "${O[@]}" | "${NC[@]}" | "${LOGL[@]}" | rg -v --pcre2 '\bstart_date\s*='; ck 1 ${PIPESTATUS[0]}
# 2 OR-2 parse-time work — 2a module-level calls that do I/O (AST: outside any def/lambda/class); 2b dynamic start_date or DAG arguments
h 2a; [ -s "$OUT/ORCH.txt" ] && python3 -I -B - "$OUT/ORCH.txt" <<'PY'
import ast, re, sys
IO = re.compile(r'(^|\.)(Variable\.get|get_connection|get_secret\w*|urlopen|create_engine|connect|execute|query|read_sql\w*|'
                r'read_csv|read_parquet|read_json|client|resource|listdir|scandir|glob|sleep|run|check_output)$|^(requests|httpx|boto3|'
                r'subprocess|psycopg2?|pymysql|snowflake\.connector|google\.cloud\.\w+)\.|^open$')
for path in open(sys.argv[1]).read().split('\n'):
    if not path:
        continue
    try:
        src = open(path, encoding='utf-8', errors='replace').read()
        tree = ast.parse(src)
    except (OSError, SyntaxError) as e:
        print('%s: NOT PARSED (%s) — read by hand' % (path, type(e).__name__))
        continue
    stack = list(ast.iter_child_nodes(tree))
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(node, ast.Call):
            name = ast.get_source_segment(src, node.func) or ''
            if IO.search(name) and not re.search(r'environ\.get$|getenv$', name):
                print('%s:%d: parse-time call %s(…)' % (path, node.lineno, name))
        stack.extend(ast.iter_child_nodes(node))
PY
h 2b; rg -n --pcre2 '\bstart_date\s*=\s*(?:datetime\.(?:now|utcnow|today)|pendulum\.(?:now|today)|days_ago|timezone\.utcnow|datetime\.combine\(\s*(?:date\.today|datetime\.now))|\b(?:dag_id|tags|description)\s*=\s*f["\x27][^"\x27\n]*\{(?:datetime|pendulum|time)\.' "${O[@]}" | "${NC[@]}"; ck 2b ${PIPESTATUS[0]}
# 3 OR-3 overlap and catchup — 3a concurrency > 1, catchup on, depends_on_past; 3b DAG files that never state catchup (read with the version)
h 3a; rg -n --pcre2 '\bmax_active_runs\s*[=:]\s*(?:[2-9]|\d{2,})\b|\bcatchup\s*=\s*True\b|\bdepends_on_past\b["\x27]?\s*[=:]\s*True\b' "${A[@]}" | "${NC[@]}"; ck 3a ${PIPESTATUS[0]}
h 3b; [ -s "$OUT/AF.txt" ] && tr '\n' '\0' < "$OUT/AF.txt" | xargs -0 rg -l --pcre2 '\bDAG\s*\(|@dag\b' | tr '\n' '\0' | xargs -0 -r rg --files-without-match '\bcatchup\b'
# 4 OR-4 publish regardless of upstream — trigger rules that run after a failure
h 4; rg -n --pcre2 '\btrigger_rule\s*=\s*(?:["\x27](?:all_done|none_failed\w*|always|one_success|one_done|all_skipped)["\x27]|TriggerRule\.(?:ALL_DONE|ALWAYS|NONE_FAILED\w*|ONE_SUCCESS|ONE_DONE|ALL_SKIPPED))' "${A[@]}" | "${NC[@]}"; ck 4 ${PIPESTATUS[0]}
# 5 OR-5 retries around writes — 5a retries > 0 (task, default_args, Prefect); 5b Prefect caching without persisted results
h 5a; rg -n --pcre2 '\bretries\b["\x27]?\s*[=:]\s*[1-9]' "${O[@]}" | "${NC[@]}"; ck 5a ${PIPESTATUS[0]}
h 5b; [ -s "$OUT/PF.txt" ] && tr '\n' '\0' < "$OUT/PF.txt" | xargs -0 rg -l --pcre2 '\bcache_policy\s*=|\bcache_key_fn\s*=' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bpersist_result\s*=\s*True|PREFECT_RESULTS_PERSIST_BY_DEFAULT'
# 6 OR-6 sensors with no timeout (one nesting level of parentheses read), poke mode, clock-offset dependencies
h 6; rg -n -U --pcre2 '\b\w+Sensor(?:Async)?\s*\((?:(?!\btimeout\s*=)[^()]|\((?:[^()]|\([^()]*\))*\))*\)|@task\.sensor\((?:(?!\btimeout\s*=)[^()])*\)|\bmode\s*=\s*["\x27]poke["\x27]' "${A[@]}" | "${NC[@]}"; ck 6 ${PIPESTATUS[0]}
# 7 OR-7 Airflow 3 removals (finding only when 0d pins Airflow >= 3); ruff AIR3 when installed (--no-cache: nothing written)
h 7a; rg -n --pcre2 '\{\{\s*(?:execution_date|next_execution_date|prev_execution_date(?:_success)?|tomorrow_ds\w*|yesterday_ds\w*|prev_ds\w*|next_ds\w*)\b|\bexecution_date\b|\bschedule_interval\s*=|from\s+airflow\.(?:operators\.(?:subdag|dummy\w*)|datasets|utils\.dates)\b|\b(?:SubDagOperator|DummyOperator|days_ago)\b|\bprovide_session\b|\bcreate_session\s*\(|\bsettings\.Session\b' "${A[@]}" | "${NC[@]}"; ck 7a ${PIPESTATUS[0]}
h 7b; if command -v ruff >/dev/null 2>&1 && [ -s "$OUT/AF.txt" ]; then tr '\n' '\0' < "$OUT/AF.txt" | xargs -0 ruff check --no-cache --select AIR3 --output-format concise; else echo '7b NOT-RUN (ruff absent or no Airflow file)'; fi
# 8 OR-8 zero-width interval — cron or preset schedule ∩ data_interval use ∩ no explicit interval timetable (0e can restore the AF2 default)
h 8; [ -s "$OUT/AF.txt" ] && tr '\n' '\0' < "$OUT/AF.txt" | xargs -0 rg -l --pcre2 '\bschedule\s*=\s*["\x27](?:@(?:hourly|daily|weekly|monthly|quarterly|yearly|annually)|[0-9*/,\- ]{9,})["\x27]' | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 '\bdata_interval_(?:start|end)\b' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'CronDataIntervalTimetable|create_cron_data_intervals'
# 9 OR-9 Dagster — 9a single-run backfill ∩ partition_key; 9b asset checks with no blocking=True (read: does the asset have dependants?)
h 9a; [ -s "$OUT/DG.txt" ] && tr '\n' '\0' < "$OUT/DG.txt" | xargs -0 rg -l 'BackfillPolicy\.single_run' | tr '\n' '\0' | xargs -0 -r rg -H -n --pcre2 '\bcontext\.(?:partition_key|asset_partition_key_for_output)\b'
h 9b; rg -n -U --pcre2 '@(?:multi_)?asset_check\((?:(?!\bblocking\s*=\s*True)[^()]|\([^()]*\))*\)' -g '*.py' "${X[@]}" "${ROOTS[@]}"; ck 9b $?
```

### Measured (2026-10-19)

- **Scratch sample** (three Airflow files — an Airflow 3 DAG with seeded OR-1…OR-8, an Airflow 3 decoy with an explicit `CronDataIntervalTimetable`, `catchup=False`, a pendulum literal start and a `datetime.now()` inside a log line, an Airflow 2 file with removed constructs; a Dagster file; a Prefect file; `apache-airflow==3.0.2`): under 1 s, 0 `rg` errors, `find -newer` empty. 0a 3 · 0b 1 · 0c 1. **§1** 1 (the callable's `datetime.now().date()` selecting a day; the decoy's log line is dropped by `LOGL`). **§2** 2a 1 (`Variable.get` at module level — the AST pass, which a column-0 regex misses inside `with DAG(…)` bodies); 2b 1 (`days_ago`). **§3** 3a 2 (`max_active_runs=3`, `catchup=True` in the AF2 file), 3b 1 (the AF3 DAG never states `catchup`). **§4** 1 (`all_done` publish). **§5** 5a 3 (`retries=3` on the insert task, the decoy's `retries=2` around a delete-then-insert — read and refute, the Prefect `retries=3` around a POST), 5b 1 (Prefect `cache_policy` with no persisted results). **§6** 1 (`ExternalTaskSensor` with `mode="poke"` and no timeout — one line covers both). **§7** 7a 5 (`execution_date` template, `schedule_interval`, `airflow.operators.dummy`, `days_ago` twice — the AF2 file's rows are findings only because 0d pins Airflow 3). **§8** 1 (the cron DAG that renders `data_interval_start/end`; the decoy is excluded by its timetable). **§9** 9a 1, 9b 1 (the non-blocking check; the `blocking=True` one is excluded).
- **Fixtures** (26 trees): 0 `rg` errors; 0a/0b/0c 0 on every tree — no data orchestrator in any fixture, so every § prints `N/A (no Airflow, Dagster or Prefect file)`. Application schedulers in `ds-defects`, `backend-defects` and `slow-marketplace` are backend's (§ Boundaries).
- **Real repo, read-only** (the NestJS monorepo, `ROOTS=(apps/api/src)`): 0a/0b/0c 0 — no data orchestrator; its 70 `@Cron`/`@Interval`/`@Processor` files are backend `job-lifecycle-scan`'s. **Fixture-measured only**: no real Airflow, Dagster or Prefect repo is in the program's allowed set (eval O-2).

## The 3,000-hit path

1. **Read the versions first** (0d, 0e): one Airflow pin decides every §7 row and every §8 row at once; an `airflow.cfg` with `create_cron_data_intervals = True` closes §8 repo-wide with one cited line.
2. **Group by DAG file**, then by construct: one `default_args` with `retries` covers every task that inherits it; one shared factory module that builds DAGs is one decision.
3. **Rank** DAGs that write consumed tables (marts, exports, reverse-ETL pushes) above maintenance DAGs; publish and reverse-ETL tasks first for §4/§5.
4. **Read the top 30 groups fully** (the callable, its SQL, the schedule, the interval it reads).
5. **Prefer the bulk oracle**: a DagBag import test on the pinned Airflow and one `dags test <dag> <past-date>` per DAG in a throwaway `AIRFLOW_HOME` under `$OUT` (V549) answers §1/§2/§7/§8 for every DAG in one pass.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them.

## Scans for

Severity assumes the DAG writes a table or a destination something reads. One step lower for a DAG that only notifies or cleans up. §7 is high on Airflow ≥ 3 and low on a pinned Airflow 2 (a migration note).

| § | Class (`DE-` id) | Default severity | Oracle |
|---|---|---|---|
| 1 | OR-1 task window from the wall clock | high | V549 |
| 2 | OR-2 parse-time I/O or a dynamic `start_date` / DAG argument | high | V549 |
| 3 | OR-3 overlapping runs on shared partitions; catchup implicit | medium | V550 |
| 4 | OR-4 publish runs regardless of upstream | high | V551 |
| 5 | OR-5 retries or caching around a non-idempotent write | high | V540 |
| 6 | OR-6 sensor with no timeout; clock-offset cross-DAG dependency | medium | V551 |
| 7 | OR-7 Airflow 3 removals still used | high (AF ≥ 3) / low (AF 2) | V549 |
| 8 | OR-8 Airflow 3 cron schedule + interval filter = zero-width window | high | V549 |
| 9 | OR-9 Dagster single-run backfill reading one partition key; non-blocking check on a critical asset | high | V550, V553 |

### 1. Task window from the wall clock

```
BAD:   def load(**ctx): day = datetime.now().date(); run(f"… WHERE day = '{day}'")
GOOD:  def load(data_interval_start=None, data_interval_end=None): run(sql, (data_interval_start, data_interval_end))
```
**Read the code:** Does the clock value select data, name a partition or set a file path — or only log or name a temp file (precedent § 13)? Is the task ever re-run for a past interval (backfill, clear-and-rerun, catchup)? **Finding when** the output of a run for interval I depends on when it ran. **Proof:** V549 — run the task for a past interval twice on different days (or with a frozen clock): identical output, bounded by I.

### 2. Parse-time I/O, or a dynamic `start_date`

```
BAD:   API_KEY = Variable.get("shop_api_key")                    # every parse, every scheduler loop
       DAG("orders", start_date=days_ago(1)) · dag_id=f"x_{datetime.now():%Y%m%d}"
GOOD:  read the Variable inside the task, or as a "{{ var.value.shop_api_key }}" template; start_date=pendulum.datetime(2024, 1, 1, tz="UTC")
```
**Read the code:** Is the call inside a `def` (runs at task time) or at module level, including inside a `with DAG(…)` body (runs at parse)? Does the call touch the network, a database, the metadata DB or a secrets backend? Is `start_date` or any DAG argument computed from the clock (on Airflow 3 a new DAG version per parse; on any version a moving `start_date` means runs never trigger)? Constants and imports are not this class. **Finding when** parsing the file performs I/O or produces a different DAG on each parse. **Proof:** V549 — two re-serializations produce the same DAG hash; the DagBag import test passes with the network blocked.

### 3. Overlapping runs on shared partitions; catchup implicit

**Read the code:** Do two runs of this DAG write the same table or partition (a full refresh, a delete+insert on a key not scoped to the interval)? Is `max_active_runs` > 1 (or unset with a deployment default > 1)? Is catchup stated, and is the stated value what the team needs on this major — Airflow 2 defaulted to `True` (a flood of history on unpause), Airflow 3 to `False` (silent gaps after a pause; precedent § 14)? Does order matter (`depends_on_past`)? **Finding when** two runs can interleave writes into one partition, or the version's catchup default backfills or skips intervals the team relies on. **Proof:** V550 — two overlapping runs (or a range backfill) on one partition: no duplicates, every partition written exactly once.

### 4. Publish runs regardless of upstream

```
BAD:   publish = PythonOperator(task_id="publish", …, trigger_rule="all_done")   # runs after a failed load
GOOD:  default all_success on publish; cleanup tasks keep all_done
```
**Read the code:** Is the task downstream of a load or transform, and does it publish (reverse-ETL, a file to a partner, a cache swap, a dashboard refresh, a notification that numbers are ready)? A cleanup or alert task with `all_done` is correct. **Finding when** a failed upstream lets a publish run on stale or partial data. **Proof:** V551 — fail the upstream in a test run: the publish is skipped.

### 5. Retries or caching around a non-idempotent write

**Read the code:** What does the retried callable write (an `INSERT` without a conflict clause, `to_sql(append)`, a POST without an idempotency key, a message publish)? Does a failure after the write and before success trigger the retry? Does `incremental-load-scan` §2 already rate the write idempotent (then this is refuted with that row cited)? For Prefect 3, does a `cache_policy` rely on results that are not persisted? A side effect keyed by an idempotency key is not this class. **Finding when** a retry or a cache miss repeats a side effect. **Proof:** V540 — inject a failure after the write; retry; count the side effects (one).

### 6. Sensors with no timeout; dependencies by clock offset

**Read the code:** Does every sensor set `timeout` (and `mode="reschedule"` or a deferrable variant for long waits, so it does not hold a worker slot)? Does a DAG depend on another by scheduling an hour later instead of a sensor, an asset or a dataset trigger? **Finding when** an upstream that never arrives holds a slot forever or lets the downstream run on stale data. **Proof:** V551 — the sensor's upstream never arrives: the sensor times out and alerts; the downstream does not run.

### 7. Airflow 3 removals still used

**Read the code:** Which Airflow does 0d pin? On ≥ 3: `execution_date` and the yesterday/tomorrow/prev/next `ds` templates, `schedule_interval=`, `SubDagOperator`, `DummyOperator`, `days_ago`, `airflow.datasets`, metadata-DB sessions inside tasks (`provide_session`, `settings.Session`). On a pinned Airflow 2 the same rows are a migration note (low). Prefer `ruff --select AIR3` output (7b) where installed. **Finding when** the pinned version no longer provides the construct. **Proof:** V549 — the DagBag import test on the pinned version reports no import error, and the task renders.

### 8. Cron schedule + interval filter = a zero-width window

```
BAD:   DAG("orders", schedule="0 2 * * *")  +  WHERE updated_at >= '{{ data_interval_start }}' AND updated_at < '{{ data_interval_end }}'
GOOD:  schedule=CronDataIntervalTimetable("0 2 * * *", timezone="UTC")  — or filter on [logical_date - 1 day, logical_date)
```
**Read the code:** Is Airflow ≥ 3 pinned, and is `create_cron_data_intervals` left at its new default (0e)? Does the schedule string map to `CronTriggerTimetable` on that version (a cron string does; read the installed version's docs for a preset)? Does any template or callable bound its read by `data_interval_start`/`data_interval_end`? An explicit `CronDataIntervalTimetable` is the control. **Finding when** the rendered interval is zero-width and the task's read is bounded by it — it reads no rows and succeeds. **Proof:** V549 — render one run's templates: `data_interval_end > data_interval_start`.

### 9. Dagster: single-run backfill and non-blocking checks

**Read the code:** Under `BackfillPolicy.single_run()`, a backfill hands one run a **range** of partitions; does the asset read `context.partition_key` (one key) instead of the partition key range or time window? For each `@asset_check` without `blocking=True`, does the checked asset have downstream assets that consume bad data when the check fails (precedent § 3 keeps advisory checks)? **Finding when** a range backfill processes one partition, or a failed check lets a critical asset feed its dependants. **Proof:** V550 — materialize a three-partition range: three partitions written; V553 — a failing check stops the downstream materialization.

## Output

```
orchestration-scan — lanes: airflow 3.0.2 (requirements.txt:1), dagster 1.9.3, prefect 3.1.0; create_cron_data_intervals: default
Surface: 3 Airflow files · 1 Dagster · 1 Prefect

Findings: 3 · Unconfirmed: 2

1. dags/orders_dag.py:16                                          [report-with-fix]   high
   §8 OR-8 — schedule "0 2 * * *" on Airflow 3.0.2 with no interval timetable; the transform reads
   [data_interval_start, data_interval_end). V549: rendered interval 2026-10-18T02:00 → 2026-10-18T02:00, 0 rows, success.
   Fix: schedule=CronDataIntervalTimetable("0 2 * * *", timezone="UTC").
2. dags/orders_dag.py:7                                           [report-with-fix]   high
   §2 OR-2 — Variable.get at module level: a secrets-backend call on every parse. Fix: "{{ var.value.shop_api_key }}".
3. dags/orders_dag.py:23                                          [report-with-fix]   high
   §4 OR-4 — publish with trigger_rule all_done after load and transform. V551: load failed, publish ran.
4. dags/orders_dag.py:10                                          [report-flagged]    high
   §1 OR-1 — the load selects `day = datetime.now().date()`. Unproven link: whether the DAG is ever backfilled. Settling: V549.
5. dags/orders_dag.py:18                                          [report-flagged]    high
   §5 OR-5 — retries=3 around an INSERT…SELECT with no conflict clause (incremental-load-scan §2 row 2b). Settling: V540.

Verification: 19 candidates → 3 findings · 2 unconfirmed · 4 hardening · 10 refuted (self-verified; precedents § 13, § 14, § 3)

Class coverage:
  §1 wall clock        checked (1 → 1 unconfirmed)
  §2 parse-time I/O    checked (2a 1 + 2b 1 → 1 finding; days_ago in the AF2 file → §7)
  §3 overlap/catchup   checked (3a 2 + 3b 1 → hardening: one run per partition, delete-then-insert by ds)
  §4 trigger rules     checked (1 → 1 finding)
  §5 retries           checked (5a 3 + 5b 1 → 1 unconfirmed; the decoy deletes the interval first)
  §6 sensors           checked (1 → hardening: the upstream DAG is a 5-minute job; timeout added as advice)
  §7 AF3 removals      checked (7a 5 → 0 findings in deployed DAGs; af2_dag.py is not mounted — read the compose volume)
  §8 zero-width        checked (1 → 1 finding)
  §9 Dagster           checked (9a 1 + 9b 1 → refuted: orders has no dependants yet — advisory)
```

`[report-with-fix]`: the oracle failed (a rendered interval, a test run with the upstream failed, a reserialization diff) or the fact is two-ended with the version pin quoted, and the fix is local to the DAG, the asset or the flow. `[report-flagged]`: one link is unproven (whether backfills happen, the deployment's mounted folder, the side effect's idempotency); the row names it and the settling oracle. The coverage block lists **all nine** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep>: rg exit 2)`, `→ <owner> (k)` or `Live, unreviewed (k)`.

## False positives / precedents

The verifier reads [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- § 13 `datetime.now()` for logging or a temp name; § 14 no `catchup=` on Airflow 3 (flips back when the team needs backfills, or on Airflow 2); § 3 a non-blocking check that is advisory.
- A delete-then-insert keyed on the run's own interval makes a retry or an overlap idempotent (§5 and §3 refute with the line cited).

## When to run

- On any diff that touches a DAG, asset, flow, `default_args`, a sensor, `airflow.cfg`, the orchestrator pin or its image tag — `/audit-data-quality`'s orchestration signal; before and after an Airflow 2 → 3 upgrade (with `/upgrade-dep`).
- On every whole-repo `/audit-data-quality`, reporting all nine §s.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets the version pin, the `file:line` and the run that breaks — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) §1–§8 with [`precedents/data-engineering.md`](../../../../snippets/precedents/data-engineering.md). Under `/audit-data-quality` that is `@dag-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`.
- **Halt before §7 and §8 when no version pin is read**: they print `[report-flagged]` with the missing pin, never a verdict from what Airflow "usually" is.
- **Never trigger, clear, backfill or unpause a DAG on a shared or production Airflow, and never run a Dagster or Prefect job against production resources.** Oracles run in a throwaway environment: `AIRFLOW_HOME="$OUT/airflow"` (Airflow writes its home on import), `AIRFLOW__CORE__LOAD_EXAMPLES=False`, `DO_NOT_TRACK=1` and `SCARF_ANALYTICS=false` set defensively (no usage-data option was found in the 3.3 configuration reference, fetched 2026-10-19), no connections to real systems. Whether the Airflow 3 DagBag import needs a metadata DB is UNVERIFIED; a test that cannot be isolated is `NOT-RUN`.
- **This skill writes nothing into the audited repo**; `ruff` runs with `--no-cache`. `find <root> -newer "$OUT"` is empty at the end; a fix is `/data-fix`'s.
- **No `[report-with-fix]` without the V-oracle failing** or a two-ended static fact (the pin and the construct). **Do not grade application schedulers** (§ Boundaries). **Do not print "the DAGs look fine"** without the coverage block.

## Related

- `/audit-data-quality` dispatches this skill; `@dag-reviewer` judges OR rows; `/data-fix` closes them; `/upgrade-dep` owns an Airflow major upgrade and reads §7/§8 as its parity list.
- This pack: `incremental-load-scan` (the write a retry replays; backfill shapes), `data-test-scan` (checks that cannot fail).
- backend `job-lifecycle-scan`, distributed-systems `coordination-scan`, when those packs are installed.

## Sources

From the data-engineering research (2026-10-19): Airflow "Upgrading to Airflow 3", best practices and FAQ (3.3.2 docs, Apache-2.0); apache-airflow 3.3.2 on PyPI (2026-09-17); ruff AIR rules and AIR304 (ruff 0.17.1, 2026-10-15, MIT); Dagster asset checks and backfills (1.13.26 docs); Prefect 3 caching. Airflow configuration reference 3.3 fetched 2026-10-19 for the telemetry note. Class ids DE-A-10…19 as catalogued there. Counts are from read-only runs of the block above. Paraphrased; no text reproduced beyond identifiers.
