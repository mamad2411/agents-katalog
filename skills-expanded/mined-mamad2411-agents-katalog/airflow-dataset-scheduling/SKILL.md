---
name: airflow-dataset-scheduling
description: >
  Airflow 2 Dataset-driven scheduling for owned DAGs: produce/consume Datasets,
  scheduling after data updates, dual timetable+dataset patterns, and operational
  debugging of dataset events. Use when migrating from huge sensor meshes or
  tightly coupled dag runs to data-aware scheduling — not for Airflow security
  hardening alone (see airflow-dag-security).
---

# Airflow Dataset Scheduling

## Scope And Authorization

- **In scope:** Airflow 2.x+ environments you operate where Datasets (data-aware scheduling) are available.
- **Out of scope:** Changing production schedules without owner approval; using datasets to exfiltrate data.
- Test new producer/consumer links in a non-prod DAG folder first.
- Dataset URIs may reveal sensitive path names — redact in public docs if needed.
- Pair DAG code with `code-quality-standards` and secrets rules from `airflow-dag-security`.

## When To Use

- Replacing long `ExternalTaskSensor` chains with Dataset scheduling.
- Triggering downstream DAGs when a table/file/partition is updated.
- Coordinating multi-DAG pipelines with explicit data contracts.
- Debugging why a consumer DAG did not run after producer success.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Airflow security / secrets / RBAC | `airflow-dag-security` |
| Airbyte ELT connector trust | `airbyte-connector-security` |
| Generic observability | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Meaning |
| --- | --- |
| Dataset | Logical data object URI (e.g. `s3://bucket/path`, `postgres://db/schema.table`) |
| Producer | Task/DAG outlets that emit dataset updates on success |
| Consumer | DAG scheduled on one or more datasets (AND semantics for multiple) |
| Dataset event | Record that a dataset was updated at a time |
| Timetable + dataset | Combine time schedule with data readiness where supported |
| URI convention | Org-standard naming so teams share contracts |

**Note:** Exact APIs evolved (Dataset → broader data assets in later Airflow). Match docs for your version; patterns below use Airflow 2 Dataset style.

## Workflow

### 1. Confirm scope and success criteria

1. Record Airflow version, producer/consumer teams, data URIs, SLA.
2. Success: consumer runs after producer success without brittle `execution_date` sensors; missed events debuggable; no circular waits.
3. Inventory current sensors and cross-DAG dependencies.

### 2. Define dataset contracts

```text
# URI naming convention (example)
dataset://analytics/raw/orders
dataset://analytics/curated/orders_daily
s3://datalake/prod/orders/ds={{ ds }}   # prefer stable logical URIs over raw dated paths when possible
```

| Field | Guidance |
| --- | --- |
| URI | Stable logical id; document partition semantics separately |
| Owner | Team + oncall |
| SLA | Max lag after producer |
| Schema | Link to table/file schema doc |

### 3. Implement producer outlets

```python
from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.python import PythonOperator
from datetime import datetime

ORDERS_RAW = Dataset("dataset://analytics/raw/orders")

with DAG(
    dag_id="produce_orders_raw",
    start_date=datetime(2024, 1, 1),
    schedule="@hourly",
    catchup=False,
    tags=["producer"],
) as dag:
    def extract():
        # ... write data ...
        pass

    PythonOperator(
        task_id="extract_orders",
        python_callable=extract,
        outlets=[ORDERS_RAW],  # emits dataset event on success
    )
```

1. Emit outlets only when data is actually usable (not on empty failed writes).
2. Avoid emitting from empty no-op success paths.

### 4. Implement consumer schedule

```python
from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.empty import EmptyOperator
from datetime import datetime

ORDERS_RAW = Dataset("dataset://analytics/raw/orders")
CUSTOMERS = Dataset("dataset://analytics/raw/customers")

with DAG(
    dag_id="curate_orders",
    start_date=datetime(2024, 1, 1),
    schedule=[ORDERS_RAW, CUSTOMERS],  # runs when BOTH updated (AND)
    catchup=False,
    tags=["consumer"],
) as dag:
    EmptyOperator(task_id="build_curated")
```

| Pattern | Use when |
| --- | --- |
| Single dataset schedule | Simple 1:1 producer→consumer |
| List of datasets | Need all inputs ready (AND) |
| Time schedule only | Pure batch clock |
| Dual (version-dependent) | Ready-by-data but not more than hourly, etc. |

### 5. Migrate off sensors

1. Map each `ExternalTaskSensor` to a Dataset URI.
2. Deploy producer outlets first; confirm events in UI (Datasets view) / metadata DB.
3. Switch consumer schedule; keep sensor disabled temporarily for rollback.
4. Remove sensors after soak.

### 6. Debug missed runs

```bash
airflow dags list
airflow dags show curate_orders
# UI: Datasets → events; Graph shows dataset edges on supported versions
# Check producer task success and outlets configuration
airflow tasks states-for-dag-run produce_orders_raw <run_id>
```

| Symptom | Checks |
| --- | --- |
| No consumer run | Producer failed; outlet missing; URI string mismatch |
| Extra runs | Multiple producers emit same URI; retries emitting twice (understand idempotency) |
| Partial data | Outlet emitted before publish committed — fix task boundaries |
| Circular dependency | A↔B datasets — redesign |

### 7. Ops and hand off

1. Document URI catalog in data portal / README.
2. Alert if consumer lag > SLA after producer event.
3. Queue discipline: consumer concurrency limits so event storms do not melt warehouses.
4. Security: dataset scheduling is not authz — still enforce warehouse IAM (`airflow-dag-security`).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| URIs | Shared constants module | Typos `"orders"` vs `"order"` silently diverge |
| Emit | After commit/visibility | Before job finishes writing |
| Sensors | Removed after soak | Infinite ExternalTaskSensor mesh forever |
| Semantics | Document AND of inputs | Assume OR without testing |
| Security | Secrets still in backend | Dataset URI with embedded tokens |

## Output Checklist

- [ ] Airflow version supports planned Dataset features
- [ ] URI catalog and owners published
- [ ] Producers declare outlets on success paths
- [ ] Consumers schedule on correct dataset sets
- [ ] Sensor migration plan/rollback
- [ ] Event visibility verified in UI/CLI
- [ ] SLA/lag alerts considered
- [ ] No secrets in URIs or DAG defaults
- [ ] `code-quality-standards` applied

## Rules

- Operate only on owned Airflow.
- Treat URI strings as API contracts — centralize constants.
- Do not emit dataset events for failed/partial data.
- Dataset scheduling complements security skills; it does not replace them.
- Prefer simple graphs; avoid cyclic dataset dependencies.
