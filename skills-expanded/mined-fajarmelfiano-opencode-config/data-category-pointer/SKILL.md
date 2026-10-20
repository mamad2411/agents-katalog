---
name: data-category-pointer
description: "Pointer to a library of 41 specialized Data skills. Use when working on data-related tasks."
risk: none
---

# Data Capability Library 🎯

This is a **pointer skill**. The 41 specialized Data skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **alpha-vantage** — Access 20+ years of global financial data: equities, options, forex, crypto, commodities, economic indicators, and 50+ technical indicators.
- **amplitude-automation** — Automate Amplitude tasks via Rube MCP (Composio): events, user activity, cohorts, user identification. Always search tools first for current schemas.
- **analytics** — When the user wants to set up, improve, or audit analytics tracking and measurement.
- **analytics-product** — Analytics de produto — PostHog, Mixpanel, eventos, funnels, cohorts, retencao, north star metric, OKRs e dashboards de produto.
- **analytics-tracking** — Design, audit, and improve analytics tracking systems that produce reliable, decision-ready data.
- **arrowspace** — Spectral vector search using graph Laplacian eigenstructure. Use when cosine/L2 similarity misses latent structure in your embeddings.
- **data-engineer** — Build scalable data pipelines, modern data warehouses, and real-time streaming architectures. Implements Apache Spark, dbt, Airflow, and cloud-native data platforms.
- **datacircle** — Look up LinkedIn profiles by URL through Datacircle (Up2Data or HarvestAPI, no markup), over its hosted MCP server or REST API, with the user's yes before each paid call.
- **dbt-transformation-patterns** — Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing.
- **firecrawl-scraper** — Deep web scraping, screenshots, PDF parsing, and website crawling using Firecrawl API. Use when you need deep content extraction from web pages, page interaction is required (clicking, scrolling, etc.), or you want screenshots or PDF parsing.
- **glasser** — Search, inspect, and run third-party data APIs through one CLI when the environment has no suitable integration.
- **huggingface-datasets** — Use this skill for Hugging Face Dataset Viewer API workflows that fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs, and read size or statistics.
- **looot** — Search, price and run 2,500+ data API endpoints (work emails, company search, SERP, web pages) from one prepaid balance via the looot MCP server.
- **mixpanel-automation** — Automate Mixpanel tasks via Rube MCP (Composio): events, segmentation, funnels, cohorts, user profiles, JQL queries. Always search tools first for current schemas.
- **monte-carlo-asset-health** — Curated upstream guidance for Monte Carlo Asset Health; use when the workflow matches the user goal.
- **monte-carlo-context-detection** — Route data-related requests to the right Monte Carlo skill or workflow. USE WHEN alerts, incidents, data broken, stale, coverage gaps, data quality, or any ambiguous data observability request.
- **monte-carlo-monitor-creation** — Guides creation of Monte Carlo monitors via MCP tools, producing monitors-as-code YAML for CI/CD deployment.
- **monte-carlo-performance-diagnosis** — Diagnoses pipeline performance issues -- slow jobs, expensive queries, latency trends -- using Monte Carlo's cross-platform observability. Uses a tiered investigation approach: discover problems, bridge to affected tables, then drill into root causes.
- **monte-carlo-remediation** — Investigate and remediate data quality alerts using Monte Carlo MCP tools. Runs root cause analysis, assesses blast radius, discovers available tools (MCP/CLI/API), proposes and executes fixes, or escalates with full context when uncertain.
- **monte-carlo-storage-cost-analysis** — Analyze a warehouse for stale, unused, or redundant tables via the analyze_storage_costs MCP tool. Classifies waste patterns and table categories, computes safety tiers, and handles category drill-downs and lineage follow-ups.
- **monte-carlo-validation-notebook** — Generates SQL validation notebooks for dbt PR changes with before/after comparison queries.
- **nexrad-mosaic-access** — Access official NOAA/NCEP MRMS radar and multisensor composites for a region and time; validate product, grid, domain, quality, timestamp, and provenance.
- **nexrad-product-access** — Discover and access NEXRAD data for a selected radar site, time, product, or Level II moment using completed archive volumes, real-time chunks, or supported Level III sources with metadata validation.
- **noaa-radar-satellite-fetching** — Retrieve NOAA NEXRAD and GOES products from public cloud archives using verified site, product, channel, sector, and scan-time selection.
- **optim-agent** — Guide agent-driven parameter optimization for configurable systems with measurable objectives. Use for HPO, inference tuning, simulations, or RL/control experiments.
- **postgres-readonly-queries** — Execute safe read-only SQL queries against PostgreSQL databases with multi-connection support and defense-in-depth write protection.
- **posthog-automation** — Automate PostHog tasks via Rube MCP (Composio): events, feature flags, projects, user profiles, annotations. Always search tools first for current schemas.
- **segment-automation** — Automate Segment tasks via Rube MCP (Composio): track events, identify users, manage groups, page views, aliases, batch operations. Always search tools first for current schemas.
- **segment-cdp** — Expert patterns for Segment Customer Data Platform including Analytics.js, server-side tracking, tracking plans with Protocols, identity resolution, destinations configuration, and data governance best practices.
- **spark-optimization** — Optimize Apache Spark jobs with partitioning, caching, shuffle optimization, and memory tuning. Use when improving Spark performance, debugging slow jobs, or scaling data processing pipelines.
- **sql-pro** — Master modern SQL with cloud-native databases, OLTP/OLAP optimization, and advanced query techniques. Expert in performance tuning, data modeling, and hybrid analytical systems.
- **sql-sentinel** — Audit SQL for the cost & performance anti-patterns that burn warehouse credits. Scores warehouse health 0-100 and outputs a prioritized cost-reduction plan for BigQuery, Snowflake, Redshift, and Postgres.
- **warehouse** — Plan and review read-only data warehouse analysis with explicit scope, privacy, provenance, and validation checks.
- **weather-data-lifecycle-management** — Manage ownership, retention, and cleanup of downloaded weather data across one-shot jobs, interactive viewers, caches, failures, and cancellation.
- **weather-data-reproducibility** — Record and verify provenance manifests for weather-data inputs and derived artifacts, including object identity, selections, software versions, transformations, and hashes.
- **weather-model-data-fetching** — Retrieve numerical weather prediction data from public AWS S3 and HTTP archives using GRIB2 inventories, byte ranges, Herbie, provider fallbacks, and verified caching.
- **weather-model-run-discovery** — Resolve the newest complete numerical weather prediction cycle and forecast objects across provider mirrors without downloading full payloads.
- **weather-observation-fetching** — Retrieve surface and upper-air weather observations from authoritative APIs and archives with station identity, time, units, and quality flags preserved.
- **weather-pipeline-performance-diagnosis** — Diagnose slow weather-data workflows by measuring discovery, transfer, parsing, scientific processing, and rendering separately before changing code.
- **web-scraper** — Web scraping inteligente multi-estrategia. Extrai dados estruturados de paginas web (tabelas, listas, precos). Paginacao, monitoramento e export CSV/JSON.
- **x-twitter-scraper** — Use Xquik for X data workflows: tweet search, user lookup, follower export, media downloads, monitors, webhooks, REST API, MCP, SDK setup, and approval-gated account actions.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/data/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/data`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
