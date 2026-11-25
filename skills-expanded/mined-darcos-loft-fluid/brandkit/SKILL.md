---
name: brandkit
description: Generate premium brand reference images for a design system, covering logo concepts, color and type boards, and product mockups. Use when a brief needs visual references or a brand kit before or alongside building the UI. Tool-agnostic (works with Nano Banana / Gemini, Higgsfield, Midjourney, or any image model).
license: MIT
---

# Brandkit

Premium reference imagery for a brand: the visual north-star before code. Works with any image model. Pairs with the `design-system` skill, which provides the palette and type; this renders them.

## What it produces
- **Logo concepts**: a mark and a wordmark, on the brand palette.
- **A brand board**: palette swatches, type specimens, the mood in one frame.
- **Product mockups**: the site or app in context, premium product-photography style.
- **Optional hero**: an "open and reveal" sequence (below).

## Prompt formula (premium product photography)
```
[Subject + material and finish], centered in frame, 3/4 front angle.
Clean [brand background hex] background, soft studio lighting, subtle shadows.
[Detail specific to the brand]. Photorealistic, 16:9, catalog quality,
Apple-style product photography. No text, no logos, no other objects in frame.
```

## The "open and reveal" hero (two-image to video)
A signature, attention-grabbing hero: an intact object that opens and whose contents spill out.
1. **Image A, closed**: the object intact and clean.
2. **Image B, open**: the same object, opened, contents floating around it. Golden rule: identical subject, angle, light, and background, only the state changes, or the animation will jump.
3. **Animate A to B** with an image-to-video model (Higgsfield, Kling, Veo): set A as the start frame, B as the end frame, plus a motion prompt describing the opening. Fallback: animate image B alone with a floating motion.

## Rules
- The brand palette and type come from the `design-system`, not invented here. Render the system, do not redesign it.
- Real material, premium light, no clutter. Generated does not mean cheap.
- One consistent style across the whole kit.
- Remove any model watermark before use (crop or a clean export).

Pairs with: `design-system` (the identity this renders).
