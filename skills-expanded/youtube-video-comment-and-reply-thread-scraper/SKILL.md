---
name: youtube-video-comment-and-reply-thread-scraper
description: "Get a YouTube video's comments with nested replies attached, author identity, like counts, and pinned/hearted/verified flags, filterable by keyword and minimum likes. Output fields: authorName, text, likeCount, replyCount, isHearted and more, as JSON rows. Use it for requests like \"YouTube video comment scraper\", or a CSV/JSON export of public YouTube data."
---

# YouTube Video Comment & Reply Thread Scraper

Get a YouTube video's comments with nested replies attached, author identity, like counts, and pinned/hearted/verified flags, filterable by keyword and minimum likes.

- Actor: https://apify.com/nimbryxo-studio/youtube-video-comment-and-reply-thread-scraper (ID `nimbryxo-studio~youtube-video-comment-and-reply-thread-scraper`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/youtube-video-comment-and-reply-thread-scraper.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- YouTube video comment scraper
- a repeatable export of public YouTube data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `commentId`: Comment ID
- `authorName`: Author
- `text`: Text
- `likeCount`: Likes
- `replyCount`: Replies
- `isHearted`: Hearted
- `videoTitle`: Video

All 24 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `videoUrls` | array | no | [] | Watch, youtu.be, Shorts, embed, live, v/ links, or bare 11-character IDs. Every video is normalized to a watch URL internally. |
| `channelUrls` | array | no | [] | Channel /videos sources: /@handle, /channel/UC..., /c/name, /user/name, a bare @handle, or a UC... channel ID. Scrapes up to Max videos per source. |
| `playlistUrls` | array | no | [] | Playlist sources: youtube.com/playlist?list=... or a bare playlist ID. Scrapes up to Max videos per source. |
| `searchQueries` | array | no | [] | YouTube search terms or search-result URLs. Only video results are used, deduplicated, up to Max videos per source. |
| `maxVideosPerSource` | integer | no | 20 | Discovery cap for channel, playlist and search sources. 0 = every video the source exposes. |
| `maxComments` | integer | no | 100 | Top-level comments to examine per video. 0 = all. Comments rejected by filters still count toward this scan cap (so restrictive filters cannot paginate forever); replies do not. |
| `includeReplies` | boolean | no | true | Fetch reply threads. Emitted as flat rows by default; use Output mode tree to embed them instead. |
| `maxRepliesPerComment` | integer | no | 50 | Per-thread reply cap. 0 = all replies, stopping when the continuation token is exhausted. YouTube serves roughly 9-10 on the first reply page and 44-49 afterwards. |
| `maxReplyDepth` | integer | no | 1 | 0 = top-level comments only, 1 = direct replies (the shape observed publicly). Values above 1 are reserved for nested sub-threads, which YouTube has not exposed in the samples… |
| `maxTotalRows` | integer | no | 5000 | Global budget for emitted comment + reply rows. 0 = unlimited. Status rows are never counted and are not billable data rows. |
| `sortBy` | string | no | top | top = YouTube relevance order; newest = chronological, recommended for date cutoffs and complete windows. A date cutoff forces newest automatically. |
| `commentsSince` | string | no |  | Optional cutoff as an ISO date/datetime (2026-10-16) or relative duration (7d, 24h, 30m). Forces newest sort. |
| `keywords` | array | no | [] | Case-insensitive OR filter on comment and reply text. Empty = no keyword filter. A parent comment that does not match is skipped, so its replies are not fetched. |
| `minLikes` | integer | no | 0 | Drop comments and replies below this like count. Applied after fetching. YouTube only exposes rounded counts (K/M), so the comparison uses the rounded value. |

3 more optional fields on the Actor's Input tab.

Example (`references/example-input.json`):

```json
{
  "videoUrls": [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  ],
  "maxComments": 25,
  "maxRepliesPerComment": 3,
  "maxTotalRows": 20
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxComments` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~youtube-video-comment-and-reply-thread-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/nimbryxo-studio~youtube-video-comment-and-reply-thread-scraper/runs" \
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
