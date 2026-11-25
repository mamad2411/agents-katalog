---
name: elt
description: "Extract, Load, Transform architecture, raw data lake ingestion, in-warehouse transformations with dbt, and modular data modeling"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/elt/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# ELT Architecture & Modern Data Stack

## Scope
ELT decouples extraction/loading from transformation by landing raw schemaless data directly into scalable cloud warehouses (Snowflake, BigQuery) before transforming in-place via SQL.

## ELT Design Patterns
- **Three-Tier Modeling Architecture**:
  1. *Raw / Landing Layer*: Immutable source dumps (`raw.stripe_charges`).
  2. *Staging / Intermediate Layer*: Cleaned, renamed, typed views (`stg_stripe__charges`).
  3. *Marts / Dimensional Layer*: Business-facing facts and dimensions modeled with Kimball star schema (`fct_mrr`, `dim_customers`).
- **dbt Transformation Engine**: Declarative version-controlled SQL models, `ref()` dependency graph resolution, automated schema tests (`unique`, `not_null`).

## Tools & Standards
- **Software**: dbt (data build tool), Fivetran, Snowflake, Google BigQuery.
