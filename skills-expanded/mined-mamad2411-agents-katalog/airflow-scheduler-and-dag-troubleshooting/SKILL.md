---
name: airflow-scheduler-and-dag-troubleshooting
description: >
  Diagnoses a stuck or failed Airflow DAG run, scheduler-health problems
  (slow parsing, stuck queued tasks), and plans safe task-retry/backfill
  strategy. Use when the user reports "Airflow DAG is stuck," "task stuck
  in queued state," "scheduler seems unhealthy," "DAG run failed and I
  need to retry it," "should I backfill this DAG," or asks to
  troubleshoot a live Airflow production incident.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Airflow Scheduler and DAG Troubleshooting

## Purpose

A DAG run that's stuck, a task frozen in `queued` state, or a scheduler
that's silently falling behind on parsing/scheduling are among the most
common live Airflow incidents, and they can look similar from the outside
("nothing is running") while having very different root causes and fixes
— a genuinely unhealthy scheduler process, a worker/executor capacity
problem, or a single DAG's bad task logic. This skill is the diagnostic
playbook for telling those apart and choosing a retry/backfill strategy
that doesn't make things worse, building on the authoring practices
(idempotency, sensor mode, `catchup` behavior) covered in
[airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)
rather than re-deriving them.

## When to use

- A DAG run appears stuck — no tasks progressing, state unchanged for
  longer than expected.
- A specific task is stuck in `queued` (or `scheduled`) state and never
  transitions to `running`.
- The scheduler itself seems unhealthy: DAG runs aren't being created on
  schedule, or there's a growing gap between a DAG's expected next-run
  time and when it actually fires.
- Deciding whether and how to retry a failed task or DAG run, or whether a
  backfill is safe given the DAG's task idempotency.
- Investigating a paging alert tied to DAG SLA misses, scheduler heartbeat
  metrics, or executor/worker queue depth.

## Prerequisites & environment

- Access to the Airflow webserver UI (Grid/Graph view, task instance
  logs) and, ideally, the scheduler/worker logs directly (not just what
  surfaces in the UI) — some scheduler-level problems (e.g. a DAG file
  raising an intermittent import error) show up in scheduler logs before
  they show up as a visibly stuck task in the UI.
- CLI access (`airflow tasks state`, `airflow dags state`,
  `airflow celery`/`airflow kubernetes` subcommands depending on
  executor) or equivalent read access to the metadata database.
- Knowledge of the deployed executor (`CeleryExecutor`,
  `KubernetesExecutor`, `LocalExecutor`) — the diagnostic steps for a
  stuck-in-queued task differ meaningfully by executor, since the reason a
  task can't move from `queued` to `running` depends on what's actually
  responsible for picking it up (a Celery worker pool vs. the Kubernetes
  API scheduling a pod).
- Familiarity with the specific DAG's task idempotency (established per
  [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md))
  before deciding on a retry or backfill strategy — retrying a
  non-idempotent task is itself a risk, not a safe default action.

## Step-by-step guidance

1. **Check scheduler health first, independent of any specific DAG** —
   a DAG that looks "stuck" is sometimes actually healthy, just waiting
   behind a struggling scheduler:
   ```bash
   airflow jobs check --job-type SchedulerJob --hostname <scheduler-host>
   ```
   Also check the scheduler's own heartbeat/latency metrics if exported
   (`scheduler_heartbeat`, DAG parse duration) and, in the UI, whether
   *other* DAGs are also failing to progress at their expected pace — if
   many unrelated DAGs are all behind schedule simultaneously, this points
   at a scheduler-wide problem (parsing backlog, resource starvation on
   the scheduler host), not an issue specific to the DAG being
   investigated.

2. **If only one DAG is affected, check for a DAG-file import error
   first** — the scheduler silently stops updating a DAG whose file fails
   to import, which looks like "this DAG stopped running" without an
   obvious error in the DAG-run history itself:
   ```bash
   airflow dags list-import-errors
   ```
   An import error here (e.g. a bad Jinja template reference, a Python
   exception from a top-level call the way
   [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)
   warns against) means the scheduler literally cannot see the current
   version of the DAG — it keeps serving/scheduling the last successfully
   parsed version (or nothing, if it's a new DAG) until the import error
   is fixed. This is a very common cause of "the DAG I just edited isn't
   picking up my changes."

3. **For a task stuck in `queued`, check what's actually responsible for
   picking it up, based on executor**:
   ```bash
   # CeleryExecutor: check worker pool capacity and queue routing
   airflow celery flower  # or: check active/reserved task counts on workers
   # KubernetesExecutor: check whether a pod was ever actually scheduled
   kubectl get pods -n airflow -l dag_id=orders_daily_rollup
   ```
   - `CeleryExecutor`: a task can sit in `queued` indefinitely if the
     worker pool is fully occupied by other tasks (check
     `parallelism`/`worker_concurrency` against actual worker count) or if
     the task was queued to a specific queue name no active worker is
     listening on.
   - `KubernetesExecutor`: check whether a pod was ever created for the
     task — if not, this is a scheduler-to-Kubernetes-API problem
     (permissions, resource quota); if a pod exists but is `Pending`,
     it's a cluster-capacity/scheduling problem (insufficient node
     resources, an unsatisfiable node selector/toleration), not an
     Airflow-level issue at all.

4. **Check `pool` and `max_active_tasks`/`max_active_runs` settings** if
   tasks are queued but concurrency limits — not raw worker capacity —
   are the actual constraint:
   ```python
   @dag(
       max_active_runs=1,       # only one run of this DAG in flight at a time
       max_active_tasks=8,      # cap on concurrent task instances for this DAG
   )
   ```
   A DAG with `max_active_runs=1` deliberately queues a new run behind an
   already-running one — this is often intentional (to avoid two runs of
   a non-parallelizable pipeline overlapping) but can look like "the DAG
   is stuck" to someone unaware of the setting. Confirm whether the
   constraint is intentional before treating it as a bug.

5. **For a genuinely failed task, read the actual task instance log before
   deciding on a retry** — Airflow surfaces the task's exit state in the
   UI, but the log has the real error:
   ```bash
   airflow tasks logs orders_daily_rollup compute_rollup 2024-06-01
   ```
   Distinguish a transient failure (a timeout calling a flaky downstream
   API, a brief database connection blip — safe to retry as-is) from a
   deterministic failure (a bug in the task's logic, bad input data for
   that specific date — retrying without a code/data fix will fail
   identically every time, just delaying the real fix).

6. **Retry a failed task only after confirming its idempotency**, using
   the UI's "clear" action or the CLI, scoped as narrowly as possible:
   ```bash
   airflow tasks clear orders_daily_rollup -t compute_rollup \
     -s 2024-06-01 -e 2024-06-01
   ```
   Clearing re-queues the task for re-execution. This is safe for an
   idempotent task (per
   [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)'s
   overwrite-by-partition guidance) but can duplicate side effects (a
   sent notification, an append-only insert, a charged payment) for a
   task that isn't idempotent — confirm the task's actual behavior on
   re-run before clearing it, not after.

7. **Treat `airflow dags backfill` as a destructive/dangerous action
   requiring the same care as a bulk data-mutation** — it re-runs a
   DAG for a date range, re-executing every task's logic for each date in
   that range:
   ```bash
   # WARNING: this re-runs every task for every date in the range.
   # Confirm every task in the DAG is idempotent for the given dates
   # before running this — a non-idempotent task (e.g. one that sends
   # a notification or appends rather than overwrites) will re-trigger
   # that side effect for every date being backfilled.
   airflow dags backfill orders_daily_rollup \
     -s 2024-05-01 -e 2024-05-07
   ```
   Before running a backfill: confirm every task is idempotent for the
   date range (a task that overwrites-by-partition is safe; one that
   sends a customer notification or calls a non-idempotent external API
   is not, and needs a dry-run flag or a temporary bypass for those steps
   during backfill); confirm downstream consumers of this DAG's output
   can tolerate a burst of re-processed historical data; and prefer a
   narrow, explicit date range over an open-ended one. If any task sends
   real-world side effects (emails, payments, external API calls with
   effects), either exclude those tasks from the backfill run (e.g. via
   `-t`/task regex exclusion, if the executor/version supports it) or
   temporarily gate them behind a "backfill mode" flag/environment
   variable checked at task run time.

8. **For a repeatedly-failing task, check retry/backoff configuration
   before assuming manual intervention is the only path**:
   ```python
   default_args = {
       "retries": 3,
       "retry_delay": timedelta(minutes=5),
       "retry_exponential_backoff": True,
       "max_retry_delay": timedelta(minutes=30),
   }
   ```
   A task that's failing due to a transient, time-bound issue (a
   downstream service's brief outage) may resolve itself within the
   configured retry window without manual action — check whether
   automatic retries are still in progress before manually clearing/
   re-triggering, since doing so mid-retry can be redundant or, for a
   non-idempotent task, actively harmful (see step 6).

## Best practices

- Diagnose scheduler-wide health (step 1) before diving into a specific
  DAG's symptoms — a DAG that looks broken is sometimes just waiting
  behind a scheduler-level problem affecting everything.
- Check `airflow dags list-import-errors` early in any "this DAG isn't
  updating/running" investigation — it's a fast check that rules out (or
  confirms) one of the most common causes.
- Never clear or retry a task without first checking whether it's
  idempotent — a "safe-looking" retry can duplicate a side effect for a
  task that appends rather than overwrites.
- Treat `airflow dags backfill` as requiring the same sign-off rigor as
  any bulk production data operation — confirm task idempotency and
  downstream tolerance for reprocessed data before running it, and prefer
  the narrowest date range that satisfies the actual need.
- Alert on DAG-file import errors and on scheduler heartbeat/parse-latency
  metrics directly, not only on individual task failures — these
  scheduler-level signals often precede or explain a wave of
  DAG-specific symptoms.
- Match diagnostic steps to the actual executor in use (`CeleryExecutor`
  vs. `KubernetesExecutor`) rather than applying Celery-specific
  troubleshooting to a Kubernetes-executor deployment or vice versa.

## Common pitfalls

- **Symptom:** A DAG "stopped running" after a recent edit, with no error
  visible in the DAG-run history because there simply are no new runs.
  **Fix:** Check `airflow dags list-import-errors` first — the DAG file
  almost certainly fails to import after the edit, and the scheduler
  can't create new runs for a DAG it can't parse. Fix the import error
  (often a Python exception in top-level code, per
  [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md))
  rather than looking for a scheduling-configuration problem.

- **Symptom:** A task sits in `queued` state for a long time on a
  `CeleryExecutor` deployment, and restarting the scheduler doesn't help.
  **Fix:** Check actual worker capacity and queue routing, not scheduler
  health — this is very often the worker pool being fully occupied by
  other tasks, or the task being queued to a named queue (`queue=` on
  the operator) that no currently-running worker is configured to
  consume from. Restarting the scheduler doesn't add worker capacity or
  fix a queue-routing mismatch.

- **Symptom:** An on-call engineer clears/retries a failed task to
  "unblock the pipeline," and a duplicate customer notification (or
  duplicate row, or duplicate charge) results.
  **Fix:** The task wasn't idempotent, and clearing it re-executed a side
  effect that isn't safe to repeat. Before ever clearing a failed task,
  check what it actually does on re-run — this is exactly the idempotency
  property [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)
  calls out as the most important thing to get right at authoring time,
  and its absence is what makes incident response risky rather than
  routine.

- **Symptom:** Someone runs `airflow dags backfill` for a multi-week date
  range to "regenerate historical data," and it re-sends every
  notification email and re-calls every non-idempotent external API for
  every day in that range.
  **Fix:** **This is a destructive action when tasks aren't fully
  idempotent, and the range should never be run without first confirming
  every task's behavior on re-run.** Before backfilling: identify any task
  with a real-world side effect (notifications, payments, non-idempotent
  API calls), exclude or gate those tasks for the backfill run, and
  backfill the narrowest date range that actually satisfies the need
  rather than an open-ended or "just to be safe, do the whole quarter"
  range.

## Worked example

**Scenario:** On-call is paged because the `orders_daily_rollup` DAG (from
[airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)'s
worked example) hasn't produced a new DAG run in over 24 hours, and the
on-call engineer's first assumption is "the scheduler is down."

Step 1 — scheduler health:
```bash
$ airflow jobs check --job-type SchedulerJob --hostname scheduler-1
Found one alive job.
```
The scheduler itself is healthy and other DAGs are running on schedule —
this rules out a scheduler-wide problem and narrows the investigation to
this one DAG.

Step 2 — import errors:
```bash
$ airflow dags list-import-errors
filepath                          error
dags/orders_daily_rollup.py       ModuleNotFoundError: No module named 'orders_utils'
```
A recent commit added a helper import (`orders_utils`) that isn't
installed in the scheduler's Python environment. The scheduler has been
silently failing to parse this DAG file since that deploy — there are no
new DAG runs because the scheduler literally can't see an up-to-date,
importable version of the DAG, which explains the "stopped running"
symptom far better than a scheduler outage would.

Fix: revert the dependency-adding commit (or fix the deployment's
dependency installation step) so the file imports cleanly again, verified
with:
```bash
$ python -c "from airflow.models import DagBag; db = DagBag(dag_folder='dags/', include_examples=False); assert not db.import_errors, db.import_errors"
```
Once the import error clears, the scheduler resumes creating DAG runs for
`orders_daily_rollup` on its normal `@daily` schedule. Because
`catchup=False` was set at authoring time (per
[airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)),
the scheduler does not attempt to backfill the missed day automatically —
the team decides separately whether the missed date needs an explicit,
narrow `airflow dags backfill -s <missed-date> -e <missed-date>`, first
confirming `compute_rollup` and `notify_downstream` are both idempotent
(the rollup task overwrites its partition; the notification task is
checked and found to be safe to re-send for this one date) before running
it.

## Cross-references

- [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md) — the idempotency, sensor, and `catchup` authoring practices that determine whether the retry/backfill actions here are safe.
- [dagster-and-prefect-pipeline-authoring](../dagster-and-prefect-pipeline-authoring/SKILL.md) — how comparable re-run/backfill risk is handled in asset-based orchestrators, relevant if considering a migration away from Airflow.
- [kafka-consumer-lag-and-partition-troubleshooting](../kafka-consumer-lag-and-partition-troubleshooting/SKILL.md) — a similarly structured live-incident diagnostic playbook (distinguish "nothing is happening" causes before acting) for the messaging side of a data platform.
