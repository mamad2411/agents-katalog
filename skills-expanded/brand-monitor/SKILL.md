---
name: brand-monitor
description: Reddit brand & market intelligence engine. AI-powered onboarding — give it a brand name and it auto-generates the monitoring strategy. Supports multi-brand, layered subreddit monitoring, real-time alerts, and daily digests. Triggers on "/brand-monitor", "monitor [brand]", "check brand", "brand health", "market intelligence".
inputs:
  - name: brand_name
    type: string
    required: true
    description: The brand or competitor name to monitor on Reddit
  - name: scan_tiers
    type: list
    required: false
    description: Subreddit tiers to scan — A (high-signal), B (niche), C (broad). Defaults to all tiers.
outputs:
  - name: alerts
    type: list
    description: List of high-urgency mentions requiring immediate attention
  - name: digest
    type: text
    description: Human-readable daily digest of brand mentions and sentiment
  - name: buyer_signals
    type: list
    description: List of posts/comments showing purchase intent or competitor dissatisfaction
---

# Brand Monitor — Reddit Brand & Market Intelligence Engine

AI-powered brand monitoring system. Give it a brand name and it auto-generates a complete monitoring strategy — subreddit tiers, keywords, competitors, urgency rules. Then it runs on cron, scanning Reddit, analyzing sentiment, and pushing alerts + daily digests.

---

## Architecture

```
Phase 1: Brand Onboarding (one-time per brand)
  User says "monitor DJI" → Agent analyzes website → generates monitoring plan → user confirms → saved to config

Phase 2: Continuous Monitoring (cron-driven, every 4h)
  Read config → curl Reddit JSON → deduplicate → AI analysis → alert or archive

Phase 3: Reporting (cron-driven, daily/weekly)
  Aggregate results → generate digest → send via Telegram
```

---

## Phase 1: Brand Onboarding

When user says "monitor [brand]" or "help me monitor [brand]":

### Step 1 — Analyze the Brand

1. Ask user for the brand website URL if not provided (or search for it)
2. Use `web_fetch` to visit the brand's website
3. Extract:
   - Brand name (English + local name if applicable)
   - Product lines and sub-brands
   - Main product categories
   - Target market / use cases
4. Infer competitors based on industry knowledge + web context
5. Infer common user pain points based on product category

### Step 2 — Generate Tiered Monitoring Plan

Build a three-tier subreddit + keyword strategy:

**Tier A — Core (brand-specific communities)**
- Search for `r/{brand}` and related subreddits
- Keywords: pain points + opportunity words (no brand name needed since the community IS about the brand)
- Scan interval: every 4 hours
- Example for DJI: r/dji, r/djimini → keywords: flyaway, gimbal issue, firmware bug...

**Tier B — Category (industry communities)**
- Search for subreddits matching the product category
- Keywords: brand name + product names
- Scan interval: every 8 hours
- Example for DJI: r/drones, r/DronePhotography → keywords: DJI, Mavic, Avata...

**Tier C — Interest (broad interest communities)**
- Subreddits based on product application scenarios
- Keywords: brand name only (cast wide net)
- Scan interval: every 24 hours
- Example for DJI: r/travel, r/Filmmakers → keywords: DJI, Mavic, Osmo...

### Step 3 — Present Plan to User

Send the monitoring plan for confirmation:

```
Brand Monitor Plan — [Brand Name]

A. Core Communities (scan every 4h):
  - r/xxx — keywords: pain1, pain2, pain3...

B. Category Communities (scan every 8h):
  - r/aaa — keywords: brand1, product1, product2...

C. Interest Communities (scan every 24h):
  - r/ccc — keywords: brand1, product1

Competitors: Competitor1, Competitor2
Critical keywords: recall, injury, lawsuit, class action, fire, explode

Reply "OK" to start monitoring, or tell me what to change.
```

### Step 4 — Save Config

On user confirmation, write the brand profile to `memory/brand-monitor-config.json`.

Profile structure:
```json
{
  "brand_name": "DJI",
  "display_name": "DJI",
  "website": "https://www.dji.com",
  "enabled": true,
  "created_at": "2026-01-01T12:00:00+08:00",
  "tiers": {
    "A": {
      "subreddits": ["dji", "djimini"],
      "keywords": {
        "pain": ["flyaway", "gimbal issue", "firmware bug"],
        "opportunity": ["love my", "best purchase", "recommend"]
      },
      "scan_interval_hours": 4
    },
    "B": {
      "subreddits": ["drones", "DronePhotography"],
      "keywords": {
        "brand": ["DJI", "Mavic", "Avata", "Air 3"]
      },
      "scan_interval_hours": 8
    },
    "C": {
      "subreddits": ["travel", "Filmmakers"],
      "keywords": {
        "brand": ["DJI", "Mavic", "Osmo"]
      },
      "scan_interval_hours": 24
    }
  },
  "competitors": ["Autel", "Skydio", "Parrot"],
  "urgency_rules": {
    "critical_keywords": ["recall", "injury", "lawsuit", "class action", "fire", "explode", "dangerous", "safety hazard"],
    "high_score_threshold": 50,
    "high_comment_threshold": 20
  }
}
```

After saving, immediately run a first scan and report a summary to the user.

---

## Phase 2: Continuous Monitoring (Cron-Driven)

### Data Collection

On each cron wake:

1. Read `memory/brand-monitor-config.json` — if no profiles exist, reply `HEARTBEAT_OK`
2. Read `memory/brand-monitor-state.json` for last scan timestamps
3. For each enabled brand, check which tiers are due based on `scan_interval_hours`
4. For due tiers, fetch posts from Reddit JSON API:

```bash
# Tier A: search pain/opportunity keywords within brand community
curl -s -H "User-Agent: BrandMonitor/1.0" \
  "https://www.reddit.com/r/{subreddit}/search.json?q={keywords_OR_joined}&restrict_sr=1&sort=new&t=day&limit=25"

# Tier B/C: search brand keywords within category/interest community
curl -s -H "User-Agent: BrandMonitor/1.0" \
  "https://www.reddit.com/r/{subreddit}/search.json?q={brand_keywords_OR_joined}&restrict_sr=1&sort=new&t=day&limit=25"
```

**Rate limiting:** 3 seconds between requests, max 15 requests per cron run.

### Deduplication

Compare each post's `id` against `seen_posts` in state file. Window: 72 hours.

### AI Analysis

For each new post, analyze and produce:

```json
{
  "post_id": "t3_xxxxx",
  "subreddit": "dji",
  "tier": "A",
  "title": "Post title",
  "score": 42,
  "num_comments": 23,
  "url": "https://reddit.com/r/dji/comments/xxxxx",
  "created_utc": 1708300000,
  "sentiment": "negative",
  "intent": "bug_report",
  "urgency": "high",
  "summary": "One-line summary",
  "affected_product": "Mini 4 Pro",
  "competitor_mentioned": null,
  "recommended_action": "Suggested action"
}
```

**Sentiment values:** negative, positive, neutral, mixed  
**Intent values:** bug_report, cs_issue, feature_request, positive_showcase, newbie_question, competitor_comparison, buyer_signal, market_insight, general_discussion  
**Urgency values:** critical, high, medium, low

### Alert Routing

| Urgency | Action |
|---------|--------|
| critical | IMMEDIATELY send alert |
| high | IMMEDIATELY send alert |
| medium | Archive to daily results, include in digest |
| low | Archive to daily results only |

### Alert Format (critical/high)

```
Brand Alert — [Brand Name]

Severity: [CRITICAL/HIGH]
Post: [Title] (score: X, comments: Y)
Intent: [Bug Report / CS Issue / etc.]
Summary: [one-line summary]
Product: [affected product or "General"]
Action: [recommended action]
Link: https://reddit.com/r/xxx/comments/xxx

Reply "dig deeper" to analyze comments, or "draft reply" to generate a brand response.
```

---

## Phase 3: Reporting

### Daily Digest

For each enabled brand with results:

```
[Brand Name] Daily Digest — YYYY-MM-DD

Negative (N):
  1. [intent] Title — score/comments

Positive (N):
  1. [intent] Title — score/comments

Buyer Signals (N):
  - [summary]

Trends:
  - Top discussed topics
  - Sentiment shift vs last 7 days
  - Competitor mentions

Insights:
  - Agent's analysis and recommendations
```

### Weekly Report

```
[Brand Name] Weekly Report

Overview:
  - Total posts scanned: X
  - Alerts triggered: Y (Z critical)
  - Sentiment distribution: +N% / -N% / ~N%

Trends, Competitor Watch, Product Line Breakdown, Recommendations...
```

---

## Interactive Commands

| User Says | Agent Does |
|-----------|-----------|
| "monitor [brand]" | Start onboarding flow |
| "check [brand]" | Run immediate full scan |
| "dig deeper [post_url]" | Fetch all comments, deep sentiment analysis |
| "draft reply [post_url]" | Generate brand-appropriate response draft |
| "daily digest" | Generate and send today's digest immediately |
| "weekly report" | Generate and send weekly report immediately |
| "pause [brand]" | Set brand.enabled = false |
| "resume [brand]" | Set brand.enabled = true |
| "monitor list" | List all brand profiles with status |

---

## File Locations

| File | Purpose |
|------|---------|
| `memory/brand-monitor-config.json` | Brand profiles, subreddits, keywords, settings |
| `memory/brand-monitor-state.json` | Scan timestamps, seen posts, daily results, stats |
| `memory/brand-monitor-assets.json` | Saved UGC candidates, positive showcases |

---

## Cron Schedule

| Job | Schedule | Purpose |
|-----|----------|---------|
| Reddit Scan | Every 4h | Fetch new posts, analyze, alert |
| Daily Digest | Daily 09:00 (your TZ) | Aggregate and send results |

---

## Edge Cases

### Reddit API Rate Limited
Stop scanning, save progress, retry on next cron cycle.

### Multiple Brands
Each brand is an independent profile. Cron processes them sequentially. Prioritize Tier A across all brands if approaching request limits.

### Overlapping Subreddits
If two brands monitor the same subreddit, scan it once and apply results to both based on keyword matching.
