---
name: ad-library-research
description: Research competitors ads in the Meta (Facebook and Instagram) Ad Library, Google Ads Transparency Center and LinkedIn Ad Library - active ads, creatives, copy, landing pages and how long ads have run. Use when the user asks what ads a company runs, wants ad inspiration, or wants to find brands that advertise in a niche. Uses the ScrapeIO API.
---

# Ad library research

## Endpoints (use `call_endpoint` with the path when using MCP)

- Meta, by company: `/v1/facebook/adLibrary/company/ads` (`companyName` or `pageId`, `country`, `status`: ACTIVE, `media_type`, `sort_by`: total_impressions), 1 credit per page
- Meta, by keyword: `/v1/facebook/adLibrary/search/ads` (`query`, `country`, `status`, `search_type`: keyword_exact_phrase), 1 credit per page
- Google: `/v1/google/company/ads` (`domain` or `advertiser_id`, `region`, `platform`, `format`), up to 25 credits per call, so ask first
- LinkedIn: `/v1/linkedin/ads/search` (`company` or `keyword`, `countries`), then `/v1/linkedin/ad` for one ad

Pass `trim=true` on Meta calls when you only need the copy and creative links.

## Steps

1. **Company or keyword?** For named competitors use the company endpoints. To find who advertises in a niche, search Meta ads by keyword and list the advertisers.
2. **Active first.** Start with `status=ACTIVE` in the user's country.
3. **Longest running ads win.** An ad that has run for months is usually profitable. Sort and highlight by start date.
4. **Read the creatives**: headline, primary text, call to action, landing page, format (video, image, carousel). Group ads by angle (price, pain point, social proof, offer).

## Output

Per competitor: number of active ads, main angles with example copy (quoted), the longest running ads with start dates and links, formats used, and landing pages. End with 3 angles the user could test. Never claim spend or impression numbers the data does not include.

## How to call ScrapeIO

Needs `SCRAPEIO_API_KEY`. If it is missing, ask the user to get a free key at https://scrapeio.com/login (100 credits, no card). Never print the key.

- **With the `scrapeio` MCP server:** use the named tool when it exists (for example `tiktok_profile`). For any other path, use `call_endpoint` with `{ "path": "/v1/...", "params": { ... } }`.
- **Without MCP:** `curl -s "https://scrapeio.com<path>?<params>" -H "x-api-key: $SCRAPEIO_API_KEY"`.
- Answers are in `data`; lists are `data.items` with `data.cursor` and `data.has_more`. Fields are the same on every platform: `handle`, `followers`, `plays`, `likes`, `comments`, `shares`, `created_at`, `url`.
- 403 (private) and 404 (not found) are free: skip and move on. Retry 502 once. 402 means the user needs credits (https://scrapeio.com/pricing).
- Watch `credits_remaining` and tell the user before a step would spend more than they expect.
