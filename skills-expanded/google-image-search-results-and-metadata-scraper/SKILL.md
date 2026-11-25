---
name: google-image-search-results-and-metadata-scraper
description: "Run a Google Images search and get back full-resolution image URLs with dimensions, thumbnails, source page titles, and the web page each image came from. Output fields: engine, title, sourceDomain, imageUrl, imageWidth and more, as JSON rows. Use it for requests like \"Google image Search results scraper\", or a CSV/JSON export of public Google Search data."
---

# Google Image Search Results & Metadata Scraper

Run a Google Images search and get back full-resolution image URLs with dimensions, thumbnails, source page titles, and the web page each image came from.

- Actor: https://apify.com/nimbryxo-studio/google-image-search-results-and-metadata-scraper (ID `nimbryxo-studio~google-image-search-results-and-metadata-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/google-image-search-results-and-metadata-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Google image Search results scraper
- a repeatable export of public Google Search data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `engine`: Engine
- `imageUrlType`: URL type
- `title`: Title
- `sourceDomain`: Source domain
- `imageUrl`: Image URL
- `imageWidth`: Width
- `imageHeight`: Height

All 29 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `queries` | array | no |  | One or more image search queries. Each query is searched independently. Google operators such as site:, quoted phrases and -exclusions are passed through. |
| `maxResults` | integer | no | 100 | Maximum number of image rows to return for each query. Google Images usually runs out around 300-400 results for a query; this is a ceiling, not a guarantee. |
| `minWidth` | integer | no | 0 | Drop images narrower than this many pixels. Rows without published dimensions are dropped when this is set. 0 disables the filter. |
| `minHeight` | integer | no | 0 | Drop images shorter than this many pixels. Rows without published dimensions are dropped when this is set. 0 disables the filter. |
| `country` | string | no | US | Two-letter country used for Google's gl parameter (and Bing's cc parameter). Local sites rank higher in local results. |
| `language` | string | no | en | Interface and result language used for Google's hl parameter (and Bing's setlang parameter). |
| `safeSearch` | string | no | active | Google SafeSearch level. 'active' filters explicit images; 'off' does not. |
| `imageSize` | string | no |  | Google Images size filter. The MP values are minimum megapixels. Bing fallback applies the nearest size category and enforces the exact MP floor locally when dimensions are known. |
| `imageColor` | string | no |  | Google Images color filter. 'black_and_white' is grayscale; 'transparent' looks for a transparent background. |
| `imageType` | string | no |  | Google Images type filter: photographs, faces, clip art, line drawings or animated images. |
| `fileType` | string | no |  | Only images in this format. Google applies this server-side; Bing fallback applies it to the image URL extension locally. |
| `timeRange` | string | no |  | Only images Google found within this period. Bing fallback maps 'hour' to its 24-hour window. |
| `usageRights` | string | no |  | Google's usage-rights labels. These are Google's labels, not a legal guarantee; check the licence on the source page before reuse. |
| `googleOnly` | boolean | no | false | When true, a failed or empty Google search fails that query with a clear status instead of using another engine. |

1 more optional field on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "queries": [
    "Alfons Mucha"
  ],
  "maxResults": 25
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxResults` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~google-image-search-results-and-metadata-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~google-image-search-results-and-metadata-scraper/runs" \
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
