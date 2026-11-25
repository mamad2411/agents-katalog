---
name: images-and-video-seo
description: Optimizes images and video for discovery and Search appearance. Use when media should appear in Google Images/Video surfaces or CLS is media-related.
---

# Images and Video SEO

## Overview

Make media crawlable, well-described, and stable in layout.

## When to Use

- Image/video indexing or appearance issues; missing media metadata

**Not for:** General article copy (pair with content skills).

## Official sources

- https://developers.google.com/search/docs/appearance/google-images
- https://developers.google.com/search/docs/appearance/video

## Process

1. Ensure media is reachable (not blocked) and referenced by crawlable URLs.
2. Provide descriptive filenames/alt for images; relevant titles/captions where helpful.
3. Set width/height (or reserve aspect-ratio) to reduce CLS.
4. For video, follow Video structured data / sitemap guidance when eligible.
5. Prefer modern formats thoughtfully; don’t hide critical text only in images.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Alt text is optional decoration." | Meaningful images need descriptive alt for accessibility and Images. |
| "Width/height are cosmetic." | Missing dimensions contribute to CLS. |
| "Text in images ranks the same." | Critical text should be real HTML when possible. |

## Red Flags

- Inventing ranking factors not documented by Google
- Skipping verification ("looks fine")
- Advising spammy shortcuts (cloaking, doorways, link schemes)

## Verification

- [ ] Alt/descriptive text present for meaningful images
- [ ] Dimensions reserved
- [ ] Video discovery method documented if video is primary content
