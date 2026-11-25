---
name: social-trend-research
description: Research what is trending on TikTok, Instagram, YouTube and X - trending videos, hashtags, sounds, topics and search suggestions by country - and explain which trends fit a brand. Use when the user asks what is trending, wants content ideas, or wants to know how big a hashtag or sound is. Uses the ScrapeIO API.
---

# Social trend research

## Sources

- TikTok trending feed: `tiktok_trending` (`/v1/tiktok/trending`, `region` as a 2-letter country code) or `tiktok_trending_feed`
- TikTok hashtag size and videos: `tiktok_search_hashtag` (`hashtag`)
- TikTok sounds: `tiktok_song` for usage count, `tiktok_song_videos` (`music_id`) for videos using it
- TikTok search suggestions: `/v1/tiktok/search/suggestions`
- Instagram: `instagram_hashtag`, `/v1/instagram/reels/trending`, reels with an audio track via `instagram_audio_reels`
- YouTube: `/v1/youtube/shorts/trending`, `youtube_search_hashtag`, `youtube_search_typeahead` for what people type
- X: `twitter_trends` (country), then `twitter_search` to see the posts

## Steps

1. **Scope**: country, platform, and the brand or niche (if any).
2. **Collect** the trending feed for the country, then pull the hashtags and sounds that repeat across it.
3. **Size** each candidate: hashtag totals, sound usage count, median `plays` of the videos using it, and how recent they are (`created_at`). A trend whose top videos are all over a week old is fading.
4. **Fit**: for a brand, keep trends whose videos match its audience and tone. Pull 2 or 3 transcripts to understand the format.

## Output

A ranked list: trend, platform, size, momentum (rising, peaking, fading, with the evidence), example videos with links, and one line on how the brand could use it. Note the country and the date.

## How to call ScrapeIO

Needs `SCRAPEIO_API_KEY`. If it is missing, ask the user to get a free key at https://scrapeio.com/login (100 credits, no card). Never print the key.

- **With the `scrapeio` MCP server:** use the named tool when it exists (for example `tiktok_profile`). For any other path, use `call_endpoint` with `{ "path": "/v1/...", "params": { ... } }`.
- **Without MCP:** `curl -s "https://scrapeio.com<path>?<params>" -H "x-api-key: $SCRAPEIO_API_KEY"`.
- Answers are in `data`; lists are `data.items` with `data.cursor` and `data.has_more`. Fields are the same on every platform: `handle`, `followers`, `plays`, `likes`, `comments`, `shares`, `created_at`, `url`.
- 403 (private) and 404 (not found) are free: skip and move on. Retry 502 once. 402 means the user needs credits (https://scrapeio.com/pricing).
- Watch `credits_remaining` and tell the user before a step would spend more than they expect.
