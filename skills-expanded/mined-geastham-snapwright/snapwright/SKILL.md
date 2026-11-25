---
name: snapwright
description: Design buildable brick models (the interlocking stud-and-tube kind) from a photo, sketch or description, verify in software that every part really connects, and produce a step-by-step instruction book (PDF), an interactive 3D build viewer, LDraw files and BrickLink/Rebrickable parts lists. Use this skill whenever someone wants to turn an image, character, object, building, pet, logo of their own, or idea into a brick build, brick sculpture or brick mosaic; asks for building instructions, a parts list or a BOM for a brick model; wants a brick design or its build log fixed (floating parts, separate structures, tipping over, weak joints); mentions MOCs, BrickLink, Rebrickable, LDraw or Studio files; or wants a buildable toy-brick version of anything, even if they don't say "skill" or name a file format.
---

# Snapwright

Turn an idea into a brick model someone can actually build: shape, real parts, checks, steps, book.

The pipeline is deterministic Python in `scripts/`. Your job is the part code can't do: read
the reference, choose scale and palette, write the design file, look at previews, fix what
looks wrong, and interpret the checks.

## Guided creations (the wizard)

When the user starts a new creation from pictures, asks "how do I start?", or wants the
likeness to matter, walk them through `references/wizard.md`, stage by stage:
1. three kickoff questions;
2. `sw.py new` for a project folder;
3. `sw.py refs` to check the reference images and write prompts for any missing views;
4. the brief;
5. block-out and likeness;
6. build;
7. hand-over.

Show something at every stage and ask at most one question. For quick one-line requests,
use sensible defaults and go straight to the design.

## 0. Before designing: subject and IP

Build original subjects, the user's own creations, generic things (animals, buildings,
vehicles, objects, landscapes), real places, or public-domain works. If asked to recreate a
known character, mascot, logo or commercial set someone else owns, say so in one sentence and
offer an original design in a similar spirit instead. Never put a toy-brick manufacturer's
brand name in a model title, file name or book. Read `references/ip-and-naming.md` if the
user wants to sell or publish designs.

## 1. Intake (ask at most one short question; otherwise pick sensible defaults and say so)

Settle: subject and reference, target size (cm) or part budget, audience (kids / family /
adult / expert, which sets parts per step), finish (smooth tiled tops or studs), and outputs
wanted. Defaults: 20-35 cm tall display model, adult, tiled finish, all outputs.
Rules of thumb: 1 stud = 8 mm, 1 plate = 3.2 mm, 1 brick = 3 plates. Solid sculptures cost
roughly 1 part per 5-6 voxels; hollow shells far less. For a part budget ("under 400
pieces"), round outlines and thin 1-stud rails cost the most parts: prefer octagons and
squares, and make section heights multiples of 3 plates (whole bricks).

## 2. Design file

Write `design.py` with the DSL in `references/design-dsl.md`. Block out big masses first,
then detail, then paint colours. Keep it an honest likeness at the chosen resolution: pick a
scale where the features that make the subject recognisable are at least 2 studs wide.
For solid masses wider than ~12 studs, finish the design with `model.hollow()` (keeps a
2-stud shell, 3-plate caps and internal bracing columns; saves plastic and weight) or build
shells directly with `inner=`/`inner_r=`. Use only catalog colours (`assets/catalog.json`);
prefer `core` tier. Tapers, domes and flares don't need special handling: the build smooths
them with slopes, inverted slopes and round parts automatically.

```bash
python <skill>/scripts/sw.py preview design.py --out out/preview
```
Look at all four `preview_view*.png` next to the reference. If preview prints a
`warning: ... voxels ... don't touch the rest of the model or the ground`, join that part
to the model now: nothing can hold it up and the build will fail.

When there is a reference picture, measure the likeness instead of eyeballing it:

```bash
python <skill>/scripts/sw.py compare design.py --ref photo.jpg --out out/compare
```

It finds the camera angle where the model best matches the picture (azimuth 0 = the model's
+z face, so design subjects facing +z), prints the silhouette IoU, colour agreement and
concrete hints ("40-50% down from the top: the model is 20% too narrow"), and writes
`compare.png` (reference, model at that view, overlap). Look at the PNG, apply the hints,
re-run. Iterate until IoU >= 0.8 and the features that make the subject recognisable are at
least 2 studs wide (compare and preview list 1-stud colour details). Usually 2-5 rounds.
Details, including busy backgrounds (`--mask`), in `references/likeness.md`.

If the user has a 3-D model (.obj, .stl, .glb), start from it:
`model = Model.from_mesh("thing.glb", height_cm=25)` (`up="z"` for Z-up files) then refine as
usual: STL has no colours, so `paint` them (e.g. fins and nose). Parts thinner than a stud
(fins, flags) come out 1-2 studs thick and joined to the body; check them in the preview.

## 3. Build and check

```bash
python <skill>/scripts/sw.py build design.py --out out --audience adult --seeds 8
```
Exit code 0 = checks passed and the book was written; 2 = failures (book skipped unless
`--no-strict`). By default the build shapes visible tapers and curves with slopes and round
parts (`--no-shapes` for bricks, plates and tiles only) and stands a model that would tip
over on a 2-plate base (`--base off` to keep the failure and fix the design yourself). Read the `summary` block at the end of the log: it is exactly what the book
finale and the viewer will say. For every FAIL or note, apply the matching fix from
`references/geometry-and-checks.md` (usually a design change: join a floating part, add
support under an overhang, thicken a weak point, widen a 1-stud feature, simplify a colour
speckle), then rebuild. Never present a model with floating parts, multiple structures,
large trims or a centre of mass under 3 mm inside the footprint as buildable.

Report honestly, from the summary: every auto-repair (cells recoloured, overhang cells
trimmed, tops that got studded plates instead of tiles, an added base), the surface shaping
(slopes and rounds change the silhouette slightly), weak points (pieces held by 3 studs or
fewer), single-stud joints, and the part-colour availability line as written (the catalog is
verified against Rebrickable's set inventories; only call combos verified if the summary
says so).
Everything is "checked in software"; nobody has built it until someone builds it.
Builds are deterministic: the same design file and seeds give the same model. Add
`--profile` to see where time goes on big models (a 5,000-part model takes ~2 minutes).

## 4. Outputs (all in `out/`)

- `<slug>-instructions.pdf`: cover, parts inventory, bags of ~150 parts each with a parts page,
  numbered steps and sub-steps with named-colour callouts, progress bar, finale
- `<slug>-viewer.html`: self-contained 3D viewer: build playback, step-by-step (arrow keys)
  with new parts highlighted, exploded panels, record to video, parts list, checks
  (`?step=N` opens paused at step N; `&explode=1` pulls panels out). three.js is embedded, so
  it opens offline and from an attachment; `sw.py viewer model.json --out f.html --cdn` writes
  a smaller copy that loads three.js from a CDN (for hosting on a website)
- `<slug>.ldr`: LDraw with STEP markers (opens in LeoCAD, Studio, Mecabricks)
- on request, a build video (the model assembling itself, then its other sides):
  `sw.py video out/model.json --out out/build.mp4 [--size 1080x1350] [--seconds 24]`; MP4 needs
  ffmpeg (else an animated WebP); ~0.3 s per frame for a 3,000-part model
- `<slug>-bricklink.xml`: the order list. On BrickLink: Want -> Upload, then *Buy All*
  to find shops that have everything.
- `<slug>-rebrickable.csv`: import on Rebrickable as a part list.
- `<slug>-parts.csv`: a readable list with a BrickLink link per part and colour.
- `model.json`: canonical model (schema in `references/geometry-and-checks.md`)

Share the PDF and the viewer first. Give the headline numbers (parts, height, steps, lots),
anything the user should know before buying parts, and one concrete next improvement.

### Build it by hand in the browser (Handbuild)

[Handbuild](https://snapwright.eastham.ai) is a web player for Snapwright models: the user holds
their hands up to a webcam and pinches each part into place, step by step from the book (mouse
and touch work too). After a build PASSes, offer it in one line, and when the user says yes or
asks to "open it in Handbuild", "play it" or "build it with my hands":

- **With the `gh` CLI signed in** (`gh auth status` succeeds): the link needs the model online,
  so say first that this uploads `model.json` as a secret GitHub gist on their account, which
  anyone with the link can open, and go ahead only if they agree. Then:

  ```bash
  gh gist create out/model.json --desc "Snapwright model: <title>"
  ```

  It prints `https://gist.github.com/<user>/<id>`. Give the user
  `https://snapwright.eastham.ai/?gist=<id>` (add `&input=camera` to skip the start screen).
  After a rebuild, update the same gist rather than making a new one, so the link keeps working:
  `gh gist edit <id> -f model.json out/model.json`.
- **Without `gh`, or with no network (the claude.ai sandbox):** don't upload anything. Tell the
  user to open https://snapwright.eastham.ai, choose "Open your own build" and pick
  `out/model.json` (or drag it onto the page). The file stays on their computer.

Never upload a model the user asked to keep private, and don't install or sign in to `gh` for them.

## 5. Sideways panels (faces, signs, chest plates)

When a flat face of the model carries a picture that needs finer vertical detail or a smooth
upright finish (a face, a sign, a screen), build it as a sideways panel: it is built flat and
clipped onto side-stud bricks, so its pixels are a stud tall instead of a plate.

```python
face = model.panel("Face", face="+z", at=4, width=8, height=6)   # carves its space
face.box(0, 0, 0, 8, 6, 1, "black")      # panel coords: x across, z rows DOWN, y layers out
face.box(0, 0, 1, 8, 6, 2, "white")      # outer layer (tiles)
face.box(1, 1, 1, 3, 3, 2, "black")      # left eye
```

Give `top=` (the plate line of its top edge) so the panel lands on the surface across its own
rows, not a part sticking out lower down; pass `plane=` if that surface steps.
The model must be solid right behind the panel (anchor rows every 2 studs); `face.mosaic(img)`
reads upright from the front. Use even heights. The build checks each panel on its own (one
piece, every part held, at least 2 side studs), shows it in a boxed "sub-build" in the book
with an attach step, and animates the attach in the viewer. Details in
`references/design-dsl.md`.

For a face that must sit at an angle (a ring's face, a dashboard), use
`model.hinged_panel(...)`: built flat, clicked on with locking hinges at a multiple of 22.5
degrees. Its top layer can take curved tiles placed by hand (`face.place("27507", x, z,
"black", rot=k)`: macaroni, quarter and round tiles) for true circles and arcs, which the voxel
grid can't make. See "Hinged panels and curved tiles" in `references/design-dsl.md`.

## 6. Photos to mosaics

For "make a mosaic of this photo": `model = Model(48, 48, 3)` then
`model.mosaic("photo.jpg", mode="flat")`: two staggered base plate layers hold it together
and the picture is a layer of tiles on top (the grid grows if it is too short). Crop the
photo to the mosaic's aspect first. Default colours are every opaque colour made as a 1x1
tile and plate; pass `colors=` for a graphic look. Features thinner than a pixel (a sun's
reflection, a horizon line) blur into mud: `paint` them back over the mosaic. Or
`mode="upright"` with a height in plates of roughly width x 2.5 for correct aspect.

## Files

- `scripts/sw.py`: CLI (new, refs, preview, compare, build, viewer, book, video, sync-catalog)
- `scripts/snapwright/`: dsl, brickify, validate, steps, render, book, exporters, pipeline
- `assets/catalog.json`: parts and colours; `assets/viewer_template.html`
- `references/wizard.md`: the guided creation flow, stage by stage, with checkpoints
- `references/design-dsl.md`: every DSL call with examples. Read before writing a design.
- `references/likeness.md`: compare, reading its hints, masks, meshes
- `references/geometry-and-checks.md`: units, connection rules, repairs, each check and its fix,
  model.json schema
- `references/book-style.md`: book conventions and what to avoid imitating
- `references/ip-and-naming.md`: subject choice, trademarks, disclaimers, selling designs
