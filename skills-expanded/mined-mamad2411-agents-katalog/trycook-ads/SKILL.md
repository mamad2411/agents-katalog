---
name: trycook-ads
description: Create, analyze, and iterate on ad creatives using TryCook CLI ad builder tools. Use when asked to "create ad", "build ad creative", "analyze ad", "ad b-roll", "ad campaign", "video ad", "static ad", or any advertising creative production request.
allowed-tools:
  - Bash(trycook *)
  - Read
---

# TryCook Ad Builder

Create, analyze, and iterate on ad creatives via the TryCook CLI.

**Prerequisite:** Ensure `trycook status` shows authenticated before proceeding.

## Create an Ad

Start a new ad creative:

```bash
trycook tool info create_ad
trycook tool call create_ad '{"name": "Summer Sale Hero", "type": "static", "brief": "Eye-catching summer promotion for skincare line, 20% off, bright and clean aesthetic"}'
```

Types: `static` (image), `video` (motion creative).

## Analyze an Existing Ad

Upload or reference an ad for AI analysis:

```bash
trycook tool info analyze_ad
trycook tool call analyze_ad '{"url": "https://example.com/ad-creative.mp4"}'
```

Returns: hook strength, emotional triggers, CTA effectiveness, audience targeting signals, improvement suggestions.

## Generate B-Roll

Create supporting footage for video ads:

```bash
trycook tool info generate_broll
trycook tool call generate_broll '{"prompt": "close-up of woman applying face cream, soft morning light, slow motion", "duration": 5}'
```

## List & Manage Ads

```bash
# List all ads in workspace
trycook tool info list_ads
trycook tool call list_ads '{}'

# Get a specific ad
trycook tool info get_ad
trycook tool call get_ad '{"adId": "ad_abc123"}'

# Save/update an ad
trycook tool info save_ad
trycook tool call save_ad '{"adId": "ad_abc123", "name": "Summer Sale Hero v2"}'

# Cancel an in-progress ad generation
trycook tool info cancel_ad
trycook tool call cancel_ad '{"adId": "ad_abc123"}'
```

## Apply Ad Template

Apply a proven creative framework to your ad:

```bash
trycook tool info apply_ad
trycook tool call apply_ad '{"adId": "ad_abc123", "template": "problem-agitate-solve"}'
```

## Workflow: Full Ad Creative from Scratch

### 1. Research Phase

```bash
# Scrape competitor ads
trycook tool call foreplay '{"query": "skincare ads", "limit": 10}'

# Analyze a winning competitor ad
trycook tool call analyze_ad '{"url": "https://competitor-ad-url.mp4"}'
```

### 2. Asset Creation

```bash
# Hero image
trycook tool call generate_image '{"prompt": "product flat lay with summer botanicals, clean white background, studio lighting"}'

# B-roll clips (run multiple for variety)
trycook tool call generate_broll '{"prompt": "woman smiling at reflection, natural skin, warm sunlight", "duration": 4}'
trycook tool call generate_broll '{"prompt": "close-up serum drops falling into palm, macro shot", "duration": 3}'
```

### 3. Audio

```bash
# Voiceover
trycook tool call create_voiceover '{"text": "This summer, your skin deserves the best. 20% off our entire collection.", "voice": "alloy"}'

# Background music
trycook tool call generate_music '{"prompt": "upbeat positive summer vibes, acoustic guitar, light percussion", "duration": 15}'
```

### 4. Assembly

```bash
# Create the ad combining all assets
trycook tool call create_ad '{"name": "Summer Sale 2026", "type": "video", "brief": "Combine hero image, b-roll clips, voiceover, and music into a 15-second ad"}'
```

### 5. Analysis & Iteration

```bash
# Analyze the result
trycook tool call analyze_ad '{"adId": "ad_abc123"}'

# Iterate based on feedback
trycook tool call save_ad '{"adId": "ad_abc123", "brief": "Make the CTA more prominent, add urgency"}'
```

## Ad Types Reference

| Type | Use Case | Key Tools |
|-|-|-|
| Static | Feed ads, stories, display | `generate_image`, `create_ad` |
| Video | Reels, TikTok, YouTube | `generate_clip`, `generate_broll`, `create_voiceover`, `create_ad` |
| UGC-style | Testimonial, review | `create_avatar`, `create_voiceover`, `generate_broll` |

## Tips

- Always `analyze_ad` before and after iterations to measure improvement
- B-roll works best with specific, cinematic prompts (lighting, angle, motion)
- Generate 3-5 b-roll variants per scene — pick the best
- Use `foreplay` to study what's working in your niche before creating
