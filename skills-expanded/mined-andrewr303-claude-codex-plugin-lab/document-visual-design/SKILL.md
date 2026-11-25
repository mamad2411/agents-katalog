---
name: document-visual-design
description: Design beautiful document and presentation visuals, including cover pages, title pages, report layouts, proposal packaging, charts, diagrams, callouts, generated images, executive deck visual systems, and PDF/Word visual polish. Use when the user asks for a document to look better, more polished, premium, branded, investor-ready, or visually appealing.
---

# Document Visual Design

Use this skill when the document or deck needs visual judgment, not only text editing.

## Required resources

Read before implementing visual work:

- `../../visual-design-skill.txt`
- `../../canvas-design-codex/SKILL.md` when generated visuals, SVG, canvas, charts, or rendered pixels matter.
- `../word-document-studio/SKILL.md` for Word layout and title pages.
- `../presentation-document-studio/SKILL.md` for deck layouts.
- `../document-data-charts/SKILL.md` for charts and data visuals.

## Visual system workflow

1. Identify the artifact type and audience.
2. Choose a visual concept: formal, editorial, premium, technical, investor, operational, legal, or sales.
3. Choose type hierarchy, palette, spacing rhythm, page/slide furniture, table treatment, chart treatment, and image style.
4. Use the smallest consistent system that can support the whole artifact.
5. Apply design through real Word/PowerPoint structures, not random manual formatting.
6. Render/export and inspect.

## Title and cover pages

For title pages:

- Keep the information hierarchy simple.
- Use strong typography and spacing.
- Include only useful metadata.
- Avoid generic stock-photo clutter.
- Use generated imagery only when it supports the message.
- Verify image crop, contrast, and text legibility after export.

## Images and generated visuals

Use image generation when original artwork, cover imagery, concept illustration, or decorative support materially improves the document.

- Use the available image generation tool.
- If model selection is exposed, choose `gpt-image-2`.
- Specify aspect ratio, safe text area, crop intent, mood, material style, and whether people or objects should be left/right/center.
- Do not place critical text inside generated images unless it will be checked and corrected.
- Inspect generated images before embedding.

## Charts and diagrams

- Use diagrams only when they clarify relationships or flow.
- Use native Office charts/shapes where editability matters.
- Use generated imagery for aesthetic or illustrative diagrams, not for precise data charts.
- Ensure labels are readable at final output size.

## Visual QA

Check:

- Clipping.
- Overlap.
- Low contrast.
- Bad crop.
- Image blur.
- Overfull tables.
- Unbalanced margins.
- Inconsistent heading hierarchy.
- Inconsistent footers/page markers.
- Awkward page/slide breaks.
