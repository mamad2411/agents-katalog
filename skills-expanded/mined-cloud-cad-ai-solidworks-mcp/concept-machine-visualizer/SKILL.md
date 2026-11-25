---
name: concept-machine-visualizer
description: Turn a mechanical machine spec or problem statement into 2–3 concept alternatives, a weighted selection, back-of-envelope sizing (motors, gearing, actuators, bearings, frames), and a dimensioned concept sheet (third-angle views + isometric + BOM) backed by a machine-readable concept.json for downstream CAD/design agents. Use this whenever someone needs a machine, mechanism, fixture, rig, robot, conveyor, press, gripper, test stand, or any mechanical-design concept conceptualised, sketched, laid out or visualised from requirements — even if they only say "come up with a design for…", "what would this machine look like", "concept for a device that…", or hand over a spec sheet. Not for detailed drawings of an existing CAD model or for pure data charts.
---

# Concept machine visualizer

You are acting as a mechanical design engineer at the **concept stage**: requirements are fuzzy, nothing is drawn yet, and the goal is a credible, sized, visual concept that the next person (or agent) can pick up and detail in CAD without re-asking basic questions.

Two outputs, always together:

1. **`concept.json`** — the single source of truth. Structured requirements, assumptions, alternatives, decision matrix, sizing, BOM and primitive geometry. This is what downstream agents consume, so it must be complete and internally consistent.
2. **`<name>_sheet.html`** — rendered from the JSON by `scripts/render_concept.py`. One page: top/front/right views at a common scale with overall dims and the envelope limit, an isometric with BOM balloons and motion arrows, plus all the tables. This is what humans look at.

Why this format: a JSON + primitive-geometry sheet is fast to produce (seconds to render, no CAD licence), unambiguous to a downstream agent, and still reads as an engineering drawing to a person. Don't jump to real CAD or photoreal renders at concept stage — they cost far more time and lock in detail the concept hasn't earned yet. If a downstream step *does* need CAD, the JSON geometry maps 1:1 onto sketches + extrudes (see "Handing off" below).

## Workflow

Work through these in order. Each step feeds the JSON; write the JSON progressively rather than at the end.

### 1. Parse the spec into requirements

Pull every quantitative and qualitative requirement out of the input into `requirements[]` with an ID (R1, R2…), the requirement, a target value with units, and `source` (`spec`, `derived`, or `assumed`). Typical things to look for — and to *derive* when missing:

- **Function**: what goes in, what comes out, what changes (position, shape, state, energy).
- **Payload**: mass, size, material, fragility, orientation, CoG.
- **Motion**: axes, strokes, speeds, accelerations, cycle time / throughput, positioning accuracy & repeatability.
- **Forces / torques**: process forces (cutting, pressing, clamping), gravity, inertia, friction.
- **Envelope & interfaces**: max footprint/height, mounting, utilities available (power, voltage, air pressure), operator access, upstream/downstream equipment.
- **Duty & life**: hours/day, cycles, design life, environment (dust, washdown, temperature, food/clean room).
- **Constraints**: cost target, quantity (one-off vs. production), standards/safety (guarding, e-stop, pinch points), make vs. buy preference.

If something critical is missing, **don't stop to ask** unless the gap makes the whole concept unworkable — pick a sensible engineering default, log it in `assumptions[]` with the reasoning, and keep going. The concept sheet surfaces assumptions prominently so the user can correct them cheaply. Asking five questions up front costs more than one revision.

### 2. Decompose functions and generate alternatives

Break the overall function into sub-functions (e.g. *hold part*, *move X*, *lift Z*, *apply force*, *sense position*, *support everything*). For each, list 2–4 working principles in a morphological chart (`morphology[]`): e.g. *move X* → belt drive | ball screw | rack & pinion | rodless pneumatic cylinder.

Combine choices into **2–3 genuinely different concepts** — different architectures, not the same machine with a different motor. A good set usually spans: simplest/cheapest, highest-performance, and one lateral idea (e.g. gravity, cam, compliant mechanism, re-using an off-the-shelf module). Give each a name, a 2–3 sentence description, pros and cons in `concepts[]`.

### 3. Select with a weighted decision matrix

Choose 4–7 criteria that actually discriminate for *this* spec (cost, cycle time, accuracy, footprint, reliability/maintenance, safety, manufacturability, risk). Weights sum to 1.0. Score each concept 1–5. The renderer computes the weighted totals; put the winner in `selected_concept` and a one-sentence `selection_rationale`. If engineering judgement overrides the numbers, say why — the validator will flag the mismatch so it's visible.

### 4. Size the selected concept (back-of-envelope)

Size every element that determines the geometry or a buy decision: actuators and motors, transmissions, guides/bearings, shafts, structure, pneumatics. Use the formulas in `references/sizing.md` — read it now if you haven't. For each row in `sizing[]` record: item, formula, inputs (with units), result, chosen catalogue size/class, and margin / safety factor.

Rules of thumb that keep this honest:
- Always include inertia (acceleration) loads, not just static — they dominate in fast automation.
- Apply efficiencies and a safety factor (typ. 1.5–2 on torque/force, 2–3 on structural yield for concept stage) and state them.
- Choose real standard sizes (NEMA/IEC frames, ISO cylinder bores, standard rail sizes, standard tube sections) so the downstream engineer can source them.
- Check the obvious failure modes: motor RMS vs. continuous rating, inertia ratio (load/motor ≲ 10:1 for servos), screw critical speed for long strokes, frame deflection at the tool point vs. accuracy requirement.

### 5. Lay out the geometry

Model the selected concept from primitives in `geometry[]` — boxes and cylinders, in **mm**, with the coordinate system:

- **+X** = length (left → right in the front view)
- **+Y** = depth (front → back; operator usually stands at −Y)
- **+Z** = up, Z = 0 on the floor or base plate

Model at "block diagram in 3D" fidelity: frame members, base plate, rails, carriages, motors, gearboxes, screws/belts, cylinders, grippers/tooling, the payload itself, guards and control box as simple envelopes. Every primitive gets an `item` linking to a BOM line and a `group` (frame, drive, transmission, motion, tooling, payload, electrical, pneumatic, guarding, sensor) which sets its colour. 15–60 primitives is typical; more is rarely useful at this stage.

Draw the payload and show the motion: add `motions[]` with linear strokes (from/to points) and rotary axes, labelled with stroke/speed. Draw the max envelope (`envelope`) if the spec has one — the renderer dashes it and flags violations.

Sanity-check the layout as you build it: does the stroke physically fit between end stops? Is there clearance for the payload through the full stroke? Can an operator reach the load point? Is the motor somewhere it can be serviced?

Full field reference: `references/concept-schema.md`. A worked example: `assets/example_concept.json` — copying its structure is the fastest way to start.

### 6. Render and review

```bash
python <skill-dir>/scripts/render_concept.py concept.json -o <name>_sheet.html --svg-dir views/
```

Read the validation flags it prints and fix them (unlinked parts, BOM items not drawn, envelope violations, decision/selection mismatch, missing sizing results). Then **look at the result** — open or screenshot the HTML if you can — and check: views agree with each other, nothing floats in mid-air, motion arrows sit on the right axes, proportions look like a real machine. Fix the JSON and re-render; it's cheap.

### 7. Deliver

Hand over both files (`concept.json` and the sheet; the `views/*.svg` are optional extras for docs/slides). In the message, give: the selected concept in one line, the 3–5 key numbers (envelope, motor sizes, cycle time achieved, mass), and the top assumptions/risks the user should confirm. Don't re-describe what the sheet already shows.

## Handing off to CAD / downstream agents

`concept.json` is the contract. A downstream CAD step can build each primitive directly: a box is a rectangle sketch on the XY plane at `pos[2]` extruded `size[2]`; a cylinder is a circle on the plane normal to `axis` extruded `length`. Keep `id` stable across revisions so downstream edits can be matched. If a SolidWorks (or other CAD) connector is available *and the user asks for CAD*, build the selected concept's primitives there as a skeleton assembly — otherwise stay in the sheet.

When revising after feedback, bump `rev`, edit the JSON, re-render. Never edit the HTML by hand — it'll drift from the JSON.

## What good looks like

- A reader can tell in 10 seconds what the machine does, how big it is, and what moves.
- Every number on the sheet traces to a requirement, an assumption, or a sizing row.
- Alternatives are real alternatives, and the choice is defensible.
- The BOM names buyable things with sizes (e.g. "NEMA 23 stepper, 2.4 N·m", "HGR20 rail ×2, 900 mm", "Ø40×100 ISO 15552 cylinder") rather than "motor".
- Risks are specific ("belt stretch may exceed ±0.1 mm repeatability at 3 m/s — verify or switch to screw") not generic ("may need testing").
