---
name: ml-serving-mlops-review
description: "Review ML serving changes to contracts, parity, artifacts, rollout, monitoring, or lineage."
---

# ML Serving MLOps Review

Use this skill for production ML serving, MLOps, deployment review, monitoring, retraining, model cards, release gates, and ML debugging triage.

## Trigger boundary

Use this skill when a production ML serving or MLOps change affects serving mode, model/input/output contracts, train-serving parity, artifacts/registry, rollout or rollback, monitoring/drift, retraining, lineage, model cards, or release gates.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no serving, model artifact, deployment, monitoring, lineage, retraining, or release impact; follow the repository's established convention directly.

## Process

1. Identify the serving mode: batch, online, streaming, edge, embedded library, managed provider, or model server.
2. Inspect model contracts, input/output validation, feature manifests, preprocessing versions, artifact formats, fallback behavior, and train-serving parity tests.
3. For real project work, detect repo-pinned model/runtime/framework versions first. Use `itsol-current-tech-context` for current official docs before judging fast-moving model-serving APIs, registries, providers, or security defaults.
4. If Rust/Rig/Candle/provider runtime code is the primary surface, route first to `rust-ml-llm-architecture`, `rust-ml-llm-debugging`, or `rust-ml-llm-review`; use this skill for cross-cutting serving, MLOps, rollout, monitoring, and review concerns.
5. Lead review output with concrete findings, severity, affected behavior, missing verification, rollback risk, and file references.

## Evidence

Prefer model contracts, schema tests, parity tests, registry records, model cards, CI logs, training run metadata, deployment manifests, monitoring dashboards, incident logs, eval reports, and release approvals over assumptions.

## Focused References

- [01-serving-contracts-parity.md](./references/01-serving-contracts-parity.md) - serving modes, contracts, validation, train-serving parity, batching, scaling, fallback, and model formats.
- [02-deployment-monitoring-retraining.md](./references/02-deployment-monitoring-retraining.md) - shadow, canary, A/B, champion/challenger, rollback, monitoring, drift, and retraining.
- [03-lineage-model-cards-ci.md](./references/03-lineage-model-cards-ci.md) - lineage, registry records, model cards, CI/CD jobs, training pipeline gates, and promotion checks.
- [04-security-privacy-fairness.md](./references/04-security-privacy-fairness.md) - data privacy, supply chain, model attacks, LLM/agent security, risk management, and segment fairness.
- [05-debugging-and-review.md](./references/05-debugging-and-review.md) - debugging symptoms, edge cases, ML testing, ML Test Score readiness, and large ML PR review split.
