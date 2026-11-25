---
name: decrypt-crypto-news-finder-by-category-and-keyword
description: "Search Decrypt's crypto, Web3, and AI news by keyword or category, or look up specific articles, for full article text, authors, tags, mentioned coins, and featured images. Output fields: title, authors, category, publishedAt, readingTimeMinutes and more, as JSON rows. Use it for requests like \"Decrypt crypto news\", or a CSV/JSON export of public Decrypt data."
---

# Decrypt Crypto News Finder by Category & Keyword

Search Decrypt's crypto, Web3, and AI news by keyword or category, or look up specific articles, for full article text, authors, tags, mentioned coins, and featured images.

- Actor: https://apify.com/dataspryva/decrypt-crypto-news-finder-by-category-and-keyword (ID `dataspryva~decrypt-crypto-news-finder-by-category-and-keyword`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/decrypt-crypto-news-finder-by-category-and-keyword.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

Short video breakdown:
- [Turn ticker news into a market brief](https://www.youtube.com/shorts/9wMkmbVIg3U)

## When to use

Use this skill when the user wants:

- Decrypt crypto news
- a repeatable export of public Decrypt data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `authors`: Authors
- `category`: Category
- `publishedAt`: Published At
- `readingTimeMinutes`: Reading Time Minutes
- `wordCount`: Word Count

All 7 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | What to fetch. Search matches titles, excerpts and article bodies. The latest mode returns the newest stories. |
| `searchQuery` | string | no |  | Keyword or phrase matched against article titles, excerpts and bodies (mode=search). E.g. bitcoin, ethereum, NFT. |
| `category` | string | no |  | One Decrypt category slug (mode=browseByCategory and as a filter in other modes). Leave empty for any category. |
| `categories` | array | no | [] | Filter by several category slugs at once. Applies to search, latest, tag, coin and author modes. |
| `tagSlugs` | array | no | [] | Filter by Decrypt tag slugs, e.g. bitcoin, ethereum, regulation. Tag names are not accepted; use the slugs returned in each record. |
| `coinSlugs` | array | no | [] | Filter by coin slugs, e.g. bitcoin, ethereum, solana. Names and ticker symbols are also accepted and mapped to slugs. |
| `authorSlugs` | array | no | [] | Filter by author slugs, e.g. jose, stephengraves. Author names are not accepted; use the slugs returned in each record. |
| `articleIds` | array | no | [] | Article IDs or decrypt.co URLs (mode=byId). Accepts bare IDs, /id/slug, localized /es/id/slug, ?p=id and /resources/slug URLs. |
| `locale` | string | no |  | Article language. Leave empty to include every locale. |
| `dateRangeFrom` | string | no |  | Only articles published on or after this date (YYYY-MM-DD). The date range is applied by the source. |
| `dateRangeTo` | string | no |  | Only articles published on or before this date (YYYY-MM-DD). The date range is applied by the source. |
| `sortBy` | string | no | newest | Newest first, oldest first, or best match. Best match needs a search query; otherwise newest is used. |
| `includeContent` | boolean | no | true | Include full HTML and plain-text article bodies, TL;DR content and word count. Turn off for a lighter dataset. |
| `onlyNew` | boolean | no | false | Skip article IDs returned by earlier runs of this actor. Useful for scheduled monitoring. State is kept automatically. |

2 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "searchQuery": "bitcoin",
  "category": "news",
  "articleIds": [
    "375656"
  ],
  "locale": "en",
  "maxItems": 25,
  "proxyConfiguration": {
    "useApifyProxy": false
  },
  "mode": "search"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~decrypt-crypto-news-finder-by-category-and-keyword/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~decrypt-crypto-news-finder-by-category-and-keyword/runs" \
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
