---
name: video-transcript-to-micro-content-repurposer
description: "Repurpose long-form video transcripts into platform-optimized micro-content: short clips with captions, pull quotes for LinkedIn/Twitter, blog snippets, and email hooks. Use when the user needs multi-channel content distribution from webinars, YouTube videos, or Loom recordings."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎬"
    }
  }
---

## Overview

The **Video Transcript to Micro-Content Repurposer** transforms long-form video transcripts into ready-to-publish micro-content across all major platforms. Instead of manually extracting highlights, generating captions, and rewriting content for different channels, this skill automates the entire workflow.

### Why This Matters

Video creators and marketing teams waste hours manually repurposing content. A 60-minute webinar transcript could yield:
- 8-12 short-form clips (TikTok, Instagram Reels, YouTube Shorts)
- 15-20 quotable pull quotes (LinkedIn, Twitter/X, Pinterest)
- 3-5 blog post sections with SEO optimization
- 10+ email subject lines and preview text hooks

This skill does all that in minutes, identifying the highest-impact moments automatically using AI analysis of engagement patterns, emotional peaks, and key concepts.

### Integrations & Platform Support

Works seamlessly with:
- **Video Platforms**: YouTube, Loom, Vimeo, Zoom transcripts
- **Content Platforms**: WordPress, Medium, Substack
- **Social**: LinkedIn, Twitter/X, TikTok, Instagram
- **Email**: Mailchimp, ConvertKit, ActiveCampaign (via templates)
- **Cloud Storage**: Google Drive, Dropbox, AWS S3
- **Video Editors**: CapCut, Adobe Premiere (JSON export for subtitles)

---

## Quick Start

### Example 1: Extract LinkedIn Pull Quotes from a Webinar

```
Transcript: [Paste your 30-min webinar transcript here]
Task: Extract 8 LinkedIn-ready pull quotes with context.
Format: Include the speaker name, timestamp, and 2-3 follow-up engagement questions per quote.
Tone: Professional but conversational, emphasis on insights that drive shares.
```

**Expected Output:**
- 8 standalone quotable moments
- Each with attribution, timestamp, and suggested hashtags
- Character count optimized for LinkedIn feed + carousel
- Suggested image dimensions (1200x627px)

---

### Example 2: Generate Short-Form Video Clips with Captions

```
Transcript: [Your YouTube video transcript]
Duration: Original video is 45 minutes
Clip Length: 60 seconds maximum per clip
Platforms: TikTok, Instagram Reels, YouTube Shorts
Task: Identify hook-worthy sections. Generate captions in SRT format with speaker identification.
Include: B-roll suggestions, pacing notes, and emotional intensity markers (0-10 scale).
```

**Expected Output:**
- 10-12 clip suggestions with exact timestamps
- SRT subtitle files ready for video editors
- Hook copy for each clip (max 280 characters)
- Recommended music/sound effect genre per clip
- Technical specs: resolution, aspect ratio, duration

---

### Example 3: Create Blog Post Snippets & SEO Metadata

```
Transcript: [Your expert interview transcript]
Length: 90-minute deep-dive conversation
Task: Extract 4 standalone blog sections (800-1200 words each).
Requirements: SEO-optimized headers, meta descriptions, internal linking suggestions.
Include: Pull quote callouts, expert credentials, CTA buttons.
Blog Platform: WordPress
```

**Expected Output:**
- 4 complete, publish-ready blog sections
- Meta titles and descriptions
- Suggested featured images (dimensions + keywords)
- Internal link recommendations
- Keyword density analysis
- Estimated read time

---

## Capabilities

### 1. **Intelligent Hook Identification**
Uses multi-model AI analysis to identify:
- Emotional peaks (excitement, revelation, urgency)
- Key concept introductions (when an idea is first mentioned)
- Story moments (case studies, customer wins, personal anecdotes)
- Contrarian statements (perspective shifts, myth-busting)
- Question prompts (calls-to-action, engagement drivers)

Each moment is scored 0-100 for repurposing potential.

### 2. **Multi-Platform Output Formatting**

#### LinkedIn
- Pull quotes (280-500 characters)
- Carousel decks (10-15 slides)
- Document shares (formatted as PDF)
- Video snippets with captions
- Hashtag recommendations (#contentmarketing #videomarketing)

#### Twitter/X
- Threads (5-15 connected tweets)
- Quote snippets (120-140 characters)
- Thread starters with engagement hooks
- Retweet-optimized versions

#### TikTok/Reels
- Hook copy (first 3 seconds critical)
- Captions with speaker identification
- Pacing recommendations
- Trending audio suggestions
- Call-to-action variations

#### Email
- Subject line variations (5 A/B test pairs)
- Preview text (50-85 characters)
- Body copy sections
- Email template recommendations
- CTA button copy

### 3. **Caption & Subtitle Generation**
- Automatic SRT/VTT formatting
- Speaker identification and color-coding
- Timestamp accuracy to within 1 second
- Multiple language support (auto-translate)
- Accessibility-optimized (punctuation, pacing)

### 4. **SEO Optimization**
- Primary keyword identification from transcript
- Meta tag generation (title, description)
- Header hierarchy (H1, H2, H3)
- Internal linking suggestions
- Featured snippet formatting
- Schema markup recommendations

### 5. **Engagement Metrics & Predictions**
- Predicted engagement score (0-100) for each clip
- Optimal posting times by platform
- Hashtag recommendations with volume/competition
- Similar trending topics
- Audience sentiment analysis

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API key (for transcript analysis and content generation)
OPENAI_API_KEY=sk-xxx

# Anthropic Claude API (optional, for fact-checking and nuanced writing)
ANTHROPIC_API_KEY=sk-ant-xxx

# Optional: Cloud storage access
GOOGLE_DRIVE_API_KEY=xxx
AWS_S3_ACCESS_KEY=xxx
AWS_S3_SECRET_KEY=xxx
```

### Setup Instructions

1. **Get your transcript** (plain text, VTT, or SRT format)
   - YouTube: Use automatic captions (Settings → Captions → Show Transcript)
   - Loom: Download transcript automatically
   - Zoom: Export from cloud recording
   - Manual: Paste from rev.com, Otter.ai, or similar

2. **Specify your platforms** (which channels are you using?)
   ```
   platforms: ["linkedin", "twitter", "tiktok", "email", "blog"]
   ```

3. **Set output preferences**
   ```
   tone: "professional" | "casual" | "educational" | "humorous"
   industry: "SaaS" | "ecommerce" | "health" | "finance" | "tech"
   clip_duration: 30 | 60 | 90  # seconds
   target_audience: "founders" | "marketers" | "developers" | "general"
   ```

---

## Example Outputs

### Output Type 1: LinkedIn Pull Quote Card

```
╔════════════════════════════════════════════════════════╗
║  "The biggest mistake companies make is assuming       ║
║   users want more features. Users want their time      ║
║   back."                                              ║
║                                                        ║
║  — Sarah Chen, Product Lead at TechCorp               ║
║    [Timestamp: 23:15]                                 ║
║                                                        ║
║  💡 What's your biggest product assumption?            ║
║  🔗 Reply in comments                                  ║
║  #ProductStrategy #UserExperience #Startup            ║
╚════════════════════════════════════════════════════════╝
Character Count: 298
Estimated Reach: 2,400-4,200 impressions
Optimal Post Time: Tuesday, 8 AM PT
```

### Output Type 2: Short-Form Video Clip Spec

```
CLIP #3: "The Pivot Moment"
Duration: 58 seconds
Timestamp: 34:12 — 35:10
Engagement Score: 87/100
Hook Type: Contrarian Statement + Story

HOOK COPY (First 5 seconds):
"We spent 2 years building the wrong thing. Here's what we learned."

CAPTIONS (SRT format):
00:00:00,000 --> 00:00:03,000
We spent 2 years building the wrong thing.

00:00:03,500 --> 00:00:06,800
Here's what we learned about product market fit.

[... continues through 00:00:58 ...]

PLATFORMS: TikTok, Instagram Reels, YouTube Shorts
ASPECT RATIO: 9:16 (vertical)
RESOLUTION: 1080x1920 minimum

B-ROLL SUGGESTIONS:
- Screen recording of old product (0-5 sec)
- Customer feedback (5-15 sec)
- Current product demo (15-55 sec)
- Call-to-action graphic (55-58 sec)

MUSIC/SOUND: Uplifting, contemplative tone (Spotify: "Indie Focus" playlist)
PACING: Slow reveal, builds to insight at 45 sec
```

### Output Type 3: Email Subject Line A/B Tests

```
Subject Line Pair #1 (Test Audience: 25%)
A: "We wasted 2 years building this (here's the lesson)"
B: "The $500K mistake that taught us about product-market fit"
Expected Winner: B (curiosity gap + specificity)
Send Time: Tuesday 10 AM

Subject Line Pair #2 (Test Audience: 25%)
A: "Product strategy: The contrarian take"
B: "Why more features actually hurt your users"
Expected Winner: B (concrete benefit)
Send Time: Tuesday 10 AM

Winner Send: Thursday, both audiences (50%)
Control: Your standard subject line to 25%

Preview Text Suggestions (50-85 chars):
"We learned the hard way about feature bloat. Here's our framework..."
```

### Output Type 4: Blog Post Section (SEO-Ready)

```
BLOG POST SECTION: "Building Products Users Actually Want"

SEO METADATA:
- Primary Keyword: "product-market fit strategy" (monthly volume: 890)
- Secondary Keywords: "feature creep", "user feedback", "MVP development"
- Meta Title: "Product-Market Fit: Why More Features Hurt Growth (Case Study)"
- Meta Description: "Learn the $500K lesson about feature bloat. Real strategy for building products users actually want in 2024."
- Word Count: 1,247 words
- Estimated Read Time: 5 minutes

CONTENT:
---
## Why More Features Actually Hurt Your Growth

Sarah Chen, Product Lead at TechCorp, made a discovery that changed how her team thinks about product development.

"We spent 2 years building features," she explains in an recent interview. "And we completely missed what users actually wanted."

### The $500K Mistake

[Full section with blockquotes, subheaders, examples...]

> "The biggest mistake companies make is assuming users want more features. Users want their time back." — Sarah Chen

### The Framework We Use Today

[Detailed methodology section...]

---

INTERNAL LINKING SUGGESTIONS:
- Link "MVP development" → your guide on building MVPs
- Link "user feedback loops" → your customer research article
- Suggest this post link back from: "Feature Prioritization Framework"

FEATURED IMAGE:
- Dimensions: 1200x627px
- Alt Text: "Product roadmap showing prioritized features vs. MVP scope"
- Suggestion: Chart showing feature adoption curve
- Designer Brief: Show contrast between complex vs. simple product interfaces

CALL-TO-ACTION:
- Primary CTA: "Download our Product Strategy Checklist" (pdf lead magnet)
- Secondary CTA: "Read our case study on market fit" (internal link)
- Placement: After section 2, end of post

SCHEMA MARKUP RECOMMENDED:
- Article schema
- FAQPage schema (if FAQs included)
- Author schema (Sarah Chen credentials)

---
```

---

## Tips & Best Practices

### 1. **Transcript Quality Matters**
- **Use auto-captions** when possible (YouTube, Zoom are highly accurate)
- **Clean up common errors** before processing:
  - Remove timestamps if using raw text export
  - Fix obvious speech-to-text errors (names, technical terms)
  - Remove filler words if you want more polished quotes

**Pro Tip:** If using Otter.ai or Rev, request "verbatim" transcripts (they preserve natural speech patterns better).

### 2. **Optimize for Your Audience First**
Don't just repurpose for all platforms equally. Ask yourself:
- Which platform does my audience actually use? (B2B execs on LinkedIn, creators on TikTok)
- What's the maturity of my audience? (Students need simple language; CTOs want technical depth)
- What action do you want? (LinkedIn drives B2B leads; TikTok builds awareness)

**Pro Tip:** Use the `target_audience` parameter to ensure all outputs match your ICP.

### 3. **The 70/20/10 Rule for Content Mix**
- **70%:** Educational/value content (frameworks, tips, lessons learned)
- **20%:** Behind-the-scenes/personal stories (builds relatability)
- **10%:** Direct promotion (product, course, book, CTA)

Use this skill's engagement prediction scores to verify your mix aligns.

### 4. **Batching Creates Compounding Returns**
- Repurpose 1 long-form video → 40-50 pieces of micro-content
- Schedule this content over 3-4 months
- Compound effect: Each piece drives backlinks, cross-platform discovery, brand presence

**Pro Tip:** Use the skill on your competitor's videos too (public, educational content only). See what resonates.

### 5. **Captions Dramatically Increase Video Completion**
- Videos with captions have 25% higher watch-through rate
- 85% of video is watched with sound OFF (mobile use case)
- Use this skill's SRT export directly in CapCut, Premiere, or YouTube Studio

**Pro Tip:** Add captions even to platform-native uploads (not just external embeds).

### 6. **Email Subject Lines Are Your Biggest Leverage**
- A/B testing one subject line can increase CTR by 20-50%
- Use the predicted winner recommendation, but always test in your market
- The skill suggests 5 pairs; test the top 2 pairs first, then scale the winner

### 7. **SEO Compounds Over Months**
- Each blog snippet is a separate keyword target
- Link them to each other (internal linking boost SEO)
- Republish the same content in 6 months (Google loves fresh updates)

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Fabricate information.** All outputs are extracted/derived from your source transcript. We don't add facts, stats, or claims not in the original video.

❌ **Bypass copyright.** You must own, have license to, or have permission to repurpose the source video. Check:
- Your original video rights
- Guest speaker permissions (especially for interviews)
- Licensed music/imagery rights
- Platform ToS (YouTube, LinkedIn, etc.)

❌ **Publish without review.** AI-generated content should always be reviewed by a human before publishing:
- Verify tone matches your brand voice
- Check facts and attributions
- Ensure context isn't lost in extraction
- Validate punctuation and emoji use

❌ **Create deepfakes or manipulated video.** This skill generates text and captions, not altered video content. All output is authentic to source material.

❌ **Guarantee engagement metrics.** Predictions (87/100 engagement score) are estimates based on content analysis, not guarantees. Actual performance depends on:
- Your audience size and loyalty
- Timing of posts
- External trending topics
- Platform algorithm changes

### Boundaries & Limitations

🔸 **Transcript accuracy:** Skill quality = source transcript quality.