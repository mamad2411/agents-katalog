---
name: taste-banners
description: Designs social covers, ad creatives, website heroes, email headers, Open Graph cards and print banners as export-ready HTML/SVG, always in three genuinely different art directions from one token set, with platform safe zones, crop tests and Playwright PNG export. Use for "banner", "OG image", "social cover", "LinkedIn/X/YouTube header", "Instagram post/story", "display ad", "hero image", "email header", "poster".
---

# Taste Banners: one message, three real directions

Reads `brand-guidelines.md` and `design-tokens.json` (run brand Light and tokens Minimal first if missing).

Platform sizes change. Use `references/sizes.md`, verify against the platform's current spec when web access exists, and say "unverified" otherwise.

## Procedure

1. **Brief** (6 lines, infer; ask max 2 questions): goal, platform(s), audience, the single message, one CTA, mandatory elements (logo, legal line, date, price).
2. **Three directions** from `references/directions.md`, each a different idea (not a recolor), with one line each for concept, hierarchy, color use and eye path.
3. **Compose** the largest size first using the rules below, then **reflow** (never scale) to other sizes.
4. **Build** one HTML file per direction x size: `banners/<campaign>-<direction>-<w>x<h>.html` plus `banners/index.html` preview grid.
5. **Check** safe zones, crop behaviour, contrast, file-size budget. **Export** PNG at 2x with `scripts/export-banners.mjs` where Node + Playwright exist.

## Composition rules

- Hierarchy: headline, then proof line or visual, then CTA, then logo. Max 3 text levels.
- Copy: headline at most 7 words (tiny formats 4); verb-led CTA of 2-3 words; formulas from taste-brand (PAS, BAB, 4U). Never invent statistics, testimonials or discounts (C03).
- Grid: margins at least 5% of the shorter side; align to a baseline; token spacing.
- Contrast: text 4.5:1 (3:1 for 24px+ bold); photos get a scrim (surface color at 60-80%) or a text panel.
- Type: brand fonts, 2 weights max, tighter tracking at display sizes, no text over busy image areas.
- Color: 60/30/10; the accent is for the CTA only. No default AI gradient (V01), blobs (V04) or glow (V09).
- Imagery: supplied, original or generated abstract/illustrative only; no identifiable people without rights; no third-party logos.
- Motion (HTML ads): max 15s or 3 loops, `prefers-reduced-motion` respected, final frame carries the whole message.
- Alt text for every exported image in the notes.

## Artboard pattern

```html
<section class="banner" style="width:1200px;height:630px" role="img" aria-label="<alt text>">
  <div class="bg"></div>
  <div class="content"><h1>...</h1><p>...</p><span class="cta">...</span></div>
  <svg class="logo" aria-hidden="true">...</svg>
</section>
```
Fixed pixel artboard for exact export; preview pages scale it with `transform: scale()` only.

## Quality gate

- [ ] One message, one CTA, headline within limit.
- [ ] Three distinct directions with rationale.
- [ ] Text inside safe zones; crop-tested per platform.
- [ ] Contrast verified; scrim on photos.
- [ ] Tokens only; no invented claims or third-party marks.
- [ ] Exact dimensions; within file-size budget; alt text written.
