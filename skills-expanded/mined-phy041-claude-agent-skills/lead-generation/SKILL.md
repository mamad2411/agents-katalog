---
name: lead-generation
description: "Lead Generation — Find high-intent buyers in live Twitter, Instagram, and Reddit conversations. Auto-researches your product, generates targeted search queries, and discovers people actively looking for solutions you offer. Social selling and prospecting powered by 1.5B+ indexed posts via Xpoz MCP."
homepage: https://xpoz.ai
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["mcporter"],
          "skills": ["xpoz-setup"],
          "network": ["mcp.xpoz.ai"],
          "credentials": "Xpoz account (free tier) — auth via xpoz-setup skill (OAuth 2.1)"
        },
        "install": [{"id": "node", "kind": "node", "package": "mcporter", "bins": ["mcporter"], "label": "Install mcporter (npm)"}],
      },
  }
tags:
  - lead-generation
  - sales
  - prospecting
  - social-media
  - twitter
  - instagram
  - reddit
  - find-leads
  - social-selling
  - buyer-intent
  - outreach
  - growth
  - marketing
  - customer-discovery
  - leads
  - mcp
  - xpoz
  - intent
  - discovery
inputs:
  - name: product_description
    type: string
    required: false
    description: Plain-text description of your product and the problems it solves (use this OR product_url)
  - name: product_url
    type: string
    required: false
    description: Your product's website URL — skill will auto-profile it to generate search queries (use this OR product_description)
outputs:
  - name: leads
    type: list
    description: Scored leads ready for outreach review, each with {platform, username, score, url, outreach_draft}
---

# Lead Generation

**Find high-intent buyers from live social conversations.**

Discovers leads expressing problems your product solves, complaining about competitors, or actively seeking solutions across Twitter, Instagram, and Reddit.

## Setup

Run `xpoz-setup` skill to authenticate. Verify: `mcporter call xpoz.checkAccessKeyStatus`

## 3-Phase Process

### Phase 1: Product Research (One-Time)

Ask for product reference (website/GitHub/description). Use `web_fetch`/`web_search` to research. Build profile:
- Product description
- Target audience / ICP
- Pain points addressed
- Competitors
- Keywords

**Validate with user before proceeding.**

Generate 12-18 search queries across:
1. **Pain point queries** — people expressing problems your product solves
2. **Competitor frustration** — complaints about alternatives
3. **Tool/solution seeking** — "recommend a tool for..."
4. **Industry discussion** — target audience conversations

Save to `data/lead-generation/product-profile.json` and `data/lead-generation/search-queries.json`.

### Phase 2: Lead Discovery (Repeatable)

```bash
# Twitter posts (highest intent signal)
mcporter call xpoz.getTwitterPostsByKeywords query="QUERY" startDate="DATE"

# Poll for results (every 5s until completed)
mcporter call xpoz.checkOperationStatus operationId="op_..."

# Find relevant people
mcporter call xpoz.getTwitterUsersByKeywords query="..."

# Reddit posts (good for tool comparison threads)
mcporter call xpoz.getRedditPostsByKeywords query="QUERY" limit=10
```

### Phase 3: Scoring & Output

**Score (1-10):**

| Signal | Points |
|--------|--------|
| Explicitly asking for tool/solution | +3 |
| Complaining about named competitor | +2 |
| Project blocked by pain point | +2 |
| Active in target community | +1 |
| High engagement (>10 likes / 5 comments) | +1 |
| Recent (<48h) | +1 |
| Profile matches ICP | +1 |
| Is selling a competing product | -3 |
| Is a KOL/content creator (not a buyer) | -2 |

**Tiers:** 8-10 = 🔴 Hot (outreach now), 6-7 = 🟠 Warm (monitor), 5 = Watchlist, <5 = Skip

Deduplicate via `data/lead-generation/sent-leads.json` (key: `{platform}:{author}:{post_id}`).

**Output format for each lead:**

```
🔴 HOT LEAD (Score: 8/10)
@username | Job Title | Platform
"Quote from their post..."
URL: https://...
Posted: X days ago | Y likes, Z replies

Why: [Signal breakdown]

Outreach draft:
"Had the exact same problem — we ended up building [solution].
Happy to share what worked. (Disclosure: I work on [Product])"
```

## Query Limitations (Xpoz)

**Xpoz uses split-word matching, NOT phrase matching.**

- "brand voice" → matches "brand" OR "voice" → noisy results
- **FIX**: Use domain-specific compound terms with unique identifiers
- **Competitor queries work best** because competitor names are unique

## Tips

- Save product profile once, reuse daily
- Quality > quantity — filter aggressively
- Always disclose affiliations in outreach drafts
- Drafts only — user reviews before sending
- Daily budget: ~6 queries/day on free tier (~5,000 credits total)
