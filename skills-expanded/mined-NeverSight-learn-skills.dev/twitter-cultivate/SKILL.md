---
name: twitter-cultivate
description: Twitter/X account cultivation and growth system. Checks account health (TweepCred, shadowban), analyzes tweets, finds engagement opportunities, recommends unfollows, and tracks progress. Triggers on "/twitter-cultivate", "check my twitter", "twitter health", "grow my twitter", "twitter maintenance", "fix my twitter reach".
inputs:
  - name: twitter_handle
    type: string
    required: true
    description: Your Twitter/X handle (without @) to run cultivation on
outputs:
  - name: health_report
    type: json
    description: Account health metrics including TweepCred score, shadowban status, follower/following ratio
  - name: unfollow_recommendations
    type: list
    description: List of accounts recommended for unfollowing (inactive, non-reciprocal, or low-value)
  - name: opportunities
    type: list
    description: List of engagement opportunities — trending posts or accounts worth replying to
---

# Twitter Account Cultivation Skill

Systematic approach to growing Twitter presence based on the **open-source algorithm analysis**.

---

## Prerequisites

- **rnet** installed (`pip install "rnet>=3.0.0rc20" --pre`)
- **rnet_twitter.py** — the lightweight GraphQL client included in this repo
- **Twitter cookies** exported to: `twitter_cookies.json`
  Format: `[{"name": "auth_token", "value": "..."}, {"name": "ct0", "value": "..."}]`
- Your Twitter handle configured

### Getting Cookies

1. Open Chrome → go to `x.com` → log in
2. DevTools → Application → Cookies → `https://x.com`
3. Copy `auth_token` and `ct0` values
4. Save to `twitter_cookies.json` (see `twitter_cookies.example.json`)
5. Cookies last ~2 weeks. Refresh when you get 403 errors.

---

## Core Metrics to Track

| Metric | Healthy Range | Impact |
|--------|---------------|--------|
| Following/Follower Ratio | **< 0.6** | TweepCred score |
| Avg Views/Tweet | 20-40% of followers | Algorithm favor |
| Media Tweet % | **> 50%** | 10x engagement |
| Link Tweet % | **< 20%** | Avoid algorithm penalty |
| Reply Rate | Reply to 100% of comments | +75 weight boost |

---

## Workflow: Full Health Check

### Step 1: Analyze Account

```python
import asyncio
from rnet_twitter import RnetTwitterClient

async def analyze(username: str):
    client = RnetTwitterClient()
    client.load_cookies("twitter_cookies.json")

    # Get user profile
    user = await client.get_user_by_screen_name(username)
    followers = user.get("followers_count", 0)
    following = user.get("friends_count", 0)
    ratio = following / max(followers, 1)

    # Get recent tweets for content analysis
    tweets = await client.get_user_tweets(user["rest_id"], count=20)

    return {
        "username": username,
        "followers": followers,
        "following": following,
        "ratio": round(ratio, 2),
        "tweet_count": user.get("statuses_count", 0),
        "recent_tweets": len(tweets),
    }

asyncio.run(analyze("YOUR_USERNAME"))
```

### Step 2: Check Shadowban Status

Manual check: [shadowban.yuzurisa.com](https://shadowban.yuzurisa.com)

### Step 3: Analyze Following List

Recommends accounts to unfollow based on:
- No tweets in 90+ days (inactive)
- Never interacted with you (no value)
- Low follower count + high following (likely bots)
- No mutual engagement

### Step 4: Find Engagement Opportunities

Use `search_tweets` to find trending conversations:

```python
async def find_opportunities(niche_keywords: list[str]):
    client = RnetTwitterClient()
    client.load_cookies("twitter_cookies.json")

    opportunities = []
    for keyword in niche_keywords:
        tweets = await client.search_tweets(
            f"{keyword} lang:en -filter:replies",
            count=50,
            product="Top"
        )
        # Filter for high-engagement, recent tweets
        for t in tweets:
            if t["favorite_count"] >= 50 and t["reply_count"] < 20:
                opportunities.append(t)

    return sorted(opportunities, key=lambda t: t["favorite_count"], reverse=True)
```

### Step 5: Generate Weekly Report

Compile metrics from Steps 1-4 into a structured report.

---

## Account Health Scoring

Based on Twitter's open-source algorithm:

### TweepCred Estimation

```
Score = PageRank x (1 / max(1, following/followers))
```

| Ratio | Estimated TweepCred | Algorithm Treatment |
|-------|---------------------|---------------------|
| < 0.6 | 65+ (healthy) | All tweets considered |
| 0.6 - 2.0 | 40-65 | Limited consideration |
| 2.0 - 5.0 | 20-40 | Severe penalty |
| > 5.0 | < 20 | **Only 3 tweets max** |

---

## Unfollow Strategy

### Priority 1: Inactive Accounts
- No tweets in 90+ days
- Safe to unfollow, no relationship loss

### Priority 2: Non-Engagers
- Never liked/replied to your tweets
- One-way relationship

### Priority 3: Low-Value Follows
- High following/low followers (bot-like)
- No content in your niche

### Execution Plan

```
Week 1: Unfollow 30 inactive accounts
Week 2: Unfollow 30 non-engagers
Week 3: Unfollow 30 low-value follows
Week 4: Evaluate ratio improvement
```

**Target:** Get ratio below 2.0, ideally below 0.6

---

## Content Strategy (Algorithm-Optimized)

### Tweet Types by Algorithm Weight

| Type | Weight | Recommendation |
|------|--------|----------------|
| Tweet that gets author reply | **+75** | ALWAYS reply to comments |
| Tweet with replies | +13.5 | Ask questions |
| Tweet with profile clicks | +12.0 | Be intriguing |
| Tweet with long dwell time | +10.0 | Use threads |
| Retweet | +1.0 | Low value |
| Like | +0.5 | Lowest value |

### Content Mix

- **40%** Value content (insights, tips, frameworks)
- **30%** Engagement bait (questions, polls, hot takes)
- **20%** Build-in-public (progress updates, wins, losses)
- **10%** Promotion (with value attached)

### Media Requirements

Every tweet should have ONE of:
- Image (infographic, screenshot, meme)
- Video (< 2:20, hook in first 3 sec)
- Poll
- Thread (7-10 tweets)

**NEVER post text-only tweets**

---

## Posting Schedule

### Optimal Times (General)

| Day | Best Time | Second Best |
|-----|-----------|-------------|
| Tuesday | 9-10 AM | 1-2 PM |
| Wednesday | 9-10 AM | 3-4 PM |
| Thursday | 10-11 AM | 2-3 PM |

### First 10 Minutes Protocol

```
1. Post at optimal time
2. Immediately self-reply with additional insight
3. Reply to ANY comment within 10 minutes
4. Have 2-3 "pod" members ready to RT
```

### Frequency

- **Minimum:** 1 tweet/day
- **Optimal:** 3-5 tweets/day
- **Gap:** 30-60 min between tweets

---

## Engagement Tactics

### Reply Strategy (Most Important)

The algorithm gives **+75 weight** when you reply to replies on your tweets.

```
Someone comments on your tweet
    |
Reply within 30 minutes (CRITICAL)
    |
Algorithm sees author engagement
    |
Tweet gets boosted to more feeds
```

### Quote Tweet Strategy

```
Find viral tweet in your niche
    |
Quote with your unique take
    |
Add value, not just "great point"
    |
Post during optimal hours
```

### Thread Formula

```
1/ Hook (curiosity gap or bold claim)
2-6/ Individual points with specifics
7/ Summary
8/ CTA: Question or "follow for more"
```

---

## Weekly Routine

### Daily (15 min)

- [ ] Post 1-3 tweets with media
- [ ] Reply to ALL comments on your tweets
- [ ] Engage with 5-10 tweets in your niche
- [ ] Check notifications and respond

### Weekly (Saturday)

- [ ] Run full health check
- [ ] Review what content performed best
- [ ] Unfollow 10-20 low-value accounts
- [ ] Plan next week's content themes

### Monthly

- [ ] Full ratio review (target < 2.0)
- [ ] Shadowban check
- [ ] Content audit (media %, link %)
- [ ] Milestone check (follower goals)

---

## Recovery Plan (Low Follower Count)

### Phase 1: Emergency Ratio Fix (Week 1-2)

If your ratio is > 5.0 (following >> followers):
- Unfollow 100+ inactive/non-engaging accounts
- Target: ratio < 5.0 as first milestone

### Phase 2: Content Upgrade (Week 2-4)

If you have 0% media tweets:
- Add image/video to EVERY tweet
- Use Canva/Figma for quick graphics
- Screenshot interesting data/insights

### Phase 3: Engagement Building (Week 3-6)

- Reply to 20+ tweets/day in your niche
- Quote tweet viral content with your take
- Join relevant Twitter communities
- DM potential collaborators

### Phase 4: Consistency (Ongoing)

- 3-5 tweets/day
- Reply to 100% of comments
- Weekly analysis and adjustment
