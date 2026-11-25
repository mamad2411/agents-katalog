---
name: google-ads-reporting-gaql
description: Use this skill when the user asks to extract performance metrics, build reports, or write Google Ads Query Language (GAQL) queries.
---

# Google Ads Reporting and GAQL Skill

This skill assists with writing queries and extracting performance data using the Google Ads Query Language (GAQL).

## Core Responsibilities
- **GAQL Queries**: Constructing accurate `SELECT` statements for campaigns, ad groups, and keywords.
- **Metrics Extraction**: Fetching performance data like Clicks, Impressions, CTR, and Conversions.
- **Date Ranges**: Implementing precise date filters using standard date literals (e.g., `DURING LAST_30_DAYS`).

## Best Practices
1. **SearchStream vs Search**: Prefer `SearchStream` over `Search` for large result sets to avoid pagination overhead.
2. **Resource Alignment**: Ensure that the resources requested in the `SELECT` clause are compatible with the resource specified in the `FROM` clause.
3. **Segmentation**: Understand how adding segments (e.g., `segments.date`, `segments.device`) multiplies the number of rows returned.
