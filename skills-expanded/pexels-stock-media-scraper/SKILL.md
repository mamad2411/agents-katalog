---
name: pexels-stock-media-scraper
description: "Scrape free stock photos and videos from Pexels. Search by keyword, browse curated/popular media, a photographer's portfolio, or a curated collection. Get direct image and video file URLs, photographer credit, tags, colors, and more. Output fields: title, photographerName, width, height, orientation and more, as JSON rows. Use it for requests like \"Pexels stock media scraper\", or a CSV/JSON export of public Pexels data."
---

# Pexels Stock Media Scraper

Scrape free stock photos and videos from Pexels. Search by keyword, browse curated/popular media, a photographer's portfolio, or a curated collection. Get direct image and video file URLs, photographer credit, tags, colors, and more.

- Actor: https://apify.com/nimbryxo-studio/pexels-stock-media-scraper-2 (ID `nimbryxo-studio~pexels-stock-media-scraper-2`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/pexels-stock-media-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Pexels stock media scraper
- a repeatable export of public Pexels data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `photoId`: Photo Id
- `videoId`: Video Id
- `title`: Title
- `photographerName`: Photographer Name
- `width`: Width
- `height`: Height
- `orientation`: Orientation
- `durationSeconds`: Duration Seconds
- `license`: License
- `attribution`: Attribution
- `downloadUrl`: Download Url
- `pageUrl`: Page Url

All 13 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | What to fetch from Pexels. |
| `searchQuery` | string | no |  | Keyword to search for (mode=search). Example: `nature`, `city skyline`, `coffee`. |
| `mediaType` | string | no | photos | Which kind of media to return. For mode=search this selects between Pexels' separate photo-search and video-search pages (`all` is treated as `photos`). |
| `orientation` | string | no | all | Filter results by image/video orientation. |
| `minWidth` | integer | no | 0 | Only return media whose width is at least this many pixels. 0 disables the filter. |
| `minHeight` | integer | no | 0 | Only return media whose height is at least this many pixels. 0 disables the filter. |
| `minDuration` | integer | no | 0 | Only return videos at least this many seconds long (videos only; ignored for photos). 0 disables the filter. |
| `maxDuration` | integer | no | 0 | Only return videos at most this many seconds long (videos only; ignored for photos). 0 disables the filter. |
| `peopleCount` | string | no | all | Filter photo search results by how many people appear in them (mode=search, photos only). |
| `photoIds` | array | no | [] | Pexels photo IDs or full photo page URLs (mode=byPhotoId: look up these exact photos; mode=similarPhotos: find photos visually/topically similar to each of these). |
| `username` | string | no |  | Pexels photographer handle or profile URL (mode=byUser). Example: `alex-ivanov-773258579` or `https://www.pexels.com/@alex-ivanov-773258579/`. |
| `collectionSlug` | string | no |  | Pexels curated collection slug or full collection URL (mode=byCollection). Example: `aquatic-aesthetic-bw7dkse` or `https://www.pexels.com/collections/aquatic-aesthetic-bw7dkse/`. |
| `maxItems` | integer | no | 30 | Maximum number of media records to return. NOTE: Pexels' own public search pagination resets to empty results past page 20 (confirmed live: page 20 returns real results, page 21+… |
| `proxyConfiguration` | object | no | {"useApifyProxy":false} | Optional Apify proxy. Pexels is generally reachable without a proxy; enable the free Automatic datacenter group only if you experience blocking. |

Example (`references/example-input.json`):

```json
{
  "searchQuery": "nature",
  "photoIds": [
    "18872916"
  ],
  "username": "alex-ivanov-773258579",
  "collectionSlug": "aquatic-aesthetic-bw7dkse",
  "mode": "search"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 30, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~pexels-stock-media-scraper-2/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~pexels-stock-media-scraper-2/runs" \
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
