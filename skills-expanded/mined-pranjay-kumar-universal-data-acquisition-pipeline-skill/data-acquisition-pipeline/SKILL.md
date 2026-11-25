---
name: data-acquisition-pipeline
description: "Use when the user wants a production-grade scraping/API/browser pipeline design or implementation plan: pipeline.yaml, schemas, raw/staged/normalized outputs, dedupe, incremental refresh, checkpoints, retries, rate-limit strategy, quality gates, observability, run reports, and recovery."
---

# Data Acquisition Pipeline

Act as the pipeline architect. Turn known or proposed sources into a restartable, observable, quality-checked pipeline.

## Shared Core

Read from `../data-acquisition-core/references/`:

- `pipeline-engineering.md`
- `source-access.md`
- `output-contracts.md`
- `source-strategies.md`
- `compliance-boundaries.md`

## Output

Return:

- `SourceAccessClass`
- `PipelineQualityPlan`
- `PipelinePlan`
- schema
- output layout
- run report shape
- validation gates
- `ApprovalGate`

If implementing, keep secrets local and outputs incremental.
