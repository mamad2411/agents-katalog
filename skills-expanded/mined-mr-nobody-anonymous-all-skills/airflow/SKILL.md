---
name: airflow
description: "Apache Airflow: Directed Acyclic Graphs (DAGs), task dependencies, sensors, custom operators, XComs, and Celery/Kubernetes executors"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/airflow/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Apache Airflow Orchestration

## Scope
Apache Airflow authoring, programmatic workflow scheduling, task dependency definition, SLA monitoring, and scalable distributed executor management.

## Core Concepts & Invariants
- **DAG Definition Invariants**:
  - DAG files must be lightweight and free of top-level code or database calls (parsed repeatedly by scheduler).
  - Deterministic execution date (`data_interval_start`, `data_interval_end`).
- **Task Dependencies**: Upstream/downstream bitshift operators: `extract >> transform >> load`.
- **Executors**: CeleryExecutor (Redis/RabbitMQ queue), KubernetesExecutor (dynamic ephemeral pod per task).

## Tools & Standards
- **Software**: Apache Airflow 2.x, Astronomer.
