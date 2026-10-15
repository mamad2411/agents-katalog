---
name: ppt-rebuild-v15
description: Rebuild image-only PPT slides into editable PPTX. Use for restoring slide screenshots or image2-generated PPT images into editable PowerPoint, preserving visual similarity while keeping text, tables, shapes, and KPI cards editable.
---

# PPT Rebuild Skill v15

## Purpose
Convert image-only PPT pages into editable `.pptx` files. v15 favors a practical high-fidelity route:

1. Extract or provide a scene graph with text bboxes and visual objects.
2. If an original slide image is available, create a textless backdrop by inpainting text regions.
3. Crop detected photos/icons from the original image by bbox and reuse them as PPT image assets.
4. Overlay all detected text as editable PPT text.
5. For structured pages, render native editable shapes/tables/KPI cards from the scene graph.
6. Run QA for editable text count, text overflow, and text-to-text overlap.

## Key Difference From v14
v15 keeps v14's placement-plan renderer and adds stricter delivery rules learned from rendered badcases:

- default macOS Chinese font is `PingFang SC` for PPT output;
- text measurement is more conservative for CJK line height and width;
- the `paradigm_shift_1_vs_2` comparison page is a supported reference scene;
- a rendered preview must be visually checked before delivery, even when JSON QA passes.

## Key Difference From v13
v13 routed to templates but did not use template plans during rendering. v15 renders from `placements` plans and includes a default fallback that actually works:

- `--image + scene`: textless backdrop image + editable text layer.
- `--mode scene`: fully editable reconstruction from scene objects.
- visual assets are cropped from the source image before any redraw/recreation.

## When To Use Each Mode
- Use `--mode auto --image input.png` when visual fidelity is most important. This keeps the original non-text artwork close to the screenshot and makes text editable.
- Use `--mode scene` when the page is structured enough to rebuild as native PPT shapes, tables, cards, arrows, and text.
- Use templates only when they return real `placements`; empty template plans are ignored.

## Visual Asset Policy
Do not redraw source photos, equipment images, logos, icons, or detailed decorative graphics by default.

Priority order:

1. Crop the asset from the original slide image using the detected bbox.
2. If no source image is available but the scene has `asset_kind` or `asset_prompt`, generate an SVG source plus PNG fallback for PPT insertion.
3. If the asset is a simple editable icon, optionally convert or redraw it as SVG/native shapes only when the visual match is reliable.
4. If the crop is low quality and the user permits, regenerate a replacement image.
5. Never silently replace a real source image with a made-up placeholder.

Scene objects with `type: "image"`, `"photo"`, or `"icon"` and no `path` are cropped automatically when `--image` is supplied.

When no source image is available, scene objects with `asset_kind` generate local SVG+PNG assets. Current built-in kinds:

- `green_building`
- `awareness_training`
- `carbon_dashboard`

The PPTX uses the PNG fallback for compatibility, while the SVG source is saved next to it for further editing or replacement.

## Scene Graph Requirements
The scene graph must include:

- `slide_size`: source image size, usually `[1600, 900]`.
- `objects`: objects with `id`, `type`, `bbox`, and optional `style`.
- Text objects use `type: "text"` and `text`.
- Mixed-color paragraphs use `type: "rich_text"` and `segments`.
- Images can use relative paths resolved from the skill root.

Supported render types include:

- `text`, `rich_text`
- `rect`, `rounded_rect`, `ellipse`, `triangle`, `arrow`, `line`
- `image`, `photo`, `icon`

## Quick Run

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py \
  --scene examples/china_factor_vs_ipcc.scene.json \
  --mode scene \
  --out test/v15_user_image/china_factor_vs_ipcc_rebuilt.pptx \
  --plan-out test/v15_user_image/china_factor_vs_ipcc.plan.json
```

With an original image:

```bash
python scripts/run_pipeline.py \
  --image input.png \
  --scene scene_graph.json \
  --mode auto \
  --out output/rebuilt_editable.pptx
```

Multi-slide editable scene deck:

```bash
python scripts/run_deck.py \
  --mode scene \
  --scenes page1.scene.json page2.scene.json page3.scene.json page4.scene.json \
  --images page1.png page2.png page3.png page4.png \
  --out output/rebuilt_editable_deck.pptx \
  --plans-out output/rebuilt_editable_deck.plan.json
```

Use `--mode scene` when the user explicitly needs editable PPT objects. It rebuilds native shapes/text and crops source photos/icons from the matching source image.

## QA Gates
The run writes `<output>.qa.json` and should pass:

- `overflow.status == "pass"`
- `overlap.status == "pass"`
- `editable_char_count` is high enough for the slide
- `placement_count` is non-zero

When Quick Look, LibreOffice, or PowerPoint rendering is available, render a PNG preview and visually inspect it against the source image before delivering.

## Known v15 Failure Mode: False QA Pass With Rendered Text Overlap
`overflow` and `overlap` audits operate on scene bboxes and a crude text estimator. They can pass while PowerPoint/Quick Look still wraps text differently, especially when:

- scene `font_size` is treated as PPT points instead of source-image pixels;
- a text bbox is too short for CJK line height;
- rich colored text is built as a single paragraph and reflows around segment boundaries;
- centered labels inside narrow KPI cards wrap after export;
- table cells rely on visual centering but the actual font metrics differ.

Mitigation:

1. Convert source-image pixel font sizes to PPT points with `pt = px * 0.72`.
2. Render a preview PNG after exporting PPTX.
3. Treat visible overlap in the preview as a failure even if JSON QA says pass.
4. For dense table cells, reduce font size or widen the bbox before delivery.
5. For rich text, prefer multiple positioned text boxes when exact line breaks matter.

## Reference Scene Added In v15

`examples/paradigm_shift_1_vs_2.scene.json` covers the two-column "1.0 vs 2.0" comparison pattern:

- title and subtitle are editable text;
- left/right badges are editable text over native rounded rectangles;
- six illustration blocks are cropped from the source image, not redrawn;
- arrows, rules, background tints, and labels are native PPT objects;
- preview rendering is required to catch badge wrapping and CJK text reflow.
