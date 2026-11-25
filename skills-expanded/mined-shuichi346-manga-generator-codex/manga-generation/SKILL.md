---
name: manga-generation
description: Plan and generate colorful manga pages from user-provided story drafts, character/reference images, and style notes. Use when Codex is asked to turn a manga story or script into page-by-page manga art, choose manga manuscript templates, create panel-by-panel drawing and dialogue briefs, expand drafts in Original/Slight Expansion/Expansion modes, or generate completed multi-panel manga page images with $imagegen.
---

# Manga Generation

## Core Rule

Generate manga per page, not per panel. Each imagegen call should create one complete colorful manga page containing all panels, borders, bubbles, dialogue, sound effects, and page composition.

Do not create final manga art by placing or compositing images with Python, Pillow, HTML/CSS, SVG, or other deterministic layout code. Those tools may be used only to maintain blank layout templates and manifests. Final manga pages must be rendered by `$imagegen` from the selected layout template, user reference images, and a detailed page prompt.

## Inputs

Use these defaults unless the user specifies otherwise:

- Expansion mode: `Original`
- Maximum pages/images: `5`
- Template folder: `assets/Manga_Panel_Layout_Template/` relative to this skill directory
- Output folder for final pages: `output/manga-pages/` relative to the active workspace or repository root

Treat attached or referenced images explicitly by role: `character reference`, `style reference`, `scene/object reference`, or `panel layout template`.

When the user provides character or object images, treat them as visual references to be redrawn into the manga page, not as cut-out assets to paste into panels.

## Draft Expansion Modes

- `Original`: Preserve the draft structure, events, character intent, and dialogue as much as possible. Only add panel-level clarity.
- `Slight Expansion`: Add small connective actions, expressions, setting details, and short dialogue where needed. Keep the same plot shape.
- `Expansion`: Develop the premise into a fuller manga sequence with added beats, transitions, emotional escalation, and scene detail. Preserve the user's premise and constraints.

## Workflow

1. Read the story draft and image references. Ask one focused question only if a missing choice would materially change the manga.
2. Build a beat sheet sized to the page limit. If the draft is short, use fewer than the maximum pages rather than padding weak scenes.
3. Choose a page template from `assets/Manga_Panel_Layout_Template/template_manifest.json`. If the manifest is missing, inspect the PNGs in `assets/Manga_Panel_Layout_Template/`.
4. Write a page plan before generating images. For every page, include the selected template filename, page purpose, continuity notes, and exact panel briefs.
5. Load any local template or reference images that should influence generation before calling imagegen. Label each loaded image by role before generation.
6. Use `$imagegen` to generate one completed full-color manga page per planned page in story order: Page 1 first, then Page 2, and so on. Keep prompts page-specific and include all panels for that page in one prompt.
7. Save final project-bound images under `output/manga-pages/` with stable sequence filenames such as `page-001.png`, `page-002.png`, and `page-003.png`, matching the story order exactly.
8. Report saved paths, selected templates, expansion mode, and page count in ascending page order.

## Story Order Requirements

- Treat the beat sheet as the source of truth for story progression.
- Do not reorder planned pages after image generation based on completion time, visual quality, template choice, or file system ordering.
- When multiple images are generated, present and arrange the completed pages in numeric page order from the story plan.
- If a page must be regenerated, keep its original page number and filename so later pages do not shift.

## Required Page Plan Format

Use this shape before every generation pass:

```text
Expansion mode: <Original | Slight Expansion | Expansion>
Maximum pages: <number>

Page 1
Template: <filename from assets/Manga_Panel_Layout_Template/>
Page purpose: <story function>
Continuity: <character outfits, setting, props, mood>
Color continuity: <hair, clothing, environment palette, lighting, recurring motif colors>

Panel 1:
Draw: <subject/action/camera/background>
Dialogue: "<verbatim text or none>"
SFX: "<verbatim text or none>"
Balloon/caption placement: <where text belongs without covering key art>

Panel 2:
Draw: <subject/action/camera/background>
Dialogue: "<verbatim text or none>"
SFX: "<verbatim text or none>"
Balloon/caption placement: <where text belongs without covering key art>
```

Use the visible panel numbers on a selected template as the panel IDs and reading order. Do not infer a Western left-to-right order when the template numbers indicate a manga flow.

## Imagegen Prompt Rules

Use `$imagegen` with `Use case: illustration-story`. In each page prompt, include:

- The selected template filename and its role as a panel layout reference.
- A clear instruction to draw or edit into a complete full-color manga page in one image.
- The full panel list in numeric order with `Draw`, `Dialogue`, `SFX`, and placement.
- Character consistency notes from supplied character references, including face shape, hair, outfit, age impression, and recurring props.
- Color continuity notes for hair, clothing, environment, lighting, mood, and recurring visual motifs.
- Constraints: preserve panel borders, keep gutters clear, do not add unrelated text, do not add watermarks, and do not generate extra panels.

Prompt with concrete imagegen verbs. Prefer "draw this page using the template image as the panel layout reference" or "edit the layout reference by redrawing it as a finished manga page" instead of vague instructions such as "combine these images."

For exact text, keep dialogue concise. If exact lettering is critical and imagegen text is unreliable, generate clean speech balloons with reserved text areas and plan a separate lettering pass.

See `references/page-plan-format.md` for a compact filled example.
See `references/template-selection.md` for template selection guidance.
See `references/imagegen-page-prompt.md` for the page prompt scaffold.

## Template Maintenance

Use `scripts/generate_manga_templates.py` to regenerate deterministic blank manuscript bases, clean panel layout templates, and `assets/Manga_Panel_Layout_Template/template_manifest.json`.

Do not write personal local paths, credentials, API keys, tokens, or machine-specific configuration into prompts, manifests, or generated metadata.
