---
name: eni-scraper-workflow
description: "Unified structured web collection workflow using request-first Scrapy-style crawling and Playwright-style browser fallback, with schema, retry, deduplication, and quality gates."
x-alice-class: assist
---

# Scraper Workflow 2.1

Define allowed sources, output schema, freshness, pagination, identity keys, and quality thresholds. Start with direct HTTP or a Scrapy-style crawler. Escalate to Playwright-style browser automation only when rendering or state requires it. Persist raw responses when useful, normalize records, deduplicate, checkpoint pagination, handle retry and backoff, and validate counts, types, null rates, uniqueness, and sampled records before export.
