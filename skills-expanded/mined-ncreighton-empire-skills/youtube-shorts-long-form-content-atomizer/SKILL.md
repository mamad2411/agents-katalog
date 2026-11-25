---
name: youtube-shorts-long-form-content-atomizer
description: "Transform viral YouTube Shorts into SEO-optimized long-form content across 5 platforms instantly. Use when the user needs multi-format content repurposing, engagement analysis, and cross-platform distribution without manual rewriting."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["YOUTUBE_API_KEY","OPENAI_API_KEY"],"bins":["ffmpeg"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📹"}}
---

## Overview

The **YouTube Shorts → Long-Form Content Atomizer** is a production-grade content repurposing engine that automatically converts viral short-form videos into 3-5 distinct long-form pieces tailored for specific platforms. 

This skill analyzes YouTube Shorts by **view velocity** (virality trajectory), **engagement rate** (comments, likes, shares), and **comment sentiment** (audience reception), then intelligently reframes the core message as:

1. **SEO-optimized blog posts** (1,200-2,500 words) with meta descriptions
2. **LinkedIn professional articles** (800-1,200 words) with executive insights
3. **Twitter/X thread scripts** (12-15 tweets with threading markup)
4. **Email newsletter sequences** (3-part nurture with CTAs)
5. **Podcast episode scripts** (8-12 minute transcripts with timestamps)

Each output includes:
- **Hook extraction** — identifies what makes the original viral
- **Angle repositioning** — reframes the narrative for each platform's audience
- **SEO metadata** — keywords, internal linking suggestions, schema markup
- **Platform-specific formatting** — hashtags, CTA buttons, call-to-action copy
- **Engagement predictions** — projected CTR, shares, and comment likelihood

**Integrations**: YouTube Data API v3, OpenAI GPT-4, WordPress (via REST API), LinkedIn Share API, Google Search Console, Slack (for delivery), native exports to Markdown/JSON/HTML.

---

## Quick Start

### Example 1: Analyze a Single Viral Short

```
Atomize this YouTube Short: https://youtu.be/dQw4w9WgXcQ

Focus on the hook and reposition it for:
- Blog post (SEO angle: "productivity hacks")
- LinkedIn article (thought leadership angle)
- Twitter thread (viral engagement angle)

Include sentiment analysis of top 50 comments.
```

### Example 2: Batch Process a Creator's Last 10 Shorts

```
Creator: @TechInfluencer (channel ID: UC_x5XG1OV2P6uZZ5FSM9Ttw)

Criteria:
- Minimum 500K views
- Engagement rate > 8%
- Upload date: last 30 days

Generate:
- 1 comprehensive blog post (combine themes)
- 5 individual Twitter threads (one per video)
- 1 newsletter sequence (3-email arc)
- Slack notification with preview links

Output format: JSON + Markdown files + WordPress drafts
```

### Example 3: Deep-Dive Single Content Atomization

```
YouTube Short URL: https://youtu.be/abc123xyz

Analyze:
- Transcription (auto-caption + context)
- View velocity (daily growth rate)
- Comment sentiment breakdown
- Top 5 hooks (extracted from video + comments)

Generate all 5 content formats with:
- Internal linking suggestions (to my existing posts)
- Recommended hashtags (research current trends)
- Optimal posting times (by platform)
- A/B testing subject lines (for email)
- Thumbnail/featured image prompts (DALL-E compatible)
```

---

## Capabilities

### 1. Video Analysis Engine
- **Automatic transcription** via YouTube captions (English, Spanish, French, German, Japanese)
- **View velocity calculation** — hours-to-100K, growth curve trajectory
- **Engagement metrics extraction** — like ratio, comment density, share velocity
- **Sentiment analysis** — positive/negative/neutral breakdown of top comments
- **Topic extraction** — 3-5 primary themes using NLP clustering
- **Hook identification** — first 3-5 seconds analyzed for attention triggers

### 2. Content Generation (All Formats)

**Blog Posts (SEO-Optimized)**
- Title + meta description (150 chars)
- H1 structure with keyword targeting
- Internal linking suggestions
- Schema markup (Article schema)
- Reading time estimate
- CTA button code (HTML)

**LinkedIn Articles**
- Professional tone, executive-friendly
- 3-act narrative structure
- Conversation starters (questions to engage)
- Recommended hashtags (trending in your industry)
- Author byline template

**Twitter/X Threads**
- 12-15 connected tweets
- Thread numbering format (1/15, 2/15, etc.)
- Hashtag strategy (primary + trend research)
- Emoji optimization for engagement
- Thread conclusion with CTA

**Email Sequences**
- 3-part nurture arc (Awareness → Interest → Action)
- Subject lines A/B variants
- Preheader text optimization
- Segmentation suggestions
- Click tracking placeholders (UTM-ready)

**Podcast Scripts**
- 8-12 minute reading duration
- Timestamp breakpoints for chapters
- Intro/outro templates
- Question prompts for guest interviews
- Ad-read integration points
- Sound effect cues

### 3. SEO & Distribution Tools
- **Keyword research** — related search terms, monthly volume, competition
- **Internal linking map** — suggests which existing pages to link to
- **Readability scoring** — Flesch-Kincaid grade level, AIDA alignment
- **Meta tag generation** — og:image, og:description, Twitter card format
- **Schema markup** — automatic JSON-LD for SEO
- **Optimal posting times** — platform-specific (based on audience timezone data)

### 4. Angle Repositioning
Automatically reframes core message for each audience:
- **Busy professional** (LinkedIn) → "How I saved 5 hours/week using..."
- **SEO audience** (blog) → "The complete guide to [topic] in 2024..."
- **Social-first audience** (Twitter) → "Everyone's doing [wrong thing]... Here's the actual way..."
- **Email subscribers** → Problem-agitation-solution framework
- **Podcast listeners** → Story-driven narrative with personal lessons

---

## Configuration

### Required Environment Variables

```bash
YOUTUBE_API_KEY=AIzaSyD...          # YouTube Data API v3 key
OPENAI_API_KEY=sk-proj-...          # GPT-4 access for content generation
WORDPRESS_API_TOKEN=xxxxx           # Optional: WP REST API token
LINKEDIN_ACCESS_TOKEN=xxxxx         # Optional: LinkedIn Share API token
```

### Optional Configuration

```bash
# Content generation preferences
TONE_PROFILE=professional           # professional | casual | educational | humorous
TARGET_AUDIENCE=entrepreneurs       # entrepreneurs | executives | students | general
CONTENT_LENGTH_PREFERENCE=medium     # short | medium | long

# Platform delivery
SLACK_WEBHOOK_URL=https://hooks...  # For notifications
WORDPRESS_SITE_URL=https://...      # Auto-post as drafts
BUFFER_API_TOKEN=xxxxx              # Queue to Buffer for scheduling

# Analysis preferences
MIN_VIEW_THRESHOLD=100000           # Skip videos with fewer views
SENTIMENT_ANALYSIS_DEPTH=50         # Number of top comments to analyze
LANGUAGE_DETECTION=auto             # auto | en | es | fr | de | ja
```

### Setup Instructions

1. **Get YouTube API Key** (free tier: 10K units/day)
   - Go to Google Cloud Console → Create Project
   - Enable YouTube Data API v3
   - Create OAuth 2.0 credentials (API key)

2. **Get OpenAI API Key** (pay-per-use)
   - Visit platform.openai.com/api/keys
   - Create new secret key
   - Estimated cost: $0.03-$0.15 per atomization (GPT-4)

3. **Install FFmpeg** (for video metadata extraction)
   ```bash
   # macOS
   brew install ffmpeg
   
   # Linux
   sudo apt-get install ffmpeg
   
   # Windows
   choco install ffmpeg
   ```

4. **Authenticate** (first run)
   ```bash
   claw skill authenticate youtube-shorts-long-form-content-atomizer
   ```

---

## Example Outputs

### Output 1: Blog Post (Excerpt)

```markdown
# 5 Productivity Hacks That Actually Work (The Science-Backed Edition)

**Meta Description:** Discover 5 science-backed productivity hacks that increase 
focus by 47%. Learn from viral YouTube experiments + implement in 24 hours.

**Reading Time:** 6 minutes | **SEO Score:** 92/100

## Hook: Why This Matters
Most productivity advice fails because it ignores how your brain actually works...

## The 5 Hacks
1. **The 90-Minute Ultradian Rhythm** (backed by Kleitman's research)
   - [Internal link to: "Sleep Science for Peak Performance"]
   - Why it works: Your brain naturally cycles between focus/rest
   - Implementation: Set 90-min timers, rest for 15-20 min

[...continued content with H2/H3 structure, internal links, CTA...]

**Internal Links Suggested:**
- Sleep Science for Peak Performance (anchor: "sleep research")
- Time Management Tools Compared (anchor: "productivity tools")

**Recommended Featured Image:** [DALL-E prompt: "Professional minimalist desk at 
sunrise with timer, notebook, green plant. Warm lighting."]

**CTA Button:**
<a href="/email-course" class="cta-primary">Get My 5-Day Focus Masterclass →</a>
```

### Output 2: Twitter Thread

```
1/14
Everyone wastes time on the wrong tasks. Here's what science says about the 
90-minute focus cycle (and why your 8-hour workday might be lying to you) 🧠⏱️

2/14
Researcher Nathaniel Kleitman found that your brain naturally moves through 
~90-minute cycles of high focus → gradual decline → need for rest.

The problem? We ignore these cycles and push through...
```

### Output 3: Email Sequence (Subject Lines)

```
EMAIL 1 (Awareness)
Subject A: "The 90-minute trick that changed my productivity"
Subject B: "Why 8-hour workdays don't exist (and what actually works)"
Open rate prediction: 32% | Recommendation: Test Subject A first

EMAIL 2 (Interest)
Subject A: "Here's how I structured my days..."
Subject B: "[Framework] I use to plan my week"
Open rate prediction: 24%

EMAIL 3 (Action)
Subject A: "Join 5,000+ people using this system"
Subject B: "Ready to try it? (Simple guide inside)"
Open rate prediction: 18% | CTA: "Enroll Now" (38% CTR predicted)
```

---

## Tips & Best Practices

### 1. Maximize Virality Score
- **Input**: Videos with 500K+ views and >8% engagement rate perform best
- **Analysis**: Look at comment sentiment first—negative sentiment can reveal pain points worth exploiting
- **Reposition**: If sentiment is mixed, address objections in your blog post FAQ section

### 2. SEO Optimization Strategy
- Blog posts should target a **primary keyword** (500-750 word focus per post)
- Use the "People Also Ask" suggestions from YouTube comments
- Link internally to 3-4 existing posts (if you have them)
- Publish 24-48 hours after YouTube Short goes live (freshness boost)

### 3. Platform-Specific Wins
- **LinkedIn**: Post after atomization on **Tuesday-Thursday, 8-10 AM local time** (highest engagement)
- **Twitter/X**: Thread performs best posted at **9 AM or 6 PM** (peak activity windows)
- **Blog**: Publish on **Wednesdays** (SEO lift, reduced competition)
- **Email**: Send sequences **Monday 9 AM or Thursday 2 PM** (highest open rates)

### 4. Batch Processing for Efficiency
- Atomize 5-10 Shorts at once to amortize API costs ($0.15-$0.50 per Shorts vs. $0.03-$0.15 in batch)
- Use the same research/keywords across outputs (reduce duplicate API calls)
- Generate all formats simultaneously (save 60% processing time)

### 5. Engagement Hack: Hooks Library
- Extract and save top-performing hooks from each Short
- Build a "hooks swipe file" to reference for future content
- Reuse hook structures (but reskin for new topics) for 3x faster writing

### 6. WordPress Integration
- Auto-post atomized blog content as **drafts only** (review before publishing)
- Use featured image prompts to generate images via Unsplash API
- Tag posts automatically with extracted topics
- Schedule via WordPress native scheduler (24-72 hours post-creation)

---

## Safety & Guardrails

### What This Skill WILL NOT Do

❌ **Not a plagiarism tool** — The skill generates *original* content inspired by the Short's themes, not direct transcriptions. Each output is 70-90% newly written based on the topic.

❌ **Not authorized for copyrighted music/video usage** — Analysis includes the video topic/narrative only. Never republishes copyrighted audio or video clips. You are responsible for music licensing in podcasts/videos you create.

❌ **Not a factual verification engine** — The skill assumes input video content is accurate. It does NOT fact-check claims. Verify all statistics, quotes, and attributions before publishing.

❌ **Not designed for misinformation/spam** — The skill will refuse to generate content designed to mislead, deceive, or violate platform ToS (e.g., artificial engagement manipulation, scams, hate speech).

❌ **Not for private/restricted videos** — Only works on publicly visible YouTube Shorts. Cannot process private videos or age-restricted content.

### Content Boundaries

**Acceptable Use Cases:**
- Original creator repurposing their own content ✅
- Marketers extending reach of brand-owned videos ✅
- Educators transforming lesson content ✅
- Journalists expanding story angles ✅

**Prohibited Use Cases:**
- Republishing others' content without permission ❌
- Generating "deepfake" or altered attributions ❌
- Circumventing platform monetization/copyright systems ❌
- Creating engagement bait or clickbait ❌

### Rate Limits & Costs

- **YouTube API**: 10,000 units/day (free tier). Single atomization ≈ 100-200 units
- **OpenAI API**: $0.03-$0.15 per atomization (based on model + content length)
- **Recommended budget**: $50-100/month for 100-200 atomizations

### Attribution & Ethics

- Always credit original creator when republishing (blog: byline + link, LinkedIn: tag/mention)
- Disclose AI-assisted content creation per FTC guidelines (if required in your jurisdiction)
- Include original video URL in all republished content

---

## Troubleshooting

### Common Issues & Solutions

#### ❓ Issue: "Invalid YouTube URL" or "Video Not Found"
**Solution:** 
- Verify URL is a public YouTube Short (format: `youtube.com/shorts/[VIDEO_ID]`)
- Check video isn't age-restricted or private
- Ensure YouTube API key has correct permissions (YouTube Data API v3, not YouTube Analytics)

#### ❓ Issue: "OpenAI API Error: Insufficient Tokens"
**Solution:**
- Check OpenAI account has active billing method
- Monitor API usage at platform.openai.com/account/usage
- Consider using GPT-3.5-turbo (cheaper, 30% faster) for drafts: set `OPENAI_MODEL=gpt-3.5-turbo`

#### ❓ Issue: "Content Generation is Very Generic/Repetitive"
**Solution:**
- Add context prompt: `"Write in a [specific industry] style. Target audience: [specific persona]"`
- Increase creativity parameter: Set `TEMPERATURE=0.8` (default: 0.7)
- Provide sample "tone reference" from existing content you like
- Use `CONTENT_LENGTH_PREFERENCE=long` to force deeper exploration

#### ❓ Issue: "Engagement Predictions Are Inaccurate"
**Solution:**
- Skill provides *baseline* predictions for new creators; accuracy improves with historical data
- Once you've published 5+ pieces, provide past performance metrics for calibration
- Predictions assume similar audience