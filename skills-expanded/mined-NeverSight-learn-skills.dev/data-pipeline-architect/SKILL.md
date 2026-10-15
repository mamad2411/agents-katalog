---
name: data-pipeline-architect
description: >-
  Analyzes and designs batch and streaming data pipelines with contracts,
  lineage, reliability, and cost controls. Use for ingestion and
  transformation systems. NOT for ad-hoc analysis or schema design.
argument-hint: "<mode> [pipeline]"
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Data Pipeline Architect

Design resilient data movement and transformation systems for batch, streaming,
and hybrid workloads.

**Scope:** Ingestion, transformation, serving-path pipeline design, and
operational controls. NOT for ad-hoc analytics (data-wizard) or database schema
design (database-architect).

## Canonical Vocabulary

| Term | Definition |
|------|------------|
| **source** | Upstream system producing data |
| **sink** | Destination system receiving data |
| **batch window** | Time slice processed as a single scheduled unit |
| **watermark** | Progress marker used to reason about event-time completeness |
| **data contract** | Agreement on schema, semantics, freshness, and quality |
| **checkpoint** | Persisted progress state used for restart and recovery |
| **late data** | Records arriving after their expected processing window |
| **quarantine** | Isolated holding area for invalid or suspicious records |
| **lineage** | Trace from source records through transformations to outputs |
| **replay** | Reprocessing data from a prior point in time |

## Dispatch

| $ARGUMENTS | Mode |
|------------|------|
| `design <pipeline>` | Design a new batch or streaming pipeline |
| `review <pipeline or architecture>` | Audit an existing pipeline |
| `operate <issue>` | Improve reliability, monitoring, and recovery |
| `migrate <change>` | Plan a pipeline migration or re-platform |
| `contract <dataset>` | Define a producer-consumer data contract |
| Natural language about ingestion, ETL, ELT, or streaming | Auto-detect the closest mode |
| Empty | Show the mode menu with examples |

## References

| File | Purpose |
|------|---------|
| `references/decision-matrix.md` | Choose batch vs streaming vs hybrid, contract style, and replay posture |
| `references/failure-modes.md` | Common pipeline failure modes, symptoms, and design controls |
| `references/worked-examples.md` | Worked examples for common ingestion and transformation patterns |
| `references/output-templates.md` | Reusable output shapes for each public mode |

## Mode Menu

| # | Mode | Example |
|---|------|---------|
| 1 | Design | `design clickstream ingestion to warehouse and feature store` |
| 2 | Review | `review nightly billing ETL architecture` |
| 3 | Operate | `operate strategy for backfills and failed partitions` |
| 4 | Migrate | `migrate from cron scripts to orchestrated pipeline` |
| 5 | Contract | `contract orders fact table feed` |

## When to Use

- Designing ingestion from APIs, files, databases, or event streams
- Choosing between batch, streaming, or hybrid data movement
- Defining data contracts, lineage, and recovery strategy
- Reviewing a pipeline with freshness, quality, or cost issues
- Planning backfills, replays, or platform migrations

## Classification Logic

Use this gate before selecting a mode:

1. If the task is primarily database schema modeling, table design, or index strategy, use `database-architect`.
2. If the task is primarily BI analysis, metric interpretation, or dashboard storytelling on produced data, use `data-wizard`.
3. If the task is primarily vendor setup, cluster provisioning, broker administration, or deployment wiring, use `devops-engineer` or `infrastructure-coder`.
4. If the task is primarily incident command or outage coordination for a broken pipeline, use `incident-response-engineer`.
5. If the task is primarily service-wide telemetry architecture rather than pipeline controls, use `observability-advisor`.

## Instructions

### Mode: Design

1. Identify sources, sinks, latency expectations, data volume, correctness requirements, and downstream consumers.
2. Choose the processing model: batch, streaming, or hybrid.
3. Use `references/decision-matrix.md` if the processing model, handoff contract, or replay posture is not obvious.
4. Define the stages: ingest, validate, normalize, transform, publish, and monitor.
4. Write the data contract for every handoff, including schema, quality checks, freshness target, and ownership.
5. Specify checkpointing, replay strategy, late-data handling, and quarantine behavior.
6. Produce the architecture with observability and cost controls.

### Mode: Review

1. Read the pipeline description, orchestration flow, and dataset interfaces.
2. Check for weak contracts, silent data loss, poor retry boundaries, unclear lineage, or no replay strategy.
3. Flag reliability, quality, cost, and operability issues separately.
4. Use `references/failure-modes.md` to pressure-test likely blind spots before concluding the review.

### Mode: Operate

1. Define the pipeline SLOs: freshness, success rate, and data quality thresholds.
2. Specify what is checkpointed, what is retried, and what is quarantined.
3. Design backfill and replay paths that do not interfere with the live path.
4. Recommend dashboards and alerts tied to business-significant failure modes.
5. Keep live and replay state transitions explicit so operators can reason about what data is safe to re-run.

### Mode: Migrate

1. Map the current state and pain points: cron jobs, brittle scripts, hidden contracts, or platform lock-in.
2. Preserve source-of-truth semantics while moving stages one at a time.
3. Define coexistence, validation, and rollback for the migration window.
4. Separate migration-state bookkeeping from business output state so cutover validation stays auditable.

### Mode: Contract

1. Define the dataset owner, schema versioning rule, freshness target, and required validations.
2. Name breaking and non-breaking changes explicitly.
3. State what invalid records look like and how they are handled.
4. Define replay and backfill expectations for consumers when contract versions change.

## Output Requirements

- Every design must name the processing model and the contract at each boundary.
- Every review must separate reliability, data quality, and cost findings.
- Every operate plan must include checkpointing, replay, and quarantine.
- Every migration plan must name coexistence boundaries, rollback triggers, and validation checkpoints.
- Every contract must name ownership, freshness, versioning, and invalid-record handling.

## Critical Rules

1. Every producer-consumer boundary must have an explicit data contract.
2. Pipelines must define how invalid records are quarantined or rejected.
3. Backfills and replays must be designed separately from the live path.
4. Freshness and quality targets must be measurable, not implied.
5. If the task is primarily analysis on the produced data, route it to data-wizard.

## Scaling Strategy

- Small: single-source or single-sink batch flow. Favor one durable checkpoint boundary, one batch cadence, and one clear replay path before adding more stages.
- Medium: multi-stage batch or micro-batch flow. Add stage-level contracts, separate publish boundaries, and batch-oriented validation between stages.
- Large: hybrid or streaming flow with multiple consumers. Define watermark, late-data policy, backfill isolation, and parallel recovery boundaries before recommending the topology.
- Large migration or platform change: treat coexistence, replay, and cutover as separate batch workstreams rather than one big rewrite.

## State Management

- Persist checkpoint state at every recovery boundary so operators know what can be retried, replayed, or skipped safely.
- Track watermark or batch-window progress separately from business output state so late data and replay are visible instead of inferred.
- Keep quarantine metadata, contract version, and lineage references alongside failed or replayed records so recovery decisions are auditable.
- Define idempotency expectations for ingest, transform, and publish stages before recommending retries or dual-run migrations.

## Progressive Disclosure

- Start with the mode contract in this file and only load the reference file that resolves the current uncertainty.
- Use `references/decision-matrix.md` when the topology or replay posture is the open question.
- Use `references/failure-modes.md` when reviewing reliability, quality drift, or operator burden.
- Use `references/worked-examples.md` when the user needs a concrete pattern to adapt.
- Use `references/output-templates.md` when the user needs a structured response shape.

## Scope Boundaries

**IS for:** ingestion architecture, orchestration boundaries, reliability strategy, data contracts, lineage, replay, migration planning.

**NOT for:** ad-hoc analytics, BI storytelling, low-level DBA work, or greenfield schema modeling.
