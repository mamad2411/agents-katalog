---
name: trycook-research
description: Scrape websites, social media platforms, and run market research using TryCook CLI research tools. Use when asked to "scrape", "research", "competitor analysis", "find trending", "scrape reddit", "scrape tiktok", "instagram scrape", "youtube comments", "google trends", "facebook groups", or any web scraping/market research request.
allowed-tools:
  - Bash(trycook *)
  - Read
---

# TryCook Research & Scraping

Scrape websites, social platforms, and run market intelligence via the TryCook CLI.

**Prerequisite:** Ensure `trycook status` shows authenticated before proceeding.

## Website Scraping

```bash
trycook tool info scrape_website
trycook tool call scrape_website '{"url": "https://example.com", "includeMarkdown": true}'
```

For deep crawls:

```bash
trycook tool info firecrawl
trycook tool call firecrawl '{"url": "https://example.com", "maxPages": 10}'
```

## Social Media Scraping

### Reddit

```bash
trycook tool info reddit_scrape
trycook tool call reddit_scrape '{"subreddit": "supplements", "sort": "hot", "limit": 25}'
```

### TikTok

```bash
trycook tool info tiktok_scrape
trycook tool call tiktok_scrape '{"query": "skincare routine", "limit": 20}'
```

### Instagram

```bash
trycook tool info instagram_scrape
trycook tool call instagram_scrape '{"username": "brandname", "limit": 12}'

# Comments on a specific post
trycook tool info instagram_comments
trycook tool call instagram_comments '{"postUrl": "https://instagram.com/p/...", "limit": 50}'
```

### YouTube

```bash
trycook tool info youtube_scrape
trycook tool call youtube_scrape '{"query": "best supplements 2026", "limit": 10}'

# Channel deep dive
trycook tool info youtube_channel
trycook tool call youtube_channel '{"channelUrl": "https://youtube.com/@channelname"}'

# Comment analysis
trycook tool info youtube_comments
trycook tool call youtube_comments '{"videoUrl": "https://youtube.com/watch?v=...", "limit": 100}'
```

### Facebook

```bash
trycook tool info facebook_scrape
trycook tool call facebook_scrape '{"query": "weight loss tips", "limit": 20}'

# Groups
trycook tool info facebook_groups
trycook tool call facebook_groups '{"query": "keto diet", "limit": 10}'
```

### Twitter/X

```bash
trycook tool info twitter_scrape
trycook tool call twitter_scrape '{"query": "from:competitor_brand", "limit": 20}'
```

### LinkedIn

```bash
trycook tool info linkedin_scrape
trycook tool call linkedin_scrape '{"query": "SaaS founder", "limit": 10}'
```

## Trend Research

### Google Trends

```bash
trycook tool info google_trends
trycook tool call google_trends '{"keyword": "ozempic", "timeframe": "past_12_months"}'
```

### Discover Trending Content

```bash
trycook tool info discover_trending
trycook tool call discover_trending '{"niche": "fitness supplements", "platform": "tiktok"}'
```

## Ad Intelligence

```bash
# Search ad creatives by segment
trycook tool info search_ad_segments
trycook tool call search_ad_segments '{"query": "protein powder", "platform": "facebook"}'

# Foreplay ad library search
trycook tool info foreplay
trycook tool call foreplay '{"query": "skincare brand ads", "limit": 20}'
```

## Workflow: Competitor Deep Dive

1. **Scrape their site** — `scrape_website` for copy, pricing, offers
2. **Check their socials** — `instagram_scrape` + `tiktok_scrape` for content strategy
3. **Analyze their ads** — `foreplay` or `search_ad_segments` for paid creative
4. **Read their reviews** — `youtube_comments` + `reddit_scrape` for sentiment
5. **Track trends** — `google_trends` for market positioning

## Workflow: Market Research Sprint

1. **Trend scan** — `google_trends` + `discover_trending` for demand signals
2. **Reddit mining** — `reddit_scrape` relevant subreddits for pain points
3. **Competitor audit** — `scrape_website` top 5 competitors
4. **Social proof** — `youtube_comments` + `instagram_comments` for voice-of-customer
5. **Ad landscape** — `foreplay` to see what's running

## Tips

- Always check `trycook tool info <name>` for the exact schema before calling
- Scraping tools return structured data — parse the JSON output for the fields you need
- Rate limits apply — avoid calling the same scraping tool in rapid succession
- For large scrapes, use `limit` to control result count
