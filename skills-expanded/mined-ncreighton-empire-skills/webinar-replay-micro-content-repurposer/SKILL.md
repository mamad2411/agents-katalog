---
name: webinar-replay-micro-content-repurposer
description: "Transform webinar recordings into 40+ social clips, email sequences, and marketing assets. Use when the user needs to repurpose video content, create social media campaigns, or automate lead nurture workflows from webinars."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","YOUTUBE_API_KEY","ASSEMBLY_AI_KEY"],"bins":["ffmpeg"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🎬"}}
---

## Overview

The **Webinar Replay Micro-Content Repurposer** automates the extraction and transformation of webinar recordings into a complete content ecosystem. Feed it a video file or YouTube link, and it delivers:

- **8-12 key moment timestamps** (Q&A, product demos, objection handling, success stories)
- **Clip-specific social media hooks** (LinkedIn, Twitter/X, Instagram, TikTok formats)
- **Email follow-up sequences** tied to each moment for segmented nurture
- **SEO-optimized transcripts** for blog posts
- **Visual assets** recommendations (thumbnails, captions)
- **Engagement metrics** framework for each piece

**Why this matters:** A single 60-minute webinar typically generates $800-2,500 in production value. Most teams extract 2-3 pieces of content and leave 85-90% on the table. This skill automatically unlocks 40-60 derivative assets from one source, multiplying your content ROI across WordPress, LinkedIn, email platforms (HubSpot, Marketo, ConvertKit), and social scheduling tools (Buffer, Later, Hootsuite).

**Integrations supported:** YouTube, Vimeo, AWS S3, Google Drive, Zapier, WordPress REST API, Slack webhooks, HubSpot CRM, Marketo, SFDC.

---

## Quick Start

Try these prompts immediately to see the repurposer in action:

### Example 1: YouTube Webinar
```
Repurpose this webinar into micro-content:
URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Title: "Advanced SaaS Sales Tactics for SMBs"
Duration: ~45 minutes
Audience: Sales directors, founders
Tone: Conversational, educational
Social platforms: LinkedIn, Twitter, TikTok
Email segments: Free tier users, enterprise prospects
Output format: JSON with timestamps, hooks, and sequences
```

### Example 2: Local Video File
```
Analyze this webinar recording for micro-content repurposing:
File: webinar-Q3-marketing-trends.mp4
Format: MP4 (1080p, 58 minutes)
Key topics: Content marketing, AI, influencer partnerships
Company: B2B SaaS (MarTech)
Extract: 10 key moments, 4 social hooks per clip, nurture sequences
Include: Transcript highlights, speaker quotes, CTA recommendations
Output JSON with clip durations, best-performing platforms, and suggested posting schedule
```

### Example 3: Batch Processing
```
Repurpose 3 webinars into a content calendar:
Webinars:
1. "Product Roadmap 2025" (YouTube link)
2. "Customer Success Stories" (S3 file)
3. "Competitive Positioning" (Vimeo link)

Create:
- 40+ social clips (LinkedIn, Twitter, Instagram)
- 9 email nurture sequences (1 per webinar segment)
- Blog outline with embedded clips
- Slack notification with top 3 moments
Output: Content calendar (CSV), Zapier integration config, email templates
```

---

## Capabilities

### 1. Intelligent Moment Detection
The skill identifies 8-12 key moments using speech analysis, sentiment detection, and engagement heuristics:

- **Audience Questions** — Auto-flags Q&A segments; extracts objections
- **Product/Feature Demos** — Detects "show you," "looks like," screen shares
- **Success Stories/Case Studies** — Identifies customer mentions, metrics, results
- **Expert Quotes** — Captures quotable statements for social amplification
- **Call-to-Action Moments** — Flags natural CTAs for lead capture
- **Pain Point Discussions** — Extracts common challenges for email nurture
- **Humorous/Viral Moments** — Detects lighter segments for TikTok/short-form video
- **Objection Handling** — Captures "common concern is..." responses

**Output example:**
```json
{
  "moments": [
    {
      "id": 1,
      "type": "demo",
      "timestamp": "12:34-14:22",
      "duration_seconds": 108,
      "transcription": "Let me show you how the automation actually works...",
      "sentiment": 0.89,
      "engagement_score": 9.2
    },
    {
      "id": 2,
      "type": "objection_handle",
      "timestamp": "22:15-24:47",
      "transcription": "The most common concern is about implementation time...",
      "emotional_trigger": "concern_relief"
    }
  ]
}
```

### 2. Social Media Hook Generation
For each key moment, generates 3-5 platform-specific hooks:

- **LinkedIn** — Professional takeaway + connection call; 150-300 words
- **Twitter/X** — Punchy insight + engaging question; 280 characters max
- **Instagram** — Aspirational headline + story hook; caption + hashtags
- **TikTok** — Snackable hook + trend alignment; 15-60 second concept
- **YouTube Shorts** — Thumbnail concept + pattern interrupt hook

**Example output:**
```json
{
  "moment_id": 1,
  "clip_title": "The Automation Demo That Changed Everything",
  "hooks": {
    "linkedin": {
      "copy": "Most teams spend 40+ hours/week on manual workflows. Watch this 2-minute demo to see how [Company] cut that to 4 hours. The difference? Intelligent automation.",
      "cta": "Link in comments to learn more",
      "hashtags": ["Automation", "Productivity", "B2B"]
    },
    "twitter": {
      "copy": "40 hours → 4 hours. That's not a typo. See how intelligent automation is reshaping team productivity. 🚀",
      "engagement_q": "What manual task wastes your team's time most?"
    },
    "tiktok": {
      "hook": "Watch how this team automated their entire workflow (hint: they didn't expect this to work)",
      "trend": "before_after_transformation",
      "trending_audio": "upbeat_motivational"
    }
  }
}
```

### 3. Email Sequence Generation
Builds segmented, multi-step nurture flows tied to webinar moments:

- **Segment 1** — Attended live (send 24 hours after)
- **Segment 2** — Watched replay (send 48 hours after)
- **Segment 3** — Clicked specific clip (send 72 hours after)
- **Segment 4** — Free tier users (send deal-focused sequence)
- **Segment 5** — Enterprise prospects (send ROI-focused sequence)

Each email includes:
- **Subject line** with A/B test variant
- **Hook** tied to specific moment
- **Social proof** (attendee count, engagement metric)
- **CTA** (watch clip, schedule demo, download case study)
- **Unsubscribe compliance** (GDPR, CAN-SPAM)

**Example:**
```json
{
  "sequence_name": "Demo-Driven nurture",
  "segment": "free_tier_users",
  "emails": [
    {
      "email_1": {
        "subject": "The 2-minute workflow demo 427 of you watched",
        "subject_variant_b": "See how teams saved 36 hours/week",
        "send_delay_hours": 24,
        "body": "Hi [FirstName],\n\nThanks for attending our webinar. I wanted to share the moment that got the most engagement: our live workflow automation demo.\n\nThis 2-minute clip shows exactly how to cut manual work from 40+ hours to just 4.\n\n[WATCH CLIP BUTTON]\n\nAfter you watch, let me know: what's your biggest time-drain right now?\n\nCheers,\n[Sender]",
        "cta_url": "https://yourdomain.com/clips/demo-42",
        "tracking_event": "demo_clip_clicked"
      }
    },
    {
      "email_2": {
        "subject": "Still thinking about that demo?",
        "send_delay_hours": 72,
        "body": "Hi [FirstName],\n\nIf you didn't catch the demo clip, here's the key insight: most teams are still doing this manually.\n\nWe automated it. 36-hour savings per team per week.\n\n[WATCH NOW]\n\nOr if you want a personalized walkthrough, let's chat:\n\n[SCHEDULE 15-MIN CALL]",
        "cta_url_primary": "https://yourdomain.com/clips/demo-42",
        "cta_url_secondary": "https://calendly.com/your-domain/15min"
      }
    }
  ]
}
```

### 4. Transcript & SEO Optimization
- Converts audio to searchable transcript (powered by AssemblyAI or Google Cloud Speech-to-Text)
- Extracts speaker quotes for attribution
- Suggests blog post outline with embedded clips
- Generates meta descriptions, schema markup, and internal linking recommendations
- Flags sections for repurposing as LinkedIn articles, Medium posts, or guides

### 5. Visual Asset Recommendations
- Suggests optimal thumbnail designs based on moments
- Recommends caption placement/styling for each clip
- Identifies speaker expressions/moments for hero images
- Generates frame-grab recommendations for social cards

---

## Configuration

### Environment Variables Required
```bash
# Speech-to-text & AI (pick one or use both)
OPENAI_API_KEY=sk-...                    # For GPT-4 analysis & hook generation
ASSEMBLY_AI_KEY=aai_...                  # For transcription (faster, cheaper)
GOOGLE_CLOUD_SPEECH_KEY=...              # Alternative transcription

# Video platform APIs
YOUTUBE_API_KEY=AIza...                  # For YouTube video ingestion
VIMEO_ACCESS_TOKEN=...                   # For Vimeo links

# Cloud storage (optional, for batch processing)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=webinar-archive

# Email platform integrations
HUBSPOT_API_KEY=...                      # For HubSpot email sequences
MARKETO_CLIENT_ID=...
MARKETO_CLIENT_SECRET=...

# Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Optional: WordPress/CMS
WORDPRESS_REST_TOKEN=...
WORDPRESS_SITE_URL=https://blog.yourcompany.com
```

### Skill Options
```json
{
  "transcription_service": "assembly_ai",  // or "google_cloud", "openai"
  "moment_detection_sensitivity": 0.75,    // 0.5-1.0 (higher = more moments)
  "email_platform": "hubspot",             // or "marketo", "convertkit"
  "social_platforms": ["linkedin", "twitter", "tiktok", "instagram"],
  "target_clip_duration_sec": 120,         // 30-180 seconds recommended
  "include_timestamps": true,
  "include_captions": true,
  "output_format": "json",                 // or "csv", "airtable"
  "slack_notifications": true
}
```

---

## Example Outputs

### Output 1: JSON Comprehensive Report
```json
{
  "webinar": {
    "title": "Advanced SaaS Sales Tactics",
    "duration_minutes": 45,
    "processed_at": "2025-01-15T14:32:00Z"
  },
  "summary": {
    "total_moments": 11,
    "total_clips": 11,
    "total_social_hooks": 44,
    "email_sequences": 5,
    "estimated_content_pieces": 52
  },
  "clips": [
    {
      "clip_id": "clip_001",
      "title": "The Discovery Call Framework",
      "timestamp": "05:12-08:47",
      "category": "demo",
      "transcript_excerpt": "The key to discovery is asking about...",
      "social_hooks": {
        "linkedin": "Most sales teams skip this critical step...",
        "twitter": "Discovery > Pitch. Here's why:",
        "tiktok_concept": "POV: Your sales calls actually convert"
      },
      "email_subject_line": "The discovery technique 450 reps use",
      "video_url_placeholder": "[CLIP WILL BE HERE]",
      "recommended_cta": "learn_more"
    }
  ],
  "email_sequences": [
    {
      "sequence_id": "seq_001",
      "name": "Framework-Driven Nurture",
      "target_segment": "free_tier_users",
      "email_count": 3,
      "first_email_subject": "The sales framework that's changing Q1 deals"
    }
  ],
  "blog_outline": {
    "title": "5 Advanced Sales Tactics from Our Q1 Webinar",
    "sections": [
      {
        "heading": "1. Master the Discovery Call",
        "clip_embedding": "clip_001",
        "key_takeaway": "..."
      }
    ]
  }
}
```

### Output 2: CSV Format (for spreadsheet workflows)
```
Clip_ID,Title,Timestamp,Duration_Sec,Category,LinkedIn_Hook,Twitter_Hook,Email_Subject,Recommended_CTA
clip_001,Discovery Framework,05:12-08:47,215,demo,"Most sales teams skip...",Discovery > Pitch,"Framework that's changing deals",learn_more
clip_002,Objection Handling,22:15-24:47,152,objection_handle,"The 'budget concern'...","How to handle budget pushback","Why budget concerns aren't real objections",schedule_demo
```

### Output 3: Slack Notification
```
🎬 Webinar Repurposing Complete!

📊 Results for "Advanced SaaS Sales Tactics":
   • 11 clips extracted
   • 44 social hooks generated
   • 5 email sequences created
   • ~52 total content pieces

🔥 Top Moment:
   "Discovery Call Framework" (05:12-08:47)
   Engagement Score: 9.4/10

📧 Email sequences ready in HubSpot
🐦 Twitter hooks preview: [LINK]
📰 Blog outline: [LINK]

Next: Schedule clip uploads & queue emails
```

---

## Tips & Best Practices

### 1. Pre-Webinar Setup
- **Title your webinar descriptively** — Include keywords for better SEO extraction
- **Enable Q&A capture** — The skill extracts objections from audience questions; make Q&A prominent
- **Plan speaker callouts** — Brief the presenter to highlight key moments; add visual cues (screen color changes, pauses)
- **Use slide decks** — Moments tied to visible slide changes get higher engagement scores

### 2. Optimize Clip Length
- **LinkedIn**: 60-120 seconds (premium content tolerance)
- **Twitter/X**: 15-30 seconds (retweet incentive)
- **TikTok**: 30-45 seconds (algorithm sweet spot)
- **YouTube Shorts**: 15-60 seconds (monetization threshold)
- **Instagram Reels**: 15-90 seconds

**Tip:** Let the skill auto-select durations, then customize for platform. A 108-second demo might be split into 2-3 clips (demo setup, execution, results).

### 3. Email Sequencing Best Practices
- **Send first email within 24 hours** — Maximize memory recall
- **Segment by engagement level** — Attended live vs. watched replay gets different copy
- **Use clip CTAs, not generic CTAs** —