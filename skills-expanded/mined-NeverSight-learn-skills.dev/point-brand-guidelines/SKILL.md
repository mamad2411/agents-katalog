---
name: point-brand-guidelines
description: Apply and review Point's official visual brand system for logos, typography, colors, artwork, photography, and comparison layouts. Use when creating, editing, or auditing Point-branded web pages, ads, decks, documents, social assets, illustrations, photo direction, design systems, CSS, or UI components where visual brand compliance matters.
---

# Point Brand Guidelines

Apply Point's official visual identity consistently across design and implementation work.

## Workflow

1. Read [visual-guidelines.md](references/visual-guidelines.md) before creating or reviewing a visual asset. For illustration work, also read [illustration-system.md](references/illustration-system.md) and [illustration-reference-index.md](references/illustration-reference-index.md).
2. Identify the output medium, dimensions, audience, and supplied brand assets. Inspect `assets/` before looking elsewhere for logos or fonts.
3. Reuse the approved files in `assets/` when the deliverable needs a Point logo or bundled typeface; copy or embed the appropriate file in the output rather than recreating it.
4. Apply the exact logo, typography, color, and spacing rules before making stylistic choices.
5. Treat the artwork, photography, and comparison-layout guidance as direction derived from the guide's examples, not as an exhaustive asset library.
6. Use only approved logo, font, artwork, and photo files supplied by Point or available in Point's media kit. Do not redraw the logo, recolor it, or silently substitute proprietary fonts.
7. If the deliverable includes marketing copy, also use the sibling `point-brand-voice` skill. Keep visual-brand review and copy/compliance review distinct.
8. Verify accessibility, rendering, and current product accuracy before delivery.

For visual references, distinguish files that are approved for reuse from files supplied only to demonstrate style. Do not copy an example image into production unless the reference index or current brief explicitly confirms reuse rights.

## Bundled Assets

Use `assets/` as the first source for production files. Do not load binary assets into context merely to inspect the folder; list filenames and use the selected files directly in the deliverable.

- `assets/SVG/`: Prefer for web, UI, and other scalable digital work.
- `assets/PNG/`: Use when a transparent raster image is required.
- `assets/JPG/`: Use only when a flattened raster image is appropriate; JPG files do not preserve transparency.
- `assets/PDF/`: Prefer for print and vector-capable document workflows.
- `assets/Fonts/`: Contains the supplied ITC Century, Circular Std, and Lora font files. Use Lora Italic when an italic serif treatment is needed. Follow the full typography rules in [visual-guidelines.md](references/visual-guidelines.md).

Choose the logo color variant for legibility on the actual background. Use a `-padded` file when the output needs built-in canvas space; otherwise enforce the required clear space in the surrounding layout. Preserve the original asset filename and proportions, and do not modify the artwork inside the file.

## Nonnegotiable Rules

- Keep the logo's original proportions and approved colors.
- Use a minimum logo height of 20 px in digital work or 0.6 in in print.
- Keep clear space on every side equal to at least 50% of the rendered logo height.
- Use ITC Century Book for primary headers. Use Circular Bold only for smaller headers.
- Set header line height to 150% (1.5em), and keep headers short and left- or center-aligned.
- Use Circular Std Book for body copy; use the Medium, Bold, and Black weights deliberately for hierarchy or emphasis.
- Use Lora Italic for italic serif text.
- Use yellow and Point Blue sparingly. Reserve Point Blue primarily for links or a focal element against muted colors.
- Use `yorange` (`#F4C65D`) with `pointBlack` (`#444444`) for primary CTA buttons unless the approved design specifies another button variant.
- Center CTA labels horizontally and vertically. Use Point's standard 0.25rem radius rather than a pill or heavily rounded treatment.
- Test color contrast in the actual composition. A palette token's name does not replace an accessibility check.
- Never reuse the product amounts, terms, loan-to-value figures, availability counts, or competitor data shown in the guide's design examples as current claims. Validate live product facts separately.

## Review Checklist

Before delivering an asset, confirm:

- The correct approved logo variant is legible on its background.
- Minimum size and clear-space rules are met.
- Typefaces, weights, alignment, and 1.5 header line height follow the guide.
- Colors match the official values and accent colors are restrained.
- CTA colors, label alignment, and corner radius follow the current Point button pattern.
- Artwork or photography feels consistent with the reference direction without copying an example as a reusable asset.
- Comparison layouts make Point prominent without compromising clarity or accessibility.
- Text, controls, charts, and tables meet the applicable accessibility standard.
- Product facts and marketing claims come from current approved sources, not the historical design mockups.

## Source

Base decisions on the official [Point Brand Guide](https://files.point.com/Point-brand-guidelines.pdf). Use [visual-guidelines.md](references/visual-guidelines.md) as the concise working reference.
