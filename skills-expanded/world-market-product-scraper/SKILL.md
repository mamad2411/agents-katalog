---
name: world-market-product-scraper
description: "Get product data from Cost Plus World Market, a US home decor, furniture, and specialty food retailer. Search by keyword or browse by department for price, brand, item number, category, images, availability, and ratings. Output fields: title, price, originalPrice, saleBadge, rating and more, as JSON rows. Use it for requests like \"World Market product scraper\", or a CSV/JSON export of public World Market data."
---

# World Market Product Scraper

Get product data from Cost Plus World Market, a US home decor, furniture, and specialty food retailer. Search by keyword or browse by department for price, brand, item number, category, images, availability, and ratings.

- Actor: https://apify.com/nimbryxo-studio/world-market-product-scraper (ID `nimbryxo-studio~world-market-product-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/world-market-product-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- World Market product scraper
- a repeatable export of public World Market data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `price`: Price
- `originalPrice`: Original Price
- `saleBadge`: Sale Badge
- `brand`: Brand
- `sku`: Sku
- `availability`: Availability
- `pickupStatus`: Pickup Status
- `rating`: Rating
- `reviewCount`: Review Count
- `productUrl`: Product Url

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | What to fetch. `search` uses a keyword, `byCategory` browses a department or collection, and `byProductUrls` reads the URLs you paste. |
| `searchQuery` | string | no | candle | Keyword to search for (mode=search), e.g. `candle`, `dining chair`, `chocolate`. |
| `category` | string | no |  | A World Market department or curated collection. Use `categoryUrl` instead if you want a sub-category that is not listed here. |
| `categoryUrl` | string | no |  | A worldmarket.com category or collection URL, e.g. `https://www.worldmarket.com/c/furniture/shop-all-furniture/`. Takes priority over `category`. |
| `productUrls` | array | no | [] | Direct worldmarket.com product-page URLs, e.g. `https://www.worldmarket.com/p/-.html`. Up to 500 unique URLs per run. |
| `sortBy` | string | no | bestselling | Sort order for search and department results. `bestselling` and `newArrivals` keep World Market's own listing order. |
| `minPrice` | integer | no |  | Drop products whose current price is below this amount. |
| `maxPrice` | integer | no |  | Drop products whose current price is above this amount. |
| `maxItems` | integer | no | 20 | Hard cap on emitted products (1–500). Search and department pages are read 120 tiles at a time. |
| `storeId` | string | no |  | A World Market store ID such as `store398`. Used only when `includePickup` is enabled. If omitted, the nearest store is resolved from `postalCode`. |
| `postalCode` | string | no |  | US ZIP code used to resolve the nearest store when `storeId` is not set and `includePickup` is enabled. |
| `includeVariants` | boolean | no | true | Include the selectable color, size or fragrance options for products that have them (up to 20). |
| `includePickup` | boolean | no | false | Add per-store pickup status, quantity and message. Requires `storeId` or `postalCode`. |
| `proxyConfiguration` | object | no |  | Optional. The actor connects directly first and only uses a proxy fallback if World Market blocks a request. Choose your own proxy to use it as that fallback, or leave it unset. |

Example (`references/example-input.json`):

```json
{
  "maxItems": 25,
  "mode": "search"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~world-market-product-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~world-market-product-scraper/runs" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d @references/example-input.json)
RUN_ID=$(echo "$RUN" | jq -r '.data.id'); DATASET=$(echo "$RUN" | jq -r '.data.defaultDatasetId')
curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?waitForFinish=60" -H "Authorization: Bearer $APIFY_TOKEN" | jq -r '.data.status'
curl -s "https://api.apify.com/v2/datasets/$DATASET/items?format=json" -H "Authorization: Bearer $APIFY_TOKEN" > output.json
```

## Cost and limits

- Apify bills the Actor's usage on your account; the Actor's Pricing tab shows the current price.
- Keep the limit in the input small for a first run.

## Guardrails

- Public data only. Do not pass cookies, sessions or private account data.
- Do not use the output for spam, harassment or unlawful discrimination.
- Check the target site's terms and local law before running at scale.
