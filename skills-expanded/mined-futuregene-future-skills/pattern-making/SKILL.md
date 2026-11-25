---
name: pattern-making
description: Pattern making, pattern design and sewing (garment drafting, flat pattern design, draping logic, sewing construction). Turns a request, a photo, a technical drawing or a fashion sketch, including sculptural or unconventional volumes, into real patterns drafted the way professional patterns are drafted, for every garment family and accessory (skirts, trousers, bodices, dresses, shirts, sleeves, collars, tailoring, outerwear, knits, lingerie, swimwear, gloves, hats, bags). Adds allowances, notches, grain lines, grades sizes, exports 1:1 SVG, DXF or CLO3D. Use whenever a garment pattern, a sketch to develop, body measurements, ease, grading, a toile, sewing techniques or a 3D garment comes up, whatever the software. 中文触发：服装打版、纸样、制版、放码、缝制工艺、CLO3D。
license: MIT license
category: engineering
metadata: {"version": "1.0", "skill-author": "Adrien Delmas (pattern-making-skill)"}
---

# Pattern making

> **来源与边界**：移植自 `https://github.com/adriendelmas/pattern-making-skill`
> （`skills/pattern-making/`, commit `6587004c4c0495592d0a3947553b52e72f1e354c`, MIT），资源整目录复制。
> 中文边界：本技能是**服装/纺织**打版（几何计算 + SVG/DXF/CLO3D 导出），需 Python 3.8+（引擎仅用标准库，
> `scripts/sheet.py` 出 PNG 需 Pillow）；不覆盖工业产品设计（ID/CMF/结构）。详见 `SOURCE.md`。

Universal pattern-making skill. It drafts like a professional pattern maker: from the construction of
real garments and established methods, never from a silhouette alone. The knowledge is in `references/`,
the calculations are done by `scripts/pattern.py` (Python 3.8 or newer, standard library only).

## Rules

1. **Know the construction before drafting.** From a photo or a drawing, run the analysis protocol
   (`references/reference-analysis.md`): every seam, fold, piece, finish, with evidence and confidence,
   dimensions measured at scale on the photo, and its checklist answered line by line (front edge and
   overlap, closure, symmetry, collar, shoulders, volume, pockets...). A blank line is a misread garment.
   From a fashion sketch, follow `references/design-from-sketch.md`. Write the construction sheet first.
2. **Draft like real patterns.** For every garment type, follow the technique sheet of its family in
   `references/techniques/`. If the construction is not covered there, look up how published patterns
   and pattern-making books draft it (web search, pattern images the person gives), study their pieces,
   and draft the same way. Never invent a construction a pattern maker would not recognise.
3. **Always start from measurements.** Ask for the measurements needed (`references/measurements.md`). If
   they are missing, start from a standard size and say clearly which values are estimated.
4. **Never calculate in your head.** Coordinates go through the script. An error of a few millimetres is
   repeated on every seam.
5. **Read the checks.** Each draft prints a report. A line marked `!!` must be fixed before going on.
6. **Validate in 3D or on a toile, and correct the pattern, not the simulation.** When a piece is too
   complex to place automatically in CLO3D, hand it over to the person (`references/clo3d.md`).
7. **Stay neutral on the method.** The engine's blocks are proportional and tied to no author. If the
   person follows a given method (Aldrich, Armstrong, Müller, Esmod, Bunka, other), use its values.

## Construction laws (checked by the engine on every export)

1. **Reciprocal lengths**: edges sewn together have the same length within 1 mm. Every intended difference
   (cap ease, gathers, easing) is declared on the seam with its ratio and reason.
2. **Right angles at the fold**: a half piece meets its fold at 90 degrees (neckline, waist, hem), so the
   unfolded piece has no point or dip.
3. **Volume needs shaping**: the body is not developable. Curvature is taken by darts, seams, ease or
   stretch; joints with large movement get inserted pieces (gussets, set-in thumbs, crotch extensions).
4. **Shapes come from real patterns**: complex pieces (thumbs, gussets, collars, sleeve heads) follow the
   shapes of published patterns, scaled to the measurements, never an improvised outline.

Every piece cut from another one (facing, interfacing, pocket facing; not linings, which are larger by design) declares it with `"within"`, so the
engine checks it does not pass its piece; the engine also flags pieces pinched between two wide parts.

A pattern is finished when its report has no `!!` line and its seam table (`seams_<size>.md`) is all OK.

## Whole garments from a spec

Jackets and coats are drafted by `python scripts/pattern.py garment spec.json --out folder`
(`references/garment-spec.md`): reusable constructions on the bodice block (body ease, extended and padded
shoulders, darts, boxy or armhole princess with flare, overlap or wrap, notched lapel drafted in place, stand or
funnel collar, two-piece sleeve matched to the armhole, facings, lining, pockets). It writes the cut pieces and
the 3D shell for CLO3D with every seam and wrap hold; `python scripts/sheet.py folder/pieces_<size>.json` draws PNG
sheets (Pillow). Add a construction to `scripts/garment.py` rather than writing a one-off script.

## Any garment as data

Garments the engine has no block for are written as a recipe: pieces with named nodes, Bezier curves, holes
and mirror pairs, plus a seam list pairing edges by node names, with declared ease
(`references/piece-format.md`). `python scripts/pattern.py piece recipe.json --out folder` validates it with
the same laws, exports it, and `clo3d ... --assemble` sews it in CLO3D. No new code per garment.

## Knowledge map

Start with the knowledge base: one entry per garment, piece or technique (recognition, pieces, shape with
anchors and seam correspondence, drafting, sewing order, fabrics, fit faults, CLO3D, confidence):

```
python scripts/pattern.py kb search <words>     # English or French, accents ignored
python scripts/pattern.py kb show <id>
```

Worked specs: `examples/notched-lapel-jacket/` (fitted and oversize, lined) and `examples/velvet-coat/` (princess,
flare, 16 cm wrap, funnel collar, lined). Index: `references/kb/INDEX.md`. Format of an entry: `references/kb/FORMAT.md`. A shape marked
"unverified" must be checked against real drawn patterns before it goes into a pattern.

| Need | Sheet |
|---|---|
| Analyse a photo, recognise constructions | `references/reference-analysis.md` |
| Develop a sketch, sculptural volumes, unconventional cutting | `references/design-from-sketch.md` |
| Skirts, trousers, shorts, jumpsuits | `references/techniques/skirts-trousers.md` |
| Bodices, dart manipulation, dresses, tops, shirts | `references/techniques/bodices-dresses-tops.md` |
| Sleeves, cuffs, plackets, collars, hoods | `references/techniques/sleeves-collars.md` |
| Jackets, coats, tailoring, outerwear | `references/techniques/tailoring-outerwear.md` |
| Knits, lingerie, swimwear, activewear | `references/techniques/knits-lingerie-swimwear.md` |
| Gloves, hats, bags, belts, ties | `references/techniques/accessories.md` |
| Seams, hems, facings, closures, pockets, gathers, elastic | `references/techniques/sewing-techniques.md` |
| Engine blocks and how they are drafted | `references/blocks.md` |
| Dart pivot, slash and spread, fullness | `references/transformations.md` |
| Measurements, ease, finishes, piece format | `references/measurements.md`, `ease.md`, `finishes.md`, `piece-format.md` |
| Sending, sewing and simulating in CLO3D | `references/clo3d.md` |

## Workflow

1. **Understand the request**: garment, wearer, fabric (woven, knit, stretch, leather), intended fit.
   With an image, write the construction sheet (rule 1). Read the technique sheet of the family.
2. **Measurements**: `python scripts/pattern.py measurements --body women --size 38` prints every
   measurement used. For personal measurements, write a JSON file and pass it with `--measurements`.
3. **Ease**: by garment and fabric (`references/ease.md`), overridden in the measurements file (`"ease"`).
4. **Base**: `python scripts/pattern.py block <skirt|bodice|sleeve|trousers|all> --body ... --out folder`
   gives the standard blocks. `block glove --size 7 --length 40 --end-girth 26` drafts a leather glove like
   real glove patterns (trank, Bolton thumb in a tongued hole, fourchettes) with its seam list; personal
   hand measurements go under `"hand"` in the measurements file (`references/techniques/accessories.md`). Garments that do not start from these blocks (gloves, hats, bags, circle
   skirts, sculptural pieces) are drafted directly from their technique sheet, as pieces in the skill's
   format (`references/piece-format.md`).
5. **Transformation**: `pivot` closes or transfers a dart, or opens a slash for fullness; `smooth`
   redraws a hem or a neckline. Methods in `references/transformations.md` and the technique sheets.
   Finish with `python scripts/pattern.py piece file.json --out folder`, which prints every edge length
   to check that seams match.
6. **Finishes and construction**: allowances by seam type, notches, grain, facings, closures
   (`references/finishes.md`, `references/techniques/sewing-techniques.md`).
7. **Grading**: `--sizes 36,38,40,42` produces every size and an SVG where they nest.
8. **Output**:
   - `pattern.svg`: print at 100 %, check the 10 cm square.
   - `pattern_<size>.dxf`: for CAD software (layers CUT, SEAM, NOTCHES, GRAIN, TEXT).
   - `clo3d_<size>.py` and `clo3d_<size>.json`: for CLO3D, with the plugin and MCP server of
     [clo3d-mcp-extended](https://github.com/adriendelmas/clo3d-mcp-extended). Exact curves, one CLO3D
     line per pattern edge. Workflow, seams, mesh, placement: `references/clo3d.md`. Defaults for every
     piece: added collision thickness 0, mesh size by fit.
   - `pieces_<size>.json`: the skill's editable format, in cm.

## Conventions

- Inputs in centimetres, SVG, DXF and CLO3D outputs in millimetres.
- Piece axes: x towards the side, y downwards, origin at center front or center back.
- Symmetric pieces are drafted as half pieces, with an edge "on the fold". The CLO3D export unfolds them.
- Notches: one notch at the front, two notches at the back.

## Without Python

If the agent cannot run a script, apply the methods of `references/` by hand, writing out each
calculation, and say that the draft was not verified by the automatic checks.
