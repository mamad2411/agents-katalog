---
name: competitor-social-audit
description: Audit and compare brands or competitors on TikTok, Instagram, YouTube, X and LinkedIn - followers, posting cadence, median views, engagement, top posts and content themes. Use when the user asks how a competitor is doing on social, to benchmark brands, or what content works for them. Uses the ScrapeIO API.
---

# Competitor social audit

Benchmark 2 to 5 brands side by side and explain what works for each.

## Steps

1. **Find the handles.** If the user gives only brand names, search (`tiktok_search_users`, `instagram_search_profiles`) and confirm the official account (verified, highest followers, matching bio link). Ask if unsure.
2. **Profiles** on each platform: `tiktok_profile`, `instagram_profile`, `youtube_channel`, `twitter_profile`, and `/v1/linkedin/company` for LinkedIn.
3. **Recent posts** (aim for the last 30 to 60 days): `tiktok_profile_videos`, `instagram_user_posts`, `youtube_channel_videos`, `twitter_user_tweets`, `/v1/linkedin/company/posts`. Page with `cursor` until you pass the date window.
4. **Per brand and platform**, compute: followers, posts per week, median `plays`, median engagement rate ((likes + comments + shares) / plays), and the top 3 posts by plays.
5. **Themes.** Read captions of the top 10 and bottom 10 posts. For the top 3 videos, pull transcripts (`tiktok_transcript`, `youtube_transcript`, `instagram_transcript`) to see the hook in the first lines.
6. **Ads (optional).** Use the ad-library-research skill to add what each brand is paying to promote.

## Output

1. A comparison table: brand x platform with followers, posts per week, median plays, engagement rate.
2. Per brand: the 3 best posts with links and one line on why they worked (format, hook, topic).
3. Three concrete takeaways for the user.

## Cost

About 2 to 4 credits per brand per platform, plus 1 per transcript. A 3-brand, 3-platform audit is usually 30 to 50 credits.

## How to call ScrapeIO

Needs `SCRAPEIO_API_KEY`. If it is missing, ask the user to get a free key at https://scrapeio.com/login (100 credits, no card). Never print the key.

- **With the `scrapeio` MCP server:** use the named tool when it exists (for example `tiktok_profile`). For any other path, use `call_endpoint` with `{ "path": "/v1/...", "params": { ... } }`.
- **Without MCP:** `curl -s "https://scrapeio.com<path>?<params>" -H "x-api-key: $SCRAPEIO_API_KEY"`.
- Answers are in `data`; lists are `data.items` with `data.cursor` and `data.has_more`. Fields are the same on every platform: `handle`, `followers`, `plays`, `likes`, `comments`, `shares`, `created_at`, `url`.
- 403 (private) and 404 (not found) are free: skip and move on. Retry 502 once. 402 means the user needs credits (https://scrapeio.com/pricing).
- Watch `credits_remaining` and tell the user before a step would spend more than they expect.
