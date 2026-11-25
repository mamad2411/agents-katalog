---
name: aieng-cad-authoring
description: Active MCP-first CAD authoring skill for AIENG Workbench. Use when the user asks to create, design, draft, model, or iteratively build CAD geometry through the active cad.* MCP tools. Do not use for solver/result review, schema/library implementation, or editing legacy IR plans.
---

# aieng-cad-authoring

MCP-first CAD authoring discipline for agents driving the active AIENG Workbench.
The recommended path is the live MCP toolchain and build123d runtime, not the older schema-plan CLI flow.

## Purpose

- Create or extend real CAD geometry through `cad.execute_build123d`.
- Keep generated geometry inspectable with named parts, colors, and editable constants.
- Use the UI as the live 3D viewer and spatial pointer surface.
- Preserve evidence honesty: CAD output is geometry evidence, not engineering validation.

## When to use

Use when the user asks to create, build, design, model, add, or substantially modify CAD geometry.
For pure dimensional tweaks on an existing editable model, prefer `cad.edit_parameter`.
For engineering audit only, use `cad.critique` without mutating geometry.
For solver workflows, use `aieng-cad-cae-copilot`.

## Required workflow

1. Call `aieng.agent_readme`, `aieng.list_projects`, and `aieng.agent_context { project_id }` when project state is not already known.
2. Call `cad.get_source { project_id }` before incremental edits; use `mode="append"` only when `has_base=true`.
3. For new/additive geometry, call `cad.execute_build123d` with build123d Python that:
   - binds the final model to `result`,
   - omits export calls,
   - sets `.label` on every meaningful part,
   - sets `.color = Color(r,g,b)` for readability,
   - declares editable dimensions as `UPPER_SNAKE_CASE` constants,
   - asserts design intent with `require(condition, "message")` — e.g.
     `require(WALL_THICKNESS >= 3, "wall below 3mm CNC minimum")`. A failed
     `require()` (or a bare `assert`) fails the build deterministically and is
     returned as a structured `code: design_rule_violation`, so constraints are
     verified by construction instead of hoped for; a passing one is a no-op.
4. Inspect the returned thumbnail, `named_parts`, `parts_added`, `geometry_report_summary`, symmetry, and gaps before continuing.
5. For pure dimensional changes, use `cad.edit_parameter` and read both `regression_diff` (topology drift) and `critique_diff` (manufacturability) before trusting the result.
6. For mechanical parts, call `cad.critique` after creation and fix blocking manufacturability findings.

## Self-correction before presenting a result

Do not present a build as done just because it executed. Read the deterministic
signals every `cad.execute_build123d` / `edit_parameter` / `replace_part` /
`remove_part` returns and self-correct first:

- **`geometry_report_summary`** is always present (both `response_detail` modes):
  a one-line `part_count / size / proportions / floating=N / symmetry_issues=N / spatial_issues=N`.
  Non-zero `floating` means a part is detached (usually a coordinate typo);
  non-zero `symmetry_issues` means a left/right pair is mismatched or missing;
  non-zero `spatial_issues` means bounding boxes show deep overlap or solid
  containment, which is the common "parts are in the wrong place / interpenetrate"
  failure mode.
- **`critique_diff`** is returned by every `cad.edit_parameter` / `replace_part`
  / `remove_part`: it runs the engineering critique before and after the edit and
  reports whether manufacturability violations **increased**. A verdict of `fail`
  (new high-severity finding) or `warn` (new medium/low) means the edit made the
  part *less* manufacturable even if topology looks fine — read its `introduced`
  list and fix or reconsider before presenting the result. `improved` / `clean`
  are safe; `skipped` means no solids to critique.
- **When `floating`, `symmetry_issues`, or `spatial_issues` is non-zero, call
  `cad.design_review`** (read-only). It folds the critique + those structural
  signals into one
  severity-ranked `actions` list and binds each fixable finding to a concrete
  `cad.edit_parameter` target (`featureId` / `parameterName` / range). Fix the
  highest-severity targets, then re-run the review. It mutates nothing — applying
  a fix still goes through the approval-gated edit path.
- **Read the modeling-fidelity verdict** — every `cad.execute_build123d` /
  `cad.edit_parameter` / `cad.replace_part` / `cad.remove_part` response carries a
  compact `modeling_fidelity` ({level, score, findings}), and the full `fidelity`
  block is on `cad.critique` / `cad.design_review`. It is a SEPARATE axis
  from manufacturability: a part can pass DfM yet score `crude` (`level` ∈
  `designed` / `basic` / `crude`, 0–100) because it is primitive-stacked or
  unfinished — no fillets/chamfers (sharp edges read as crude), bare boxes with no
  detail, or parts buried inside others. **Do not present a `crude`/`basic` result
  as done** — apply the findings' fixes (break visible edges with `fillet()`/
  `chamfer()` last, after booleans; shape designed bodies with loft/sweep/revolve;
  expose hidden parts) via a geometry edit, then re-review. Cylindrical parts
  (shafts/pins) are not penalised — a cylinder is legitimately a cylinder.
- **Reference images.** When the user names a real product / character / vehicle
  but supplies no picture, call `cad.search_reference_image { project_id, query }`
  before iterating — it attaches a Wikimedia Commons match so every thumbnail is
  calibrated against the real proportions. Verify the returned `page_url`'s
  source/license; `status: "no_results"` just means proceed without one. If the
  user gives a URL/file, use `cad.set_reference_image` directly.
- **Reversibility.** Each successful CAD mutation is auto-snapshotted; if an edit
  goes wrong, `cad.list_snapshots` then `cad.restore_snapshot` rolls back
  (approval-gated). Iterate freely rather than over-planning a single build.
- **Category starters.** For a common shape (flange, plate, bracket, enclosure,
  bushing, aircraft, vehicle, wheel), `cad.plan_build123d_skill` returns a
  parameterized starting point with editable constants — review it, then execute.

## Complex models — decompose, validate, then commit

Do not one-shot a whole complex model (multi-part assembly, gearbox, robot arm,
multi-shell housing, anything with a kinematic chain or many mates). A single
large `cad.execute_build123d` script is the highest-failure path. Instead:

1. **Author a CAD brief first (the contract).** Before any geometry, call
   `cad.author_brief { units, model_type, parts:[{name,size_mm}], overall_size_mm }`
   — it records the plan and auto-derives a validation-target list (parts present,
   counts, overall/part sizes, no-floating). Name every part and its role; identify
   the inter-part relationships that must hold (shaft-in-bore, gear mesh center
   distance, links connecting end-to-end); state landmark coordinates / lengths /
   angles as `UPPER_SNAKE_CASE` constants. After building, call
   `cad.validate_targets` (with no args it uses the brief's targets) — it returns
   pass/fail/unknown per target so a plausible-but-mispositioned model can't pass silently.
2. **Validate each sub-structure in isolation before committing it.** Use
   `cad.validate_subpart { code }` (read-only, no package write) to check that a
   sketch→solid, a boolean, or one sub-assembly builds into a non-empty solid and
   read its error if not. This turns the all-or-nothing build loop into cheap,
   debuggable steps. `valid` means it builds into a solid — NOT that it is
   manifold/watertight or manufacturable.
3. **Position parts relative to each other, not by guessed coordinates.** Raw
   `Location(x, y, z)` guesses are the top cause of parts that look close but
   aren't mated. Use the positioning helpers — `centered_on`, `offset_from`,
   `coaxial(part, ref, axis=)` (shaft-in-bore), `stack_on(part, ref, gap=)` (cover
   on housing) — so parts mate by construction, then verify with the matching
   `cad.define_mate` predicate (`concentric` / `coincident`).
4. **Commit incrementally so the user watches it assemble.** First part with
   `mode="replace"`, then `mode="append"` (building on `previous_result`) for each
   subsequent part; fix or swap a single part with `cad.replace_part` /
   `cad.remove_part` instead of rewriting the whole script. Read `regression_diff`
   after each edit — `internal_feature_change` flags a bore/hole/pocket edit that
   changed volume without moving the bounding box (it is a real change, not a no-op).
5. **Self-correct from `geometry_report` between steps** — `floating_parts` means
   a part didn't connect (usually a coordinate typo); symmetry issues mean a
   left/right pair is off. Fix before adding the next part.

6. **Record the assembly structure (optional, when relationships matter).** A
   `Compound(children=[...])` with `.label`ed parts is only a *visual* assembly.
   To make the parts and their relationships first-class, author the Assembly IR:
   - `cad.define_part { geometry_ref: "<label>", role }` for each part (links to
     the named CAD solid and verifies the ref).
   - `cad.define_interface { part_id, semantic_role, face_ids }` to bind a part to
     specific B-Rep faces (`@face:*` from `agent_context` / the brep graph) — this
     is what makes a mate *geometric*.
   - `cad.define_mate { connection_type, part_a, part_b, interface_a, interface_b }`
     for each connection (`rigid_tie` / `bonded` / `bolted_proxy` / `welded_proxy`
     / `contact_proxy` / `spring_proxy`). A mate to an undefined part is refused;
     proxy connections always carry honest limitations. When it references
     interfaces, the response carries a resolved `connection_geometry` verdict
     (`plausible` / `warning` / `invalid`) — read it to catch parts that don't
     actually touch where you mated them. Add a `mate_predicate` (`concentric` /
     `tangent` / `coincident` / `clearance`, with `mate_tolerance_mm`) to verify
     the engineering relationship — e.g. `tangent` flags gear pitch circles that
     don't mesh, `concentric` flags a shaft not coaxial with its bore. A violated
     predicate marks the connection `invalid`.

Honesty: the Assembly IR records parts and **proxy** connections — it is
representation + validation only. It models **no** contact mechanics, **no** bolt
preload, and runs **no** solver, so do not claim kinematic validity, fit,
interference-free assembly, or load capacity from the IR (or from CAD geometry)
alone.

## Standard parts (bd_warehouse)

For standard mechanical parts — fasteners, nuts, washers, bearings, gears, threads,
pipes, flanges — prefer the **bd_warehouse** library over approximating with
`Cylinder`/`Box`. It gives ISO/DIN/ANSI-compliant dimensions and semantically real
parts (a screw, not a cylinder). It is pre-installed and the modules are pre-bound
in the `cad.execute_build123d` namespace — no import line needed:

```python
# Pre-bound module aliases: fastener, bearing, gear, thread, pipe, flange, sprocket
screw = fastener.SocketHeadCapScrew("M6-1", length=12, simple=True)
screw.label = "mounting_bolt_M6"          # keep labels semantic + canonical
brg = bearing.SingleRowDeepGrooveBallBearing("608", bearing_type="SKT")
result = Compound(children=[screw, brg])
```

You may also `from bd_warehouse.fastener import SocketHeadCapScrew` explicitly.

**Clearance / tapped holes — pass a Fastener OBJECT, never a size string.**
`ClearanceHole` / `TapHole` / `InsertHole` take the actual fastener instance as
their `fastener=` argument (so they can look up the correct drill diameter), plus
a `fit` of `"Close"` / `"Normal"` / `"Loose"`. Passing a string like
`fastener="M6"` raises `AttributeError: 'str' object has no attribute
'clearance_hole_diameters'`. Build them inside the part so they cut the bolt
pattern:
```python
with BuildPart() as bp:
    Box(80, 60, 8, align=(Align.CENTER, Align.CENTER, Align.MIN))
    screw = fastener.SocketHeadCapScrew(size="M6-1", length=16, simple=True)
    with Locations((30, 20, 8), (-30, 20, 8), (30, -20, 8), (-30, -20, 8)):
        fastener.ClearanceHole(fastener=screw, fit="Normal")   # object, not "M6"
    result = bp.part
```
If you only need the hole (no fastener semantics), a plain `Hole(radius=...)` is
fine — but it will not carry `standard_part` ISO designation in the feature graph.

- Use `simple=True` on threaded fasteners unless real thread geometry is required
  (real threads add many faces → larger STEP/STL and slower viewer load).
- Label standard parts with semantic roles (`screw`, `bolt`, `washer`, `bearing`,
  `gear`, `flange`) even though the runner now records best-effort
  `bd_warehouse` provenance automatically. Recognized standard parts become
  `standard_part` feature-graph entries, remain available in `named_parts`, and
  carry source library, canonical type, designation, detection method, and
  confidence when known.
- Standard-part faces are pickable through the B-Rep pointer pipeline. A picked
  face may include conservative hints such as `head_top`, `head_side`,
  `shank_side`, `bearing_face`, or `washer_face`; do not treat those hints as
  preload, contact, thread engagement, or solver evidence.
- Gears: only spur gears are covered. Springs/cams/worms are not — hand-build those.

## Hard rules

- **Repair-loop contract for high-risk builds.** Before presenting a high-risk
  build as done — a multi-part / assembly / product model, any nonzero
  floating/spatial/symmetry issue, a `crude` fidelity level, a build with a
  reference image, or an explicit "accurate representation of a real X" request —
  run `cad.diagnose` and repair every `blocking_issue` (via the approval-gated
  edit path) until `verdict == "ready"`. Do not report such a build complete while
  `cad.diagnose` returns `needs_repair`.
- Respect `[APPROVAL REQUIRED]` tools; never bypass or hide approval boundaries.
- If `AIENG_MCP_BLOCK_APPROVAL_TOOLS=1` is active, gated CAD tools will be refused by the MCP server; report that and stop.
- Do not claim strength, safety factor, manufacturability, meshability, or simulation correctness from CAD generation alone.
- Do not read `aieng/src/` to infer live workbench capabilities; use MCP tool returns and `aieng.agent_readme`.
- For visible products/characters/vehicles, prefer loft/sweep/revolve/fillet helpers over primitive box stacking.
- For engineering parts, use canonical labels such as `base_plate`, `mounting_hole`, `rib`, `boss`, `flange`, and `interface_face`.

## Response contract

Report: tool sequence, key assumptions, parts created/changed, approval status, evidence inspected, and remaining limitations.
