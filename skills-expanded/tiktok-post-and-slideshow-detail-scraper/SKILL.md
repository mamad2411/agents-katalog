---
name: tiktok-post-and-slideshow-detail-scraper
description: "Fetch full metadata for any TikTok video or photo-carousel post by URL or ID: engagement stats, author snapshot, music details, hashtags, mentions, and signed media URLs. Output fields: postUrl, caption, playCount, likeCount, commentCount and more, as JSON rows. Use it for requests like \"TikTok post scraper\", or a CSV/JSON export of public TikTok data."
---

# TikTok Post & Slideshow Detail Scraper

Fetch full metadata for any TikTok video or photo-carousel post by URL or ID: engagement stats, author snapshot, music details, hashtags, mentions, and signed media URLs.

- Actor: https://apify.com/nimbryxo-studio/tiktok-post-and-slideshow-detail-scraper (ID `nimbryxo-studio~tiktok-post-and-slideshow-detail-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/tiktok-post-and-slideshow-detail-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- TikTok post scraper
- a repeatable export of public TikTok data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `postId`: Post ID
- `postUrl`: Post URL
- `postType`: Type
- `caption`: Caption
- `createdAt`: Created At
- `playCount`: Plays
- `likeCount`: Likes
- `commentCount`: Comments
- `shareCount`: Shares
- `author`: Author
- `source`: Source

All 23 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | no | posts | What to scrape: individual posts, a profile's newest posts, or comment threads on posts. |
| `postUrls` | array | no |  | TikTok video/photo URLs, /v/ share links, embed links, vm.tiktok.com or vt.tiktok.com short links, or bare numeric post IDs. Duplicates are scraped once. |
| `postIds` | array | no |  | Numeric TikTok post IDs (15-20 digits). Use this instead of, or in addition to, postUrls. |
| `profiles` | array | no |  | TikTok usernames (@handle), profile URLs, or bare handles. Profiles mode returns up to 500 newest posts per profile; comments mode can use them as comment targets. |
| `maxItems` | integer | no | 100 | Global cap on output rows. Posts mode counts posts; profiles mode counts posts; comments mode counts comments and replies. Status rows do not count. |
| `maxDetail` | integer | no | 50 | How many posts get the slower page/detail enrichment (caption language, collect/repost counts, video tracks). Remaining posts use the fast embed record. |
| `maxCommentsPerPost` | integer | no | 100 | Maximum comments plus replies to keep for each post in comments mode, or to attach to each post when Include comments is on. |
| `includeReplies` | boolean | no | false | Fetch the reply thread under each root comment and include replies with their parent. |
| `includeComments` | boolean | no | false | In posts/profiles mode, attach a comments array to each post. In comments mode, emit root comment rows (comments mode enables this automatically when both comment toggles are off). |
| `proxyConfiguration` | object | no |  | Optional. Leave empty to run directly; a proxy is not required. The actor falls back to an Apify datacenter proxy on a block signal. |
| `includeMediaUrls` | boolean | no | true | Include signed video, cover, music, and slideshow image URLs plus mediaUrlExpiresAt. They typically expire in about 48 hours. |
| `validateMediaUrls` | boolean | no | false | Check the main media URL with a GET Range request (TikTok's CDN rejects HEAD) and add mediaUrlAccessible. Adds latency. |
| `includeAuthorStats` | boolean | no | true | Include follower, following, heart, and video counts in author and authorStats. |
| `includeHashtags` | boolean | no | true | Include the hashtags array extracted from the caption. |

3 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "postUrls": [
    "https://www.tiktok.com/@khaby.lame/video/7574844184952081686"
  ],
  "maxItems": 25,
  "maxDetail": 1,
  "maxCommentsPerPost": 25
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~tiktok-post-and-slideshow-detail-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~tiktok-post-and-slideshow-detail-scraper/runs" \
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
