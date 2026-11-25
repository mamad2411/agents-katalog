---
name: comment-insights
description: Pull comments from TikTok, Instagram, YouTube, X or Facebook posts and turn them into insights - top questions, objections, sentiment, feature requests, buying signals and audience language. Use when the user asks what people say about a post, product, creator or brand, or wants voice-of-customer research. Uses the ScrapeIO API.
---

# Comment insights

## Comment endpoints (all take the post `url`)

- TikTok: `tiktok_comments` (most liked first), replies via `tiktok_comment_replies`
- Instagram: `instagram_comments` (`sort`: `popular` for the top 15, `recent` to page), replies via `instagram_comment_replies`
- YouTube: `youtube_comments` (`order`: `relevance` or `time`), replies via `youtube_comment_replies`
- X: `twitter_replies`
- Facebook: `facebook_comments`, replies via `facebook_comment_replies` (pass `feedback_id` and `expansion_token` from the comment)

Each page costs 1 credit. Ask before pulling more than 10 pages per post.

## Steps

1. **Pick posts.** Use the user's links, or take the top posts by `plays` from a profile's recent posts.
2. **Pull comments**, 1 to 5 pages per post. Keep `text`, `likes`, `replies` and `created_at`. Pull replies only for comments with many replies.
3. **Clean**: drop emoji-only, spam and repeated bot text, but count them (bot share is a useful signal).
4. **Group** into themes: questions, complaints and objections, praise, feature or product requests, purchase intent ("where can I buy", "link?"), comparisons with other brands.
5. **Weight** themes by comment likes, not just counts.

## Output

Top themes with a count, total likes, and 2 or 3 real example comments each (quoted exactly). Then a short "what to do with this" section: FAQ answers to write, objections to address, content ideas. Note how many comments were read and the credits spent.

## How to call ScrapeIO

Needs `SCRAPEIO_API_KEY`. If it is missing, ask the user to get a free key at https://scrapeio.com/login (100 credits, no card). Never print the key.

- **With the `scrapeio` MCP server:** use the named tool when it exists (for example `tiktok_profile`). For any other path, use `call_endpoint` with `{ "path": "/v1/...", "params": { ... } }`.
- **Without MCP:** `curl -s "https://scrapeio.com<path>?<params>" -H "x-api-key: $SCRAPEIO_API_KEY"`.
- Answers are in `data`; lists are `data.items` with `data.cursor` and `data.has_more`. Fields are the same on every platform: `handle`, `followers`, `plays`, `likes`, `comments`, `shares`, `created_at`, `url`.
- 403 (private) and 404 (not found) are free: skip and move on. Retry 502 once. 402 means the user needs credits (https://scrapeio.com/pricing).
- Watch `credits_remaining` and tell the user before a step would spend more than they expect.
