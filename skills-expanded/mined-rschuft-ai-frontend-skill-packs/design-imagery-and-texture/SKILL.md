---
name: design-imagery-and-texture
description: "Improve web image and icon quality, scalable SVG/raster choices, photo crops, artwork consistency, textures and text-on-image legibility while respecting asset licenses and accessibility."
---

# Imagery and texture

## Scope

Use this specialist when the actual task involves imagery issues. Check documented brand/system decisions before prescribing changes. Do not conflate taste with accessibility standards or make assumptions from screenshots alone.

Affecting category: **imagery**. Related governing principles: contrast, unity. Route from `design-diagnose` or `design-review` when observations match this category, or load directly during a focused implementation.

## Procedure

- **fuzzy-icons**: Prefer licensed SVG for flat scalable artwork, responsive raster assets for photos; inspect aspect ratio. Verify: Icon silhouette stays crisp across DPR and controls retain accessible names.
- **mixed-art-direction**: Specify crop, light, saturation, illustration strokes and backgrounds as art-direction rules. Verify: Side-by-side media grid reads as a coherent set without reducing essential content variation.
- **text-on-photo**: Add stable text backing/scrim or relocate text; ensure contrast under worst crop and image load failure. Verify: Text passes WCAG on representative imagery/crops and remains legible during image loading.

Read `references/playbook.md` for exact discriminating checks, implementation examples, tradeoffs and acceptance tests. Keep the fix within the existing component architecture. Report original observation, selected recipe and evidence. For usability, engage `ux-*`; for normative accessibility, engage `wcag-*`.
