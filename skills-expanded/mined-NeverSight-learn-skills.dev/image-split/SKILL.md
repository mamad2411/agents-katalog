---
name: image-split
description: Split generated slide/page images into editable-ready transparent visual element layers. Use when Codex needs to extract PPT/Image2/AI-generated slide visuals into PNG assets, separate text from visual components, preserve original slide layout, build a "visual elements" folder, create CopySlides-like region schemas, run OCR-racing evidence, rebuild slide visuals before adding editable text, or avoid OCR/OpenCV fragmentary split failures.
---

# Image Split

## Core Rule

For editable PPT reconstruction, split by atomic visual assets, not broad skeleton layers and not connected-component fragments.

- Use OCR only to locate text masks. Do not let OCR boxes define visual element boundaries.
- For difficult pages, run OCR racing as evidence for text/content/layout only; the production boundary is the region schema and visual anchors, not the first OCR result.
- Rebuild simple geometry such as cards, tabs, badges, arrows, rules, circles, and dashed boxes as clean drawn layers.
- Extract complex visuals such as icons, diagrams, photos, charts, logos, decorative line art, and illustrations from the source image.
- For circular icon UI, split the object into separate assets: deterministic circle/ring shape, inner glyph, and optional separator/accent. Do not crop the entire circular icon as one bitmap unless it is a photo/logo.
- Prefer one reusable visual object per asset: each badge, pill, icon, card outline, arrow, connector, divider, logo, footer, and illustration should be its own named asset when it is meant to be editable/movable/replaced.
- Output cropped transparent PNG assets plus placement metadata when building an editable deck; full-canvas PNG layers are acceptable only for preview compatibility or true background-wide elements.
- Remove semantic text from visual layers unless the user explicitly wants logo text, chart labels, or decorative background text preserved.
- Do not blur alpha for geometric/UI assets. Use antialiasing only from clean vector drawing or high-resolution downsampling.

## Runtime Assumptions

- The bundled smoke demo is deterministic and can run without an AI model once Python dependencies are installed.
- Production splitting needs a Codex-style agent that can inspect images, read/write files, run Python/OCR commands, and review generated PNG artifacts.
- Use a strong multimodal reasoning model for real slide reconstruction. The author-known-good profile is macOS, Codex-style local agent, GPT-5.5-class multimodal reasoning, and `xhigh` reasoning for difficult pages.
- Use `high` reasoning for normal production work; use `xhigh` when available for dense decks, ambiguous OCR, or layout-heavy pages.
- Smaller models may run the scripts but are more likely to create weak region schemas, miss visual anchors, or accept poor splits.
- For macOS/Windows/Linux setup details, read `references/runtime-and-platform.md` before promising reproducibility to a user.

## Routes

- `atomic-assets route`: production route for editable PPT. Outputs many named, cropped transparent assets with `position` metadata and optional full-canvas preview layers.
- `copyslides-like region route`: production route for difficult Image2 slide pages. First creates a semantic `region-schema.json`, optionally supported by OCR-racing evidence, then rebuilds regular UI geometry as clean drawn assets and extracts complex illustrations/photos as separate image objects. This route must not use a full-page textless/inpaint image as the production visual base.
- `visual-skeleton route`: quick preview route. Uses a few broad full-canvas layers to test layout rhythm, but is not accepted as final editable素材.

## Workflow

1. Inspect the source slide image before scripting. Identify:
   - slide chrome: header lines, footer bars, page number zones
   - geometric components: cards, labels, badges, arrows, dividers
   - extracted image components: icons, illustrations, chart/photo regions, background line art
   - text zones to rebuild later as editable text
2. Choose the route explicitly. Use `atomic-assets route` unless the user only asks for a rough visual skeleton.
3. For dense or previously failed pages, create a CopySlides-like region schema before extracting assets:
   - classify `title`, `body`, `flow_label`, `card`, `tab`, `badge`, `chart`, `microscopy`, `photo`, `image`, `illustration`, `caption`, `footer`, and `page_number` regions
   - record region boxes, anchors, z-order, colors, editability, native-shape requirement, OCR sources, confidence, and intended reconstruction method
   - use the schema as the contract between `image-split` and `image-ppt`
4. For high-risk text-heavy pages, run OCR racing and merge evidence:
   - capture Apple Vision / PaddleOCR / PP-Structure / MinerU results when locally available and approved for the document
   - write `ocr-candidates.json`, `ocr-merged.json`, and `ocr-review-report.md`
   - use agreement between engines for text content; use layout regions plus OCR boxes for rough masks only
   - mark low-confidence or conflicting text as `needs-human-review` instead of silently choosing one engine
5. Create an atomic component map:
   - separate every repeated UI unit that a user may want to move, replace, recolor, or delete
   - keep repeated groups consistently named, such as `card_tl_outline`, `card_tl_tab_bg`, `card_tl_icon`, `connector_tl_line`
   - split text away from visual shapes; label text belongs to `image-ppt`
6. Use full-canvas preview only as QA. Do not confuse a full-canvas preview layer with a production asset.
7. Use OCR text masks only as subtraction masks for extracted image regions. Tighten or override OCR masks when they hit icons, logos, or line art.
8. Draw simple PPT-like shapes instead of trying to crop them from the bitmap.
9. Extract complex regions with foreground, color, or line-art masks; apply morphology lightly so thin strokes and antialiasing survive.
10. For icon glyphs:
   - draw the circle/ring/pill base as vector-like geometry
   - crop only the internal glyph pixels with a tight box
   - use light masks for white glyphs on blue and color-distance masks for blue glyphs on pale backgrounds
11. Generate QA artifacts: `manifest.json`, `assets_contact_sheet.png`, `composite_no_text_preview.png`, `text_mask_for_reference.png`, and `region-schema.json` when using the CopySlides-like route.
12. Run textless-layer OCR or manual text-region review for high-risk pages. If title/body/card text remains in visual layers, fix the split before `image-ppt`.
13. Review the composite preview against the original and the contact sheet for asset quality. Fix missing geometry with drawn assets; fix missing source art with wider regions or a line-art mask.

For the stricter v2 workflow used on difficult editable-PPT pages, read `references/v2-atomic-workflow.md` before authoring the elements file.
For the CopySlides-like route validated on Image2 deck page 16, read `references/copyslides-like-region-workflow.md` before authoring the region schema or visual layers.
For OCR racing, region-schema fields, and merge rules, read `references/region-schema-ocr-racing.md` before accepting text-heavy pages.
For public one-command OCR setup and supported engines, read `references/ocr-tools.md` when available.
For final or high-risk samples, read `references/acceptance-rubric.md` and report pass/warn/fail gates before handing visual layers to `image-ppt`.

## Bundled Script

After installing this skill folder by itself, install script dependencies from the skill root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

For production editable-PPT samples, prefer an atomic elements file and cropped positioned assets:

```bash
python scripts/atomic_asset_split.py \
  --image /path/to/slide.png \
  --elements /path/to/elements.json \
  --out /path/to/output-folder
```

The script writes cropped transparent PNG assets, `manifest.json`, `assets_contact_sheet.png`, and `composite_no_text_preview.png`. The manifest is consumable by `image-ppt` because each cropped asset has `position` and `canvas` metadata. For cropped raster assets, use `mask: "nonwhite"` for art on pale backgrounds, `mask: "light"` for pale line art/icons on deep color backgrounds, and `mask: "color"` for single-color glyphs on pale backgrounds.

Run the bundled smoke demo from the skill root:

```bash
python scripts/atomic_asset_split.py \
  --image assets/demo/input.png \
  --elements assets/demo/elements.json \
  --out outputs/demo
```

Use `scripts/component_layer_split.py` for repeatable component-layer extraction from a single source image:

```bash
python scripts/component_layer_split.py \
  --image /path/to/slide.png \
  --out /path/to/output-folder \
  --recipe /path/to/recipe.json \
  --ocr-json /path/to/ocr.json \
  --slide 3
```

The script reads a recipe, writes full-canvas transparent PNG layers, and generates contact-sheet/composite QA images. Read `references/recipe-schema.md` before authoring or patching a recipe.

Use `scripts/ocr_race.py` to generate OCR evidence:

```bash
python scripts/ocr_race.py \
  --image /path/to/slide.png \
  --out /path/to/ocr-output \
  --engines tesseract,paddleocr,mineru \
  --lang eng+chi_sim
```

The script writes `ocr-candidates.json`, `ocr-merged.json`, `ocr-review-report.md`, and `ocr_boxes_preview.png`. In the public repository, the default one-command path is `make ocr-demo`, which runs Tesseract in Docker; PaddleOCR and MinerU are optional heavier engines.

When this skill folder is installed by itself, the same Docker path is bundled at the skill root:

```bash
make ocr-demo
```

This writes OCR artifacts under `outputs/ocr-demo/`. Without Docker, install optional OCR Python bindings with `pip install -r requirements-ocr.txt` and make sure the Tesseract binary is installed on the host before running `scripts/ocr_race.py`.

## Recipe Pattern

Use drawn assets for stable geometry:

```json
{
  "name": "cards_tabs_badges_arrows",
  "type": "draw",
  "items": [
    {"shape": "rounded_rect", "box": [40, 376, 258, 706], "outline": "#0052AA", "width": 3, "radius": 15},
    {"shape": "rounded_rect", "box": [56, 337, 241, 388], "fill": "#0052AA", "radius": 10},
    {"shape": "circle", "center": [151, 300], "radius": 31, "fill": "#0052AA"},
    {"shape": "arrow", "from": [273, 489], "to": [313, 489], "fill": "#0052AA"}
  ]
}
```

Use extracted assets for complex source art:

```json
{
  "name": "card_icons_no_text",
  "type": "extract",
  "mask": "foreground",
  "regions": [[65, 405, 230, 535], [360, 420, 500, 535]],
  "subtract_text": true,
  "close": 3
}
```

## Tool Choices

- Use OpenCV/Pillow for deterministic masks, drawing, contact sheets, and previews.
- Use Apple Vision, PaddleOCR/PP-Structure, or MinerU for OCR/layout evidence. Do not let any one OCR engine define final visual assets by itself.
- Consider SAM/SAM2 for difficult object masks if region extraction is not enough.
- Use inpainting or LaMa only for small background repairs; do not rely on it to reconstruct covered visual components.
- For blue UI geometry, cards, rules, dashed connectors, and badges, prefer vector/native shape generation or clean drawn assets over bitmap extraction.
- Do not use a full-page inpainted/textless base as the production layer for pages with editable labels/cards/title text. It tends to preserve residual glyphs and creates false QA passes.

## Quality Bar

Accept a split only when:

- All layer PNGs have the exact original canvas size and transparency.
- In `atomic-assets route`, all production assets are atomic and named; broad layers are limited to background/footer/line-art/chart/photo regions.
- In `copyslides-like region route`, a `region-schema.json` exists and the production visual layers are traceable to semantic regions.
- The composite preview restores the visual layout without obvious missing cards, icons, lines, or badges.
- Semantic text is absent from visual layers, except intentional logo/decorative/chart text.
- Extracted components are grouped by design meaning, not by arbitrary pixel connectivity.
- UI asset edges are crisp: no Gaussian-blurred alpha, fuzzy rounded corners, rectangular source-crop halos, or background-colored residue.
- Any remaining limitations are documented in `manifest.json` or the final response.

## Acceptance Standards

Run these checks before declaring a split usable.

Use `references/acceptance-rubric.md` for the detailed gate model. The short standard below is only the minimum.

### Required Artifacts

Each processed slide must have:

- `manifest.json` with layer names, source/drawn status, and known limitations.
- For `atomic-assets route`: cropped transparent PNG assets with source-canvas `position` metadata, plus optional full-canvas preview layers.
- For `visual-skeleton route`: full-canvas transparent PNG layers, all matching the source image size.
- For `copyslides-like region route`: `region-schema.json`; for high-risk text-heavy slides, `ocr-candidates.json`, `ocr-merged.json`, and `ocr-review-report.md`.
- `composite_no_text_preview.png` showing all visual layers reassembled at `(0,0)`.
- `assets_contact_sheet.png` for quick layer review.
- `text_mask_for_reference.png` or an equivalent OCR/hand text-zone mask.
- For important slides, a source / composite / diff review image.

### Structural Checks

- Every layer is RGBA or otherwise has a real alpha channel.
- Atomic cropped assets must include precise `position` metadata: source x/y/w/h, source canvas size, and intended slide size if known.
- Full-canvas preview layers must use the original slide canvas size.
- A typical editable page may have 20-80 atomic assets. Do not collapse independent UI objects into one broad layer just to reduce layer count.
- Do not accept dozens of arbitrary connected-component fragments; fragments are only valid if each corresponds to an intentional visual object.
- Layer names must describe design meaning, such as `header_chrome`, `cards_tabs`, `diagram_icons`, `footer_lineart`; names like `component_42` are not sufficient for production.
- Blocking structural failure: an asset named like a group (`blue_filled_ui`, `source_visuals`, `all_icons`, `all_cards`) contains multiple unrelated movable objects in production output.

### Visual Checks

- Compare `composite_no_text_preview.png` with the source page while ignoring intended text-removal zones.
- Outside text zones, large missing cards, blue labels, number badges, icons, lines, footers, campus line art, and diagram/photo regions are blocking failures.
- Any obvious white patch, solid-color repair block, unexpected deep-blue block, broken circle, cropped icon, or missing footer/page chrome is a blocking failure.
- Any fuzzy corner, blurred alpha edge, background halo, rectangular crop boundary, or merged multi-object patch on UI assets is a blocking failure for `atomic-assets route`.
- Circular icons must pass a component split check: the circle/ring base is a drawn asset, the glyph is a tight transparent crop, and the contact sheet does not show a full circular bitmap with background residue.
- Review `assets_contact_sheet.png`: each tile should show one complete, sharp visual object or one documented background-wide element.
- For pixel checks, use thresholds as a guide, not a substitute for review: outside text zones, changed pixels above 25 RGB levels should usually stay below 8-12% for clean geometric pages. Complex chart/photo pages may exceed this but must be manually justified.

### Text Removal Checks

- OCR the composite preview when practical. Main semantic text should be gone from visual layers.
- For high-risk pages, `textless layer OCR` is a blocking gate: if the composite still reads as title/body/card text, the split fails even when non-text diff is good.
- Preserved text must be intentional and documented: logo text, chart/axis text, microscopy labels, or decorative background text.
- If OCR masks damage icons, logos, dashed rules, or fine line art, override them manually rather than accepting a damaged layer.

### Image2 Textless Skeleton Route

When the visual skeleton comes from Image2 or another generative edit instead of deterministic splitting:

- Treat it as a separate route, not as a normal split.
- Compare the skeleton against the source for layout anchors: title baseline, header line, footer band, card/frame boxes, icon centers, and chart/photo bounding boxes.
- If Image2 moved or invented components, do not reuse old text coordinates without remapping.
- A skeleton that is visually polished but changes layout must be marked `layout-remap-required` in `manifest.json` or the final response.

### Stop Conditions

Stop before full-deck work if a sample slide has:

- missing or broken primary visual components,
- visible repair patches,
- unacceptably changed layout anchors,
- semantic text still baked into major visual layers,
- or no reliable way to distinguish intended text removal from damaged visuals.
