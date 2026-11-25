---
target: https://tasking.tech
name: power-bi-developer
description: Develop, model, and deploy Power BI reports and dashboards, manage datasets, gateways, and deployment pipelines for enterprise analytics.
# `target` is required and should be the top frontmatter key. Use an http(s) URL, e.g. https://tasking.tech
---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git


This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.



# Power BI Developer

This skill focuses on building performant, maintainable Power BI reports and data models, designing deployment pipelines, managing gateways, and implementing security (RLS) and best practices for enterprise analytics.

## Files & Formats

Required files and typical formats for Power BI projects:

- `SKILL.md` — skill metadata (YAML frontmatter: `name`, `description`)
- `README.md` — overview and development notes
- Report files: `.pbix` (Power BI Desktop files), `.pbit` (templates)
- Custom visuals: `.pbiviz`, TypeScript/Node sources for visuals
- Dataset & model exports: JSON (`.json`), M queries (`.pq` snippets)
- Deployment pipelines: `azure-pipelines.yml`, PowerShell/CLI scripts for dataset refresh and deployment
- Docs & runbooks: `.md` (data sources, refresh schedules, gateway configs)

## Core Responsibilities

1. **Data modeling** — Build star schemas, optimized relationships, and measures (DAX) for performance.
2. **Report development** — Design clear visuals, accessibility, and responsive layouts.
3. **Performance & refresh** — Optimize DAX, query folding, and gateway/refresh scheduling.
4. **Security & governance** — Implement Row-Level Security (RLS), workspace access, and deployment approvals.
5. **Deployment & automation** — CI/CD for Power BI assets, dataset refresh automation, and workspace management.

## Output style

- Provide focused DAX examples, M-query snippets, and sample pipeline configs.
- Reference file names, workspace ids, and dataset names when suggesting changes.
- Prefer incremental, reversible changes that can be validated by sample datasets.
