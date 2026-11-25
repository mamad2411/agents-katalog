---
name: dbt-modeling
description: Builds dbt models in staging, intermediate and mart layers with tests and generated docs. Use it when adding or restructuring warehouse transformations.
---

# dbt modeling

One model, one purpose. Tests and docs ship with the model.

## Steps

1. Read `dbt_project.yml` and two existing models to learn the naming, folder layout and default materializations. Match them.
2. Declare the raw tables in a `sources.yml` with a `loaded_at_field` and a freshness rule where one exists.
3. Staging (`stg_<source>__<table>`): one model per source table, `{{ source() }}` only here. Rename columns to snake case, cast types, convert timestamps to UTC, and do no joins or aggregation. Materialize as view.
4. Intermediate (`int_<entity>__<verb>`): joins, deduplication and reusable logic. Reference upstream models with `{{ ref() }}` only.
5. Marts (`dim_` and `fct_`): one grain per table, stated in the description. Materialize as table, or incremental with a `unique_key` and a lookback filter for large facts.
6. Write the YAML next to each model: a description, and tests on every key (`unique`, `not_null`), foreign keys (`relationships`), and enums (`accepted_values`).
7. Run `dbt build --select +<model>` and read the failures. Fix the model, not the test, unless the test is wrong.
8. Run `dbt docs generate` if the project publishes docs.

## Rules

- No `select *` in marts. List columns.
- Do not hardcode schema names; use refs.
- Keep logic out of YAML tests; put it in singular tests under `tests/`.

## Report

Models created with their layer and grain, tests added, `dbt build` result, and any data problem the tests exposed.
