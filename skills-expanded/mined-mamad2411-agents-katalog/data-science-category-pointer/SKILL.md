---
name: data-science-category-pointer
description: "Pointer to a library of 8 specialized Data Science skills. Use when working on data-science-related tasks."
risk: none
---

# Data Science Capability Library 🎯

This is a **pointer skill**. The 8 specialized Data Science skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **data-engineering-data-driven-feature** — Build features guided by data insights, A/B testing, and continuous measurement using specialized agents for analysis, implementation, and experimentation.
- **data-engineering-data-pipeline** — You are a data pipeline architecture expert specializing in scalable, reliable, and cost-effective data pipelines for batch and streaming data processing.
- **data-quality-frameworks** — Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, implementing validation rules, or establishing data contracts.
- **data-scientist** — Expert data scientist for advanced analytics, machine learning, and statistical modeling. Handles complex data analysis, predictive modeling, and business intelligence.
- **data-storytelling** — Transform raw data into compelling narratives that drive decisions and inspire action.
- **data-structure-protocol** — Give agents persistent structural memory of a codebase — navigate dependencies, track public APIs, and understand why connections exist without re-reading the whole repo.
- **plotly** — Interactive visualization library. Use when you need hover info, zoom, pan, or web-embeddable charts. Best for dashboards, exploratory analysis, and presentations. For static publication figures use matplotlib or scientific-visualization.
- **polars** — Fast in-memory DataFrame library for datasets that fit in RAM. Use when pandas is too slow but data still fits in memory. Lazy evaluation, parallel execution, Apache Arrow backend. Best for 1-100GB datasets, ETL pipelines, faster pandas replacement. For larger-than-RAM data use dask or vaex.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/data-science/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/data-science`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
