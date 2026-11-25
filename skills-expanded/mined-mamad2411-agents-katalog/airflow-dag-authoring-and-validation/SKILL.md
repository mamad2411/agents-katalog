---
name: airflow-dag-authoring-and-validation
description: >
  Authors Apache Airflow DAGs — task dependencies, operator choice,
  sensors, idempotency — and validates them with `airflow dags test`,
  import-time checks, and DAG linting before they reach a production
  scheduler. Use when the user asks to "write an Airflow DAG," "add a
  task dependency," "use a sensor to wait for a file/table," "validate a
  DAG before deploying it," "lint an Airflow DAG," or reviews a DAG file
  for correctness before merge.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Airflow DAG Authoring and Validation

## Purpose

An Airflow DAG file is Python that runs on every scheduler heartbeat (to
parse the DAG structure) in addition to running each task at execution
time — a slow, broken, or non-idempotent DAG file causes problems long
before any task actually fails, by slowing down or breaking DAG parsing
across the whole scheduler. This skill covers writing DAGs that are
correct, idempotent, and fast to parse, and validating them with
`airflow dags test` and lint-style checks before they reach a production
scheduler — diagnosing a DAG that's already stuck or a scheduler that's
already unhealthy in production is covered separately in
[airflow-scheduler-and-dag-troubleshooting](../airflow-scheduler-and-dag-troubleshooting/SKILL.md).

## When to use

- Writing a new Airflow DAG: defining task dependencies, choosing
  operators, adding sensors that wait on an external condition.
- Reviewing a DAG file (in a pull request or otherwise) before it's
  deployed to a scheduler that other teams' DAGs also run on.
- Validating a DAG runs correctly end-to-end for a specific logical date
  before relying on the scheduler to pick it up.
- Refactoring an existing DAG to remove top-level code that shouldn't run
  at parse time, or to fix non-idempotent tasks.
- Setting up a CI gate that validates every DAG file before merge.

## Prerequisites & environment

- Apache Airflow 2.x (this skill uses the TaskFlow API and operator
  patterns current in Airflow 2; DAG authoring changed substantially from
  Airflow 1.x, and some syntax here — e.g. `@task` decorators — isn't
  available before 2.0).
- A local or CI-accessible Airflow environment (even a minimal
  `airflow standalone` or the `astro` / `docker compose` based local
  dev setups most distributions provide) to actually run `airflow dags
  test`, not just visually review the DAG file.
- Access to whatever the DAG's tasks actually depend on in a test/staging
  form (a connection ID configured for a test database, a mock/staging
  API endpoint) — `airflow dags test` executes real task logic, so it
  needs real (or safely mocked) dependencies to be a meaningful check, not
  just a syntax check.
- Familiarity with the DAG's intended schedule and whether backfill
  behavior is expected — this affects `catchup` and `start_date` choices
  made during authoring (see step 6).

## Step-by-step guidance

1. **Keep all top-level DAG-file code cheap and side-effect-free** —
   anything at module level runs on every scheduler parse cycle, not just
   when the DAG actually executes:
   ```python
   from airflow.decorators import dag, task
   from datetime import datetime, timedelta

   # BAD: a network call or heavy computation at module level runs on
   # every DAG-file parse, for every scheduler heartbeat, for every DAG
   # file in the DAGs folder — this is a scheduler-health issue waiting
   # to happen, not just this DAG's problem.
   # config = requests.get("https://config-service/orders-dag-config").json()

   # GOOD: defer any external call to inside a task, which only runs when
   # the DAG actually executes.
   @dag(
       schedule="@daily",
       start_date=datetime(2024, 1, 1),
       catchup=False,
       default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
       tags=["orders"],
   )
   def orders_daily_rollup():
       @task
       def fetch_config():
           import requests
           return requests.get("https://config-service/orders-dag-config").json()

       fetch_config()

   orders_daily_rollup()
   ```

2. **Express task dependencies explicitly and readably**, using either
   the `>>`/`<<` bitshift operators or TaskFlow's automatic dependency
   inference from function calls passing data between tasks:
   ```python
   @task
   def extract():
       ...

   @task
   def transform(raw):
       ...

   @task
   def load(transformed):
       ...

   load(transform(extract()))
   ```
   For non-TaskFlow (classic operator) DAGs, prefer explicit `>>` chains
   over relying on definition order, which is easy to misread once a DAG
   has more than a handful of tasks:
   ```python
   extract_task >> transform_task >> load_task
   transform_task >> [validate_task, notify_task]
   ```

3. **Choose the operator that matches what the task actually does**, not
   the most familiar one. A `PythonOperator`/`@task` for arbitrary Python
   logic; a provider-specific operator (`BigQueryInsertJobOperator`,
   `S3ToRedshiftOperator`, `KubernetesPodOperator`, etc.) when one exists
   for the target system, since it typically handles retries,
   connections, and templating more correctly than a hand-rolled Python
   call to the same API:
   ```python
   from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

   run_query = BigQueryInsertJobOperator(
       task_id="run_daily_rollup_query",
       configuration={"query": {"query": "{% include 'sql/daily_rollup.sql' %}", "useLegacySql": False}},
   )
   ```
   A `KubernetesPodOperator`/`DockerOperator` is often the right choice
   when a task's actual logic lives in another language/runtime or needs
   isolation from the scheduler's own Python environment, rather than
   forcing everything through a `PythonOperator` shelling out to a
   subprocess.

4. **Use a sensor (or the deferrable/async equivalent) to wait on an
   external condition, with an explicit timeout and reasonable poke
   interval** — never poll in a tight loop inside a `PythonOperator`:
   ```python
   from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

   wait_for_upstream_file = S3KeySensor(
       task_id="wait_for_upstream_export",
       bucket_name="upstream-exports",
       bucket_key="orders/{{ ds }}/export.parquet",
       poke_interval=300,
       timeout=60 * 60 * 6,
       mode="reschedule",
   )
   ```
   `mode="reschedule"` releases the worker slot between pokes (the sensor
   task goes back to `up_for_reschedule` instead of holding a worker slot
   the entire wait) — use this for anything that might wait more than a
   few minutes; `mode="poke"` holds a worker slot for the whole wait,
   which at scale can exhaust worker capacity with sensors doing nothing
   but waiting. Always set an explicit `timeout` so a sensor that never
   sees its condition fails visibly instead of waiting forever.

5. **Make every task idempotent — safe to re-run for the same logical
   date without corrupting state** — since retries, backfills, and manual
   re-runs all mean a task may execute more than once for the same
   `data_interval`:
   ```python
   @task
   def load_daily_rollup(ds=None):
       # idempotent: overwrite/replace the partition for this date rather
       # than blindly appending, so re-running for the same `ds` produces
       # the same result instead of duplicate rows
       run_sql(f"""
           DELETE FROM orders_daily_rollup WHERE rollup_date = '{ds}';
           INSERT INTO orders_daily_rollup
           SELECT '{ds}' AS rollup_date, COUNT(*), SUM(amount_cents)
           FROM orders WHERE DATE(created_at) = '{ds}';
       """)
   ```
   An `INSERT`-only task that doesn't first delete/overwrite the target
   partition produces duplicate data on any retry or backfill —
   idempotency is the single most important property to review for in a
   DAG, more so than the specific operator or scheduling syntax used.

6. **Set `start_date`, `schedule`, and `catchup` deliberately, understanding
   their interaction before deploying**:
   ```python
   @dag(
       schedule="@daily",
       start_date=datetime(2024, 1, 1),
       catchup=False,  # do not automatically backfill every interval since start_date
   )
   ```
   `catchup=True` (the historical default in older Airflow versions —
   check the deployed version's actual default rather than assuming) runs
   one DAG run for *every* schedule interval between `start_date` and now
   the moment the DAG is first deployed/unpaused — for a `start_date` set
   a year in the past on a daily schedule, that's 365 backfill runs firing
   immediately, which is rarely the intended behavior for a newly
   authored DAG. Set `catchup=False` explicitly unless historical backfill
   on first deploy is genuinely wanted.

7. **Validate the DAG with `airflow dags test` before merging**, which
   runs every task in the DAG for a specific logical date synchronously,
   surfacing real task failures (not just import errors):
   ```bash
   airflow dags test orders_daily_rollup 2024-06-01
   ```
   This is a stronger check than just confirming the file imports without
   error — it actually executes task logic (against whatever connections/
   variables are configured in the test environment), so it catches
   runtime failures a pure syntax/import check would miss. Follow with an
   explicit DAG-structure lint step (see step 8) for issues
   `dags test` alone won't catch, like top-level side effects or missing
   `catchup` settings.

8. **Add a DAG-linting CI step** that checks for the structural issues
   most likely to cause scheduler-health problems, not just Python
   syntax errors:
   ```bash
   # confirm the file parses without raising, and check parse time
   time python -c "from airflow.models import DagBag; db = DagBag(dag_folder='dags/', include_examples=False); \
     assert not db.import_errors, db.import_errors"
   ```
   A DAG file taking more than a second or two to parse is worth
   investigating for accidental top-level work (step 1) — scheduler
   parse time scales with every DAG file in the folder, so one slow file
   affects the whole deployment, not just its own DAG. Tools like Astronomer's
   `astro dev` linting, or a custom script asserting every DAG has
   `catchup` set explicitly and every task has `retries` configured, can
   be added to the same CI gate.

## Best practices

- Never put a network call, database query, or heavy computation at DAG
  *file* top level — only inside a task/operator, so it runs at task
  execution time, not on every scheduler parse cycle.
- Make every task idempotent for its logical date/`data_interval` —
  overwrite-by-partition instead of append-only writes for anything that
  might retry, backfill, or be manually re-run.
- Prefer provider-specific operators over hand-rolled `PythonOperator`
  calls to the same external system when a well-maintained operator
  exists — they typically handle retries, connection management, and
  Jinja templating more correctly.
- Use `mode="reschedule"` for any sensor that might wait more than a few
  minutes, and always set an explicit `timeout`.
- Set `catchup=False` explicitly on new DAGs unless historical backfill on
  first deploy is a deliberate, reviewed decision — don't rely on
  whatever the deployed Airflow version's default happens to be.
- Run `airflow dags test` for a representative logical date as part of
  code review or CI, not just a DAG-parses-without-error check — it
  catches real task-logic failures that an import check can't.
- Keep DAG files small and focused; a DAG that grows to dozens of loosely
  related tasks is harder to reason about for dependency correctness and
  slower to parse than several smaller, clearly-scoped DAGs.

## Common pitfalls

- **Symptom:** A DAG deployed for the first time immediately triggers
  dozens or hundreds of DAG runs back-to-back instead of just running for
  "today."
  **Fix:** `catchup` defaulted to `True` (or was left unset and the
  deployed Airflow version's default is `True`) with a `start_date` far in
  the past. Set `catchup=False` explicitly, and if genuine historical
  backfill is needed, run it deliberately and separately via `airflow
  dags backfill` with an explicit date range (see the destructive-action
  warning on backfill in
  [airflow-scheduler-and-dag-troubleshooting](../airflow-scheduler-and-dag-troubleshooting/SKILL.md)),
  not by accident on first deploy.

- **Symptom:** A task retried after a transient failure produces duplicate
  rows in the target table, or a backfill for a past date corrupts data
  for dates that were already correct.
  **Fix:** The task isn't idempotent — it appends rather than
  overwriting its target partition/rows for the given logical date.
  Rewrite the task to delete-then-insert (or `MERGE`/upsert) scoped to
  the specific `data_interval`/`ds` being processed, so re-running it
  produces the same end state rather than accumulating duplicates.

- **Symptom:** Scheduler CPU/parse latency across the *entire* Airflow
  deployment degrades noticeably after one particular DAG file is added,
  and every DAG's scheduling becomes sluggish, not just the new one.
  **Fix:** Check the new DAG file for top-level code doing real work (a
  database query, an API call, a large in-memory computation) — this
  runs on every scheduler parse cycle for every DAG file in the folder,
  so one badly-written DAG file degrades scheduling for all DAGs, not
  just its own. Move any such work inside a task.

- **Symptom:** A sensor task holds its worker slot for hours while waiting
  on an upstream file/condition, and other tasks queue up behind it
  unable to get a worker.
  **Fix:** The sensor is running in the default `mode="poke"`, which
  occupies a worker slot for its entire wait duration. Switch to
  `mode="reschedule"` so the sensor releases its slot between poke
  attempts, and set an explicit `timeout` so a condition that never
  arrives fails the task visibly instead of waiting indefinitely.

## Worked example

**Scenario:** Authoring a new `orders_daily_rollup` DAG that waits for an
upstream export file to land in object storage, then computes and loads a
daily rollup table, idempotently, once per day.

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor


@dag(
    dag_id="orders_daily_rollup",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)},
    tags=["orders", "rollup"],
)
def orders_daily_rollup():
    wait_for_export = S3KeySensor(
        task_id="wait_for_upstream_export",
        bucket_name="upstream-exports",
        bucket_key="orders/{{ ds }}/export.parquet",
        poke_interval=300,
        timeout=60 * 60 * 6,
        mode="reschedule",
    )

    @task
    def compute_rollup(ds=None):
        # idempotent: replaces the partition for `ds`, safe to retry/backfill
        run_sql(f"""
            DELETE FROM orders_daily_rollup WHERE rollup_date = '{ds}';
            INSERT INTO orders_daily_rollup
            SELECT '{ds}' AS rollup_date, COUNT(*), SUM(amount_cents)
            FROM staging_orders_export WHERE rollup_date = '{ds}';
        """)

    @task
    def notify_downstream(ds=None):
        publish_completion_event(rollup_date=ds)

    wait_for_export >> compute_rollup() >> notify_downstream()


orders_daily_rollup()
```

Validation before merge:
```bash
$ airflow dags test orders_daily_rollup 2024-06-01
```
This runs `wait_for_upstream_export` against the actual (test-environment)
S3 bucket, then `compute_rollup` and `notify_downstream` for logical date
`2024-06-01`, surfacing any real failure (e.g. the SQL referencing a
column that doesn't exist in the staging table) rather than only
confirming the DAG file imports cleanly. A DAG-lint CI step separately
confirms `catchup` is set explicitly and no top-level code performs I/O,
before the DAG is approved for the shared production scheduler.

## Cross-references

- [airflow-scheduler-and-dag-troubleshooting](../airflow-scheduler-and-dag-troubleshooting/SKILL.md) — diagnosing a stuck/failed run or scheduler-health issue once this DAG is running in production, including the destructive-action risks of `airflow dags backfill`.
- [dagster-and-prefect-pipeline-authoring](../dagster-and-prefect-pipeline-authoring/SKILL.md) — an asset-based alternative worth considering for new pipelines before committing to Airflow's task-based model.
- [kafka-configuration-validation](../kafka-configuration-validation/SKILL.md) — a comparable pre-production validation gate (config/topology checked before go-live) for the messaging side of a pipeline this DAG might consume from or publish to.
