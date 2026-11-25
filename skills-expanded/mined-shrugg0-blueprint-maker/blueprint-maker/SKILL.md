---
name: "blueprint-maker"
description: Turns a 3D model (GLB/glTF/OBJ/STL/PLY/OFF) or any 2D image (photo, render, drawing, logo) into a technical blueprint sheet or desktop wallpaper - blue/graphite/paper style with hidden-line views, dimension lines, numbered callouts, title block, description, spec table and design remarks. Use this whenever the user asks for a blueprint, technical drawing, "tavola tecnica", "progetto tecnico", schematic, engineering-style sheet, cutaway-style poster or technical wallpaper of ANY object, vehicle, creature, character, building, product or image - even if they only say "make it look like a technical drawing" or "sfondo stile blueprint". Also use it when they upload a .glb/.gltf/.obj/.stl and want it as a drawing, or an image and want it as line art with dimensions and callouts.
---

# Blueprint Maker

Generates a finished blueprint-style sheet (PNG, default 1920x1080) from either:

- **a 3D model** -> real hidden-line orthographic views: a large 3/4 view plus side, top and front views with measured dimension lines (3D pipeline), or
- **a 2D image** -> line extraction with silhouette outline, bounding-box dimensions and callouts (2D pipeline).

Both pipelines share one layout engine (frame, panels, title block, text fitting) so the result looks the same.

## What it can and cannot do (say this to the user when relevant)

- **No file, no blueprint.** An object described only in words cannot be turned into an accurate drawing. Ask for a 3D model or an image. Do not invent geometry.
- **3D gives real orthographic views; 2D cannot.** A single photo has one viewpoint, so the 2D pipeline produces one line-art view, not front/side/top.
- **Line quality depends on the mesh/image.** Game-extracted meshes with hundreds of thousands of triangles give dense lines; it is a good automatic base, not hand-made illustration quality.
- **Scale is unknown unless the user gives it.** Dimensions are in model units (`u`) or pixels (`px`) unless a `scale_ref` (a real measurement) is supplied. Never present a guessed real-world size as fact.
- **Fonts:** bundled text rendering uses DejaVu (Latin, Greek, Cyrillic). CJK/Arabic/Hebrew text will not render correctly.
- **Layout is designed for 16:9** (tested 1920x1080, 2560x1440, and 1920x1200). Other aspect ratios stretch the panel layout; check the output.
- **Ripped game/film assets are someone's IP.** Fine for a personal wallpaper; mention not to redistribute.

## Step 0 - Gather inputs (ask once, only what is missing)

1. The file (model or image).
2. Name of the object, and a description - or offer to draft it. **The description must match what is actually in the render** (look at it first). A description of a wheeled vehicle on a four-legged creature destroys the credibility of the sheet; if the user's text does not match the geometry, say so and rewrite it.
3. Output resolution and the **top safe zone** if it is a wallpaper (a desktop bar covers the top). Default `top_safe` = 76 (frame starts 76 px down at 1080p, room for a bar of ~1 cm on a laptop). If the user gives centimetres, convert: px_per_cm = screen_width_px / screen_width_cm (about 36 px/cm on a 24" 1080p monitor, about 56 px/cm on a 15.6" laptop). Use bar height in px + ~12.
4. Style: `blueprint` (default, blue), `graphite` (dark with orange lines), `paper` (light, printable).
5. Language of the text (default English; write the spec text in that language).

Do not interrogate the user: if they already gave enough, proceed with defaults and state your assumptions.

## Step 1 - Setup

```bash
pip install trimesh numpy scipy networkx pillow opencv-python-headless matplotlib --break-system-packages -q
# optional, only for meshes > 700k faces: pip install fast-simplification --break-system-packages
```

All scripts live in `scripts/` next to this file. Replace `SKILL_DIR` with the skill folder.

## Step 2A - 3D model

### Inspect (always do this first - one image, one command)

```bash
python3 SKILL_DIR/scripts/blueprint3d.py inspect MODEL.glb --out /home/claude/insp
```

Open `inspect.png` with `view` (it is a single contact sheet) and read the printed text:

- **Top row** = raw axis projections: work out which raw axis is **up** and which way the object **faces**.
- **Bottom** = the 3/4 view with **numbered anchor candidates** (yellow). The console lists each `cand N` with its pixel and canonical position. The faint grid is in 1500x860 reference pixels (usable as `pick`).

Orientation flags (canonical frame: +y up, object front toward -x):
`--up +Y` (default for GLB/glTF; `+Z` for other formats) and `--front -X|+X|+Z|-Z|...`. The printed hint names the longest horizontal axis; the front must be at the LEFT of the side view, so flip the sign if the head/front is on the other side. If the orientation was wrong, re-run `inspect` once with other values. Put the final values in the spec as `"up"` and `"front"`.

`inspect` also takes `--az`, `--el` (default 58 / 20) and `--k` (number of candidates, default 16). **Use the same `view` az/el in the spec**, otherwise candidate numbers will not match.

### Write the spec

Create `spec.json` (schema below, working example in `assets/example_spec_3d.json`). For each callout give a title, a short description and **one** anchor:

- `"cand": N` - a numbered candidate from `inspect.png` (cheapest: no pixel guessing). Candidates are spread over the visible surface, so check that the dot really lands on the part you name; if no candidate is close enough, use `pick`.
- `"pick": [px, py]` - pixel in the 1500x860 reference view (the grid in `inspect.png`)
- `"extreme": "+x" | "-x" | "+y" | "-y" | "+z" | "-z"` - extreme point in the canonical frame (front is `-x`; may be hidden behind geometry)
- `"point": [x, y, z]` - exact canonical coordinates

**Do not set `"label"`** unless you need to: label positions are then chosen automatically (text kept off the model silhouette and off other labels, tidy columns at the panel sides, short non-crossing leaders). `"label": [x, y]` (1920x1080 reference coords, main panel x 40-1290, y 96-826) forces a manual position and is checked by the audit below.

### Build

```bash
python3 SKILL_DIR/scripts/blueprint3d.py build MODEL.glb spec.json --out /mnt/user-data/outputs/blueprint.png
```

The painted views are cached on disk (`~/.cache/blueprint-maker`, or `$BP_CACHE`), keyed by model + view + style. Changing text, labels, callouts or palette-independent content rebuilds in about 2 s instead of re-painting; `--no-cache` or `"cache": false` disables it.

Layouts: `"layout": "multi"` (default: big 3/4 view + side/top/front + dimensions) or `"single"` (just the 3/4 view, wider).

### Spec lock (binding between spec and model)

Anchors written as `cand`, `pick` or `extreme` only mean something for the model, orientation and view they were chosen on. The first build writes `<spec>.lock.json` next to the spec: the 3D point each anchor resolved to, a geometric fingerprint of the model, and the settings that influence anchors (`up`, `front`, view az/el, `candidates`, `max_faces`). Every later build re-resolves the anchors and compares:

- anchors moved (different model, orientation or view) -> **build fails** with `error: spec is not bound to this model ...`, naming each callout and what changed. Re-run `inspect` with the spec's settings, re-pick the anchors, then build with `--relock` (or restore the original model/settings);
- model differs but every anchor still lands on the same place (e.g. a lossless re-export) -> `WARNING: binding: ...`; check, then `--relock`;
- you edited an anchor on purpose (same model/settings) -> the lock entry is updated silently.

`--no-lock` skips the check (not recommended). Keep the lock file with the spec (commit it). Never "fix" a binding error by ignoring it: the labels would point at the wrong parts.

## Step 2B - 2D image

```bash
python3 SKILL_DIR/scripts/blueprint2d.py inspect IMAGE.png --out /home/claude/insp
```

Read the printed mask coverage (background removal works for flat backgrounds or transparent PNGs; otherwise it reports "none"), then `view` `inspect.png`: left = the source with a grid labelled in **source pixels** (for `point_px`), right = what the line extractor sees. Callout labels are placed automatically here too (leave out `"label"`).

Write `spec.json` (see `assets/example_spec_2d.json`) and build:

```bash
python3 SKILL_DIR/scripts/blueprint2d.py build IMAGE.png spec.json --out /mnt/user-data/outputs/blueprint.png
```

Tuning: `"detail"` 0.3 (clean, bold) to 0.8 (busy); `"mode": "edges"` (Canny, photos/renders) or `"sketch"` (XDoG, soft/low-contrast art); `"bg": "none"` to keep the whole frame, or `"mask": "path.png"` for a hand-made silhouette; `"crop": [x0,y0,x1,y1]` to isolate the subject; `"fill"` 0-1 for the translucent body tint.

## Step 3 - Check the result (do not skip, but keep it cheap)

The builder prints `WARNING:` lines. **Read them first** - they are an automatic audit, so you usually need to `view` the PNG only once, at the end:

- `error: spec is not bound to this model` - see "Spec lock" above; this is a hard failure, not a warning.
- `layout: ...` - callout text overlapping the model, two labels overlapping, a leader crossing another label's text / another leader / its own text, text outside the panel, text on the axis triad. Fix by removing the manual `"label"` (let the placer decide), changing the anchor, or shortening the text.
- `description / specs / notes: shrunk to Npx` or `does NOT fit` - shorten the text or drop rows rather than accepting unreadable text.

Then `view` the final PNG once and verify what the audit cannot know:

1. Model upright and facing the intended way in all views; dimensions plausible.
2. Each callout dot really lands on the part its text names.
3. The top safe zone is empty (wallpaper use).

If something is wrong, edit the spec (anchors, `view.az`/`view.el`, text length, `feature_deg`) and rebuild; with the cache this takes seconds. Typical total: 1 inspect + 1-2 builds, 2-3 image views.

## Step 4 - Deliver

Save under `/mnt/user-data/outputs/`, call `present_files`, then reply briefly. In the reply, always state:

- which texts you **invented** (descriptions, specs, remarks, callout functions) versus what is measured from the file - the user should replace invented technical claims they care about;
- the units/scale assumption;
- any `WARNING` or visible limitation (dense lines, hidden anchor, aspect ratio).

## Keeping token use low

- One `inspect` image, one final `view`; rely on the printed audit instead of re-viewing after each tweak.
- Use `cand` anchors and leave `label` out; do not hand-tune pixel coordinates.
- Write the spec once, completely (anchors, texts), then build; edit only the fields that the audit or the final view flagged.

## Writing the annotation text

- Describe only what is visible in the renders; keep functional claims plausible and generic. If the object is from a franchise, do not state lore details you are not sure about.
- Callout titles: 2-4 words. Callout text: one short sentence (about 70 characters). Notes: 3-5 short items. Description: about 600-700 characters. Spec rows: value under ~45 characters.
- Keep wording technical and consistent: designation, spec number, revision, units.

## Spec reference

Common keys (both pipelines):

| key | meaning | default |
|---|---|---|
| `title` | big title in the title block | "UNTITLED" |
| `subtitle` | line under the title | "" |
| `designation` | bold line at top of the description box | "" |
| `description` | paragraph for the description box | (box omitted) |
| `specs` | `[["Label","Value"], ...]` for the spec table | (omitted) |
| `notes` | list of strings for the remarks box (A, B, C...) | (omitted) |
| `notes_title` | heading of that box | "DESIGN REMARKS" / "NOTES" |
| `callouts` | list of callout objects (below) | none |
| `spec_no`, `class`, `rev`, `sheet`, `scale` | title-block fields (blank ones are skipped) | sheet "01 / 01", scale "AS SHOWN" |
| `fields` | full override of title-block fields: `[["KEY","value"], ...]` | auto |
| `width`, `height` | output size in px | 1920, 1080 |
| `top_safe` | y (at 1080p) where the frame starts; keep a desktop bar clear | 76 |
| `palette` | `blueprint`, `graphite`, `paper` | `blueprint` |
| `scale_ref` | `{"axis": "length|height|width" (3D) or "width|height" (2D), "value": 3.2, "unit": "m"}` to get real-world dimensions | model units / px |

3D-only: `up`, `front`, `layout` (`multi`/`single`), `view` `{"az": 58, "el": 20, "margin": 0.045}`, `candidates` (k used for `cand`, default 16; must equal inspect `--k`), `feature_deg` (edge angle threshold, default 38; raise to 50-60 for fewer lines), `feature_deg_small` (default 44, side/top/front views), `max_faces` (default 700000), `cache` (default true).

2D-only: `mode`, `detail`, `bg`, `mask`, `crop`, `fill`, `fit_subject` (crop to the subject, default true), `view_title`, `view_sub`.

Callout object: `{"title": "...", "desc": "..."}` plus the anchor - 3D: `cand` / `pick` / `extreme` / `point`; 2D: `point_px: [x, y]` in source-image pixels - and optionally `"label": [x, y]` to force a manual position.

## Troubleshooting

- **Model sideways / upside down / facing away:** re-run `inspect` with `--up` / `--front`; check the top row of `inspect.png`.
- **Just a grey blob of lines:** raise `feature_deg` (50-65); for a very dense mesh also set `max_faces` lower (needs `fast-simplification`).
- **Parts missing or see-through holes:** the mesh is not watertight or has inverted faces; the painter's-algorithm renderer tolerates that, but internal parts of game assets can show through. Lower `view.margin`, or try a different `az`.
- **Very slow:** meshes above ~700k faces are decimated automatically if `fast-simplification` is installed; otherwise a build can take minutes.
- **2D mask is wrong or fragmented:** subject colour is too close to the background. Use `"bg": "none"`, a `crop`, or provide a `mask` PNG (white = subject).
- **Text warnings:** shorten text; do not lower font sizes by hand.
- **Candidate numbers do not match the picture / `spec is not bound to this model`:** the model file, `up`/`front`, the spec `view` az/el or `candidates` differ from the ones the spec was written for. Re-run `inspect` with the spec's settings, re-pick the anchors, build with `--relock`.
- **Auto label placement keeps failing ("no collision-free position"):** too many or too long callouts for the panel; shorten the descriptions, drop callouts, or use `"layout": "single"` for a wider panel.
- **Stale-looking output after editing the scripts:** the cache key includes the renderer code, but if in doubt run once with `--no-cache`.

## Files

- `scripts/binding.py` - spec lockfile (fingerprint + anchor drift check)
- `assets/demo/` - procedural demo rover (GLB) + demo image, regenerated by `make_demo_assets.py` (no third-party assets)
- `tests/test_binding.py` - run `python3 tests/test_binding.py`
- `docs/examples/` - sample output images

- `scripts/blueprint3d.py` - 3D CLI (`inspect`, `build`)
- `scripts/blueprint2d.py` - 2D CLI (`inspect`, `build`)
- `scripts/hlr.py` - hidden-line mesh renderer (orientation remap, edges, painter's algorithm, render cache)
- `scripts/bp_common.py` - drawing primitives, layout, text fitting, palettes, label placement and audit
- `assets/example_spec_3d.json`, `assets/example_spec_2d.json` - working example specs
