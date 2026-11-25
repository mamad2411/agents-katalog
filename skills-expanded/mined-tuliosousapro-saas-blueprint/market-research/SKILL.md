---
name: market-research
description: Deep web research skill using Firecrawl MCP. Use when estimating market size (TAM/SAM/SOM), analyzing trends, or scraping competitors. For competitor teardowns, see competitor-analysis.
---

# Market Research Skill

## When to Use
- During **Phase 0 (Idea)** → Market Research, Competitor Analysis, Opportunity Mapping
- During **Phase 1 (Validation)** → Demand Testing
- Any time you need structured intelligence about a market, niche, or competitor

## Tools Required

| Tool | Purpose |
|------|---------|
| `firecrawl_search` | Web search for market data, trends, competitors |
| `firecrawl_scrape` | Extract structured data from specific pages |
| `firecrawl_extract` | Pull pricing, features, positioning from competitor sites |
| `firecrawl_map` | Discover all pages on a competitor's site |

## Instructions

### 1. Define Research Scope
Before starting any research, clarify with the user:
- **Market/Industry**: What space are we researching?
- **Geography**: Global, US, EU, LATAM, specific country?
- **Depth**: Quick scan (30 min) or deep dive (2+ hours)?
- **Focus**: TAM estimation, competitor landscape, trend signals, or all three?

### 2. TAM/SAM/SOM Estimation

Execute these searches in parallel:
```
firecrawl_search: "{industry} market size 2024 2025 report"
firecrawl_search: "{industry} SaaS revenue growth forecast"
firecrawl_search: "{niche} total addressable market"
```

Structure the output as:
| Metric | Value | Source | Confidence |
|--------|-------|--------|------------|
| TAM | $X B | {source} | High/Med/Low |
| SAM | $X M | {source} | High/Med/Low |
| SOM | $X M | {source} | High/Med/Low |

### 3. Competitor Landscape

For each competitor identified:
```
firecrawl_extract:
  urls: ["{competitor_url}"]
  prompt: "Extract: company name, tagline, pricing tiers, key features, target audience, tech stack indicators"
  schema: {
    name: string,
    tagline: string,
    pricing: [{ tier: string, price: string, features: [string] }],
    target_audience: string,
    key_features: [string]
  }
```

Compile into a comparison matrix:
| Feature | Competitor A | Competitor B | Competitor C | **Our Opportunity** |
|---------|-------------|-------------|-------------|-------------------|

### 4. Trend Analysis

Search for:
```
firecrawl_search: "{industry} trends 2025 2026"
firecrawl_search: "{niche} emerging technology"
firecrawl_search: "{industry} pain points users complain"
```

Categorize trends as:
- **Tailwinds** (market forces working in our favor)
- **Headwinds** (forces working against us)
- **Wildcards** (unpredictable but high-impact)

### 5. Output Format

Save all research to the relevant PLAYBOOK.md directory as `RESEARCH.md` with:
1. Executive Summary (3 sentences max)
2. TAM/SAM/SOM table
3. Competitor matrix
4. Trend analysis (tailwinds/headwinds/wildcards)
5. Key insight + recommended action
6. Sources list with URLs

## Quality Gates
- Minimum 3 independent sources for any TAM claim
- Competitor data must be scraped, not assumed
- All monetary values must include year and currency
- Trends must be dated (no stale 2022 data presented as current)
