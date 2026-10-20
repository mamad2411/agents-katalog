---
name: dbt-fabric-patterns
description: >
  Practitioner-level dbt patterns for Microsoft Fabric. Covers materialization
  decisions, incremental model gotchas, snapshot strategies, selector/tag
  patterns, ref() chain rules, and Fabric-specific T-SQL quirks. Use when
  writing, reviewing, or debugging dbt models on Fabric. Also use when setting
  up dbt_project.yml configuration or CI/CD pipelines for dbt-fabric projects.
tools: Read, Write, Edit, Glob, Grep, Bash
type: platform
domain: dbt on Microsoft Fabric
version: 1.0.5
---

# dbt on Fabric — Practitioner Patterns

Hard-to-find patterns for running dbt on Microsoft Fabric. Focuses on what Context7 and official docs don't cover well: Fabric-specific divergences, common LLM mistakes, and decision frameworks for materialization, incremental models, and snapshots.

## Quick Reference

The patterns most likely to prevent mistakes:

### Materialization by layer

| Layer | Default | When to change |
|---|---|---|
| Staging (`stg_`) | `view` | Never — staging is always a view |
| Intermediate (`int_`) | `view` | Use `table` if query is expensive and referenced multiple times. **Never `ephemeral`** — unsupported on Fabric |
| Marts (`fct_`/`dim_`) | `table` | Use `incremental` when source volume exceeds ~1M rows or query time exceeds 60s |
| Snapshots | `snapshot` | Always — this is a dedicated materialization type |

### Incremental model checklist

Before writing an incremental model, answer these:
1. **What is the `unique_key`?** Single column preferred. Composite keys need ALL columns — omitting one causes silent duplicates.
2. **What is the merge strategy?** Default to `merge` on Fabric. It requires `unique_key`.
3. **What is the lookback window?** `is_incremental()` is false on first run. Late-arriving data needs a lookback buffer (typically 3 days).
4. **What happens on schema change?** Plan for `--full-refresh` when adding columns. Schedule periodic full refreshes.

### ref() chain rules

```
source() → stg_ → int_ → fct_/dim_
           ↑               ↑
     ONLY layer that   Can ref other marts
     uses source()     (no circular refs)
```

- `source()` is used ONLY in staging models. Everything else uses `ref()`.
- Cross-project refs: `{{ ref('other_project', 'model_name') }}`.
- Circular refs are a hard error — break cycles with intermediate models.

### Fabric divergences from Snowflake/Postgres

| Pattern | Snowflake/Postgres | Fabric |
|---|---|---|
| Ephemeral models | Supported | **Unsupported** — use views instead |
| Utils package | `dbt-utils` | **`tsql-utils`** — different macro signatures |
| Authentication | Various | **ServicePrincipal only** — no SQL auth |
| Table format | Various | **Delta mandatory** |
| Write path | Direct SQL | SQL analytics endpoint is **read-only** — dbt writes via the warehouse endpoint |

## Anti-patterns

What LLMs consistently get wrong with dbt on Fabric:

- **`dbt-utils` on Fabric** — must use `tsql-utils`. Macro names look similar but signatures differ.
- **Ephemeral materialization** — unsupported by dbt-fabric adapter. Use views.
- **`source()` outside staging** — only `stg_` models use `source()`. Marts use `ref()`.
- **Joins in staging** — staging is 1:1 with source tables. No joins, no business logic.
- **Single underscore in staging names** — `stg_stripe__payments` (double underscore separates source from entity).
- **`dbt run` + `dbt test` in CI** — use `dbt build` which runs in DAG order.
- **Missing `unique_key` in incremental** — Fabric merge strategy requires it. Without it, every run appends duplicates.
- **Snapshot on staging models** — snapshot source tables directly, not staging views (staging views have no history).
- **SQL auth on Fabric** — unsupported. ServicePrincipal auth only.

## Reference Files

For deeper guidance on specific patterns:

- **[references/modeling-patterns.md](references/modeling-patterns.md)** — Snapshot strategies (timestamp vs check), incremental model patterns (composite keys, late-arriving data, lookback windows), ref() dependency chains, and materialization decision framework.
- **[references/project-config.md](references/project-config.md)** — dbt_project.yml configuration, selectors and graph operators, tag cascading, meta fields, and CI/CD pipeline patterns.
- **[references/fabric-quirks.md](references/fabric-quirks.md)** — Fabric-specific T-SQL patterns, Liquid Clustering, Delta table behaviors, ServicePrincipal setup, and tsql-utils macro mapping.
