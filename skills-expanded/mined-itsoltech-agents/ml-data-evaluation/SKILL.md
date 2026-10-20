---
name: ml-data-evaluation
description: "Evaluate ML data and models for leakage, splits, metrics, calibration, and errors."
---

# ML Data Evaluation

Design and review ML datasets, data contracts, split strategy, metrics, eval datasets, and error analysis as first-class engineering artifacts.

## Process

1. Treat data as a product: identify owner, source, license, privacy constraints, schema, freshness, lineage, update cadence, retention, and permitted uses.
2. Create or review a datasheet, data contract, validation checks, immutable raw layer, manifests, checksums, and versioned transformation outputs.
3. Choose splits that match production use. Freeze the test set and do not use it for feature selection, threshold tuning, model selection, or repeated experiment feedback.
4. Check leakage before trusting any metric: point-in-time availability, duplicate and near-duplicate records, group/time contamination, target encoding, preprocessing order, synthetic data, and benchmark contamination.
5. Select metrics by task and business cost. Report segment results, calibration, confidence or variance, challenge set behavior, and operational cost.
6. For LLM and generative systems, separate retrieval, generation, deterministic scorers, human review, LLM judge calibration, safety tests, and private domain evals.
7. Add data/eval testing evidence before recommending model or deployment decisions.

## Coordination

Use with `ml-ai-project-planning` when the business decision, baseline, or project card is still unclear. Use with `ml-training-experiments` for experiment tracking and training reproducibility. Use with `ml-llm-rag-engineering` for RAG, LLM judges, generated-output validation, and agent evals. Use `ml-serving-mlops-review` when production monitoring, retraining, rollback, or model cards are in scope.

## Reference Routing

- Data as product, dataset layers, datasheets, ownership, data contracts, validation, lineage, manifests, and quality gates: read [01-data-product-contracts.md](./references/01-data-product-contracts.md).
- Split strategy, test set discipline, leakage checks, large data formats, partitioning, lazy execution, streaming, incremental processing, and sampling: read [02-splits-leakage-large-data.md](./references/02-splits-leakage-large-data.md).
- Task metrics, calibration, LLM/generative eval datasets, benchmark pitfalls, error analysis, and data/eval testing: read [03-metrics-error-analysis-evals.md](./references/03-metrics-error-analysis-evals.md).

## Version Policy

- Existing repo: inspect pinned data frameworks, storage formats, validation libraries, orchestration, evaluation harnesses, lockfiles, and CI before recommending commands or APIs.
- New project or version-sensitive choice: use `itsol-current-tech-context` to verify current official guidance before naming package versions or provider-specific APIs.
- Keep evaluation conclusions tied to the observed data, manifest, split, config, and metric implementation version.
