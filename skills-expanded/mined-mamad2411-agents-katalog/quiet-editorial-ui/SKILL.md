---
name: quiet-editorial-ui
description: Apply a brand-neutral Quiet Editorial UI edit style to an existing HyperFrames project. Use when someone asks to apply Quiet Editorial UI, use a quiet editorial editing style, add a refined editorial software look, restyle HyperFrames with serif-led editorial graphics, place elegant overlays in negative space or over footage, or use the same visual system for a full-frame graphic composition.
---

# Quiet Editorial UI

Apply this skill as a visual layer after the owning HyperFrames workflow is known. Preserve the project's story, timing, footage, audio, copy, and approved brand assets unless the user separately requests editorial changes.

## Load the contracts

1. Read `/hyperframes` first.
2. Read `/hyperframes-core` before editing composition HTML.
3. Read `/hyperframes-creative` for the project's design-spec precedence.
4. Read `/hyperframes-animation` before authoring motion.
5. Read `/media-use` caption guidance when captions are requested or already present.

Resolve this skill's directory as `<skill-dir>`. Read these references as needed:

- Visual tokens and component grammar: `references/style-system.md`
- Layout selection and project integration: `references/layout-modes.md`
- Caption construction: `references/captions.md`
- Platform safety and collision rules: `references/safe-zones.md`
- Motion vocabulary: `references/motion-language.md`
- Licensed Georgia setup: `references/font-setup.md`

## Apply the style

1. Resolve the HyperFrames composition directory. Read its brief, storyboard or motion board, design spec, transcript, composition files, and representative frames.
2. Inventory faces, logos, source UI, load-bearing source text, and useful negative space. Do not infer a talking-head layout from this style.
3. Select the first matching mode:
   - `available-area`: a stable unused region can hold the complete graphic idea.
   - `direct-overlay`: footage owns the frame and graphics must sit over it.
   - `full-frame`: no footage is present, or a beat intentionally gives graphics the whole frame.
4. Preserve an existing conflicting `frame.md` as `frame.pre-quiet-editorial-ui.md`, unless that exact backup already exists. Then copy `assets/frame.md` to the project as the effective `frame.md` and merge only approved logos, copy rules, and semantic brand colors into its `Approved Entities` section. Quiet Editorial UI owns typography, surfaces, spacing, hierarchy, captions, and motion.
5. Copy the bundled Inter files from `assets/fonts/` into the composition's `public/fonts/`. Do not copy or distribute Georgia. Require the user-supplied files described in `references/font-setup.md`.
6. Run the font preflight before any render-affecting command:

   ```bash
   node <skill-dir>/scripts/preflight.mjs <composition-dir>
   ```

   Stop if the preflight reports missing or invalid Georgia files. Do not silently substitute another serif.
7. Build the visual treatment with the selected layout mode. Keep one dominant idea per beat, use the token values exactly, and keep source content recognizable.
8. If captions are needed, copy `assets/components/quiet-editorial-caption.html` into the project and follow `references/captions.md`. If placement is uncertain, temporarily add `assets/components/quiet-editorial-safe-zones.html` as a top-track sub-composition; remove or hide it before delivery.
9. Validate with `npx hyperframes lint`, `npx hyperframes check`, and snapshots at representative beats. Inspect the result at phone scale as well as full resolution.

## Boundaries

- Do not choose or replace the owning narrative workflow.
- Do not change cuts, timing, audio, narration, claims, or copy solely to fit the style.
- Do not assume footage, a speaker, a fixed speaker size, or a fixed split-screen arrangement.
- Do not introduce product-specific names, logos, toggles, prompts, interface replicas, example files, or branded icons from any reference source.
- Do not use the success green as a general brand accent.
- Do not shrink captions below the documented floor to solve a collision; choose another safe lane.
- Do not render with a fallback display face when licensed Georgia is unavailable.

## Bundled assets

- `assets/frame.md`: effective project design specification.
- `assets/components/quiet-editorial-caption.html`: transcript-timed caption sub-composition.
- `assets/components/quiet-editorial-safe-zones.html`: removable safety overlay.
- `assets/examples/golden-frames.html`: neutral visual benchmark across three aspect ratios.
- `assets/fonts/Inter-400-latin.woff2` and `Inter-700-latin.woff2`: redistributable UI fonts.

Run package validation after changing the skill:

```bash
node <skill-dir>/scripts/validate-package.mjs <skill-dir>
```
