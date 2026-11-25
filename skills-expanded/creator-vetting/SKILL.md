---
name: creator-vetting
description: Check whether a creator or influencer account is worth paying, by spotting fake followers, bought engagement, inactive audiences and brand-safety issues on TikTok, Instagram and YouTube. Use before a sponsorship, a UGC deal or a partnership. Uses the ScrapeIO API.
---

# Creator vetting

Give a clear yes, no or "ask for more data" on one creator, with the evidence.

## Steps

1. **Profile**: `tiktok_profile`, `instagram_profile` or `youtube_channel` with the `handle`.
2. **Last 20 to 30 posts**: `tiktok_profile_videos`, `instagram_user_posts` or `youtube_channel_videos`. Page once if the first page has fewer than 20.
3. **Compute**:
   - median `plays` and view rate (median plays / followers). Healthy short-video accounts are usually above 5%; under 1% is a red flag.
   - engagement rate (likes + comments) / plays. Very high likes with very few comments suggests bought likes.
   - spread: one viral post and the rest flat means the follower count overstates reach. Report the median, not the mean.
   - posting cadence and the date of the last post.
   - share of posts marked `is_ad`, if present.
4. **Comment sample**: pull comments on 2 recent posts (`tiktok_comments`, `instagram_comments`, `youtube_comments`, by `url`). Look for generic bot comments ("nice", emoji only, repeated text from many accounts) and for what the audience actually talks about.
5. **Brand safety**: skim captions and transcripts of the 5 most viewed posts (`tiktok_transcript`, `instagram_transcript`, `youtube_transcript`) for topics the brand would not want.
6. **Optional, TikTok only**: `/v1/tiktok/user/audience` (`handle`) returns audience demographics; it costs up to 26 credits, so ask first.

## Output

Verdict first (Go, No go, or Ask for their analytics), then a short evidence table: followers, median plays, view rate, engagement rate, comment quality, last post, red flags. Link the posts you looked at.

## Cost

About 5 to 8 credits per creator, plus up to 26 for audience demographics.

## How to call ScrapeIO

Needs `SCRAPEIO_API_KEY`. If it is missing, ask the user to get a free key at https://scrapeio.com/login (100 credits, no card). Never print the key.

- **With the `scrapeio` MCP server:** use the named tool when it exists (for example `tiktok_profile`). For any other path, use `call_endpoint` with `{ "path": "/v1/...", "params": { ... } }`.
- **Without MCP:** `curl -s "https://scrapeio.com<path>?<params>" -H "x-api-key: $SCRAPEIO_API_KEY"`.
- Answers are in `data`; lists are `data.items` with `data.cursor` and `data.has_more`. Fields are the same on every platform: `handle`, `followers`, `plays`, `likes`, `comments`, `shares`, `created_at`, `url`.
- 403 (private) and 404 (not found) are free: skip and move on. Retry 502 once. 402 means the user needs credits (https://scrapeio.com/pricing).
- Watch `credits_remaining` and tell the user before a step would spend more than they expect.
