---
name: excalidraw
description: Use when producing a diagram as a .excalidraw file, or when asked for an architecture, flow, sequence, tree, mind map, org chart, timeline, network, ERD, swimlane, kanban or wireframe drawing that should look hand-drawn. Writes a short spec and expands it deterministically with measured font metrics, real layout and correct arrow bindings, then lints and renders it. Triggers on excalidraw, diagram, sketch, whiteboard, architecture diagram, flowchart, sequence diagram, mind map, hand-drawn, and on a diagram that opens with overlapping boxes or detached arrows.
license: Apache-2.0
compatibility: Requires Python 3.9+ and nothing else for the build and the lint. PyYAML only if the spec is YAML rather than JSON. Chrome is needed to look at a render and to regenerate the font metrics, and is invoked by you rather than by any script here.
metadata:
  version: "1.2.0"
  changeSummary: Adds crossing, overlap and label-collision lint rules, C4 typing and provenance in the spec with matching lint notes, a Mermaid label-fidelity checker, and offset reverse arrow pairs.
  isBreaking: "false"
---

# Excalidraw diagrams

## The contract

**Write a spec. Never write `.excalidraw` JSON by hand.** A spec of 20 to 60 lines becomes hundreds of lines of correct JSON, and the three things a model is worst at are done by code instead:

| Problem | Why hand-writing fails | What does it here |
|---|---|---|
| Coordinates | Placing boxes is arithmetic, and the failure is visible: overlapping nodes, arrows through shapes | A layout pass with deterministic tie-breaks |
| Text width | **Excalidraw never re-measures text on open.** `restoreElements` runs without `refreshDimensions`, so a wrong stored width silently clips glyphs | Advance widths measured in a browser against the real fonts |
| Invariants | Most violations open fine and look wrong, so nothing tells you | A linter that runs before you look |

```bash
S=~/.claude/skills/excalidraw/scripts
python3 $S/exdraw.py mydiagram.yaml -o mydiagram.excalidraw   # build
python3 $S/exlint.py mydiagram.excalidraw                     # MANDATORY, before looking
python3 $S/exfidelity.py source.mmd mydiagram.excalidraw      # only when redrawn from Mermaid
python3 $S/exsvg.py mydiagram.excalidraw -o preview.svg       # deterministic preview
google-chrome --headless --disable-gpu --screenshot=preview.png \
  --window-size=1600,1200 preview.svg                         # then READ the png
```

The render step is not optional and it is not a formality. A diagram is a user-facing surface, so the standing rule applies: never report it done without looking at it yourself.

## Why the multiplier everyone uses is wrong

Every published generator estimates width as `len(text) * fontSize * 0.55` or `* 0.6`. Measured against the real Excalifont at `fontSize: 20`:

| Text | True advance | At x0.6 | At x0.55 |
|---|---:|---:|---:|
| `Authentication Service` | **219.76** | 264.0 (+20%) | 242.0 (+10%) |
| `MMMMM` | **76.60** | 60.0 (-22%) | 55.0 (-28%) |
| `iiiii` | **24.40** | 60.0 (+146%) | 55.0 (+125%) |

Wrong in both directions, because the per-glyph spread is 3.5x (`l` is 0.225 em, `W` is 0.786 em). That is why other tools either clip text or leave dead space.

`assets/font-metrics.json` holds per-glyph advance widths and kern pairs for all eight bundled families, measured with canvas `measureText` in Chrome against Excalidraw's own woff2 subsets. The browser is the ground truth, because the browser is what produced the widths Excalidraw stored. Verified against four independently published values, reproduced to two decimals: `Hello world` 101.90, `Hello` 43.20, `Database` 93.92, `Start` 54.92.

Error bound, stated because it matters for `autoResize: false`: within about 0.1% on prose, up to 3-7% over on a short kern-heavy word. Over is the safe direction, and container widths round up.

## The spec

```yaml
type: flow            # flow tree grid swimlane mindmap sequence timeline network org c4 kanban journey gantt
title: Request path
style: architecture   # architecture (roughness 1) | formal (roughness 0) | sticker (roughness 2)
fontSize: md          # sm 16 | md 20 | lg 28 | xl 36

nodes:
  - id: api
    label: API
    color: blue       # ink red green blue yellow violet grey
    kind: decision    # decision -> diamond, start/end/state -> ellipse, default rectangle
    emphasis: true
    boundary: true    # dashed outline: a scope, not a thing

edges:
  - from: lb
    to: api
    label: HTTPS
    style: dashed
    arrow: false      # headless line

notes:
  - at: api
    text: rate-limited, 100 rps
```

`type: c4` adds C4 notation ([c4model.com](https://c4model.com)) and one more pair of fields is open to every type, provenance:

```yaml
type: c4
title: Online shop, containers       # required whenever `source` is set
source: {repo: example.org/acme/shop, commit: 3f9a2c1}   # 7 to 64 hex characters

nodes:
  - id: api
    label: Orders API
    c4: container                    # person | system | container | component
    tech: Python, FastAPI            # becomes "[Container: Python, FastAPI]" in the same label
    at: api/orders/routes.py:12-140  # repo-relative path:lines, or `external`
  - id: db
    label: Orders database
    c4: container
    tech: Postgres
    shape: database                  # drawn as an ellipse: Excalidraw has no cylinder
  - id: pay
    label: Payment provider
    c4: system
    external: true                   # grey, typed External Software System

edges:
  - from: api
    to: db
    label: Reads and writes orders   # what flows, never just "uses"
    tech: SQL                        # becomes a "[SQL]" line in the arrow label
```

The type and the technology go into the ONE bound label, at the same size, so they move with the shape. `c4`, `tech`, `external` and `shape` outside `type: c4` are a spec error, and so are an absolute path or `..` in `at`, and a `source` with no `title`. Everything lands in `customData` (`c4`, `tech`, `provenance`, and `role: title` on the title), which Excalidraw preserves verbatim and the linter reads. A full example is [`examples/c4.yaml`](examples/c4.yaml).

Everything else is derived. `style` is one decision that sets roughness, fill and font together, which is what keeps a diagram internally consistent.

## Design rules, measured rather than asserted

From 20 real published `.excalidraw` scenes (about 1,700 elements) and all 232 community libraries (about 55,000 elements). Most of this contradicts the popular prose skills, and the measurements are in [`references/design-rules.md`](references/design-rules.md).

1. **One roughness value per diagram.** 20 of 20 real scenes use exactly one. Every drawing that mixes them is in the ugly pile. `1` for architecture, `0` when the shapes carry formal meaning, `2` only for sticker cards.
2. **One fill style, one stroke width, one stroke colour.** 17 of 20, 16 of 20, and 10 of 20 use exactly one respectively; median distinct stroke colours is 1.5. The two ugliest scenes had 14 to 15.
3. **Colour budget: 1 stroke + 3 to 5 fills, each with a stated job.** Pair a shade-200 fill with the same hue's shade-800 stroke, or with `#1e1e1e`. Across 55,000 elements, palette-to-palette pairs are the same hue family in 1,048 of 1,069 cases.
4. **6 to 12 primary nodes. Split above about 15.**
5. **Node aspect 2.5 to 3.5 : 1, height about 3x font size, never below 20x50 px** - below that `adjustRoughness()` silently halves the roughness and the node renders smoother than its neighbours.
6. **Gutters about 1.5x node height, minimum 40 px.** Not the 200 to 300 px the popular skills prescribe, which is two to three times what real diagrams use.
7. **Nesting inset 20 px, and stop at three levels.** Encode depth by desaturating one hue, never by stacking saturated fills.
8. **Labels of 1 to 3 words, bound to the container.** 106 of 218 real labels are one word. The cleanest scenes bind 90 to 100% of labels; the messy ones bind none. Binding is what centres the label and grows the box.
9. **Arrows: 2 points, one head, bound at both ends.** 82% of real arrows are straight 2-point; `(null, "arrow")` in 13 of 13 scenes. Double-headed arrows are 2% of the corpus, so draw bidirectionality as two parallel arrows. The builder gives every arrow between the same two nodes its own lane 20 px apart (a reverse pair sits 10 px each way), so no two share one line.
10. **Bind an arrow label to the arrow.** That is how it gets an opaque backing: the renderer punches a hole of label + 10 px through the arrow behind a *bound* label. Free text laid over an arrow does not get it.
11. **Two text sizes, three at most, on the 16/20/28/36 ladder.** A fractional font size is the most reliable machine-detectable tell of an unmade diagram, because it comes from dragging a text box.
12. **Two typefaces, two jobs.** Hand-drawn for prose, the code font for anything literal: IPs, paths, commands, table and topic names.
13. **Dashes are scarce.** 0.9% of strokes in the corpus. Solid = fixed, owned, synchronous. Dashed = elastic, logical, async, a boundary. Dotted = a note or a lane separator.
14. **Rotate nothing, opacity 100, canvas white.** Zero rotated elements in 14 of 20 scenes; white canvas in 20 of 20. The hand-drawn feel comes from roughness, not tilt.

## Format facts that decide correctness

Full reference in [`references/element-schema.md`](references/element-schema.md). The ones that bite:

- **Bindings are reciprocal and `restore` repairs neither.** An arrow follows a moved shape via the SHAPE's `boundElements`; its endpoint comes from the ARROW's binding. Different mechanisms, both required. One alone renders correctly and detaches on first drag. This is the most-reported defect in agent-written Excalidraw files.
- **The binding schema changed.** Current is `{elementId, fixedPoint: [rx, ry], mode: "orbit"}`. `focus` and `gap` are gone from the type, and a legacy binding is migrated by *discarding your numbers and recomputing from where the points already are* - so endpoint geometry is the real contract.
- **No `fixedPoint` coordinate may be exactly `0.5`.** It is snapped off centre to stop the arrow heading flipping. This builder writes `0.5002`, because the upstream `0.5001` minus `0.5` is just under `0.0001` in IEEE 754 double, which is still inside the `1e-4` guard it was chosen to clear.
- **`points[0]` must be `[0, 0]`** on any linear element, or the element visibly jumps on load.
- **`endArrowhead` defaults to `"arrow"` when omitted.** Write `null` for a headless arrow.
- **Always write `lineHeight`.** Omit it while supplying a height and Excalidraw back-derives a bogus value that permanently distorts line spacing.
- **`roundness` must match the element class** or it silently yields radius 0: `{type:3}` rectangle/image/iframe/embeddable, `{type:2}` line/arrow/diamond, `null` ellipse/text.
- **Omit `index`.** A hand-written partially-invalid set throws `invalid order key`, the throw is swallowed, and the canvas renders blank.
- **Never emit exactly `0`** for a coordinate. Three upstream falsy-zero bugs are open on it. This builder starts the canvas at 100.
- **`opacity` is 0 to 100**, not 0 to 1. **`fillStyle` defaults to `solid`**, not hachure. **`angle` is radians.**
- **Container geometry is not the naive formula.** Max text width is `w - 10` for a rectangle but `round(w/2 * sqrt2) - 10` for an ellipse and `round(w/2) - 10` for a diamond. The `x = container.x + (container.width - textWidth)/2` that every published skill uses is wrong for ellipses and diamonds by the inscribed-box inset.

## Determinism

**The same spec produces a byte-identical file.** Ids, `seed` and `versionNonce` come from a BLAKE2b of the spec (as canonical JSON, with `source` and every node and edge `at` left out, so bumping a commit does not re-roll the seeds) plus each element's path within it; `created`/`updated` default to a fixed epoch; layout iteration counts are fixed and every tie-break sorts on a stable key.

No prior implementation manages this. The most-installed skill in the field seeds from Python's `hash()`, which is salted per process by `PYTHONHASHSEED`, so it looks reproducible and is not; the closest CLI uses `Math.random()` and `Date.now()`.

Verify it yourself:

```bash
python3 $S/exdraw.py spec.yaml -o a.excalidraw
python3 $S/exdraw.py spec.yaml -o b.excalidraw
cmp a.excalidraw b.excalidraw && echo "byte-identical"
```

`--stamp-now` opts out, and gives up reproducibility in exchange for a real timestamp.

## Verification

1. **Lint.** `exlint.py` checks referential integrity in both directions, `points[0]`, roundness class, 0x0 elements, NaN, exact-zero coordinates, text overflow, node overlap, lines through boxes, and the style rules above. A blind A/B on seeded defects found geometric checks caught 12 of 12 with no false positives, versus 11 of 12 with one false positive by eyeballing renders. Lint first, always.
   - **Strokes, solved exactly.** `arrow-crossing` (warn): two arrows or lines cross. Crossings are the one layout aesthetic with measured weight on reading errors and time, see [`design-rules.md`](references/design-rules.md) section 6. Not a crossing: a touch (one stroke ends on the other, a bus spur), a fan-out or fan-in (within 8 px of an end that both strokes bind to the same shape). `arrow-overlap` (warn): two strokes on one line, which is worse than a crossing. Exempt only when the two share exactly one bound end (a trunk that splits, or spurs merging into one target); two strokes sharing both ends are a duplicate drawn on itself. `arrow-through-label` (warn): a stroke across another arrow's label. A multi-point arrow, rounded or not, is tested as its polyline. The summary line ends with `crossings: N`, so two layouts compare by number.
   - **C4, as notes tagged "c4model checklist"**, active when any element carries `customData.c4`: `c4-untyped` (a boundary is exempt), `c4-no-tech` on a container or component, `c4-vague-edge` (no label, or only uses, calls, connects to, talks to, depends on or interacts with), `c4-no-title`, `c4-too-many` at 20 containers. Not checked, because it needs a human: whether the scope is clear, whether a label reads in its arrow's direction, and mixed zoom levels in one diagram.
   - **Provenance**, active when the title carries a `source`: `provenance-missing` (warn) on a shape or arrow with no `at`, `provenance-commit` (error) on a commit that is not 7 to 64 hex characters. Whether each line range still says what the edge claims is not checked: that needs the repo and a reader.
2. **Fidelity, when the diagram is a redraw of a Mermaid flowchart.** `exfidelity.py source.mmd out.excalidraw [--json]` lists every node, edge and subgraph label kept, missing or ambiguous, every source edge with or without an arrow between the matching shapes, and every arrow with no source edge. A node must equal one shape's bound label exactly (the `[type: tech]` line aside), one node to one shape; an edge label is read from its own arrow, so swapped labels fail; a match with two candidates fails as ambiguous. Exit 0 all kept, 1 something lost or ambiguous, 2 the source or the scene cannot be read (any crash is 2 as well, in all three scripts). It reads `flowchart` and `graph` only and fails closed: any other diagram type, or one line it does not understand, is exit 2, never a silent pass.
3. **Look at it.** Render and read the PNG. The SVG preview is exact on geometry and an approximation of stroke texture.
4. **Open it in Excalidraw once and drag a bound shape.** Confirm the arrow follows, the label stays centred, and on a C4 or sourced diagram that `customData` survives a save. No linter can check that, and it is the failure this skill exists to prevent.

## Gotchas

| Symptom | Cause / fix |
|---|---|
| Arrows detach the first time a box is dragged | Only one side of the binding was written. Both are required, and nothing repairs them. |
| Text is clipped, or a box has dead space | Stored width is wrong and never re-measured. Use the metrics, not a multiplier. |
| A label sits off-centre in an ellipse or diamond | The naive centring formula. Use the inscribed-box inset. |
| The canvas opens blank | A hand-written `index` that fails to parse. Omit `index`. |
| One box looks smoother than the rest | It is below 20x50 px, so `adjustRoughness()` halved it. |
| An arrow renders right, then snaps on first interaction | `points` disagree with what the binding implies. |
| A shape is invisible | `width` and `height` both 0, or `backgroundColor` left transparent while a fill was intended. |
| An element vanished with no error | Unknown `type` string. `restoreElement` has no default case and drops it silently. |
| The diagram looks synthetic despite roughness 1 | Every element got `seed: 1`. Seeds must differ. |
| A PNG export clips the right edge of text | `exportToSvg` computes the viewBox from stored dimensions while text renders at its natural width. Correct metrics prevent it. |
| An arrow disappeared | It spanned more than 75,000 px, so Excalidraw deleted it and substituted a stub. |

## Prior art (checked 2026-09)

The field is crowded at the prose layer and empty at the engineering layer. skills.sh lists 100 excalidraw skills; GitHub code search returns 9,552 skill files mentioning it; there is no official Anthropic one. **Nothing surveyed combines measured font metrics, a real layout pass, current-schema bindings, genuine hand-drawn output and a pre-render linter. The best have three, and nothing has the first two together.**

- **[`github/awesome-copilot`](https://github.com/github/awesome-copilot) `excalidraw-diagram-generator`**, 29,210 installs and the most-installed in existence, correctly mandates `fontFamily: 5`. Its arrow script writes **no bindings at all**, hardcodes `"index": "a0"` on every element, and seeds from `hash()`.
- **[`coleam00/excalidraw-diagram-skill`](https://github.com/coleam00/excalidraw-diagram-skill)**, 4,737 stars, has the best design doctrine in the field, including the Isomorphism Test: *"If you removed all text, would the structure alone communicate the concept?"* It also refuses to generate (*"Don't write a Python generator script"*) and pays for it with a documented ~32,000-token output ceiling. Its two most-copied numbers are contradicted by measurement: the under-30%-containers rule is backwards, and its 200 to 300 px gutters are two to three times reality.
- **[`excalidraw/mermaid-to-excalidraw`](https://github.com/excalidraw/mermaid-to-excalidraw)** is the strongest prior art and its limits are structural: it has no layout engine of its own, it scrapes geometry from a rendered DOM so a real browser is mandatory, and every unsupported diagram type becomes a raster image.
- **[`zsviczian/obsidian-excalidraw-plugin`](https://github.com/zsviczian/obsidian-excalidraw-plugin)**'s ExcalidrawAutomate is the richest programmatic surface that exists and the source of the `0.5001` fixed-point trick.

What this adds: the metrics, the determinism guarantee, the linter, and native handling for the types the whole field leaves raster-only.

## Status

Built 2026-09-09. Font metrics verified against four independently published values and reproduced to two decimals by a different method than the one that published them. Every lint rule is proven by falsification: the defect is seeded, the check must fire, the defect is removed, the check must stop. Determinism is asserted by building twice and comparing bytes.

## Related

- [`references/design-rules.md`](references/design-rules.md) - the measurements, the palette pairing table, per-diagram-type recipes.
- [`references/element-schema.md`](references/element-schema.md) - the verified format reference, for the raw escape hatch.
- This skill owns diagrams only. Visual doctrine for product surfaces (typography, colour, motion, growth mechanics) is a separate concern and is not covered here.
