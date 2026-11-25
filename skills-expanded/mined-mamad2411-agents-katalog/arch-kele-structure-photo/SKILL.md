---
name: arch-kele-structure-photo
description: Transform one supplied photograph into two matching editorial structural-study images—one clean artwork without the source photo and one version with the unchanged source photo inset at the upper-right—while preserving recognizable geometry in an airy exploded or layered watercolor composition with warm paper, analytical construction lines, restrained labels, and a source-derived palette. Use when asked to turn a photo into a 结构图、解构图、爆炸图、建筑或物件结构分析海报、分层水彩示意图, or an exploded-view editorial illustration. Adapt the method to architecture, objects, people, animals, plants, interiors, streetscapes, and landscapes. Use bundled examples only when available and only for style calibration, never for subject matter or palette.
---

# Arch Kele Structure Photo

Create two finished variants from one supplied photograph. Treat that photograph as the sole content source. First create a clean structural-editorial artwork containing no source-photo inset. Then duplicate that exact artwork and add the unchanged source photograph as one small rectangular provenance inset at the upper-right. Deliver both variants.

## Workflow

1. Inspect the photograph. Identify the dominant subject, primary axis, camera viewpoint, foreground-to-background order, three to seven identity anchors, four to six source colors, and any people or objects that establish scale.
2. Select a truthful decomposition:
   - For architecture or assembled objects, separate real roofs, shells, floors, frames, modules, or nested parts along their natural axis.
   - For interiors, streets, and landscapes, separate foreground, middle ground, background, canopy, horizon, or enclosure as depth sheets rather than pretending they are mechanical parts.
   - For people, animals, or plants, use overlapping contour, gesture, surface, and color planes. Keep the body whole and dignified; never imply injury, amputation, or anatomical dissection.
3. Preserve the subject's silhouette, proportions, perspective, symmetry or asymmetry, orientation, material color roles, and decisive details. Simplify repeated ornament before altering structural facts.
4. Build two to five coherent strata with modest, regular gaps. Keep them on one shared axis or perspective grid so the viewer can mentally reassemble the subject. Leave one stable base or anchor region intact.
5. Compose a clean editorial plate, normally vertical 3:4. Center the main study, reserve generous warm-ivory paper around it, and keep the most detailed rendering in the lower or central anchor. Retain observed people as small scale figures when useful. Reserve the quiet upper-right corner for the source-photo inset; use another empty corner only when the upper-right would cover an identity anchor.
6. Combine three mark systems only: a faithful colored watercolor-and-ink subject rendering, pale source-derived watercolor blooms behind it, and fine graphite or ink analysis marks such as axes, arcs, dashed projections, alignment points, and a faint auxiliary elevation or contour.
7. Add a compact title only when it can be grounded in user-provided text or visible evidence. Use a neutral descriptive title when identification is uncertain. Keep all other text sparse; never invent dates, dimensions, provenance, technical specifications, logos, signatures, or factual labels.
8. Check whether the bundled example files listed in [references/example-selection.md](references/example-selection.md) are actually available. If they are available, classify the current photo by structural problem and inspect the single closest example. Use two examples only when the user explicitly requests a hybrid. Learn only the shared visual grammar; never copy an example's subject, palette, title, figures, layer count, or exact layout. If the files are absent or inaccessible, continue immediately with the written visual specification; do not stop, fail, or ask the user to supply an example.
9. Read [references/generation-prompt.md](references/generation-prompt.md), replace every bracketed field with observations from the current photo, and call image generation with the supplied photo as reference image 1. If a bundled example was successfully found, add it as the next style-only reference and state both roles explicitly. Otherwise, use only the supplied photo plus the complete written prompt. Ask the generator to leave the upper-right corner quiet, but do not ask it to render the inset.
10. Inspect the structural rendering. Regenerate if the subject is no longer recognizable, layers cannot be mentally reassembled, gaps are arbitrary, perspective drifts, people are malformed or duplicated, text is garbled, or the result looks like a photo collage, CAD render, generic infographic, or fantasy ruin.
11. Save the inspected generated plate as variant 1, the clean artwork. It must contain no original-photo rectangle, inset, thumbnail, collage fragment, or imitation of the source photograph.
12. Create variant 2 from the exact variant-1 file by running `scripts/add-source-inset.ps1` with variant 1 as `-BaseImage`, the exact user photograph as `-SourcePhoto`, and `-Corner TopRight`. Do not regenerate the artwork for variant 2. The script must preserve the source aspect ratio and add a straight-corner rectangular inset approximately 18% of the canvas width, with a thin warm-ivory mount and hairline neutral border.
13. Inspect both variants. They must be pixel-identical outside the inset area. In variant 2, ensure the inset contains the unchanged photograph, remains subordinate, and does not cover the title, subject, exploded layers, scale figures, or analytical marks. It must have no caption, shadow, rotation, rounded corners, or circular crop. Keep it at the upper-right; if essential content occupies that corner, regenerate the clean artwork with a quieter upper-right rather than moving the inset.
14. Verify the final pixel dimensions, not merely the visual orientation. Both variants must have identical dimensions and default to exactly 3:4 (`width / height = 0.75`). If image generation returns 2:3 or another ratio, extend the warm-paper canvas symmetrically to 3:4 before creating variant 2, without stretching or cropping the structural artwork. Reinspect both results before delivery.
15. Return both completed images in this order: (1) clean artwork without the source photo; (2) matching artwork with the unchanged source photo inset at the upper-right. Add no explanation unless the user asks for it.

## Guardrails

- Derive subject matter, palette, geometry, viewpoint, and scale cues only from the current photograph.
- Never consult or attach images from another skill. When this skill's bundled examples are available, use them for technique rather than content; when unavailable, rely on the written specification and continue normally.
- Preserve text already visible on the subject when it is an identity anchor, but do not create extra pseudo-writing across detailed surfaces.
- Keep technical marks subordinate to the subject. Avoid dense blueprint grids, HUD graphics, arrows everywhere, fake measurements, and diagram clutter.
- Use restrained paper texture and edge blooms; avoid sepia vintage distress, heavy stains, torn edges, tape, decorative frames, shadows, mockups, neon, gradients, glossy 3D rendering, or photomontage cutouts. The single thin rectangular source-photo mount is the only permitted frame.
- Variant 1 must contain zero source-photo insets. Variant 2 must contain exactly one unchanged source-photo inset at the upper-right. Never use a circle, oval, rounded rectangle, polaroid treatment, torn edge, or multiple thumbnails.
- Do not invent crowds, scenery, structural components, cultural symbols, or decorative motifs absent from the source.
- Prefer fewer, structurally meaningful layers over many dramatic fragments.
