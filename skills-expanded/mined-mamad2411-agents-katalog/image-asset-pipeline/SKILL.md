---
name: image-asset-pipeline
description: Manage Token Hold'em image asset generation, organization, manifests, naming, and UI integration. Use when Codex is asked to generate image assets, background assets, tavern or poker table art, candle/bar/bartender/chip/card assets, transparent PNGs, asset naming rules, asset manifests, or integrating generated images into the Token Hold'em UI.
---

# Image Asset Pipeline

## Core Rule

Design assets for the actual Token Hold'em UI composition. Inspect the current layout, viewport targets, layering, crop boxes, CSS dimensions, and interaction states before generating or integrating images. Avoid standalone art that looks good in isolation but fails in the interface.

## Workflow

1. Inspect the app first:
   - Find the UI entrypoints, asset directories, styling files, and any existing manifest or asset imports.
   - Identify where the image will render, its displayed size, aspect ratio, z-index/layer, darkening overlays, and nearby text or controls.
   - Capture or reason from the current viewport layout before writing prompts.

2. Create or update an asset manifest:
   - Prefer a structured file if the repo already has one, otherwise create a small manifest near the assets, such as `src/assets/manifest.ts`, `src/assets/assets.ts`, or `public/assets/manifest.json` depending on existing patterns.
   - Track each asset with `id`, `file`, `role`, `dimensions`, `format`, `alpha`, `anchor`, `safeArea`, `states`, `prompt`, `source`, and `qa`.
   - Keep manifest IDs stable even if filenames change.

3. Generate only assets with layout requirements:
   - Include exact canvas size, visible crop area, transparency requirements, lighting direction, camera angle, and how the asset sits behind or beside UI controls.
   - For layered props, generate transparent PNGs unless the visual is a full background.
   - Generate variants only when the UI needs states, breakpoints, or animation frames.

4. Organize and name files:
   - Store generated app art under the app's existing asset path. If none exists, use `public/assets/token-holdem/` for static references or `src/assets/token-holdem/` for imported build assets.
   - Use lowercase kebab-case names: `<surface>-<subject>-<variant>-<size>.<ext>`.
   - Include size for generated bitmaps: `tavern-bg-main-1920x1080.png`, `table-felt-top-1536x864.png`, `chip-dealer-button-idle-256.png`.
   - Use suffixes consistently: `idle`, `hover`, `active`, `disabled`, `mobile`, `desktop`, `dark`, `lit`, `frame-01`.

5. Integrate through the UI:
   - Use manifest imports or constants rather than scattering literal paths.
   - Set explicit CSS dimensions, aspect ratios, object-fit, object-position, and pointer-events behavior.
   - Preserve readable text contrast and tappable controls. Add overlays in CSS when needed instead of baking UI darkness into every image.

6. Verify before and after:
   - Before: screenshot or inspect the layout without the new art and record intended asset slots.
   - After: run the app, inspect desktop and mobile viewports, and verify no overlap, unwanted cropping, blurry scaling, blank assets, broken imports, or unreadable text.

## Asset Manifest Shape

Use this shape unless the project already has a stronger convention:

```ts
export type TokenHoldemAsset = {
  id: string;
  file: string;
  role: "background" | "table" | "prop" | "card" | "avatar" | "panel" | "badge";
  dimensions: { width: number; height: number };
  format: "png" | "webp" | "jpg" | "svg";
  alpha: boolean;
  anchor: "full-bleed" | "center" | "table-center" | "seat" | "hud" | "overlay";
  safeArea: string;
  states?: string[];
  prompt?: string;
  source?: string;
  qa?: string[];
};
```

Minimum manifest entry:

```ts
{
  id: "dealer-button-idle",
  file: "/assets/token-holdem/chip-dealer-button-idle-256.png",
  role: "prop",
  dimensions: { width: 256, height: 256 },
  format: "png",
  alpha: true,
  anchor: "table-center",
  safeArea: "Keep readable at 36-64 CSS px on top of the poker table.",
}
```

## Recommended Dimensions

- Tavern background: `1920x1080` or `2560x1440`, full-bleed, no alpha, important action kept away from the center table and HUD edges.
- Poker table: `1536x864` or `2048x1152`, transparent PNG if it floats over the tavern, otherwise no alpha if baked into the scene.
- Candles: `256x512` or `512x1024`, transparent PNG, flame separated from text-heavy areas.
- Bar or bartender: `1024x768` or `1536x1024`, transparent PNG if placed as a foreground/midground element, otherwise part of the tavern background.
- Dealer button chip: `256x256`, transparent PNG, readable at small sizes.
- Cards: `512x716` for individual card faces/backs, transparent only if the card silhouette is not rectangular; keep shared radius and border thickness.
- Player avatar portraits: `512x512` square portraits or `512x768` sprites, transparent PNG for sprites and framed portraits only if the UI frame supplies the mask.
- UI panels and action badges: generate as nine-slice-friendly or CSS-backed assets when possible; use `512x256`, `768x256`, or `1024x512` depending on target size.

## Prompt Templates

Use prompts that specify the UI slot and constraints.

Full background:

```text
Token Hold'em game background, cozy fantasy tavern poker room, camera slightly above table height, warm candle and hearth lighting, darker readable central area for a poker table and card UI, detailed bar in background but not distracting, no text, no logos, no playing cards in the background, 16:9 canvas, designed for full-bleed web game UI with safe margins at top and bottom.
```

Transparent prop:

```text
Single [asset subject] for Token Hold'em poker UI, isolated on transparent background, warm tavern candle lighting from upper left, 3/4 view matching table perspective, crisp silhouette, no cast shadow baked outside the object, no text unless explicitly requested, centered with 12% padding, PNG alpha.
```

Card or chip:

```text
[Card/chip subject] for Token Hold'em interface, readable at small web UI sizes, consistent rounded edges, warm tavern palette, top-down or slight 3/4 perspective matching poker table, centered, transparent background, no extra objects, no decorative text except [required label].
```

Avatar:

```text
Token Hold'em player avatar portrait, [character archetype], cozy tavern poker setting, readable face silhouette at 64px, warm rim light, neutral expression suitable for repeated gameplay, centered composition, no text, no cards covering the face, transparent background only if used as a sprite.
```

UI panel or badge:

```text
Token Hold'em [panel/action badge] UI asset, warm tavern poker theme, subtle wood/leather/brass material, designed to sit behind live text rendered by CSS, no baked words, clean inner safe area, transparent background, consistent edge treatment for repeated buttons and panels.
```

## Transparency Requirements

- Require PNG alpha for candles, chips, cards that are not full rectangular card images, avatars/sprites, table overlays, panels, and badges.
- Ask for transparent background explicitly and reject outputs with colored or checkerboard backgrounds baked in.
- Keep 8-12% transparent padding unless the UI needs edge-to-edge alignment.
- Avoid baked drop shadows when the asset may move over multiple surfaces; add shadows in CSS.
- Preserve premultiplied-alpha edges by visually checking against both light and dark backgrounds.

## Integration Checklist

- Add files in the chosen asset directory with kebab-case names and dimensions in filenames.
- Register each asset in the manifest with role, size, alpha, safe area, prompt, and QA notes.
- Wire UI imports through the manifest or a local asset module.
- Use responsive CSS constraints matching the intended slot, not raw bitmap dimensions.
- Set `alt=""` for decorative assets and meaningful alt text only for semantic images.
- Confirm transparent assets do not intercept clicks unless interactive.
- Keep UI text, cards, controls, pot amount, player stacks, and action buttons rendered by code, not baked into images.

## QA Checks

Before generation:
- Confirm target viewport sizes and breakpoints.
- Confirm the image slot aspect ratio and crop behavior.
- Confirm which UI elements must remain readable over or near the asset.
- Confirm whether the asset needs alpha, variants, hover/active states, or animation frames.

After generation:
- Inspect alpha on a checkerboard, dark background, and tavern background.
- Check image sharpness at actual rendered CSS size and at 2x density.
- Check visual continuity: lighting direction, perspective, card/table scale, and palette.
- Verify no baked words conflict with live UI labels.
- Verify crop safety in desktop and mobile screenshots.
- Verify file names, manifest entries, imports, and production build paths.

After integration:
- Run the app and capture desktop and mobile screenshots.
- Confirm assets load with no console 404s.
- Confirm no layout shift, text overlap, unreadable controls, or click-blocking layers.
- Compare before/after screenshots and revise prompts or CSS when the art fights the layout.
