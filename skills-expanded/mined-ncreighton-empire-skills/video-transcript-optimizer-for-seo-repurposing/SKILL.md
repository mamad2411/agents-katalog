---
name: video-transcript-optimizer-for-seo-repurposing
description: "Auto-extract SEO descriptions, chapters, social clips, blog outlines & quote graphics from raw video transcripts. Use when the user needs content repurposing, multi-format distribution, or timestamp-based editing for video content."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_CLOUD_API_KEY"],
        "bins": ["ffmpeg"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎬"
    }
  }
---

## Overview

**Video Transcript Optimizer for SEO & Repurposing** transforms raw video transcripts into a complete suite of repurposed content assets in minutes. This skill solves the creator's dilemma: "I have 50 hours of video content but can't efficiently distribute it across blogs, social media, email, and search engines."

The skill intelligently extracts:
- **SEO-optimized video descriptions** (YouTube, Vimeo, WordPress)
- **Chapter timestamps** with auto-generated summaries
- **Social media clips** with burned-in captions (TikTok, Instagram Reels, YouTube Shorts format)
- **Blog post outlines** with H2/H3 structure ready for expansion
- **Quotable moments** formatted as shareable graphics
- **Speaker identification & attribution** for multi-speaker content
- **Multi-language support** (transcription and translation)

**Why it matters:** Content creators and agencies spend 15+ hours manually repurposing a single hour of video. This skill cuts that to 5 minutes per video, multiplying content ROI across WordPress blogs, LinkedIn, Twitter/X, email newsletters, and YouTube channels.

**Integration ecosystem:** Works with YouTube Data API, Google Cloud Speech-to-Text, OpenAI GPT-4, WordPress REST API, Slack webhooks, and standard video formats.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Basic Transcript Processing
```
Process this video transcript for repurposing:

[00:00] Host: "Today we're talking about AI in marketing."
[00:15] Guest: "AI is transforming how we work..."
[00:45] Host: "What's the biggest challenge?"
[01:20] Guest: "Finding quality training data..."
[02:10] Host: "Any recommendations?"
[02:35] Guest: "Start with open-source models..."
[03:00] Host: "Thanks for being here."

Extract: SEO description, 3 chapter breaks, 2 pull quotes, and a blog outline.
```

### Example 2: Multi-Language Content
```
I have a Spanish-language webinar transcript (45 minutes). 
- Extract SEO description in Spanish AND English
- Identify speaker names automatically
- Create 4 social clips (Instagram Reels format: 9:16 vertical)
- Generate blog outline in both languages
- Find top 3 quotable moments
```

### Example 3: Timestamped Editing with Segments
```
My transcript has speaker labels [SPEAKER: Name]. 
Extract only segments from "Product Manager" speaker.
Create a 5-minute highlight reel outline with timestamps.
Format for YouTube Shorts (auto-add captions).
Generate LinkedIn post from these highlights.
```

### Example 4: Batch Processing with Metadata
```
I have 10 podcast transcripts (CSVs with columns: Title, Transcript, Duration, Guest).
For each:
- Generate YouTube SEO description (160 chars)
- Extract top 2 quotable moments as image templates
- Create chapter markers (target 5-7 chapters)
- Output as WordPress blog outline
- Save metadata to JSON for bulk upload
```

---

## Capabilities

### 1. SEO Description Generation
Automatically crafts YouTube, Vimeo, and WordPress-optimized descriptions (160-500 characters) that:
- Include primary keyword in first sentence
- Incorporate 3-5 long-tail keywords naturally
- Add CTA (link to blog, signup, product)
- Include timestamp chapters for accessibility
- Follow YouTube's best practices for discoverability

**Example output:**
```
Learn how AI transforms marketing strategy without coding. 
Guest expert shares proven frameworks for automating campaigns, 
finding training data, and scaling with open-source models. 
Perfect for marketers, product managers, and startup founders. 
[00:00 Intro] [00:45 AI Challenges] [02:35 Recommendations]
→ Read full guide: [link]
```

### 2. Intelligent Chapter Extraction
Analyzes transcript content to identify natural breakpoints and creates:
- Auto-generated chapter titles (3-8 per hour of video)
- Precise timestamp markers (within 5-10 seconds)
- Chapter summaries (1-2 sentences each)
- SEO-friendly slug format for YouTube chapters

**Usage:**
```
Extract chapters from this 28-minute sales webinar transcript.
Target: 6-8 chapters, each 3-5 minutes long.
Naming convention: "Section: Specific Topic"
Include chapter descriptions for YouTube SEO.
```

### 3. Social Media Clip Generation
Extracts and formats video clips for platform-specific distributions:
- **TikTok/Reels:** 9:16 vertical format, auto-caption placement
- **YouTube Shorts:** 1080×1920, burn-in captions
- **Twitter/X:** Tweet-sized quotes (280 chars) with video timestamp
- **LinkedIn:** Professional clips with context headers
- Outputs as timestamp ranges + caption JSON for automated video editing

**Example:**
```
{
  "clips": [
    {
      "start": "00:45",
      "end": "01:20",
      "platform": "reels",
      "caption": "AI isn't replacing marketers. It's replacing marketers who don't learn AI.",
      "cta": "Watch the full interview →"
    }
  ]
}
```

### 4. Blog Post Outline Generation
Transforms transcripts into WordPress-ready blog structures:
- H2 headers from chapter breaks
- H3 subheadings from key discussion points
- Suggested image breakpoints (every 2-3 min of video)
- Internal linking recommendations
- Meta description suggestions
- Estimated read time and word count targets

**Output format:** Markdown or WordPress XML ready for bulk import

### 5. Quote Graphics & Pullquote Extraction
Identifies memorable, shareable moments and outputs:
- Top 5-10 quotable moments ranked by engagement potential
- Text formatting with speaker attribution
- Suggested visual templates (Canva-compatible JSON)
- Image dimensions for Instagram (1080×1350), Pinterest (1000×1500), Twitter (1200×628)
- Hashtag recommendations per quote

### 6. Speaker Identification & Attribution
- Auto-detects speaker names from labeled transcripts
- Resolves speaker consistency (handles "the host" → "John Smith")
- Extracts speaker bios/roles from context
- Generates speaker cards for blog headers
- Creates podcast guest profiles for WordPress custom post types

### 7. Multi-Language Support
- **Transcription:** Converts audio transcripts into Spanish, French, German, Mandarin, Japanese
- **Automatic translation:** Creates parallel transcripts and bilingual SEO descriptions
- **Cultural adaptation:** Adjusts tone and references for target markets
- **Subtitle generation:** SRT/VTT format for captions in multiple languages

---

## Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-... # GPT-4 for intelligent extraction
GOOGLE_CLOUD_API_KEY=... # Speech-to-Text & Translation API

# Optional
WORDPRESS_REST_URL=https://yourblog.com/wp-json/wp/v2
WORDPRESS_REST_USER=...
WORDPRESS_REST_PASS=...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### Configuration Options
```json
{
  "extraction": {
    "targetChapters": 6,
    "minChapterDuration": 180,
    "includeTimestamps": true,
    "speakerLabeling": true
  },
  "seo": {
    "keywordDensity": "1-2%",
    "descriptionLength": 160,
    "includeCTA": true
  },
  "socialClips": {
    "formats": ["reels", "shorts", "tiktok"],
    "captionBurnIn": true,
    "minimumClipLength": 15
  },
  "languages": ["en", "es", "fr"],
  "output": {
    "format": "json",
    "includeImages": true,
    "wordpressExport": true
  }
}
```

### Setup Instructions
1. **Obtain API keys:**
   - OpenAI: https://platform.openai.com/api-keys
   - Google Cloud: https://console.cloud.google.com

2. **Install dependencies:**
   ```bash
   pip install openai google-cloud-speech google-cloud-translate
   ```

3. **Configure environment:**
   ```bash
   export OPENAI_API_KEY="your-key"
   export GOOGLE_CLOUD_API_KEY="your-key"
   ```

4. **Test the skill:**
   ```bash
   openclaw run video-transcript-optimizer-for-seo-repurposing \
     --input "sample-transcript.txt" \
     --config config.json
   ```

---

## Example Outputs

### Sample 1: Complete Repurposing Package
**Input:** 32-minute product launch webinar transcript

**Outputs generated:**

```
📄 OUTPUTS/
├── youtube_description.txt
│   "Discover how our new AI platform transforms customer support. 
│    Watch Co-founder Sarah explain the 3-part framework, live demos, 
│    and roadmap. [00:00 Intro] [05:20 The Problem] [12:45 Demo] 
│    [24:10 Pricing & Roadmap] [30:00 Q&A]"
│
├── chapters.json
│   {
│     "chapters": [
│       {"start": "00:00", "title": "Introduction", "description": "Welcome & agenda"},
│       {"start": "05:20", "title": "Problem Statement", "description": "Why legacy systems fail"},
│       {"start": "12:45", "title": "Live Product Demo", "description": "End-to-end walkthrough"},
│       {"start": "24:10", "title": "Pricing & Roadmap", "description": "Plans and 2024 features"}
│     ]
│   }
│
├── social_clips.json
│   {
│     "clips": [
│       {
│         "title": "The Biggest Mistake",
│         "start": "07:15", "end": "08:45",
│         "platforms": ["reels", "shorts", "tiktok"],
│         "caption": "90% of teams are still using spreadsheets for customer support. It's costing them $200K+ annually.",
│         "imageTemplate": "quote-dark-blue"
│       },
│       {
│         "title": "Live Demo Moment",
│         "start": "14:30", "end": "16:50",
│         "platforms": ["youtube", "linkedin"],
│         "caption": "Watch the AI respond to 50 support tickets in seconds",
│         "cta": "See demo →"
│       }
│     ]
│   }
│
├── blog_outline.md
│   # How Our AI Platform Transforms Customer Support
│   ## The Problem: Legacy Systems Are Broken
│   ### Why Spreadsheets Don't Scale
│   ### Real Cost of Manual Support
│   ## The Solution: AI-Powered Triage
│   ### Intelligent Ticket Routing
│   ### Automated Response Generation
│   ## Live Demo: See It In Action
│   ## Pricing & Roadmap
│   ### 3-Tier Pricing Model
│   ### 2024 Feature Roadmap
│   ## Getting Started
│
├── quotes.json
│   {
│     "quotes": [
│       {
│         "text": "90% of teams are still using spreadsheets for customer support.",
│         "speaker": "Sarah Chen",
│         "timestamp": "07:20",
│         "engagement_score": 0.94,
│         "platforms": ["linkedin", "twitter", "pinterest"],
│         "imageTemplates": ["minimal-light", "bold-dark", "gradient-modern"]
│       },
│       {
│         "text": "We've reduced response time from 24 hours to 2 minutes.",
│         "speaker": "Sarah Chen",
│         "timestamp": "25:45",
│         "engagement_score": 0.89,
│         "platforms": ["all"]
│       }
│     ]
│   }
│
└── wordpress_import.xml
    <item>
      <title>How Our AI Platform Transforms Customer Support</title>
      <description>Learn the 3-part framework...</description>
      <content:encoded><![CDATA[
        <h2>The Problem: Legacy Systems Are Broken</h2>
        <p>[Embed video with timestamp: 5:20]</p>
        <p>90% of teams are still using spreadsheets...</p>
      ]]></content:encoded>
    </item>
```

### Sample 2: Multi-Language Output
**Input:** Spanish webinar transcript (45 min)

```json
{
  "en": {
    "seoDescription": "Learn advanced SEO strategies from industry expert...",
    "chapters": [...],
    "blogOutline": "..."
  },
  "es": {
    "seoDescription": "Aprende estrategias de SEO avanzadas del experto...",
    "chapters": [...],
    "blogOutline": "..."
  },
  "socialClips": {
    "clips": [
      {
        "caption_en": "The #1 SEO mistake most teams make...",
        "caption_es": "El error #1 de SEO que cometen la mayoría...",
        "timestamp": "12:45-14:20"
      }
    ]
  }
}
```

---

## Tips & Best Practices

### 1. Transcript Quality = Output Quality
- **Best:** Professional transcription with speaker labels, minimal errors
- **Good:** Automated captions with 95%+ accuracy
- **Acceptable:** Raw transcripts with 5-10% errors (skill corrects common terms)
- **Poor:** Highly corrupted or low-quality audio transcripts

**Pro tip:** Use Otter.ai, Rev, or Google Cloud Speech-to-Text for best results before importing.

### 2. Optimize Chapter Structure
- Aim for **5-8 chapters per hour** of video content
- Use **semantic breaks** (topic changes) rather than time intervals
- Name chapters with **action words:** "Discover," "Learn," "Master," "Avoid"
- Keep chapters **3-5 minutes** for YouTube Shorts repurposing

### 3. Leverage Speaker Labels for Authority
- Always include **speaker names** and titles in transcript
- Format: `[SPEAKER: John Smith, CEO]` or `[HOST:]` / `[GUEST:]`
- Enables automatic speaker cards, LinkedIn attributions, and podcast guest profiles
- Improves engagement metrics when audiences know who's speaking

### 4. Plan Social Clip Strategy
- Extract **2-3 clips per 10 minutes** of video for maximum coverage
- Prioritize **contrarian takes**, **data points**, and **tips** for high engagement
- Use clips to drive traffic back to **long-form content** (blog, YouTube)
- Schedule clips across **3-7 days** to maximize reach without saturation

### 5. SEO-First Blog Outlines
- Extract outline **before** writing blog post
- Use generated **H2/H3 structure** as skeleton, add 30-50% new content
- Include **video embeds at chapter breaks** for dwell time and backlinks
- Add **internal links** to related posts (suggested by skill)

### 6. Multi-Language = Expanded Reach
- Translate to **2-3 high-value languages** based on audience (Spanish, Portuguese, French most ROI)
- Use **bilingual SEO descriptions** to rank in both language searches
- Schedule translated content with **2-week stagger** to avoid cannibalization

### 7. Automate Downstream Publishing
- Export WordPress XML directly to **bulk upload** 10+ blog posts weekly
- Use **Zapier/Make integration** with