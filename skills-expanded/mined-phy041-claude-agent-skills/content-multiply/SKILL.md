---
name: content-multiply
description: Data-driven content multiplication engine. Detects high-performing posts via engagement data, then auto-generates adapted versions for other platforms. One piece of content → 3-5 derivatives. Triggers on "multiply content", "repurpose top posts", "content multiply", "cross-post winners", "what should I repurpose".
inputs:
  - name: engagement_data
    type: json
    required: true
    description: Engagement metrics from engagement-tracker output — list of {platform, url, upvotes, views, replies}
outputs:
  - name: derivatives
    type: list
    description: List of repurposed content pieces, each with {source_url, platform, content, suggested_date}
---

# Content Multiplication Engine

When a post crosses an engagement threshold, automatically generate adapted versions for other platforms. One insight, many formats. Data-driven, not guesswork.

---

## Why Data-Driven Repurposing Beats Calendar Repurposing

| | Calendar-Based Repurposing | Content Multiplication Engine |
|---|---|---|
| **Trigger** | Time (every Friday) | Data (engagement threshold crossed) |
| **Input** | "Review this week's content" (vague) | Specific post with proven engagement |
| **Output** | Suggestions | Actual drafted derivatives ready to review |
| **Signal** | No signal — reviews everything | Engagement data proves the post works |
| **Confidence** | Low (guessing what might work) | High (it already worked on one platform) |

**Key insight:** A Reddit comment with 30 upvotes is a proven winner. Adapting it for Twitter/LinkedIn has much higher expected value than creating new content from scratch.

---

## Engagement Thresholds

Posts crossing these thresholds trigger multiplication:

| Platform | Content Type | Default Threshold | Notes |
|----------|-------------|-------------------|-------|
| Reddit | Comment | ≥ 15 upvotes | Adjust based on your account size |
| Reddit | Original post | ≥ 25 upvotes | |
| Twitter | Reply | ≥ 5 likes OR ≥ 2,000 views | Lower for smaller accounts |
| Twitter | Original tweet | ≥ 10 likes OR ≥ 5,000 views | |
| LinkedIn | Post | ≥ 500 impressions OR ≥ 10 reactions | |
| XHS | Post | ≥ 50 saves (collections) | XHS gold metric — saves > likes |

**Thresholds should start LOW** for new accounts. Raise them as engagement grows (review monthly).

### Threshold Config (in state file)

```json
"thresholds": {
  "reddit_comment_upvotes": 15,
  "reddit_post_upvotes": 25,
  "twitter_reply_likes": 5,
  "twitter_reply_views": 2000,
  "twitter_post_likes": 10,
  "twitter_post_views": 5000,
  "linkedin_reactions": 10,
  "xhs_saves": 50
}
```

---

## Workflow

### Step 1: Read Engagement Data

Read `memory/analytics/engagement-log.json` and find entries that:
1. Cross the engagement threshold
2. Are NOT already processed (avoid re-processing)
3. Are less than 7 days old (stale content doesn't multiply well)

### Step 2: Determine Multiplication Routes

| Source Platform | → Target Platforms |
|----------------|-------------------|
| **Reddit comment** | Twitter, LinkedIn |
| **Reddit post** | Twitter thread, LinkedIn, XHS carousel, DEV.to (if technical) |
| **Twitter reply** | Reddit comment, LinkedIn insight |
| **Twitter original** | LinkedIn, Reddit, XHS |
| **LinkedIn post** | Twitter (compress), XHS (translate + adapt) |
| **XHS post** | Twitter (English extract), LinkedIn |

### Step 3: Generate Derivatives

#### Reddit Comment → Twitter Post

```
Source: Reddit comment (15+ upvotes)

Twitter version:
"[Extract the core insight from the comment]
[Reframe for Twitter audience — shorter, punchier]"
```

Rules:
- Strip Reddit-specific context
- Lead with the insight, not the backstory
- Under 280 chars for single tweet, or 3-5 tweets for thread

#### Reddit Comment → LinkedIn Post

```
LinkedIn version:
"[Professional hook — what's the business/career implication?]
[Expand the insight with professional context]
[Tie to a broader theme: productivity, AI tools, builder mindset]
[Soft CTA: What's your experience with X?]"
```

Rules:
- More formal tone, still personal
- Add "why this matters" framing
- Under 3000 chars, plain text only

#### Any Winner → XHS Carousel Suggestion

If a winner has enough substance for 3+ slides:

```json
{
  "template": "dark",
  "slides": [
    {"type": "cover", "title": "[Chinese title]", "subtitle": "[Chinese subtitle]"},
    {"type": "content", "title": "[Point 1]", "number": 1, "body": "[Details]"},
    {"type": "list", "title": "[Key steps]", "items": ["item 1", "item 2"]},
    {"type": "summary", "title": "总结", "points": ["takeaway 1", "takeaway 2"], "cta": "关注获取更多干货"}
  ]
}
```

→ Generate with `xhs-image-gen` skill

---

## Scheduling Rules (CRITICAL)

1. **NEVER publish all derivatives on the same day.** Space over 2-3 days minimum.
2. **Stagger by platform priority:**
   - Day 0: Original platform (already posted)
   - Day 1: Twitter — fastest audience turnover
   - Day 2: LinkedIn — professional audience
   - Day 3: XHS (if carousel) — needs Chinese audience peak time
3. **Weekend boost:** If derivative ready on Friday, suggest LinkedIn for Tuesday (engagement drops on weekends).
4. **Don't stack with other scheduled posts.** Check content calendar for conflicts.

---

## Approval Flow

```
Content Multiplier — [date]

[N] post(s) crossed engagement thresholds!

--- Winner #1 ---
Source: [platform] | [title/topic] | [metric]: [value]
Original: [URL]

Derivatives:

1. Twitter post (suggested: post tomorrow)
   "[draft]"

2. LinkedIn post (suggested: post in 2 days)
   "[draft]"

3. XHS carousel (suggested: post in 3 days)
   [content structure or "generate with xhs-image-gen?"]

Reply:
  "post all" — queue all on suggested schedule
  "skip 2" — skip derivative #2
  "change 1: [text]" — edit derivative #1
  "not now" — skip everything
```

### User Responses

| User says | Action |
|-----------|--------|
| "post all" | Queue all derivatives on suggested schedule |
| "post now" | Post immediately |
| "skip 2" / "skip linkedin" | Skip specific derivative |
| "change 1: [text]" | Edit specific derivative |
| "not now" / "skip" | Skip everything |
| No reply | Do nothing. NEVER auto-post. |

---

## State File

Location: `memory/analytics/content-multiply-state.json`

```json
{
  "last_checked_at": "ISO8601",
  "thresholds": { ... },
  "multiplied": [
    {
      "source_id": "reddit-2026-01-01-001",
      "source_platform": "reddit",
      "source_metric": {"upvotes": 48},
      "detected_at": "ISO8601",
      "derivatives": [
        {
          "platform": "twitter",
          "status": "posted",
          "posted_at": "ISO8601",
          "url": "https://x.com/..."
        },
        {
          "platform": "linkedin",
          "status": "pending_approval",
          "suggested_date": "YYYY-MM-DD"
        }
      ]
    }
  ],
  "stats": {
    "total_winners_detected": 0,
    "total_derivatives_posted": 0
  }
}
```

---

## Quality Gate

Before sending derivatives:

- [ ] Hook is adapted for the target platform (not copy-pasted from source)
- [ ] Length fits platform limits (Twitter: 280, LinkedIn: 3000, XHS: 1000 chars)
- [ ] No hype words in any derivative
- [ ] Derivatives are meaningfully different from each other
- [ ] Suggested schedule doesn't conflict with other planned posts
- [ ] Would someone who saw the original NOT feel like they're seeing the same thing?

---

## Content Flywheel

```
CREATE          MEASURE           MULTIPLY          MEASURE AGAIN
  ↓                ↓                 ↓                   ↓
Reddit post → Engagement Tracker → Content Multiply → Engagement Tracker
                (daily check)       (daily check)       (next day)
                                                         ↓
                                                    If derivative also
                                                    crosses threshold...
                                                    MULTIPLY AGAIN!
```

### Connected Skills

| Skill | Relationship |
|-------|-------------|
| **Engagement Tracker** | Provides the data (upstream) |
| **Ship Digest** | Creates original content that feeds into this engine |
| **GitHub Monitor** | Creates launch posts that can be multiplied |
| **XHS Image Gen** | Generates carousel images for XHS derivatives |

---

## Edge Cases

### No Winners This Period
Normal. Not every post will cross thresholds. Reply `HEARTBEAT_OK`.

### Too Many Winners (5+ in one day)
Prioritize by engagement magnitude. Pick top 3, save the rest for tomorrow.

### Winner Already Manually Repurposed
Check daily memory logs for same topic on multiple platforms. Skip if already repurposed.
