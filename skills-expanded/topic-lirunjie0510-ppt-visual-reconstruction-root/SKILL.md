---
name: ppt-visual-reconstruction
description: High-fidelity image-to-editable-PPTX reconstruction for slide screenshots, image-like PPT decks, visual mockups, AI-generated slide images, and one-picture-per-slide PowerPoints. Use when the user asks to convert pictures to editable PowerPoint, restore a screenshot as PPTX, make bitmap slide text editable, reproduce a visual deck, or preserve complex visual fidelity while rebuilding main text, labels, callouts, page numbers, and simple shapes as editable PowerPoint objects.
---

# PPT Visual Reconstruction

Use this skill to reconstruct image-like slide material into a useful editable PPTX, not a naive OCR dump and not a single flattened screenshot.

## Operating Mode

Use this skill together with the Presentations skill when producing the final PPTX.

Default to a hybrid reconstruction, not a full redraw and not a single flattened slide image:

- Preserve complex visual assets as bitmap layers: backgrounds, 3D objects, illustrations, product UI, medical/technical renderings, textures, light effects, shadows, icons, logos, photos, and intricate diagrams.
- Rebuild editable information layers natively: main title, subtitle, paragraphs, quote lines, key numbers, conclusion boxes, notes, footer text, chapter labels, page numbers, simple rules, simple separators, simple labels, and basic geometric shapes.
- If a detail would lose quality when rebuilt as PowerPoint primitives, keep it as an image unless it is required main text.
- Prefer a visually convincing business deliverable over theoretical full editability. A partially editable deck that matches the source is better than a fully editable deck that looks wrong.

## Workflow

1. Inspect the input.
   - If the PPTX contains a single large image per slide, extract the image from `ppt/media`.
   - If the input is an image, treat it as the reference and source bitmap.
   - Confirm the aspect ratio and output a 16:9 deck unless the user explicitly asks otherwise.

2. Split each slide into layers.
   - `complex visual layer`: retain as source bitmap crops or a cleaned full-slide bitmap.
   - `editable information layer`: rebuild with native text boxes, shapes, lines, tables, or editable chart primitives.
   - `repair layer`: remove old bitmap text only in regions that will be replaced by editable objects.

3. Remove old text only where replacement text will be editable.
   - Do not leave old text behind the new text.
   - Avoid a visible flat rectangle in textured backgrounds.
   - Prefer local texture repair: sample nearby clean background, mirror/scale clean zones, or use soft masks.
   - Use broad flat masks only when the reference area is already plain and the mask will be hidden by editable text.
   - For icon rows, clear label text but paste the original icon artwork back with circular/alpha masks rather than rectangular crops.

4. Rebuild editable text.
   - Use system fonts that match the visual tone, usually Microsoft YaHei or a similar Chinese sans for Chinese slides.
   - Match hierarchy, color, weight, line breaks, alignment, and spacing.
   - Give text boxes enough slack to avoid clipping after PowerPoint font fallback.
   - Keep page numbers, footer claims, icon labels, subtitles, and key conclusion text editable.
   - Keep Chinese text in Microsoft YaHei or a visually compatible Chinese sans-serif unless the source clearly uses another available font.

5. Export and preview.
   - Render the rebuilt PPTX to PNG.
   - Create an original-vs-rebuilt comparison image.
   - Iterate when there is visible old-text ghosting, harsh mask edges, wrong scale, color drift, text overflow, or obvious spacing mismatch.

6. Verify package mechanics.
   - Confirm the final PPTX exists and has the expected slide count.
   - Confirm no empty media files.
   - Inspect PPT XML for the required editable text strings.
   - Treat layout-check text-over-background-image warnings as expected only when the design intentionally places editable text over a visual layer and the rendered preview is clean.

## QA Gates

Do not deliver until:

- Main required text is editable in the PPTX.
- No old bitmap text is visibly readable behind editable text.
- Complex visual areas preserve the original texture and depth.
- Local masking does not create an obvious flat box, hard seam, or rectangular crop in a textured area.
- Simple separators, page markers, and labels align with the reference.
- Final response states which elements are editable and which remain image assets.

If the user circles a flawed restored area, first inspect whether the problem is a mask seam, lost texture, text ghosting, or crop boundary. Then repair the visual layer and rerender before changing editable text.

See [layering-and-qa.md](references/layering-and-qa.md) for detailed repair patterns.

## Strong Defaults

- Output generated files under the current project `outputs/` directory unless the user requests another path.
- Name the final deck clearly, for example `outputs/<task-name>/reconstructed_editable.pptx`.
- Keep intermediate images, extracted media, rendered previews, and comparison images beside the final deck for auditability.
- Do not delete source files or extracted media without explicit user confirmation.
- When the user asks for "as editable as possible", increase editability for text, rules, simple cards, labels, page numbers, tables, and simple charts; do not redraw complex logos, screenshots, or art if that would degrade fidelity.
- When the user asks for "most faithful", keep more visual regions as cleaned bitmap assets and overlay editable key text.
