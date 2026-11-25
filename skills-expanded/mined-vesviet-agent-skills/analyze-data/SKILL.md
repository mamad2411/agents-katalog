---
name: analyze-data
description: Explore analytical datasets using DuckDB/Polars, query canonical Semantic Metric Catalogs (dbt MetricFlow, Cube.js, Apache Ossie) to eliminate Text-to-SQL hallucinations, detect statistical distribution drift, track agent query costs as FinOps line item, and deliver quantitatively verified insights with explicit fact/interpretation separation. Use when answering business questions from data without owning production pipeline infrastructure.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, query_db, read_database, run_tests, execute_command]
---

# Analyze Data

Use this skill for **decision science and analytical** work: querying canonical metrics, profiling data in-process, evaluating statistical drift, conducting causal inference, and producing verifiable stakeholder reports.

## When to Use

- answering business, product, and KPI questions using conformed lakehouse tables
- querying certified metrics via Semantic Metric Layers (dbt MetricFlow, Cube.js, **Apache Ossie**)
- executing fast in-process exploratory analytics on Parquet/Iceberg extracts via DuckDB and Polars
- auditing statistical feature and cohort distribution drift (PSI, Two-Sample KS-test, Tukey's IQR)
- evaluating A/B tests with automated Sample Ratio Mismatch (SRM) checks and causal DAG inference
- producing decision-ready quantitative reports with explicit fact vs interpretation separation
- **tracking agent query costs as a FinOps line item** for AI agent data access
- **Apache Ossie (Incubating) universal semantic layer** for vendor-neutral metric portability
- **DuckDB v2.0 readiness** (breaking storage format, VARIANT type, Quack server mode)
- **FastMCP sqlglot AST validation** for anti-hallucination gateway

## Core Rules

- **Read-Only Access**: treat all source tables, lakehouse catalogs, and databases as strictly read-only.
- **Canonical Semantic Layer Precedence**: query metrics exclusively through version-controlled semantic models (dbt MetricFlow, Cube.js, **Apache Ossie**); never invent ad-hoc SQL joins across unverified tables.
- **Apache Ossie (Incubating) Interchange** (July 2026): universal standard for semantic data — vendor-neutral YAML configuration, Apache 2.0, AI-ready semantic context; 50+ organization coalition (Alation, Anomalo, Atlan, AtScale, Bigeye, BlackRock, Blue, Collate, Databao, Denodo, Kyvos, Qlik, Salesforce, Snowflake); enables portable semantic model definitions across MetricFlow, Cube.js, and other semantic layers.
- **FastMCP Anti-Hallucination Gateway** with **sqlglot AST validation**:
  - assert single read-only `SELECT` (prohibit mutations, multi-statements, arbitrary subqueries)
  - enforce join complexity depth ≤ 3 joins to prevent Cartesian fanout and chasm traps
  - enforce hard row limit ≤ 1000 rows
  - honor `agent_accessible: true` allowlist and enforce "Show-The-Definition" attribution (lineage + SQL formula)
  - **MCP Registry Integration** for external tool workflows
- **DuckDB/Polars In-Process Resource Ceilings**:
  - enforce local memory caps: `SET max_memory = '4GB';` with temporary NVMe disk spilling (`/tmp/duckdb_spill`)
  - use zero-copy Apache Arrow C Data Interface between DuckDB and Polars (`con.execute(q).pl()`)
  - evaluate datasets larger than RAM using Polars LazyFrames with streaming engine (`collect(streaming=True)`)
  - **DuckDB v2.0 readiness**: prepare for breaking storage format, VARIANT type support, and Quack server mode for remote query execution
  - **Iceberg extension**: full DML (INSERT/UPDATE/DELETE), process 1TB in 30 seconds
  - **quacklake**: DuckLake catalog on quack deployed to Cloudflare Workers with Durable Objects + JWT auth
- **Agent Query Cost FinOps**: track AI agent query execution costs (token usage, compute time, scanned bytes) as a dedicated FinOps line item; enforce per-agent query cost budgets and alerting thresholds
- **Statistical Distribution Drift Testing**:
  - compute Population Stability Index (PSI) using baseline decile quantile bins: <0.10 (stable), 0.10–0.25 (moderate drift), >0.25 (significant drift; **halt automated pipelines**)
  - run Two-Sample Kolmogorov-Smirnov (KS) tests on continuous metrics; flag shifts when p < 0.01
  - compute non-parametric outlier boundaries using Tukey's IQR fences (Q₁ - 1.5×IQR, Q₃ + 1.5×IQR)
- **Causal Inference & Pearson SRM Pre-Checks**:
  - execute Pearson's Chi-squared SRM test on A/B test sample counts; if p < 0.001, **ABORT EVALUATION IMMEDIATELY**
  - formalize causal hypotheses in DOT-formatted Causal DAGs; identify treatment effects via Backdoor Criterion
  - strictly avoid Collider Bias (Berkson's Paradox): never condition on colliders (T → C ← Y)
  - execute 3-way DoWhy refutations: Placebo Treatment (p > 0.05), Random Common Cause (< 10% shift), Data Subset (< 15% shift)
  - **DoWhy simplified API**: `dowhy.api` for model → estimate → identify → refute workflow
- **Two-Column Table of Evidence**: separate empirical observations (facts) from analytical interpretations in all outputs.
- **Uncertainty Calibration & Provenance**: report 95% confidence intervals, standardized effect sizes, Parquet SHA-256 hashes, and verify 0.00% variance against independent ledger control totals.
- **PII & Security**: classify datasets per `data-classification.yaml`; mask PII; enforce OWASP ASI guardrails.
- **Dosi + Ossie 10-Minute AI Agent Semantic Layer**: CLI, API, and MCP unified — install Dosi, query DuckDB dataset, connect to AI agent over MCP

## Suggested Process

### 1. Frame Question & Query FastMCP Semantic Gateway

Define business decision context, target grain, and time range. Retrieve canonical metrics and dimensions via the FastMCP semantic tool interface. Verify `agent_accessible: true` and obtain underlying SQL formulas. **Query through Apache Ossie interchange format for vendor-neutral semantic model portability.**

### 2. In-Process Profiling via DuckDB/Polars (< 4GB RAM)

Scan partitioned Parquet files or Iceberg snapshots locally using DuckDB with `SET max_memory = '4GB';` and NVMe spill. Profile column null rates, cardinalities, and transfer Arrow batches zero-copy into Polars. **Prepare for DuckDB v2.0 breaking storage format, VARIANT support, and Quack server mode.** Assess DuckLake ACID time-travel via quacklake.

### 3. Execute Statistical Drift & Anomaly Tests

Compute vectorized PSI against historical baseline deciles. Evaluate continuous variables using Two-Sample KS-tests (p < 0.01). Isolate transient spikes using Tukey's IQR fences to score anomalies. **Halt pipelines on PSI > 0.25.**

### 4. Causal Identification, SRM Gate & DoWhy Refutations

For A/B experiments or policy decisions:
1. Run Pearson's Chi-squared SRM pre-check; **halt if p < 0.001**.
2. Construct Causal DAG in DOT format; verify Backdoor Criterion; avoid conditioning on colliders.
3. Estimate Average Treatment Effect (ATE) with 95% CI (or apply CUPED / DML).
4. Subject estimate to Placebo, Random Common Cause, and Data Subset refuters via DoWhy.

### 5. Track Agent Query Costs (FinOps)

Record token usage, compute time, and scanned bytes per agent query. Enforce per-agent cost budgets and alerting. Tag as FinOps line item in `contracts/schemas/data-analysis-report.json`.

### 6. Populate Table of Evidence & Emit Analysis Report

Populate the two-column Table of Evidence separating empirical data from narrative inferences. Validate and emit `contracts/schemas/data-analysis-report.json`.

## Checklist

- [ ] business question, decision context, and temporal grain explicitly framed
- [ ] canonical metrics retrieved from FastMCP / Semantic Layer (dbt MetricFlow / Cube.js / **Apache Ossie**); zero ungrounded ad-hoc joins
- [ ] **Apache Ossie YAML semantic model** authored/imported for all canonical metrics
- [ ] **Ossie interchange format** used for vendor-neutral portability (MetricFlow ↔ Cube.js ↔ Ossie)
- [ ] queries validated via `sqlglot` AST (read-only `SELECT`, join depth ≤ 3, row limit ≤ 1000)
- [ ] `agent_accessible: true` allowlist enforced with Show-The-Definition attribution
- [ ] **MCP Registry integration** for external tool workflows
- [ ] exploratory queries executed in DuckDB/Polars under 4GB RAM limit with out-of-core spilling
- [ ] **Zero-copy Arrow C Data Interface**: `con.execute(q).pl()` DuckDB → Polars
- [ ] **Polars LazyFrames streaming**: `collect(streaming=True)` for >RAM datasets
- [ ] **DuckDB v2.0 readiness assessed**: breaking storage format, VARIANT support, Quack server mode
- [ ] **Iceberg full DML** (INSERT/UPDATE/DELETE) compatibility verified
- [ ] **DuckLake/quacklake** time-travel queries via Cloudflare Workers + Durable Objects
- [ ] statistical distribution drift (PSI, Two-Sample KS-test, IQR fences) calculated and evaluated
- [ ] **PSI > 0.25 triggers pipeline halt**; 0.10–0.25 moderate drift flagged
- [ ] A/B experiments pass Pearson's Chi-squared SRM pre-check (p ≥ 0.001); **aborted if p < 0.001**
- [ ] causal claims backed by DOT Causal DAG, Backdoor adjustment, and 3-way DoWhy refutations
- [ ] **DoWhy 3-way refutations**: Placebo (p > 0.05), Random Common Cause (< 10%), Data Subset (< 15%)
- [ ] deliverables strictly separate empirical facts from analytical interpretations in Table of Evidence
- [ ] point estimates accompanied by 95% confidence intervals and 0.00% variance against ledger control totals
- [ ] input Parquet SHA-256 hashes recorded; PII masked per `data-classification.yaml`
- [ ] report emitted and validated against `contracts/schemas/data-analysis-report.json`
- [ ] **Agent query costs tracked as FinOps line item**: token usage, compute time, scanned bytes
- [ ] **Per-agent query cost budgets** with alerting thresholds enforced
- [ ] **Dosi + Ossie 10-minute AI agent semantic layer** available for agent access

## Related Skills

- **build-data-pipeline**: Reusable ingestion, lakehouse modeling, and production ETL infrastructure
- **analyze-business-requirements**: Align quantitative metrics with business rules and stakeholder outcomes
- **database-maintenance**: Operational lakehouse maintenance, compaction, and read-only query tuning
- **conduct-research**: External benchmarks and industry data when internal datasets are insufficient
- **write-documentation**: Data dictionaries, metric definitions, and analytical knowledge bases

## Output Contracts

When delivering analysis to stakeholders, BI engineers, or downstream agent workflows, emit:

- **`contracts/schemas/data-analysis-report.json`** — structured business context, metric definitions, dataset lineage, findings with fact/interpretation indices, anomalies, drift metrics, causal estimates, recommendations, and agent query costs as FinOps line items (incorporating Apache Ossie semantic models, AST validation rules, and DoWhy causal configurations).
- **`contracts/schemas/data-pipeline-spec.json`** — when data pipeline ingestion, DuckDB/Polars streaming configurations, or lakehouse ETL steps are required.
- Markdown summary brief providing executive findings, narrative context, and recommended decisions.

## Failure Modes

- **Text-to-SQL hallucination**: AI or analyst crafts ad-hoc SQL with invalid join logic or chasm traps. Mitigation: query through FastMCP Semantic Gateway with `sqlglot` AST validation.
- **Reporting SRM-tainted A/B tests**: computing treatment effect when allocation mechanism is corrupt. Mitigation: mandate automated Pearson Chi-squared SRM abort gate (p < 0.001).
- **Conflating correlation with causation**: presenting observational regression as causal proof. Mitigation: enforce Pearl's hierarchy, Causal DAG Backdoor adjustment, and DoWhy refutations.
- **Silent covariate drift**: underlying population shifts invalidate historical conclusions. Mitigation: enforce automated PSI and KS-test distribution drift evaluations before reporting.
- **Unmanaged in-memory spill**: large unpartitioned queries exhaust local RAM. Mitigation: enforce DuckDB `max_memory = '4GB';` and Polars streaming scans.
- **Missing Apache Ossie interchange**: semantic models not portable across vendor layers. Mitigation: adopt Apache Ossie interchange format for vendor-neutral metric portability.
- **Unprepared for DuckDB v2.0**: storage format changes break compatibility. Mitigation: assess breaking storage format, VARIANT support, and Quack server mode readiness.
- **Untracked agent query costs**: AI agent data access lacks FinOps visibility. Mitigation: track token usage, compute time, scanned bytes as dedicated line item.
- **Ossie model drift**: Semantic definitions diverge across tools. Mitigation: Ossie as single source of truth, automated sync validation.
- **DuckDB v2.0 migration break**: Storage format change breaks existing Parquet/Iceberg. Mitigation: Pre-migration compatibility testing, dual-format support during transition.
- **FastMCP bypass**: Agent crafts raw SQL bypassing semantic gateway. Mitigation: Enforce MCP Registry as only access path, audit query logs.
- **SRM-tainted A/B test**: Proceeding with evaluation despite allocation corruption. Mitigation: Hard ABORT gate at p < 0.001, no override.
- **Collider bias in causal inference**: Conditioning on T → C ← Y. Mitigation: DOT DAG verification, automated collider detection.
- **Unbounded agent query costs**: AI agent scans petabytes unchecked. Mitigation: Per-agent budget enforcement, automatic query termination.
- **Quack server mode security**: Remote query execution exposure. Mitigation: JWT auth, Durable Objects isolation, rate limiting.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: classify and mask customer PII; use aggregate summaries in cross-role handoffs.
- **ASI04 Supply Chain**: validate versions of analytics libraries (DuckDB, Polars, scipy, dowhy) against trusted package indexes.
- **ASI05 RCE Guard**: parameterize all analytical scripts; reject string-concatenated SQL queries; enforce AST read-only validation.
- **ASI06 Context & Memory Poisoning**: treat cached analysis and prompt memory as untrusted until verified against live data.
- **ASI07 Inter-Agent Communication**: emit structured `data-analysis-report.json` so downstream decision agents share identical evidence **including agent query costs as FinOps line item**.
- **ASI09 Human-Agent Trust Exploitation**: disclose confidence intervals, statistical limitations, and residual uncertainties honestly.

Last updated: 2026-09-25