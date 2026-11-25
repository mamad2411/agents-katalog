---
name: video-transcript-seo-optimized-blog-schema-markup-generator
description: "Convert YouTube/podcast transcripts into SEO-optimized blog posts with keyword density, H2/H3 structures, FAQ schema, and internal linking suggestions. Use when the user needs content repurposing, video SEO, or multi-format publishing."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "GOOGLE_SEARCH_API_KEY", "SEMRUSH_API_KEY"],
        "bins": ["node", "python3"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎬"
    }
  }
---

## Overview

**Video Transcript → SEO-Optimized Blog + Schema Markup Generator** transforms raw video transcripts (YouTube, podcasts, webinars, Zoom recordings) into publication-ready blog posts with enterprise-grade SEO optimization and structured data markup.

This skill automates the entire content repurposing workflow:
- **Transcript Processing**: Cleans, timestamps, and segments raw transcripts
- **Keyword Research Integration**: Analyzes search intent using Google Search Console + Semrush APIs
- **Content Structure**: Auto-generates hierarchical heading outlines (H1→H2→H3)
- **Schema Markup**: Injects VideoObject, FAQPage, and BreadcrumbList JSON-LD
- **Readability Optimization**: Flesch-Kincaid, Hemingway Editor integration, passive voice detection
- **On-Page SEO**: Keyword density analysis, meta description generation, alt-text suggestions
- **Internal Linking**: Recommends crosslinks to existing content (WordPress/Contentful API support)
- **Publishing**: Direct WordPress XML-RPC or Markdown export with frontmatter

**Why it matters**: Video content captures 1,200% more shares than text+images combined, but 95% of videos lack associated blog posts. This skill recovers SEO value trapped in video platforms by creating indexable, linkable content that drives 40%+ more organic traffic than video-only strategies.

**Integrations**: WordPress, Contentful, Slack notifications, Google Analytics 4, HubSpot CRM

---

## Quick Start

### Example 1: YouTube Video to Ranked Blog Post

```
Convert this YouTube transcript to a production-ready blog post:

Video: https://youtube.com/watch?v=dQw4w9WgXcQ
Title: "The Complete Guide to SEO in 2024"
Target Keywords: SEO tips, search engine optimization, ranking factors
Audience: Small business owners, SaaS founders
CMS: WordPress

Include:
- 2000-word blog post with keyword density 1-2%
- JSON-LD FAQ schema from transcript Q&As
- VideoObject schema for YouTube embed
- Internal links to these posts: /seo-tools, /technical-seo-audit
- Meta title, meta description, and OG tags
- Reading time estimate and outline

Publish directly to WordPress after validation.
```

### Example 2: Podcast Episode with Multi-Format Output

```
Process podcast transcript and create:

Transcript source: https://podcasts.example.com/episode-42.json
Topic: "Remote Work Productivity Hacks"
Tone: Conversational but professional
Output formats: Blog post, LinkedIn article, Twitter thread

Generate:
- Main blog post (1500 words, H2/H3 structure)
- 5 branded quote blocks for social media
- FAQ schema from listener questions
- Author bio schema and expertise markup
- Suggested internal links (auto-analyze existing blog via sitemap)
- Export as WordPress XML + Markdown + JSON

Readability target: Grade 8-10 (Flesch-Kincaid)
```

### Example 3: Webinar Recording with Lead Magnet Schema

```
Convert webinar transcript to gated content:

Video: Zoom recording (uploaded as .vtt transcript)
Title: "Advanced Analytics for E-Commerce"
Lead magnet: "Exclusive Webinar Slides PDF"
Audience: E-commerce managers, digital marketers

Create:
- Blog post with keyword optimization for: ecommerce analytics, tracking conversions
- HubSpot form schema (gated content with email capture)
- VideoObject schema pointing to embedded video player
- Structured data for Author (speaker credentials)
- FAQ schema from Q&A session
- Internal link suggestions from blog network analysis
- Slack notification with preview link + SEO score
```

---

## Capabilities

### 1. Intelligent Transcript Processing
- **Auto-Cleanup**: Removes filler words (um, uh, like), speaker labels, timestamps
- **Segment Recognition**: Identifies topic shifts, natural chapter breaks
- **Timestamp Preservation**: Optional linked timestamps for video chapters
- **Multi-Language**: Handles English (US/UK), Spanish, French, German transcripts
- **Confidence Scoring**: Flags low-confidence OCR/STT sections for manual review

**Usage Example**:
```
Process transcript with speaker identification:
- Remove: [CROSSTALK], [INAUDIBLE], filler words
- Preserve: Natural conversational tone
- Extract: Named entities (people, companies, products mentioned)
- Flag: Technical terms for glossary generation
```

### 2. Keyword Density & Search Intent Analysis
- **Keyword Research Integration**: Pulls data from Google Search Console + Semrush APIs
- **Density Analysis**: Calculates primary/secondary keyword density (targets 1-2% for primary)
- **LSI Keywords**: Auto-suggests semantically related long-tail keywords
- **Search Intent Matching**: Determines if content targets informational, navigational, or transactional queries
- **SERP Analysis**: Compares keyword difficulty, CPC, search volume
- **Keyword Placement**: Recommendations for H1, first 100 words, H2s, meta description

**Output Example**:
```json
{
  "primary_keyword": "SEO for beginners",
  "search_volume": 5400,
  "difficulty": 42,
  "density_current": 1.8,
  "density_target": 1.5,
  "placement_recommendations": {
    "h1": "SEO for Beginners: The Complete 2024 Guide",
    "first_100_words": "Include 'SEO for beginners' in opening paragraph",
    "h2_sections": 3,
    "meta_description": "Learn SEO for beginners with this comprehensive guide covering ranking factors, tools, and strategies..."
  },
  "lsi_keywords": ["beginner SEO tips", "basic search optimization", "how to start SEO"]
}
```

### 3. Content Structure & Outline Generation
- **H1-H3 Hierarchy**: Creates logical, nested heading structure from transcript flow
- **Section Detection**: AI identifies natural topic boundaries for H2 creation
- **Readability Segmentation**: Breaks long sections into scannable paragraphs (max 4 sentences)
- **Outline Preview**: Shows structure before writing for approval
- **Customizable Depth**: Generate 2-level or 4-level hierarchies based on content length

**Generates**:
```markdown
# Main Topic (H1)

## Key Concept 1 (H2)
### Sub-topic 1a (H3)
### Sub-topic 1b (H3)

## Key Concept 2 (H2)
### Sub-topic 2a (H3)

## FAQ Section (H2)
### Question 1? (H3)
### Question 2? (H3)
```

### 4. Schema Markup Auto-Generation
- **VideoObject Schema**: Embeds YouTube/self-hosted video with duration, thumbnail, description
- **FAQPage Schema**: Converts Q&A sections into structured data (increases featured snippet chance by 34%)
- **BreadcrumbList**: Suggests navigation hierarchy for WordPress categories
- **Author Schema**: Extracts speaker credentials, organization, image
- **OrganizationSchema**: Company details from transcript mentions
- **DateModified & DatePublished**: Auto-populated with timezone support

**Sample Output**:
```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "The Complete Guide to SEO in 2024",
  "description": "...",
  "thumbnailUrl": ["https://example.com/thumb.jpg"],
  "uploadDate": "2024-01-15T08:00:00Z",
  "duration": "PT42M30S",
  "embedUrl": "https://youtube.com/embed/dQw4w9WgXcQ",
  "videoQuality": "HD"
}
```

### 5. Readability & Tone Analysis
- **Flesch-Kincaid Grade Level**: Targets Grade 8-10 for general audiences
- **Passive Voice Detection**: Flags and suggests active voice rewrites
- **Sentence Length**: Identifies run-ons (avg 15-20 words recommended)
- **Paragraph Length**: Ensures short paragraphs (3-5 sentences max)
- **Hemingway Integration**: Real-time suggestions for clarity, adverb reduction
- **Tone Consistency**: Maintains voice throughout (conversational, professional, academic, etc.)

**Score Report**:
```
Readability Score: 78/100 ✓ Good
- Flesch-Kincaid: Grade 9 ✓
- Avg sentence length: 16 words ✓
- Passive voice: 12% (target <15%) ✓
- Paragraphs >150 words: 2 ⚠️ (consider breaking up)
- Transition phrases: 8 ✓
```

### 6. On-Page SEO Checklist Validation
Auto-validates before publishing:
- ✅ Meta title length (50-60 characters)
- ✅ Meta description (150-160 characters)
- ✅ Primary keyword in H1, first 100 words, H2s
- ✅ Images with alt-text and compressed <100KB
- ✅ Internal links (min 3-5 per 1000 words)
- ✅ External authoritative links (min 2-3)
- ✅ Schema markup (valid JSON-LD)
- ✅ Readability (Flesch-Kincaid Grade 6-12)
- ✅ URL slug (hyphenated, <50 characters)
- ✅ CTA clarity and placement

**Pre-Publish Validation**:
```
🔍 SEO Validation Report:
✅ Meta title: "SEO for Beginners: The Complete 2024 Guide" (54 chars)
✅ Meta description: "Learn SEO with this guide covering ranking factors..." (155 chars)
✅ Primary keyword density: 1.8% (target 1.5%) ⚠️ Slightly high
✅ H1 structure: 1 main H1 found
✅ H2 sections: 6 sections (optimal range)
✅ Internal links: 4 links detected
✅ External links: 3 authoritative sources
✅ Images: 5 images, all with alt-text
✅ Readability: Grade 9 (optimal)
❌ Mobile optimization: Test with Google Mobile-Friendly Test
🟡 Schema markup: VideoObject + FAQPage valid, BreadcrumbList missing

Status: READY TO PUBLISH (1 warning to address)
```

### 7. Internal Linking Intelligence
- **Sitemap Analysis**: Crawls WordPress/Contentful to find existing content
- **Semantic Matching**: Suggests links based on topic relevance (not just keyword matching)
- **Anchor Text Optimization**: Recommends natural, contextual anchor text
- **Link Placement**: Suggests optimal positions for internal links (2nd-3rd paragraph, conclusion)
- **Cannibalization Detection**: Warns if new post competes with existing content
- **Link Velocity**: Considers existing link structure to avoid over-optimization

**Suggestions**:
```
Suggested Internal Links:
1. "For advanced ranking factors, see our /technical-seo-audit guide"
   - Topic match: 94% | Anchor: "technical SEO guide"
2. "Our SEO tools roundup covers the best software for keyword research"
   - Topic match: 87% | Anchor: "SEO tools roundup"
3. "Learn more about on-page optimization in our dedicated post"
   - Topic match: 82% | Anchor: "on-page optimization"

Cannibalization Warning:
Your existing post "/SEO-basics-guide" covers similar content (74% overlap).
Recommendation: Merge posts or clarify target keyword differentiation.
```

### 8. Direct CMS Publishing
- **WordPress XML-RPC**: Direct publish with featured image, categories, tags
- **Markdown Export**: Frontmatter compatible with Hugo, Jekyll, Contentful
- **Slack Notifications**: Preview links, SEO scores, publishing confirmation
- **Scheduled Publishing**: Queue posts for future publication
- **Draft Saving**: Auto-save to WordPress drafts for manual review
- **Revision Tracking**: Version history with timestamp

---

## Configuration

### Required Environment Variables

```bash
# OpenAI for transcript processing and content generation
export OPENAI_API_KEY="sk-proj-xxxxx"

# Google Search Console for keyword research
export GOOGLE_SEARCH_API_KEY="AIzaSyxxxxx"

# Semrush for competitor analysis and keyword difficulty
export SEMRUSH_API_KEY="xxxxx"

# WordPress API (optional, for direct publishing)
export WORDPRESS_API_URL="https://yoursite.com/wp-json"
export WORDPRESS_API_USER="api_user"
export WORDPRESS_API_PASSWORD="application_password_xxxxx"

# Slack webhook (optional, for notifications)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/xxxxx"

# HubSpot (optional, for gated content + lead capture)
export HUBSPOT_API_KEY="pat-na1-xxxxx"
```

### Usage Configuration File

Create `config.json`:
```json
{
  "content_length": "1500-2000",
  "reading_level": "grade-9",
  "keyword_density": "1-2",
  "internal_links": 4,
  "schema_types": ["VideoObject", "FAQPage", "BreadcrumbList"],
  "output_formats": ["markdown", "html", "wordpress-xml"],
  "cms": "wordpress",
  "auto_publish": false,
  "slack_notifications": true,
  "image_optimization": {
    "format": "webp",
    "max_width": 1200,
    "compress": true
  }
}
```

---

## Example Outputs

### Output 1: Generated Blog Post (Markdown)

```markdown
---
title: "The Complete Guide to SEO in 2024: Ranking Factors, Tools & Strategies"
description: "Learn SEO with this comprehensive guide covering ranking factors, tools, and actionable strategies for beginners."
slug: "seo-complete-guide-2024"
author: "Alex Johnson"
date: "2024-01-15"
categories: ["SEO", "Digital Marketing"]
tags: ["seo-tips", "ranking-factors", "search-optimization"]
schema: {
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "The Complete Guide to SEO in 2024...",
  "image": "https://example.com/seo-guide-hero.png",
  "author": { "@type": "Person", "name": "Alex Johnson" },
  "datePublished": "2024-01-15T08:00:00Z"
}
---

# The Complete Guide to SEO in 2024: Ranking Factors, Tools & Strategies

## Overview

Search engine optimization (SEO) remains one of the most effective ways to drive organic traffic to your website. In this comprehensive guide, we'll explore the latest ranking factors, essential tools, and actionable strategies that will help you dominate search results in 2024.

*Reading time: 12 minutes | Last updated: January 15, 2024*

## How SEO Works: The Basics

SEO is fundamentally about helping search engines understand your content. Google's algorithm evaluates hundreds of ranking factors to determine which pages deserve top positions...

[Continues with full blog content structure]

---

## FAQ

### What Are The Most Important SEO Ranking Factors in 2024?

The top ranking factors include:
- Core Web Vitals (page speed, interactivity, visual stability)
- Mobile-friendliness and responsive design
- Content quality and E-E-A-T (Experience,