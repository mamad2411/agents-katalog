---
name: databases-data-orchestrator
description: "Route a database/data task to the right skill among the data-layer specialists — PostgreSQL, MySQL/MariaDB, the Prisma ORM, Redis, ClickHouse analytics, cross-engine migrations, and high-throughput ingestion/ETL. USE WHEN a user is designing, querying, optimizing, migrating, or moving data but hasn't named the specific engine or concern."
cluster: databases-data
version: 1.0.0
---

# Databases & Data Orchestrator

The single entry skill for data-layer work. It locates the task on the **engine ×
concern** map and delegates to one of the specialist spokes. The cross-cutting
decision every data task starts from — *which store fits this workload* (OLTP vs OLAP
vs cache vs ORM-managed) — plus the conventions every spoke shares (index choice, ID
strategy, pooling, migration safety, idempotent writes) lives in `databases-data-core`;
read it before picking a store or planning a schema change.

## Routing map (intent → spoke)

**Pick & design a relational store (OLTP)**
- PostgreSQL schema, indexes, RLS, pooling, query tuning → `postgres-patterns`
- MySQL / MariaDB schema, replication, deadlocks, connection pools → `mysql-patterns`
- TypeScript backend going through an ORM → `prisma-patterns` *(traps: `updateMany` returns count, `migrate dev` resets the DB, serverless pool exhaustion)*

**Analytics & time-series (OLAP)**
- Column-store schema, MergeTree, materialized views, batch ingest → `clickhouse-io`

**Cache, locks, queues, rate limits (in-memory)**
- Caching, distributed locks, rate limiting, pub/sub, streams → `redis-patterns`

**Change the schema safely**
- Zero-downtime DDL, backfills, rollbacks, expand/contract across PG/MySQL/ORMs → `database-migrations` *(model in `databases-data-core`)*

**Move data fast & correctly**
- Large ingestion, backfill, export, ETL, warehouse load, manifest catch-up → `data-throughput-accelerator`

## Routing rules by intent

- **"Which database should I use?"** → start in `databases-data-core` §1 (the OLTP/OLAP/cache/ORM decision), then the matching engine spoke.
- **"My query is slow."** → the engine spoke (`postgres-patterns`, `mysql-patterns`, `clickhouse-io`); if it's an ORM-generated query, `prisma-patterns` first (N+1, `relationJoins` row explosion).
- **"I need to alter a production table / add a column / index."** → `database-migrations` for the rollout sequence, with the engine spoke for the exact DDL.
- **"I need caching / a lock / a rate limiter / a queue."** → `redis-patterns` (and check whether a `SKIP LOCKED` SQL queue in the engine spoke fits better).
- **"This backfill/ETL is too slow."** → `data-throughput-accelerator`; pair with the target engine spoke for native-load specifics.
- **Polyglot ask** (e.g. "Postgres for app data + ClickHouse for analytics + Redis cache") → fan out to each engine spoke; route the cutover through `database-migrations`.

## Folded spokes

Additional data-layer specialists folded into this cluster. Route to them on demand the same way as the spokes above (load `skills/<spoke-name>/SKILL.md`). They cover the pipeline/transform/quality/ML/analytics concerns that sit alongside the engine spokes.

**Pipelines & orchestration / ETL**
- Apache Airflow DAGs — operators, sensors, scheduling, testing, deployment → `airflow-dag-patterns` *(USE WHEN building/orchestrating batch pipelines or scheduling jobs; pair with `data-throughput-accelerator` for the heavy load step.)*
- Apache Spark tuning — partitioning, caching, shuffle, memory → `spark-optimization` *(USE WHEN a Spark job is slow or won't scale.)*

**Transform & analytics engineering**
- dbt models — organization, tests, docs, incremental strategies → `dbt-transformation-patterns` *(USE WHEN building warehouse transformations / analytics models; the SQL transform layer above `clickhouse-io`/`postgres-patterns`.)*

**Data quality & validation**
- Data quality frameworks — Great Expectations, dbt tests, data contracts → `data-quality-frameworks` *(USE WHEN adding validation rules, quality gates, or contracts to a pipeline; this is the correctness gate `data-throughput-accelerator` hands off to.)*

**Relational schema design (PostgreSQL deep-dive)**
- PostgreSQL table design — data types, indexing, constraints, advanced features → `postgresql` *(USE WHEN designing a Postgres schema from scratch; complements `postgres-patterns`, which owns query tuning/RLS/pooling.)*

**MLOps**
- End-to-end ML pipelines — data prep → training → validation → deployment → `ml-pipeline-workflow` *(USE WHEN building an ML training/deployment pipeline on top of the data layer.)*

**Business analytics & presentation**
- KPI dashboard design — metric selection, viz best practices, real-time monitoring → `kpi-dashboard-design` *(USE WHEN designing a business dashboard or choosing metrics.)*
- Data storytelling — turning analytics into stakeholder narratives → `data-storytelling` *(USE WHEN presenting analytics / building an exec report from data.)*

**Quantitative finance data**
- Backtesting frameworks — look-ahead/survivorship bias, transaction costs → `backtesting-frameworks` *(USE WHEN building/validating a trading strategy backtest.)*
- Risk metrics — VaR, CVaR, Sharpe, Sortino, drawdown → `risk-metrics-calculation` *(USE WHEN computing portfolio risk metrics or wiring risk limits.)*

## Picked-up spokes

Standalone data-layer skills imported from external libraries (origin noted in each spoke's frontmatter). Route to them on demand the same way (load `skills/<spoke-name>/SKILL.md`).

**Durable workflows / reliable data ops (DBOS)**
- Go application with DBOS durable workflows, steps, queues → `dbos-golang` *(USE WHEN adding fault-tolerant, exactly-once workflows to a Go service backed by Postgres.)*
- Python application with DBOS durable workflows, steps, queues → `dbos-python` *(USE WHEN adding fault-tolerant, exactly-once workflows to a Python service backed by Postgres.)*
- TypeScript application with DBOS durable workflows, steps, queues → `dbos-typescript` *(USE WHEN adding fault-tolerant, exactly-once workflows to a TypeScript service backed by Postgres.)*

**Serverless Postgres**
- Neon serverless Postgres — branching, connection pooling, Prisma/Drizzle integration → `neon-postgres` *(USE WHEN running Postgres on Neon, setting up DB branching per preview/PR, or wiring the serverless driver/pooler; complements `postgres-patterns` query tuning.)*

**Graph & scientific data (Python)**
- NetworkX graph modeling and algorithms — shortest path, centrality, community detection → `networkx` *(USE WHEN the data is a graph/network and you need graph algorithms or connectivity analysis in Python.)*
- Biopython bioinformatics — sequence/structure parsing, NCBI/Entrez, phylogenetics → `biopython` *(USE WHEN parsing biological file formats or running sequence/structure analysis in Python.)*

**Codebase structural memory**
- Data Structure Protocol — persistent dependency/public-API map for agents over a codebase → `data-structure-protocol` *(USE WHEN an agent must reason over a large codebase's structure without re-reading the whole repo.)*

## Standard flow

1. Locate the task: which **store** (relational / analytical / in-memory / ORM-managed) and which **concern** (model → query → optimize → migrate → move).
2. If it touches **store selection, schema/index design, or any schema change**, pull the model from `databases-data-core` first — these decisions interlock and a wrong store choice is expensive to undo.
3. Delegate to the spoke(s). Multi-step asks fan out in lifecycle order (e.g. "ship a new column" → `database-migrations` plan → engine spoke DDL → backfill via `data-throughput-accelerator`).
4. Return: chosen spoke(s), the store/schema decision implied, the migration or correctness gate required, and the next action.

## Sibling clusters (hand off, don't absorb)

This cluster owns engine/query/migration **internals**. Hand off when the task is about
the layer above the database:

- **App-layer repository pattern, transaction/unit-of-work boundaries, service-layer data access** → `backend-architecture`.
- **ORM work lives with its framework:** Eloquent → `php-laravel`; JPA/Hibernate → `jvm`. Prisma stays here (`prisma-patterns`) as the data-layer ORM this cluster owns.

## Guardrails

See `databases-data-core`. In short: **match the store to the access pattern** — don't
force OLAP scans onto an OLTP row store or run analytics off your primary. Treat every
production schema change as a migration (forward-only, expand/contract, no `NOT NULL`
without a default, build indexes concurrently). Validate inputs at the application
boundary; never trust client-supplied SQL fragments. Size connection pools deliberately
(serverless = external pooler + low per-instance limit). Make bulk writes idempotent and
prove correctness with manifests/counts before calling a data job done.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
