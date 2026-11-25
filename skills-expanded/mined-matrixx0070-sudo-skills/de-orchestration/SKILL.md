---
name: de-orchestration
version: 1.0.0
description: Design an orchestration DAG — task dependencies, retries, and backfill strategy.
author: matrixx0070
tags: [data-engineering, orchestration, airflow, dag, scheduling]
capabilities: []
---

# de-orchestration

## When to use

Use this when you need to schedule and coordinate pipeline tasks: what runs, in what order, on what trigger, and how failures and reruns are handled. Applies to Airflow, Dagster, Prefect, or any DAG scheduler.

**Not for:** designing what the extract/load does (use de-pipeline-design), writing the transform SQL (use de-dbt-transform), defining validation rules (use de-data-quality), or CI/CD and infra (that is devops).

## Method

1. **Decompose into atomic, idempotent tasks.** Each task does one thing and can be re-run safely for its window. Decision point: if a task cannot be safely re-run, redesign it before scheduling it.
2. **Wire dependencies as a true DAG.** Draw edges only where a real data dependency exists — over-linking serializes work that could run in parallel; under-linking races.
3. **Choose the trigger:** time-based schedule (cron), data-aware/sensor (wait for an upstream partition or file), or event-driven. Decision point: prefer data-aware triggers over fixed schedules to avoid running before inputs land.
4. **Parameterize every task by the run window** (logical/execution date), not `now()` — this is what makes backfills and reruns deterministic.
5. **Set retries and timeouts per task:** bounded retries with exponential backoff for transient failures, an SLA/timeout so a hung task alerts. Use short-circuit/skip for optional branches.
6. **Design backfills explicitly:** the DAG must accept a date range and reprocess partitions idempotently, with a concurrency cap so a backfill does not overwhelm the warehouse.

## Example

```python
# Airflow-style, date-partitioned, data-aware
with DAG("orders_daily", schedule="@hourly", catchup=True,
         default_args={"retries": 3, "retry_exponential_backoff": True,
                       "retry_delay": timedelta(minutes=2),
                       "execution_timeout": timedelta(minutes=30)}):

    wait_src = ExternalTaskSensor(task_id="wait_orders_landed")   # data-aware
    extract  = extract_orders(window="{{ data_interval_start }}") # parameterized
    load     = merge_orders(window="{{ data_interval_start }}")   # idempotent MERGE
    dbt      = run_dbt(select="fct_orders")
    check    = freshness_check()                                  # blocking

    wait_src >> extract >> load >> dbt >> check
```

Backfill Q1: `catchup=True` reruns each hourly interval, each MERGE keyed on `order_id`, so reprocessing is safe. Cap with `max_active_runs` to protect the warehouse.

## Pitfalls

- Tasks keyed on `now()` instead of the run window, making backfills non-deterministic.
- Infinite or unbacked-off retries that hammer a failing dependency instead of paging.
- One monolithic task, so a mid-pipeline failure forces re-running everything from scratch.
- Unbounded backfill concurrency that saturates the warehouse and starves live runs.

## Output format

```
DAG:        <name> | trigger: cron|sensor|event | catchup: yes|no
Tasks:      <task → does what → idempotent? y/n>
Edges:      <upstream >> downstream> (data dependencies only)
Params:     window = <execution/logical date>
Resilience: retries <n> + backoff | timeout <X> | SLA <Y>
Backfill:   range param <...> | concurrency cap <max_active_runs>
```
