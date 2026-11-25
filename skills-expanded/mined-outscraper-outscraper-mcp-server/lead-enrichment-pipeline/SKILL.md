---
name: lead-enrichment-pipeline
description: Run a lead research and enrichment pipeline across several Outscraper MCP tools. Use when an agent needs to discover a company or business, enrich it with company metadata, find emails or contacts, and optionally extract structured messaging from a website for outbound sales, GTM research, or account planning.
---

# Lead Enrichment Pipeline

Use this skill when the goal is not just to find a company, but to turn it into an actionable research record.

## Workflow

1. Discover the target using `businesses_search` or `google_maps_search`.
2. Enrich known domains with `company_insights`.
3. Find reachable contacts with `emails_and_contacts`.
4. If positioning or product messaging matters, use `ai_scraper` on the company homepage.
5. Return one concise account summary rather than separate tool dumps.

## Routing Guide

- If the user starts with a domain, skip discovery and go straight to enrichment.
- If the user starts with a geography plus business type, begin with place or business discovery.
- If the user wants outreach angles, include `ai_scraper`.

## Tool Sequence

### Discovery

Use one of:

- `businesses_search`
- `google_maps_search`

### Company Enrichment

Use `company_insights`.

```json
{
  "query": ["outscraper.com"],
  "fields": ["name", "description", "industry", "employees", "location"],
  "execution_mode": "sync"
}
```

### Contact Discovery

Use `emails_and_contacts`.

```json
{
  "query": ["outscraper.com"],
  "preferred_contacts": ["technical", "decision makers"],
  "execution_mode": "sync"
}
```

### Structured Homepage Extraction

Use `ai_scraper`.

```json
{
  "query": "https://outscraper.com",
  "prompt": "Extract company name, core product description, ideal customer types, and notable claims.",
  "schema": {
    "type": "object",
    "required": [],
    "properties": {
      "company_name": { "type": "string" },
      "product_summary": { "type": "string" },
      "ideal_customers": {
        "type": "array",
        "items": { "type": "string" }
      },
      "notable_claims": {
        "type": "array",
        "items": { "type": "string" }
      }
    }
  },
  "execution_mode": "sync"
}
```

## Output Style

Return one account brief with:

- company snapshot
- contacts found
- product positioning
- recommended next step for outreach or research
