---
name: engagement-tracker
description: Track engagement metrics on all posted content (Reddit comments, Twitter replies, original posts). Runs 24h after posting to measure performance. Produces weekly analysis with actionable insights. Triggers on "check engagement", "track metrics", "how did my posts do", "engagement report", "performance analysis".
inputs:
  - name: date_range
    type: string
    required: true
    description: Time window to pull metrics for (e.g. "yesterday", "last 7 days", "2026-02-19")
outputs:
  - name: metrics
    type: list
    description: List of per-post engagement data, each with {platform, url, upvotes, views, replies}
  - name: weekly_summary
    type: text
    description: Human-readable weekly analysis with top performers and actionable insights (only present for multi-day ranges)
---

# Engagement Tracker Skill

Closed-loop analytics for all social media activity. Scrapes engagement metrics 24h after posting, stores structured data, and produces weekly insights.

---

## Core Principle

**You can't optimize what you don't measure.** Every post gets tracked. Every week gets analyzed. Decisions come from data, not vibes.

---

## Configuration

Set your Twitter handle:
```bash
export TWITTER_HANDLE="yourhandle"
```

Point to your Twikit directory:
```bash
export TWIKIT_DIR="~/crawlee-social-scraper"  # wherever you have twikit + cookies
```

---

## Daily Engagement Check (runs at 07:00 your TZ)

### Step 1: Find Yesterday's Posts

Read `memory/YYYY-MM-DD.md` for yesterday's date. Extract all posted URLs from the log tables.

**Reddit comment URLs** look like:
```
https://www.reddit.com/r/{subreddit}/comments/{post_id}/comment/{comment_id}/
```

**Twitter reply URLs** look like:
```
https://x.com/{username}/status/{tweet_id}
```

### Step 2: Scrape Reddit Comment Metrics

For each Reddit comment URL, fetch engagement data via AppleScript Chrome:

```bash
osascript -l JavaScript -e '
var chrome = Application("Google Chrome");
var tab = chrome.windows[0].activeTab;
tab.execute({javascript: "(" + function() {
    var commentId = "COMMENT_ID";
    fetch("/api/info.json?id=t1_" + commentId, {credentials: "include"})
        .then(r => r.json())
        .then(d => {
            var c = d.data.children[0].data;
            document.title = "METRICS:" + JSON.stringify({
                id: c.name,
                score: c.score,
                ups: c.ups,
                num_replies: c.num_comments || 0,
                permalink: c.permalink,
                subreddit: c.subreddit,
                body: c.body.substring(0, 100)
            });
        });
} + ")();"});
'
sleep 2
osascript -e 'tell application "Google Chrome" to return title of active tab of first window'
```

**Multi-profile Chrome fallback:** Use System Events + Console pattern (see `reddit-cultivate` skill).

**Rate limiting:** Wait 2+ seconds between each comment check.

### Step 3: Scrape Twitter Reply Metrics

```bash
cd $TWIKIT_DIR
source venv/bin/activate
python3 -c "
import asyncio, json
from twikit import Client

async def check():
    client = Client('en-US')
    client.load_cookies('twitter_cookies.json')
    user = await client.get_user_by_screen_name('$TWITTER_HANDLE')
    tweets = await client.get_user_tweets(user.id, tweet_type='Replies', count=20)
    results = []
    for t in tweets:
        results.append({
            'id': t.id,
            'text': t.text[:100],
            'created_at': str(t.created_at),
            'likes': t.favorite_count,
            'retweets': t.retweet_count,
            'replies': t.reply_count,
            'views': t.view_count,
            'in_reply_to': t.in_reply_to_tweet_id,
            'url': f'https://x.com/$TWITTER_HANDLE/status/{t.id}'
        })
    print(json.dumps(results, indent=2))

asyncio.run(check())
"
```

### Step 4: Store Metrics

Append to `memory/analytics/engagement-log.json`:

```json
{
  "entries": [
    {
      "id": "reddit-2026-01-01-001",
      "date": "2026-01-01",
      "platform": "reddit",
      "type": "comment",
      "subreddit": "SideProject",
      "post_title": "Post title here",
      "url": "https://www.reddit.com/r/SideProject/comments/abc/comment/xyz/",
      "checked_at": "2026-01-02T07:00:00+08:00",
      "hours_since_post": 22,
      "metrics": {
        "upvotes": 12,
        "replies": 3
      }
    }
  ]
}
```

### Step 5: Daily Summary

Report only if there's notable engagement:

```
Engagement Check (24h metrics)

Reddit (3 comments yesterday):
  r/ClaudeAI "your post topic" — 12 upvotes, 3 replies
  r/SideProject "your post topic" — 8 upvotes, 1 reply

Twitter (2 replies yesterday):
  @somebody — 5 likes, 1500 views
  @someone — 2 likes, 800 views

Top performer: Reddit r/ClaudeAI comment (12 upvotes)
Needs attention: 3 replies on ClaudeAI comment — consider responding!
```

**If no notable engagement (all zeros):** Reply `HEARTBEAT_OK`, no notification.

**If replies detected:** Flag them for response (author replies = +75 algo weight on Reddit).

---

## Weekly Analysis (runs Sunday)

Reads ALL entries from `memory/analytics/engagement-log.json` for the current week.

### Metrics Computed

**Per-Subreddit (Reddit):**

| Subreddit | Posts | Avg Upvotes | Avg Replies | Hit Rate |
|-----------|-------|-------------|-------------|----------|
| r/indiehackers | 5 | 12.0 | 2.3 | 100% |
| r/SideProject | 7 | 5.1 | 0.8 | 43% |

**Hit Rate** = % of posts with upvotes > 5 (adjustable threshold).

**Per-Target Account (Twitter):**

| Account | Replies | Avg Likes | Avg Views |
|---------|---------|-----------|-----------|
| @founder | 3 | 4.2 | 2100 |
| @techperson | 2 | 2.5 | 1800 |

### Actionable Recommendations

```
Weekly Insights:

1. SHIFT WEIGHT: r/indiehackers has 2.4x better engagement than r/SideProject.
   → Recommend: 2 comments/day in indiehackers, 1 in SideProject

2. SWEET SPOT: Higher quality score comments get 1.75x more upvotes.
   → Recommend: Raise quality bar

3. TIMING: Morning posts outperform evening by 40%.
   → Consider: Add midday posting batch

4. REPLIES UNANSWERED: 7 Reddit replies went unanswered this week.
   → Action: Respond within 24h for algo boost (+75 weight).
```

### Weekly Summary Format

```
Weekly Engagement Report

REDDIT
  Posts: 21 | Avg upvotes: 7.3 | Best: 23 (r/indiehackers)
  Karma delta: +53
  Hit rate: 62% (>5 upvotes)

TWITTER
  Replies: 18 | Avg likes: 2.8 | Best: 12
  Followers delta: +7
  Avg views: 1,340

TOP 3 POSTS THIS WEEK:
  1. r/indiehackers "auth rebuild" — 23 upvotes, 5 replies
  2. @founder "reply" — 12 likes, 3,200 views
  3. r/ClaudeAI "setup" — 15 upvotes, 4 replies

RECOMMENDATIONS:
  → Shift Reddit weight to r/indiehackers (+2.4x ROI)
  → 7 unanswered replies — respond today!
```

---

## Data Schema

### engagement-log.json (append-only)

```json
{
  "entries": [
    {
      "id": "string (platform-date-seq)",
      "date": "YYYY-MM-DD",
      "platform": "reddit | twitter | linkedin | xhs",
      "type": "comment | reply | original_post",
      "subreddit": "string (reddit only)",
      "target_account": "string (twitter only)",
      "post_title": "string",
      "url": "string",
      "checked_at": "ISO8601",
      "hours_since_post": "number",
      "metrics": {
        "upvotes": "number",
        "likes": "number",
        "retweets": "number",
        "replies": "number",
        "views": "number"
      }
    }
  ]
}
```

---

## Integration with Other Skills

### Feeds Into:
- **Weekly Review** — reads weekly summary for its report
- **Content Multiply** — uses performance data to find winners worth repurposing

### Reads From:
- `memory/YYYY-MM-DD.md` — daily logs with posted URLs
- Reddit API (via AppleScript Chrome)
- Twitter API (via Twikit)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Reddit API returns 403 | Rate limited — wait 5 min, retry |
| Twikit cookie expired | Re-export cookies from Chrome |
| Comment deleted/removed | Log as `metrics: null`, note "deleted" |
| Chrome multi-profile issue | Use Method 2 (System Events + Console) from reddit-cultivate |
