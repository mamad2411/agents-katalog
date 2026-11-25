# High-Fidelity Generation Guidance

Use this reference only when creating or editing the target image. Do not use image generation for a direct-conversion request.

Before writing or sending any generation/edit prompt, complete the skill's mandatory official-character research gate. For a named or recognizable character, use web search and the saved `00_official_character_research.md` brief as the identity authority; keep verified facts separate from inference. For an original/non-character subject, record `official_character_research_status=not_applicable` instead of inventing official data. Never call image generation before this gate is complete.

## Text-only generation

Adapt this structure to the user’s subject and requested style:

```text
Use case: high-fidelity source image for a layered RYBW 3MF plaque.
Primary request: Create <subject and action> as a polished, detailed raster image.

Official-character research: Use the verified brief at `<official-character-research-file>` for canonical identity, appearance, costume, palette, props, and signature motifs. Do not copy logos, readable marks, slogans, or long source text.

Composition: Use one clearly readable subject on a square canvas. Unless requested otherwise, use a natural portrait or upper-body composition with a clean silhouette and enough margin for later square preparation. Do not include text, watermark, UI, frame, or extra characters.

Rendering: Preserve smooth curves, antialiasing, small identifying details, natural gradients, layered shading, material texture, and coherent high-resolution anatomy. Use the user’s requested photographic, illustrative, anime, painterly, or rendered style. Keep important features readable when the final object is approximately 65 mm wide.

Conversion awareness: Avoid extremely thin disconnected elements that will be fragile at print scale. Keep the subject/background separation visually clear when a transparent plaque is intended. Do not reduce the palette merely because the final print uses an RYBW LUT; Lumina will perform the color mapping.

Avoid: pixel art, visible logical grids, large uniform pixel blocks, nearest-neighbor enlargement, deliberately low resolution, jagged stair-step contours, text, watermark, duplicated features, malformed hands or face, and accidental background clutter.
```

## Reference-guided generation or editing

First inspect the uploaded image. Explicitly identify which properties the user wants transferred: identity, clothing, color palette, medium, pose, lighting, composition, mood, or another named trait.

Use this addendum:

```text
Use the supplied image as a reference for <requested properties>. Preserve those properties faithfully while producing the requested high-fidelity target. Use the verified official-character brief at `<official-character-research-file>` when the subject is a named or recognizable character. Do not copy unrelated defects, background clutter, text, watermark, crop, or pose unless the user asks for them. Keep smooth high-resolution rendering and do not pixelate the result.
```

For an explicitly requested local correction to a user-provided target, preserve all accepted geometry and change only the named defect. Do not use this for defects in a generated target; regenerate those from scratch instead:

```text
Edit the supplied target with the minimum possible change. Preserve the composition, crop, identity, face and body geometry, palette, lighting, texture, edges, background treatment, and resolution. Correct only <named defect>. Do not pixelate, simplify, or redesign unrelated regions.
```

## Direct conversion

Do not generate or edit. Preserve the uploaded file in `01_source.<ext>`, create a lossless working copy when possible, and proceed only with necessary background/canvas preparation.

## Acceptance

Reject and regenerate a generated target when it is visibly pixelated, unexpectedly low-resolution, contains accidental text/watermark, duplicates the subject, breaks requested identity or composition, or contains obvious generation artifacts. Do not use the failed generated target as an edit target or image reference. Do not reject a direct-conversion source for creative reasons; report limitations instead.
