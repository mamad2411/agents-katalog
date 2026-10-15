---
name: broker-price
description: Multi-platform price research for C2C resale. Search prices across bound platforms using the user's authorized session. Use when user wants to know "what is this worth", "price this", "market price", "询价", or needs a transparency pricing report before listing. Also usable standalone via /broker-price with a product description.
---

# broker-price: Authenticated Price Research

Searches prices across all bound platforms using the user's own account session — the same search they'd do manually in each app. No web scraping, no anti-bot issues.

## Workflow

1. Receive product info (from broker-recognize or user description)
2. Build platform-specific search queries
3. For each bound platform with valid session:
   - Search active listings → extract prices, conditions
   - Search sold listings → extract actual transaction prices
4. Calculate:
   - Price range (min → max)
   - Median active listing price
   - Median sold price (preferred metric)
   - Market sentiment (seller-favorable / balanced / buyer-favorable)
5. Recommend price: **median of sold comparables** (when available), or 5% below active median (when no sold data)
6. Present transparency report with data sources

## Script

```bash
python3 scripts/research.py --product product.json
    # Searches all bound platforms, outputs transparency report
```

## Fallback

If session-based search fails (expired session, platform API change), fall back to Claude Code's WebSearch for comparable listings. Results from fallback are clearly labeled as lower-confidence estimates.
