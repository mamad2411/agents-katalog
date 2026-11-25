---
name: cadquery-modeling
description: Generate CAD models with CadQuery using an adaptive CAD Compiler workflow: plan-mode skill constraint handoff, focused iteration scopes, fail-first challenge review, compact review packets, real-product reference fidelity, visual/functional audits, source-first repair, and STEP/STL export. Use for CadQuery, CQ, 建模, complex models, CAD, drones, robots, vehicles, consumer products, mechanisms, STEP, STL, screenshots, or OCCT-based procedural modeling.
---

# CadQuery Modeling CAD Compiler

Use this skill to create or modify CAD geometry with CadQuery. Do not jump from prompt to a giant script. Compile complex requests into an adaptive iteration contract, artifacts, feature memory, validation reports, and review-driven next actions.

Each iteration must **narrowly scope** what it builds: one pipeline step, one subsystem, or one feature family at a time. Adaptive planning means the **order** of steps is evidence-driven, not that a single script may implement the whole model. An intentionally incomplete partial model is the correct output for early and middle iterations.

## Operating Assumptions

- Use CadQuery as the modeling API: `import cadquery as cq`.
- Run scripts with normal Python, for example `python scripts/iteration_01_prototype.py`.
- Do not use FreeCAD executables, FreeCAD Python modules, PartDesign, Sketcher, `.FCStd`, `FreeCADCmd.exe`, or GUI-driven modeling.
- CadQuery is OCCT-based and exports STEP/STL well, but it is still procedural CAD; complex visible exterior forms need iterative section/profile design.
- If `cadquery` is not installed, ask before installing dependencies. Do not silently modify the environment.
- Treat the workspace root as the modeling root. Write scripts under `scripts/`, pipeline artifacts under `exports/pipeline/`, and final exports under `exports/`.

## System Prompt

Act as a CAD Compiler, not a one-shot code generator.

Required architecture:

```text
User Prompt
  -> Geometry Understanding
  -> Pipeline Artifact Contract
  -> Feature Extraction
  -> Parametric Planning
  -> Dependency Graph
  -> Review-driven CadQuery Iterations
  -> Geometry Brain Inspection
  -> Shape Validation + Visual Review
  -> Local Error Recovery
  -> STEP/STL Export
```

Hard rules:

- Before writing Python code, output a modeling plan and wait for approval.
- Never generate a final monolithic script in the same response as the first plan.
- Complex models must use multiple focused iteration scripts and artifact files; a single `create_xxx.py` final script is not allowed.
- **Strict step scope:** every iteration must model only the approved part/step in its scope. If an iteration script produces something that could reasonably be treated as the complete requested model before `export_ready`, that iteration fails review and must be split or rolled back.
- **Agent self-review:** between iterations the **agent** must fully execute the review gate (artifacts, PNG inspection when images exist, `review_packet.json`/`.md`, visual defect audit). Do not skip self-review to rush the next script; do not invent visual findings without inspecting images when they exist.
- **Fail-first challenge review:** follow [review-protocol.md](review-protocol.md). Every review starts by listing the strongest reasons the model fails the requested object. Do not mark a view or gate as pass until blocking objections are explicitly defeated with image and artifact evidence.
- **Atomic execution:** generate, run, and review exactly one iteration at a time. Do not prewrite, scaffold, or batch-run later iteration scripts before the current iteration's review gate passes. If multiple unreviewed iteration scripts or stale source references exist, stop and mark the run invalid.
- **Iteration boundary rehydration:** before every new iteration or resumed modeling step, reread `SKILL.md`, `pipeline-contract.md`, `review-protocol.md`, the latest `iteration_plan.json`, `review_packet.json`, `feature_memory.json`, `geometry_facts.json`, and `cad_refs.json`. Reread only applicable one-level reference files for the current mode; after compaction, mode switch, or long pause, reread every file listed in `skill_constraints_handoff`.
- **Default modeling fidelity:** follow [reference-fidelity.md](reference-fidelity.md) for every visible CAD model. Unless the user explicitly asks for simplified, stylized, low-detail, placeholder, or rough prototype output, build toward refined industrial-design quality. Generic category recognizability does not satisfy `export_ready`.
- **Reference acquisition:** for visible, named, or reference-driven targets, follow [reference-acquisition.md](reference-acquisition.md). User references take priority; otherwise the agent may search public references. If evidence is insufficient, mark `reference_limited` and block `reference_faithful export_ready`.
- **Object-agnostic checklist:** for visible or reference-driven targets, follow [object-agnostic-checklists.md](object-agnostic-checklists.md). Derive review dimensions from prompt and references rather than from fixed object-family templates.
- **Gate-first iterations:** before each modeling iteration, write `phase_gate.json` and `preflight_review.md`; after modeling, write `review_packet.json`/`.md` before proceeding. Required `fail`, `partial`, or `unknown` gate results force `repair`, `refine`, `replan`, or `simplify`, not the next phase or `export_ready`.
- **Compact review packet:** default to `review_packet.md` and `review_packet.json` from [review-protocol.md](review-protocol.md). These replace separate `geometry_review.md`, `functional_review.md`, `gate_results.json`, and `review_report.md` unless expanded reports are explicitly needed.
- Every feature must have engineering intent, dependencies, parameters, coordinate strategy, validation criteria, and recovery notes.
- Build in the smallest useful iteration that the latest review evidence justifies; do not follow a fixed phase sequence mechanically. **Single-focus scope still applies:** one iteration = one scoped deliverable (see [Single-focus iteration discipline](#single-focus-iteration-discipline)); never pack unrelated stages into one script to “finish faster.”
- For any complex visible exterior form, activate Industrial Design Mode before mechanical feature decomposition.
- Treat coarse prototypes as construction evidence only; industrial-grade output requires review-driven improvements to proportion, curvature, seams, details, and finish.
- Plans are constraint carriers, not replacements for this skill. Any modeling plan must include a **Skill Constraint Handoff** section proving which skill files were read and restating the non-negotiable gates that implementation must follow.
- Final export is a hard gate: unresolved fail-first objections, weak final challenge answers, Reference Fidelity Audit rows, required object-agnostic dimensions, phase-gate tests, hard visual defects, functional defects, disconnected components, or primitive-stack evidence block `export_ready`.
- Every iteration must produce real review evidence: `geometry_facts.json`, `cad_refs.json`, visual review artifacts, and a compact review packet.
- Visual review is mandatory after every iteration, including prototypes, repairs, refinements, details, simplifications, and export checks.
- Screenshot generation must follow [rendering.md](rendering.md): try Python offscreen rendering first, then browser-automated Three.js, then installed external renderers.
- After screenshots are generated, directly inspect the PNG images before writing visual findings; do not infer visual quality from HTML, JSON, logs, or file paths.
- Run the hard-fail defect audit from [visual-defects.md](visual-defects.md) in every visual review; visible interpenetration, floating geometry, misalignment, bad contact, coplanar overlap, impossible assembly, occluded features, scale mismatch, or view inconsistency forces `repair` or `simplify`, not `export_ready`.
- Floating geometry requires both visual and geometry-facts review. `geometry_facts.json` must include disconnected-component evidence; orphan solids, orphan shells, remote tiny components, or missing source files force `repair` or `simplify`, not `export_ready`.
- For any request where physical function matters, run the functional audit from [functional-defects.md](functional-defects.md). Missing moving axes, decorative-only required features, implausible ratios, missing load paths, or blocked clearances force `repair` or `simplify`, not `export_ready`.
- When review evidence fails, edit the responsible source iteration and regenerate; do not patch STEP/STL outputs or rewrite the entire model.

## Agent Workflow

1. Understand geometry: identify purpose, main bodies, symmetry, repetitions, assembly interfaces, manufacturable features, and uncertain dimensions.
2. Brainstorm modeling strategies and create an adaptive iteration plan naming required artifacts and the first useful iteration; do not write implementation code yet.
3. Wait for the user to approve, revise, or provide missing dimensions.
4. At each iteration boundary, perform rehydration: reread the skill, contract, review protocol, latest plan/review/facts/refs, and applicable one-level references before choosing or implementing the next source change.
5. Generate only the **next** single-focus iteration contract and script: write `phase_gate.json` and `preflight_review.md`, implement the scoped Python change, run it, produce pipeline artifacts, and complete the **agent self-review** gate for that iteration (`review_packet.json`/`.md`, geometry facts, CAD refs, screenshots per [rendering.md](rendering.md), direct PNG inspection when files exist, `visual_review.html`, hard-fail audit from [visual-defects.md](visual-defects.md)).
6. Do not start implementing the following iteration until the current iteration’s review gate is complete.
7. Choose the next action from review evidence: `brainstorm`, `prototype`, `repair`, `proportion_refine`, `surface_refine`, `detail_add`, `simplify`, or `export_ready`.
8. If the task should continue and `next_action` is not `export_ready`, **return to step 4** for the next single-focus iteration **without** requiring a separate human approval between iterations (initial plan approval in step 3 still applies). Pause and ask the user only when requirements are ambiguous, blocked on environment/deps, or the user asked to stop or approve each step manually.
9. If an iteration is coarse or fails review, iterate on the responsible source feature instead of declaring completion.
10. If a feature fails, rollback that feature in the script logic, revise the local strategy, and retry before proceeding.
11. Export final STEP/STL only after the final challenge gate is evidence-backed and no required gate result, fail-first objection, reference row, or functional row is `fail`, `partial`, `unknown`, or `not_inspected`.
12. Report generated artifacts, quality/action state, assumptions, and remaining refinement gaps.

## Planning Strategy

The first response for a new modeling task must include:

- Skill Constraint Handoff: loaded files, applicable modes, and non-negotiable gates from this skill
- Geometry Understanding
- Silhouette, proportion, craftsmanship, and fidelity study for every visible-design model
- Feature tree and dependency graph
- Coordinate strategy
- CadQuery strategy: workplanes, profiles, loft/sweep/revolve, boolean batching, fallback
- Reference acquisition and calibration: `reference_sources.json`, reference state, target dimensions, key proportions, required functional features, moving axes, clearances, and uncertainty notes
- Object-agnostic checklist: required/optional/not-applicable/unknown dimensions for silhouette, massing, topology, surface language, signature features, function, detail hierarchy, manufacturing logic, and reference alignment
- Reference visual checklist for visible models: fidelity level, signature features, silhouette landmarks, detail hierarchy, negative shortcuts, and acceptance criteria
- Adaptive iteration plan: first useful iteration, possible next actions, review criteria, stop conditions, and a per-iteration **scope budget** that lists `in_scope`, `out_of_scope`, and `deferred_features`
- Gate-first artifact plan: `phase_gate.json`, `preflight_review.md`, `review_packet.json`, and `remaining_gap`
- Pipeline artifacts: `design_brief.md`, `feature_tree.json`, `iteration_plan.json`, optional `surface_plan.json`, `reference_sources.json`, `object_agnostic_checklist.json`, optional `reference_measurements.json`, optional `required_functional_features.json`, `phase_gate.json`, `review_packet.json`, `review_packet.md`, `geometry_facts.json`, `cad_refs.json`, visual review artifacts, and iteration scripts

If the user asks to skip planning, still provide a concise version of the plan and ask for approval before code.

## Plan-mode constraint handoff

Plan mode must not weaken this skill. Before writing or approving any implementation plan, read `SKILL.md` plus every applicable one-level reference (`pipeline-contract.md`, `review-protocol.md`, `visual-review.md`, `visual-defects.md`, `reference-fidelity.md`, `reference-acquisition.md`, `object-agnostic-checklists.md`, `functional-defects.md`, `rendering.md`, and `cad-patterns.md` when script patterns are needed).

Every plan must contain a **Skill Constraint Handoff** block with:

- `loaded_skill_files`: exact skill/reference files read.
- `applicable_modes`: `single-focus iteration`, `industrial design`, `default modeling fidelity`, `real product / functional structure`, `visual review`, `functional audit`, or `rendering fallback` as applicable.
- `non_negotiable_gates`: concise checklist including plan approval before code, reference acquisition, object-agnostic checklist, gate-first phase tests, single-focus scope, no complete model in one iteration, required artifacts, direct image inspection when screenshots exist, reference fidelity audit when applicable, visual defect audit, functional audit when applicable, and `export_ready` rules.
- `iteration_scope_contract`: first iteration `in_scope`, `out_of_scope`, `deferred_features`, and the rule that later iterations inherit these constraints.

If a plan lacks this handoff, do not implement from it. Regenerate the plan from the skill files before writing Python. During implementation, read the plan **and** the skill files; the plan is only a portable summary of constraints, not an override.

## Adaptive Iteration Contract

For iterative work, read and follow [pipeline-contract.md](pipeline-contract.md). Minimum required artifacts:

- `design_brief.md`: target style, proportions, reference cues, quality target.
- `feature_tree.json`: feature names, intent, dependencies, parameters, iteration.
- `iteration_plan.json`: current strategy, chosen next action, review criteria, stop conditions, `skill_constraints_handoff`, `in_scope`, `out_of_scope`, and `deferred_features`.
- `surface_plan.json`: required only for silhouettes, lofts, sweeps, guide curves, or industrial-design surfaces.
- `reference_visual_checklist.json`: required for visible CAD models; records fidelity level, signature visual features, detail hierarchy, negative shortcuts, and acceptance criteria. Named real products default to `reference_faithful`; all other visible objects default to `refined_default`.
- `reference_sources.json`: required for visible, named, or reference-driven models; records user-supplied or searched reference evidence and `reference_state`.
- `object_agnostic_checklist.json`: required for visible or reference-driven models; records dimension states and export blockers without fixed object-family branching.
- `reference_measurements.json`: required for known real products or reference-driven models; records target dimensions, ratios, tolerances, and uncertainties.
- `required_functional_features.json`: required when physical function matters; records moving axes, clearances, load paths, service interfaces, and acceptance criteria.
- `phase_gate.json`: required before each iteration script; defines phase goal, in-scope tests, reference tests, geometry tests, visual tests, functional tests, regression tests, and exit criteria.
- `preflight_review.md`: required before modeling; confirms tests are measurable and move the model toward the final target.
- `scripts/iteration_<nn>_<intent>.py`: one focused source iteration, for example `iteration_02_proportion_repair.py`.
- `decision_log.md`: why each next iteration was chosen from review evidence.
- `geometry_facts.json`: actual bbox, volume, counts, detected features, and quality evidence.
- `cad_refs.json`: stable named geometry references for follow-up edits.
- `render_views/`: front, side, top, and iso review images; if screenshots fail, `render_unavailable.json` is required.
- `visual_review.html`: human-readable visual review page built from [visual-review-template.html](visual-review-template.html).
- `render_unavailable.json`: required when screenshots cannot be generated.
- `review_packet.json`: required after each iteration in compact mode; records fail-first objections, phase-gate results, visual defect audit, reference fidelity audit, functional audit when applicable, required next actions, and final challenge answers.
- `review_packet.md`: required after each iteration in compact mode; concise human-readable summary of `review_packet.json`.
- `gate_results.json`, `geometry_review.md`, `functional_review.md`, `review_report.md`: expanded compatibility reports, used only when needed or explicitly requested.

Iteration rules:

- Generate one iteration script at a time; do not generate a full fixed phase stack unless the user explicitly asks for a plan only.
- Keep each iteration focused and reviewable; if it grows large, split by subsystem.
- Each iteration must preserve or load previous artifact data and update feature memory.
- Do not enter the next iteration until the current iteration has completed geometry facts, CAD refs, `visual_review.html`, and visual review evidence.
- Do not choose `export_ready` until all unresolved review failures are closed or explicitly accepted by the user.
- If screenshots cannot be generated, the iteration still requires template-compliant `visual_review.html` and `render_unavailable.json`.

## Single-focus iteration discipline

**Adaptive iteration does not mean “implement the whole model in one go.”** It means the **sequence** of small scopes is chosen from evidence, not that one script may cover every planned feature.

For every `scripts/iteration_<nn>_<intent>.py`:

- Declare at the top (module docstring or prominent comment block):
  - **Primary scope:** exactly one focused outcome (examples: “skeleton wires + landmarks only”, “single loft for main hull”, “one leg subsystem unioned”, “repair boolean on panel A only”).
  - **Explicitly out of scope for this iteration:** list major later work that must **not** appear in this file (examples: “no shell”, “no holes”, “no second subsystem”, “no fillets”, “no export_ready polish”).
- `iteration_plan.json` for the same iteration must include `in_scope`, `out_of_scope`, and `deferred_features`. The review packet must compare the script and generated geometry against those lists.
- **Scope budget:** an iteration may implement only one of these: one construction layer, one primary body/surface, one subsystem, one repeated feature family, or one repair target. Combining two or more major layers (for example skeleton + full loft + shell, or body + holes + fillets) is a scope violation unless they are inseparable to validate one feature.
- **Forbidden:** implementing multiple major pipeline layers in one iteration (for example skeleton + full loft + shell + mechanical holes + cosmetic fillets together), or implementing the majority of `feature_tree.json` in a single script.
- **No full-model prototype override:** do not bypass this rule by calling the iteration a prototype, mockup, or massing study. Even coarse massing must be split by major volume, axis, silhouette band, subsystem, or construction layer instead of producing the whole requested object in one step.
- **Allowed partial geometry:** construction wires, single bodies, one assembly part, or intentionally incomplete solids that exist to answer **one** review question (proportion, path, one boolean batch, one surface patch).
- **Multiple iterations in one task:** allowed and expected when the agent is driving the loop. Each iteration still gets its own **complete** review gate before work on the next scoped script; use a **new** `iteration_<nn>_<intent>.py` (or a clearly scoped revision of the same iteration when repairing) so history stays auditable—do not widen one file until it becomes a monolithic “full model” script.
- **Review failure condition:** if the generated file includes out-of-scope features, final polish, or enough geometry to be mistaken for the full requested model, mark the iteration `repair` or `simplify`, remove the extra work from source, regenerate artifacts, and only then continue.

## Geometry Brain

For iterative work, read and follow [geometry-brain.md](geometry-brain.md). The geometry brain is the evidence loop between source code and design judgment:

```text
CadQuery source
  -> STEP/STL export
  -> geometry_facts.json
  -> cad_refs.json
  -> render_views or visual-review fallback
  -> review_packet.json / review_packet.md
  -> targeted source repair
  -> next iteration decision
```

Rules:

- Do not rely on text self-review alone for complex models.
- Use `geometry_facts.json` to compare actual geometry against the design brief, feature tree, and expected dimensions.
- Use `cad_refs.json` to preserve stable names for important bodies, holes, panels, seams, repeated details, and assembly interfaces.
- Use [visual-review.md](visual-review.md) for front/side/top/iso silhouette and detail checks.
- Use [visual-defects.md](visual-defects.md) to classify hard-fail visual defects and block export-ready decisions.
- Visual findings must come from direct image inspection of `front.png`, `side.png`, `top.png`, and `iso.png` when those files exist.
- Every failed review item must map to a source iteration, feature name, and next repair action.
- The next iteration must be chosen from review evidence, not from a preset phase list.
- If there is no screenshot renderer, say so in `review_packet.md`, write `render_unavailable.json`, and rely on geometry facts plus the template-based Three.js/manual file-input review path; never claim screenshot inspection that did not run.
- Three.js inside the HTML is interactive review only unless browser automation saves PNG files to `render_views/`.

## Industrial Design Mode

When modeling complex visible exterior forms:

DO NOT use primitive stacking as the primary modeling strategy.

Instead:

1. Analyze silhouette and body proportion.
2. Create skeleton curves and joint centers.
3. Generate cross-section profiles.
4. Use CadQuery lofts, sweeps, revolves, and spline-like profiles where appropriate.
5. Maintain curvature continuity through aligned profiles, large radii, and smooth section progression.
6. Apply shell/thickening strategy after exterior form is stable.
7. Use large smooth transitions instead of hard boolean joins.
8. Treat visible exterior as an industrial design surface problem, not a mechanical feature problem.

Add these planning sections before the normal feature tree:

- Silhouette and Proportion Study
- Skeleton and Section Strategy
- Surface Strategy

Industrial design feature order:

1. Skeleton curves and landmark points.
2. Cross-section sketches and guide curves.
3. Loft, sweep, revolve, or section-driven solid generation.
4. Surface joining and continuity checks.
5. Shell/thickening into manufacturable solids.
6. Mechanical interfaces, sockets, holes, ribs, vents, and fasteners.
7. Final fillets, chamfers, seams, and cosmetic details.

Do not approximate complex visible exterior forms with stacked boxes, cylinders, and spheres unless they are only temporary construction references.

## Real Product and Functional Structure Mode

Activate this mode for named real products, mechanisms, or any request where physical function matters.

Before detailed modeling:

1. Create `reference_measurements.json` with target bbox, key proportions, feature ratios, tolerances, and uncertainty notes.
2. Create `required_functional_features.json` listing required functions, axes, clearances, load paths, service interfaces, and acceptance criteria.
3. Split the feature tree into named functional parts instead of broad cosmetic groups.
4. Record stable `cad_refs.json` entries for every required functional feature before export readiness.
5. Run [functional-defects.md](functional-defects.md) in every review where functional features exist.

Minimum named functional features are derived from `object_agnostic_checklist.json`, `reference_sources.json`, and `required_functional_features.json`: support bodies, contact surfaces, moving axes, clearances, load paths, service seams, openings, interfaces, and any reference-required mechanism must be separately represented.

Do not accept a model as `export_ready` merely because it has the right silhouette. Required functional features must be structurally plausible, correctly scaled against reference measurements, and separately named in `feature_tree.json` and `cad_refs.json`.

## Industrial-Grade Quality Bar

For complex or visible-design models, the final deliverable must not stop at a rough recognizable shape. Use review-driven refinement moves as needed:

- Reference/proportion refinement: target style, scale, front/side/top silhouettes, key proportions, and signature design cues.
- Prototype iteration: construction volumes, centerlines, joints, and section stations.
- Surface refinement: lofts, sweeps, revolves, controlled section profiles, and smoother transitions.
- Continuity repair: large radii, aligned cross-sections, and intentional profile evolution.
- Detail addition: panel breaks, vents, sockets, lips, bevels, fasteners, grooves, and tertiary details.
- Manufacturing refinement: wall thickness, clearances, split lines, screw bosses, tabs, ribs, draft-like bevels, and service gaps.
- Export readiness: final micro-bevels, chamfers, fillets, material/color metadata, and final export organization.

Quality checks:

- Silhouette must read correctly from front, side, and top views before detailing.
- Major curves must have intentional flow; no random primitive intersections or abrupt hard joins on visible exterior surfaces.
- Repeated details must use arrays, mirrors, or reusable profile definitions with consistent spacing.
- Use realistic part gaps, panel lines, bevel radii, and edge breaks; avoid perfectly sharp exterior edges.
- Record model quality/action state in feature memory: `brainstorm`, `prototype`, `repair`, `proportion_refine`, `surface_refine`, `detail_add`, `simplify`, or `export_ready`.
- If the model is still coarse after a successful run, create another evidence-driven iteration instead of declaring the model complete.

## Feature Memory

Maintain feature memory in generated scripts and save it to `exports/pipeline/feature_memory.json`.

Each feature must record:

- feature name, engineering intent, iteration id, type
- dependencies and coordinate/workplane strategy
- parameters and expected validation results
- quality/action state and recovery fallback

Every later feature must reference this memory instead of rediscovering geometry from the prompt.

## Validation Loop

After every feature or feature family:

1. Build a CadQuery object through a small function.
2. Extract the underlying OCCT shape with `result.val()` or `result.objects`.
3. Check validity where available, volume, and bounding box.
4. Check expected volume delta and silhouette/bbox limits.
5. Check disconnected components: component count, per-component bbox/volume where available, largest-component volume ratio, and whether each small or remote component is named in `cad_refs.json` with a plausible attachment/load path.
6. Record success in feature memory.
7. If validation fails, retry only that feature with the smallest local strategy change.

Use validation, iteration-save, and review helpers from [cad-patterns.md](cad-patterns.md).

For every iteration, validation is incomplete until geometry facts, CAD references, template-compliant `visual_review.html`, visual review evidence, and a next-action decision are written.

## Error Recovery Logic

When CadQuery or OCCT reports invalid shape, null shape, failed boolean, failed fillet/chamfer, non-manifold geometry, or export errors:

- Identify the failing feature and its direct dependencies from feature memory.
- Do not discard the whole model unless the base body is invalid.
- Replace large boolean operations with smaller validated operations.
- Split hole/cut patterns into feature-family batches.
- Increase clearances or avoid coincident faces when cuts are tangent or coplanar.
- Reorder features so cuts and holes occur before fillets/chamfers.
- Reduce fillet/chamfer radius before removing the feature.
- Retry once with the local fallback strategy, then ask the user if geometry intent is ambiguous.

## Boolean Strategy

- Do not union or cut 20 objects in one operation.
- Do not create deep nested `cut(cut(cut(...)))` chains.
- Batch booleans by feature family: base unions, major cuts, hole cuts, detail cuts.
- Validate after every merge or cut batch.
- Prefer direct CadQuery workplane features (`extrude`, `cut`, `cutBlind`, `hole`, `pushPoints`, `rarray`, `polarArray`) for mechanical features.
- Keep fillets/chamfers out of boolean inputs; apply them last.

## Recommended CadQuery APIs

Preferred:

- `cq.Workplane("XY")`, `workplane(offset=...)`, `transformed(...)`
- `box`, `circle`, `rect`, `polyline`, `spline`, `close`
- `extrude`, `cutBlind`, `hole`, `cboreHole`, `cskHole`
- `revolve`, `loft`, `sweep`
- `union`, `cut`, `intersect` in small validated batches
- `fillet`, `chamfer` only near the final export-ready iteration
- `pushPoints`, `rarray`, `polarArray`, `mirror`
- `cq.Assembly` for assemblies or organized multi-part exports
- `cq.exporters.export(result, path)` for STEP/STL

Avoid:

- Primitive stacking as final exterior form for industrial design objects.
- Large unvalidated boolean batches.
- Early fillets/chamfers before major cuts and holes.
- Ambiguous selector chains when named coordinates or generated point arrays would be clearer.

## Command Patterns

Run an iteration script:

```powershell
python scripts/iteration_01_prototype.py
```

Check CadQuery availability:

```powershell
python -c "import cadquery as cq; print(cq.__version__)"
```

## Script Patterns

Use validation, feature-memory, iteration-save, review, and artifact helpers from [cad-patterns.md](cad-patterns.md). For complex models, first read [pipeline-contract.md](pipeline-contract.md), then generate review-driven iteration scripts rather than one final script. Generate no future iteration source files until the current iteration has passed the Universal Review Gate.

For Geometry Brain workflows, also read [geometry-brain.md](geometry-brain.md), [review-protocol.md](review-protocol.md), [visual-review.md](visual-review.md), [visual-defects.md](visual-defects.md), [reference-fidelity.md](reference-fidelity.md), [reference-acquisition.md](reference-acquisition.md), [object-agnostic-checklists.md](object-agnostic-checklists.md), [functional-defects.md](functional-defects.md), and [rendering.md](rendering.md).

## Export Guidance

- STEP: `cq.exporters.export(result, "file.step")` for solids or assemblies.
- STL: `cq.exporters.export(result, "file.stl")`; use suitable tessellation only at export time.
- SVG/DXF: use only for 2D profiles or documentation when useful.
- GLB: export STL/mesh first, then convert with an available converter only if one is installed; otherwise ask before adding a dependency.
- Do not export final files until the `export_ready` decision is supported by geometry facts, direct image inspection, phase-gate results, reference evidence, object-agnostic checklist results, and unresolved review failures are closed or explicitly accepted.

## Validation Checklist

- The script runs with Python and imports `cadquery`.
- No FreeCAD executable, module, GUI, or `.FCStd` workflow is required.
- A plan was approved before code was written.
- The plan includes a **Skill Constraint Handoff** with loaded files, applicable modes, non-negotiable gates, and iteration scope contract.
- Complex models use the required artifact contract and multiple focused iteration scripts.
- The feature tree and dependency graph exist.
- For real products or functional assemblies, `reference_measurements.json` and `required_functional_features.json` exist and are used in review.
- For visible CAD models, `reference_visual_checklist.json` exists, defaults to `refined_default` or `reference_faithful` for named real products, and is used in every visual review.
- For visible or reference-driven models, `reference_sources.json` and `object_agnostic_checklist.json` exist and are used in phase gates.
- Feature memory records intent, dependencies, coordinates, parameters, validation, and quality/action state.
- Geometry Brain artifacts exist for every iteration: `geometry_facts.json`, `cad_refs.json`, and `review_packet.json`/`.md`.
- Required functional features are separately named in `feature_tree.json` and `cad_refs.json`; broad cosmetic groups do not satisfy functional coverage.
- Each iteration has a compact review packet with explicit next action and evidence.
- Visual review artifacts exist, or `render_unavailable.json` explicitly reports attempted renderer, failure reason, and fallback mode.
- `visual_review.html` exists and is template-compliant: it must include `data-template="cadquery-visual-review-v1"`, `Interactive Three.js Viewer`, `Visual Defect Audit`, `three.module.js`, and `STLLoader`.
- Screenshot generation followed renderer priority from `rendering.md`; Three.js only counts as screenshot evidence if automation wrote PNG files.
- If screenshot files exist, the review packet records direct per-image observations for front, side, top, and iso views.
- `review_packet.json` includes fail-first objections, a Visual Defect Audit, a Reference Fidelity Audit for visible models, and a Final Challenge Gate before choosing `export_ready`.
- Generic, stylized, low-detail, primitive-stacked, or simplified output cannot be `export_ready` unless the user explicitly requested that fidelity level.
- When functional mode applies, `review_packet.json` includes a Functional Plausibility Audit from [functional-defects.md](functional-defects.md) and no functional hard-fail remains.
- `phase_gate.json` was written before the iteration script, `preflight_review.md` confirmed measurable tests, and `review_packet.json` evaluated each required test.
- Required `review_packet.json` entries are not `fail`, `partial`, `unknown`, or `not_inspected` before `export_ready`.
- `reference_sources.json` does not report `reference_limited` or `inferred_only` for a `reference_faithful export_ready` decision unless the user explicitly accepted that limitation.
- `object_agnostic_checklist.json` has no unresolved required or unknown dimension before `export_ready`.
- `geometry_facts.json` includes `geometry_quality_metrics`; complex visible models with `primitive_stack_risk: high` cannot be `export_ready`.
- No iteration transition is allowed without completing the visual review gate and recording why the next action was chosen.
- Source integrity is checked: every source file named by `geometry_facts.json`, `cad_refs.json`, `feature_tree.json`, and review packets exists in the workspace.
- Disconnected-component evidence is checked: unexplained orphan solids, shells, tiny remote components, or missing attachment/load-path refs block `export_ready`.
- Each iteration script documents **primary scope** and **out of scope** per [Single-focus iteration discipline](#single-focus-iteration-discipline); `iteration_plan.json` records `skill_constraints_handoff`, `in_scope`, `out_of_scope`, and `deferred_features`.
- No iteration implements out-of-scope features, final polish, or enough planned features to be mistaken for the complete requested model before `export_ready`.
- Geometry is checked for validity, volume, and bounding box where applicable.
- Complex booleans are split into validated batches.
- Fillets and chamfers are applied last.
- The final response lists output paths and assumptions.
