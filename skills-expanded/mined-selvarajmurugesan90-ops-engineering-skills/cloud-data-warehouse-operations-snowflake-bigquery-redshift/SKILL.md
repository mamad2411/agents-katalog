---
name: cloud-data-warehouse-operations-snowflake-bigquery-redshift
description: >
  Comparative operations guide for the three dominant managed cloud data
  warehouses: Snowflake virtual warehouse sizing and multi-cluster
  scaling, BigQuery slot allocation and on-demand vs. capacity pricing,
  and Redshift cluster/RA3 node sizing and workload management (WLM) —
  plus cost-control and query-performance practices common to all three.
  Use when the user asks to "size a Snowflake warehouse," "control
  BigQuery query costs," "tune Redshift WLM queues," "why is this
  warehouse query slow," "reduce our data warehouse bill," or "choose
  between Snowflake, BigQuery, and Redshift."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: database-operations
  maturity: stable
---

# Cloud Data Warehouse Operations: Snowflake, BigQuery, and Redshift

## Purpose

Snowflake, BigQuery, and Redshift solve the same problem — running
analytical SQL over very large datasets without managing physical
servers — but with materially different billing models and scaling
knobs, which means "tuning performance" and "controlling cost" are
almost the same operational activity in all three, just expressed
through different levers: **virtual warehouse size and auto-suspend**
in Snowflake, **slot allocation and bytes-scanned pricing** in BigQuery,
and **node type/count and workload management queues** in Redshift.
This skill covers the operational levers specific to each, plus the
cost-control and query-performance discipline that generalizes across
all three, so a team choosing between them (or operating more than one)
has a single comparative reference instead of three disconnected vendor
docs.

## When to use

- Sizing a new Snowflake virtual warehouse, BigQuery reservation/slot
  commitment, or Redshift cluster for a new workload.
- The monthly warehouse bill has grown unexpectedly and needs
  attribution to specific workloads/queries before deciding what to cut.
- A query that used to run quickly has degraded, and the cause could be
  warehouse/slot contention, a bad query plan, or data growth.
- Configuring Snowflake multi-cluster warehouses, BigQuery reservation
  assignment, or Redshift WLM queues to isolate workloads (e.g. ETL vs.
  ad hoc BI) from starving each other.
- Evaluating which of the three (or a combination) fits a given
  workload's query pattern and team's operational preferences.

## Prerequisites & environment

- Administrative access to the relevant warehouse's account-level
  configuration: `ACCOUNTADMIN` or a role with `MONITOR`/warehouse
  management privileges in Snowflake; a GCP project with BigQuery Admin
  or Resource Manager access for slot/reservation configuration; an AWS
  account with Redshift cluster/parameter-group management permissions.
- Query-history/billing visibility: Snowflake's `ACCOUNT_USAGE` schema
  (or `INFORMATION_SCHEMA` for shorter retention), BigQuery's
  `INFORMATION_SCHEMA.JOBS` views and Cloud Billing export, Redshift's
  `STL_QUERY`/`SVL_QUERY_SUMMARY` system tables or Redshift's query
  monitoring in the console — all three require this for any cost-
  attribution or slow-query diagnosis in this skill.
- An understanding of the workload's actual query pattern (concurrent
  BI dashboard load vs. scheduled batch ETL vs. ad hoc analyst queries)
  before sizing anything — the right warehouse/slot/cluster size and
  concurrency-scaling configuration depends entirely on this, not on the
  data volume alone.
- For Redshift specifically: familiarity with whether the cluster uses
  legacy dense-compute/dense-storage nodes or RA3 nodes (RA3 separates
  compute from managed storage, which changes both scaling and cost
  characteristics materially compared to older node types).

## Step-by-step guidance

### 1. Size a Snowflake virtual warehouse and configure auto-suspend/auto-resume

```sql
CREATE WAREHOUSE analytics_wh
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 60          -- seconds of inactivity before suspending
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;
```
Warehouse size (`X-SMALL` through `4X-LARGE` and beyond) determines
compute capacity and cost **per-second while running** — Snowflake
bills by warehouse-seconds regardless of how much of that compute a
query actually used, so `AUTO_SUSPEND` set too high (or left at a large
default) is pure wasted spend for bursty workloads. Start smaller than
intuition suggests and scale up based on measured query queuing/spill,
not a guess based on data volume — a bigger warehouse doesn't help a
query that's actually bottlenecked on a bad join order or missing
clustering key. For concurrent-query throughput (many simultaneous BI
dashboard users, not a single large query), use a **multi-cluster
warehouse** instead of a single larger warehouse:
```sql
ALTER WAREHOUSE analytics_wh SET
  WAREHOUSE_TYPE = 'STANDARD'
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 4
  SCALING_POLICY = 'STANDARD';
```
Multi-cluster scales *out* (more clusters of the same size handling
more concurrent queries) rather than *up* (a bigger single warehouse for
one query needing more compute) — pick based on whether the actual
bottleneck is concurrency (many queries queuing) or per-query size, by
checking `QUERY_HISTORY` for queued-vs-executing time.

### 2. Manage BigQuery slot allocation and pricing model

BigQuery's default **on-demand pricing** bills by bytes scanned per
query, with slots (BigQuery's unit of query-execution compute)
allocated dynamically and shared across the project/organization with
no dedicated capacity guarantee. For predictable, high query volume,
purchase a **capacity commitment** (a slot reservation) instead:
```sql
-- Assign a reservation to a specific project/folder (via bq CLI or console)
bq mk --reservation --project_id=<PROJECT_ID> \
  --location=US --slots=500 --edition=ENTERPRISE analytics_reservation

bq mk --reservation_assignment --project_id=<PROJECT_ID> \
  --reservation_id=analytics_reservation \
  --job_type=QUERY --assignee_id=<PROJECT_ID>
```
Reservations trade variable on-demand cost for predictable capacity and
(usually) lower effective cost at sustained high query volume — the
crossover point depends on actual query volume/bytes-scanned, so
compare a representative month's on-demand billing against reservation
pricing before committing, rather than assuming reservations are always
cheaper. Regardless of pricing model, control cost primarily by
**reducing bytes scanned**, since on-demand bills on exactly that:
```sql
SELECT customer_id, total_amount FROM orders
WHERE order_date BETWEEN '2026-01-01' AND '2026-01-31';   -- partition-pruned if orders is partitioned by order_date
```
A table partitioned by date (`PARTITION BY DATE(order_date)`) and
clustered by a common filter column lets BigQuery skip scanning
irrelevant partitions entirely — an unpartitioned equivalent table
scans (and bills for) the full table on every query regardless of the
`WHERE` clause.

### 3. Configure Redshift node sizing and workload management (WLM)

```sql
-- Check current WLM queue configuration and queuing/wait time
SELECT service_class, num_query_tasks, total_queue_time, total_exec_time
FROM stl_wlm_query
ORDER BY total_queue_time DESC LIMIT 20;
```
Redshift's **Workload Management (WLM)** partitions cluster resources
into queues (e.g. one for scheduled ETL, one for ad hoc BI) so a
long-running batch load doesn't starve interactive dashboard queries of
memory/concurrency slots. Prefer **automatic WLM** (Redshift dynamically
manages memory/concurrency per queue) as the default, only moving to
manual WLM queue configuration when a specific workload has proven,
measured contention that automatic WLM isn't resolving:
```json
[
  {"query_group": "etl", "query_concurrency": 3, "memory_percent_to_use": 50},
  {"query_group": "bi", "query_concurrency": 8, "memory_percent_to_use": 50}
]
```
For node sizing, **RA3 nodes** (current generation) separate compute
from managed storage — scaling compute (adding/resizing nodes) no
longer requires also scaling storage, unlike legacy dense-storage
nodes where the two were coupled. Use **Concurrency Scaling** (Redshift
automatically adds transient capacity for bursts of concurrent read
queries) for spiky BI dashboard load instead of permanently over-
provisioning the base cluster for peak concurrency:
```sql
ALTER TABLE orders SET (concurrency_scaling = 'auto');  -- workload-group level in newer parameter groups
```

### 4. Diagnose a slow query with each warehouse's plan/profile tooling

```sql
-- Snowflake: check the query profile for spilling to local/remote disk
SELECT query_id, bytes_spilled_to_local_storage, bytes_spilled_to_remote_storage
FROM snowflake.account_usage.query_history
WHERE query_id = '<QUERY_ID>';
```
Spilling (a query's intermediate data exceeding warehouse memory and
spilling to disk) is the single most common Snowflake performance
problem traceable to warehouse sizing — a warehouse one size larger
gives proportionally more memory, which can eliminate spill for a
specific heavy join/sort, but confirm spill is actually occurring
before assuming "bigger warehouse" is the fix.
```sql
-- BigQuery: check the query execution plan for shuffle/skew
SELECT * FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_id = '<JOB_ID>';
```
Look at `total_bytes_processed` against table size (confirms whether
partition/cluster pruning worked) and the query execution details for
stage-level skew (one worker doing dramatically more work than others,
usually from a skewed `JOIN`/`GROUP BY` key).
```sql
-- Redshift: check for a table with skewed distribution or missing sort key benefit
SELECT "table", diststyle, sortkey1, size
FROM svv_table_info WHERE "table" = 'orders';
```
A `diststyle` of `EVEN` or a poorly chosen `DISTKEY` for a table
frequently joined on a specific column forces cross-node data
redistribution during the join (a network-shuffle cost) — redefining
`DISTKEY`/`SORTKEY` requires a table rebuild (`CREATE TABLE ... LIKE`
plus reload, or `ALTER TABLE ... ALTER DISTKEY` in newer Redshift
versions that support in-place key changes) and should be validated
against actual join patterns, not guessed.

### 5. Control cost with usage attribution before cutting capacity blindly

All three warehouses make it possible to attribute spend to a specific
team/workload — do this before reducing warehouse size, slots, or node
count, since an undersized cut applied to the wrong workload just
trades a cost problem for a performance incident:
```sql
-- Snowflake: cost by warehouse over the last 30 days
SELECT warehouse_name, sum(credits_used) AS credits
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time > dateadd('day', -30, current_timestamp())
GROUP BY warehouse_name ORDER BY credits DESC;
```
```sql
-- BigQuery: bytes billed by user/query over the last 30 days
SELECT user_email, sum(total_bytes_billed) AS bytes_billed
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > timestamp_sub(current_timestamp(), interval 30 day)
GROUP BY user_email ORDER BY bytes_billed DESC;
```

## Best practices

- Size compute (warehouse/slots/nodes) based on measured queuing, spill,
  or shuffle evidence from query history, not data volume alone or an
  intuition-driven guess.
- Set aggressive `AUTO_SUSPEND` on Snowflake warehouses for bursty
  workloads — idle warehouse-seconds are pure waste under per-second
  billing, and `AUTO_RESUME` makes the cold-start cost of suspending
  aggressively negligible for most interactive workloads.
- Partition and cluster tables by real, dominant filter columns in
  BigQuery (and choose `DISTKEY`/`SORTKEY` deliberately in Redshift) —
  this is the highest-leverage cost/performance lever in both, since it
  directly reduces bytes scanned or data shuffled, unlike compute
  sizing which only processes the same excess data faster.
- Isolate workload classes (scheduled ETL vs. ad hoc BI vs. dashboard
  refresh) via multi-cluster warehouses, reservation assignment, or WLM
  queues so one workload's burst can't starve another's latency
  budget.
- Attribute spend to team/workload before cutting capacity — reducing a
  warehouse/slot/node count without knowing which workload actually
  drives the cost risks degrading the wrong thing.
- Treat any table restructuring (repartitioning, changing
  cluster/distribution/sort keys) as the equivalent of an index redesign
  elsewhere in this repo — validate against real query patterns and
  expect a rebuild, not a free in-place change, in most cases.

## Common pitfalls

- **Symptom:** A Snowflake bill is dominated by warehouse-seconds even
  though actual query volume seems modest.
  **Fix:** `AUTO_SUSPEND` is set too high (or a warehouse was left
  `RESUME`d manually and never suspended) — every idle second the
  warehouse stays running is billed the same as a busy second. Lower
  `AUTO_SUSPEND` to the shortest value tolerable for the workload's
  query pattern (60 seconds is a common starting point for interactive
  workloads) and audit for any warehouse left permanently resumed by
  habit.

- **Symptom:** A BigQuery on-demand bill spikes dramatically for a query
  that "only" needed a small date range of data.
  **Fix:** The underlying table isn't partitioned (or the query's
  `WHERE` clause doesn't align with the partition column in a way
  BigQuery can prune), so the full table is scanned and billed
  regardless of the filter. Confirm via `total_bytes_processed` in the
  job's execution details, then partition the table by the dominant
  filter column and re-point ETL/dashboards at the partitioned table.

- **Symptom:** Redshift queries queue for a long time during business
  hours even though the cluster's CPU utilization doesn't look
  saturated.
  **Fix:** WLM queue concurrency is set too low for the actual
  concurrent query count, so queries wait for a queue slot rather than
  cluster resources genuinely being exhausted. Check `stl_wlm_query`
  queue wait time versus execution time; raise queue concurrency (or
  switch to automatic WLM) rather than assuming a bigger cluster is
  needed for what's actually a queue-configuration problem.

- **Symptom:** A join between two large Redshift tables is far slower
  than expected, with high network I/O visible in query monitoring.
  **Fix:** One or both tables use a `DISTKEY`/`DISTSTYLE` that doesn't
  align with the join column, forcing Redshift to redistribute rows
  across nodes at query time. Check `svv_table_info.diststyle` and
  redesign the distribution key to match the dominant join pattern —
  this requires a table rebuild, so validate the new key against all
  major query patterns for that table, not just the one query being
  fixed.

- **Symptom:** Someone runs `TRUNCATE TABLE` or `DROP TABLE` directly
  against a production warehouse table (Snowflake, BigQuery, or
  Redshift) intending to clear staging data, and it turns out to be the
  production fact table feeding live dashboards.
  **Fix:** This is an immediately destructive, and in most
  configurations irreversible outside of engine-specific time-travel/
  fail-safe windows, action.
  > **Warning — destructive action.** Snowflake's Time Travel
  > (`UNDROP TABLE`, historical `SELECT ... AT`) and BigQuery's
  > time-travel window offer a limited recovery path (typically
  > measured in days, and configurable in Snowflake via
  > `DATA_RETENTION_TIME_IN_DAYS`) — but Redshift has no equivalent
  > built-in undo for a `TRUNCATE`/`DROP`. Before any destructive DDL
  > against a shared warehouse, independently confirm the target
  > object and environment, and restrict `TRUNCATE`/`DROP` privileges
  > on production schemas to a narrow role rather than broad analyst/
  > engineer access; see
  > [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md)
  > for the restore-testing discipline that should back up whatever
  > time-travel window each engine provides.

## Worked example

**Scenario:** A BI team's Snowflake `MEDIUM` warehouse shows growing
query queue times during a 9am dashboard-refresh spike, while a
separate nightly ETL job intermittently spills to disk and runs long.
Monthly Snowflake spend has also grown 40% quarter-over-quarter with no
corresponding growth in data volume.

1. Check cost attribution first:
   ```sql
   SELECT warehouse_name, sum(credits_used) FROM snowflake.account_usage.warehouse_metering_history
   WHERE start_time > dateadd('month', -3, current_timestamp())
   GROUP BY warehouse_name ORDER BY 2 DESC;
   ```
   Finds the single shared `analytics_wh` warehouse serves both the
   9am dashboard spike and the nightly ETL, and `AUTO_SUSPEND` is set to
   the default 600 seconds — much of the credit growth is idle-seconds
   accumulated between light, scattered ad hoc queries throughout the
   day, not the two known workloads.
2. Split the shared warehouse into two purpose-sized ones: a
   multi-cluster `MEDIUM` warehouse (`MIN_CLUSTER_COUNT=1,
   MAX_CLUSTER_COUNT=3`) for the concurrent dashboard workload, and a
   separate `LARGE` single-cluster warehouse for nightly ETL, each with
   `AUTO_SUSPEND = 60`.
3. Check the ETL job's query profile for the spill cause:
   ```sql
   SELECT bytes_spilled_to_local_storage FROM snowflake.account_usage.query_history
   WHERE query_id = '<ETL_QUERY_ID>';
   -- 40GB spilled
   ```
   Confirms a genuine memory-bound spill (not a bad join order — the
   plan itself is reasonable for the data volume), so the `LARGE`
   sizing for ETL is justified rather than a workaround for a fixable
   query.
4. Re-measure after one week: dashboard queue time drops to near-zero
   during the 9am spike (multi-cluster now scales out instead of
   queuing behind ETL), ETL spill disappears entirely, and overall
   credit consumption drops relative to the prior shared-warehouse
   baseline once `AUTO_SUSPEND` stops accumulating idle-seconds across
   the whole day.
5. Document the two-warehouse split and revised `AUTO_SUSPEND` as the
   new standing configuration, with a monthly cost-attribution review
   added going forward instead of only investigating after a bill spike
   is already noticed.

## Cross-references

- [clickhouse-analytical-database-operations](../clickhouse-analytical-database-operations/SKILL.md) — a self-hosted OLAP alternative to these three managed warehouses, useful when full operational control (at the cost of managing the cluster yourself) is preferred over a managed service's billing model.
- [postgresql-operations-and-performance-tuning](../postgresql-operations-and-performance-tuning/SKILL.md) — Redshift's query engine and much of its SQL surface derive from PostgreSQL, so `EXPLAIN`-driven query diagnosis concepts there carry over partially, though Redshift's columnar/MPP execution model differs materially from OLTP PostgreSQL.
- [database-backup-and-restore-strategies](../database-backup-and-restore-strategies/SKILL.md) — the restore-testing discipline that should back up each warehouse's time-travel/snapshot recovery window for accidental destructive DDL.
