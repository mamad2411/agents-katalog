---
name: home-loan-rate
description: Weekly mortgage rate check for a chosen region via Perplexity. EXAMPLE.
---

# Home Loan Rate (example)

> **EXAMPLE.** Simple "single MCP call + format" pattern.

Spawn a Haiku sub-agent if `[cron ...]` suffix present.

## Setup

Requires Perplexity MCP configured with an API key.

Set `${REGION}` to your area (e.g. "Dallas, Texas" or "Boston, Massachusetts").

## Procedure

### STEP 1 — Query Perplexity

```
mcp__perplexity__perplexity_search with query: "best home mortgage loan interest rates ${REGION} today 2026 30-year fixed 15-year fixed"
```

Collect:
- Top 3-5 lenders with lowest 30-year fixed rates (company, rate, APR, points, link)
- Top 3-5 lenders with lowest 15-year fixed rates
- Any special programs (first-time buyer, VA, FHA) worth noting

### STEP 2 — Format

Markdown for Telegram (under 500 chars):

```
🏠 *${REGION} Mortgage Rates — [date]*

*30-year fixed:*
• Lender A — 6.25% (APR 6.38%, 0 pts) — link
• Lender B — 6.30%
• Lender C — 6.35%

*15-year fixed:*
• Lender A — 5.45%
• Lender D — 5.50%

Notes: [any special programs]
```

### STEP 3 — Send

`reply` MCP with `chat_id` from `USER.md`. End with `RATES_OK <timestamp>`.

### STEP 4 — On failure

If Perplexity unavailable, `reply` "🏠 Weekly rate check: Perplexity unavailable." Don't exit silently. End with `RATES_FAIL <timestamp>`.
