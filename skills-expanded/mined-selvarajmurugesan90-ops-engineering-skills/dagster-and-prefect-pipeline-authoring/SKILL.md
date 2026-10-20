---
name: dagster-and-prefect-pipeline-authoring
description: >
  Authors data pipelines with Dagster's asset-based model or Prefect's
  Pythonic flow/task model as modern alternatives to Airflow, and gives a
  decision framework for when each fits better than task-based DAG
  orchestration. Use when the user asks to "write a Dagster asset,"
  "define a Prefect flow," "should we use Dagster instead of Airflow,"
  "asset-based vs. task-based orchestration," or is evaluating a
  data-orchestration tool for a new pipeline.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: messaging-and-data-orchestration
  maturity: stable
---

# Dagster and Prefect Pipeline Authoring

## Purpose

Airflow models a pipeline as a DAG of *tasks* — the unit of scheduling and
retry is "did this task run." Dagster inverts this to an *asset*-based
model, where the unit of definition is "what data object does this
produce" and the DAG of dependencies is derived from asset relationships;
Prefect keeps a task/flow model closer to Airflow's but with a more
Pythonic, dynamic authoring experience and different defaults around
retries and dynamic task generation. Neither is a strict upgrade over
Airflow — each fits certain pipeline shapes and team preferences better.
This skill covers authoring in both and a decision framework for
choosing, alongside Airflow's task-based approach covered in
[airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md).

## When to use

- Starting a new data pipeline and deciding between Airflow, Dagster, and
  Prefect before committing to one.
- Authoring Dagster software-defined assets, ops, and jobs, including
  asset dependencies and partitions.
- Authoring Prefect flows and tasks, including retries, caching, and
  dynamic task mapping.
- Explaining the practical difference between "asset-based" and
  "task-based" orchestration to a team evaluating a migration.
- Reviewing a Dagster or Prefect pipeline definition for correctness
  before deploying it.

## Prerequisites & environment

- Dagster 1.x (the asset-based `@asset` API is the current recommended
  authoring pattern; the older `@op`/`@job`-only style still works but
  is not the primary model in recent Dagster documentation and examples)
  with Dagster's own scheduler/daemon (`dagster-daemon`) or Dagster Cloud
  for schedule/sensor execution.
- Prefect 2.x/3.x (Prefect's flow/task decorator API; check which major
  version is targeted, since orchestration-engine internals and some
  deployment mechanics changed between them) with either Prefect Cloud or
  a self-hosted Prefect server for flow-run orchestration.
- A clear sense of the pipeline's actual shape: is it naturally described
  as "these tables/files depend on each other" (favors Dagster's asset
  model) or "these steps run in this order, with dynamic branching based
  on runtime values" (favors Prefect's more dynamic task model, or
  Airflow's task-based model if the team already has Airflow expertise
  and infrastructure)?
- For Dagster: familiarity with its resource/IO-manager abstractions,
  which are how assets read/write data without hardcoding storage details
  into the asset function itself.
- For Prefect: familiarity with its work pool/worker deployment model for
  actually executing flow runs (distinct from just defining the flow in
  Python).

## Step-by-step guidance

1. **Decide asset-based (Dagster) vs. task-based (Prefect/Airflow) by
   what the pipeline is actually organized around.** If the team thinks
   about the pipeline primarily in terms of the data it produces (this
   pipeline's job is to keep `orders_daily_rollup`, `customer_ltv`, and
   `fulfillment_metrics` up to date, and their dependencies are what
   drives execution order), Dagster's asset model maps directly onto that
   mental model and gives first-class data lineage/freshness tracking for
   free. If the pipeline is more naturally a sequence of operational
   steps (extract, validate, branch based on a runtime condition, fan out
   dynamically over a list not known until runtime), a task-based model
   (Prefect or Airflow) tends to fit with less friction, since forcing a
   highly dynamic, branch-heavy process into asset definitions can feel
   unnatural.

2. **Define a Dagster asset with explicit dependencies inferred from
   function parameters**, not a separate dependency-declaration step:
   ```python
   from dagster import asset, Definitions

   @asset
   def raw_orders() -> None:
       # extract raw orders from source system into staging storage
       extract_orders_to_staging()

   @asset(deps=[raw_orders])
   def orders_daily_rollup() -> None:
       # Dagster infers this depends on raw_orders from the `deps` argument
       # (or automatically from a type-annotated parameter matching
       # another asset's name, depending on IO manager setup)
       run_sql("""
           DELETE FROM orders_daily_rollup WHERE rollup_date = CURRENT_DATE;
           INSERT INTO orders_daily_rollup
           SELECT CURRENT_DATE, COUNT(*), SUM(amount_cents) FROM staging_orders;
       """)

   defs = Definitions(assets=[raw_orders, orders_daily_rollup])
   ```
   The asset graph (`raw_orders` → `orders_daily_rollup`) is visible
   directly in Dagster's UI as a lineage graph of data objects, not just a
   task-execution DAG — this is the core practical difference from
   Airflow: the unit shown and reasoned about is "what data exists and
   how fresh is it," not "which tasks ran."

3. **Use Dagster partitions for date-based (or otherwise partitioned)
   assets**, which is Dagster's mechanism for backfill/reprocessing that's
   more structured than Airflow's logical-date templating:
   ```python
   from dagster import asset, DailyPartitionsDefinition

   daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")

   @asset(partitions_def=daily_partitions)
   def orders_daily_rollup(context) -> None:
       partition_date = context.partition_key
       run_sql(f"""
           DELETE FROM orders_daily_rollup WHERE rollup_date = '{partition_date}';
           INSERT INTO orders_daily_rollup
           SELECT '{partition_date}', COUNT(*), SUM(amount_cents)
           FROM staging_orders WHERE rollup_date = '{partition_date}';
       """)
   ```
   As with Airflow, the `DELETE`-then-`INSERT` pattern makes re-running a
   specific partition idempotent — Dagster's partition model doesn't
   remove the need for idempotent task logic, it just gives a more
   structured UI/API for selecting which partitions to (re)materialize.

4. **Define a Prefect flow and tasks using plain Python control flow** —
   Prefect's model allows ordinary `if`/`for` logic to drive task
   execution, rather than Airflow's more declarative dependency graph:
   ```python
   from prefect import flow, task
   from datetime import timedelta

   @task(retries=3, retry_delay_seconds=60)
   def extract_orders():
       return fetch_orders_from_source()

   @task(retries=2)
   def compute_rollup(orders, rollup_date):
       # idempotent: overwrite the partition for rollup_date
       upsert_rollup(rollup_date, orders)

   @flow(name="orders-daily-rollup")
   def orders_daily_rollup_flow(rollup_date: str):
       orders = extract_orders()
       if not orders:
           # ordinary Python control flow — no special "branch operator"
           # needed the way Airflow requires a BranchPythonOperator
           return
       compute_rollup(orders, rollup_date)
   ```
   The `if not orders: return` branch is plain Python — Prefect doesn't
   need Airflow's dedicated branching operators for this, which is one of
   the concrete authoring-ergonomics differences teams cite when
   preferring Prefect for highly dynamic pipelines.

5. **Use Prefect's `.map()` (or the equivalent dynamic task generation)
   for fan-out over a runtime-determined list**, rather than needing a
   fixed, pre-declared set of parallel tasks:
   ```python
   @task
   def process_region(region: str, rollup_date: str):
       compute_rollup_for_region(region, rollup_date)

   @flow
   def orders_daily_rollup_flow(rollup_date: str):
       regions = fetch_active_regions()  # not known until runtime
       process_region.map(regions, rollup_date=rollup_date)
   ```
   Airflow's equivalent (dynamic task mapping, `expand()`) exists in
   Airflow 2.3+ too, so this specific capability is no longer a hard
   Prefect-only differentiator — but Prefect's version requires
   noticeably less ceremony, which matters for a highly dynamic pipeline
   authored primarily in plain Python.

6. **Set retries and caching at the task/asset level deliberately**, since
   both frameworks' defaults differ from Airflow's and from each other:
   ```python
   @task(retries=3, retry_delay_seconds=60, cache_key_fn=lambda ctx, params: str(params))
   def extract_orders(source_date: str):
       ...
   ```
   Prefect's task-level caching (keyed on a function of the task's
   parameters) can skip re-execution entirely for a task whose inputs
   haven't changed — a capability with no direct Airflow equivalent at
   the task level. Use it deliberately for genuinely expensive,
   deterministic steps, not for anything with side effects that should
   run every time regardless of cached inputs.

7. **Confirm idempotency for both frameworks the same way as Airflow** —
   asset-based or dynamic-flow authoring doesn't remove the need for
   overwrite-safe logic, it just changes how re-execution is
   triggered/scoped (Dagster: re-materializing a partition; Prefect:
   re-running a flow run or an individual mapped task):
   ```python
   # Both frameworks still need this discipline — the framework doesn't
   # make a naive append-only write safe to retry.
   ```
   The idempotency guidance in
   [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md)
   applies unchanged regardless of which orchestrator executes the task.

8. **Validate Dagster assets and Prefect flows before deploy** — each has
   its own equivalent of `airflow dags test`:
   ```bash
   # Dagster: materialize an asset (or subset) for a specific partition,
   # actually executing the logic
   dagster asset materialize --select orders_daily_rollup --partition 2024-06-01

   # Prefect: run a flow directly as a local Python invocation
   python -c "from pipeline import orders_daily_rollup_flow; orders_daily_rollup_flow(rollup_date='2024-06-01')"
   ```
   As with `airflow dags test`, these actually execute task/asset logic
   against real (or test) dependencies — treat them the same way: a
   required pre-merge check, not optional.

## Best practices

- Choose based on the pipeline's actual shape (data-lineage-centric vs.
  step-sequence-centric with runtime branching) rather than defaulting to
  whichever tool is newest or most discussed — Airflow's maturity and
  ecosystem still matter for teams with existing Airflow infrastructure
  and expertise, and switching orchestrators is a real migration cost.
- Use Dagster's asset model deliberately when data lineage/freshness
  tracking across the pipeline is a real requirement, not just because
  "assets" sounds more modern than "tasks."
- Use Prefect's dynamic `.map()`/plain-Python-control-flow authoring for
  pipelines with genuine runtime-determined branching/fan-out, not for
  every pipeline by default — a simple, static, linear pipeline gains
  little from this flexibility and Airflow/Dagster may be simpler to
  operate for it.
- Keep the same idempotency discipline (overwrite-by-partition, not
  append-only) regardless of which orchestrator is used — none of these
  frameworks make non-idempotent task logic safe to retry.
- Validate with each framework's actual-execution check
  (`dagster asset materialize`, a direct Prefect flow invocation, or
  `airflow dags test`) before merge, not just a syntax/import check.
- Don't migrate an existing, working Airflow pipeline to Dagster or
  Prefect purely on the strength of the asset/task-model argument — weigh
  the migration cost (rewriting DAGs, retraining the team, dual-running
  during cutover) against the concrete operational benefit for that
  specific pipeline.

## Common pitfalls

- **Symptom:** A team adopts Dagster expecting its asset model to
  automatically make pipelines idempotent, but a re-materialized asset
  still produces duplicate/incorrect data.
  **Fix:** Dagster's partition/asset model changes how re-execution is
  triggered and scoped, but the asset function's own logic still needs to
  overwrite (not append) its target for the given partition — this is the
  same idempotency requirement as Airflow, not something the framework
  handles automatically.

- **Symptom:** A highly dynamic pipeline (fan-out over a runtime-determined
  list, several conditional branches) is forced into Dagster's asset
  model, and the resulting asset graph is awkward — either an
  explosion of dynamically-partitioned assets or logic buried inside a
  single asset function that no longer reflects real data lineage.
  **Fix:** This is a sign the pipeline's actual shape is more
  step-sequence-centric than data-lineage-centric — Prefect's task/flow
  model (or Airflow's dynamic task mapping) is often a better fit for
  this pattern than forcing it into asset definitions built for a more
  static lineage graph.

- **Symptom:** A Prefect task with caching enabled (`cache_key_fn`) skips
  execution on a run where the task's side effect (e.g. sending a
  notification) was actually needed.
  **Fix:** Caching is appropriate for deterministic, side-effect-free
  computation whose output only depends on its inputs — it's the wrong
  tool for a task with an external side effect that should run every time
  regardless of whether its inputs match a previous run. Remove caching
  from tasks with real side effects, and reserve it for genuinely
  expensive, pure computation steps.

- **Symptom:** A team switches from Airflow to Dagster or Prefect
  expecting an immediate operational-simplicity win, but ends up running
  and maintaining two orchestration systems in parallel for months with
  no clear migration end date.
  **Fix:** This is a migration-planning gap, not a tooling problem —
  before migrating, scope a concrete cutover plan (which pipelines move
  first, how long dual-running is acceptable, what the rollback plan is)
  the same way any infrastructure migration would be planned, rather than
  starting the migration without a bounded timeline.

## Worked example

**Scenario:** A team is deciding how to build a new pipeline that keeps
three related tables fresh — `raw_orders` (extracted from a source
system), `orders_daily_rollup` (aggregated from `raw_orders`), and
`customer_ltv` (computed from `orders_daily_rollup` plus a customer
dimension table) — and wants clear lineage/freshness visibility across
all three for a data-quality dashboard the analytics team relies on.

Decision: this is a strong fit for Dagster's asset model — the pipeline
is fundamentally about keeping three related data objects fresh and
correctly ordered, and the analytics team's freshness-visibility
requirement is exactly what Dagster's asset lineage graph provides
natively, without needing to bolt on a separate lineage-tracking system
the way a purely task-based DAG would.

```python
from dagster import asset, Definitions, DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")

@asset(partitions_def=daily_partitions)
def raw_orders(context) -> None:
    extract_orders_to_staging(partition_date=context.partition_key)

@asset(partitions_def=daily_partitions, deps=[raw_orders])
def orders_daily_rollup(context) -> None:
    partition_date = context.partition_key
    run_sql(f"""
        DELETE FROM orders_daily_rollup WHERE rollup_date = '{partition_date}';
        INSERT INTO orders_daily_rollup
        SELECT '{partition_date}', COUNT(*), SUM(amount_cents)
        FROM staging_orders WHERE rollup_date = '{partition_date}';
    """)

@asset(partitions_def=daily_partitions, deps=[orders_daily_rollup])
def customer_ltv(context) -> None:
    partition_date = context.partition_key
    run_sql(f"""
        DELETE FROM customer_ltv WHERE as_of_date = '{partition_date}';
        INSERT INTO customer_ltv
        SELECT c.customer_id, '{partition_date}', SUM(r.amount_cents)
        FROM orders_daily_rollup r JOIN customers c ON r.customer_id = c.customer_id
        WHERE r.rollup_date <= '{partition_date}'
        GROUP BY c.customer_id;
    """)

defs = Definitions(assets=[raw_orders, orders_daily_rollup, customer_ltv])
```

Validation before deploy:
```bash
$ dagster asset materialize --select raw_orders,orders_daily_rollup,customer_ltv \
  --partition 2024-06-01
```
This actually executes each asset's logic in dependency order for the
`2024-06-01` partition, the Dagster equivalent of `airflow dags test`.
The analytics team's dashboard then queries Dagster's asset-freshness API
directly to show "as of when is `customer_ltv` current," which would have
required custom instrumentation on top of a purely task-based DAG but is
native to the asset model chosen here.

By contrast, if this same team's next pipeline were "poll an
upstream API for a list of newly onboarded partners (unknown count until
runtime), and run a distinct validation-and-import flow per partner with
several conditional branches depending on each partner's contract type,"
that pipeline would be a better fit for Prefect's dynamic `.map()` and
plain-Python branching (or Airflow, if the team already operates Airflow
and the dynamic task mapping added in Airflow 2.3+ covers the need) than
for Dagster's asset model.

## Cross-references

- [airflow-dag-authoring-and-validation](../airflow-dag-authoring-and-validation/SKILL.md) — the task-based authoring model this skill compares against, including the idempotency discipline that applies unchanged across all three tools.
- [airflow-scheduler-and-dag-troubleshooting](../airflow-scheduler-and-dag-troubleshooting/SKILL.md) — the retry/backfill risk considerations here (idempotency before re-running) map directly onto Dagster partition re-materialization and Prefect flow re-runs.
- [kafka-schema-registry-and-compatibility-management](../kafka-schema-registry-and-compatibility-management/SKILL.md) — schema-evolution discipline relevant to any asset/flow that consumes messages from a Kafka topic as one of its upstream dependencies.
