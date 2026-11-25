---
name: dailymotion-video-discovery-by-topic-and-channel
description: "Search Dailymotion by keyword, browse trending or topic videos, or pull a channel's uploads, with language, country, and duration filters, views, likes, tags, and owner details per video. Output fields: title, ownerUsername, views, likes, duration and more, as JSON rows. Use it for requests like \"Dailymotion video discovery\", or a CSV/JSON export of public Dailymotion data."
---

# Dailymotion Video Discovery by Topic & Channel

Search Dailymotion by keyword, browse trending or topic videos, or pull a channel's uploads, with language, country, and duration filters, views, likes, tags, and owner details per video.

- Actor: https://apify.com/dataspryva/dailymotion-video-discovery-by-topic-and-channel (ID `dataspryva~dailymotion-video-discovery-by-topic-and-channel`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/dailymotion-video-discovery-by-topic-and-channel.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Dailymotion video discovery
- a repeatable export of public Dailymotion data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `title`: Title
- `ownerUsername`: Owner Username
- `views`: Views
- `likes`: Likes
- `duration`: Duration
- `publishedAt`: Published At
- `videoUrl`: Video Url

All 8 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | search | What to fetch from Dailymotion. |
| `searchQueries` | array | no |  | One or more keywords to search (mode=search, mode=searchUsers). Each query is paginated up to Max items. Existing tasks with the old `searchQuery` field keep working. |
| `topic` | string | no | news | Dailymotion category to browse (mode=byTopic). |
| `videoIds` | array | no | [] | Specific videos to look up (mode=byVideoIds). Accepts bare IDs (`x4d4447`), dailymotion.com/video/... links, or dai.ly links. Unavailable IDs are skipped. |
| `sortBy` | string | no | relevance | Result order. Values apply where the Dailymotion API supports them: `relevance` needs mode=search/searchUsers; `popular` is mode=searchUsers only; `old`/`id-asc` are not available… |
| `language` | string | no |  | Only include videos in this language. Leave as All languages for every language. |
| `country` | string | no |  | Only include videos published from this country (mode=search, trending). Leave as All countries for every country. |
| `verifiedOnly` | boolean | no | false | Only include videos from verified Dailymotion channels (mode=search, trending). |
| `liveOnly` | boolean | no | false | Only include live streams instead of on-demand videos. |
| `tag` | string | no |  | Only include videos carrying this tag (mode=search, byTopic, byUser, byPlaylist). Example: `jazz`. |
| `createdAfter` | string | no |  | Only include videos published on or after this date, as `YYYY-MM-DD` (mode=search, trending, byTopic, byUser). Long ranges are fetched automatically in overlapping windows. |
| `createdBefore` | string | no |  | Only include videos published on or before this date, as `YYYY-MM-DD` (mode=search, trending, byTopic, byUser). Long ranges are fetched automatically in overlapping windows. |
| `minDuration` | integer | no |  | Only include videos at least this many seconds long. |
| `maxDuration` | integer | no |  | Only include videos at most this many seconds long. |

3 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "searchQueries": [
    "technology news"
  ],
  "maxItems": 25,
  "mode": "search"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~dailymotion-video-discovery-by-topic-and-channel/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/dataspryva~dailymotion-video-discovery-by-topic-and-channel/runs" \
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
