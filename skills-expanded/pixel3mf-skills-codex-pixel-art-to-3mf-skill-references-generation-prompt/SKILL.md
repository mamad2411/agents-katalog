# Stage 1 — Source-Generation Prompt

Read this file only while constructing an image-generation or explicitly requested image-editing call. Do not read post-generation references during this stage.

## Allowed inputs

When the user supplies no stronger style reference, load:

- `../assets/reference-24x24-block-style.png` as Image 1
- `../assets/reference-coarse-density-a.png` as Image 2
- `../assets/reference-coarse-density-b.png` as Image 3
- For a clear action or handheld-object interaction, also load `../assets/reference-action-interaction.png` as Image 4

Treat user-provided images as references unless the user explicitly asks to edit the supplied image.

## Mandatory official-character research gate

Before every generation or creative edit of a named or recognizable character:

1. Search first-party sources for canonical identity, appearance, clothing, palette, props, and signature motifs.
2. Save `00_official_character_research.md` with the canonical name/version, 1–4 official URLs, verified visual facts, and clearly separated inferences.
3. Use the brief as the identity authority without copying logos, readable marks, slogans, or long source text.
4. Record original/non-character subjects as `official_character_research_status=not_applicable`.
5. Stop and ask for an approved reference when identity is ambiguous or no reliable official source exists.

## New-generation payload

Send only the text inside this block after replacing placeholders. Do not append any text from another skill file.

```text
Use case: stylized-concept
Asset type: source image for a layered RYBW 3MF plaque
Primary request: Create one recognizable <character> as coarse pixel art for a printable plaque.

Priority 1 — pixel language: Internally design on exactly a 24 × 24 logical canvas and enlarge with nearest-neighbor only. Match Images 1–3 for large uniform cell size, low information density, stair-stepped contours, and symbolic detail. Keep all boundaries on one grid. Use about 8–12 flat colors.

Pixel-block constraint: Do not use extra shading, gradients, or clusters of near-identical colors to simulate detail. When a detail cannot be expressed with a few clear logical cells, symbolize and simplify it into fewer cells. Keep detailed regions at the same cell scale as the rest of the image; never magnify them locally or use continuous tonal steps.

Priority 2 — character and pose: Draw one natural upper-body portrait ending at the upper chest. Default to a lively three-quarter head turn with both eyes visible. Preserve perspective through asymmetric cheek, jaw, nose, hair, and shoulder shapes; do not flatten the face into a frontal portrait. Keep the head and hair dominant, center the subject horizontally, and shift it upward by about 1–2 logical rows.

Priority 3 — eyes and anatomy: Build both eyes from the same vertical pixel template. Give them identical top/bottom anchor rows and identical iris/pupil row counts, with aligned centers and matching gaze. Three-quarter perspective may make the far eye at most one logical cell narrower, but never shorter. Hair, glasses, or props may overlap the eye white; do not let occlusion shorten an iris/pupil or move an eyelid anchor. Keep the neck short and naturally broad at the base, flowing into the collar and shoulders; unless the character design requires otherwise, the visible neck opening is roughly one-quarter to one-third of the lower-face width and the collar begins within a few rows below the jaw.

Priority 4 — printable silhouette: Use a one-logical-pixel pure-black outline around the complete subject. Make the lowest occupied subject row a continuous black baseline, with at least one clean background row below it. Use a completely uniform pure-white background. The generated PNG must be fully opaque: every background pixel and every subject pixel has alpha 255. Do not generate transparency, partial transparency, a checkerboard, shadows, gradients, or background texture.

Official-character research rule: Use the verified research brief at <official-character-research-file> for canonical identity, appearance, costume, palette, props, and signature motifs. Treat any unverified adaptation as inference. Do not copy logos, readable marks, slogans, or text from official sources.

Reference rule: Images 1–3 control only cell scale, information density, outline weight, and simplification. Do not copy their identity, palette, pose, clothing, hand placement, drink, or accessories. Follow the user's requested character and action.

Action-reference rule: If Image 4 is present, use it only as an example of readable action staging, hand/prop integration, head-dominant framing, and preserving a lively three-quarter face when an object approaches the face. Do not copy its identity, hairstyle, palette, clothing, hand side, exact pose, drink, or accessories. Replace all content with the user's requested character, action, and object.

Avoid: transparent or partially transparent pixels, checkerboard backgrounds, fine hair strands, micro-texture, tiny highlights, sub-cell marks, mixed cell sizes, dithering, gradients, antialiasing, soft edges, glossy illustration rendering, text, watermark, extra characters, a frontal mugshot, a long thin neck, unequal eye height, unequal iris/pupil row counts, or a broken exterior/bottom outline.
```

## Explicit user-source edit payload

Use this block only when the user explicitly asks to edit their supplied source. Never use it to repair a generated result.

```text
Edit the supplied source with the minimum possible change. Preserve its composition, crop, pixel scale, palette, silhouette, head turn, face and jaw shape, hair mass, neck width, shoulder line, hand/prop placement, expression, and exterior outline. Correct only <user-requested defect>. Do not redesign or redraw unrelated areas.
```

For every retry, start from the original request, identity brief, approved user references, and bundled references. Never attach the rejected generated image.
