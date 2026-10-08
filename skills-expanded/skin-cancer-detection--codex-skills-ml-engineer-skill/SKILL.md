---
name: ml-engineer
description: Build, serve, monitor, and scale production machine learning systems. Use when the task involves training infrastructure, model serving, feature pipelines, experiment tracking, online or batch inference, ML observability, or deployment tradeoffs.
---

# ML Engineer

## Quick Start

1. Define the prediction task, serving pattern, and business success metric.
2. Separate concerns across data prep, training, validation, registry, and inference.
3. Design for reproducibility, rollback, and monitoring before optimizing throughput.
4. Implement with explicit data contracts and model versioning.
5. Validate both model quality and operational behavior.

## Workflow

### Design the system

- Decide whether the workload is batch, streaming, synchronous, or asynchronous.
- Keep training-time and serving-time feature logic aligned.
- Choose model packaging and deployment paths that match the runtime environment.

### Build for operations

- Version datasets, features, models, configs, and metrics together.
- Add validation around schemas, feature freshness, and model input shape.
- Plan for rollback, shadow traffic, or canary release before broad rollout.
- Monitor latency, throughput, drift, error rate, and business KPIs separately.

### Validate the result

- Run offline evaluation with leakage-aware splits.
- Test inference paths with realistic payloads and failure cases.
- Report system limits, retraining triggers, and operational ownership.

## Deliverables

- A production-minded ML system design or implementation.
- Clear tradeoffs across quality, cost, latency, and maintenance.
- A rollout and monitoring plan tied to the model lifecycle.
