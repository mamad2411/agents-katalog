---
name: beam-runner-choice
description: >
  Choose Apache Beam runners for owned pipelines: DirectRunner, DataflowRunner,
  FlinkRunner, SparkRunner, and PortableRunner trade-offs for features, cost,
  latency, and ops. Use when designing or migrating Beam pipelines — not for
  unauthorized jobs on shared clusters.
---

# Apache Beam Runner Choice

## Scope And Authorization

- **In scope:** Pipelines and runners in projects/clusters you own or are authorized to use.
- **Out of scope:** Submitting jobs to third-party Dataflow/Flink without approval; data exfil via pipelines.
- Runner choice affects exactly-once, autoscaling, and connectors — validate SLAs.
- Use `code-quality-standards` for pipeline code; cloud identity skills for execution SA/MI.

## When To Use

- New streaming/batch pipeline: which runner to target.
- Moving from DirectRunner prototypes to managed Dataflow or self-managed Flink.
- Feature gaps (timers, state, SDF, draining) driving runner selection.
- Cost/latency comparison for the same pipeline graph.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Bigtable key design for sinks | `bigtable-row-key-design` |
| Backpressure general patterns | `backpressure-patterns` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Runner | Typical fit |
| --- | --- |
| DirectRunner | Local unit/integration tests; small data |
| DataflowRunner | Managed GCP batch/stream; autoscaling |
| FlinkRunner | Self-managed / Amazon managed Flink; low-latency stream |
| SparkRunner | Batch-oriented Spark shops |
| PortableRunner / Samza / others | Multi-language portability needs |
| Tooling | Apache Beam SDK, `PipelineOptions`, cloud consoles, metrics |

## Workflow

### 1. Confirm scope and success criteria

1. Batch vs streaming, peak throughput, latency SLO, stateful needs, cloud preference, authorization.
2. Success: runner selected with ADR; pipeline passes integration tests on that runner; cost estimate accepted.
3. Portable coding standards: avoid runner-specific transforms when possible.

### 2. Inventory pipeline requirements

```text
- Sources/sinks: Pub/Sub, Kafka, Files, BigQuery, Bigtable, JDBC...
- Windowing / triggers / state / timers
- Languages: Java / Python / Go
- Exactly-once vs at-least-once acceptable?
- Max runtime / streaming 24/7?
```

1. List Beam features used (`StatefulDoFn`, SDF, side inputs size).
2. Note org platform standards (only Dataflow allowed?).
3. Data residency constraints.

### 3. Baseline prototype

```bash
# Local correctness
mvn test
# or
python -m pytest
# Run small job with DirectRunner
```

1. Measure shape of data skew and large side inputs.
2. Identify non-serializable DoFn state bugs early.

### 4. Choose and configure runner

**Decision matrix (simplified):**

| Requirement | Prefer |
| --- | --- |
| Managed ops on GCP | Dataflow |
| Existing Flink platform | FlinkRunner |
| Heavy batch Spark SQL estate | SparkRunner (evaluate feature gaps) |
| CI unit tests | DirectRunner |
| Multi-lang portability | Portable runner ecosystem |

```bash
# Dataflow example (Java)
mvn -Pdataflow-runner compile exec:java \
  -Dexec.args="--runner=DataflowRunner --project=$PROJECT --region=$REGION --tempLocation=gs://$BUCKET/tmp"
```

```python
# Python options sketch
options = PipelineOptions([
    "--runner=DataflowRunner",
    f"--project={project}",
    f"--region={region}",
    f"--temp_location=gs://{bucket}/tmp",
    "--streaming",
])
```

1. Service account/MI least privilege for data sources/sinks.
2. Enable streaming engine / prime features only with cost awareness (Dataflow).
3. Checkpointing/savepoints strategy on Flink.
4. Avoid DirectRunner assumptions (single machine order) in production logic.

### 5. Verify with evidence

1. Integration job on target runner with production-like windows.
2. Failure injection: worker loss → pipeline recovers per model.
3. Metrics: system lag, throughput, shuffle cost.
4. Cost report for 24h soak vs estimate.

### 6. Observe and harden

1. Alerts on data freshness / DLQ sizes / job failed.
2. Upgrade Beam SDK + runner versions on schedule.
3. Cap max workers; budget alerts.

### 7. Hand off

1. ADR: runner choice and rejected alternatives.
2. Runbook: drain/update/cancel job.
3. IAM for launcher vs runtime identities.

## Feature Caution List

| Feature | Validate on runner |
| --- | --- |
| Exact-once sinks | Runner + sink combo |
| Large side inputs | Memory strategy |
| Custom windows | Support maturity |
| Python streaming | Performance expectations |
| Cross-language | Portable protocol versions |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Prototype | DirectRunner tests | Only tested in prod Dataflow |
| IAM | Scoped runtime SA | User creds for jobs |
| Code | Runner-agnostic transforms | Hard-coded Dataflow options in library code |
| Cost | Max workers + budget | Unbounded autoscaling surprise |
| State | Sized and TTL’d | Unbounded per-key state |

## Output Checklist

- [ ] Requirements (batch/stream/SLA) documented
- [ ] Feature compatibility checked for candidate runners
- [ ] ADR records chosen runner
- [ ] Pipeline runs successfully on that runner
- [ ] IAM least privilege configured
- [ ] Metrics/alerts set
- [ ] Cost controls applied
- [ ] `code-quality-standards` applied to pipeline code

## Rules

- Authorized projects/clusters only.
- Don’t assume DirectRunner semantics in prod.
- Validate sinks for delivery guarantees.
- Least privilege execution identities.
- Document and revisit runner choice when SLOs change.
