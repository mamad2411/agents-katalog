---
name: ml-ai-project-planning
description: "Plan ML/AI projects around decision fit, baselines, data, metrics, guardrails, and phases."
---

# ML AI Project Planning

Plan ML and AI work from the decision, data, risk, and operating model before choosing a model. Use this skill to decide whether ML is appropriate, define success, and create an actionable project card.

## Process

1. Start from the business decision, user, prediction unit, prediction moment, available data, target, latency, cost, audit, privacy, and owner.
2. Check whether deterministic rules, search, a parser, a heuristic, or the current process can solve the problem with lower risk than ML.
3. Quantify false positive, false negative, abstain/no-decision, latency, compute, operational, and review costs.
4. Define how uncertainty is represented and when the system falls back, asks for human review, or refuses to decide.
5. Establish a baseline before proposing complex models. Do not approve large training work without a stable evaluator and baseline.
6. Choose business metrics, model metrics, segment reporting, guardrails, minimum useful improvement, and release acceptance criteria together.
7. Produce a project card or planning report with scope, assumptions, data needs, evaluation plan, phases, risks, and explicit non-goals.

## Coordination

Use with `ml-data-evaluation` when datasets, splits, leakage, metrics, eval datasets, or error analysis are in scope. Use `ml-serving-mlops-review` when rollout, monitoring, retraining, rollback, model cards, or production review are in scope. For Rust/Rig/Candle implementation details, route to the existing `rust-ml-llm-*` skills first.

## Reference Routing

- Problem definition, ML fit, deterministic alternatives, decision owner, error costs, uncertainty, and human handoff: read [01-problem-and-ml-fit.md](./references/01-problem-and-ml-fit.md).
- Business/model metrics, baselines, guardrails, segment reporting, minimum useful improvement, and acceptance criteria: read [02-metrics-baselines-success.md](./references/02-metrics-baselines-success.md).
- Project phases, project-card fields, minimum team standard, scope boundaries, and readiness gates: read [03-project-card-and-phases.md](./references/03-project-card-and-phases.md).

## Version Policy

- Existing repo: inspect pinned languages, frameworks, model providers, data tools, lockfiles, configs, and CI before recommending concrete tools or commands.
- New project or version-sensitive choice: use `itsol-current-tech-context` to verify current official guidance before naming package versions or provider-specific APIs.
- Keep project plans tool-agnostic unless the repo or user already chose a stack.
