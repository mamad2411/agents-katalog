---
name: architectural-concept-design
description: >-
  Turns a building brief into a checked concept design package: requirement matrix, decision
  questions, design specification, CAD floor plans, elevations and a section (DXF, PDF, PNG), a
  furnished interactive 3D model in one HTML file, and an area schedule. Write one JSON design
  model, and the bundled engine checks circulation, door swings, daylight, stairs, area limits
  and setbacks before drawing anything. Use whenever the user wants to design or lay out a house,
  cottage, bungalow, apartment or other small building; turn a room list, brief or sketch into floor
  plans; get a 3D model or renders of a layout; check a plan against area limits or clearances;
  or produce DXF/PDF drawings for a concept design, even without the words "concept design".
  Not for structural engineering, construction documents or large non-residential buildings.
license: MIT
compatibility: Python 3.10+ with ezdxf, PyMuPDF and Pillow (uv installs them automatically); headless renders need Chrome, Edge or Chromium.
metadata:
  version: "1.0.1"
  author: Mehran Gharooni
---

# Architectural concept design

Design a small building the way an architect does at concept stage, but as data. One
`design.json` holds the site, levels, walls, openings, rooms, stairs and furniture. The bundled
engine validates it, enforces design rules, and generates every output from it, so drawings, 3D
model and areas cannot disagree. Your job is the design thinking. The engine's job is
geometry, rules and drawing.

## Commands

Paths are relative to this skill's folder. Run them with `uv run`, which installs dependencies,
or with `python` after `pip install -r scripts/requirements.txt`.

```bash
python scripts/concept.py init <project>                   # design.json, brief.md, specification.md
python scripts/concept.py check <project>/design.json      # validate + design rules; exit 1 on errors
python scripts/concept.py build <project>/design.json --renders
python scripts/concept.py schedule <project>/design.json   # area schedule as a Markdown table
```

Run the scripts; there is no need to read their source. `check --json` gives machine-readable
findings. `build` refuses to write anything while a rule error remains, and writes
`output/report.json` listing every file it made.

## Workflow

Copy this checklist into your task list, or into a `NOTES.md` in the project folder, and keep
it current:

```
- [ ] 1. Brief -> requirement matrix (brief.md)
- [ ] 2. Decision questions answered, or assumptions recorded
- [ ] 3. Constraints fixed: site, area limits, setbacks, local rules
- [ ] 4. Specification written (specification.md)
- [ ] 5. design.json written
- [ ] 6. check: 0 errors, warnings reviewed
- [ ] 7. build --renders, outputs reviewed and fixed
- [ ] 8. Results presented with assumptions and open issues
```

**1. Requirement matrix.** Turn the brief into rows: program (spaces), limits (areas, heights,
setbacks), preferences (orientation, adjacency) and site facts. Each row has a source and a
status. Format and examples: [references/briefing.md](references/briefing.md).

**2. Decision questions.** Ask only what changes the layout, for example stair type, parking,
open or closed kitchen, or the number of bathrooms. Each question has three options, one
recommendation and one reason. If the user wants speed, adopt your recommendations and record
them as assumptions. Never invent site facts such as boundary sizes, the north direction or area
limits. Ask for them, or label them clearly as placeholders.

**3. Constraints.** Fix the site polygon, street side, setbacks, area limit per level and any
local regulation the user names. Where local rules are unknown, use the defaults in
[references/standards.md](references/standards.md), and say that they are defaults.

**4. Specification.** Fill `specification.md`: the site strategy, levels, a table of spaces with
sizes and reasons, circulation, openings, facades and open issues. The design model must follow it.

**5. Design model.** Read [references/design-model.md](references/design-model.md) before
writing `design.json`; it defines every field and convention. Plan the layout with
[references/layout-guide.md](references/layout-guide.md): grid and bands, zoning, the stair and
wet-room core, door swings and furniture clearances. Work in this order:

1. footprint and levels
2. partitions
3. doors and windows
4. rooms with label points
5. stairs
6. furniture

Starting from `init` or from a similar model is faster than writing from scratch.

**6. Check, fix, repeat.** Run `check`. Fix every error in `design.json`, never in an output,
then run it again. Treat warnings as design questions: fix them, or explain to the user why they
stand. The usual fixes:

| Finding | Usual fix |
|---|---|
| `reach`: a room cannot be reached | add a door or an opening in the wall between it and the circulation |
| `door-swing`: swings into furniture or a wall | move the item, flip `hinge`/`opens`, or shift the door along the wall |
| `clash`: furniture overlaps or stands in a wall | move or resize the item; keep it inside the room |
| `area-limit` | shrink the footprint or move space to another level |
| `setback` / `site` | move or shrink the footprint inside the buildable zone |
| `daylight` | enlarge or add windows on outside walls of that room |
| `stair` | lengthen the stair rectangle; 2 x rise + going should be 0.60 to 0.65 m |
| `label` | shorten the room name or move `label_at`; labels are larger on 1:100 plans |

**7. Build and review.** Run `build --renders`. Then look at the outputs yourself: open the plan
PNGs in `output/drawings/png/` and the renders in `output/model/renders/`. Walk through the
building with [references/review-checklist.md](references/review-checklist.md). A furnished 3D
view shows problems the rules cannot: a kitchen with no window over the sink, a TV facing a
window, a bed under a sloping roof, a dark hall. The reachability rule ignores furniture, so
check the routes past sofas and tables against the clearances in the layout guide. Fix each
problem in `design.json` and build again. If no browser is available for renders, review the
plans, elevations and section, and ask the user to open `output/model/index.html`.

**8. Present.** Give the user:

- the drawing set (`output/drawings/concept-drawings.pdf`)
- the 3D model (`output/model/index.html`, which opens in any browser, offline)
- two or three renders, and the area schedule against each limit
- the check summary, the assumptions you made and the open issues

State plainly that this is concept-stage design. Structure, services and code compliance need
licensed professionals.

## Fixing or changing an existing design

When the user brings a `design.json` that fails, or asks for a change to one, skip steps 1-4
unless they want a redesign.

1. Run `check` first. Validation errors name the JSON path; rule findings name the opening or
   furniture index.
2. Change only what the request and the findings need, and honour the user's limits, such as
   "keep the room layout".
3. If the file used to build, compare it with the last version that passed. Before large edits,
   keep a copy of the passing file.
4. Run `check` until it is clean, then `build`. Problems you were not allowed to fix go in the
   open issues.

## Outputs

| Path under `output/` | Contents |
|---|---|
| `drawings/concept-drawings.pdf` | A3 set: cover with area schedule, site plan (when `site` is given), a plan per level, four elevations, section A-A |
| `drawings/dxf/`, `pdf/`, `png/` | each sheet as DXF R2018 (AIA/NCS layers), PDF and PNG |
| `drawings/model_1to1_metres.dxf` | every plan at true size in metres, for CAD work |
| `model/index.html` | furnished 3D model: cutaway levels, whole building with roof and site |
| `model/renders/*.png` | 1920 x 1200 views (with `--renders`) |
| `area-schedule.md`, `.csv` | rooms, stairs, circulation and walls; rows add up to the built area |
| `report.json` | check findings, DXF audit, built areas and every output path |

The 3D page takes deep links: `#house`, `#house-rear`, `#level-<id>`, `#level-<id>-rear`. Add
`-still` to hide the interface.

## Engine limits

- Plans are orthogonal: walls, rooms and furniture are axis-aligned rectangles. Footprints may be
  unions of rectangles (L, U or courtyard shapes).
- Stairs are straight or U-shaped. Roofs are gable (ridge along x or y) or flat.
- The site is treated as flat at ±0.00. Basements are allowed, but sloping terrain is not modelled.
- Rules are concept-level checks, not a building-code audit.
