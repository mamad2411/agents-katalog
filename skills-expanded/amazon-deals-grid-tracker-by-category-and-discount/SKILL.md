---
name: amazon-deals-grid-tracker-by-category-and-discount
description: "Pull Amazon's Today's Deals grid across 23 marketplaces, with deal price, list price, savings amount/percent, deal type, brand, and department for each product. Filter by category, brand, price range, and discount range. Output fields: asin, title, dealPrice, savingsPercent, averageRating and more, as JSON rows. Use it for requests like \"Amazon deals grid\", or a CSV/JSON export of public Amazon data."
---

# Amazon Deals Grid Tracker by Category & Discount

Pull Amazon's Today's Deals grid across 23 marketplaces, with deal price, list price, savings amount/percent, deal type, brand, and department for each product. Filter by category, brand, price range, and discount range.

- Actor: https://apify.com/dataspryva/amazon-deals-grid-tracker-by-category-and-discount (ID `dataspryva~amazon-deals-grid-tracker-by-category-and-discount`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/amazon-deals-grid-tracker-by-category-and-discount.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Catch Amazon deals before Monday's price check](https://www.youtube.com/shorts/rbaQJ__OtNg)

## When to use

Use this skill when the user wants:

- Amazon deals grid
- a repeatable export of public Amazon data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `asin`: Asin
- `title`: Title
- `dealPrice`: Deal Price
- `savingsPercent`: Savings Percent
- `averageRating`: Average Rating
- `dealEndsAt`: Deal Ends At
- `category`: Category

All 8 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `marketplace` | string | yes | amazon.com | Which Amazon domain's Today's Deals page to scrape. |
| `categories` | array | no | [] | Amazon departments to scan. Common names: Electronics, Home & Kitchen, Kitchen, Beauty & Personal Care, Clothing Shoes & Jewelry, Toys & Games, Sports & Outdoors, Books, Pet… |
| `collection` | string | no |  | Restrict to one of Amazon's curated deal collections. The collection names differ by marketplace; unsupported collections return a clear status record instead of unfiltered data. |
| `brand` | string | no |  | Case-insensitive brand name substring (e.g. Anker, Samsung). Leave empty for all brands. |
| `minRating` | integer | no |  | Keep only deals whose product rating is at least this value. Deals without a rating are excluded when this is set. |
| `priceMin` | integer | no |  | Keep deals at or above this price in the marketplace's local currency. |
| `priceMax` | integer | no |  | Keep deals at or below this price in the marketplace's local currency. |
| `discountMin` | integer | no |  | Keep deals with at least this percentage off, filtered by Amazon itself. |
| `discountMax` | integer | no |  | Keep deals with at most this percentage off, filtered by Amazon itself. |
| `primeExclusiveOnly` | boolean | no | false | Only return deals in Amazon's Prime Exclusive collection. |
| `sortBy` | string | no | featured | Featured keeps Amazon's order. Other sorts read the fetched deal window before returning, so they may take longer. |
| `maxItems` | integer | no | 30 | Hard cap on emitted deal records. Amazon exposes up to 500 deals per category/collection query; add categories to partition the window. |

Example (`references/example-input.json`):

```json
{
  "maxItems": 25,
  "marketplace": "amazon.com"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~amazon-deals-grid-tracker-by-category-and-discount/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~amazon-deals-grid-tracker-by-category-and-discount/runs" \
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
