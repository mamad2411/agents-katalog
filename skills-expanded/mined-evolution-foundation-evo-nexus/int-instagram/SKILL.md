---
name: int-instagram
description: "Query Instagram Graph API — profile stats, recent posts, engagement, insights. Supports multi-account (OAuth via Social Auth App). Use when user asks about Instagram metrics, followers, posts, engagement, or any reference to Instagram analytics."
---

# Instagram Graph API

Instagram integration to monitor company and user profiles. Supports multiple accounts via OAuth (Social Auth App).

## Setup

Accounts configured via `make social-auth` (OAuth login with Facebook). Saved in `.env`:
```env
SOCIAL_INSTAGRAM_1_LABEL=your_account
SOCIAL_INSTAGRAM_1_ACCESS_TOKEN=YOUR_TOKEN
SOCIAL_INSTAGRAM_1_ACCOUNT_ID=YOUR_ACCOUNT_ID
SOCIAL_INSTAGRAM_1_PAGE_TOKEN=YOUR_PAGE_TOKEN
```

## API Client

```bash
python3 {project-root}/.claude/skills/int-instagram/scripts/instagram_client.py <command> [args]
```

### Commands

```bash
# List configured accounts
instagram_client.py accounts

# Profile (followers, bio, media count)
instagram_client.py profile [account_label]

# Last N posts with engagement
instagram_client.py recent_posts [account] [N]

# Top N posts by engagement
instagram_client.py top_posts [account] [N]

# Insights for a specific post
instagram_client.py post_insights POST_ID [account]

# Account insights (impressions, reach, profile views — 30d)
instagram_client.py account_insights [account]

# Summary of all accounts
instagram_client.py summary
```

## Key metrics
- Followers (delta via daily snapshots)
- Engagement rate: (likes + comments) / followers
- Reach and impressions (via account insights)
- Profile views
- Best post of the period
- Reels vs static posts
- Publishing frequency

## Rate Limits
- Instagram Platform endpoints: `4800 × impressions` per 24h
- Business Discovery / Hashtag: 200 calls/hour/user
