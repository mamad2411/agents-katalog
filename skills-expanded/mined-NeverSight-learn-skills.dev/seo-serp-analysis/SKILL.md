---
name: seo-serp-analysis
description: "Deep SERP analysis and backlink profiling for high-priority keywords using DataForSEO"
version: 1.0.0
metadata:
  openclaw:
    emoji: "🏆"
    homepage: https://github.com/AipengHuang/seo-keyword-intelligence
    primaryEnv: DATAFORSEO_LOGIN
    envVars:
      - name: DATAFORSEO_LOGIN
        required: true
        description: "DataForSEO account email. See seo-seed-discovery for setup instructions."
      - name: DATAFORSEO_PASSWORD
        required: true
        description: "DataForSEO account password."
    install:
      - kind: node
        package: seo-skill-core
---

# SEO SERP Analysis

Perform deep SERP analysis on priority keywords: examine top-ranking pages, SERP features, and domain authority.

## Credentials Check

If `DATAFORSEO_LOGIN` or `DATAFORSEO_PASSWORD` are missing, tell the user:
> "DataForSEO credentials are not configured. Please run `seo-seed-discovery` first — it will guide you through the setup."

## When to Use

After `seo-keyword-metrics` has produced `metrics.json`. Focus analysis on the most promising keywords.

## Prerequisites

- Workspace with `metrics.json`

## Procedure

### Step 1: Deep SERP Data

```bash
node {baseDir}/scripts/deep-serp.ts --workspace <workspace_path> --limit 30
```

For the top priority keywords, fetches full SERP data including organic positions, ads, People Also Ask, featured snippets, and related searches. Writes `serp-deep.json`.

### Step 2: Domain Authority Check

```bash
node {baseDir}/scripts/backlink-check.ts --workspace <workspace_path>
```

Checks domain rank / backlink profile for top-ranking domains in the SERPs. Writes `backlinks.json`.

> **What is Backlinks / Domain Rank?** Domain Rank (DR) is a score 0–100 reflecting how many high-quality external websites link to a domain. A high DR means the site is authoritative and hard to outrank. Low DR domains (under 30) in the top 10 signal that the keyword is achievable for newer sites.

## Expert Analysis Framework

As a senior SEO specialist, analyze each SERP:

1. **SERP Feature Landscape**: Does the SERP have featured snippets, PAA, knowledge panels? These indicate content opportunities
2. **Authority Gap**: What's the average DR of top 10? Can the user's domain realistically compete?
3. **Weak Spots**: Are there low-DR domains, Reddit posts, or UGC in the top positions? These signal opportunity
4. **Content Type Pattern**: Are top results how-to guides, comparisons, product pages, or tools?
5. **SERP Intent Match**: Does the SERP content type match the user's planned content type?

## Output Format

- **Per-Keyword SERP Profile** (top 5 results, features, DR range)
- **SERP Winability Assessment** for each keyword
- **Featured Snippet Opportunities** (keywords where snippets are present)
- **Content Type Recommendations** based on SERP analysis
