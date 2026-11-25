---
name: og-image
description: Design Open Graph / social share images (1200x630) that render well in link previews - on-brand, legible, correctly exported. Use when a page or post needs a share/preview image.
---

# og-image

The image that represents a link everywhere it's shared. Small, legible, on-brand.

## Process
1. **Canvas 1200x630** (1.91:1). Keep key content centered - platforms crop edges differently.
2. **Hierarchy:** a short headline (large, legible), optional supporting line, logo, a simple background or
   hero. Don't cram - it renders small.
3. **Build** via Canva (branded) or `image-generate` for the background, then place text.
4. **Contrast:** text must pass over the background (the `contrast-guard` hook) - add a scrim if needed.
5. **Export** optimized PNG/JPG (< ~1MB), absolute-URL ready; name kebab-case.

## Output
- The OG image (confirmed from the connector) + the exact dimensions and the optimized file, ready to wire to `og:image`.

## Guardrails
- Legible at small size; safe margins; on-brand. Optimized weight.
- Verify it actually renders in a preview tester before claiming done; confirm connector output is real.
