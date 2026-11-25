---
name: hyperframes-tactile-collage
description: Apply a brand-neutral Tactile Paper Collage style to a HyperFrames video using warm paper, cutout layers, ink marks, tape, stamps, notebook diagrams, editorial typography, and playful physical motion. Use when someone asks for a tactile paper collage edit, animated scrapbook, mixed-media notebook graphics, paper-cutout editorial styling, analog collage motion, or this visual treatment on talking-head footage or a full-frame HyperFrames composition.
---

# Tactile Paper Collage

Apply this skill as a visual companion after the owning HyperFrames workflow is known. Preserve the project's story, timing, footage, audio, claims, copy, and approved brand assets unless the user separately requests editorial changes.

## Load the contracts

1. Read `/hyperframes` first.
2. Read `/hyperframes-core` before editing composition HTML.
3. Read `/hyperframes-creative` for design-spec precedence.
4. Read `/hyperframes-animation` before authoring motion.
5. Read `/media-use` before changing footage, creating a subject cutout, or styling captions.

Resolve this skill's directory as `<skill-dir>`. Read:

- `references/style-system.md` for the visual tokens and component grammar.
- `references/scene-grammar.md` for translating narrative functions into collage scenes.
- `references/layering-safe-zones.md` for layout modes, subject layering, fallbacks, and platform safety.
- `references/motion-captions-audio.md` before implementing animation, captions, or sound.

## Apply the style

1. Resolve the HyperFrames composition directory. Read its brief, design spec, storyboard or motion board, transcript, composition files, and representative frames.
2. Inventory faces, gestures, logos, source UI, load-bearing text, approved brand colors, negative space, and existing media treatments.
3. Divide the story into beats with one dominant idea each. Record the chosen physical metaphor and layout mode for every beat.
4. Select the first viable mode:
   - `behind-subject`: place the photographic base below illustrated plates and a transparent subject above them.
   - `direct-overlay`: keep intact footage as the base and place bounded paper objects only in stable clear regions.
   - `full-frame`: hand a beat completely to the paper world when no useful footage or cutout exists.
5. Start from `assets/frame.md`. Copy it into the project as the active design specification, preserving an existing conflicting spec once as `frame.pre-tactile-paper-collage.md`. Merge approved identity assets and semantic brand colors; do not import source-project content.
6. Install the bundled fonts before rendering:

   ```bash
   node <skill-dir>/scripts/install-fonts.mjs <composition-dir>
   ```

7. Build static hero frames before motion. Use separate sub-compositions for coherent scenes and reserve the caption lane before placing decorative elements.
8. When captions are needed, copy `assets/components/tactile-caption.html` into the project's compositions directory and adapt its neutral word array. Temporarily copy and mount `assets/components/tactile-safe-zones.html` on the highest track while checking portrait collisions; remove or hide it before delivery. For other aspect ratios, update its internal dimensions and rectangles from `references/layering-safe-zones.md` before mounting.
9. Animate only after every paused hero frame reads clearly at phone size. Keep all render-critical behavior deterministic and seek-safe.
10. Run the project's current HyperFrames lint/check commands, create representative snapshots, and inspect the opening, every transition, the densest frame, and the final frame.

## Boundaries

- Do not replace the owning narrative workflow.
- Do not change cuts, narration, timing, facts, claims, or copy solely to fit the style.
- Do not require a transparent subject; use the documented overlay or full-frame fallback.
- Do not force the default palette over approved brand colors. Preserve the paper/ink contrast roles and remap accents semantically.
- Do not reproduce people, screenshots, transcripts, filenames, folder trees, palettes, or story concepts from any reference video.
- Do not use decorative clutter as a substitute for a clear metaphor.
- Do not use unseeded randomness, infinite loops, runtime clocks, or forward-only animation callbacks.
- Do not place critical content outside the destination platform's safe region.

## Bundled resources

- `assets/frame.md`: generic design-spec template.
- `assets/components/tactile-caption.html`: configurable transcript-timed caption treatment.
- `assets/components/tactile-safe-zones.html`: removable safe-zone overlay.
- `assets/fonts/*.woff2.b64`: encoded open-licensed Permanent Marker and Courier Prime fonts.
- `scripts/install-fonts.mjs`: decode and install the fonts into a composition.
- `scripts/validate-package.mjs`: validate structure, portability, licenses, and source isolation.

Run package validation after changing the skill:

```bash
node <skill-dir>/scripts/validate-package.mjs <skill-dir>
```
