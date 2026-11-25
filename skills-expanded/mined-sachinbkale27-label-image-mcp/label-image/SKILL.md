---
name: label-image
description: Annotate images, including H&E histopathology slides, and turn them into training data with the Histopathology Annotation MCP server (label-image-mcp, Image Label at labels.sachin-kale.com). Use when the user wants to upload images or whole slides (SVS, NDPI, pyramidal TIFF), outline objects with Segment Anything / MedSAM, detect and measure nuclei (StarDist), type cells (HoVer-Net), check slide quality, normalize stain, fix or clean up annotations, share an annotated image, or export COCO JSON, YOLO or QuPath GeoJSON. Also use when the user mentions Image Label, labels.sachin-kale.com, or tools such as detect_nuclei, analyze_slide, segment_objects or export_annotations.
license: MIT
---

# Image annotation, including histopathology slides

This skill drives the `label-image` MCP server (Histopathology Annotation MCP), which manages images
and annotations in [Image Label](https://labels.sachin-kale.com), analyses H&E images and whole slides,
and exports COCO JSON, YOLO or QuPath GeoJSON. Results are for research and education, not diagnosis.

## Before you start

1. Check that the tools are available (`list_images`, `get_image`, `upload_image`, `detect_nuclei`,
   `segment_objects`, `export_annotations`, ...). If they are missing, tell the user to install the server:
   ```bash
   claude mcp add label-image -- uvx label-image-mcp
   ```
   Other clients: https://github.com/sachinbkale27/label-image-mcp#install. No browser setup? The same
   tools run at https://agent.sachin-kale.com/#annotate.
2. **No account is needed.** Without credentials the server works as a guest: images kept 7 days (up to
   50), 20 MB per image, 200 analyses a day, no whole slides. An account (`LABEL_USERNAME` /
   `LABEL_PASSWORD` in environment variables; never ask the user to paste a password into chat) keeps
   images 90 days and allows whole slides up to 5 GB. An `HTTP 401`/`403` usually means wrong
   credentials or a guest limit: report the message, don't retry.
3. The tools see only the images of the identity they use (guest or account), not work kept only in
   the browser.

## Data model you must respect

Coordinates are **image pixels, origin top-left**. Always call `get_image` first and keep
every coordinate inside `0..width` and `0..height`.

| type | required fields | exported to COCO/YOLO? |
|---|---|---|
| `polygon` | `points` (3 or more `{x, y}`) | **yes** (segmentation + bbox) |
| `circle` | `x`, `y` (center), `radius` | **yes** (as a 32-point polygon) |
| `rectangle` | `x`, `y` (top-left), `width`, `height` | no |
| `pin` | `x`, `y` | no |
| `arrow` | `x`, `y` (label position), `arrowTarget` `{x, y}` | no |

Every annotation also takes `label` (the class name), and optionally `color` (default
`#ff0000`), `notes` and `confidence` (`high` / `medium` / `low`).

**Training data must be polygons or circles.** Rectangles, pins and arrows are silently left
out of exports. For a box, use a 4-point polygon:
`[{x:L,y:T},{x:R,y:T},{x:R,y:B},{x:L,y:B}]`. Use pins and arrows only for human-facing notes.

## Workflows

### Explore
`list_images(category?)` returns summaries with `annotationCount`. `get_image(image_id)` returns
the annotations (with their `id`s) and a signed viewing URL valid for 24 hours. Show the user a
compact table rather than raw JSON.

### Upload
`upload_image(path, name?, category?, description?)` reads the file **on the machine running the
MCP server**. Use an absolute path. With a remote HTTP server, a local path won't exist: use
`upload_image_from_url(url, ...)` for images that are online. Set a
`category` at upload: it's the only filter `list_images` has. Upload one file per call and
report each new `imageId`.

### Look at the image
`view_image(image_id)` (0.4.0+) shows the picture with a grid labelled in image pixels: read boxes and
points off it instead of guessing. `region` zooms into part of a large image. After annotating, call it
with `with_annotations: true` and fix outlines that landed on the wrong object.

### Trace outlines (preferred)
Call `warm_up("sam")` (or `"medsam"`) as soon as you know you will segment.
Use `segment_objects(image_id, objects)` when the server has it: give each object a `label` and a rough
`box` (x, y, width, height; loose is fine, it only has to contain the object), a `point` on it, or both, and
Segment Anything traces the exact edges and saves polygons. Give a box and a point together for a band
(e.g. the stratum corneum), a structure between others (e.g. a dermal papilla) or one at the image's edge:
the point says which thing in the box is meant. Don't box thin, curved structures that wrap around others
(e.g. rete ridges): mark them with labelled pins instead. Use `model: "medsam"` for medical images
(CT, MRI, X-ray, ultrasound, endoscopy, pathology), with a box for every object. Check `failed` in the
result, and report the scores: an outline can be precise but of the wrong object if the box was off.
When an image has many similar objects (glands, crypts, cells, vessels), or boxes are hard to place, call
`find_regions(image_id)` first: it outlines and numbers the objects it finds by itself and returns each
one's exact box. Choose the numbers that are the objects asked for (for a region inside another, such as
a gland's lumen inside the gland, choose the whole object) and pass their boxes unchanged to
`segment_objects`. Box any object it missed yourself.

### Histopathology (H&E images)
- `check_image_quality(image_id)` first when the image will be analysed: report its warnings (blur,
  little tissue, pen marks, faint staining) before trusting any result.
- Call `warm_up("nuclei")` early: the first run after a quiet spell takes up to a minute.
- `detect_nuclei(image_id)` outlines every nucleus automatically; no boxes needed. Pass
  `microns_per_pixel` when the scanner resolution is known (often 0.25 at 40x, 0.5 at 20x) to get
  `median_area_um2` and `per_mm2`. Report the count,
  `median_area`, `area_variation` (higher means more variable nuclear size) and the number of enlarged
  nuclei. These are measurements, not a diagnosis. It works on H&E stains only.
- `classify_cells(image_id)` (0.6.0+) after `detect_nuclei` types the nuclei (tumour, immune, connective
  tissue, dead, normal epithelial) and gives percentages and the immune-to-tumour ratio. Say it is for
  research and education only, and that types are model estimates, not a diagnosis.
- `normalize_stain(image_id)` saves a colour-standardised copy as a new image (report its new id); use it
  for pale or unusually coloured slides, or before comparing slides from different labs.
- `export_annotations(image_id, "qupath")` gives GeoJSON for QuPath.
- Whole slides (.svs, .ndpi, pyramidal .tif; account only): `upload_slide` / `upload_slide_from_url`
  (0.5.0+) start a background analysis; `analyze_slide` waits for it and `get_slide_analysis` reads it.
  `coverage: "sample"` (default) analyses a few dozen tiles spread over the tissue, with cell types;
  `coverage: "full"` (0.7.0+) analyses every tissue tile in parallel and tints the overview as a density
  heatmap. Report the slide-level nuclei per mm², median area in µm², size variation and enlarged nuclei,
  which tiles were densest (their images are saved separately for a closer look), and the QuPath GeoJSON
  link. For a sample, say the tiles are a sample of the tissue, not all of it.
- For a dataset of many images, `export_dataset(format, category=... or image_ids=[...])` (0.4.0+) gives
  one class list across all of them, so the merge script below is only needed for older servers.

### Add annotations
Use `add_annotations(image_id, [...])` for pins, arrows and shapes the user specifies, or when
`segment_objects` isn't available. It keeps existing annotations and returns `addedIds`.
- Send all annotations for one image in a single call.
- When you place shapes from your own view of the image (not coordinates the user or another
  tool gave you), set `confidence: "low"` or `"medium"`, say that the shapes are approximate,
  and ask the user to review them in the web app. Never present estimated boundaries as precise.
- Reuse the exact label strings already used in the dataset. Check with `list_images` +
  `get_image` before inventing a new class name.

### Clean up
1. Audit: for the images in scope, collect every label with its count, and flag:
   - near-duplicate labels (case, spacing, plurals, typos, synonyms such as `Tumor` / `tumour`)
   - polygons with fewer than 3 distinct points or zero area, and circles with radius 0
   - coordinates outside the image, and exact duplicate shapes
   - rectangles / pins / arrows that look like they were meant as training labels
2. Propose a plan (label mapping, shapes to fix, convert or remove) and **wait for the user's
   confirmation** before changing anything.
3. Apply it:
   - deleting only: `remove_annotations(image_id, ids)`
   - renaming labels, converting rectangles to polygons, clipping coordinates:
     `replace_annotations` with the **complete** corrected list. Start from `get_image`'s
     annotations and carry over every field (`type`, `label`, coordinates, `color`, `notes`,
     `confidence`). Anything you leave out is lost. Annotation ids and `createdAt` are
     regenerated; mention that if the user tracks ids.
4. Call `get_image` again and report the before → after counts.

### Share
`share_image(image_id)` (0.7.3+) returns a 7-day link that opens the image with its annotations in the
Image Label web app, where anyone can edit and export their own copy without an account. Anyone with the
link can see that image: share it only with people who may.

### Export a dataset
`export_annotations(image_id, format)` exports **one image**, and numbers classes by first
appearance **in that image**. Class ids and COCO category ids therefore differ between images.
Never concatenate per-image exports by hand.

1. Optionally fix the class order with the user (for example to match an existing model).
2. For each image, call `export_annotations` and save the raw tool result to a JSON file:
   - COCO: any file name (`file_name` is inside the export)
   - YOLO: name it after the image file's stem, so `scan_01.png` → `scan_01.json`
3. Merge with the bundled script:
   ```bash
   python scripts/merge_exports.py coco exports/*.json -o dataset/annotations.json
   python scripts/merge_exports.py yolo exports/*.json -o dataset --classes "tumor,stroma"
   ```
   `--classes` pins the order; labels it doesn't list are appended. For YOLO it writes
   `labels/<stem>.txt`, `classes.txt` and `data.yaml`. Copy the image files into
   `dataset/images/` yourself (download them from the `get_image` viewing URLs if needed).
4. Report the image, annotation and class counts, and how many annotations were skipped for
   being non-exportable types.

YOLO output is **detection** format (`class xc yc w h`, normalized). For segmentation masks use
COCO (`segmentation` polygons).

## Rules

- `replace_annotations` overwrites everything on an image. Show what will change and get
  confirmation first. Prefer `add_annotations` / `remove_annotations` when they're enough.
- There is no tool for deleting images, on purpose. If asked, explain that it has to be done
  in the web app.
- Batch per image, and don't loop over hundreds of images without telling the user the scope.
- Tool errors read `METHOD /path failed (HTTP status): message`. Report the message. Validation
  errors (for example `polygon needs at least 3 points`) mean fixing the input, not retrying it.
