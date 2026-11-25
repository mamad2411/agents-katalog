---
name: deviantart-artwork-search-gallery-and-trending-feed
description: "Reads DeviantArt's public feeds to find deviations by keyword, browse an artist's full gallery, or pull the current trending artwork feed by category. Output fields: title, artistUsername, publishedAt, views, favourites and more, as JSON rows. Use it for requests like \"DeviantArt artwork search, gallery\", or a CSV/JSON export of public DeviantArt data."
---

# DeviantArt Artwork Search, Gallery & Trending Feed

Reads DeviantArt's public feeds to find deviations by keyword, browse an artist's full gallery, or pull the current trending artwork feed by category.

- Actor: https://apify.com/dataspryva/deviantart-artwork-search-gallery-and-trending (ID `dataspryva~deviantart-artwork-search-gallery-and-trending`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/deviantart-artwork-search-gallery-and-trending-feed.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- DeviantArt artwork search, gallery
- a repeatable export of public DeviantArt data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `deviationId`: Deviation Id
- `title`: Title
- `artistUsername`: Artist Username
- `publishedAt`: Published At
- `views`: Views
- `favourites`: Favourites
- `deviationUrl`: Deviation Url

All 8 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | Choose what to collect. |
| `searchQuery` | string | no | fantasy art | Keyword or phrase to search for. Supports DeviantArt search syntax. |
| `tag` | string | no |  | Tag slug or tag URL, for example fantasy or `https://www.deviantart.com/tag/fantasy.` |
| `username` | string | no |  | DeviantArt username or profile URL whose gallery should be collected. |
| `artworkUrls` | array | no |  | Artwork page URLs, /art/... links, or numeric deviation IDs. |
| `contentType` | string | no | all | Limit keyword searches to images or literature. |
| `order` | string | no | recommended | Order used when browsing a tag. |
| `includeDetails` | boolean | no | false | Open each artwork page to add tags, description, original dimensions, file size and watermark flag when available. |
| `includeArtistStats` | boolean | no | false | Open each artist profile to add watchers, deviation count, pageviews and join date. |
| `excludeMature` | boolean | no | false | Skip artwork flagged as mature or sensitive. |
| `maxItems` | integer | no | 30 | Maximum number of artwork records to return. |

Example (`references/example-input.json`):

```json
{
  "mode": "tag",
  "tag": "fantasy",
  "maxItems": 25
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~deviantart-artwork-search-gallery-and-trending/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~deviantart-artwork-search-gallery-and-trending/runs" \
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
