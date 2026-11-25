---
name: x-post-reply-and-profile-lookup-by-link-or-id
description: "Resolve X post links or IDs into text, author, media, polls, quoted/parent posts, engagement metrics and replies, or resolve a handle into that account's public profile. Output fields: text, author.username, createdAt, likeCount, viewCount and more, as JSON rows. Use it for requests like \"X post, reply\", or a CSV/JSON export of public Twitter data."
---

# X Post, Reply & Profile Lookup by Link or ID

Resolve X post links or IDs into text, author, media, polls, quoted/parent posts, engagement metrics and replies, or resolve a handle into that account's public profile.

- Actor: https://apify.com/vexaloom-labs/x-post-reply-and-profile-lookup-by-link-or-id (ID `vexaloom-labs~x-post-reply-and-profile-lookup-by-link-or-id`)
- n8n workflow for the same Actor: https://github.com/bolvein-firex/scraping-n8n-workflows/blob/main/docs/x-post-reply-and-profile-lookup-by-link-or-id.md
- Example input: `references/example-input.json`
- Input schema: `references/input-schema.json`
- Output fields: `references/output-fields.json`

## When to use

Use this skill when the user wants:

- X post, reply
- a repeatable export of public Twitter data as CSV or JSON

Do not use it for private, login-protected or paywalled data.

## What it returns

One JSON row per result. Columns from the Actor's dataset schema:

- `text`: Text
- `author.username`: Author.username
- `createdAt`: Created At
- `likeCount`: Like Count
- `retweetCount`: Retweet Count
- `replyCount`: Reply Count
- `viewCount`: View Count
- `url`: Url

All 9 declared fields: `references/output-fields.json`.

## Inputs

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `tweetUrls` | array | yes |  | Paste the posts you want to collect. You can also paste post IDs, x.com/i/web/status links, twitter.com links, profile links or bare handles (a profile input returns that… |
| `includeReplies` | boolean | no | true | Collect the replies X shows for each post, walked forward from the post's publication time. |
| `maxReplies` | integer | no | 20 | How many replies to collect for each post (0-500). Posts with very large threads may return fewer because X does not expose every reply to logged-out visitors. |
| `includeQuotes` | boolean | no | false | Collect the posts that quote each requested post, with their text, author and engagement counts. |
| `maxQuotes` | integer | no | 50 | How many quote posts to collect for each requested post (0-500). |
| `includeRetweeters` | boolean | no | false | Collect the handles of accounts that reposted each requested post. X only exposes a search-index sample of visible reposts, so this is an approximate, recent-biased list. |
| `maxRetweeters` | integer | no | 50 | How many retweeter handles to collect for each post (0-500). |
| `includeQuotedTweet` | boolean | no | true | When a collected post quotes another post, attach the quoted post's text, author and metrics. |
| `includeParentTweet` | boolean | no | true | When a collected post is a reply, attach the post it answers under parentTweet. |
| `includeThreadAncestors` | boolean | no | false | When a requested post is a reply, walk up to 10 posts back to the start of the thread and attach them under threadAncestors (root first). |
| `includeMedia` | boolean | no | true | Include image links, video links and video variants for each post. |
| `includeAuthorProfile` | boolean | no | true | Attach the author's public profile details (followers, bio, verification) to every post, reply and quote row under author and authorProfile. |

Example (`references/example-input.json`):

```json
{
  "tweetUrls": [
    "https://x.com/NASA/status/2107095768821576019"
  ],
  "maxReplies": 3
}
```

The input passes the Actor's input schema (checked at every publish). The run size follows the number of inputs you pass.

## Run it

Set `APIFY_TOKEN`, then call the synchronous endpoint for small and medium runs (it waits up to 300 seconds):

```bash
curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~x-post-reply-and-profile-lookup-by-link-or-id/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @references/example-input.json > output.json
```

Or with Node 18+: `node scripts/run.mjs [input.json]`.

For large runs, start an async run and read its dataset when it finishes:

```bash
RUN=$(curl -s -X POST "https://api.apify.com/v2/acts/vexaloom-labs~x-post-reply-and-profile-lookup-by-link-or-id/runs" \
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
