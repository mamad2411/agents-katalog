---
name: pptx-processor
description: Create, edit, inspect, and validate PowerPoint presentations (.pptx) for status reporting, decisions, proposals, analysis, training, manuals, sales, events, and Japanese corporate communication. Use for new decks, template-based presentations, slide changes, data storytelling, visual redesign, and presentation quality review.
---

# PPTX Processing

## Select the communication mode

Determine the presentation's job, audience, delivery setting, speaking context, and reuse needs before selecting a visual style. Read [presentation-modes.md](references/presentation-modes.md) and choose the closest mode. Combine modes intentionally, such as a decision deck with a detailed appendix.

Do not force every deck into a sparse keynote style. A projected talk, a Japanese internal decision document, a training manual, and a recurring status deck need different information density.

## Choose a safe workflow

### Create a new deck

Use PptxGenJS for a presentation created from scratch. Define the slide size, theme fonts, palette, spacing, and reusable layout helpers before creating slides. Build each slide from structured content and reusable components.

Normalize its CommonJS default export before constructing it:

```typescript
import importedPptxGenJS from 'pptxgenjs';

type PptxGenJSConstructor = typeof importedPptxGenJS;
const PptxGenJS =
  (importedPptxGenJS as unknown as { default?: PptxGenJSConstructor }).default ??
  importedPptxGenJS;

const pptx = new PptxGenJS();
```

### Create from an existing template

1. `mcp__pptx__pptx` with `inspect` — get slide order, dimensions, theme, features.
2. `capabilities` — confirm action is supported for the target objects.
3. `read` the relevant slides to understand object structure.
4. `create-template` only when explicitly clearing template slides for a new deck.
5. Reuse the template's masters, layouts, theme, and placeholders.

### Modify an existing deck

1. `inspect` — obtain slideIds, risk features, layout paths.
2. `capabilities` — confirm the required action and backend.
3. `search` or `read` — locate slideId + objectId for every target.
4. `patch(dryRun: true, strict: true)` — verify hit counts and expectedText match.
5. `patch` — apply. Record sourceHash and outputFile.
6. `diff` — confirm only the expected slides/parts changed.
7. `validate` — verify package integrity.
8. Convert to PDF and visually inspect all slides.

**OOXML backend supports**: `replace-text`, `replace-all-text`, `set-speaker-notes`, `update-table-cells`, `duplicate-slide`, `delete-slide`, `reorder-slide`, `delete-object`, `duplicate-object`, `set-object-properties` (position/size/name).

**UNSUPPORTED (requires Office COM)**: `replace-image`, `add-object`, `reorder-object` (z-order), `align-objects`, `distribute-objects`, `update-chart-data`, SmartArt, animation, OLE. If COM is unavailable, report clearly and stop — do not fall back to unpack/raw XML.

### Add slides to an existing deck

Preserve every existing slide reference and file. Use the `add-object` or `duplicate-slide` patch operations. Only clear the entire slide list for an explicitly requested full-deck replacement, and do so on a copy.

## Design the story and slides

1. State the audience outcome: inform, decide, approve, teach, persuade, or align.
2. Draft a narrative and slide outline before coding layouts.
3. Give each slide one primary communication job.
4. Write takeaway titles when the evidence supports a conclusion; use neutral topic titles for reference or instructional slides.
5. Choose a layout pattern from [layout-and-visual-system.md](references/layout-and-visual-system.md).
6. Apply the chart guidance in [charts-and-data-storytelling.md](references/charts-and-data-storytelling.md) when presenting data.

## Handle content responsibly

- Separate facts, assumptions, interpretation, and recommendations.
- Preserve source notes, dates, units, and definitions for important claims.
- Use high-resolution, relevant images with appropriate usage rights.
- Escape XML text when performing OOXML edits and preserve whitespace deliberately.

## Validate before delivery

Follow [validation-checklist.md](references/validation-checklist.md). At minimum:

1. Run `validate` on the output file.
2. Run `diff` against the source to confirm only expected changes.
3. Convert the deck to PDF, then use PDF `to-images` on all pages for visual inspection.
4. Check overflow, overlap, clipping, missing media, font substitution, alignment, contrast, and chart readability.
5. Confirm the original remains unchanged and remove unpacked or temporary files from delivery.
