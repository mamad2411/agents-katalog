# Jax Skills Starter Prompt

Use this as a quick router before doing work in this repo.

## One-shot routing prompt

```text
You are working in jax-trading-assistant.
First choose the minimum set of skills needed, then execute in order.

If request is about file targeting/scope/safety, use: jax-repo-guardrails.
If request changes Go backend code, use: jax-go-change-workflow.
If request may change behavior (signals/execution/orchestration), use: jax-golden-replay-regression.
If request touches orchestration flows/contracts, use: jax-orchestration-pipeline.
If request changes frontend API usage/hooks/data adapters, use: jax-frontend-api-contracts.
If request is ADR-0012 migration work, use: jax-adr0012-migration.
If request is runtime/startup/debugging issue, use: jax-debug-runbook.
If request is knowledge DB/schema/ingest, use: jax-knowledge-ingest.

Always:
1) Explain selected skill(s) and order in one line.
2) Keep edits minimal and scoped.
3) Run the smallest valid verification set.
4) Report commands run and skipped.
```

## Suggested order when multiple skills apply

1. `jax-repo-guardrails`
2. domain skill (one of: `jax-go-change-workflow`, `jax-frontend-api-contracts`, `jax-orchestration-pipeline`, `jax-knowledge-ingest`, `jax-adr0012-migration`, `jax-debug-runbook`)
3. `jax-golden-replay-regression` (only if behavior-sensitive)

## Quick examples

- "Fix bug in trade sizing logic":
  - `jax-repo-guardrails` -> `jax-go-change-workflow` -> `jax-golden-replay-regression`

- "Why orchestration endpoint fails on AAPL run":
  - `jax-repo-guardrails` -> `jax-orchestration-pipeline` -> `jax-debug-runbook`

- "Add new backend field used by dashboard hook":
  - `jax-repo-guardrails` -> `jax-go-change-workflow` -> `jax-frontend-api-contracts`

- "Ingest new strategy docs into knowledge DB":
  - `jax-repo-guardrails` -> `jax-knowledge-ingest`
