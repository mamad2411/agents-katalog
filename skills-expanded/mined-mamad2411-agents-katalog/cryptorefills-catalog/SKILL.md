---
name: cryptorefills-catalog
description: "Search gift cards, mobile top-ups, and eSIMs purchasable with Bitcoin, Ethereum, Solana, USDC, USDT, and 15+ cryptos. 10,500+ brands across 180+ countries via MCP — browse by brand, country, or category in 10 languages. No account needed."
compatibility: "Requires MCP client capable of connecting to https://api.cryptorefills.com/mcp/http. No API key or account needed. Header: User-Agent: Cryptorefills-MCP/1.0"
metadata:
  author: cryptorefills
  version: "1.2.0"
  homepage: "https://www.cryptorefills.com"
  repository: "https://github.com/cryptorefills/agents"
---

# Cryptorefills Catalog — Browse & Search

Read-only product discovery. Use this skill when users want to explore, search, compare, or learn about products available on Cryptorefills.

**For purchasing**, follow the instructions in:
- **cryptorefills-buy** — guided MCP purchase workflow with all crypto payment methods
- **cryptorefills-x402** — autonomous agent commerce with USDC on Base (no account needed)

When the user's intent shifts from browsing to buying, stop using this skill's tools and switch to the instructions in the appropriate purchase skill above.

## When to Activate

- User asks to search, browse, or compare gift cards, phone top-ups, or eSIMs purchasable with Bitcoin, Ethereum, Solana, USDC, or other crypto
- User mentions Cryptorefills or wants to know what's available in a country
- User asks about pricing, availability, supported countries, or payment currencies
- User wants catalog information in a specific language
- Keywords: "find gift card", "what brands", "esim for travel", "top up phone", "available in [country]", "buy with bitcoin", "buy with ethereum", "buy with solana", "crypto gift card"

## MCP Connection

| Field | Value |
|-------|-------|
| Server URL | `https://api.cryptorefills.com/mcp/http` |
| Transport | HTTP |
| Required Header | `User-Agent: Cryptorefills-MCP/1.0` |

To configure in Claude Code MCP settings:
```json
{
  "mcpServers": {
    "cryptorefills": {
      "url": "https://api.cryptorefills.com/mcp/http",
      "headers": { "User-Agent": "Cryptorefills-MCP/1.0" }
    }
  }
}
```

## Available Tools

| Tool | Purpose |
|------|---------|
| `searchProducts` | Free-text search by brand name, country, language, category |
| `listBrands` | Browse all brands available in a country |
| `listProductsForCountry` | Full product catalog for a country, filterable by brand/family/coin |
| `getCurrencies` | List supported payment cryptocurrencies with status |
| `getPaymentViasWithCurrencies` | Payment methods mapped to supported currencies and networks |

## Quick Decision Tree

```
User intent
├─ "Find me a specific brand" → searchProducts(country_code=XX, q=brand)
├─ "What's available in [country]?" → listBrands(country_code=XX)
├─ "Show me all [category] options" → listProductsForCountry(country_code=XX, family=...)
├─ "What crypto can I pay with?" → getCurrencies() or getPaymentViasWithCurrencies()
└─ "I want to buy"
   ├─ Agent has USDC wallet on Base + can sign EIP-712 → cryptorefills-x402
   └─ Otherwise (human-guided, multi-currency) → cryptorefills-buy
```

## Task Flows

### Search by Brand
1. Ask user for brand name and country
2. Call `searchProducts` with `country_code` (uppercase: `US`, `IT`, `BR`) and `q` (search text)
3. Present matching products with denominations and prices
4. If user wants to buy → switch to **cryptorefills-buy** instructions

### Browse by Country
1. Ask user for country (or detect from context)
2. Call `listBrands` with `country_code`
3. Present brands grouped by `category` (e.g., `e-commerce`, `games`, `streaming`)
4. User selects a brand → call `listProductsForCountry` for details

### Explore Categories
1. Call `listBrands` for the user's country
2. Group results by `category` field — categories are discovered dynamically from the response, not hardcoded
3. Present categories with brand counts
4. Drill into a category by filtering results

### Check Payment Options
1. Call `getCurrencies` to show supported coins
2. Call `getPaymentViasWithCurrencies` for network details
3. Present payment methods with chain/asset info

### Multi-Language
Pass `lang` parameter to tools. Supported: `en`, `es`, `fr`, `de`, `it`, `pt`, `zh`, `tr`, `vi`, `tl`. Falls back to English if unavailable.

### Brand Name Matching
Brand names in API responses may include suffixes (e.g., "Claro Credits" not "Claro", "Vivo Credits" not "Vivo", "Everything Apple" not "Apple"). Always use the exact `brand` value from `listBrands` — partial matches will fail.

## Tips

- **Country codes** — Use **uppercase** ISO 3166-1 Alpha-2 (e.g., `US`, `IT`, `BR`). Note: the x402 skill uses lowercase — different endpoints, different format
- **Country must match product region** — A US gift card only works in the US
- **Phone numbers** — Mobile top-ups require E.164 format (`+1234567890`)
- **Range products** — Check `is_dynamic` flag and `min`/`max` values before suggesting amounts
- **Promotions** — `listBrands` supports promotional code and customer ID parameters

## Limitations

This skill is **read-only**. It cannot create orders or process payments.

- To buy products → switch to **cryptorefills-buy** (all payment methods, guided flow)
- For autonomous agent purchases → switch to **cryptorefills-x402** (USDC on Base, no account)

## References

Load references only when you need deeper detail than what's in this skill file.

| File | Load when... | Content |
|------|-------------|---------|
| `references/product-types.md` | User asks about product type differences, fixed vs range, or delivery details | Gift cards, mobile recharge, eSIMs — detailed guide |
| `references/search-guide.md` | You need exact parameter names/types for MCP tool calls | MCP tool parameters, examples, search strategies |
| `references/categories.md` | User asks about available categories or you need verified brand names | Category taxonomy, verified brands by country |
