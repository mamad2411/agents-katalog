---
name: pipeline-orchestration
description: |
  General pipeline orchestration for NON-Airflow tools (Dagster, Prefect, custom schedulers).
  Use when: the user mentions Dagster, Prefect, Luigi, or custom pipeline orchestration.
  Do NOT use for Airflow — use `airflow` or `authoring-dags` instead.
  Do NOT use for dbt — use `creating-dbt-models` or `developing-incremental-models` instead.
metadata:
  author: dataops-agent
  version: "2.0.0"
---

# Pipeline Orchestration (Non-Airflow)

For **Airflow**, use the dedicated skills: `airflow`, `authoring-dags`, `debugging-dags`, `testing-dags`, `deploying-airflow`.

For **dbt**, use: `creating-dbt-models`, `developing-incremental-models`, `refactoring-dbt-models`.

This skill covers orchestration tools **outside** the Airflow ecosystem.

## When to Apply
Use this skill when:
- Creating or refactoring Dagster pipelines (assets, ops, graphs)
- Building Prefect flows and tasks
- Implementing Luigi pipelines
- Designing custom cron-based or event-driven orchestration
- Migrating between non-Airflow orchestrators
- Comparing orchestration tools for a new project

## Best Practices
1. **Idempotency**: Ensure all tasks and pipelines are idempotent so they can be safely retried.
2. **Separation of Concerns**: Keep the orchestrator layer separate from the execution logic.
3. **Dynamic Generation**: Use dynamic pipeline generation when dealing with repetitive tasks.
4. **Alerting**: Configure appropriate SLA misses and failure callbacks.

## Execution Pattern
1. Analyze the pipeline structure and requirements.
2. Ensure proper dependency graphs are built.
3. Validate idempotency and retry mechanics.
4. Output the code or configuration needed.
