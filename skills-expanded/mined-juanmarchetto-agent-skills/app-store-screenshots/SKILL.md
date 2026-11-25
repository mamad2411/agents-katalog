---
name: app-store-screenshots
description: "Create App Store and Google Play screenshots with exact platform specs. Covers iOS/Android dimensions, gallery ordering, device mockups, captions, preview videos, localization, and A/B testing. Use when: app store screenshots, ASO, app preview, store listing, app mockup."
license: MIT
metadata:
  version: 1.0.0
  category: marketing
  tags: [app-store, google-play, screenshots, ASO, mockups, marketing, mobile]
---

# App Store Screenshots

Create app store screenshots and preview videos via [inference.sh](https://inference.sh) CLI.

## Quick Start

> Requires inference.sh CLI (`infsh`). Get installation instructions: `npx skills add inference-sh/skills@agent-tools`

```bash
infsh login

# Generate a device mockup scene
infsh app run falai/flux-dev-lora --input '{
  "prompt": "iPhone 15 Pro showing a clean modern app interface with analytics dashboard, floating at slight angle, soft gradient background, professional product photography, subtle shadow, marketing mockup style",
  "width": 1024,
  "height": 1536
}'
```


## Platform Specifications

### Apple App Store (iOS)

| Device | Dimensions (px) | Required |
|--------|-----------------|----------|
| iPhone 6.7" (15 Pro Max) | 1290 x 2796 | Required |
| iPhone 6.5" (11 Pro Max) | 1284 x 2778 | Required |
| iPhone 5.5" (8 Plus) | 1242 x 2208 | Optional |
| iPad Pro 12.9" (6th gen) | 2048 x 2732 | If iPad app |
| iPad Pro 11" | 1668 x 2388 | If iPad app |

- Up to **10 screenshots** per localization
- First **3 screenshots** are visible without scrolling (critical)
- Formats: PNG or JPEG (no alpha/transparency for JPEG)

### Google Play Store (Android)

| Spec | Value |
|------|-------|
| Min dimensions | 320 px (any side) |
| Max dimensions | 3840 px (any side) |
| Aspect ratio | 16:9 or 9:16 |
| Max screenshots | 8 per device type |
| Formats | PNG or JPEG (24-bit, no alpha) |

- Feature graphic: 1024 x 500 px (required for featuring)
- Promo video: YouTube URL (optional but recommended)

## The First 3 Rule

**80% of App Store impressions show only the first 3 screenshots** (before the user scrolls). These three must:

1. Communicate the core value proposition
2. Show the best feature/outcome
3. Differentiate from competitors

### Screenshot Gallery Order

| Position | Content | Purpose |
|----------|---------|---------|
| **1** | Hero -- core value, best feature | Stop the scroll, communicate what the app does |
| **2** | Key differentiator | What makes you unique vs competitors |
| **3** | Most popular feature | The thing users love most |
| **4** | Social proof or outcome | Ratings, results, testimonials |
| **5-8** | Additional features | Supporting features, settings, integrations |
| **9-10** | Edge cases | Specialized features for niche users |

## Screenshot Styles

### 1. Device Frame with Caption

The standard: device mockup showing the app, caption text above/below.

```
+----------------------------+
|   "Track Your Habits        |  <- Caption (benefit-focused)
|    Effortlessly"            |
|                             |
|   +--------------------+   |
|   |                    |   |
|   |   App Screen       |   |  <- Actual app UI in device frame
|   |   Content          |   |
|   |                    |   |
|   |                    |   |
|   +--------------------+   |
|                             |
+----------------------------+
```

### 2. Full-Bleed UI (No Device Frame)

The app UI fills the entire screenshot. Works for immersive apps.

### 3. Lifestyle Context

The device shown in a real-world context (person holding phone, on desk, etc.).

### 4. Feature Highlight with Callouts

UI screenshot with arrows/circles pointing to specific features.

## Caption Writing

### Rules

- **Max 2 lines** of text
- **Benefit-focused**, not feature-focused
- **30pt+ equivalent** font size (must be readable in store)

### Examples

```
Bad (feature-focused):
"Push Notification System"
"Calendar View with Filters"
"Data Export Functionality"

Good (benefit-focused):
"Never Miss a Deadline Again"
"See Your Week at a Glance"
"Share Reports in One Tap"
```

## Generating Screenshots

### Hero Screenshot (Position 1)

```bash
# Clean device mockup with hero feature
infsh app run falai/flux-dev-lora --input '{
  "prompt": "modern iPhone showing a beautiful fitness tracking app with activity rings and workout summary, device floating at slight angle against soft purple gradient background, professional product shot, clean minimal composition, subtle reflection",
  "width": 1024,
  "height": 1536
}'
```

### Feature Highlight

```bash
# Feature callout style
infsh app run bytedance/seedream-4-5 --input '{
  "prompt": "app store screenshot style, iPhone showing a messaging app with AI writing suggestions highlighted, clean white background, subtle UI callout arrows, professional marketing asset, modern design",
  "size": "2K"
}'
```

### Lifestyle Context

```bash
# Device in real-world setting
infsh app run falai/flux-dev-lora --input '{
  "prompt": "person holding iPhone showing a cooking recipe app, kitchen background with ingredients, warm natural lighting, over-the-shoulder perspective, lifestyle photography, authentic feeling",
  "width": 1024,
  "height": 1536
}'
```

### Before/After

```bash
# Split comparison
infsh app run infsh/stitch-images --input '{
  "images": ["before-screenshot.png", "after-screenshot.png"],
  "direction": "horizontal"
}'
```

## Preview Videos

### Apple App Store

| Spec | Value |
|------|-------|
| Duration | 15-30 seconds |
| Orientation | Portrait or landscape (match app) |
| Audio | Optional (loops silently in store) |
| Format | H.264, .mov or .mp4 |

### Google Play

| Spec | Value |
|------|-------|
| Source | YouTube URL |
| Duration | 30s-2min recommended |
| Orientation | Landscape preferred |

### Preview Video Structure

| Segment | Duration | Content |
|---------|----------|---------|
| Hook | 0-3s | Show the core outcome/wow moment |
| Feature 1 | 3-10s | Demonstrate top feature in action |
| Feature 2 | 10-18s | Second key feature |
| Feature 3 | 18-25s | Third feature or social proof |
| CTA | 25-30s | End screen with app icon |

```bash
# Generate preview video scenes
infsh app run google/veo-3-1-fast --input '{
  "prompt": "smooth screen recording style, finger tapping on a modern mobile app interface, swiping between screens showing charts and data visualizations, clean UI transitions, professional app demo"
}'
```

## Localization

Each language gets its own set of screenshots. Priorities:

| Market | Localization Level |
|--------|-------------------|
| Primary markets | Full: new screenshots + translated captions |
| Secondary markets | Translated captions, same screenshots |
| Other | English defaults |

Key localization markets: English, Japanese, Korean, Chinese (Simplified), German, French, Spanish, Portuguese (Brazilian)

## A/B Testing (Google Play)

Google Play Console supports store listing experiments:

- Test different screenshot orders
- Test with/without device frames
- Test different captions
- Test different color schemes
- Run for 7+ days with 50%+ traffic for significant results

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Settings screen as screenshot | Nobody cares about settings | Show core value, not infrastructure |
| Onboarding flow screenshots | Shows friction, not value | Show the app in-use state |
| Too much text | Unreadable in store | Max 2 lines, 30pt+ font |
| Wrong dimensions | Rejected by store | Use exact platform specs |
| All screenshots look the same | No reason to scroll | Vary composition and content |
| Feature-focused captions | Doesn't communicate benefit | "Never Miss a Deadline" > "Push Notifications" |
| Outdated UI | Looks abandoned | Update screenshots with each major release |
| No hero screenshot | Weak first impression | Position 1 = your best shot |

## Important

AI-generated images (via inference.sh) produce **marketing mockups**, not real app screenshots. For actual screenshots of your running app, use [maestro-mobile-testing](https://github.com/JuanMarchetto/maestro-mobile-testing) or [playwright-recording](https://github.com/JuanMarchetto/playwright-recording-skill) to capture real screens, then use this skill for framing, captions, and store optimization.

## Example Output

```
App Store Screenshot Set Generated:
- hero-iphone15pro.png (1290x2796) — "Track Your Habits Effortlessly"
- feature-calendar.png (1290x2796) — "See Your Week at a Glance"
- social-proof.png (1290x2796) — "Join 50,000+ Users"
- ipad-pro.png (2048x2732) — "Beautiful on Every Screen"
- feature-graphic.png (1024x500) — Google Play feature graphic
```

## Error Handling

- **Wrong dimensions**: Check platform specs table above — App Store and Play Store have different requirements
- **Store rejection**: Common causes: transparency in JPEG (use PNG), text too small (30pt+ minimum), screenshots show non-final UI
- **AI mockup looks generic**: Add specific details to the prompt (your app's actual color scheme, specific screen content, real feature names)

## Checklist

- [ ] Correct dimensions for target platform
- [ ] First 3 screenshots communicate core value
- [ ] Captions are benefit-focused, max 2 lines
- [ ] No onboarding or settings screens
- [ ] Preview video is 15-30s with hook in first 3s
- [ ] Localized for top markets
- [ ] Feature graphic (1024x500) for Google Play
- [ ] Screenshots updated for current app version
- [ ] A/B test variant prepared

## Related Skills

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@ai-video-generation
npx skills add inference-sh/skills@image-upscaling
npx skills add inference-sh/skills@prompt-engineering
```

Browse all apps: `infsh app list`
