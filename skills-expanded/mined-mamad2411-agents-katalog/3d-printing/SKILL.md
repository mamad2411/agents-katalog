---
name: 3d-printing
description: >-
  Complete 3D pipeline for Bambu Lab printers; the only skill for 3D work. Use for any .stl
  or .3mf file, or to scale, resize, recolor, change filament colors, mirror, rotate, split,
  merge, repair, measure, or add/resize magnet holes - even if the format isn't named. Also
  designing printable parts (bins, organizers, brackets, mounts, gridfinity), build123d CAD,
  MakerWorld - browse models, find me a model - print prep and printing - slice, print, fit
  on one plate, multi-object plate, batch print night, check printer, what's printing, AMS -
  troubleshooting - stringing, warping, bed or layer adhesion, support removal, clogs,
  elephant foot, ringing, under-extrusion, this keeps happening - and the print log: log this
  print, what settings did I use, what worked for this filament, did I fix this before,
  filament usage. When scaling, holds hardware interfaces (Maker's Supply
  parts, MH011 movement, bearings, inserts) and magnet holes at original size while the body
  scales. Defaults to a Bambu Lab H2C with PETG.
---

# 3D Printing

Edit, design, prepare and print 3D files the way a careful machinist would:
measure first, confirm intent, protect functional interfaces, verify after.

This skill is one entry point for the whole loop: editing and designing files,
preparing and running prints, and keeping the print log that makes the second
attempt at anything cheap. Deliberately one skill rather than four — the paths
share too much context to split. The one thing it hands off is **cad-khana**,
for multi-part mechanical assemblies; see Designing new parts.

**For mesh work the local Python stack is the primary path.** For printing, the
`Bambu_Printer` MCP is, when it is live — it slices with a real `h2c` profile and
drives the printer. Other externals (OrcaSlicer CLI, OpenSCAD MCP, render server)
are useful when present and frequently absent, and the failure is silent until
you are deep into a job. Preflight decides the local paths; `ListConnectors`
decides the MCP ones. See `references/external_tools.md`.

## Step 0 — preflight, every run, before promising anything

```bash
python scripts/preflight.py
```

It reports which capabilities are live and prints the fallback for each that is
not. Run it before you tell the user what you are going to do, not after you
have failed to do it. It costs a second and it is the difference between
"here's your file" and "actually, I can't."

Non-negotiables it enforces:

- **Never fabricate a machine profile to make a slicer run.** If no profile for
  the user's printer exists, output a project 3MF instead (below).
- **Never route design work to the OpenSCAD MCP** unless `ListConnectors`
  shows it live. preflight checks for a local `openscad` binary, not the
  connector — MCP liveness is a `ListConnectors` question. Default to
  build123d and the bundled scripts.
- **Never guess `bambu_model` on a slice or print call.** Take it from Your
  setup below (shipped default: `"h2c"`). A wrong model drives a wrong machine
  profile, which is the fabricated-profile failure wearing a different hat.
- A missing capability is information, not a blocker. Every one has a fallback.

preflight cannot see MCP connectors. Run `ListConnectors` alongside it whenever
the job ends in a print — the `Bambu_Printer` MCP changes the whole output path.

## Your setup — EDIT THIS SECTION

**Everything in this block is a default you should change to match your own
printer and habits.** It is the only part of this skill that is
installation-specific; the rest is general. Values below are the shipped
defaults. Apply them without re-asking the user, and re-read them if a job
seems to contradict one.

```yaml
printer:    Bambu Lab H2C          # your model — drives build volume and the MCP's bambu_model
bambu_model: h2c                   # exact string for Bambu_Printer MCP calls (p1s|p1p|p2s|x1c|x1e|a1|a1mini|h2d|h2s|h2c)
nozzle:     0.4                     # mm — the nozzle you actually print with most
material:   Bambu PETG Basic        # default filament profile
slicer:     bambustudio             # bambustudio | orcaslicer
output:     3mf                     # what to hand back by default
```

- **Printer: Bambu Lab H2C.** Dual-nozzle; build volume ≈ 325×320×325 mm
  left-nozzle-only, ≈300×320×325 mm dual. Verify at
  https://bambulab.com/en/h2c/specs if a job pushes those limits. Multi-color is
  easy on this machine — never talk the user out of color work.
  *If you changed the printer above, look up its build volume before trusting
  any fit check in this skill.*
- **Material: Bambu PETG Basic**, with PEBA (flexible) as a secondary. Shrinkage
  is handled by the slicer profile — do NOT pre-scale for shrinkage.
- **Nozzle: 0.4 mm.** Default every profile and setting to it and offer it
  first. Use 0.6 only when the user says the 0.6 is installed, and then pass
  `nozzle_diameter: "0.6"` explicitly.
- **Slicer: Bambu Studio**, chosen over OrcaSlicer for native H2C support. On
  MCP calls pass `slicer_type: "bambustudio"`. Use OrcaSlicer only if it
  demonstrably carries a correct profile for the printer above.
- **Tuning: speed and quality together**, not one traded for the other. Don't
  offer a "fast or good" choice as though it were the only axis — reach for the
  settings that buy both, and log what worked.
- **Hardware: Bambu Maker's Supply mechanical parts** — clock movements (MH011),
  bearings, gearboxes, screws, inserts, springs, magnets. Any pocket, hole or
  boss mating with these is a **protected interface**. *Swap this line for
  whatever hardware ecosystem you build with; the protected-interface machinery
  works the same for any of them.*
- **Output: always deliver a 3MF**, ready to open in the slicer. STL too only if
  asked.

These four are not printer-specific — keep them whatever your setup:

- **When modifying a file the user uploaded, edit that file — do not deliver a
  differently-named copy.** Same filename, their project intact.
- **Never silently rescale magnet holes.** Report the measured size, identify
  the likely magnet, ask whether to keep (default) or change.
- Generated artifacts go to a working/temp directory, never `~/Downloads`
  unless the user asks for a one-off there.
- Never write printer serials, LAN IPs, access codes or account tokens into any
  file in this skill. See Privacy.

## Environment setup (once per session)

```bash
pip install trimesh numpy scipy networkx lxml manifold3d shapely rtree --break-system-packages
```

`manifold3d` powers booleans; `rtree` is required for `section().polygons_full`
(cavity detection) and its absence shows up as a confusing `ModuleNotFoundError`
deep inside trimesh. If PyPI is blocked entirely, `scripts/stl_fallback.py` is
numpy + stdlib only and covers inspection, protected scaling and STL→3MF.

## Routing

```text
User wants something 3D
├── Has an STL/3MF to change?         → Core workflow, then Color changes /
│                                      Other common edits (below)
├── Scaling a model with hardware?    → Protected scaling — the signature move
├── Wants a new part designed?        → Designing new parts
│   ├── Multi-part assembly that
│   │   must fit together?            → hand off to cad-khana
│   ├── Single parametric part        → build123d (+ render server if up)
│   ├── Gridfinity                    → scripts/gridfinity_gen.py
│   └── Organic / sculpted            → MakerWorld instead
├── Wants to find an existing model?  → references/makerworld.md
├── Ready to print?                   → Print preparation and output
│   ├── Bambu MCP live?               → slice + print (printer_control.md)
│   ├── Not live?                     → project 3MF (print_prep.md)
│   ├── More than one part?           → references/plate_arrangement.md
│   └── Multi-plate 3MF handed in?    → identical-plate check, then stack if
│                                      eligible (plate_arrangement.md)
├── Asking about the printer / AMS?   → references/printer_control.md
├── "Print night" / batch session?    → references/plate_arrangement.md
├── Print finished, or went badly?    → Print log and troubleshooting
└── Settings question / recurring     → printlog.py FIRST, then
    problem?                            references/troubleshooting.md
```

## Core workflow

Every job: **measure → plan → confirm → edit → verify → deliver.**

1. **Inspect.** `scripts/mesh_info.py <file>` on every input. Note dimensions,
   watertightness, object count, colors, units. STL has no units — assume mm but
   sanity-check.
2. **Detect functional features** whenever an edit could move or resize
   geometry: `scripts/detect_features.py <file>`. The original model was
   designed around real hardware, so **the mesh is the ground truth** — trust
   measured sizes over catalog guesses.
3. **Confirm the plan** with AskUserQuestion when there is a real decision:
   which holes are hardware vs. cosmetic, keep-or-change magnet size, how to
   handle leftover space, what bin mix. Skip only for trivial unambiguous edits.
4. **Edit** with the bundled scripts or short custom trimesh/build123d code.
5. **Verify numerically.** Re-run mesh_info and detect_features on the output.
   Protected holes within ±0.02 mm, watertight, fits the build volume, paint
   intact if it should be.
6. **Deliver** the 3MF with a short summary of measured before/after numbers.

**Renders are a sanity check, not evidence.** Matplotlib and the bundled render
server both z-sort imperfectly; a base that looks detached in a render is
usually a depth-sort artifact. Confirm with cross-sections and
`is_watertight`/`body_count` before believing a render or acting on one.

## Scaling with protected interfaces (the signature move)

"Scale this up 150%" on a model with a clock-movement pocket and magnet holes
means: scale the *body*, keep the *interfaces*.

```bash
python scripts/smart_scale.py input.stl output.3mf --scale 1.5 \
  --protect "cyl:cx,cy,cz,ax,ay,az,diameter,depth,through|blind" [...]
```

- Run detect_features.py first; propose the protected set. Holes matching known
  hardware/magnets are protected by default; decorative holes scale.
- `--mode recut` (default, needs manifold3d): plugs, scales, re-cuts at original
  diameter and depth. Robust at any scale factor. Changes topology → destroys
  paint; warn first.
- `--mode project`: scales then projects hole walls back to original radius and
  compresses blind pockets to original depth. Preserves topology and therefore
  paint. Best for modest factors and plain cylinders.
- Blind-hole depth is preserved in both modes — a magnet doesn't get thicker
  when the model grows. Through-holes stay through.
- Bosses that fit *into* hardware use `boss:` instead of `cyl:`.
- Sanity-check before committing: ≥1.5 mm wall around each preserved hole for
  PETG; no preserved holes now overlapping or breaching a face. If violated,
  tell the user instead of producing a broken model.

## Designing new parts

Three local paths, in preference order. OpenSCAD only if `ListConnectors` shows
the MCP live — otherwise it is not an option, not a fallback; its workflow is in
`references/external_tools.md`.

**0. Multi-part mechanical assemblies — hand off to `cad-khana`.** Anything
where parts must fit *each other* — hinges, snap-fits, sliders, clevis/pin
joints, boxes with lids, anything with a moving DOF — is that skill's job, not
this one's. It declares interference and clearance as assertions and re-checks
them from geometry on every run, which is a stronger guarantee than looking at a
render and deciding it seems fine. Route to it early; retrofitting assertions
onto a finished model wastes the pass. Come back here for print prep, plate
arrangement and printing.

**1. Parametric solids — build123d.** For single parts, and for geometry with no
fit relationship to assert. Headless build123d is the workhorse. When
the bundled render server is up you also get eyes: POST code, look at the PNG,
iterate. Read `references/build123d.md` for the cheatsheet, the server API and
the setup commands. preflight reports whether the server is running and where
build123d lives — it is often inside `server/.venv` rather than system python.
The server is optional; cross-sections verify geometry better than renders do.

**2. Gridfinity — `scripts/gridfinity_gen.py`**, spec-exact and self-verifying:

```bash
python scripts/gridfinity_gen.py fit --size 228.28x150.43        # cells that fit
python scripts/gridfinity_gen.py baseplate --size 228.28x150.43 --out bp.stl
python scripts/gridfinity_gen.py bin --cells 2x3 --units 15 --out bin.stl
```

Read `references/gridfinity.md` before changing any constant. Every generated
part is re-measured at the four profile heights and must read
35.60 / 37.20 / 37.20 / 41.50 mm.

**3. Existing model — MakerWorld.** Best for organic or sculpted shapes, and for
anything a community has already solved well. See `references/makerworld.md`.

Design constants for all paths: wall ≥1.2 mm (3 perimeters at 0.4 mm), 0.2 mm
clearance on friction fits, `$fn`/tessellation high enough that curves read
smooth, and match the original designer's measured clearance when remixing
rather than applying a nominal one.

Two thresholds worth stating in numbers rather than vibes, borrowed from
cad-khana's printability defaults:

- **Wall thickness.** The two numbers above and here are the same rule measured
  two ways: 1.2 mm is 3 × a 0.4 mm *nozzle*, 1.5 mm is 3 × a typical 0.4 mm
  *extrusion width*. Use **1.2 mm as the hard floor** and **1.5 mm as the
  working default** — below it, walls slice as one or two perimeters with no
  infill room and under-extrude into a single ribbon. On a 0.6 mm nozzle the
  default is ≈2.0 mm. Rigid load-bearing parts go **above** 1.5 mm, not at it.
- **Maximum overhang 45°** is the rule for PLA with good part cooling. Adjust by
  material and cooling, in both directions: ABS, or PETG printed **without a
  part fan**, wants 35–40°; ASA, well-cooled PLA, or a slicer with aggressive
  overhang modifiers can reach 50–55°. The H2C does have part cooling, so 45° is
  a fair starting point for PETG here — tighten it if a specific part shows
  droop, and don't loosen the threshold just to make a part pass. Design for the
  angle or plan supports.

**Bounded iteration.** Cap the repair loop at 3–5 attempts on the same failure,
feeding each failure into the next attempt rather than restarting. Past that,
stop and say what is stuck and why — two requirements trading off against each
other, a constraint that may be infeasible. A clean "stuck here because X" beats
a long thrash, and most people would rather be told than handed something that
almost works.

## Print preparation and output

Check `ListConnectors` first, then read the reference that matches what you
found. `references/plate_arrangement.md` applies either way when there is more
than one part.

- **`Bambu_Printer` MCP live** → `references/printer_control.md`. Slice with
  `slice_stl` (or `slice_with_template`), resolve filament from the live AMS
  rather than guessing, confirm with the user, print. `bambu_model: "h2c"` on
  every call, always. This is the good path — use it.
- **A local slicer with a real profile for this printer** → fine too, and rarer.
  See `references/external_tools.md` for the OrcaSlicer CLI and its env vars.
- **Neither** → `references/print_prep.md`. Do not slice, do not invent a
  profile. Add the geometry to the user's own project 3MF, which already carries
  their printer, filament and process settings, and let them press Slice.

```bash
python scripts/project_3mf.py add-part  --project p.3mf --object 8 \
    --mesh part.stl --print-scale --name "..." --out p.3mf
python scripts/project_3mf.py add-plate --project p.3mf \
    --mesh a.stl b.stl --extruder 6 --name "Bins" --out p.3mf
python scripts/project_3mf.py inspect --project p.3mf
```

- `add-part` fuses a body into an existing object as a second part — the
  original triangle list and its paint are untouched, and the slicer fuses
  parts anyway, so the print is identical to a boolean union without the loss.
- `add-plate` computes the plate-grid offset from the project's own bed size and
  shelf-packs the parts. Verify afterwards that everything is on-bed.
- Choose the plate pattern by the geometry, using the clearance values in the
  project's `project_settings.config` — not folklore. See
  `references/plate_arrangement.md`.
- Never read a profile's display color as the user's loaded filament. Call
  `get_printer_filaments` when the MCP is live; otherwise inherit the `extruder`
  of the object you are extending.

## Color changes

- **Plain color assignment**: `scripts/bambu_3mf.py set-color`.
- **Existing project 3MFs** carry paint and settings in `Metadata/`.
  Geometry-preserving edits (uniform scale, move, rotate) go through
  `scripts/bambu_3mf.py transform`, which edits vertices in place inside the XML
  and keeps everything else byte-identical — paint survives. Adding geometry
  goes through `project_3mf.py`. Topology-changing edits lose paint; warn first.
- Splitting one object into color regions with no existing paint: boolean-split
  into bodies, export as multi-object 3MF, one color each.
- Read `references/3mf_bambu_format.md` before hand-editing any 3MF XML.

## Other common edits

- **Resize magnet holes** (D6×3 → D8×3): boolean-cut the new cylinder; if
  shrinking, plug then re-cut. 0.1–0.2 mm diameter clearance for press-fit PETG
  unless the original's measured clearance says otherwise.
- **Add magnet holes**: confirm position, size and depth; keep ≥0.8 mm floor
  between magnet and outer surface if it should be hidden.
- **Mirror / rotate / translate / split / merge / repair**: standard trimesh;
  always re-verify watertightness after booleans.
- **Cut for build plate**: if a scaled model exceeds the H2C volume, offer to
  section it with alignment features (dowels or the user's magnets).

## Print log and troubleshooting

Print troubleshooting is only cheap the second time. The first time PETG lifts
off the bed you spend an evening on it; the fifth time should take thirty
seconds — but only if the first four were written down. `scripts/printlog.py`
keeps that record, and the point is to *use* it.

### Retrieve before you advise

**Check the log before answering any settings or troubleshooting question.**

```bash
python scripts/printlog.py settings --material PETG --nozzle 0.4
python scripts/printlog.py issues --issue bed-adhesion
python scripts/printlog.py list --material PETG --result fail
python scripts/printlog.py show <id>
python scripts/printlog.py stats
python scripts/printlog.py report -o print-report.md
```

- `settings` reports what the prints that actually *succeeded* used, and — the
  part that matters — flags which values were consistent across them versus
  which varied. A consistent value is a finding; a varying one means that knob
  probably wasn't what mattered.
- `issues` returns every occurrence of a problem with its recorded fix.
- `stats` gives **success rate broken down by material** and the most common
  issues, plus total filament. The per-material rate is the one that earns its
  keep: "every PEBA print has trouble" points at a process problem rather than
  bad luck on one model, and no single entry can tell you that.

"Your last two successful PETG prints both ran 250/80 with a brim" is a real
answer. Suggesting they dry their filament when the log shows they already fixed
exactly this, a different way, is worse than useless. **If the log holds a fix
matching this material and nozzle, that is the first thing to try, and say so
plainly.** Then add ideas beyond it. If the log is silent, say that too, then
work from `references/troubleshooting.md` — and make sure the eventual fix gets
logged so next time is cheap.

### Record without ceremony

```bash
python scripts/printlog.py add --model "Grille v4" --material PETG \
  --nozzle 0.6 --layer-height 0.12 --nozzle-temp 250 --bed-temp 80 \
  --support-z-gap 0.54 --adhesion brim --dried "yes, 8h" \
  --result success --issue bed-adhesion \
  --fix "dried 8h at 65C + brim; z gap 0.54 with 0.6 nozzle" --duration 9.5 --grams 210
```

Only `--result` (`success` / `partial` / `fail`) is required. A sparse entry
beats no entry — log what is known and don't interrogate the user for fields
they didn't volunteer. When someone says "the grille finally came out clean,
turned out the filament was wet," log it and confirm in a sentence.

The fields worth chasing, in the order they turn out to matter when you look
back:

1. **`--result` and `--issue`** — what happened. `--issue` repeats; pass it more
   than once when a print had several problems.
2. **`--fix`** — what actually solved it. The single most valuable field in the
   log. When a print succeeds after a previous failure, always ask what changed
   and record it here.
3. **Material, nozzle, layer height** — the three axes most problems sort along,
   and what `settings` queries against.
4. **Temps, supports, adhesion, and whether the filament was dried.**

Keep issue tags consistent — "stringing" and "strings" won't find each other
later. The script suggests common tags and warns on new ones; the warning is not
a prohibition, just a nudge toward a tag that will match next time.

**Fill the log from the printer, not from the user's memory.** When the MCP is
live, `get_printer_status` and `get_printer_filaments` supply model, duration,
filament and grams directly. The less they have to type, the more consistently
the log gets kept, and a log with gaps stops answering questions. A finished
print is the natural moment to offer it — one line, not a form.

### Where the log lives

Defaults to `print-log.json` in the working directory, which is wrong for a
record meant to outlive the session. Ask once for a stable path the user
controls — with their 3D files, or in their documents folder — then pass
`--log` with that same path every time. A log scattered across temp directories
is not a log.

It is plain JSON on purpose: readable, greppable, and portable if the user ever
wants it somewhere else. They can open it and fix a typo without any tooling.

### Advising a fix

Both of these come from `references/troubleshooting.md`, which maps symptoms to
causes with material-specific sections:

- **Change one thing at a time.** Someone who changes temperature, speed and
  retraction together and gets a good print has learned nothing, and the log
  entry is worthless. Recommend the single highest-probability change first.
- **Prefer the cause over the symptom.** Raising temperature to fix layer
  adhesion when the real cause is wet filament produces a stringy part that
  still delaminates. Ask the diagnostic question — has this been dry-stored? —
  before reaching for a setting. When the MCP is live, `set_ams_drying` can act
  on the answer instead of just advising it.

Filament tracking rides along: the log records material, brand, color and grams,
so `stats` gives total consumption. It is not an inventory system — if the user
wants one, point at Spoolman.

## Hardware dimension lookups

`references/bambu_hardware.md` has known Maker's Supply specs and tolerances.
For anything unlisted or marked unverified, fetch the Bambu store page or
web-search `"<PART-NUMBER>" site:makerworld.com`. But remember: the mesh's
measured dimensions already include the designer's clearance — preserve
*measured* sizes, not bare catalog sizes.

## Privacy

Never write printer serial numbers, access codes, Bambu account credentials,
cloud tokens, LAN IPs, Wi-Fi details, local usernames, private file paths or
customer/private model names into this skill's files, references, or anything
committed. Treat downloaded private STLs, generated 3MF/G-code, printer logs,
screenshots, MakerWorld session data and any local config file as private —
they stay in the working directory, never in anything shared or published. If
this skill is ever published or shared, secret-scan it first and confirm only
placeholders remain. Use placeholders:
`<printer-lan-ip>`, `<printer-serial>`, `<access-code>`, `<output-dir>`. If
MakerWorld login is needed, use an existing browser session — never ask for
credentials in chat, never store them in a file.

## Failure modes to avoid

- Scaling magnet/hardware holes along with the body (the whole point).
- Booleans on non-watertight meshes — repair first.
- Silently converting a painted project 3MF through trimesh and handing back a
  stripped file.
- Trusting catalog dimensions over measured ones.
- Delivering STL when the standing preference is 3MF, or a renamed copy when
  the user asked for their file edited.
- Fabricating a printer profile so a slicer will run.
- Promising an OpenSCAD, OrcaSlicer-CLI or printer-MCP path before checking it
  is live — preflight for the CLI and local binaries, `ListConnectors` for MCPs.
- Guessing or defaulting `bambu_model`. It is `"h2c"`.
- Using the MCP's `scale_stl` on a model with hardware interfaces — it scales
  the holes too. `scripts/smart_scale.py` first, then slice.
- Starting a print without confirming it with the user.
- Answering a settings or troubleshooting question without checking the print
  log first, or fixing a print and not logging what worked.
- Recommending three changes at once, so the log entry can't say which worked.
- Designing a multi-part assembly here instead of handing it to cad-khana, then
  discovering the fit problem after it printed.
- Trusting a render over a cross-section.
- Lofting rings with a zero-length extension — duplicate rings at the same z
  make manifold3d reject the solid with "Not all meshes are volumes". Same
  error appears when a loft's winding is inconsistent; call `fix_normals()`.

## Adding lessons

A lesson about a *print* — symptom, cause, fix — goes in the log via
`printlog.py`, where the query commands can find it later. A lesson about the
*process* goes in the reference file it belongs to, tight: failure mode → root
cause → fix → why it matters.
