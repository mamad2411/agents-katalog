---
name: competitor-analysis
description: Structured competitor teardown skill. Use when scraping competitor sites, extracting pricing/features/positioning, or analyzing strategic gaps. For general research, see market-research.
---

# Competitor Analysis Skill

## When to Use
- During **Phase 0 (Idea)** → Competitor Analysis module
- When evaluating a new market or niche
- Before any pricing strategy or positioning work
- When a user says "who else does this?" or "what's out there?"

## Tools Required

| Tool | Purpose |
|------|---------|
| `firecrawl_search` | Discover competitors via web search |
| `firecrawl_map` | Crawl competitor site structure |
| `firecrawl_scrape` | Extract full page content for analysis |
| `firecrawl_extract` | Pull structured data (pricing, features) |

## Instructions

### 1. Identify Competitors

Run parallel searches:
```
firecrawl_search: "{product_description} SaaS alternatives"
firecrawl_search: "{problem_statement} software solutions"
firecrawl_search: "best {category} tools 2025 2026"
firecrawl_search: "{category} vs comparison"
```

Categorize into:
- **Direct competitors**: Same problem, same audience, same delivery model
- **Indirect competitors**: Same problem, different approach (e.g., agencies, spreadsheets)
- **Aspirational**: Where we want to be in 2+ years

### 2. Deep Teardown (Per Competitor)

For each direct competitor (max 5):

#### a. Pricing Intelligence
```
firecrawl_extract:
  urls: ["{competitor}/pricing"]
  prompt: "Extract all pricing tiers, prices, billing frequency, feature limits per tier, and any free tier details"
  schema: {
    tiers: [{
      name: string,
      price_monthly: string,
      price_annual: string,
      features: [string],
      limits: [string]
    }],
    free_tier: boolean,
    enterprise_custom: boolean
  }
```

#### b. Feature Inventory
```
firecrawl_scrape:
  url: "{competitor}/features"
  formats: ["json"]
  jsonOptions:
    prompt: "List every feature mentioned on this page with a one-line description"
    schema: {
      features: [{ name: string, description: string, category: string }]
    }
```

#### c. Positioning & Messaging
```
firecrawl_scrape:
  url: "{competitor}"
  formats: ["markdown"]
  onlyMainContent: true
```
Extract from the homepage:
- Headline / value proposition
- Target audience language
- Key differentiators they claim
- Social proof (customer count, logos, testimonials)

#### d. Tech Stack Detection
```
firecrawl_search: "{competitor_name} tech stack built with"
firecrawl_search: "site:{competitor_domain} careers engineer"
```

### 3. Build Comparison Matrix

Output as a markdown table:

| Dimension | {Our Product} | Competitor A | Competitor B | Competitor C |
|-----------|--------------|-------------|-------------|-------------|
| **Pricing (starter)** | TBD | $X/mo | $X/mo | $X/mo |
| **Free tier** | TBD | Yes/No | Yes/No | Yes/No |
| **Feature 1** | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| **Feature 2** | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ |
| **Target audience** | {ours} | {theirs} | {theirs} | {theirs} |
| **Weakness** | — | {gap} | {gap} | {gap} |

### 4. Gap Analysis

Identify:
- **Underserved segments**: Who are competitors ignoring?
- **Missing features**: What do users complain about on G2, Reddit, Twitter?
- **Pricing gaps**: Is there room between free and expensive tiers?
- **UX gaps**: Where is the friction in competitor products?

Search for complaints:
```
firecrawl_search: "{competitor_name} review complaints problems"
firecrawl_search: "site:reddit.com {competitor_name} alternative"
firecrawl_search: "site:g2.com {competitor_name} cons"
```

### 5. Output Format

Save to `BRAINIAC/0. Idea/0.4 Competitor Analysis/ANALYSIS.md`:
1. Executive summary (3 bullet points: biggest threat, biggest gap, our edge)
2. Competitor profiles (one section per competitor)
3. Comparison matrix
4. Gap analysis
5. Strategic recommendation (1 paragraph)
6. Raw data sources

## Quality Gates
- Minimum 3 direct competitors analyzed
- Pricing data must come from actual scrapes, not memory
- Gap analysis must cite specific user complaints with sources
- Matrix must include our product column (even if TBD)
