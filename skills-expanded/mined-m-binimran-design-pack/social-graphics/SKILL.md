---
name: social-graphics
description: Produce a set of platform-sized social/marketing graphics (correct dimensions, safe areas, on-brand) via Canva or image generation. Use for campaign posts, stories, ads, and banners.
---

# social-graphics

One concept, correctly sized for every platform, on-brand.

## Platform sizes (verify current specs)
- Instagram post 1080x1080 / portrait 1080x1350; Story/Reel 1080x1920.
- Facebook/LinkedIn shared ~1200x630; X ~1600x900.
- YouTube thumbnail 1280x720; cover/banner per platform.
Keep text inside safe areas; mind platform UI overlap on stories.

## Process
1. **One strong concept** (headline, hero visual, CTA) from the brand kit.
2. **Generate/lay out** via Canva (branded) or `image-generate` for custom hero art.
3. **Resize** to each platform - reflow, don't just crop; keep hierarchy and safe areas.
4. **Check contrast** of text over imagery (the `contrast-guard` hook + `accessibility-contrast`).
5. **Export + name** per platform (hand to `asset-export`); note licensing.

## Output
- The graphic set (one per platform, confirmed from the connector), with sizes + the brief + licensing notes.

## Guardrails
- On-brand colours/type/logo; text legible over imagery (contrast).
- Fair platform ad rules; record stock/AI licensing. Confirm connector output is real.
