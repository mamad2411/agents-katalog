---
name: threads-public-post-reply-and-profile-data-extractor
description: "Pull posts, replies, media, reposts, keyword search, hashtag search, or a post's reply thread from Threads, with real engagement counts, captions, media, and profile bios. Output fields: authorUsername, postText, likeCount, commentCount, shareCount and more, as JSON rows. Use it for requests like \"Threads public post, reply scraper\", or a CSV/JSON export of public Threads data."
---

# Threads Public Post, Reply & Profile Data Extractor

Pull posts, replies, media, reposts, keyword search, hashtag search, or a post's reply thread from Threads, with real engagement counts, captions, media, and profile bios.

- Actor: https://apify.com/vexaloom-labs/threads-public-post-reply-and-profile-data (ID `vexaloom-labs~threads-public-post-reply-and-profile-data`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/threads-public-post-reply-and-profile-data-extractor.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- Threads public post, reply scraper
- a repeatable export of public Threads data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `authorUsername`: Author Username
- `postText`: Post Text
- `publishedAt`: Published At
- `likeCount`: Like Count
- `commentCount`: Comment Count
- `repostCount`: Repost Count
- `quoteCount`: Quote Count
- `shareCount`: Share Count
- `mediaType`: Media Type
- `postUrl`: Post Url

All 11 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `mode` | string | yes | profile | What to collect from Threads. |
| `usernames` | array | no |  | Threads usernames, with or without @, or full profile URLs. Used by mode=profile / profileReplies / profileMedia / profileReposts. |
| `searchQueries` | array | no |  | Keywords, phrases, or #hashtags. Used by mode=search and mode=profilesByKeyword. |
| `tag` | string | no |  | Hashtag or topic to search without the # sign, e.g. 'ai' or 'mma'. Used by mode=tag. |
| `postUrls` | array | no |  | Threads post links (threads.com or threads.net). Each returns the post and its reply thread. Used by mode=postReplies. |
| `sortBy` | string | no | top | Order for keyword search results: Top (relevance) or Recent (newest first). 'default' is accepted as an alias of Top. |
| `includeProfileInfo` | boolean | no | true | For profile modes, also output one profile record per username with bio, follower count, verification, links, and topics. |
| `postedAfter` | string | no |  | Optional lower date bound. Accepts ISO dates (2026-01-31) or relative windows such as 7d, 24h, or 2w. |
| `postedBefore` | string | no |  | Optional upper date bound. Accepts ISO dates or relative windows such as 7d, 24h, or 2w. |
| `includeMediaUrls` | boolean | no | true | Store photos and videos in the run's key-value store so their links keep working after Threads' signed CDN links expire. Turn off to keep the original links. |
| `maxItems` | integer | no | 100 | Maximum number of post, reply, or discovered-profile records to return. |

Example (`references/example-input.json`):

```json
{
  "usernames": [
    "zuck"
  ],
  "searchQueries": [
    "openai"
  ],
  "tag": "ai",
  "postUrls": [
    "https://www.threads.com/@zuck/post/DZpPDXbCeTt"
  ],
  "includeMediaUrls": false,
  "maxItems": 25,
  "mode": "profile"
}
```

The input passes the Actor's input schema (checked at every publish). First run: `maxItems` = 25, small enough for the 300-second sync wait; raise it once the rows look right.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~threads-public-post-reply-and-profile-data/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~threads-public-post-reply-and-profile-data/runs" \
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
