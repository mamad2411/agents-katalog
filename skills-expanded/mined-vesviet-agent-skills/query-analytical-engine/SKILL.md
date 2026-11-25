---
name: query-analytical-engine
description: Execute in-process analytical SQL with chDB and DuckDB v1.5+, orchestrate multi-step stateful pipelines via chdb.session, federate queries across S3 Parquet, PostgreSQL, MySQL, and Iceberg without heavy ETL, leverage Apache Arrow C Data Interface, and enforce safe read-only AST validation. Use when conducting fast in-process analytical queries, cross-source federation, or ad-hoc OLAP exploration.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_build, run_tests]
---

# Query Analytical Engine

Use this skill when executing in-process analytical queries, orchestrating multi-step analytical pipelines, or federating queries across disparate data sources without heavy ETL. For production lakehouse schema design and storage tuning, use `optimize-olap-database` instead.

## When to Use

- running sub-second analytical queries directly in-process via embedded chDB or DuckDB v1.5+
- orchestrating multi-step analytical pipelines and temporary session state using `chdb.session.Session`
- federating queries and joins across S3 Parquet, PostgreSQL, MySQL, and Apache Iceberg without ETL jobs
- transferring in-memory tabular datasets zero-copy via the Apache Arrow C Data Interface
- calculating analytical window functions, moving averages, quantiles, and aggregate state combinators
- validating and hardening AI-generated analytical SQL statements via sqlglot AST parsing
- enforcing read-only connection isolation, connection pooling governance, and execution timeout ceilings

## Core Rules

- **In-Process Vectorized Execution**: execute analytical queries in-process using chDB or DuckDB v1.5+ (the 2.0 LTS line is current since 2026-10-21); avoid spinning up external warehouse clusters for sub-terabyte exploratory analysis.
- **Stateful Session Isolation**: manage multi-step data pipelines using `chdb.session.Session()`; isolate temporary views and tables within the session and execute explicit cleanup in try-finally blocks.
- **Zero-Copy Memory Interchange**: transfer tabular data between chDB, DuckDB, Polars, and PyArrow exclusively via the Apache Arrow C Data Interface (`__arrow_c_stream__`).
- **Direct Cross-Source Federation**: join operational databases (PostgreSQL, MySQL) directly with object storage Parquet/Iceberg layers using engine table functions (`s3()`, `postgresql()`, `iceberg()`).
- **AST Query Validation**: parse every query through `sqlglot` prior to execution; strictly assert single read-only `SELECT`/`EXPLAIN`, reject all DDL/DML, enforce join depth <= 3, and clamp `LIMIT` <= 1000.
- **Read-Only Scoping**: enforce read-only settings (`SET readonly = 1;` in ClickHouse/chDB; `SET TRANSACTION READ ONLY;` in PostgreSQL) on analytical connections.
- **Timeout Ceilings & Memory Caps**: configure strict query execution timeout ceilings (maximum 30s) and enforce memory limits (`SET max_memory = '4GB';`).
- Detailed execution patterns, Python scripts, and federation guides are maintained in [`references/analytical-query-guide.md`](references/analytical-query-guide.md).

## Suggested Process

### 1. Scope Analytical Inquiry & Data Sources
Determine business question, target metrics, required time window, and locations of required source tables (S3 Parquet, live PostgreSQL, Iceberg).

### 2. Engine Selection & Session Initialization
Select engine (`chDB` for ClickHouse analytical function library, `DuckDB` for complex ANSI SQL windowing). Initialize stateful session (`sess = chdb.session.Session()`).

### 3. AST Query Validation & Safety Assertion
Parse proposed query with `sqlglot`. Verify single read-only `SELECT`, join depth <= 3, absence of mutating tokens, and row limit clamp <= 1000.

### 4. Cross-Source Federated Query Execution
Execute federated query joining remote storage partitions (`s3()`) with operational database tables (`postgresql()`). Push down filters to source functions.

### 5. Zero-Copy Arrow Interchange & Downstream Profiling
Expose result set via Apache Arrow C Data Interface capsule to Polars or Pandas for statistical visualization and validation without serialization.

### 6. Emit Analysis Report & Provenance Artifacts
Validate output against `contracts/schemas/data-analysis-report.json`, recording input data hashes, row counts, and 95% confidence intervals.

## Checklist

- [ ] analytical query executed in-process via chDB or DuckDB within 4GB memory ceiling
- [ ] multi-step stateful pipelines orchestrated and cleaned up via `chdb.session.Session`
- [ ] tabular data transferred zero-copy across engines via Apache Arrow C Data Interface
- [ ] cross-source query joins S3/Iceberg Parquet with PostgreSQL/MySQL without ETL data copying
- [ ] query AST validated via sqlglot: read-only `SELECT`, join depth <= 3, LIMIT clamped <= 1000
- [ ] connection settings enforce read-only mode (`readonly = 1`) and strict 30s timeout ceiling
- [ ] input source Parquet SHA-256 hashes and row count provenance documented in report
- [ ] report specifications emitted and validated against `contracts/schemas/data-analysis-report.json`

## Related Skills

- **analyze-data**: High-level decision science, causal inference, and statistical drift audits
- **optimize-olap-database**: Columnar schema design, 8192 sparse indexing, and storage tuning
- **build-data-pipeline**: Production lakehouse ingestion pipelines and ODCS contract validation
- **sandbox-sdk**: Execute untrusted code within hardened containerized sandboxes
- **write-documentation**: Document analytical findings, query dictionaries, and runbooks

## Output Contracts

When emitting analytical query findings and execution plans, emit:

- `contracts/schemas/data-analysis-report.json` — primary analyst deliverable containing verified metrics, confidence intervals, and cryptographic input hashes.
- `contracts/schemas/data-pipeline-spec.json` — federated query extraction specifications when recurring pipeline automation is required.

## Failure Modes

- **Unbounded memory blowup**: running cross-source query without memory limits exhausts RAM. Mitigation: enforce `SET max_memory = '4GB'` and disk spilling.
- **SQL injection / DDL execution**: executing untrusted LLM-generated SQL mutates database state. Mitigation: mandate pre-execution `sqlglot` AST validation.
- **Network join saturation**: performing unfiltered full-table join across remote operational database and S3. Mitigation: push down filter predicates inside `postgresql()` and `s3()` table functions.
- **Session state leakage**: failing to clean up `chdb.session` leaves orphaned temp files. Mitigation: wrap session execution in `try ... finally: session.cleanup()`.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: restrict database credentials used in `postgresql()` table functions to read-only replica users with row-level security.
- **ASI04 Agentic Supply Chain**: verify binary wheel provenance of embedded engine packages (`chdb`, `duckdb`, `pyarrow`).
- **ASI05 Unexpected Code Execution**: prohibit dynamic SQL string interpolation; validate all queries against AST security policies.
- **ASI06 Memory & Context Poisoning**: verify data integrity against raw input Parquet cryptographic hashes before reporting findings.
- **ASI07 Insecure Inter-Agent Communication**: emit structured `data-analysis-report.json` contracts for downstream agents.
- **ASI09 Human-Agent Trust Exploitation**: disclose sample sizes, confidence intervals, and analytical limitations truthfully.
