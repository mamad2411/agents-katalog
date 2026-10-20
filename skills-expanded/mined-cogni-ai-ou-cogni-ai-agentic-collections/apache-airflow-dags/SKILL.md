---
name: apache-airflow-dags
description: 'Expert-level guide for authoring Apache Airflow Dags, focusing on the skeleton strategy, contract-driven logic, and environment context. You MUST load this skill when asked to write, refactor, or structure Airflow Dags.'
license: MIT
---

# Apache Airflow Dags

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- Generating or writing new Apache Airflow Dags.
- Refactoring, debugging, or analyzing existing Airflow Dags.
- Architecting data pipelines using Airflow's TaskFlow API.

## WHEN NOT TO USE

- Interacting with the Airflow REST API to trigger Dag runs or manage connections (use `apache-airflow-api` instead).

## Core Process

1. **Define the Universe**: Explicitly declare the context (Airflow version, executor type, cloud provider, and constraints) before generating code to avoid deprecated syntax.
2. **Apply the Skeleton Strategy**:
   - Step 1: Draft the high-level plan in natural language without generating code.
   - Step 2: Generate the Dag structure graph using placeholders (e.g., `EmptyOperator` from `airflow.providers.standard.operators.empty`). Do not add business logic or documentation yet.
   - Step 3: Iteratively replace placeholders with actual business logic and TaskFlow decorators.
   - Step 4: Add selective comments explaining the *why* (not the *what*), configure retries, and set up notifications.
3. **Establish Data Contracts**: Specify explicit input schemas, output targets, and idempotency constraints (e.g., using `MERGE` or `UPSERT`) rather than vague transformation requests.
4. **Format as a Technical Spec**: Structure requests and workflows using Markdown headers (`## Goal`, `## Context`, `## Data Contract`) and pseudo-XML tags (`<schema>`, `<code_snippet>`) for raw data.
5. **Force the Source of Truth**: Inject exact snippets from official documentation (e.g., `llms.txt`) to anchor the execution and prevent context contamination from older Airflow versions.

## Naming Conventions & Grammar

- Write **Dag** (title case) in all prose.
- Keep the all-caps or lowercase spelling only when reproducing a literal code token — never rewrite these, even inside fenced code blocks:
  - Python: the SDK class `DAG` (`from airflow.sdk import DAG`, `dag = DAG("my_dag", ...)`); identifiers like `dag_id`, `dag`, `my_dag`.
  - CLI: `airflow dags list`, `airflow dags test`, etc.
  - Paths and config keys: `dag_processing/`, `dagprocessor`, `get_dag`, etc.
- Don't spell out **Directed Acyclic Graph** except for historical context.

## Architecture Boundaries

1. Users author Dags with the Task SDK (`airflow.sdk`).
2. Dag File Processor parses Dag files in separate processes and stores serialized Dags in the metadata DB. Software guards prevent individual parsing processes from accessing the database directly and enforce use of the Execution API.
3. Scheduler reads serialized Dags — **never runs user code** — and creates Dag runs / task instances.
4. Workers execute tasks via Task SDK and communicate with the API server through the Execution API — **never access the metadata DB directly**. Each task receives a short-lived JWT token scoped to its task instance ID.
5. Triggerer evaluates deferred tasks/sensors in separate processes, steering through the Execution API rather than direct database access.

## Core Principles

- **Code is a Liability**: Auto-generated code without clear guardrails leads to maintainability issues. Ensure the *why* and the *schema constraints* are thoroughly defined.
- **Context is King**: Always prioritize explicit constraints over general assumptions, matching the target environment perfectly.

## Best Practices

- **Use Golden Records**: Reference established, production-ready Dags (golden records) to enforce organizational naming conventions and architectural patterns.
- **Embrace TaskFlow API**: Leverage `@task` and `@dag` decorators for cleaner data passing over legacy XCom patterns, unless constrained otherwise.

## What to Avoid

- **Vibe Coding Large Blocks**: Generating hundreds of lines of Dag logic in a single shot without verifying the structural skeleton first.
- **Over-commenting**: Creating comments that simply narrate Python syntax.
- **Assuming Idempotency**: Never assume a task will automatically be idempotent; explicitly define boundaries like `logical_date` and insert strategies.

## Common Pitfalls

- **Context Contamination**: Defaulting to deprecated Airflow paradigms (e.g., `schedule_interval` instead of `schedule` or `timetable`). *Prevention: Always define the target Airflow version (e.g., Airflow 3.1) in the context block.*
- **Hallucinated Schemas**: Generating column names or relationships that do not exist. *Prevention: Use contract-driven definitions with explicit schemas.*
- **Missing Provider Packages**: Referencing operators that the environment lacks. *Prevention: Verify that the imported operators align with the available or defined providers.*

## References

Examples from <https://airflow.apache.org/docs/task-sdk/stable/examples.html>:

- [example_asset_alias.py](references/example_asset_alias.py)
- [example_assets.py](references/example_assets.py)
- [example_dag_decorator.py](references/example_dag_decorator.py)
- [example_dynamic_task_mapping.py](references/example_dynamic_task_mapping.py)
- [example_setup_teardown_taskflow.py](references/example_setup_teardown_taskflow.py)
- [example_task_group_decorator.py](references/example_task_group_decorator.py)
- [example_xcomargs.py](references/example_xcomargs.py)

Examples from: <https://github.com/astronomer/webinar-demos/tree/local-data-engineering/dags>:

- [customer_stats.py](references/customer_stats.py)
- [daily_report.py](references/daily_report.py)
- [route_performance.py](references/route_performance.py)
- [tutorial_taskflow_api.py](references/tutorial_taskflow_api.py)
